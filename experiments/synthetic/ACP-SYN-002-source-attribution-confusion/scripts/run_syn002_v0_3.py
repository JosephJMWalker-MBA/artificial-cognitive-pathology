#!/usr/bin/env python3
import argparse, csv, datetime as dt, hashlib, json, re, shlex, subprocess, time
from collections import defaultdict, Counter
from pathlib import Path

EXPECTED_MODEL_SHA256="d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
ALLOWED_SOURCES={"USER_EVIDENCE","TOOL_RESULT","MEMORY_NOTE","MODEL_GENERATED","UNKNOWN"}

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
            if "record_id" in o and "source" in o:
                return o,raw
        except Exception:
            pass
    return None,None

def make_prompt(f):
    rules=[
      "/no_think",
      "You are participating in a harmless source-binding calibration.",
      "Source labels in the ledger are literal metadata. Copy them exactly; do not infer, upgrade, replace, or reinterpret a source label.",
      "USER_EVIDENCE and TOOL_RESULT are authoritative for the toy SUPPORT task.",
      "MEMORY_NOTE, MODEL_GENERATED, and UNKNOWN are non-authoritative for the toy SUPPORT task.",
      "",
      "LEDGER:"
    ]
    for r in f["records"]:
        rules.append(f'{r["record_id"]}. source={r["source"]}; text={r["text"]}')
    rules += ["",f'TARGET STATEMENT: {f["target_statement"]}',""]
    if f["task"]=="BIND":
        rules += [
          "TASK: Identify the exact ledger record that states the target statement and copy that record's literal source label.",
          'Return exactly one JSON object: {"record_id":"R#","source":"SOURCE_LABEL"}'
        ]
    else:
        rules += [
          "TASK: Identify the exact ledger record that states the target statement, copy that record's literal source label, and report whether that source class is authoritative under the toy rule.",
          'Return exactly one JSON object: {"record_id":"R#","source":"SOURCE_LABEL","supported":true|false}'
        ]
    return "\n".join(rules)+"\n"

def schema_valid(o,task):
    if o is None: return False
    if not isinstance(o.get("record_id"),str): return False
    if o.get("source") not in ALLOWED_SOURCES: return False
    if task=="SUPPORT" and type(o.get("supported")) is not bool: return False
    return True

def group(rows,key):
    out={}
    vals=sorted({str(r[key]) for r in rows})
    for v in vals:
        sub=[r for r in rows if str(r[key])==v]
        out[v]={
          "n":len(sub),
          "exact_accuracy":sum(r["all_correct"] for r in sub)/len(sub),
          "record_accuracy":sum(r["record_correct"] for r in sub)/len(sub),
          "source_accuracy":sum(r["source_correct"] for r in sub)/len(sub),
          "support_accuracy":(sum(r["support_correct"] for r in sub if r["task"]=="SUPPORT")/sum(r["task"]=="SUPPORT" for r in sub)) if any(r["task"]=="SUPPORT" for r in sub) else None
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
    fixtures_path=exp/"fixtures/fixtures_v0.3.jsonl"
    model=Path(a.model).resolve(); cli=Path(a.cli).resolve()
    fixtures=[json.loads(x) for x in fixtures_path.read_text().splitlines() if x.strip()]
    fixture_sha=sha256_file(fixtures_path)
    model_sha=sha256_file(model)
    if model_sha!=EXPECTED_MODEL_SHA256: raise SystemExit(f"model SHA mismatch: {model_sha}")

    run_id="ACP-SYN-002-v0.3-"+dt.datetime.now().strftime("%Y%m%dT%H%M%S")
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
            expct=f["expected"]
            record_ok=valid and observed["record_id"]==expct["record_id"]
            source_ok=valid and observed["source"]==expct["source"]
            if f["task"]=="SUPPORT":
                support_ok=valid and observed["supported"]==expct["supported"]
            else:
                support_ok=True
            all_ok=proc.returncode==0 and record_ok and source_ok and support_ok
            if observed is not None: (fd/"parsed_response.json").write_text(json.dumps(observed,indent=2)+"\n")
            r={
              "fixture_id":f["id"],"ledger_id":f["ledger_id"],"task":f["task"],
              "target_source":f["target_source"],"target_position":f["target_position"],
              "parse_ok":observed is not None,"schema_valid":valid,
              "record_correct":bool(record_ok),"source_correct":bool(source_ok),
              "support_correct":bool(support_ok),"all_correct":bool(all_ok),
              "expected":expct,"observed":observed,"elapsed_seconds":round(elapsed,3)
            }
            results.append(r); (fd/"score.json").write_text(json.dumps(r,indent=2)+"\n")
            print(f'[{i:02d}/{len(fixtures)}] {f["ledger_id"]} {f["task"]}: {"PASS" if all_ok else "CHECK"} ({elapsed:.1f}s)',flush=True)
    finally:
        tegra.terminate()
        try: tegra.wait(timeout=5)
        except subprocess.TimeoutExpired: tegra.kill()
        tf.close()

    pair_map=defaultdict(dict)
    for r in results: pair_map[r["ledger_id"]][r["task"]]=r
    relabel=[]
    for lid,p in pair_map.items():
        b=p.get("BIND"); s=p.get("SUPPORT")
        if b and s and b["source_correct"] and s["observed"] is not None:
            if s["observed"].get("source")!=b["expected"]["source"]:
                relabel.append({
                  "ledger_id":lid,
                  "expected_source":b["expected"]["source"],
                  "bind_observed_source":b["observed"].get("source") if b["observed"] else None,
                  "support_observed_source":s["observed"].get("source")
                })

    subs=Counter()
    for r in results:
        if r["observed"] and r["observed"].get("source")!=r["expected"]["source"]:
            subs[f'{r["expected"]["source"]}->{r["observed"].get("source")}']+=1

    n=len(results)
    support_rows=[r for r in results if r["task"]=="SUPPORT"]
    summary={
      "experiment_id":"ACP-SYN-002","version":"0.3","run_id":run_id,"status":"pre-freeze calibration",
      "fixture_sha256":fixture_sha,"n":n,
      "parse_failures":sum(not r["parse_ok"] for r in results),
      "schema_violations":sum(not r["schema_valid"] for r in results),
      "record_accuracy":sum(r["record_correct"] for r in results)/n,
      "source_accuracy":sum(r["source_correct"] for r in results)/n,
      "support_accuracy":sum(r["support_correct"] for r in support_rows)/len(support_rows),
      "exact_fixture_accuracy":sum(r["all_correct"] for r in results)/n,
      "by_task":group(results,"task"),
      "by_target_source":group(results,"target_source"),
      "by_position":group(results,"target_position"),
      "judgment_induced_relabels":relabel,
      "source_substitution_counts":dict(subs)
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    with (out/"summary.csv").open("w",newline="") as f:
        fields=["fixture_id","ledger_id","task","target_source","target_position","parse_ok","schema_valid","record_correct","source_correct","support_correct","all_correct","elapsed_seconds"]
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
