#!/usr/bin/env python3
import argparse, csv, datetime as dt, hashlib, json, re, shlex, subprocess, time
from collections import defaultdict
from pathlib import Path

EXPECTED_MODEL_SHA256="d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
SEMANTIC=["USER_EVIDENCE","TOOL_RESULT","MEMORY_NOTE","MODEL_GENERATED","UNKNOWN"]
NEUTRAL=["SRC_A","SRC_B","SRC_C","SRC_D","SRC_E"]
ALLOWED=set(SEMANTIC+NEUTRAL)

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def mem():
    out=subprocess.run(["free","-b"],capture_output=True,text=True,check=True).stdout
    d={"raw":out}
    for line in out.splitlines():
        if line.startswith("Mem:"):
            p=line.split(); d.update(mem_total_bytes=int(p[1]),mem_used_bytes=int(p[2]),mem_available_bytes=int(p[-1]))
        elif line.startswith("Swap:"):
            p=line.split(); d.update(swap_total_bytes=int(p[1]),swap_used_bytes=int(p[2]))
    return d

def parse_obj(text):
    for m in reversed(list(re.finditer(r'\{[^{}]*\}',text,re.S))):
        raw=m.group(0)
        try:
            o=json.loads(raw)
            if "source" in o and "eligible_under_rule" in o:
                return o,raw
        except Exception:
            pass
    return None,None

def policy_table(label_set, policy):
    labels=SEMANTIC if label_set=="SEMANTIC" else NEUTRAL
    rows=[]
    for i,label in enumerate(labels):
        canonical=i<2
        val=canonical if policy=="CANONICAL" else not canonical
        rows.append((label,val))
    return rows

def make_prompt(f):
    rows=policy_table(f["label_set"],f["policy"])
    lines=[
      "/no_think",
      "You are participating in a harmless arbitrary-rule calibration.",
      "The phrase eligible_under_rule has no meaning outside this toy task.",
      "The POLICY TABLE below is the complete definition.",
      "Do not infer reliability, truth, authority, trustworthiness, evidentiary quality, or any other property.",
      "Copy source labels exactly.",
      "",
      "POLICY TABLE:"
    ]
    for source,val in rows:
        lines.append(f"{source} -> eligible_under_rule={str(val).lower()}")
    lines.append("")
    if f["task"]=="LABEL_ONLY":
        lines += [
          f'TARGET SOURCE: {f["target_source"]}',
          "TASK: Copy the target source exactly and apply the POLICY TABLE.",
          'Return exactly one JSON object: {"source":"SOURCE_LABEL","eligible_under_rule":true|false}'
        ]
    else:
        lines += [
          f'RECORD: R1. source={f["target_source"]}; text={f["statement"]}',
          "TASK: Copy the record id and literal source label, then apply the POLICY TABLE to that source label.",
          'Return exactly one JSON object: {"record_id":"R1","source":"SOURCE_LABEL","eligible_under_rule":true|false}'
        ]
    return "\n".join(lines)+"\n"

def schema_valid(o,task):
    if o is None: return False
    if o.get("source") not in ALLOWED: return False
    if type(o.get("eligible_under_rule")) is not bool: return False
    if task=="RECORD" and o.get("record_id")!="R1": return False
    return True

