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

Read 57 public search-listing pages across 36 queries, retained **1,146 unique scanner records**, and inspected **43 original report downloads**. The eight added relay-domain searches returned identical empty responses and are inconclusive, so they did not add records. Also searched 460 npm/RubyGems and 55 NuGet package metadata records, reviewed 25 selected registry documents/metadata assessments including PyPI and NuGet, and searched 58 public Apify Actor listings with nine selected assessments. Ordinary wiki histories, one public workpad task with three replies, and 80 messages in four public chat rooms were also checked. These numbers count artifacts, not agents. Of the scanner records, 382 occur in the comparison dataset; absence from it does not establish novelty. Most listing records have not received full manual review.

| Lead | Evidence checked | Assessment |
| --- | --- | --- |
| Afternoon Amap-related programs | Public reports from 5 October, including 14:40 and 16:02 UTC; decoded text and recorded requests | Fresh observations of a known target. Operator, connection to the published fleet and coordination remain unresolved. |
| Fedresurs sequence | Three original July records and exact-ID dataset comparison | Already catalogued in the comparison release; no visible inter-agent exchange. |
| Five “cohort” matches | Decoded programs and keyword context | Medical-data filter; false positive for coordination. |
| Recent Anna paste feed | Public messages and reply chain | Human-requested outreach, inherited historical task text, or unavailable body; insufficient for a new rogue swarm. |
| September UseMod bot entry | September 20 sandbox revision and related public posts | Self-described bot; related posts explicitly describe operator authorization. |
| Registry matches | 24 searches and 15 selected metadata/README reviews | Software documentation and intended messaging products; no new incident established. |
| Live public job/game rooms | 80 messages; outer signatures verified offline | Intended public coordination. Different keys are not verified AI agents or rogue behavior. |
| September Quidax batch | Six original reports and exact-ID comparison | Already published by Transluce; excluded as a discovery. |
| August UseMod fleet envelopes | Current read-only histories, exact-name novelty search, and September 4 prior observer account | Previously published; deleted shells, single-operator alternative and later contact contamination leave no verified multi-agent result exchange. |
| Agent Workpad task/replies | One indexed public task with three result replies | Concrete result transfer, but on a service built for intentional agent research coordination; not rogue evidence. |
| NuGet coordination metadata | Eight searches, 55 unique package IDs, ten selected assessments | Intended orchestration/protocol/memory software or a keyword false friend; no incident artifact or unintended behavior. |
| PublicTestWiki template test | Deletion audit, revision 82469 and the bounded May 27 Sandbox history | Previously published one-contributor template sequence on a test venue; no distinct-participant result exchange or boundary crossing established. |
| Apify Actor Store | Eight metadata searches, 58 unique Actor IDs, nine selected assessments | Intended analyzers, relays, routers, auditors or utilities; listing/user metadata is not a rogue incident or participant evidence. |

- [Dated investigation log](research/2026-10-05.md)
- [Reviewed leads and exact evidence links](research/leads.md)
- [Source register](data/sources.json)
- [Snapshot index and collection limits](data/README.md)
- [Read-only search tools and limitations](tools/README.md)

Hourly follow-up research is enabled from 5 October 2026. Each pass reads the latest repository state, rotates into coverage gaps, and commits meaningful new evidence or coverage. Alerts are reserved for credible new candidates, material developments or access blockers. Scheduled execution is distinct from a continuously running live process. The search prioritizes original exchanges and provenance over keyword or traffic-volume matches.
