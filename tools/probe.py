#!/usr/bin/env python3
"""
Retrieval-only probe, written in unit 2 to see what run_eval.py can't.

    python tools/probe.py --label before

run_eval.py says whether each answer was right. It doesn't say how close
retrieval came to getting it wrong. This records two things, and costs no
model calls:

1. For each test question, the rank and distance of the first retrieved chunk
   that actually contains the answer. Criterion 1 only asks "is it somewhere
   in the top 5"; rank 1 and rank 5 both pass, but they aren't the same system.

2. Ten off-topic questions that *sound* like travel — the kind unit 1 found
   the gate can't separate — and whether the gate lets them through. These
   are not criterion 3's OUT_OF_SCOPE list, which is untouched.

Everything goes through `store.search` and `gate.check`, the same path the
real system uses, so a change to retrieval shows up here.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config  # noqa: E402
import gate  # noqa: E402
import questions as qs  # noqa: E402
from store import search  # noqa: E402

# A phrase that only appears in a chunk which really answers the question.
# Written from reading the documents, not from the system's output.
ANSWER_MARKERS = {
    "What days do buses run from Brightwater to Kestrelford?":
        ["not at all on Sundays", "does not run on Sundays"],
    "How much does it cost to climb the church tower in Kestrelford?":
        ["tower you can climb for £2"],
    "Where should I eat in Halden Bay to avoid harbour front prices?":
        ["Fell Street"],
    "How often do Marchwood's trams run on weekdays?":
        ["every 8 minutes on weekdays"],
    "Which town in the region is easiest to get around with limited mobility?":
        ["Thornby Wells** is the easiest town"],
}

TRAVEL_OFF_TOPIC = [
    "How do I get from Lisbon to Porto by train?",
    "What is the best beach in Portugal?",
    "Where should I eat in Paris on a budget?",
    "How often do the trams run in Amsterdam?",
    "What days do buses run in Edinburgh?",
    "Which hotels in Rome have step-free access?",
    "When is the best time to visit Iceland?",
    "How much does it cost to climb the Eiffel Tower?",
    "Is Barcelona easy to get around in a wheelchair?",
    "What is the best hiking trail in the Lake District?",
]


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    lines = [
        f"# Retrieval probe{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `tools/probe.py::main`",
        f"- top-k: {config.TOP_K} · relevance cutoff: {config.THRESHOLD}",
        f"- When: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Where the answer-bearing chunk ranks",
        "",
        "| Question | Answer chunk rank | Its distance | Rank-1 chunk | Rank-1 distance |",
        "|---|---|---|---|---|",
    ]

    for item in qs.answered():
        question = item["question"]
        markers = ANSWER_MARKERS.get(question, [item.get("expects", "")])
        results = search(question)
        rank, hit = None, None
        for i, r in enumerate(results, 1):
            if any(m in _flat(r.text) for m in markers):
                rank, hit = i, r
                break
        top = results[0]
        lines.append(
            f"| {question} | {rank if rank else 'not retrieved'} "
            f"| {f'{hit.distance:.4f}' if hit else '—'} "
            f"| {top.label} | {top.distance:.4f} |"
        )
        print(f"rank {rank}  {question}")

    lines += [
        "",
        "## Travel-sounding off-topic questions through the gate",
        "",
        "| Question | Best distance | Gate |",
        "|---|---|---|",
    ]
    passed = 0
    for question in TRAVEL_OFF_TOPIC:
        decision = gate.check(search(question))
        passed += decision.passed
        verdict = "**let through**" if decision.passed else "refused"
        lines.append(f"| {question} | {decision.best_distance:.4f} | {verdict} |")
        print(f"{verdict:16s} {decision.best_distance:.4f}  {question}")
    lines += ["", f"Gate let through {passed} of {len(TRAVEL_OFF_TOPIC)}.", ""]

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"probe_{stamp}{f'_{args.label}' if args.label else ''}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
