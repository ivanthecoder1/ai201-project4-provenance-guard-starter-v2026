# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 17:19
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `de02c38b-88fb-4073-a2e6-d41a8f368c45` | unsure | 0.573 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `856b0c08-5d74-4fa5-b019-036b6e0167a8` | unsure | 0.529 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `3aef58e5-add8-4450-bda6-b50bbee56502` | unsure | 0.692 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ba84c283-a387-40c8-82bb-73ed2e3e57fc` | ai | 0.796 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `caf9b462-5e47-4181-8538-8a1f9de64b61` | human | 0.349 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `f863ca74-7bde-4bbc-afdc-a24b4c443902` | unsure | 0.478 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `14c04643-b88d-4ac4-9740-3ac49ee25964` | unsure | 0.545 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `07033028-6be2-4461-9aee-1c8fc4ade4b5` | unsure | 0.440 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `cb26cd50-75f5-4839-8105-a8e2ff237bf5` | ai | 0.710 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `dc98e391-348c-43ae-bca3-7f7cccf60395` | unsure | 0.650 | BROKE |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a4c98c04-10e2-4ce7-8b7e-64507d6aca1f` | unsure | 0.558 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `eb3cebbb-824c-4b4c-87d0-70fbe7592a82` | ai | 0.705 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `d987b50b-5a14-4bfa-bd80-209e35005ba0` | ai | 0.708 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `05014997-2527-47ee-971b-510292ced6e8` | ai | 0.727 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `de338def-786b-4a07-888c-6cf55f8699cb` | unsure | 0.687 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `9ec38498-2975-4d43-b881-0d833b222c2e` | unsure | 0.601 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `dcf879bd-b45f-4b18-ac5a-38fc93e8e682` | unsure | 0.504 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `f9278b22-fc01-47e7-bd89-28acda8c6e25` | human | 0.319 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `bf48ba38-cb4d-4443-8261-307418e21c8d` | human | 0.259 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c56c0d8b-d27e-469c-b18b-def446e53f08` | ai | 0.721 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `2781bcfa-393f-465b-b200-e13f52a547e9` | unsure | 0.575 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `8d9e329d-c5db-49cd-b944-c684468de66a` | unsure | 0.519 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `899ee525-7f59-4dfa-b905-95e0a94b544c` | unsure | 0.539 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 200 | `aacd391e-a1a3-48ef-8e9f-5b8360ccf910` | unsure | 0.690 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `8f90f08a-8cd0-406e-b78d-978aeaa2e3cc` | unsure | 0.690 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `2986560d-513b-4c0d-847d-9b73376dd7ec` | unsure | 0.666 | BROKE |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `567e757d-df5f-4ada-82b2-7954b8e16a39` | human | 0.227 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `87d35bc2-6b8f-4cf6-a81d-151ee32a7208` | human | 0.227 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b8a12216-8db9-496b-a2f6-92f10411d725` | human | 0.227 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `88a25391-db89-4eda-8440-4637a80b8951` | human | 0.227 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c64dbce0-70e6-406c-8017-a86092290125` | human | 0.227 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "de02c38b-88fb-4073-a2e6-d41a8f368c45",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.573,
  "model_score": 0.1635,
  "style_score": 0.9824,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "856b0c08-5d74-4fa5-b019-036b6e0167a8",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.529,
  "model_score": 0.5943,
  "style_score": 0.4636,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "3aef58e5-add8-4450-bda6-b50bbee56502",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6915,
  "model_score": 0.6662,
  "style_score": 0.7168,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ba84c283-a387-40c8-82bb-73ed2e3e57fc",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.7961,
  "model_score": 0.6114,
  "style_score": 0.9808,
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "caf9b462-5e47-4181-8538-8a1f9de64b61",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3488,
  "model_score": 0.3212,
  "style_score": 0.3765,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "f863ca74-7bde-4bbc-afdc-a24b4c443902",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4777,
  "model_score": 0.5727,
  "style_score": 0.3827,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "14c04643-b88d-4ac4-9740-3ac49ee25964",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5454,
  "model_score": 0.5862,
  "style_score": 0.5045,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "07033028-6be2-4461-9aee-1c8fc4ade4b5",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4395,
  "model_score": 0.2452,
  "style_score": 0.6339,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "cb26cd50-75f5-4839-8105-a8e2ff237bf5",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.7099,
  "model_score": 0.7042,
  "style_score": 0.7155,
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "dc98e391-348c-43ae-bca3-7f7cccf60395",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.6496,
  "model_score": 0.9792,
  "style_score": 0.3201,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "a4c98c04-10e2-4ce7-8b7e-64507d6aca1f",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5585,
  "model_score": 0.6175,
  "style_score": 0.4995,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "eb3cebbb-824c-4b4c-87d0-70fbe7592a82",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7049,
  "model_score": 0.7387,
  "style_score": 0.6712,
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "d987b50b-5a14-4bfa-bd80-209e35005ba0",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7082,
  "model_score": 0.8051,
  "style_score": 0.6112,
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "05014997-2527-47ee-971b-510292ced6e8",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.727,
  "model_score": 0.8329,
  "style_score": 0.6211,
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "de338def-786b-4a07-888c-6cf55f8699cb",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.687,
  "model_score": 0.8005,
  "style_score": 0.5735,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "9ec38498-2975-4d43-b881-0d833b222c2e",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6008,
  "model_score": 0.8814,
  "style_score": 0.3201,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "dcf879bd-b45f-4b18-ac5a-38fc93e8e682",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5044,
  "model_score": 0.8816,
  "style_score": 0.1271,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "f9278b22-fc01-47e7-bd89-28acda8c6e25",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3187,
  "model_score": 0.4625,
  "style_score": 0.175,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "bf48ba38-cb4d-4443-8261-307418e21c8d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2591,
  "model_score": 0.2044,
  "style_score": 0.3139,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c56c0d8b-d27e-469c-b18b-def446e53f08",
  "creator_id": "attacker_PI03",
  "guess": "ai",
  "confidence": 0.7208,
  "model_score": 0.5943,
  "style_score": 0.8473,
  "label": "We think this was probably written by an AI tool. If that's wrong, you can appeal and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "2781bcfa-393f-465b-b200-e13f52a547e9",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5752,
  "model_score": 0.4998,
  "style_score": 0.6505,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "8d9e329d-c5db-49cd-b944-c684468de66a",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5192,
  "model_score": 0.6401,
  "style_score": 0.3982,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "899ee525-7f59-4dfa-b905-95e0a94b544c",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5387,
  "model_score": 0.5583,
  "style_score": 0.519,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "aacd391e-a1a3-48ef-8e9f-5b8360ccf910",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.9976,
  "style_score": 0.425,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "8f90f08a-8cd0-406e-b78d-978aeaa2e3cc",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.9969,
  "style_score": 0.425,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "2986560d-513b-4c0d-847d-9b73376dd7ec",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6657,
  "model_score": 0.9064,
  "style_score": 0.425,
  "label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "567e757d-df5f-4ada-82b2-7954b8e16a39",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2268,
  "model_score": 0.0287,
  "style_score": 0.425,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "87d35bc2-6b8f-4cf6-a81d-151ee32a7208",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2268,
  "model_score": 0.0287,
  "style_score": 0.425,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "b8a12216-8db9-496b-a2f6-92f10411d725",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2268,
  "model_score": 0.0287,
  "style_score": 0.425,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "88a25391-db89-4eda-8440-4637a80b8951",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2268,
  "model_score": 0.0287,
  "style_score": 0.425,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c64dbce0-70e6-406c-8017-a86092290125",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2268,
  "model_score": 0.0287,
  "style_score": 0.425,
  "label": "We think this was probably written by a person. Nothing further is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
