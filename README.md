# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard guesses whether a piece of writing is AI-generated, and lets
the writer appeal.

1. **`POST /submit`** receives `text` and `creator_id`.
2. **Input check** (`app.py::submit`) rejects bad requests before any model
   runs: non-object body or missing field (400), text under 50 characters
   (400) or over 20,000 (413). Rejections are logged.
3. **`content_id`** (`uuid.uuid4()`) links the decision, log and any appeal.
4. **Signal one** (`detector.py::model_signal`): how predictable gpt2 finds
   the text, 0–1.
5. **Signal two** (`stylometry.py::style_signal`): the text's shape, 0–1.
6. **Combine and label** (`scoring.py`): one `confidence` score, then a guess
   (`ai` / `human` / `unsure`) and the sentence a reader sees.
7. **Log, then respond** (`audit.py::log_decision`). The writer can send the
   `content_id` to `POST /appeal` to move the item to `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Predictability: gpt2's perplexity on the first 400
tokens, mapped to 0–1 by `1 / (1 + (perplexity / 45) ^ 1.6)`. Lower
perplexity = higher AI score.

**Why that might differ between human and AI writing:** Models write by
picking likely next words; people make odder choices.

**What it can't see:** Predictable isn't machine-written. Plain or formal
human writing scores as AI: the Gettysburg Address scored **0.73**, above my
AI samples. AI text with rare words scores as human. Nothing past 400 tokens
is read.

### Signal two — the style signal

**What it measures:** The text's shape, via three measures:

| Measure | Computed as | AI when | Weight |
|---|---|---|---|
| Sentence-length spread | stdev ÷ mean of words per sentence | low | 0.50 |
| Type-token ratio | unique ÷ total words, per 50-word window | high | 0.35 |
| Punctuation density | `, ; : — – ( ) " …` per word | low | 0.15 |

Each is scaled to 0–1 between a human value and an AI value (spread
0.65 → 0.25, TTR 0.70 → 0.90, punctuation 0.10 → 0.04), then weighted. With
fewer than 2 sentences or 50 words, that measure counts as 0.5.

**Why that might differ between human and AI writing:** AI prose tends toward
even sentence lengths; human writing is lumpier. On my five calibration texts,
spread separated the groups, punctuation barely did, and type-token ratio ran
*opposite* to the starter's hint (AI used more varied words), so high TTR
counts as AI. Five texts is a first guess, not a measurement.

**What it can't see:** Meaning. Splitting sentences, typos, synonyms or extra
dashes all move it. Poems, lists and short posts break it.

**Why they're two different signals:** One asks "would a model say this?",
the other "does it look like model output?". Typos fool only the style
signal; rare words fool only the model. Plain human writing can fool both.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals equally. If either one is below 0.5
(leans human), cap the result at 0.69, so a disagreement can be "unsure" but
never "AI". The human label isn't capped, because only a wrong AI label
accuses someone.

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Weights (model / style) | 0.5 / 0.5 | `config.WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL` |
| Cap applies when a signal is below | 0.5 | `config.DISAGREE_BELOW` |
| Cap | 0.69 (`AI_THRESHOLD - 0.01`) | `scoring.py::combine_signals` |
| Human / unsure / AI | < 0.35 / 0.35–0.70 / ≥ 0.70 | `config.HUMAN_THRESHOLD`, `AI_THRESHOLD` |

Equal weights because neither signal has earned more trust. The AI line moves
up from 0.65 to 0.70 because that's the label that costs a person something.
The cost: lightly edited AI (0.68) lands in "unsure", and a writer who fools
*both* signals still gets labeled AI.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

The Gettysburg Address: **0.73** model (reads as AI), **0.45** style (leans
human). It averages to 0.59, "unsure", and because style is under 0.5 the cap
would hold it at 0.69 or below even if the model scored it higher. Never "AI".


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

