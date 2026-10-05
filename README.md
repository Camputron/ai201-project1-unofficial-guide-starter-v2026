# The Unofficial Guide

**Corpus:** `city_guides`

---

# Unit 1

## What This Does

This is a question-answering system over `city_guides`, a set of fourteen
travel guides for a fictional region — nine guides to individual towns, plus
five that cut across all of them on eating, walking, regional transport,
seasons, and accessibility. You ask a plain question like "How often do
Marchwood's trams run on weekdays?" and it finds the relevant sections,
answers from them, and names the files the answer came from.

It handles the kinds of questions a guidebook actually gets asked: practical
logistics (how to reach a town, what days buses run), prices and opening
hours, and comparisons across the region (which town is easiest to get around
with limited mobility). When a question isn't covered by the guides, a
relevance gate stops it before it reaches the model and the system says it
doesn't have enough information rather than inventing an answer.

## Chunking Strategy

**Chunk size:** one `##` section per chunk — variable, 174 to 762 characters,
averaging 322. A 1200-character ceiling splits the few over-long sections at
a paragraph break.
**Overlap:** none.

These documents aren't prose — they're guides divided into labelled sections:
"Getting there", "Getting around", "Eat and drink", "Where to stay", "When to
go". Reading them in Milestone 1, the thing I noticed is that the answer to a
question is almost always *the whole of exactly one section*, and never
part of two. So the section is the natural unit and a character count is just
a guess that sometimes lands in the right place.

The starter's fixed 800-character window shows why this matters. On
`guide_kestrelford.md` it produced four chunks: the first ended mid-word on
`## Eat and drin`, the second opened mid-sentence on "lower car park is
steeper than it looks", and the fourth was a 59-character orphan — "irts. The
nearest full hospital is in Brightwater; there is". Each chunk straddled
three or four unrelated topics, so it matched every question about
Kestrelford a little and no question well.

Two details worth naming:

- **Every chunk carries its town name.** A section that reads "Two inns on the
  square and a handful of rooms above the pubs" is useless without knowing
  whose square. The `# Title` line gets prepended to every chunk, so each one
  stands on its own.
- **Overlap is zero on purpose.** Overlap exists to stop a sentence being cut
  in half — but cutting at headings never cuts a sentence at all, so there's
  nothing for it to protect. Repeating the tail of "Eat and drink" at the top
  of "What to see" would make both chunks match both questions slightly,
  which is the exact blurring overlap is meant to prevent.

**What I changed partway through.** My first version emitted a bare
23-character chunk containing nothing but a title. Four of the cross-cutting
guides go straight from `# Title` to the first `## ` heading with no intro
paragraph, so the "preamble" was just the title line. I hadn't predicted that
— I found it by sorting chunks by length after the first run. Those empty
preambles are now dropped, since the title is prepended everywhere anyway.
That took the shortest chunk from 23 to 174 characters.

Result: **51 chunks → 94 chunks**, shortest **24 → 174** characters.

## Sample Chunks

From `python app.py --corpus city_guides chunks -n 5`.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

**Reading these back:** chunks 2 through 5 each stand on their own. Chunk 4
answers "what can you do in Kestrelford?" and "how much is the church tower?"
with nothing before or after it, because the town name and the heading are
both right there. Chunk 1 is the weakest of the five — it's a real intro
paragraph rather than a stranded heading, so it isn't a fragment, but it sets
up a document rather than answering anything. It's the shortest chunk in the
corpus at 174 characters, and it's the one I'd look at first if
`guide_accessibility.md` started matching questions it shouldn't.

## Sample Answer

**Question:** Where should I eat in Halden Bay to avoid harbour front prices?

**Answer:**

```
  (best distance 0.229, cutoff 0.65)

To avoid harbour front prices, you should eat on Fell Street, one level up,
where comparable food costs roughly half as much as it does on the harbour
front.

(Source: `guide_halden_bay.md` and `guide_eating.md`)

Sources retrieved: guide_eating.md, guide_halden_bay.md
```

I picked this one rather than an easier question because it's the question
this corpus is worst at. The Fell Street fact lives in `guide_eating.md`, a
cross-cutting guide — not in `guide_halden_bay.md`, which is where anyone
would look first and which retrieval ranks first (0.2286 against 0.2822). An
answer citing only `guide_halden_bay.md` would look completely correct and
would satisfy criterion 2, which is why I wrote criterion 5 separately.

