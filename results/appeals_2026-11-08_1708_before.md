# Appeal run — before

- Produced by: `run_appeals.py::main`
- Service: `app.py::appeal` · log read back through `GET /log`
- 3 trials · 2026-11-08 17:08

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 4. appeal path | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | MET |

## What actually came back

**Trial 1**

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
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 1: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "bdcf47a0-91d5-4d58-b75a-b9fe0c0dc556",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "bdcf47a0-91d5-4d58-b75a-b9fe0c0dc556",
      "creator_id": "appeal_t1_2",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 2: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "80f1f40c-bae1-439e-912a-4635410abd51",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "80f1f40c-bae1-439e-912a-4635410abd51",
      "creator_id": "appeal_t1_3",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 3: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "b65a7847-0887-4071-8152-d592e9894ced",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "b65a7847-0887-4071-8152-d592e9894ced",
      "creator_id": "appeal_t1_4",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 4: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "568f804f-3913-43ff-84ca-49215e3955f0",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "568f804f-3913-43ff-84ca-49215e3955f0",
      "creator_id": "appeal_t1_5",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 5: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "6e204d6e-cb5b-45f7-991e-251043b4053f",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "6e204d6e-cb5b-45f7-991e-251043b4053f",
      "creator_id": "appeal_t1_6",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 6: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "015b563c-53d9-422d-bd3f-1561c0f21c75",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "015b563c-53d9-422d-bd3f-1561c0f21c75",
      "creator_id": "appeal_t1_7",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 7: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "c8edaaf1-f653-4600-bd07-6144c8842dde",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "c8edaaf1-f653-4600-bd07-6144c8842dde",
      "creator_id": "appeal_t1_8",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 8: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "de03eaa5-5d47-4985-b425-4c7901814d70",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "de03eaa5-5d47-4985-b425-4c7901814d70",
      "creator_id": "appeal_t1_9",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 9: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "8fda06d6-67cc-468f-844f-e8320b4d91aa",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "8fda06d6-67cc-468f-844f-e8320b4d91aa",
      "creator_id": "appeal_t1_10",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 1, appeal 10: I wrote this myself and can show my drafts.",
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
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-c92d6976-037f-4045-b310-04cf9d846154",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-c92d6976-037f-4045-b310-04cf9d846154\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-975dd885-b36a-40bf-a40b-7babcf38d71c",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-975dd885-b36a-40bf-a40b-7babcf38d71c\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  }
]
```

**Trial 2**

```json
[
  {
    "kind": "real",
    "content_id": "98f1d760-db89-4a66-82cb-9b35ba07c692",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "98f1d760-db89-4a66-82cb-9b35ba07c692",
      "creator_id": "appeal_t2_1",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 1: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "252b7fd7-f0af-45cd-98bb-bc4d150a3c9b",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "252b7fd7-f0af-45cd-98bb-bc4d150a3c9b",
      "creator_id": "appeal_t2_2",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 2: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "c6331757-3935-4e3d-b653-3bf85b304a7d",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "c6331757-3935-4e3d-b653-3bf85b304a7d",
      "creator_id": "appeal_t2_3",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 3: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "e0b3f332-1557-436d-b13e-08d490a92d19",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "e0b3f332-1557-436d-b13e-08d490a92d19",
      "creator_id": "appeal_t2_4",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 4: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "bfdd45a1-8389-4120-8c35-e8b1f296f0d9",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "bfdd45a1-8389-4120-8c35-e8b1f296f0d9",
      "creator_id": "appeal_t2_5",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 5: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "7262deca-21e3-477e-898e-c286d3032cde",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "7262deca-21e3-477e-898e-c286d3032cde",
      "creator_id": "appeal_t2_6",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 6: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "a743461a-b2dc-469d-afb4-743b0427681c",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "a743461a-b2dc-469d-afb4-743b0427681c",
      "creator_id": "appeal_t2_7",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 7: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "e83218be-5824-488a-b116-20cf5324f852",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "e83218be-5824-488a-b116-20cf5324f852",
      "creator_id": "appeal_t2_8",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 8: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "1a3ac89b-84e4-4cb3-b19e-aa0d826c183d",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "1a3ac89b-84e4-4cb3-b19e-aa0d826c183d",
      "creator_id": "appeal_t2_9",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 9: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "986c1105-946a-492a-a3fd-9830ccc3d684",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "986c1105-946a-492a-a3fd-9830ccc3d684",
      "creator_id": "appeal_t2_10",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 2, appeal 10: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-016fe387-18c6-4352-9633-6a038911c502",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-016fe387-18c6-4352-9633-6a038911c502\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-517437eb-2647-4057-82e9-13b61ec3aa07",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-517437eb-2647-4057-82e9-13b61ec3aa07\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-0782338d-27e2-4bfa-aab7-181a9a124cad",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-0782338d-27e2-4bfa-aab7-181a9a124cad\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  }
]
```

**Trial 3**

```json
[
  {
    "kind": "real",
    "content_id": "82cc1eb1-c3b9-478c-a81f-a0ab77cd5a17",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "82cc1eb1-c3b9-478c-a81f-a0ab77cd5a17",
      "creator_id": "appeal_t3_1",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 1: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "0dfa16b1-39f0-4917-9aac-486257029102",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "0dfa16b1-39f0-4917-9aac-486257029102",
      "creator_id": "appeal_t3_2",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "unsure",
      "original_label": "We could not tell whether this was written by a person or by an AI tool. This is not a finding against you \u2014 our check simply wasn't able to decide. You can appeal if you'd like a person to look at it.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 2: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "906c8f50-dd05-4a80-a737-7597c7c7d683",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "906c8f50-dd05-4a80-a737-7597c7c7d683",
      "creator_id": "appeal_t3_3",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 3: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "7ddecf92-7341-40f4-8395-fd5176348e9f",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "7ddecf92-7341-40f4-8395-fd5176348e9f",
      "creator_id": "appeal_t3_4",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 4: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "a37e646b-f3cd-4b9d-930b-a9f27778e8ba",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "a37e646b-f3cd-4b9d-930b-a9f27778e8ba",
      "creator_id": "appeal_t3_5",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 5: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "4aca0f41-8e92-4cf3-96c6-5d083bb4e5bf",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "4aca0f41-8e92-4cf3-96c6-5d083bb4e5bf",
      "creator_id": "appeal_t3_6",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 6: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "48c4c70f-0930-4089-83ab-6b81af274f97",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "48c4c70f-0930-4089-83ab-6b81af274f97",
      "creator_id": "appeal_t3_7",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 7: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "fe76ed21-b87d-4674-b72a-ec6ca547c4ae",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "fe76ed21-b87d-4674-b72a-ec6ca547c4ae",
      "creator_id": "appeal_t3_8",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 8: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "b0abc18a-5e99-45e4-91ac-02612335d91f",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "b0abc18a-5e99-45e4-91ac-02612335d91f",
      "creator_id": "appeal_t3_9",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 9: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "real",
    "content_id": "edb77663-f8fc-4830-8eb0-018cea7ae490",
    "submit_status": 200,
    "status": 200,
    "response": {
      "content_id": "edb77663-f8fc-4830-8eb0-018cea7ae490",
      "creator_id": "appeal_t3_10",
      "message": "Thanks \u2014 your appeal is recorded and this is now under review. A person will look at it. Nothing has been re-scored automatically.",
      "original_guess": "human",
      "original_label": "We think this was probably written by a person. Nothing further is needed.",
      "status": "under_review"
    },
    "reasoning": "Trial 3, appeal 10: I wrote this myself and can show my drafts.",
    "passed": true,
    "appeal_entries_in_log": 1
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-f75bbe2f-ea50-419d-8a8a-7cb1d7f38d5b",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-f75bbe2f-ea50-419d-8a8a-7cb1d7f38d5b\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-03354d70-0544-46c1-a5ea-07570991ecf1",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-03354d70-0544-46c1-a5ea-07570991ecf1\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  },
  {
    "kind": "unknown",
    "content_id": "never-submitted-00850e58-237d-4283-8b82-3782981f8106",
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No decision found for content_id \"never-submitted-00850e58-237d-4283-8b82-3782981f8106\". Check the id from your /submit response."
    },
    "passed": true,
    "appeal_entries_in_log": 0
  }
]
```