Ranges are the ones `scoring.label_ranges()` prints, so they can't drift from
`config.py`. No number appears in any label — the reader gets a sentence.

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was probably written by a person. Nothing further is needed." |
| unsure | 0.35 – 0.70 | "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it." |
| high-confidence AI | 0.70 – 1.00 | "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it." |

**Where it lives:** `scoring.py::score_to_label`

**Why I worded the "unsure" one this way:**

It names *our* failure, not a property of the writing. "This text has some
AI-like qualities" sounds like a soft accusation with no way to answer it —
the reader hears "we found something" and has to prove a negative. "We could
not tell" says the check ran out of road, which is the true thing and is
nobody's fault. The sentence "This is not a finding against you" is there
because a reader who has written every word themselves will assume the worst
otherwise, and the appeal line is last so the way out is the thing they read
on the way out.

The AI label gets an appeal line too, for the same reason: it's the only
label that costs a person anything. The human label doesn't, because nobody
needs to contest being believed.

**All three are reachable** — here is real text producing each one, through
the running service. Combined scores land at 0.25, 0.35 and 0.71, one in each
band, so there's no gap:

| Text submitted | model_score | style_score | confidence | Label produced |
|---|---|---|---|---|
| "I lost the receipt. Again. My brother-in-law Teodor, who once drove a forklift…" | 0.1911 | 0.3129 | 0.2520 | high-confidence human |
| "The meeting ran long on Thursday. We talked about the budget and then about hiring…" | 0.3367 | 0.3702 | 0.3534 | unsure |
| "The system works well and handles most cases correctly. Users generally find it easy…" | 0.6418 | 0.7725 | 0.7071 | high-confidence AI |

Worth saying plainly: the text that got the AI label is plain, short-sentenced
human-style writing about a product. That is the blind spot from Signal one
showing up in the labels exactly where the detector doc said it would — and
it's the appeal in the Sample Run below.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "The system works well and handles most cases correctly. Users generally find it easy to use and understand. The interface is clean and the results are provided quickly. Overall the tool provides good value for most teams. It is reliable and the documentation is clear. Support is responsive when issues arise.", "creator_id": "ivan"}'
```

```json
{
  "appeal": "Think we got this wrong? POST /appeal with this content_id.",
  "confidence": 0.7071,
  "content_id": "8c0d564e-3288-4c0b-ab5f-32fc6e6e865b",
  "guess": "ai",
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "model_score": 0.6418,
  "status": "decided",
  "style_score": 0.7725
}
```

**An appeal**

Using the `content_id` from the submission above — the plain-English product
blurb that got accused.

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "8c0d564e-3288-4c0b-ab5f-32fc6e6e865b", "reasoning": "I wrote this myself. It is a product update for our internal wiki, so I kept the sentences short and plain on purpose because half the team reads English as a second language. Writing clearly should not count against me."}'
```

```json
{
  "content_id": "8c0d564e-3288-4c0b-ab5f-32fc6e6e865b",
  "creator_id": "ivan",
  "message": "Thanks — your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
  "original_guess": "ai",
  "original_label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "status": "under_review"
}
```

