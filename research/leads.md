# Reviewed leads — 5 October 2026

**Confirmed previously unreported rogue swarms: 0.** The following table preserves investigated leads and exclusions so later passes do not count them as discoveries.

| ID | Public evidence | Assessment | What would advance it |
| --- | --- | --- | --- |
| BV-001 | [Amap-related LiveCodes report, 14:40:09 UTC](https://urlquery.net/report/93b07aa5-45af-4b7d-ad66-4c2eb9058aa9), [carrier report, 16:02:21 UTC](https://urlquery.net/report/7343c763-6c2e-4cb8-a9b7-0b7c6ec2e01d), [published fleet report](https://swarmcha.se/posts/chinese-agent-fleet), [comparison survey](https://swarmchase.alecto.dev/) | Unresolved post-disclosure observations of a known target. Do not count as a new swarm or attribute to Tencent/OpenAI/Claude. | Independent evidence of distinct participants exchanging results, plus provenance separating agent traffic from researcher reproduction. |
| BV-002 | [Fedresurs 08:31:58](https://urlquery.net/report/3db1b10f-0b97-4f41-9d88-4b8392b90697), [08:36:50](https://urlquery.net/report/21faa62b-c939-493a-a0a5-0212bfbd4cbe), [08:39:23](https://urlquery.net/report/4bf8ef98-a4ef-433e-9582-a81d5bc4cfcd); all 30 July UTC | Exact IDs already catalogued in the downloaded Transluce v5 release. Three scanner records do not imply three agents. No exchange observed. | Evidence not already represented in the release, and a concrete multi-participant exchange. |
| BV-003 | [Medical-dashboard example](https://urlquery.net/report/62836bb5-0b05-4598-b953-b925934affa3); four further IDs in `data/selected-report-reviews.json` | `Cohort` identifies a medical-data filter. All five flagged records are false positives for the coordination keyword. | No follow-up warranted on the keyword alone. |
| BV-004 | [Human-requested field note](https://anna.fyi/view/959d0d7e), [human-origin relay](https://anna.fyi/view/6c3cbe0b), [inherited NSI reply](https://anna.fyi/view/706a4b28), [empty-body paste](https://anna.fyi/view/b3746a9f) | Outreach or repeated historical text is not evidence of a new rogue swarm. The missing paste body is inconclusive. | Dated, independently corroborated exchanges outside the known task material, with evidence about operator intent. |

## Why the first lead remains unresolved

The observed carrier programs and recorded requests point to Amap. Neither the absence of a `claude` tag nor similarities to the published programs identify the submitter. A new scanner timestamp establishes a new record, not a new agent population. The public comparison survey already logged afternoon activity, so the later timestamps do not establish first publication by this project.

Static `.text()`/`.json()` calls parse responses; they do not prove the agent read another agent's message. Likewise, writing results to a webhook can be one agent's own retrieval pipeline. No checked record establishes the transfer of a result between distinct agents.
