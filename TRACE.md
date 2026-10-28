# Milestone 1 — Tracing a submission before building one

Written before any route code exists. This is the plan everything else has to
fit, and the README's **What This Does** section will be built from part 1.

---

## 1. The path a piece of text takes

| # | Where | What it adds |
|---|---|---|
| 1 | **The writer's site → `POST /submit`** | A JSON body: `text` and `creator_id`. Flask parses it into a dict (`request.get_json`). |
| 2 | **Input check** (`app.py::submit`) | Refuses anything it can't judge: missing, non-string, empty or too-short `text`; text over the size cap; missing `creator_id`. A refusal returns a 400/413 and is written to the log with `audit.log_rejection`, so no decision is ever made on bad input. |
| 3 | **A content id** (`uuid.uuid4()`) | A unique handle for this one submission. It's the only thing that links the decision, the log, and a later appeal. |
| 4 | **Signal one** (`detector.py::model_signal`) | A 0–1 score from how predictable gpt2 finds the text (perplexity). Higher = more AI-like. Only the first 400 tokens are read. |
| 5 | **Signal two** (`stylometry.py::style_signal`) | A 0–1 score from the shape of the text: sentence-length spread, word variety, punctuation. Higher = more AI-like. |
| 6 | **Combine + label** (`scoring.py::combine_signals`, `score_to_label`) | Two numbers become one `confidence` score, and that score becomes a guess (`ai` / `human` / `unsure`) plus the sentence a reader sees. |
| 7 | **Log, then answer** (`audit.py::log_decision`, then the JSON response) | One line in `logs/audit.jsonl` with both signal scores, the combined score, the label, and `status: "decided"`. Then the same facts go back to the caller, and the site shows the label beside the piece. |

Order matters in step 7: the log is written *before* the response is sent, so
there is never a label someone saw that the log doesn't know about.

---

## 2. The two signals

### Signal one — model signal (`detector.py`, given)

- **Measures:** predictability. How surprised gpt2 is by each next word
  (perplexity), squashed onto 0–1 so low perplexity → high AI score.
- **Why it might differ:** a language model writes by picking likely next
  words, so its output is text a model finds easy to guess. People make odder,
  more specific choices.
- **Blind spot:** predictable ≠ machine-written. It rewards common words in
  ordinary sentences, so **plain human writing** — a second-language writer, a
  younger writer, anyone writing simply on purpose — scores as AI. And the
  reverse: AI text asked to use rare or ornate words scores as human. It also
  only sees the first 400 tokens, so anything after that is invisible to it.

### Signal two — style signal (`stylometry.py`, mine to build)

- **Measures:** the text as a shape, with no understanding of meaning:
  - sentence-length spread (std dev ÷ mean of words per sentence)
  - type-token ratio (unique words ÷ total words)
  - punctuation density, weighted toward `; — : ( )` over full stops
- **Why it might differ:** generated prose tends toward even, mid-length
  sentences and a narrower band of safe vocabulary. Human writing is lumpier —
  a three-word sentence next to a forty-word one, an aside in a dash.
- **Blind spot:** it can't read. Anything that changes the shape without
  changing the substance moves it: inserting typos (raises word variety),
  chopping or merging sentences (changes spread), adding dashes or a pasted
  quote. That's cheap to do on purpose. It is also length-sensitive — type-token
  ratio falls as text gets longer — and a one-sentence poem has no spread at
  all. Poems and lists, with deliberate repetition and no normal punctuation,
  break every assumption it makes.

**Why these count as two signals:** one asks "would a model have said this?",
the other asks "does this look like the shape models produce?". They fail on
different inputs — typos fool signal two but barely move signal one; rare
vocabulary fools signal one but not signal two.

**Where they overlap, which is the worrying part:** plain, even, repetitive
human writing triggers *both* blind spots at once. The two signals agreeing is
not independent evidence for that writer.

---

## 3. Tracing the false positive

**The writer:** Mai learned English as an adult. She posts a short personal
essay about her first winter. Short, clear sentences, words she's sure of, few
commas, nothing fancy. Every word is hers.

**Through the service**, with the starter's placeholder settings
(weights 0.5 / 0.5, AI threshold 0.65):

1. Her text passes the input check and gets `content_id` `c-7f3a…`.
2. **Signal one:** gpt2 finds her text easy to predict — perplexity around 25.
   `1 / (1 + (25/45)^1.6)` ≈ **0.72**.