**My relevance cutoff: 0.65**

I ran all ten questions through retrieval and recorded the best distance for
each. The two groups came out cleanly separated, with a 0.30-wide gap:

| Question | In corpus? | Best distance |
|---|---|---|
| What days do buses run from Brightwater to Kestrelford? | yes | 0.1975 |
| Where should I eat in Halden Bay to avoid harbour front prices? | yes | 0.2286 |
| How often do Marchwood's trams run on weekdays? | yes | 0.2437 |
| How much does it cost to climb the church tower in Kestrelford? | yes | 0.4390 |
| Which town is easiest to get around with limited mobility? | yes | 0.5023 |
| What is the capital of Mongolia? | no | 0.8026 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.8350 |
| How do I write a for loop in Rust? | no | 0.8365 |
| How do I change the oil in a diesel engine? | no | 0.8881 |
| Who won the 1994 World Cup? | no | 0.9753 |

In-corpus ran **0.1975 – 0.5023**. Out-of-scope ran **0.8026 – 0.9753**.
Nothing landed between 0.5023 and 0.8026.

I put the cutoff at 0.65 rather than the starter's 0.6. Both separate today's
numbers perfectly, so the choice is about which direction I'd rather be wrong
in. 0.6 leaves 0.098 of headroom above my hardest real question; 0.65 leaves
0.148 and still refuses the nearest off-topic question by 0.15. A real
question phrased less directly than my five seemed likelier to creep upward
than an off-topic one was to creep down.

**The gap is narrower than it looks.** All five out-of-scope questions are
from unrelated domains — football, engine oil, medicine. When I tried
off-topic questions that *sound* like travel, the separation mostly
collapsed:

| Off-topic question | Best distance | Would the gate stop it? |
|---|---|---|
| How do I get from Lisbon to Porto by train? | 0.7165 | yes, but by 0.07 |
| What is the best beach in Portugal? | 0.5836 | **no — it passes** |

So my honest refusal rate is worse than 5 of 5 makes it look, and a cutoff
low enough to catch the Portugal beach question would start refusing the
mobility question at 0.5023. That's the first thing I'd dig into in unit 2.

**Top-k is 5**, left at the default deliberately. The Halden Bay question is
the reason: `guide_halden_bay.md` takes rank 1, and the two `guide_eating.md`
chunks holding the actual answer come back at ranks 2 and 3. At k=1 or k=2
that question could not be answered at all.

## How I Used AI

**1. Writing the section-based chunker.** I described what I wanted — split
at `##` headings, one section per chunk, prepend the town name — and had
Claude draft `split_documents`. The draft worked on the nine town guides and
was wrong on the cross-cutting ones: it treated everything before the first
`##` as a chunk, which on `guide_walking.md` and three others meant emitting
a chunk containing nothing but `# Walking in the region`, 23 characters.
Neither of us caught it by reading the code. I found it by sorting all 94
chunks by length and looking at the bottom of the list, which is a check I'd
now run before trusting any chunker. The fix — drop a preamble that's only a
title, since the title gets prepended anyway — is the `preamble_body` block
in `chunker.py`. This is also why I don't fully trust the 1200-character
`MAX_SECTION` path: nothing in this corpus is long enough to exercise it
hard, so it's the least-tested code I have.

**2. Pressure-testing my acceptance criteria.** Milestone 2 says not to have
an AI write your criteria, so I wrote all five myself and then asked Claude
the suggested question — how would you test each of these using only the
sentence? Two came back fine. Criterion 4 came back with a real problem: I'd
written "every chunk begins at a `##` heading", and the answer pointed out
that the ten town intro paragraphs legitimately don't, so the criterion as
written would fail on correct behaviour. I reworded it to "never a fragment
of a section", which is what I'd actually meant. Separately, writing the
reason under criterion 3 made me realise I'd only tested off-topic questions
from unrelated domains, so I measured two travel-sounding ones myself — and
found that "What is the best beach in Portugal?" scores 0.5836 and slips
under my cutoff. That's the most useful thing I learned this unit, and it
came from being made to justify a number rather than from the code.

*No stretch features attempted.*

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

