Show What You Know: The Unofficial Guide

Every college has two kinds of knowledge. There's the official kind: course catalogs, housing handbooks, the university website. Then there's the real kind, the stuff students tell each other so they can survive. Which dining hall is worth the walk. Which professor actually answers email. Which apartment building has the mold problem.

In this unit you'll build The Unofficial Guide, a system that makes the second kind searchable. Someone asks a plain question — "Is the housing lottery actually random?" — and gets back an answer drawn from real documents, with sources.

This project runs for two units. In this unit you build the system and write down what "working" would mean for it. In the next unit you test it against that standard, find where it falls short, and fix something. You'll submit the same repository both units, so don't delete it when you're done.

You get more support here than you will in later projects. Use it. The habits you build now are the ones you'll need when the scaffolding comes off.

🎯 Goals

By completing this project, you will be able to:

    Build a document pipeline that loads, chunks, and embeds text
    Query a vector store and get back relevant results
    Write answers that stay grounded in the documents you retrieved
    Write acceptance criteria that name a target someone else could check


📖 Words you'll need

These come up throughout the unit. Come back here any time one stops making sense.
Term 	What it means
Chunk 	A small piece of a document. Your system searches chunks, not whole files.
Overlap 	How much text two neighboring chunks share, so a sentence doesn't get cut in half.
Embedding 	A list of numbers that stands for a chunk's meaning. Similar meaning, similar numbers.
Vector store 	The database that holds those numbers and finds close matches quickly.
Retrieval 	Handing the store a question and getting back the chunks closest to it.
Top-k 	How many chunks you pull back per question. k=5 means five.
Distance 	How far a chunk is from your question in meaning. Lower is better — 0.3 is a close match, 0.9 is unrelated.
Grounding 	Making the model answer from your documents only, not from what it already knows.

📦 What proves you did the work

Three things. If all three are in your repo, your submission is complete.

    criteria.md — five numbered acceptance criteria, each naming a target.
    README.md — the five sections listed at the bottom of this page.
    Your commit history — at least four new commits, in the repo you'll submit again in the next unit.


✅ Features
Required Features

    Document ingestion. Load one of the provided corpora and clean it — strip out navigation text, ads, and anything else that isn't the real content.

    A chunking strategy. Split the documents into chunks on purpose, not by picking a round number. Your README explains your chunk size, your overlap, and what about these documents made you choose them.

    Vector store and search. Embed your chunks, store them, and retrieve the closest ones for a given question.

    Grounded answers with sources. The model answers using the retrieved chunks and nothing else. Every answer names the document it came from.

    A relevance gate. Before the model runs, check how close the best chunk actually is. If nothing came back close enough, say so and stop — don't hand the model thin material and hope it declines. You pick the cutoff in Milestone 4.

    A way to ask questions. A web page, a command-line tool, or a notebook. It just has to work without you standing there explaining it.

    Five acceptance criteria. Three are written for you. You write two more and explain all five. Milestone 2 walks you through it.

Stretch Features

Optional, for extra credit. Say what you're adding in your README before you start.

    Metadata filtering — let people narrow results by source or date.
    Conversational memory — let the next question build on the last one.
    A second embedding model — swap one in and write down what changed. This is the one stretch option that needs a package the default install doesn't have, and it's a large one — pip install 'sentence-transformers>=3.4,<3.5' brings PyTorch with it. Install it before class, not during, and expect your relevance cutoff to move: a different model means different distances.


🛠️ Setup

Setup happens before class, not during it. The environment setup page has the commands for your operating system and the exact versions to install. This section is the part that's specific to this project: getting your own copy of the starter and confirming it runs.
1. Fork the starter repo

    Fork the Unofficial Guide starter repo, then clone your fork locally:

    git clone https://github.com/YOUR-USERNAME/ai201-project1-unofficial-guide-starter-v2026.git
    cd ai201-project1-unofficial-guide-starter-v2026

    This fork is the repository you submit, both this unit and the next. Its commit history is what shows your criteria existed before your results did, so start it now rather than pasting your work into a fresh repo at the end.

2. Install the dependencies and add your key

    Create a virtual environment inside the repo, install what's in requirements.txt, and make your .env:

    macOS / Linux

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

    Windows (PowerShell)

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    copy .env.example .env

    Then open .env and paste your key in. .env.example names the exact variable and tells you where to get a free key.

    Activate the virtual environment every time you open a new terminal. You should see (.venv) at the start of your prompt. Installing into your system Python instead is the most common cause of "it worked yesterday."