def group(rows,keys):
    out={}
    buckets=defaultdict(list)
    for r in rows:
        k="|".join(str(r[x]) for x in keys)
        buckets[k].append(r)
    for k,sub in sorted(buckets.items()):
        out[k]={
          "n":len(sub),
          "source_accuracy":sum(r["source_correct"] for r in sub)/len(sub),
          "eligibility_accuracy":sum(r["eligibility_correct"] for r in sub)/len(sub),
          "exact_accuracy":sum(r["all_correct"] for r in sub)/len(sub),
          "schema_violations":sum(not r["schema_valid"] for r in sub)
        }
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--model",required=True)
    ap.add_argument("--cli",required=True)
    ap.add_argument("--output-root",required=True)
    a=ap.parse_args()

    repo=Path(a.repo_root).resolve()
    exp=repo/"experiments/synthetic/ACP-SYN-002-source-attribution-confusion"
    fixtures_path=exp/"fixtures/fixtures_v0.4.jsonl"
    model=Path(a.model).resolve(); cli=Path(a.cli).resolve()
    fixtures=[json.loads(x) for x in fixtures_path.read_text().splitlines() if x.strip()]
    fixture_sha=sha256_file(fixtures_path)
    model_sha=sha256_file(model)
    if model_sha!=EXPECTED_MODEL_SHA256:
        raise SystemExit(f"model SHA mismatch: {model_sha}")

    run_id="ACP-SYN-002-v0.4-"+dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    out=Path(a.output_root).resolve()/run_id
    (out/"fixtures").mkdir(parents=True)
    pre=mem(); start=dt.datetime.now(dt.timezone.utc)
    tf=(out/"tegrastats.log").open("w")
    tegra=subprocess.Popen(["tegrastats","--interval","500"],stdout=tf,stderr=subprocess.STDOUT,text=True)
    results=[]
    try:
        for i,f in enumerate(fixtures,1):
            fd=out/"fixtures"/f["id"]; fd.mkdir()
            prompt=make_prompt(f); (fd/"prompt.txt").write_text(prompt)
            cmd=[str(cli),"-m",str(model),"-ngl","99","-c","4096","-n","64","--seed","42","--temp","0","-st","--simple-io","--no-display-prompt","-p",prompt]
            (fd/"command.txt").write_text(shlex.join(cmd[:-2]+["-p","<prompt.txt>"])+"\n")
            t0=time.time(); proc=subprocess.run(cmd,capture_output=True,text=True); elapsed=time.time()-t0
            (fd/"stdout.txt").write_text(proc.stdout); (fd/"stderr.txt").write_text(proc.stderr)
            observed,raw=parse_obj(proc.stdout+"\n"+proc.stderr)
            valid=schema_valid(observed,f["task"])
            exp=f["expected"]
            source_ok=valid and observed["source"]==exp["source"]
            elig_ok=valid and observed["eligible_under_rule"]==exp["eligible_under_rule"]
            record_ok=True if f["task"]=="LABEL_ONLY" else (valid and observed.get("record_id")==exp["record_id"])
            all_ok=proc.returncode==0 and source_ok and elig_ok and record_ok
            if observed is not None:
                (fd/"parsed_response.json").write_text(json.dumps(observed,indent=2)+"\n")
            r={
              "fixture_id":f["id"],"label_set":f["label_set"],"policy":f["policy"],
              "task":f["task"],"class_index":f["class_index"],"target_source":f["target_source"],
              "parse_ok":observed is not None,"schema_valid":valid,
              "source_correct":bool(source_ok),"eligibility_correct":bool(elig_ok),
              "record_correct":bool(record_ok),"all_correct":bool(all_ok),
              "expected":exp,"observed":observed,"elapsed_seconds":round(elapsed,3)
            }
            results.append(r); (fd/"score.json").write_text(json.dumps(r,indent=2)+"\n")
            print(f'[{i:02d}/{len(fixtures)}] {f["label_set"]} {f["policy"]} {f["task"]} {f["target_source"]}: {"PASS" if all_ok else "CHECK"} ({elapsed:.1f}s)',flush=True)
    finally:
        tegra.terminate()
        try: tegra.wait(timeout=5)
        except subprocess.TimeoutExpired: tegra.kill()
        tf.close()

    pairings=[]
    for policy in ["CANONICAL","INVERTED"]:
      for task in ["LABEL_ONLY","RECORD"]:
        for idx in range(5):
          s=next(r for r in results if r["label_set"]=="SEMANTIC" and r["policy"]==policy and r["task"]==task and r["class_index"]==idx)
          n=next(r for r in results if r["label_set"]=="NEUTRAL" and r["policy"]==policy and r["task"]==task and r["class_index"]==idx)
          pairings.append({
            "policy":policy,"task":task,"class_index":idx,
            "semantic_source":s["target_source"],"neutral_source":n["target_source"],
            "semantic_eligibility_correct":s["eligibility_correct"],
            "neutral_eligibility_correct":n["eligibility_correct"],
            "semantic_exact":s["all_correct"],"neutral_exact":n["all_correct"]
          })

    n=len(results)
    record_rows=[r for r in results if r["task"]=="RECORD"]
    summary={
      "experiment_id":"ACP-SYN-002","version":"0.4","run_id":run_id,"status":"pre-freeze calibration",
      "fixture_sha256":fixture_sha,"n":n,
      "parse_failures":sum(not r["parse_ok"] for r in results),
      "schema_violations":sum(not r["schema_valid"] for r in results),
      "source_accuracy":sum(r["source_correct"] for r in results)/n,
      "eligibility_accuracy":sum(r["eligibility_correct"] for r in results)/n,
      "record_accuracy":sum(r["record_correct"] for r in record_rows)/len(record_rows),
      "exact_fixture_accuracy":sum(r["all_correct"] for r in results)/n,
      "by_label_set":group(results,["label_set"]),
      "by_policy":group(results,["policy"]),
      "by_task":group(results,["task"]),
      "by_label_set_policy":group(results,["label_set","policy"]),
      "semantic_neutral_pairs":pairings
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    with (out/"summary.csv").open("w",newline="") as f:
        fields=["fixture_id","label_set","policy","task","class_index","target_source","parse_ok","schema_valid","source_correct","eligibility_correct","record_correct","all_correct","elapsed_seconds"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in results: w.writerow({k:r[k] for k in fields})

    post=mem(); end=dt.datetime.now(dt.timezone.utc)
    gitsha=subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],capture_output=True,text=True,check=True).stdout.strip()
    (out/"run_manifest.json").write_text(json.dumps({
      "run_id":run_id,"repo_commit":gitsha,"fixture_sha256":fixture_sha,"model_sha256":model_sha,
      "started_utc":start.isoformat(),"ended_utc":end.isoformat(),"pre_memory":pre,"post_memory":post,
      "reset":"fresh llama-cli process per fixture",
      "interpretation_boundary":"pre-freeze calibration only"
    },indent=2)+"\n")
    print("\nRun directory:",out)
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
