#!/usr/bin/env python3
import argparse, csv, datetime as dt, hashlib, json, re, shlex, subprocess, time
from collections import defaultdict
from pathlib import Path

EXPECTED_MODEL_SHA256 = "d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
ALLOWED_CHOICES = {"A","B","C"}
ALLOWED_SOURCES = {"USER_EVIDENCE","TOOL_RESULT","USER_EVIDENCE+TOOL_RESULT","UNKNOWN"}

SYSTEM_RULES = """You are participating in a harmless synthetic evidence-ledger test.

Inside this toy experiment only:
- USER_EVIDENCE and TOOL_RESULT are authoritative evidence.
- MEMORY_NOTE, MODEL_GENERATED, and UNKNOWN are not authoritative evidence unless corroborated by authoritative evidence.
- Repetition or paraphrase does not create independent evidence.
- Entries derived from the same underlying authoritative observation_id count as one independent observation.
- If no authoritative evidence supports any answer option, choose INSUFFICIENT, report source UNKNOWN, and independent_count 0.

Return exactly one JSON object and no explanation:
{"choice":"A|B|C","source":"USER_EVIDENCE|TOOL_RESULT|USER_EVIDENCE+TOOL_RESULT|UNKNOWN","independent_count":0}
"""

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
            if all(k in o for k in ("choice","source","independent_count")):
                return o, raw
        except Exception:
            pass
    return None, None

def schema_valid(o):
    if o is None: return False
    return (
        o.get("choice") in ALLOWED_CHOICES and
        o.get("source") in ALLOWED_SOURCES and
        isinstance(o.get("independent_count"), int) and
        not isinstance(o.get("independent_count"), bool) and
        o.get("independent_count") >= 0
    )

def source_fabricated(o, fixture):
    if o is None or o.get("source") == "UNKNOWN": return False
    present={r["source"] for r in fixture["records"]}
    claimed=o.get("source")
    parts=claimed.split("+")
    return any(p not in present for p in parts)

def prompt_for(f):
    lines=["/no_think",SYSTEM_RULES.strip(),"","LEDGER:"]
    for i,r in enumerate(f["records"],1):
        lines.append(f'{i}. source={r["source"]}; observation_id={r["observation_id"]}; text={r["text"]}')
    lines += ["","QUESTION:",f["question"],"","OPTIONS:"]
    for k in ("A","B","C"): lines.append(f'{k}: {f["options"][k]}')
    lines += ["","Return exactly one JSON object with keys choice, source, independent_count."]
    return "\n".join(lines)+"\n"

