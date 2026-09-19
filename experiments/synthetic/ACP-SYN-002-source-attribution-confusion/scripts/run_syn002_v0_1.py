#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import shlex
import subprocess
import time
from pathlib import Path

EXPECTED_MODEL_SHA256 = "d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
EXPECTED_RUNTIME_COMMIT = "d1d3c3396aa13a5f239109a822666c4870490ad5"

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

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def memory_snapshot() -> dict:
    out = subprocess.run(["free", "-b"], capture_output=True, text=True, check=True).stdout
    snap = {"raw": out}
    for line in out.splitlines():
        if line.startswith("Mem:"):
            p = line.split()
            snap["mem_total_bytes"] = int(p[1])
            snap["mem_used_bytes"] = int(p[2])
            snap["mem_available_bytes"] = int(p[-1])
        elif line.startswith("Swap:"):
            p = line.split()
            snap["swap_total_bytes"] = int(p[1])
            snap["swap_used_bytes"] = int(p[2])
    return snap

def parse_json_object(text: str):
    candidates = re.findall(r'\{[^{}\n]*"choice"[^{}\n]*\}', text)
    for raw in reversed(candidates):
        try:
            obj = json.loads(raw)
            if all(k in obj for k in ("choice", "source", "independent_count")):
                return obj, raw
        except json.JSONDecodeError:
            pass
    for m in reversed(list(re.finditer(r'\{[^{}]*\}', text, flags=re.S))):
        raw = m.group(0)
        try:
            obj = json.loads(raw)
            if all(k in obj for k in ("choice", "source", "independent_count")):
                return obj, raw
        except json.JSONDecodeError:
            continue
    return None, None

def make_prompt(fixture: dict) -> str:
    lines = ["/no_think", SYSTEM_RULES.strip(), "", "LEDGER:"]
    for idx, rec in enumerate(fixture["records"], start=1):
        lines.append(
            f'{idx}. source={rec["source"]}; observation_id={rec["observation_id"]}; text={rec["text"]}'
        )
    lines += ["", "QUESTION:", fixture["question"], "", "OPTIONS:"]
    for k in ("A", "B", "C"):
        lines.append(f'{k}: {fixture["options"][k]}')
    lines += ["", "Return exactly one JSON object with keys choice, source, independent_count."]
    return "\n".join(lines) + "\n"