3. Confirm it works

    Run the environment check that ships with the starter:

    python test.py

    The first run is slow — it downloads the embedding model, about 80 MB. If it doesn't pass, ask a TF or your AI tool for help.

RUNNING.md in the repo is your reference for everything else — every command, which command goes with which milestone, what each file does, and what to do when something breaks. Read it once now, and come back to it whenever you're stuck. You don't edit that file.

Two of the three pieces run entirely on your own machine and need no account at all — the embedding model and the vector store. Only the part that writes the final answer calls out to a service.

Your key is a secret. It goes in a .env file, which is already listed in .gitignore so it never reaches GitHub. Never paste it into your code, your README, or a message to anyone. If you think you've exposed it, say so in the help channel — keys can be replaced, and nobody is in trouble for it.

There are limits on how many questions you can send — a few per minute, and a few thousand per day. The starter handles the per-minute one for you: if you send questions faster than allowed, it waits a moment and tells you it's waiting. That pause is the starter doing its job, not a bug.

The daily limit is generous, and you'll only hit it by accident — a loop left running, or code that retries forever. If you see an error saying you're out of requests, stop the program, and it resets tomorrow.


Milestone 1: Pick your corpus and run the starter

⏰ ~25 min

Get the starter running against documents you picked, and watch it answer a question end to end before you change anything.

Seeing it work once, early, makes everything after this easier to debug. When something breaks in Milestone 3, you'll know it was working before you touched it.

    Pick one of the provided corpora. python app.py corpora lists them with a one-line description each, and corpora/README.md in your repo has the longer version. Choose the one you'd actually want to ask questions about. You can bring your own documents instead, but the provided ones are ready to go and are the default.

    Open three or four documents in corpora/ and read them. Are they short reviews or long guides? Is the useful information packed into one sentence or spread across a paragraph? You'll need this in Milestone 3, and it takes five minutes now.

    Index your corpus and ask it one question:

    python app.py index
    python app.py ask "is the housing lottery random?"

    That's the whole pipeline running end to end. To use a corpus other than the default, pass --corpus NAME or set CORPUS in config.py once — and re-run index after switching. Every command and flag is in RUNNING.md.

    The answer won't be good yet. That's fine — you're checking that it runs at all, and that your key works.

📍 Before you move on

The starter runs, ingests your corpus, and returns something when you ask it a question. Commit your work and push it to your fork — that's your first of at least four new commits.

✍️ Write this down: run python app.py --corpus advice_threads chunks -n 1 (regardless of which corpus you picked above) and write down the number it reports, just the digits, right before "chunks total." You'll need it for the special activity at the end of today's session.


Milestone 2: Write your acceptance criteria

⏰ ~75 min

An acceptance criterion is a sentence that says what "working" means, specifically enough that someone else could check it. Not "retrieval works" — that's an opinion. "For at least 4 of my 5 test questions, the top results include a chunk containing the answer" — that's a criterion. It names a number.

You're writing these now, before you test anything. That's the whole point. In the next unit you find out how you did against a standard you set when you couldn't yet know the answer.

Missing your own targets in the next unit does not cost you points. Setting a target so easy you can't miss it does.

⚠️ On AI tools: don't ask an AI to write your criteria. Use it to pressure-test them — "could someone check this without asking me what I meant?" is a good question to put to a model. A criterion you didn't write is one you can't defend.

    Write five test questions your system should be able to answer from your corpus. Make them specific enough to have a right answer. "What are good dining halls?" has no right answer. "What do students say about wait times at Commons during lunch?" does.

    They go in questions.py. Each question also takes an expects field — a word or short phrase a correct answer would have to contain. Fill that in now, while you still can't see any results, because in the next unit you'll be judging answers against it. Questions you keep in your head or in a scratch file won't run.

    Open criteria.md in your repo. Three criteria are already written:

    1. For at least 4 of my 5 test questions, the retrieved chunks include one
       that contains the answer.
    2. Every answer the system produces names at least one source document.
    3. When I ask a question my documents clearly don't cover, the relevance gate
       stops it and the system returns "I don't have enough information about
       that" — in at least 4 of 5 tries.

    Write two more. One should be about your chunks — how would you know if they're the right size? One is yours to choose: pick something you actually care about getting right. Each one needs a number or something a person could plainly observe.

    How to write acceptance criteria walks through this with examples. Run all five past the criteria self-check when you're done.

    Under each of the five, write one or two sentences on why that target and not a stricter or looser one. "I picked 4 of 5 because one of my questions is about a topic only two documents mention" is a real answer.

💬 Talk this through