Evidence: [results/run_2026-10-04_2326_before.md](results/run_2026-10-04_2326_before.md)
(`python run_eval.py --label before`, 3 runs per question, cache off, top-k 5,
cutoff 0.65) and [results/probe_2026-10-04_2328_before.md](results/probe_2026-10-04_2328_before.md)
(`python tools/probe.py --label before`, retrieval only, no model calls).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk splits a section; shortest ≥ 150 chars | 0 splits, ≥ 150 | 0 splits, 174 | 0 splits, 174 | 0 splits, 174 | MET |
| 5. Cited file genuinely contains the fact | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**How each row was counted.** There's no `scorer.py`, so `run_eval.py` left
its pass/fail cells blank and I judged every one of the 15 answers by hand.

- **Criterion 1** — I printed the five retrieved chunks for each question and
  checked them for a phrase from the document that actually answers it (the
  `ANSWER_MARKERS` in `tools/probe.py`). Retrieval is deterministic, so all
  three runs saw identical chunks, and the best distances in the results file
  agree to four places on every run.
- **Criterion 2** — each of the 15 answers names at least one `.md` file.
- **Criterion 3** — one deterministic pass from `run_eval.py::check_out_of_scope`,
  so the same number appears in all three columns.
- **Criterion 4** — `python app.py index` reported *94 chunks, 322 characters
  on average (shortest 174, longest 762)*. For each of the 14 documents, the
  number of chunks equals its `##` sections plus its intro paragraph (if it has one),
  so no section was split or merged. Chunking happens once at index time, so
  it's the same in every run.
- **Criterion 5** — for every file each answer cited, I grepped that file for
  the fact. All 15 answers cite only files that contain it.

The runs really did re-run. Wording changes between runs (the mobility answer
in run 3 adds *"because it is flat, compact, and everything is within three
minutes"*, and the Halden Bay answer formats its citation differently each
time), which wouldn't happen with a cached answer.

### Real output (run 1 unless noted)

**Criteria 1 and 5 — retrieval for the mobility question**, the closest call
in the set. Produced by `store.py::search` and recorded by `tools/probe.py::main`:

```
# Which town in the region is easiest to get around with limited mobility?
  1. guide_corry_vale.md#2           0.5023
  2. guide_accessibility.md#0        0.5113
  3. guide_accessibility.md#3        0.5326
  4. guide_accessibility.md#1        0.5528  CONTAINS Thornby Wells
  5. guide_corry_vale.md#0           0.5569
```

**Criteria 2 and 5 — answers**, produced by `generate.py::answer_from_chunks`
via `run_eval.py::run_once`:

```
Q: What days do buses run from Brightwater to Kestrelford?
Buses run from Brightwater to Kestrelford roughly hourly on weekdays and every
two hours on Saturdays, but they do not run on Sundays.
Source: `guide_kestrelford.md` (and also mentioned in `guide_regional_transport.md`).

Q: How much does it cost to climb the church tower in Kestrelford?
It costs £2 to climb the church tower in Kestrelford (guide_kestrelford.md).

Q: Where should I eat in Halden Bay to avoid harbour front prices?
To avoid harbour front prices in Halden Bay, you should eat on Fell Street, which
is one level up and offers comparable food for roughly half the price.
Source: `guide_halden_bay.md` and `guide_eating.md`.

Q: How often do Marchwood's trams run on weekdays?
Marchwood's trams run every 8 minutes on weekdays (guide_marchwood.md).

Q: Which town in the region is easiest to get around with limited mobility?
Thornby Wells is the easiest town in the region to get around with limited
mobility (guide_accessibility.md).
```

**Criterion 3 — the gate**, produced by `run_eval.py::check_out_of_scope`:

```
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.803)  What is the capital of Mongolia?
  refused  (best distance 0.888)  How do I change the oil in a diesel engine?
  refused  (best distance 0.975)  Who won the 1994 World Cup?
  refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.836)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criterion 4 — chunking**, produced by `chunker.py::split_documents`, summary
from `chunker.py::describe`:

```
  stored   94 chunks in 12.4s