def run_cmd(args, **kwargs):
    return subprocess.run(args, **kwargs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--cli", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--skip-model-hash", action="store_true")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    exp_dir = repo_root / "experiments/synthetic/ACP-SYN-002-source-attribution-confusion"
    fixture_path = exp_dir / "fixtures/fixtures_v0.1.jsonl"
    manifest_path = exp_dir / "manifests/fixture_manifest_v0.1.json"
    model = Path(args.model).resolve()
    cli = Path(args.cli).resolve()
    output_root = Path(args.output_root).resolve()

    if not fixture_path.exists():
        raise SystemExit(f"fixture file not found: {fixture_path}")
    if not manifest_path.exists():
        raise SystemExit(f"manifest not found: {manifest_path}")
    if not model.exists():
        raise SystemExit(f"model not found: {model}")
    if not cli.exists():
        raise SystemExit(f"llama-cli not found: {cli}")

    fixture_manifest = json.loads(manifest_path.read_text())
    actual_fixture_sha = sha256_file(fixture_path)
    if actual_fixture_sha != fixture_manifest["fixture_sha256"]:
        raise SystemExit(
            f"fixture SHA mismatch: expected {fixture_manifest['fixture_sha256']} got {actual_fixture_sha}"
        )

    if not args.skip_model_hash:
        actual_model_sha = sha256_file(model)
        if actual_model_sha != EXPECTED_MODEL_SHA256:
            raise SystemExit(
                f"model SHA mismatch: expected {EXPECTED_MODEL_SHA256} got {actual_model_sha}"
            )
    else:
        actual_model_sha = None

    version = run_cmd([str(cli), "--version"], capture_output=True, text=True, check=True)
    version_text = (version.stdout + version.stderr).strip()

    run_id = "ACP-SYN-002-v0.1-" + dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "fixtures").mkdir()

    pre_memory = memory_snapshot()
    start_time = dt.datetime.now(dt.timezone.utc)

    tegra_file = (run_dir / "tegrastats.log").open("w")
    tegra = subprocess.Popen(
        ["tegrastats", "--interval", "500"],
        stdout=tegra_file,
        stderr=subprocess.STDOUT,
        text=True,
    )

    fixtures = [
        json.loads(line)
        for line in fixture_path.read_text().splitlines()
        if line.strip()
    ]

    results = []
    try:
        for index, fixture in enumerate(fixtures, start=1):
            fid = fixture["id"]
            fdir = run_dir / "fixtures" / fid
            fdir.mkdir()

            prompt = make_prompt(fixture)
            (fdir / "prompt.txt").write_text(prompt)

            command = [
                str(cli),
                "-m", str(model),
                "-ngl", "99",
                "-c", "4096",
                "-n", "96",
                "--seed", "42",
                "--temp", "0",
                "-st",
                "--simple-io",
                "--no-display-prompt",
                "-p", prompt,
            ]
            (fdir / "command.txt").write_text(
                shlex.join(command[:-2] + ["-p", "<prompt.txt>"]) + "\n"
            )

            before = memory_snapshot()
            t0 = time.time()
            proc = run_cmd(command, capture_output=True, text=True)
            elapsed = time.time() - t0
            after = memory_snapshot()

            (fdir / "stdout.txt").write_text(proc.stdout)
            (fdir / "stderr.txt").write_text(proc.stderr)
            (fdir / "memory_before.json").write_text(json.dumps(before, indent=2))
            (fdir / "memory_after.json").write_text(json.dumps(after, indent=2))

            combined = proc.stdout + "\n" + proc.stderr
            parsed, raw_json = parse_json_object(combined)
            if raw_json is not None:
                (fdir / "parsed_response.json").write_text(
                    json.dumps(parsed, indent=2) + "\n"
                )

            exp = fixture["expected"]
            parse_ok = parsed is not None
            choice_ok = parse_ok and parsed.get("choice") == exp["choice"]
            source_ok = parse_ok and parsed.get("source") == exp["source"]
            count_ok = parse_ok and parsed.get("independent_count") == exp["independent_count"]
            all_ok = bool(choice_ok and source_ok and count_ok and proc.returncode == 0)

            result = {
                "fixture_id": fid,
                "index": index,
                "condition": fixture["condition"],
                "returncode": proc.returncode,
                "elapsed_seconds": round(elapsed, 3),
                "parse_ok": parse_ok,
                "choice_correct": bool(choice_ok),
                "source_correct": bool(source_ok),
                "independent_count_correct": bool(count_ok),
                "all_correct": all_ok,
                "expected": exp,
                "observed": parsed,
                "swap_before_bytes": before.get("swap_used_bytes"),
                "swap_after_bytes": after.get("swap_used_bytes"),
            }
            results.append(result)
            (fdir / "score.json").write_text(json.dumps(result, indent=2) + "\n")
            print(
                f'[{index:02d}/{len(fixtures)}] {fid} {fixture["condition"]}: '
                f'{"PASS" if all_ok else "CHECK"} ({elapsed:.1f}s)',
                flush=True,
            )
    finally:
        tegra.terminate()
        try:
            tegra.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tegra.kill()
        tegra_file.close()

    end_time = dt.datetime.now(dt.timezone.utc)
    post_memory = memory_snapshot()

    by_condition = {}
    for r in results:
        bucket = by_condition.setdefault(
            r["condition"], {"n": 0, "all_correct": 0, "parse_failures": 0}
        )
        bucket["n"] += 1
        bucket["all_correct"] += int(r["all_correct"])
        bucket["parse_failures"] += int(not r["parse_ok"])
    for bucket in by_condition.values():
        bucket["exact_accuracy"] = bucket["all_correct"] / bucket["n"]

    n = len(results)
    summary = {
        "experiment_id": "ACP-SYN-002",
        "version": "0.1",
        "run_id": run_id,
        "status": "pre-freeze calibration",
        "n": n,
        "parse_failures": sum(not r["parse_ok"] for r in results),
        "choice_accuracy": sum(r["choice_correct"] for r in results) / n,
        "source_accuracy": sum(r["source_correct"] for r in results) / n,
        "independent_count_accuracy": sum(r["independent_count_correct"] for r in results) / n,
        "exact_fixture_accuracy": sum(r["all_correct"] for r in results) / n,
        "by_condition": by_condition,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    with (run_dir / "summary.csv").open("w", newline="") as f:
        fields = [
            "fixture_id","condition","returncode","elapsed_seconds","parse_ok",
            "choice_correct","source_correct","independent_count_correct","all_correct"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in fields})

    git_sha = run_cmd(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True
    ).stdout.strip()

    run_manifest = {
        "experiment_id": "ACP-SYN-002",
        "version": "0.1",
        "run_id": run_id,
        "started_utc": start_time.isoformat(),
        "ended_utc": end_time.isoformat(),
        "repo_commit": git_sha,
        "fixture_file": str(fixture_path),
        "fixture_sha256": actual_fixture_sha,
        "model_path": str(model),
        "model_sha256": actual_model_sha or "SKIPPED",
        "expected_model_sha256": EXPECTED_MODEL_SHA256,
        "runtime_path": str(cli),
        "runtime_version": version_text,
        "expected_runtime_commit": EXPECTED_RUNTIME_COMMIT,
        "generation": {
            "gpu_layers": 99,
            "context_tokens": 4096,
            "max_new_tokens": 96,
            "seed": 42,
            "temperature": 0,
            "single_turn": True,
            "simple_io": True,
            "no_display_prompt": True,
            "qwen_no_think": True
        },
        "reset": "fresh llama-cli process per fixture",
        "pre_memory": pre_memory,
        "post_memory": post_memory,
        "interpretation_boundary": "Pre-freeze calibration only; not confirmatory ACP evidence."
    }
    (run_dir / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n")

    print("\nRun directory:", run_dir)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