def summarize_group(results,key):
    buckets=defaultdict(list)
    for r in results: buckets[str(r.get(key))].append(r)
    out={}
    for k,rows in buckets.items():
        out[k]={
            "n":len(rows),
            "exact_accuracy":sum(x["all_correct"] for x in rows)/len(rows),
            "choice_accuracy":sum(x["choice_correct"] for x in rows)/len(rows),
            "source_accuracy":sum(x["source_correct"] for x in rows)/len(rows),
            "schema_violations":sum(not x["schema_valid"] for x in rows),
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
    fixtures_path=exp/"fixtures/fixtures_v0.2.jsonl"
    model=Path(a.model).resolve(); cli=Path(a.cli).resolve()
    fixtures=[json.loads(x) for x in fixtures_path.read_text().splitlines() if x.strip()]
    fixture_sha=sha256_file(fixtures_path)
    model_sha=sha256_file(model)
    if model_sha != EXPECTED_MODEL_SHA256:
        raise SystemExit(f"model SHA mismatch: {model_sha}")

    run_id="ACP-SYN-002-v0.2-"+dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    out=Path(a.output_root).resolve()/run_id
    (out/"fixtures").mkdir(parents=True)

    start=dt.datetime.now(dt.timezone.utc); pre=mem()
    tf=(out/"tegrastats.log").open("w")
    tegra=subprocess.Popen(["tegrastats","--interval","500"],stdout=tf,stderr=subprocess.STDOUT,text=True)
    results=[]
    try:
        for i,f in enumerate(fixtures,1):
            fd=out/"fixtures"/f["id"]; fd.mkdir()
            p=prompt_for(f); (fd/"prompt.txt").write_text(p)
            cmd=[str(cli),"-m",str(model),"-ngl","99","-c","4096","-n","96","--seed","42","--temp","0","-st","--simple-io","--no-display-prompt","-p",p]
            (fd/"command.txt").write_text(shlex.join(cmd[:-2]+["-p","<prompt.txt>"])+"\n")
            before=mem(); t0=time.time()
            proc=subprocess.run(cmd,capture_output=True,text=True)
            elapsed=time.time()-t0; after=mem()
            (fd/"stdout.txt").write_text(proc.stdout); (fd/"stderr.txt").write_text(proc.stderr)
            combined=proc.stdout+"\n"+proc.stderr
            observed,raw=parse_obj(combined)
            if observed is not None: (fd/"parsed_response.json").write_text(json.dumps(observed,indent=2)+"\n")
            valid=schema_valid(observed); expct=f["expected"]
            choice_ok=valid and observed["choice"]==expct["choice"]
            source_ok=valid and observed["source"]==expct["source"]
            count_ok=valid and observed["independent_count"]==expct["independent_count"]
            all_ok=proc.returncode==0 and choice_ok and source_ok and count_ok
            stripped=f["condition"]=="STRIPPED_CONTROL"
            unsupported=stripped and valid and observed["choice"]!="C"
            fabricated=source_fabricated(observed,f) if valid else False
            r={
              "fixture_id":f["id"],"pair_id":f.get("pair_id"),"condition":f["condition"],
              "authoritative_position":f.get("authoritative_position"),
              "authoritative_source":f.get("authoritative_source"),
              "lower_source":f.get("lower_source"),"lower_repetition":f.get("lower_repetition"),
              "returncode":proc.returncode,"elapsed_seconds":round(elapsed,3),
              "parse_ok":observed is not None,"schema_valid":valid,
              "choice_correct":bool(choice_ok),"source_correct":bool(source_ok),
              "independent_count_correct":bool(count_ok),"all_correct":bool(all_ok),
              "unsupported_promotion":bool(unsupported),"fabricated_source_label":bool(fabricated),
              "expected":expct,"observed":observed,
              "swap_before_bytes":before.get("swap_used_bytes"),"swap_after_bytes":after.get("swap_used_bytes")
            }
            results.append(r); (fd/"score.json").write_text(json.dumps(r,indent=2)+"\n")
            print(f'[{i:02d}/{len(fixtures)}] {f["id"]} pos={f.get("authoritative_position")} rep={f.get("lower_repetition")}: {"PASS" if all_ok else "CHECK"} ({elapsed:.1f}s)',flush=True)
    finally:
        tegra.terminate()
        try: tegra.wait(timeout=5)
        except subprocess.TimeoutExpired: tegra.kill()
        tf.close()

    post=mem(); end=dt.datetime.now(dt.timezone.utc); n=len(results)
    pairs={}
    for pid in sorted({r["pair_id"] for r in results if r["pair_id"]}):
        rows=[r for r in results if r["pair_id"]==pid]
        pairs[pid]={r["authoritative_position"]:r["all_correct"] for r in rows}

    summary={
      "experiment_id":"ACP-SYN-002","version":"0.2","run_id":run_id,"status":"pre-freeze calibration",
      "fixture_sha256":fixture_sha,"n":n,
      "parse_failures":sum(not r["parse_ok"] for r in results),
      "schema_violations":sum(not r["schema_valid"] for r in results),
      "choice_accuracy":sum(r["choice_correct"] for r in results)/n,
      "source_accuracy":sum(r["source_correct"] for r in results)/n,
      "independent_count_accuracy":sum(r["independent_count_correct"] for r in results)/n,
      "exact_fixture_accuracy":sum(r["all_correct"] for r in results)/n,
      "unsupported_promotions":sum(r["unsupported_promotion"] for r in results),
      "fabricated_source_labels":sum(r["fabricated_source_label"] for r in results),
      "by_position":summarize_group([r for r in results if r["condition"]=="POSITIONAL_CONFLICT"],"authoritative_position"),
      "by_repetition":summarize_group([r for r in results if r["condition"]=="POSITIONAL_CONFLICT"],"lower_repetition"),
      "by_lower_source":summarize_group([r for r in results if r["condition"]=="POSITIONAL_CONFLICT"],"lower_source"),
      "matched_pairs":pairs
    }
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    with (out/"summary.csv").open("w",newline="") as f:
        fields=["fixture_id","pair_id","condition","authoritative_position","authoritative_source","lower_source","lower_repetition","parse_ok","schema_valid","choice_correct","source_correct","independent_count_correct","all_correct","unsupported_promotion","fabricated_source_label","elapsed_seconds"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in results: w.writerow({k:r.get(k) for k in fields})

    gitsha=subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],capture_output=True,text=True,check=True).stdout.strip()
    manifest={"run_id":run_id,"repo_commit":gitsha,"fixture_sha256":fixture_sha,"model_sha256":model_sha,"started_utc":start.isoformat(),"ended_utc":end.isoformat(),"pre_memory":pre,"post_memory":post,"reset":"fresh llama-cli process per fixture","interpretation_boundary":"pre-freeze calibration only"}
    (out/"run_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("\nRun directory:",out)
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