94 chunks, 322 characters on average (shortest 174, longest 762), produced by chunker.py::split_documents
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer, ≥ 4 of 5 | **MET** | 5/5 on all three runs. Every question had an answer-bearing chunk in its top 5. The closest call was the mobility question, where that chunk came back at rank 4 of 5 (0.5528), behind an irrelevant Corry Vale chunk. That's still a pass under the criterion as written. |
| 2 | Every answer names a source, 5 of 5 | **MET** | All 15 answers name at least one `.md` file. No answer was a refusal, so none were exempt. |
| 3 | Gate stops out-of-corpus questions, ≥ 4 of 5 | **MET** | The gate refused all 5. The closest one, Mongolia, scored 0.803, which is 0.15 over the 0.65 cutoff, so it wasn't marginal. |
| 4 | No chunk splits a section; shortest ≥ 150 | **MET** | The shortest chunk is 174 characters. For every document, chunks = `##` sections + intro, so nothing was split. Not close. |
| 5 | Cited file contains the fact, ≥ 4 of 5 | **MET** | I opened every cited file and found the fact in it, 5/5 on all three runs. I counted an answer naming two files as correct only if *both* contain the fact. Both did each time. |

**Arguing the other side.** The strongest case against these verdicts is
criterion 5. I predicted in unit 1 that the Halden Bay question would fail it,
because I believed *Fell Street* appeared only in `guide_eating.md`. That was
wrong. `guide_halden_bay.md` line 15 says *"Prices on the harbour front are
roughly double those on Fell Street, one level up"*. So an answer citing the
town guide is genuinely correct, and the question I picked to stress
criterion 5 couldn't actually make it fail. The verdict is still MET, because
every citation really does contain the fact. But "5 of 5" says less than it
looks like it does, because none of my five questions has a fact that lives
*only* in a cross-cutting guide. I haven't revised the criterion: the
measurement itself is sound. The test questions just don't exercise it, and
that's a test-design finding, not a broken criterion.

The case against criterion 1 is that rank 4 of 5 is one position from a miss.
The criterion only asks whether the answer is anywhere in the top 5, so the
verdict is MET. It's also why the improvement below targets that question.

No criteria were revised. `criteria.md` is unchanged.

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

**No criterion was missed.** Honestly, that says more about how safe my
targets were than about how good the system is. Four of my five questions
are answered by a chunk at rank 1 with a distance under 0.44, which is the
easy case. Below are the two near-misses that the targets let through, with
diagnoses, and then which criteria I'd tighten.

### Near-miss 1: the mobility question's answer chunk ranks 4th of 5

- **Stage: embedding → retrieval.**
- **Mechanism:** The answer is in `guide_accessibility.md#1`, a section headed
  `## Straightforward`. That heading carries no retrieval signal. The chunk
  also holds three towns' paragraphs (Thornby Wells, Marchwood, Brightwater),
  so its embedding is an average of three topics and doesn't sit close to any
  single question (0.5528). Meanwhile `guide_corry_vale.md#2` is headed
  `## Getting around` and talks about what's "walkable". The question says
  "get around", so the embedding model matches on those surface words and
  ranks a chunk about a valley you can't get around *without a car* first
  (0.5023). The literal answer phrase "the easiest town in the region" is
  almost word-for-word what the question asks. Pure semantic search glides
  past exactly that kind of exact-term match.
- **Why it still passed:** top-k is 5 and the answer chunk is at 4. At
  top-k 3, criterion 1 would be 4/5 and criterion 5 would likely fail on the
  same question.

### Near-miss 2: the gate can't separate travel-sounding off-topic questions

- **Stage: retrieval → relevance gate.**
- **Mechanism:** The gate compares one cosine distance to a fixed cutoff. Cosine
  distance measures *topic* similarity, not whether the corpus covers the
  place being asked about. "How often do the trams run in Amsterdam?" scores
  0.4613 against Marchwood's tram chunk, which is *closer* than my real mobility
  question (0.5023). So no cutoff exists that refuses it without also refusing
  a real question. Out of 10 travel-sounding off-topic questions
  (`tools/probe.py`), the gate let 6 through.
- **Why it didn't cause a wrong answer:** the grounding prompt in
  `generate.py` is the second layer. I sent all six through generation, and
  every one came back as a refusal, e.g. *"I don't have enough information to
  answer how often trams run in Amsterdam, as the documents only discuss
  Marchwood, Pellew Sands, and Kestrelford."* So the system as a whole refused
  them, but the gate wasn't the layer doing it.

**The pattern:** both near-misses are the same weakness. Retrieval relies on
embedding similarity alone, and the embedding responds to surface topic
words ("get around", "trams", "buses") more than to the specific names and
phrases that decide whether a chunk actually answers the question.

### Criteria I'd tighten

- **Criterion 1** → "for 5 of 5 questions, a chunk containing the answer is in
  the top **3**." Today that would be a **miss** (mobility is at rank 4).
