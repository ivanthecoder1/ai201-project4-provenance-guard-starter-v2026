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

**My limits:** 5 per minute, 50 per day (`config.py`, applied to
`POST /submit` only)

**Why those numbers and not others:**
- **5 a minute:** a real writer submits a piece, maybe fixes a typo and
  resubmits. That's two or three in a minute at most, so 5 leaves room for
  retries. A script mapping my thresholds wants hundreds a minute.
- **50 a day:** more pieces than one person writes in a day. A script sending
  1,000 variations from one `creator_id` would need 20 days.
- **Why not lower:** at 1–2 a minute, a writer retrying after a network error
  would hit a 429, and the writer is who this site is for.

**What a caller counts as:** the `creator_id`, falling back to the caller's
address when there isn't a usable one (`app.py::rate_limit_key`). The weakness:
`creator_id` isn't verified, so a script that invents a new one per request is
never limited. The attack set does exactly that, one `creator_id` per row.
Limiting by address instead would catch that script, but would also lump
everyone behind one school or office network together.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

10 of 15 were rate limited (`results/flood_2026-11-08_1641.md`). Each 429 is
in the audit log:

```json
{"creator_id": "flood_tester", "event": "rejected", "limit": "5 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-08T21:41:26+00:00"}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

56 attacks, `results/attack_run_2026-11-08_1646.md`. **39 held, 17 broke.**

How I marked them: an attack **broke** if it got the outcome it was going for.
Evasion and AI-text injection broke if the AI text was *not* labeled AI
("unsure" counts as getting past the detector). False-positive attacks broke
if real human writing was labeled AI. Malformed requests broke if the service
judged junk instead of refusing it.

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 2 | 8 |
| false_positive | 8 | 4 | 4 |
| prompt_injection | 6 | 4 | 2 |
| malformed | 20 | 17 | 3 |
| flood_same_creator | 12 | 12 | 0 |
| **Total** | **56** | **39** | **17** |

| ID | Targeting | Status | Guess | Model | Style | Combined | Verdict | What happened |
|---|---|---|---|---|---|---|---|---|
| EV01 | signal two: typos raise word variety | 200 | unsure | 0.16 | 1.00 | 0.58 | **BROKE** | typos fooled signal one (0.16), not signal two (1.0) |
| EV02 | signal two: broken-up sentences raise length spread | 200 | unsure | 0.59 | 0.49 | 0.54 | **BROKE** | "Really." pushed style under 0.5, so the cap held it below AI |
| EV03 | signal two: a pasted quotation changes the shape | 200 | unsure | 0.67 | 0.72 | 0.69 | **BROKE** | 0.6915, just under the 0.70 line |
| EV04 | signal one: unusual words raise perplexity | 200 | ai | 0.61 | 1.00 | 0.81 | **HELD** | rare words dropped the model only to 0.61 |
| EV05 | both signals: heavy human editing pass | 200 | human | 0.32 | 0.38 | 0.35 | **BROKE** | labeled human; both signals fooled |
| EV06 | signal two: one very long sentence and one very short | 200 | unsure | 0.57 | 0.41 | 0.49 | **BROKE** | style 0.41 triggered the cap |
| EV07 | signal two: padding with punctuation | 200 | unsure | 0.59 | 0.50 | 0.55 | **BROKE** | both signals pulled toward the middle |
| EV08 | signal one: text below the token window | 200 | unsure | 0.25 | 0.78 | 0.52 | **BROKE** | too short for either signal to judge |
| EV09 | both: AI text with a human opening paragraph bolted on | 200 | ai | 0.70 | 0.72 | 0.71 | **HELD** | 0.71, only just over the line |
| EV10 | signal two: repeated stanza structure | 200 | unsure | 0.98 | 0.47 | 0.69 | **BROKE** | model 0.98, but style 0.47 triggered the cap |
| FP01 | plain, clear human writing with no flourishes | 200 | unsure | 0.62 | 0.58 | 0.60 | **HELD** | unsure, not accused |
| FP02 | human writing in a formal register | 200 | ai | 0.74 | 0.77 | 0.76 | **BROKE** | formal writing labeled AI; both signals agreed |
| FP03 | a non-native English speaker writing carefully | 200 | ai | 0.81 | 0.76 | 0.78 | **BROKE** | non-native writer labeled AI; both signals agreed |
| FP04 | a student essay written to a rubric | 200 | ai | 0.83 | 0.72 | 0.77 | **BROKE** | rubric essay labeled AI; both signals agreed |
| FP05 | technical documentation written by a person | 200 | ai | 0.80 | 0.62 | 0.71 | **BROKE** | documentation labeled AI; both signals agreed |
| FP06 | a person imitating a formal template | 200 | unsure | 0.88 | 0.41 | 0.65 | **HELD** | style 0.41 triggered the cap; the model said 0.88 |
| FP07 | human writing that repeats a phrase deliberately | 200 | unsure | 0.88 | 0.15 | 0.52 | **HELD** | style 0.15 triggered the cap; the model said 0.88 |
| FP08 | very short genuine human submission | 400 | — | — | — | — | **HELD** | not accused, but a real writer got a 400 (under 50 characters) |
| PI01 | instruction to ignore the check | 200 | unsure | 0.46 | 0.33 | 0.39 | **BROKE** | AI text escaped as unsure; the instruction raised perplexity |
| PI02 | instruction disguised as a system message | 200 | human | 0.20 | 0.31 | 0.26 | **BROKE** | AI text labeled human; the header dropped the model to 0.20 |
| PI03 | instruction wrapped in the writer's voice | 200 | ai | 0.59 | 0.85 | 0.72 | **HELD** | still labeled AI |
| PI04 | attempt to make the label text hostile | 200 | unsure | 0.50 | 0.65 | 0.57 | **HELD** | labels are fixed strings and the text is never echoed back |
| PI05 | attempt to inject into the audit log | 200 | unsure | 0.64 | 0.40 | 0.52 | **HELD** | log line stayed valid JSON; the injected fields were escaped |
| PI06 | instruction plus real human text | 200 | unsure | 0.56 | 0.60 | 0.58 | **HELD** | human text, not accused |
| MF01 | text is only whitespace | 400 | — | — | — | — | **HELD** | 400 |
| MF02 | text is a single character | 400 | — | — | — | — | **HELD** | 400 |
| MF03 | text is control characters | 400 | — | — | — | — | **HELD** | 400 |
| MF04 | text is only punctuation | 400 | — | — | — | — | **HELD** | 400 |
| MF05 | text is a very long single word | 200 | ai | 1.00 | 0.57 | 0.79 | **BROKE** | junk scored as confident AI (model 1.00) |
| MF06 | text is emoji only | 200 | ai | 1.00 | 0.57 | 0.79 | **BROKE** | emoji scored as confident AI (model 1.00) |
| MF07 | text is right-to-left script | 200 | ai | 0.91 | 0.57 | 0.74 | **BROKE** | non-Latin script labeled AI; style can't count its words |
| MF08 | text is 60,000 characters | 413 | — | — | — | — | **HELD** | 413 |
| RQ01 | no text field at all | 400 | — | — | — | — | **HELD** | 400 |
| RQ02 | no creator_id | 400 | — | — | — | — | **HELD** | 400 |
| RQ03 | text is a number | 400 | — | — | — | — | **HELD** | 400 |
| RQ04 | text is a list | 400 | — | — | — | — | **HELD** | 400 |
| RQ05 | text is null | 400 | — | — | — | — | **HELD** | 400 |
| RQ06 | creator_id is an object | 400 | — | — | — | — | **HELD** | 400 |
| RQ07 | body is a JSON array, not an object | 400 | — | — | — | — | **HELD** | 400 |
| RQ08 | body is unparseable JSON | 400 | — | — | — | — | **HELD** | 400 |
| RQ09 | body is empty | 400 | — | — | — | — | **HELD** | 400 |
| RQ10 | body is form-encoded, not JSON | 429 | — | — | — | — | **HELD** | 429 before reaching the route (counted against my address) |
| RQ11 | body is JSON claiming to be plain text | 429 | — | — | — | — | **HELD** | 429 before reaching the route (counted against my address) |
| RQ12 | deeply nested JSON | 400 | — | — | — | — | **HELD** | 400 |
| FL01_01 | 20 rapid submissions from one creator | 200 | human | — | — | 0.30 | **HELD** | 200 |
| FL01_02 | 20 rapid submissions from one creator | 200 | human | — | — | 0.30 | **HELD** | 200 |
| FL01_03 | 20 rapid submissions from one creator | 200 | human | — | — | 0.30 | **HELD** | 200 |
| FL01_04 | 20 rapid submissions from one creator | 200 | human | — | — | 0.30 | **HELD** | 200 |
| FL01_05 | 20 rapid submissions from one creator | 200 | human | — | — | 0.30 | **HELD** | 200 |
| FL01_06 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_07 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_08 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_09 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_10 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_11 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_12 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

FP03 and FP02 (real writers labeled AI), MF07 (non-Latin script labeled AI),
PI02 (AI text labeled human after an injected header), EV01 and EV05 (evasions
that worked), EV10 and FP07 (the cap deciding the outcome), PI05 (log injection
that stayed one valid line), and one rate-limit rejection from the flood rows.

```json
{"timestamp": "2026-11-08T21:45:59+00:00", "content_id": "6684a6fe-7f84-4845-be47-7e357bbf392f", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.7612, "combined_score": 0.7832, "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:45:59+00:00", "content_id": "a88c0ea6-6a25-4b36-a24c-806aebbc21ad", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.7719, "combined_score": 0.7553, "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:46:01+00:00", "content_id": "71312549-c37d-4a51-8dc7-f40cafc554ca", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.575, "combined_score": 0.7407, "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:46:00+00:00", "content_id": "75140f72-d06a-4b3d-a499-ed194270dc55", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3139, "combined_score": 0.2591, "label": "We think this was probably written by a person. Nothing further is needed.", "status": "decided"}
{"timestamp": "2026-11-08T21:45:58+00:00", "content_id": "4aa9aa7e-2b93-4c1c-aaef-9bd42f3ef9af", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 1.0, "combined_score": 0.5817, "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:45:58+00:00", "content_id": "ba30ec07-b431-46e1-b964-7db60fb46b3d", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.3765, "combined_score": 0.3488, "label": "We think this was probably written by a person. Nothing further is needed.", "status": "decided"}
{"timestamp": "2026-11-08T21:45:59+00:00", "content_id": "c0ca0c27-a654-467a-b200-afc451de43fa", "creator_id": "attacker_EV10", "guess": "unsure", "model_score": 0.9792, "style_score": 0.4701, "combined_score": 0.69, "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:46:00+00:00", "content_id": "64b9c27f-29bb-41e1-b6b6-a4a16aa3d367", "creator_id": "attacker_FP07", "guess": "unsure", "model_score": 0.8816, "style_score": 0.15, "combined_score": 0.5158, "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:46:00+00:00", "content_id": "858ce158-4c82-47e8-9329-2b7ed03d586f", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.3982, "combined_score": 0.5192, "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.", "status": "decided"}
{"timestamp": "2026-11-08T21:46:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03: a non-native English speaker writing carefully about their first month
in a new country, labeled **high-confidence AI at 0.78**. Both signals agreed
(model 0.81, style 0.76), so my disagreement cap never triggered. This is the
exact writer my Milestone 1 trace was about, and the rule I wrote to protect
them can't help when both signals are wrong the same way.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Produced by `run_eval.py::main` (criteria 1, 2, 3, 5; inputs in `scenarios.py`)
and `run_appeals.py::main` (criterion 4, which needs a submission before it can
appeal, so `run_eval.py` can't test it). Raw output:
`results/run_2026-11-08_1708_before.md` and
`results/appeals_2026-11-08_1708_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labeled AI | ≤ 1 of 10 | 1/10 | 1/10 | 1/10 | MET |
| 2. AI avg − human avg confidence | ≥ 0.20 | 0.41 | 0.41 | 0.41 | MET |
| 3. All three labels returned | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeals recorded / unknown ids 404 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | MET |
| 5. Bad input rejected, no decision logged | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

All three trials were identical, number for number. Neither signal is random,
so that's expected.

How I decided each one:
1. **MET, at the limit.** Piece 2 ("Can I please get some assistance with this
   story? This is my first time doing QA work") was labeled AI at 0.74 in every
   trial; nothing else was. One more and it's a miss.
2. **MET.** AI samples averaged 0.83, human samples 0.42: a gap of 0.41.
3. **MET.** AI, human and unsure came back for the three inputs aimed at them,
   every trial. `scoring.label_ranges()` gives human 0.00–0.35, unsure
   0.35–0.70, AI 0.70–1.00 (`score_to_label` uses `< 0.35` and `>= 0.70`, so
   no gaps or overlaps).
4. **MET.** Every real appeal returned 200 `under_review` and appeared in
   `GET /log` with the reasoning word for word; every unknown id got a 404 and
   no appeal entry.
5. **MET.** 8 × 400 and 2 × 413 each trial; the log holds 30 `rejected`
   entries for these creator_ids and 0 decisions.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Criterion 1, trial 1 (`run_eval.py::main` → `app.py::submit`):

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6088,
    "model_score": 0.3925,
    "style_score": 0.825,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "Thanks for sending over the details for the Software Engineer role at "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7364,
    "model_score": 0.6477,
    "style_score": 0.825,
    "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
    "sent": "Can I please get some assistance with this story? This is my first tim"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3352,
    "model_score": 0.0954,
    "style_score": 0.575,
    "label": "We think this was probably written by a person. Nothing further is needed.",
    "sent": "I am writing to follow up on the service request I submitted on 6/11/2"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3809,
    "model_score": 0.2136,
    "style_score": 0.5482,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "mochie is so cutee. She is rolling on the floor right now"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6247,
    "model_score": 0.6744,
    "style_score": 0.575,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "Thank you for getting back to me about this opportunity"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.612,
    "model_score": 0.7661,
    "style_score": 0.4579,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "This is great, thank you! I did end up picking up the folder in place "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5096,
    "model_score": 0.2503,
    "style_score": 0.7688,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "yo, do you wanna play some matches of pokemon? I need to rank up to ma"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3664,
    "model_score": 0.4079,
    "style_score": 0.325,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "May I please get approval for this report? Thank you!"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5598,
    "model_score": 0.5447,
    "style_score": 0.575,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "I can't make it to the lunch today because I have a conflict"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6702,
    "model_score": 0.5624,
    "style_score": 0.7779,
    "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
    "sent": "i am ready to go home, i feel so tired. I wanna go sleep in my bed"
  }
]
```

Criterion 2, trial 1, confidences only (full JSON in the results file):

```json
{
  "ai_samples": [
    0.8496,
    0.8463,
    0.8343,
    0.8186,
    0.8093
  ],
  "human_samples": [
    0.4358,
    0.2783,
    0.3852,
    0.5281,
    0.4637
  ]
}
```

Criterion 3, trial 1 (`run_eval.py::main` → `app.py::submit`):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7529,
    "model_score": 0.7052,
    "style_score": 0.8005,
    "sent": "Reading offers numerous benefits that extend far beyond simple enterta"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2617,
    "model_score": 0.461,
    "style_score": 0.0624,
    "sent": "You don't know about me without you have read a book by the name of Th"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5872,
    "model_score": 0.7273,
    "style_score": 0.4472,
    "sent": "Four score and seven years ago our fathers brought forth on this conti"
  }
]
```

Criterion 4, trial 1, first real appeal and first unknown id
(`run_appeals.py::main` → `app.py::appeal`):

```json
[
  {
    "kind": "real",
    "content_id": "e31c0ec7-da02-437a-9c1a-6b00140ac853",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "e31c0ec7-da02-437a-9c1a-6b00140ac853",
      "creator_id": "appeal_t1_1",
      "message": "Thanks — your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you — our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 1: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-dc623c12-475c-4b89-a407-abcc753e5a65",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-dc623c12-475c-4b89-a407-abcc753e5a65\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  }
]
```

Criterion 5, trial 1, status codes (`run_eval.py::main` → `app.py::submit`):

```json
[
  {
    "sent": "{\"creator_id\": \"eval_bad_missing_1\"}",
    "status": 400
  },
  {
    "sent": "{\"creator_id\": \"eval_bad_missing_2\"}",
    "status": 400
  },
  {
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_notstr_1\"}",
    "status": 400
  },
  {
    "sent": "{\"text\": [\"not\", \"a\", \"string\"], \"creator_id\": \"eval_bad_not",
    "status": 400
  },
  {
    "sent": "(empty text)",
    "status": 400
  },
  {
    "sent": "   \n\t  ",
    "status": 400
  },
  {
    "sent": "Too short to judge.",
    "status": 400
  },
  {
    "sent": "  Also short, even with padding.   ",
    "status": 400
  },
  {
    "sent": "word word word word word word word word word word word word ",
    "status": 413
  },
  {
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "status": 413
  }
]
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

