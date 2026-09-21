# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** Four of my five questions are answered inside a single
labelled section of a single guide, so retrieval only has to find the right
heading. The fifth — where to eat in Halden Bay — is answered in
`guide_eating.md`, a cross-cutting guide, while the obvious place to look is
`guide_halden_bay.md`. I expect that one to be the miss, which is why I set
the target at 4 and not 5. Setting it at 5 would mean claiming retrieval never
prefers the topically obvious document over the correct one, and I have no
reason yet to believe that.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** All five and not four, because this one doesn't depend on
retrieval being good — only on the answer naming a file. Every chunk carries
its source filename through `store.py`, the grounding instruction in
`generate.py` asks for the filename explicitly, and a refusal doesn't count as
an answer that needs a source. For this to come out below 5 of 5 the model
would have to ignore a direct instruction while still producing prose, which
is a different failure from anything criteria 1 or 3 measure. A target of 4
here would let one silent drop pass unnoticed.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:** The two groups came out cleanly separated when I measured
them in Milestone 4 — in-corpus questions topped out at 0.5023, out-of-scope
ones started at 0.8026, and nothing landed in the 0.30-wide gap between. With
a cutoff of 0.65 sitting in that gap, all five refusals are comfortable rather
than marginal. I'm keeping the given target at 4 of 5 anyway instead of
raising it to 5, because that gap is a property of these five off-topic
questions rather than of my system. All five are from completely different
domains — football, engine oil, ibuprofen. When I tried three off-topic
questions that *sound* like travel, the gap mostly disappeared: "How do I get
from Lisbon to Porto by train?" scored 0.7165, and "What is the best beach in
Portugal?" scored **0.5836, which is under my 0.65 cutoff and would pass the
gate**. So my real refusal rate against adversarial off-topic questions is
worse than 5 of 5 suggests, and I'd rather have a target that admits that
than one the easy five make look perfect. This is the first thing I'd
investigate in unit 2.

---

## 4. No chunk splits a labelled section across two chunks

No chunk splits a labelled section, and no chunk is shorter than 150
characters. Concretely: every chunk is either exactly one `##` section of one
guide or that guide's intro paragraph, never a fragment of either, and the
"shortest" figure `python app.py index` reports is at or above 150.
Checked by reading all five sampled chunks and the index summary line.

**Why this target:** My documents are travel guides divided into labelled
sections — "Getting there", "Where to eat", "When to go" — and the answer to a
question is almost always the whole of one section. The starter's fixed
800-character cutter produced 51 chunks from 14 documents and a shortest chunk
of 24 characters, which was a heading stranded from the text underneath it.
A chunk that begins mid-section has lost the heading that says what it's
about, and a 24-character chunk can't answer anything. I picked 150 rather
than a higher floor because five sections in this corpus are genuinely short
and complete — the shortest is the 173-character "Where to stay" in
`guide_givens_mill.md`, which says there is nowhere to stay in the village and
needs no more words than that. A 200-character floor would force those five to
merge with a neighbouring section, which is a worse chunker dressed up as a
passing criterion.

---

## 5. Answers cite the document the fact actually came from

For at least 4 of my 5 test questions, the source file named in the answer is
a document that genuinely contains that fact — not merely a document about
the right town. I check this by opening the named file and looking for the
fact.

**Why this target:** This corpus makes a wrong-but-plausible citation easy.
Nine of my fourteen documents are town guides, and five cut across all of
them — eating, walking, transport, seasons, accessibility. The same fact
often appears in both, and some facts, like Halden Bay's Fell Street being
cheaper than the harbour front, live *only* in the cross-cutting guide. An
answer citing `guide_halden_bay.md` for that would look right to anyone not
checking, which is exactly the kind of error criterion 2 waves through:
criterion 2 asks whether a source is named, and a confidently wrong filename
satisfies it completely. I set 4 of 5 rather than 5 of 5 for the same reason
as criterion 1 — the Halden Bay question is the one I expect to fail, and
it would be dishonest to set a target here that assumes it won't.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
