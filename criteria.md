# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Of 10 pieces of writing I personally wrote, at most 1 is labeled high-confidence AI (`guess: "ai"` from `POST /submit`) in each of the three test trials.

The 10 pieces are each 50–20,000 characters, and at least 3 of them are written in a plain or formal style (short sentences, simple vocabulary), because that is the style my Milestone 1 trace showed both signals misread as AI.

**Why this target: A false accusation can damage a real writer's reputation, so I would rather miss some AI-generated text than incorrectly accuse someone who wrote their own work. Testing across three trials also helps account for variations in model scores.**

---

## 2. On 5 AI-generated samples and 5 human-written samples, the average `confidence` of the AI samples is at least 0.20 higher than the average `confidence` of the human samples, in each of the three trials.

AI samples: produced by an AI chatbot from a one-line prompt and submitted unedited; the model and prompt are recorded next to each sample. Human samples: writing by me or a named person, written before 2022. Each sample is 50–20,000 characters. `confidence` is the combined score, where 0 = confidently human and 1 = confidently AI.

**Why this target: A difference of at least 0.20 gives the two groups a measurable separation instead of having nearly identical scores. The system does not need to identify every sample correctly, but its scores should show a meaningful difference between the two groups.**

---

## 3. Each of the three labels (high-confidence AI, high-confidence human, and unsure) is returned by `POST /submit` for at least one test input in each of the three trials, and every confidence score from 0 to 1 maps to exactly one label, with no gaps or overlaps, as shown by `scoring.label_ranges()`.

**Why this target: Users need an unsure option when the system cannot confidently determine the source of a piece of writing. Every score should also have a defined label so that no submission receives a missing or ambiguous result.**

---

## 4. For 10 appeals, each sent to `POST /appeal` with a different `content_id` from an earlier submission and a non-empty `reasoning`, all 10 return 200 with `status: "under_review"`, and `GET /log` shows an appeal entry for each one that contains the writer's reasoning word for word. In addition, 3 appeals with a `content_id` that was never submitted all return 404 and add no appeal entry to the log.

**Why this target: Writers should have a reliable way to challenge a potentially incorrect decision. Recording every appeal makes the process traceable and ensures that an appeal does not silently disappear.**

---

## 5. 10 invalid requests to `POST /submit` are all rejected, without any new decision entry in the audit log: 2 with `text` missing, 2 with `text` that isn't a string, 2 with empty or whitespace-only `text`, 2 with `text` under 50 characters after trimming, and 2 with `text` over 20,000 characters.

Each response uses the error shape from TRACE.md, `{"error": "<code>", "message": "<sentence>"}`, with the matching status and code: 400 `missing_field`, 400 `text_too_short` (empty or short text), or 413 `text_too_long`. A `rejection` entry in the log is expected.

**Why this target: Invalid or excessively large requests should not cause the service to crash or waste resources. A clear error response helps clients understand the problem, while preventing invalid submissions from being treated as legitimate content.**

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
