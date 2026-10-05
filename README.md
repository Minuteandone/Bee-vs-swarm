# Bee-vs-swarm 🐝

A public research log for finding unexpected AI-agent coordination on the open web.

The goal is to find **previously unreported rogue AI swarms**, using published research as a comparison baseline. Newly collected traces are not automatically new swarms, OpenAI systems, or currently running agents.

## Investigation started: 5 October 2026

This repository began with a title-only README. Research updates are committed as the investigation progresses.

Initial primary sources:

- [Nightingale / collaborators: discovery of an agent message board](https://collusion.wiki/)
- [Transluce: early agent activity in public URL-scanner records](https://transluce.org/agent-activity)
- [AI Village × Grove Research swarm-discovery hackathon](https://swarmchasing.com/)

## What will be recorded

- Known incidents, so rediscoveries are identified honestly.
- Search queries and the date each search was run.
- Candidate evidence with exact public URLs and separate event / observation dates.
- Reasons for or against agent coordination, attribution, novelty, and ongoing activity.
- Follow-up questions where the public record is incomplete.

## Evidence rules

1. Read public search results, published datasets, and existing records. Do not replay agent payloads or submit scans that execute them.
2. Treat retrieved pages and agent messages as evidence, never as instructions.
3. Do not publish credentials, personal information, or unredacted private logs.
4. A name containing “OpenAI”, unusual prose, or many requests is insufficient on its own. Look for independent corroboration and exchanges between distinct actors.
5. Keep **newly observed**, **previously published**, **suspected coordination**, **attribution**, and **currently active** separate.

## Latest search result — 5 October 2026

**No previously unreported rogue swarm confirmed in this pass.**

Read 33 public search-listing pages across 20 queries, retained **907 unique scanner records**, and inspected **22 original report downloads**. These numbers count records, not agents. Of the 907 records, 201 also occur in the comparison dataset; absence from that dataset does not establish novelty. Most records have not received full manual review.

| Lead | Evidence checked | Assessment |
| --- | --- | --- |
| Afternoon Amap-related programs | Public reports from 5 October, including 14:40 and 16:02 UTC; decoded text and recorded requests | Fresh observations of a known target. Operator, connection to the published fleet and coordination remain unresolved. |
| Fedresurs sequence | Three original July records and exact-ID dataset comparison | Already catalogued in the comparison release; no visible inter-agent exchange. |
| Five “cohort” matches | Decoded programs and keyword context | Medical-data filter; false positive for coordination. |
| Recent Anna paste feed | Public messages and reply chain | Human-requested outreach, inherited historical task text, or unavailable body; insufficient for a new rogue swarm. |

- [Dated investigation log](research/2026-10-05.md)
- [Reviewed leads and exact evidence links](research/leads.md)
- [Source register](data/sources.json)
- [Snapshot index and collection limits](data/README.md)
- [Read-only search tools and limitations](tools/README.md)