3. **Signal two:** sentences all 8–12 words (low spread), a small repeated
   vocabulary (low type-token ratio), almost no punctuation beyond full stops.
   Every measure points AI-ward: roughly **0.70**.
4. **Combined:** 0.5 × 0.72 + 0.5 × 0.70 = **0.71**. Above 0.65.
5. **Label:** high-confidence AI. Logged as `decided`.
6. **What she sees:** her essay, publicly marked as probably AI-written.
7. **What she can do:** `POST /appeal` with her `content_id` and her reasons.
   The item moves to `under_review` and she gets a confirmation. Nothing
   re-checks it, and nothing in this unit says who reviews it or when.

**What this tells me before I set any numbers:**

- The weighted average *can't* save her: both signals are wrong in the same
  direction, so averaging them just averages two wrong answers. The AI label
  should need a high bar — I'll look at an AI threshold nearer 0.80, or a rule
  that the AI label needs both signals clearly high, once I have real scores
  in Milestone 4.
- The AI label is the only one that costs a person something, so it has to be
  the hardest to reach. A wide unsure band is cheaper than a wrong accusation.
- Every label that isn't "human" must tell the writer they can appeal and
  how. The `/submit` response carries an `appeal` field for exactly that.
- Her appeal must never be lost: it's logged next to the original decision
  (append-only), and the appeal response echoes back her `content_id` so she
  has proof.
- Open gap I'm naming now, not fixing: `under_review` has no reviewer. In a
  real site the label should be hidden or softened while under review.

---

## 4. The two endpoint contracts

All bodies are JSON. All errors use one shape:
`{"error": "<code>", "message": "<sentence for a human>"}`.

### `POST /submit`

**Request**

| Field | Type | Rules |
|---|---|---|
| `text` | string | Required. After trimming whitespace, at least 50 characters and at most 20,000. |
| `creator_id` | string | Required, non-empty. Who wrote it; stored, not verified. |

**Response — `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Unique id for this submission. Keep it — `/appeal` needs it. |
| `guess` | string | Exactly one of `"ai"`, `"human"`, `"unsure"`. |
| `confidence` | float, 0–1, 4 dp | The combined score. **0 = confidently human, 1 = confidently AI.** 0.5 is not a guess either way. |
| `label` | string | The full sentence a reader sees. Always one of the three fixed label texts. |
| `model_score` | float, 0–1 | Signal one on its own. Higher = more AI-like. |
| `style_score` | float, 0–1 | Signal two on its own. Higher = more AI-like. |
| `status` | string | `"decided"` for a fresh submission. |
| `appeal` | string | How to dispute it: "Think we got this wrong? POST /appeal with this content_id." |

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | Body missing, not JSON, or not a JSON object. |
| 400 | `missing_field` | `text` or `creator_id` absent or not a string. |
| 400 | `text_too_short` | `text` under 50 characters after trimming (includes empty). |
| 413 | `text_too_long` | `text` over 20,000 characters. |
| 503 | `detector_unavailable` | The model can't load. No decision is made or logged as decided. |

Every 4xx is logged with `audit.log_rejection`.

### `POST /appeal`

**Request**

| Field | Type | Rules |
|---|---|---|
| `content_id` | string | Required. Must match a submission already in the log. |
| `reasoning` | string | Required, non-empty after trimming, at most 5,000 characters. The writer's own words. |

`creator_id` is not sent — it's copied from the original decision so the
appeal entry and the decision entry share it.

**Response — `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back. |
| `status` | string | `"under_review"`. |
| `message` | string | "Thanks — we've recorded your appeal and a person will look at this piece again. The label won't be treated as final while it's under review." |
| `appealed_at` | string | ISO-8601 UTC timestamp from the log entry. |

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | Body missing, not JSON, or not an object. |
| 400 | `missing_field` | `content_id` or `reasoning` absent, not a string, or empty. |
| 404 | `unknown_content_id` | No decision in the log has that id. |

A second appeal on the same item is accepted and logged too (the log is
append-only), and returns 200 with the same status.

### Could someone build against this without asking me?

Questions I checked myself against:

- *Does a high `confidence` mean "sure it's AI" or "sure of whatever the
  guess is"?* — Answered: it's the AI-ward score. Stated in the field table.
- *What does "too short" mean?* — 50 characters after trimming.
- *Who owns an appeal?* — Not checked in unit 7; anyone with the id can appeal.
  Named here as a known weakness rather than left ambiguous.
- *What happens if the model is down?* — 503, no decision.