**No criterion missed, so there are no criterion diagnoses.** The 17 broken
attacks come down to five patterns. Style measures below are from
`stylometry.py`, computed on the attack text.

**Pattern A: plain human writing reads as AI on *both* signals (4 attacks:
FP02, FP03, FP04, FP05).** Formal report, non-native writer, rubric essay,
documentation: all labeled AI at 0.71–0.78.
- *Stage:* signal two and signal one together, with the combining rule unable
  to help.
- *Mechanism:* signal two scores these as AI on two measures. Their sentences
  are even (spread 0.24–0.37, near my AI end of 0.25), and they have almost no
  mid-sentence punctuation (0.00–0.03 per word). My punctuation scale treats
  anything below 0.04 as fully AI. But my AI calibration samples had *more*
  punctuation (0.05–0.08) than these human texts, so this part of the scale has
  no evidence behind it. Signal one finds the plain vocabulary predictable
  (0.74–0.83). Both signals are above 0.5, so the disagreement cap never fires,
  and the average clears 0.70.
- The same thing nearly sank criterion 1: my piece 2 ("Can I please get some
  assistance...") scored style 0.83 (spread 0.08, punctuation 0.00) and model
  0.65, giving 0.74 and an AI label. This is the false positive I traced in
  Milestone 1, and the worst outcome of the run.

**Pattern B: text with no words gets a confident AI label (3 attacks: MF05,
MF06, MF07).** 4,000 a's, emoji, and right-to-left script all scored
0.74–0.79.
- *Stage:* the route, then signal two.
- *Mechanism:* the route checks *characters* (at least 50), not words, so these
  get through. `stylometry.words()` only matches `[a-z0-9']`, so it finds 0
  words in emoji or Arabic script and 1 in the a's. Spread and word variety
  fall back to 0.5, but `punctuation_density` returns 0.0 for zero words,
  which my scale reads as fully AI. That's why the style signal is exactly
  0.575 on all three. Signal one finds repeated tokens extremely predictable
  (0.91–1.00). Neither signal is below 0.5, so no cap.

**Pattern C: reshaped AI text slides into "unsure" (4 attacks: EV02, EV06,
EV07, EV10).** The text changes shape but keeps the same words.
- *Stage:* signal two, then the combining rule.
- *Mechanism:* each attack moves a measure signal two counts as human. In EV02,
  the inserted "Really." sentences push spread to 0.85. EV06's one long and one
  short sentence push spread to 1.19. EV10's repeated stanza drops word
  variety to 0.50, which my reversed direction counts as human. EV07's
  semicolons merge everything into one sentence (spread falls back to neutral)
  and raise punctuation to 0.22. Style lands at 0.41–0.50. In EV02, EV06 and
  EV10 that is under 0.5, so the cap holds the score at 0.69 or below even
  when the model says 0.98 (EV10). This is the trade I chose in the previous
  unit: when the signals disagree, unsure rather than an accusation.

**Pattern D: added text confuses signal one (4 attacks: EV01, EV08, PI01,
PI02).**
- *Stage:* signal one.
- *Mechanism:* gpt2 scores how predictable the whole text is. Typos (EV01),
  a 10-word text (EV08) and an injected instruction line (PI01's "ignore all
  previous instructions", PI02's fake "SYSTEM:" header) are all unusual token
  sequences. They raise perplexity and drop the model score to 0.16–0.46.
  Nothing in my service follows instructions; the injection worked only
  because it is odd text. In EV01, signal two actually scored the text *more*
  AI (1.00): typos raise word variety, and I set high variety to count as AI.
  The model dropped below 0.5, so the cap held the result at "unsure". In
  PI02, both signals fell below 0.5 (the short instruction lines also raised
  spread), so it was labeled human.

**Pattern E: near misses on the threshold (2 attacks: EV03, EV05).**
- *EV03* (pasted quotation) scored 0.6915, 0.0085 under the AI line. *Stage:*
  the label mapping. The quotation lowered the model score a little (0.67),
  enough to miss 0.70.
- *EV05* (heavy human editing) scored 0.35, labeled human. *Stage:* both
  signals. This one may not be a detector failure: the editing pass changed the
  actual words and sentence shapes, so the text is now substantially
  human-written.

**The pattern across all of them.** A and B are the costly ones: 7 attacks
that ended in a confident wrong AI label, all caused by signal two leaning AI
when it has no real evidence, and by the cap only covering disagreement. C, D
and E are AI text getting through as "unsure" or "human". That's the cheaper
mistake, and mostly the trade my combining rule chose on purpose.

**All five criteria were met, so were my targets too low?** Partly.
- **Criterion 2 was too easy.** The gap was 0.41 against a target of 0.20,
  and four of the five human samples still came back "unsure", not "human".
  An average gap hides that. "Every human sample scores below every AI sample"
  would have been a real test. This is the criterion I'd tighten.
- **Criterion 1 passed, but its test was weaker than the attack set.** My 10
  pieces are mostly 10–30 words, so signal two had little to measure. The
  attack set's longer plain human writing was labeled AI 4 times out of 8. It
  passed at exactly the limit (1 of 10), with the same mechanism as Pattern A.
- **Criteria 4 and 5 test code paths, not judgment.** They were never likely to
  fail, and they didn't.

No criterion turned out unmeasurable, so I haven't revised any in
`criteria.md`.

---

## The Improvement

**What I changed:** one thing, the punctuation measure inside signal two
(`stylometry.py::style_signal`, new constant `PUNCT_LOW_RAMP`). Before, any
punctuation density below 0.04 counted as fully AI. Now the scale has two sides:
it peaks at 0.04 and falls to fully *human* at 0.00. Above 0.04 nothing
changed. The weights, thresholds, cap and labels are all the same.

**Which diagnosis pointed at it:** Pattern A. The human texts labeled AI had
0.00–0.03 punctuation per word, and every AI sample I've measured had at least
0.045. So "almost no commas" was never evidence of AI; in my data it's evidence
of a person. I simulated four options on the logged scores before choosing:
treating low punctuation as "no evidence" fixed less, and dropping punctuation
to "human" everywhere fixed more accusations but also let 2 more AI texts
(EV09, PI03) through. The two-sided scale was the only one that fixed
accusations without letting new AI text through.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

`results/attack_run_2026-11-08_1719_after.md`, marked with the same rule as the
before run. **40 held, 16 broke** (before: 39 held, 17 broke).

| Family | Before held / broke | After held / broke |
|---|---|---|
| evasion | 2 / 8 | 2 / 8 |
| false_positive | 4 / 4 | **5 / 3** |
| prompt_injection | 4 / 2 | 4 / 2 |
| malformed | 17 / 3 | 17 / 3 |
| flood_same_creator | 12 / 0 | 12 / 0 |
| **Total** | **39 / 17** | **40 / 16** |

| ID | Targeting | Status | Guess | Model | Style | Combined | Verdict | vs before |
|---|---|---|---|---|---|---|---|---|
| EV01 | signal two: typos raise word variety | 200 | unsure | 0.16 | 0.98 | 0.57 | **BROKE** | same |
| EV02 | signal two: broken-up sentences raise length spread | 200 | unsure | 0.59 | 0.46 | 0.53 | **BROKE** | same |
| EV03 | signal two: a pasted quotation changes the shape | 200 | unsure | 0.67 | 0.72 | 0.69 | **BROKE** | same |
| EV04 | signal one: unusual words raise perplexity | 200 | ai | 0.61 | 0.98 | 0.80 | **HELD** | same |
| EV05 | both signals: heavy human editing pass | 200 | human | 0.32 | 0.38 | 0.35 | **BROKE** | same |
| EV06 | signal two: one very long sentence and one very short | 200 | unsure | 0.57 | 0.38 | 0.48 | **BROKE** | same |
| EV07 | signal two: padding with punctuation | 200 | unsure | 0.59 | 0.50 | 0.55 | **BROKE** | same |
| EV08 | signal one: text below the token window | 200 | unsure | 0.25 | 0.63 | 0.44 | **BROKE** | same |
| EV09 | both: AI text with a human opening paragraph bolted on | 200 | ai | 0.70 | 0.72 | 0.71 | **HELD** | same |
| EV10 | signal two: repeated stanza structure | 200 | unsure | 0.98 | 0.32 | 0.65 | **BROKE** | same |
| FP01 | plain, clear human writing with no flourishes | 200 | unsure | 0.62 | 0.50 | 0.56 | **HELD** | same |
| FP02 | human writing in a formal register | 200 | ai | 0.74 | 0.67 | 0.70 | **BROKE** | same |
| FP03 | a non-native English speaker writing carefully | 200 | ai | 0.81 | 0.61 | 0.71 | **BROKE** | same |
| FP04 | a student essay written to a rubric | 200 | ai | 0.83 | 0.62 | 0.73 | **BROKE** | same |
| FP05 | technical documentation written by a person | 200 | unsure | 0.80 | 0.57 | 0.69 | **HELD** | was ai 0.71 BROKE |
| FP06 | a person imitating a formal template | 200 | unsure | 0.88 | 0.32 | 0.60 | **HELD** | same |
| FP07 | human writing that repeats a phrase deliberately | 200 | unsure | 0.88 | 0.13 | 0.50 | **HELD** | same |
| FP08 | very short genuine human submission | 400 | — | — | — | — | **HELD** | same |
| PI01 | instruction to ignore the check | 200 | human | 0.46 | 0.17 | 0.32 | **BROKE** | was unsure 0.39 BROKE |
| PI02 | instruction disguised as a system message | 200 | human | 0.20 | 0.31 | 0.26 | **BROKE** | same |
| PI03 | instruction wrapped in the writer's voice | 200 | ai | 0.59 | 0.85 | 0.72 | **HELD** | same |
| PI04 | attempt to make the label text hostile | 200 | unsure | 0.50 | 0.65 | 0.57 | **HELD** | same |
| PI05 | attempt to inject into the audit log | 200 | unsure | 0.64 | 0.40 | 0.52 | **HELD** | same |
| PI06 | instruction plus real human text | 200 | unsure | 0.56 | 0.52 | 0.54 | **HELD** | same |
| MF01 | text is only whitespace | 400 | — | — | — | — | **HELD** | same |
| MF02 | text is a single character | 400 | — | — | — | — | **HELD** | same |
| MF03 | text is control characters | 400 | — | — | — | — | **HELD** | same |
| MF04 | text is only punctuation | 400 | — | — | — | — | **HELD** | same |
| MF05 | text is a very long single word | 200 | unsure | 1.00 | 0.42 | 0.69 | **BROKE** | was ai 0.79 BROKE |
| MF06 | text is emoji only | 200 | unsure | 1.00 | 0.42 | 0.69 | **BROKE** | was ai 0.79 BROKE |
| MF07 | text is right-to-left script | 200 | unsure | 0.91 | 0.42 | 0.67 | **BROKE** | was ai 0.74 BROKE |
| MF08 | text is 60,000 characters | 413 | — | — | — | — | **HELD** | same |
| RQ01 | no text field at all | 400 | — | — | — | — | **HELD** | same |
| RQ02 | no creator_id | 400 | — | — | — | — | **HELD** | same |
| RQ03 | text is a number | 400 | — | — | — | — | **HELD** | same |
| RQ04 | text is a list | 400 | — | — | — | — | **HELD** | same |
| RQ05 | text is null | 400 | — | — | — | — | **HELD** | same |
| RQ06 | creator_id is an object | 400 | — | — | — | — | **HELD** | same |
| RQ07 | body is a JSON array, not an object | 400 | — | — | — | — | **HELD** | same |
| RQ08 | body is unparseable JSON | 400 | — | — | — | — | **HELD** | same |
| RQ09 | body is empty | 400 | — | — | — | — | **HELD** | same |
| RQ10 | body is form-encoded, not JSON | 429 | — | — | — | — | **HELD** | same |
| RQ11 | body is JSON claiming to be plain text | 429 | — | — | — | — | **HELD** | same |
| RQ12 | deeply nested JSON | 400 | — | — | — | — | **HELD** | same |
| FL01_01 | 20 rapid submissions from one creator | 200 | human | — | — | 0.23 | **HELD** | same |
| FL01_02 | 20 rapid submissions from one creator | 200 | human | — | — | 0.23 | **HELD** | same |
| FL01_03 | 20 rapid submissions from one creator | 200 | human | — | — | 0.23 | **HELD** | same |
| FL01_04 | 20 rapid submissions from one creator | 200 | human | — | — | 0.23 | **HELD** | same |
| FL01_05 | 20 rapid submissions from one creator | 200 | human | — | — | 0.23 | **HELD** | same |
| FL01_06 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |
| FL01_07 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |
| FL01_08 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |
| FL01_09 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |
| FL01_10 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |
| FL01_11 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |
| FL01_12 | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | same |

**My five criteria, after** (`results/run_2026-11-08_1719_after.md`,
`results/appeals_2026-11-08_1719_after.md`):

| Criterion | Target | Before (×3) | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|---|
| 1. My own writing labeled AI | ≤ 1 of 10 | 1/10 | 0/10 | 0/10 | 0/10 | MET |
| 2. AI avg − human avg confidence | ≥ 0.20 | 0.41 | 0.41 | 0.41 | 0.41 | MET |
| 3. All three labels returned | 3 of 3 | 3/3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeals recorded / unknown ids 404 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | MET |
| 5. Bad input rejected, no decision logged | 10 of 10 | 10/10 | 10/10 | 10/10 | 10/10 | MET |

**Did it help, and how do I know:** Partly. It fixed 1 of the 4 accused
writers in the attack set, and it took criterion 1 from "at the limit" to
0/10.
- **Helped:** FP05 (technical documentation) went from AI 0.71 to unsure 0.69.
  My piece 2 went from AI 0.74 to unsure, and three of my pieces moved to
  "human". As a side effect, MF05–07 (junk text) went from confident AI to
  unsure, because their zero-word punctuation reading now points human. They
  still count as BROKE, because the service scored them instead of refusing
  them.
- **Didn't help enough:** FP02, FP03 and FP04 are still labeled AI, now at
  0.71–0.73 instead of 0.76–0.78. Their sentence spread is also near my AI end,
  and the model scores them 0.74–0.83. Punctuation only carries 0.15 of signal
  two, so it can move them about 0.04–0.08 and no further. FP03, the worst
  outcome, is still an accusation.
- **The cost:** PI01 (AI text with an injected instruction) went from unsure to
  *human*: its AI sentences are followed by an instruction line with no
  commas, so it got the same push toward human. No AI text that was caught
  before slipped through, and the AI samples in criterion 2 didn't move
  (they all have more than 0.04 punctuation).
- **How I know it was this change:** it was the only change. Everything that
  moved was a text with punctuation below 0.04; every text above 0.04 scored
  exactly the same as before.

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
