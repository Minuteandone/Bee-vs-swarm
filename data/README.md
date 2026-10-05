# Public evidence snapshots

These files contain sanitized metadata from existing public records. They are not a list of verified agents or swarms.

| File | Contents |
| --- | --- |
| `public-report-summaries.json` | Initial eight-query snapshot: 175 unique report IDs. |
| `carrier-followup.json` | Four carrier queries, three pages each: 586 unique report IDs. |
| `coordination-followup.json` | Five keyword/carrier queries: 97 unique report IDs. |
| `tag-and-channel-followup.json` | Four provider-name/channel queries: 147 unique report IDs. |
| `structured-query-followup.json` | Three empty experimental queries and one broad keyword query: 50 unique report IDs. |
| `selected-report-reviews.json` | 22 original-report reviews, including later nested base64/hex decoding and manual assessment. |
| `novelty-comparison.json` | Exact-ID comparison for all 907 unique listing records against the downloaded 38,160-row Transluce release. |
| `sources.json` | Public comparison sources and selected paste controls. |

The listing files overlap. Across all five snapshots there are **907 distinct report IDs**, not the sum of the file counts. The comparison contains 201 overlaps and 706 absences; an absence only means the exact ID was absent from this comparison release.

Snapshots preserve collection times, query-page logs, and response hashes. Earlier snapshots have less complete text decoding; the review file supplies the later assessment for selected IDs. `review_status: unreviewed` means only bounded metadata was collected. `swarm_confirmed: false` prevents treating automated cues as confirmations; it is not proof that the underlying record has no connection to agents.

Raw submitted URLs, sink paths/topics, credentials, submitter addresses and response bodies are omitted. Report links provide public provenance. No recovered program was executed or resubmitted by this project.