- **Criterion 3** → also run the 10 travel-sounding questions and require the
  *system* (gate or prompt) to refuse at least 9 of 10. The current five are
  so far off-topic that 5/5 tells me nothing.
- **Criterion 5** → keep the wording but add a question whose fact really lives
  *only* in a cross-cutting guide, so the criterion can actually fail.

## The Improvement

**What I changed:** Hybrid search. In `store.py::search`, when
`config.HYBRID_SEARCH` is on, the new `store.py::_hybrid_search` ranks every
chunk twice: by embedding distance and by BM25 keyword score (`rank-bm25`,
already in `requirements.txt`). It merges the two rankings with reciprocal rank
fusion (`1/(60 + rank)` from each list) and keeps the top 5. Each result
still carries its real cosine distance, so the gate compares the same kind of
number against the same 0.65 cutoff. Nothing else changed: the chunker, top-k,
cutoff, prompt and model are all as they were in unit 1.

**Why I picked it:** Near-miss 1 is semantic search gliding past an exact-term
match. The answer chunk says "the easiest town in the region" nearly word for
word, yet it ranked 4th behind a chunk that only shares "get around".
Keyword matching is the direct fix for that.

### Run Log — After

Evidence: [results/run_2026-10-04_2330_after.md](results/run_2026-10-04_2330_after.md)
and [results/probe_2026-10-04_2330_after.md](results/probe_2026-10-04_2330_after.md).
Same questions, same three runs, cache off.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk splits a section; shortest ≥ 150 chars | 0 splits, ≥ 150 | 0 splits, 174 | 0 splits, 174 | 0 splits, 174 | MET |
| 5. Cited file genuinely contains the fact | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criterion 4 is unchanged because the chunker wasn't touched. Under criterion 5,
mobility run 1 now also cites `guide_walking.md`. I checked it: line 14 calls
Thornby Wells *"the region's most accessible town on foot"*, so that citation
holds.

### Before and after, side by side

The five criteria didn't move, because they were all already met. What the
change targeted shows up in the probe instead:

| Question | Answer-chunk rank before | After |
|---|---|---|
| Buses Brightwater → Kestrelford | 1 | 1 |
| Kestrelford church tower | 1 | 1 |
| Halden Bay, avoiding harbour prices | 1 | 1 |
| Marchwood tram frequency | 1 | **2** (worse) |
| Easiest town with limited mobility | 4 | **2** (better) |
| **Worst rank across the five** | **4** | **2** |

| Travel-sounding off-topic questions | Before | After |
|---|---|---|
| Let through by the gate (of 10) | 6 | 6 |

Real output for the mobility question after the change (`tools/probe.py`,
via `store.py::_hybrid_search`), with the answer it produced in run 2
(`generate.py::answer_from_chunks`):

```
| Which town in the region is easiest to get around with limited mobility? | 2 | 0.5528 | guide_accessibility.md#0 | 0.5113 |

**Thornby Wells** is the easiest town in the region to get around with limited
mobility because it is flat, compact, and everything is within three minutes
of everything else (guide_accessibility.md).
```

**Did it help?** Yes, for the problem it was aimed at, and at a small cost
elsewhere. I can tell because the answer-chunk ranks above come from the same
probe run before and after. The mobility answer moved from rank 4 to rank 2,
and the irrelevant Corry Vale chunk that used to rank first dropped out of
the top 5 entirely. The cost is the tram question. `guide_eating.md#2`
mentions both "Marchwood" and "tram" (*"Northgate — is a tram..."*), so BM25
promoted it above the real answer, from rank 1 to rank 2. Overall the
worst-case rank went from 4 to 2, so under the tighter "top 3" version of
criterion 1 I proposed above, the system would go from a miss to a pass. On
my five criteria as written, though, before and after are identical, and I
won't claim otherwise.

Two side effects worth naming:

- **The gate's number changed for the mobility question**, from 0.5023 to
  0.5113. The gate checks the closest chunk *among the five that come back*,
  and the irrelevant 0.5023 Corry Vale chunk no longer comes back. So the gate
  is now judging on a chunk that's actually about the question, but there's
  0.009 less headroom under the cutoff.
- **The out-of-scope questions got further from the cutoff.** Their best
  distances rose (Mongolia 0.803 → 0.857) for the same reason: keyword matches
  pulled in chunks that are semantically further away. It didn't change any
  refusal, but it means hybrid retrieval makes the gate's number mean
  something slightly different from what I calibrated in unit 1.