In your breakout: read one of your criteria to your group — just the sentence, no context. Ask them how they'd test it from that alone.

If they can't say, you've found the thing to fix. This happens to almost everybody the first time.

Working on your own? Paste all five into Claude (or whichever AI tool you're using) and ask:

    "Here are five acceptance criteria for a retrieval system. For each one, tell me exactly how you would test it using only what the sentence says. Don't suggest improvements — just tell me what you'd do."

Any criterion it can't turn into a test is one a grader can't either. You still decide what to change.

📍 Before you move on

questions.py holds your five questions, each with its expects phrase. criteria.md has five numbered criteria, each naming a number or an observable outcome, with a reason underneath it. Commit both — the next unit reads them.



Milestone 3: Swap in your own chunker

⏰ ~60 mins

The starter chunks your documents in a plain, generic way: fixed 800-character windows that pay no attention to where sentences or paragraphs end. Depending on which corpus you picked, that either cuts your documents in the wrong places or barely cuts them at all. You're replacing it with a strategy that fits the documents you actually read in Milestone 1.

This is the decision the rest of the project rests on. Chunks that are too big bury the useful sentence in noise. Chunks that are too small lose the context that made the sentence mean anything. Most bad answers trace back to here.

    Look at what the starter's chunker actually did before you replace it. python app.py index prints a summary line: how many chunks it made, the average length, and the shortest and longest.

    Read that line against the corpus you picked. campus_life comes out as 88 documents and 88 chunks — the starter cuts at 800 characters and almost no post is that long, so it never splits anything. That isn't a bug, and it isn't nothing. It's your first real finding: for these documents, one post already is one chunk. What you have to decide is whether that's the right call, or whether a post holding two separate thoughts should come apart.

    The same chunker turns city_guides into 51 chunks from 14 documents, slicing straight through the labelled sections. Different corpus, different problem.

    Look at the shortest chunk it reports, too. On advice_threads the starter produces a 2-character chunk — the tail end of a document that didn't divide evenly. That's the "too small" example below, and it turns up on its own without you doing anything wrong.

    Decide your chunk size and overlap, and write down why before you code. Short reviews and long guides don't want the same numbers.

    Replace the starter's chunking function with yours. The rest of the pipeline stays as it is — you're changing one piece.

    Print five chunks and read them. For each one ask: could someone answer a question using only this, without reading what came before or after?

    A good chunk stands on its own:

        "Professor Smith's exams come from the lecture slides, not the textbook. Students say attending every class matters more than doing the readings. Midterms are curved; finals are not."

    A chunk that's too small is a fragment:

        "Professor Smith's exams come from the"

    A chunk that's too big covers four topics at once, so it matches every question a little and no question well.

    Paste those five chunks into your README under Sample Chunks. Label each one and name the file it came from. Also name the function that produced them.

💬 Talk this through

In your breakout: share one of your chunks — just the text, no explanation. Ask whether they could answer a question about your topic using only that.

If they hesitate, the chunk is carrying less than you think it is.

Working on your own? Paste three chunks into Claude and ask:

    "Here are three chunks from my documents. For each one, tell me what question it could answer on its own. If it can't answer anything on its own, say so and tell me what's missing."

🛑 If you're stuck

Chunks still coming out wrong after 30 minutes? Switch back to the starter's chunker and write down what you saw — empty chunks, HTML left in, whatever it was.

That's not giving up. It's a real observation about your pipeline, and in the next unit you'll have something concrete to test.

📍 Before you move on

Five chunks are in your README, labeled, with sources and the function name. They read as complete thoughts. Commit.



Milestone 4: Tune retrieval and ground the answers

⏰ ~85 min

Three jobs. Check that retrieval brings back chunks that actually relate to the question. Decide when it hasn't, and stop. Then make sure the model answers from those chunks instead of from what it already knows.

That middle one is the piece people skip. If you just ask the model nicely to admit when it doesn't know, it will sometimes ignore you and write something confident and wrong. Those answers are much harder to catch than obvious errors. Deciding in your own code when there's nothing worth answering from is more reliable than hoping.

    Run three of your five test questions through retrieval and print what comes back, with the distance for each. Read the chunks. Are they on topic, or do they just share a few words with your question?

    Adjust top-k if you need to. Too few and the right chunk may never come back at all. Too many and you bury it in loosely related material. Start at 4 or 5.

    Set your relevance cutoff. Run all five of your test questions and write down the best distance for each. Then ask five questions your documents clearly don't cover — something from a different world entirely — and write those down too. Five are already waiting in OUT_OF_SCOPE at the bottom of questions.py if you'd rather not invent your own. Five and not three because criterion 3 names a target of 4 of 5, and you can't report 4 of 5 against three questions.

    You should see two groups of numbers with a gap between them. Put your cutoff in the gap. The starter ships with 0.6, which is a reasonable place to begin; most corpora land somewhere between 0.45 and 0.75.

    Both directions cost you something, so this is a real decision:
    If your cutoff is 	What happens
    Too low (0.3) 	The system refuses questions it had the answer to
    Too high (0.9) 	It never refuses anything and makes things up

    Write down the number you picked and what your two groups looked like. That goes in your README.

    Read the grounding instruction the starter already sends as a second layer. It is GROUNDING_INSTRUCTION in generate.py: use only the documents provided, say so when they don't cover the question, name the file. python app.py ask "..." --show-prompt prints it, followed by the assembled prompt exactly as sent. Decide whether it is strict enough for your corpus and tighten it if your answers drift past the sources. The gate catches the clear misses; this catches the near ones.

    Grounded:

        "According to student reviews of Professor Smith (rmp_smith.txt), exams are curved and drawn from lecture material rather than the textbook."

    Not grounded — sounds right, cites nothing, came from the model's training data:

        "Professor Smith likely structures exams like most CS professors, focusing on core concepts and problem-solving."

    Paste one complete question and answer into your README under Sample Answer, with the source line visible.

💬 Talk this through

In your breakout: say what cutoff you picked and what your two groups of distances looked like.

You'll hear different numbers from different people. Ask someone why theirs is higher or lower than yours — the answer is usually something about their corpus, and it's the fastest way to understand what the number is actually doing.

Working on your own? Paste both sets of distances into Claude and ask:

    "Here are the best distances for five questions my documents cover, and five they don't. Where would you put the cutoff, and what would I get wrong at that number?"

The second half of that question is the important one.

🛑 If you're stuck

Retrieval still returning unrelated chunks after 30 minutes? Keep what you have and write down the distance scores you're seeing. Compare your best result against your worst — if they're close together, the store isn't distinguishing much, and knowing that is worth more right now than fixing it.

Bring it to your group. Someone else has probably seen the same thing.

📍 Before you move on

You can ask a question and get an answer that names its source. Asking something off-topic gets you an honest "I don't know" instead of a made-up answer. Commit.



Milestone 5: Write it up and submit

⏰ ~45 min

Most of your README is already written — you filled in sections as you went. This is finishing it and checking your repo is in shape for the next unit.

    Fill in the two README sections you haven't touched yet: What This Does and How I Used AI.

    For How I Used AI, describe two specific moments. What you asked for, what came back, and what you changed about it. "I asked Claude to write the chunking function from my notes. It ignored the overlap, so I added that myself" is the level of detail we're looking for.

    Check your repo one more time: criteria.md is there, the README has all five sections, and you have at least four new commits. Push everything to your fork, then submit your fork's URL — not the CodePath starter's.

📍 Before you move on

Your repository URL is submitted. Write it down somewhere you'll find it in the next unit — you're submitting the same one, and a repo you delete and recreate loses the commit history that protects you if a grade is ever disputed.



📬 Submitting Your Project

Submit your GitHub repository URL through the Course Portal. Your repo needs these things in it:
File 	What's in it
criteria.md 	Five numbered criteria, each with a target and a reason
README.md 	The five sections below
— 	At least four new commits from this unit

Your README, section by section:
Section 	What goes in it
What This Does 	Three or four sentences: your corpus, and the kinds of questions your system answers
Chunking Strategy 	Your chunk size, your overlap, and what about your documents made you pick them. If you changed your mind partway through, say so and say why
Sample Chunks 	Five chunks pasted as text, each labeled, with its source file and the function that made it
Sample Answer 	One full question and answer pasted as text, with the source line visible. Plus your relevance cutoff, and what your two groups of distances looked like
How I Used AI 	Two specific moments — what you asked, what you got, what you changed

Paste everything as text. No screenshots, no video. A typed table of results gets full credit; a picture of the same table gets none, because the grader can't read it.

🗺️ How It's Graded

The full breakdown of graded features and points is on the course grading page.

This unit's grade comes from three questions:

    Did you build the thing we asked for? A structural check, not a judgment of whether it works well.
    Does your README describe the system you actually built?
    Are your criteria real criteria — specific, testable, each naming a target?

Whether your system works is not graded in this unit, and missing your own targets in the next unit won't cost you points. What's graded is whether you set an honest standard and tested against it honestly.