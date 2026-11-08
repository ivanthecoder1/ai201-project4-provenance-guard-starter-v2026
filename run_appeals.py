#!/usr/bin/env python3
"""
Run criterion 4, the appeal path, three times.

    python app.py                              # in one terminal
    python run_appeals.py --label before       # in another

`run_eval.py` can only send text to /submit, and an appeal needs a content_id
that a submission handed back first. So each trial here:

  1. submits 10 pieces of text, each under its own creator_id,
  2. appeals each content_id that came back, with its own reasoning,
  3. reads GET /log and checks there is an appeal entry for each one, holding
     the reasoning word for word,
  4. appeals 3 content_ids that were never submitted, and checks each gets a
     404 and leaves no appeal entry in the log.

A trial passes criterion 4 only if all 10 + 3 checks pass.
"""

import argparse
import datetime as dt
import json
import sys
import uuid

import config

APPEALS_PER_TRIAL = 10
UNKNOWN_PER_TRIAL = 3

TEXT = ("Piece {n} for the appeal test. I wrote a short note about the bus "
        "being late again this morning, which meant I missed the start of the "
        "lecture and had to borrow notes from a friend afterwards.")
REASONING = "Trial {t}, appeal {n}: I wrote this myself and can show my drafts."


def run_trial(requests, url, trial, timeout):
    """One trial: returns a list of per-check results."""
    checks = []

    for n in range(1, APPEALS_PER_TRIAL + 1):
        body = {"text": TEXT.format(n=n), "creator_id": f"appeal_t{trial}_{n}"}
        submitted = requests.post(f"{url}/submit", json=body, timeout=timeout)
        content_id = submitted.json().get("content_id")
        reasoning = REASONING.format(t=trial, n=n)
        response = requests.post(f"{url}/appeal", json={
            "content_id": content_id, "reasoning": reasoning}, timeout=timeout)
        checks.append({
            "kind": "real",
            "content_id": content_id,
            "submit_status": submitted.status_code,
            "status": response.status_code,
            "response": response.json() if response.content else None,
            "reasoning": reasoning,
        })

    for _ in range(UNKNOWN_PER_TRIAL):
        content_id = f"never-submitted-{uuid.uuid4()}"
        response = requests.post(f"{url}/appeal", json={
            "content_id": content_id, "reasoning": "This id was never submitted."},
            timeout=timeout)
        checks.append({
            "kind": "unknown",
            "content_id": content_id,
            "status": response.status_code,
            "response": response.json() if response.content else None,
        })

    entries = requests.get(f"{url}/log", timeout=timeout).json()["entries"]
    for check in checks:
        appeals = [e for e in entries
                   if e.get("content_id") == check["content_id"] and e.get("event") == "appeal"]
        if check["kind"] == "real":
            check["passed"] = (
                check["status"] == 200
                and (check["response"] or {}).get("status") == "under_review"
                and any(e.get("reasoning") == check["reasoning"] for e in appeals)
            )
        else:
            check["passed"] = check["status"] == 404 and not appeals
        check["appeal_entries_in_log"] = len(appeals)
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    import requests

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    trials = []
    for trial in range(1, args.trials + 1):
        checks = run_trial(requests, args.url, trial, args.timeout)
        real = sum(c["passed"] for c in checks if c["kind"] == "real")
        unknown = sum(c["passed"] for c in checks if c["kind"] == "unknown")
        print(f"  trial {trial}: {real}/{APPEALS_PER_TRIAL} real appeals, "
              f"{unknown}/{UNKNOWN_PER_TRIAL} unknown ids")
        trials.append((real, unknown, checks))

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeals_{stamp}{label}.md"
    target = f"{APPEALS_PER_TRIAL}/{APPEALS_PER_TRIAL} + {UNKNOWN_PER_TRIAL}/{UNKNOWN_PER_TRIAL}"
    runs = " | ".join(f"{r}/{APPEALS_PER_TRIAL} + {u}/{UNKNOWN_PER_TRIAL}" for r, u, _ in trials)
    met = all(r == APPEALS_PER_TRIAL and u == UNKNOWN_PER_TRIAL for r, u, _ in trials)
    lines = [
        f"# Appeal run{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_appeals.py::main`",
        "- Service: `app.py::appeal` · log read back through `GET /log`",
        f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1)) + " | Verdict |",
        "|---|---|" + "|".join(["---"] * args.trials) + "|---|",
        f"| 4. appeal path | {target} | {runs} | {'MET' if met else 'MISSED'} |",
        "",
        "## What actually came back",
        "",
    ]
    for number, (_, _, checks) in enumerate(trials, 1):
        lines += [f"**Trial {number}**", "", "```json", json.dumps(checks, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