- **The staff smoke test now fails one check.** `tools/smoke_test.py` asserts
  that search results come back nearest-first. Fused order breaks that on
  purpose, so 3 of its checks (one per corpus) fail with hybrid on and pass
  with it off. I left the test alone because it encodes the unit 1 contract.
  `test.py` still passes.

It did nothing for near-miss 2. The gate still lets 6 of 10 travel-sounding
questions through, which is what I expected, since keyword search wasn't aimed
at the gate.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

No criterion is missed after the fix, so nothing here is a miss. But "met"
isn't the same as "working", and these are the things I know are still
wrong:

- **The gate still lets 6 of 10 travel-sounding off-topic questions through.**
  The grounding prompt catches every one, so no wrong answer reaches the user,
  but the gate isn't doing its job for this kind of question. A lower cutoff
  can't fix it, because "trams in Amsterdam" (0.4613 before) is closer than a
  real question. Next I'd add a coverage check to `gate.py`: refuse when the
  question names a place that appears nowhere in the corpus (Paris,
  Edinburgh, Portugal). That catches exactly this pattern without touching
  distances. I stopped because this unit allows one change, and I spent it on
  retrieval, where the near-miss could have produced a wrong answer rather
  than just a redundant safety net.
- **Hybrid search costs the tram question a rank** (1 → 2). The answer is still
  retrieved, but a chunk that merely mentions "Marchwood" and "tram" now
  outranks it. Weighting the semantic list above the keyword list in the
  fusion would probably fix it, but tuning a weight against five questions
  is overfitting, so I'd want more test questions first.
- **The gate's calibration is a little stale.** The 0.65 cutoff was chosen from
  vector-only distances in unit 1. With hybrid retrieval, the closest chunk
  among the five that come back is sometimes not the closest chunk overall, so I'd
  re-measure the in-corpus/out-of-scope gap and re-pick the cutoff.
- **Criterion 5 has never been tested in the case it was written for.** None of
  my questions has a fact that lives *only* in a cross-cutting guide, so 5/5
  shows the citations are right, not that the system avoids the
  plausible-but-wrong citation I was worried about.

## What I'd Do Differently

- **Criterion 1** should name a rank, not just "in the retrieved chunks". Top-5
  let a rank-4 answer pass without comment, and the probe showed that was
  the weakest point in the system. I'd write "for 5 of 5 questions, a chunk
  containing the answer is in the top 3".
- **Criterion 3** should be tested against off-topic questions that *sound*
  on-topic. My unit 1 write-up already suspected this, and the probe
  confirmed it: 5/5 on football and engine oil, but 6 of 10 travel questions
  get past the gate. I'd also measure the whole system's refusal, not just the
  gate's, since the prompt turned out to be the layer actually doing the work.
- **Criterion 5** needs a test question built to make it fail. I chose the
  Halden Bay question because I believed Fell Street appeared only in
  `guide_eating.md`. I never grepped for it, and it's in
  `guide_halden_bay.md` too. Next time I'd check that the trap I'm setting
  actually exists before writing a target around it.
- **Criteria 1, 4 and 5 can't vary between runs**, because retrieval and
  chunking are deterministic. Only criterion 2 (and, in principle, 5) depends on
  the model. Three runs mostly measured the same thing three times. I'd put
  more of my criteria on the generated answer, where repeated runs actually
  tell you something.

## How I Used AI (unit 2)

I had Claude Code (Claude Opus 5.5) do this unit's work with me in the
editor. Specifically, it:

- Ran `run_eval.py` before and after, judged all 30 answers by hand against
  the source documents (there's no `scorer.py`), and grepped the corpus to
  check every citation for criterion 5. That's how the Fell Street assumption
  from unit 1 turned out to be wrong.
- Wrote `tools/probe.py` to show where the answer-bearing chunk ranks and how
  the gate handles travel-sounding off-topic questions. The rank-4 mobility
  result and the 6-of-10 gate result both came from that probe rather than
  from `run_eval.py`.
- Sent the six off-topic questions that passed the gate through generation, to
  check whether the prompt layer caught them. It did, which is why I aimed the
  improvement at retrieval rather than the gate.
- Implemented hybrid search in `store.py::_hybrid_search` and noticed it
  breaks the staff smoke test's nearest-first check.
- Drafted the verdicts, diagnoses and the write-up in this section of the
  README.
