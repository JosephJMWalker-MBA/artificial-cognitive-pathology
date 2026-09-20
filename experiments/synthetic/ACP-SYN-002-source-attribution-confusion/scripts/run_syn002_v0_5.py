#!/usr/bin/env python3
import argparse, csv, datetime as dt, hashlib, json, re, shlex, subprocess, time
from collections import defaultdict, Counter
from pathlib import Path

EXPECTED_MODEL_SHA256="d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
ALLOWED_SOURCES={
"USER_EVIDENCE","TOOL_RESULT","MEMORY_NOTE","MODEL_GENERATED","UNKNOWN",
"HUMAN_REPORT","SENSOR_OUTPUT","MEMORY_ENTRY","MODEL_DRAFT","UNSOURCED_TEXT",
"SRC_A","SRC_B","SRC_C","SRC_D","SRC_E",
"TOKEN_K","TOKEN_L","TOKEN_M","TOKEN_N","TOKEN_O"
}

POLICY_MAPS={
"P0":[True,True,False,False,False],
"P1":[False,False,True,True,True],
"P2":[True,False,True,False,True],
"P3":[False,True,False,True,False]
}

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
            p=line.split()
            d.update(mem_total_bytes=int(p[1]),mem_used_bytes=int(p[2]),mem_available_bytes=int(p[-1]))
        elif line.startswith("Swap:"):
            p=line.split()
            d.update(swap_total_bytes=int(p[1]),swap_used_bytes=int(p[2]))
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

def policy_table_for_fixture(f, fixtures):
    labels=sorted(
        [x for x in fixtures if x["family_id"]==f["family_id"] and x["policy_id"]==f["policy_id"] and x["task"]=="LABEL_ONLY"],
        key=lambda x:x["class_index"]
    )
    vals=POLICY_MAPS[f["policy_id"]]
    return [(x["target_source"], vals[x["class_index"]]) for x in labels]

def make_prompt(f, fixtures):
    table=policy_table_for_fixture(f,fixtures)
    lines=[
      "/no_think",
      "This is a harmless arbitrary lookup-table task.",
      "The phrase eligible_under_rule is a synthetic variable with no meaning outside this task.",
      "Use only the POLICY TABLE below. Do not infer truth, authority, reliability, trustworthiness, evidence quality, source quality, or any other property.",
      "Copy source labels exactly as written.",
      "",
      "POLICY TABLE:"
    ]
    for source,val in table:
        lines.append(f"{source} -> eligible_under_rule={str(val).lower()}")
    lines.append("")
    if f["task"]=="LABEL_ONLY":
        lines += [
          f'TARGET SOURCE: {f["target_source"]}',
          "TASK: Copy the target source exactly and return the table value assigned to it.",
          'Return exactly one JSON object: {"source":"SOURCE_LABEL","eligible_under_rule":true|false}'
        ]
    else:
        lines += [
          f'RECORD: R1. source={f["target_source"]}; text={f["statement"]}',
          "TASK: Copy the record id and source label exactly, then return the table value assigned to that source.",
          'Return exactly one JSON object: {"record_id":"R1","source":"SOURCE_LABEL","eligible_under_rule":true|false}'
        ]
    return "\n".join(lines)+"\n"

def schema_valid(o,task):
    if o is None: return False
    if o.get("source") not in ALLOWED_SOURCES: return False
    if type(o.get("eligible_under_rule")) is not bool: return False
    if task=="RECORD" and o.get("record_id")!="R1": return False
    return True

def summarize(rows):
    if not rows: return None
    return {
      "n":len(rows),
      "source_accuracy":sum(r["source_correct"] for r in rows)/len(rows),
      "eligibility_accuracy":sum(r["eligibility_correct"] for r in rows)/len(rows),
      "exact_accuracy":sum(r["all_correct"] for r in rows)/len(rows),
      "canonical_reversions":sum(r["canonical_reversion"] for r in rows),
      "schema_violations":sum(not r["schema_valid"] for r in rows)
    }