A `content_id` that doesn't exist gets a 404 rather than failing quietly, and
the miss is logged:

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "not-a-real-id", "reasoning": "testing"}'
```

```json
{
  "error": "unknown_content_id",
  "message": "No decision found for content_id \"not-a-real-id\". Check the id from your /submit response."
}
```

**What the log shows afterwards**

The log is append-only, so the original decision stays exactly where it was
and the appeal sits after it. Reading top to bottom you can see what was
decided, that it was challenged, and in what order.

```bash
$ curl.exe "http://127.0.0.1:5000/log?limit=5"
```

```json
{
  "count": 5,
  "entries": [
    {
      "combined_score": 0.7071,
      "content_id": "8c0d564e-3288-4c0b-ab5f-32fc6e6e865b",
      "creator_id": "ivan",
      "guess": "ai",
      "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
      "model_score": 0.6418,
      "status": "decided",
      "style_score": 0.7725,
      "timestamp": "2026-10-30T20:57:05+00:00"
    },
    {
      "combined_score": 0.252,
      "content_id": "a9eedfe8-0c8b-47eb-be21-0aec56a1d8b2",
      "creator_id": "ivan",
      "guess": "human",
      "label": "We think this was probably written by a person. Nothing further is needed.",
      "model_score": 0.1911,
      "status": "decided",
      "style_score": 0.3129,
      "timestamp": "2026-10-30T20:57:21+00:00"
    },
    {
      "combined_score": 0.3534,
      "content_id": "7ff52c9d-be33-468a-b715-c4adbfc6aef3",
      "creator_id": "ivan",
      "guess": "unsure",
      "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "model_score": 0.3367,
      "status": "decided",
      "style_score": 0.3702,
      "timestamp": "2026-10-30T20:57:22+00:00"
    },
    {
      "content_id": "8c0d564e-3288-4c0b-ab5f-32fc6e6e865b",
      "creator_id": "ivan",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is a product update for our internal wiki, so I kept the sentences short and plain on purpose because half the team reads English as a second language. Writing clearly should not count against me.",
      "status": "under_review",
      "timestamp": "2026-10-30T20:57:40+00:00"
    },
    {
      "content_id": "not-a-real-id",
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "unknown_content_id",
      "status": "rejected",
      "timestamp": "2026-10-30T20:57:40+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1 — the Milestone 5 functions**

- *What I asked for:* Fill in `scoring.py::score_to_label`, wire it into the
  `/submit` response, and build `app.py::appeal`. I gave it the three label
  phrasings I wanted and left the code to it.

- *What came back:* More than I asked for, and it flagged why before writing
  anything. Two things I had missed:

  1. `/submit` was still at Milestone 3 — it never called `style_signal` or
     `combine_signals`, so there was no combined score for `score_to_label`
     to read. Milestone 5 was not reachable without finishing Milestone 4's
     wiring first, so it did both.
  2. My README already described a combining rule the code didn't have: the
     0.69 disagreement cap, `config.DISAGREE_BELOW`, and an `AI_THRESHOLD`
     of 0.70 while `config.py` still said 0.65. I had written the rule down
     and never implemented it. It built the code to match what I'd claimed.

  On `/appeal` it added two things I hadn't specified: taking `creator_id`
  off the original log entry instead of trusting whatever the request body
  says, and returning a 404 with a logged rejection for an unknown
  `content_id` rather than failing silently.

- *What I changed:* 
  I took the extra scope once I'd read the reason for it, but not the
  numbers on trust. `scoring.label_ranges()` prints 0.00–0.35 / 0.35–0.70 /
  0.70–1.00 with no gap, and a deliberate 0.99 model / 0.45 style split came
  back as 0.69 "unsure" rather than "ai" — so the cap I'd described in the
  README does bite. Then I submitted three real texts and got one of each
  label, which is the evidence in Label Variants above.

**Moment 2 — the label wording**

- *What I asked for:* I wrote the three labels myself as short phrases —
  "Probably written by a human", "Probably written by an ai", "Could be
  written by an ai or human" — and asked for them as full sentences for
  someone who has never heard the word "threshold".

- *What came back:* It kept my three meanings and made each a sentence, then
  added two things I hadn't asked for and argued for both. The unsure label
  got "This is not a finding against you — our check simply wasn't able to
  decide", on the reasoning that the wording should name *our* failure rather
  than a property of the writing: "this text has AI-like qualities" sounds
  like a soft accusation the reader has to disprove, while "we could not
  tell" is the true thing and is nobody's fault. The AI and unsure labels
  both got an appeal line; the human one didn't, because nobody needs to
  contest being believed.

- *What I changed:* 
**One thing I didn't let it change:** my Signals and Scoring section claims
the Gettysburg Address scores 0.73 model / 0.45 style. Re-run on an excerpt it
came out 0.7109 / 0.4787 — the combined 0.59 and the "unsure" conclusion hold
either way. It flagged the gap and left my numbers alone rather than
overwriting a measurement I took with one taken on different input, which was
the right call: I don't know which text it used.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
