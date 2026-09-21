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

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

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

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

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