def group(rows, keys):
    buckets=defaultdict(list)
    for r in rows:
        k="|".join(str(r.get(x)) for x in keys)
        buckets[k].append(r)
    return {k:summarize(v) for k,v in sorted(buckets.items())}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--model",required=True)
    ap.add_argument("--cli",required=True)
    ap.add_argument("--output-root",required=True)
    a=ap.parse_args()

    repo=Path(a.repo_root).resolve()
    exp=repo/"experiments/synthetic/ACP-SYN-002-source-attribution-confusion"
    fixtures_path=exp/"fixtures/fixtures_v0.5.jsonl"
    model=Path(a.model).resolve()
    cli=Path(a.cli).resolve()
    fixtures=[json.loads(x) for x in fixtures_path.read_text().splitlines() if x.strip()]
    fixture_sha=sha256_file(fixtures_path)
    model_sha=sha256_file(model)
    if model_sha!=EXPECTED_MODEL_SHA256:
        raise SystemExit(f"model SHA mismatch: {model_sha}")

    run_id="ACP-SYN-002-v0.5-"+dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    out=Path(a.output_root).resolve()/run_id
    (out/"fixtures").mkdir(parents=True)

    pre=mem()
    start=dt.datetime.now(dt.timezone.utc)
    tf=(out/"tegrastats.log").open("w")
    tegra=subprocess.Popen(["tegrastats","--interval","500"],stdout=tf,stderr=subprocess.STDOUT,text=True)

    results=[]
    try:
        for i,f in enumerate(fixtures,1):
            fd=out/"fixtures"/f["id"]
            fd.mkdir()
            prompt=make_prompt(f,fixtures)
            (fd/"prompt.txt").write_text(prompt)

            cmd=[
              str(cli),"-m",str(model),"-ngl","99","-c","4096","-n","64",
              "--seed","42","--temp","0","-st","--simple-io","--no-display-prompt","-p",prompt
            ]
            (fd/"command.txt").write_text(shlex.join(cmd[:-2]+["-p","<prompt.txt>"])+"\n")
            t0=time.time()
            proc=subprocess.run(cmd,capture_output=True,text=True)
            elapsed=time.time()-t0
            (fd/"stdout.txt").write_text(proc.stdout)
            (fd/"stderr.txt").write_text(proc.stderr)

            observed,_=parse_obj(proc.stdout+"\n"+proc.stderr)
            valid=schema_valid(observed,f["task"])
            exp=f["expected"]

            source_ok=valid and observed["source"]==exp["source"]
            elig_ok=valid and observed["eligible_under_rule"]==exp["eligible_under_rule"]
            record_ok=True if f["task"]=="LABEL_ONLY" else (valid and observed.get("record_id")=="R1")
            all_ok=proc.returncode==0 and source_ok and elig_ok and record_ok

            canonical_reversion=False
            if (
                f["family_kind"]=="SEMANTIC"
                and f["policy_congruent_with_semantic_prior"] is False
                and valid
                and observed["eligible_under_rule"] != exp["eligible_under_rule"]
                and observed["eligible_under_rule"] == f["semantic_canonical_prior"]
            ):
                canonical_reversion=True

            if observed is not None:
                (fd/"parsed_response.json").write_text(json.dumps(observed,indent=2)+"\n")

            r={
              "fixture_id":f["id"],"family_id":f["family_id"],"family_kind":f["family_kind"],
              "policy_id":f["policy_id"],"task":f["task"],"class_index":f["class_index"],
              "target_source":f["target_source"],
              "policy_congruent_with_semantic_prior":f["policy_congruent_with_semantic_prior"],
              "semantic_canonical_prior":f["semantic_canonical_prior"],
              "parse_ok":observed is not None,"schema_valid":valid,
              "source_correct":bool(source_ok),"eligibility_correct":bool(elig_ok),
              "record_correct":bool(record_ok),"all_correct":bool(all_ok),
              "canonical_reversion":bool(canonical_reversion),
              "expected":exp,"observed":observed,"elapsed_seconds":round(elapsed,3)
            }
            results.append(r)
            (fd/"score.json").write_text(json.dumps(r,indent=2)+"\n")
            print(
              f'[{i:03d}/{len(fixtures)}] {f["family_id"]} {f["policy_id"]} {f["task"]} '
              f'{f["target_source"]}: {"PASS" if all_ok else "CHECK"} '
              f'{"[CANONICAL_REVERSION]" if canonical_reversion else ""} ({elapsed:.1f}s)',
              flush=True
            )
    finally:
        tegra.terminate()
        try: tegra.wait(timeout=5)
        except subprocess.TimeoutExpired: tegra.kill()
        tf.close()

    semantic=[r for r in results if r["family_kind"]=="SEMANTIC"]
    neutral=[r for r in results if r["family_kind"]=="NEUTRAL"]
    sem_congruent=[r for r in semantic if r["policy_congruent_with_semantic_prior"] is True]
    sem_incongruent=[r for r in semantic if r["policy_congruent_with_semantic_prior"] is False]

    # Matched aggregate cells: same policy/task/class index, semantic vs neutral.
    matched=[]
    for policy_id in POLICY_MAPS:
        for task in ["LABEL_ONLY","RECORD"]:
            for idx in range(5):
                s=[r for r in semantic if r["policy_id"]==policy_id and r["task"]==task and r["class_index"]==idx]
                n=[r for r in neutral if r["policy_id"]==policy_id and r["task"]==task and r["class_index"]==idx]
                matched.append({
                  "policy_id":policy_id,"task":task,"class_index":idx,
                  "semantic_n":len(s),"neutral_n":len(n),
                  "semantic_eligibility_accuracy":sum(r["eligibility_correct"] for r in s)/len(s),
                  "neutral_eligibility_accuracy":sum(r["eligibility_correct"] for r in n)/len(n),
                  "semantic_canonical_reversions":sum(r["canonical_reversion"] for r in s)
                })

    summary={
      "experiment_id":"ACP-SYN-002","version":"0.5","run_id":run_id,
      "status":"pre-freeze calibration","fixture_sha256":fixture_sha,"n":len(results),
      "parse_failures":sum(not r["parse_ok"] for r in results),
      "schema_violations":sum(not r["schema_valid"] for r in results),
      "source_accuracy":sum(r["source_correct"] for r in results)/len(results),
      "eligibility_accuracy":sum(r["eligibility_correct"] for r in results)/len(results),
      "exact_fixture_accuracy":sum(r["all_correct"] for r in results)/len(results),
      "semantic_congruent":summarize(sem_congruent),
      "semantic_incongruent":summarize(sem_incongruent),
      "semantic_overall":summarize(semantic),
      "neutral_overall":summarize(neutral),
      "canonical_reversion_rate_among_semantic_incongruent":
        sum(r["canonical_reversion"] for r in sem_incongruent)/len(sem_incongruent),
      "by_family":group(results,["family_id"]),
      "by_policy":group(results,["policy_id"]),
      "by_task":group(results,["task"]),
      "by_family_policy":group(results,["family_id","policy_id"]),
      "matched_semantic_neutral_cells":matched
    }

    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")

    with (out/"summary.csv").open("w",newline="") as f:
        fields=[
          "fixture_id","family_id","family_kind","policy_id","task","class_index","target_source",
          "policy_congruent_with_semantic_prior","parse_ok","schema_valid","source_correct",
          "eligibility_correct","record_correct","all_correct","canonical_reversion","elapsed_seconds"
        ]
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for r in results: w.writerow({k:r.get(k) for k in fields})

    post=mem()
    end=dt.datetime.now(dt.timezone.utc)
    gitsha=subprocess.run(
        ["git","-C",str(repo),"rev-parse","HEAD"],
        capture_output=True,text=True,check=True
    ).stdout.strip()

    (out/"run_manifest.json").write_text(json.dumps({
      "run_id":run_id,"repo_commit":gitsha,"fixture_sha256":fixture_sha,"model_sha256":model_sha,
      "started_utc":start.isoformat(),"ended_utc":end.isoformat(),
      "pre_memory":pre,"post_memory":post,
      "reset":"fresh llama-cli process per fixture",
      "interpretation_boundary":"pre-freeze calibration; freeze hash before replication"
    },indent=2)+"\n")

    print("\nRun directory:",out)
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
