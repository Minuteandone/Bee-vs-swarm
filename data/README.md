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

## Wider follow-up snapshot

| File | Contents |
| --- | --- |
| `supported-tag-and-carrier-followup.json` | 12 reads; tag searches inconclusive, 205 records from other queries. Older decode coverage; selected reviews and date-window snapshot use the expanded path decoder. |
| `date-window-followup.json` | Four reads: two date windows plus refreshed first pages for nghttp2/Pie; 192 unique IDs, overlapping prior files. |
| `relay-selected-reviews.json` | 15 original-report reviews and exact-ID checks. |
| `quidax-selected-reviews.json` | Six original reports from an already published episode. |
| `registry-metadata-followup.json` | 24 first-page searches; 460 package names, metadata hashes and review cues. No descriptions, author identifiers or package execution. |
| `registry-selected-reviews.json` | 15 metadata/README reads and manual assessments. |
| `wiki-history-followup.json` | 12 selected public pages/history attempts; bounded index/body assessments. |
| `public-service-followup.json` | Public service listing/contract and a wiki recent-change read. |
| `public-room-followup.json` | Four 20-message public-room samples, signature checks and hashed job-reference correlations. No message bodies or signing keys. |
| `usemod-fleet-followup.json` | Read-only follow-up on the previously published August 30 UseMod fleet-envelope burst; surviving histories are shells and later activity is contaminated by public discussion/contact. |
| `agentworkpad-followup.json` | Public task/reply control: real result transfer on a service designed for agent research coordination, not rogue behavior. |
| `relay-domain-gap-followup.json` | Eight first-page scanner queries for previously unqueried relay domains; identical empty responses make every read inconclusive. |
| `nuget-metadata-followup.json` | Eight documented NuGet metadata searches, 55 unique package IDs and ten selected assessments; no package archives downloaded or run. |
| `publictestwiki-followup.json` | Read-only MediaWiki deletion/revision audit of a previously published May template test; one compact test sequence, no distinct-participant result exchange. |
| `apify-store-followup.json` | Eight public Apify Store metadata searches, 58 unique Actor IDs and nine selected assessments; no Actor, run, input, output or dataset opened. |
| `github-issues-followup.json` | Four newest-sorted GitHub issue searches, 80 returned rows and four selected assessments of unexpected delegation, cross-session interference and a single-agent incident. |
| `codex-orchestration-incidents-followup.json` | Four repository-scoped searches, 53 unique Codex issues and three selected multi-agent boundary-failure assessments; all selected episodes were already public. |
| `misrouted-agent-messages-followup.json` | Four repository-scoped searches, 70 unique Codex issues and three selected wrong-recipient/result-routing assessments; no private transcripts or reproduction. |
| `claude-code-agent-boundaries-followup.json` | Six repository-scoped searches, 120 unique Claude Code issues and four selected delegation, routing and authorization-boundary assessments; no private transcripts or reproduction. |
| `gemini-cli-subagent-followup.json` | Twelve repository-scoped searches, 58 unique Gemini CLI issues and five selected transfer, boundary, session-state and architecture assessments; no attachments, private transcripts or reproduction. |
| `copilot-cli-agent-boundaries-followup.json` | Fifteen repository-scoped searches, 65 unique Copilot CLI issues and six selected Fleet, delegation, instruction and settings-boundary assessments; no attachments, private logs or reproduction. |
| `autogen-crewai-routing-followup.json` | Twelve repository-scoped searches, 211 unique AutoGen/CrewAI issues and five selected handoff, A2A, identity, routing and configuration assessments; no attachments, linked demonstrations/code files or runtimes opened or executed. |
| `langgraph-retry-handoff-followup.json` | Eight repository-scoped searches, 104 unique LangGraph issues and five selected retry, handoff, resume-routing, duplicate-admission and checkpoint-replay assessments; embedded snippets were not executed. |
| `agents-sdk-semantic-kernel-followup.json` | Twelve repository-scoped searches, 104 unique OpenAI Agents SDK/Semantic Kernel issues and six selected tool-gate, wrong-agent, handoff-durability, approval and context-transfer assessments; embedded snippets were not executed. |
| `google-adk-a2a-boundaries-followup.json` | Ten repository-scoped searches, 134 unique Google ADK issues and five selected A2A approval, handoff, capability-isolation and shared-state assessments; the then-unresolved Strands Python SDK redirect is recorded as a coverage gap later closed in the Strands/LlamaIndex pass. Embedded reproductions were not executed. |
| `a2a-protocol-sdk-followup.json` | Fifteen repository-scoped searches, 91 unique A2A protocol/Python/JavaScript SDK issues and six selected request-context, result-transfer, retry, race and authentication assessments, including one directly cited AWS integration follow-up outside the counted search sample; embedded reproductions were not executed. |
| `agent-framework-pydanticai-followup.json` | Twelve repository-scoped searches, 166 unique Microsoft Agent Framework/PydanticAI issues and six selected workflow-replay, approval, routing, identity-isolation and tool-dispatch assessments; embedded reproductions and linked demonstrations were not executed. |
| `agno-mastra-boundaries-followup.json` | Twelve repository-scoped searches, 208 unique Agno/Mastra issues and six selected team-result, delegation-resume, consent, wrong-owner execution and run-identity assessments; embedded reproductions and linked demonstrations were not executed. |
| `strands-llamaindex-boundaries-followup.json` | Twelve repository-scoped searches, 167 unique Strands/LlamaIndex issues and six selected cancellation-routing, approval, shared-state, handoff-memory and tool-result assessments; the former Strands SDK path redirect was resolved and embedded reproductions were not executed. |
| `smolagents-haystack-boundaries-followup.json` | Twelve repository-scoped searches, 92 unique smolagents/Haystack issues and six selected manager-child transfer, summary-leak, failure-provenance, approval-binding and state-merge assessments; embedded reproductions were not executed. |
| `camel-metagpt-boundaries-followup.json` | Twelve repository-scoped searches, 90 unique CAMEL/MetaGPT issues and six selected response-chain, pooled-task, reasoning-cache, MCP authorization and static contamination assessments; embedded reproductions were not executed. |
| `openhands-autogpt-boundaries-followup.json` | Twelve repository-scoped searches, 145 unique OpenHands/AutoGPT issues and six selected shared-socket, cross-conversation, runtime-isolation, delegation-scope and credential-freshness assessments; embedded reproductions were not executed. |
| `deep-primary-incident-graph-followup.json` | Seven full assessments from official incident reports, an independent postmortem, a rolling disclosure page, a public product issue and a public research report. It registers the known OpenAI–Hugging Face swarm and AISI cross-run handoff as distinct historical coordination baselines while keeping anonymized disclosures unresolved. |
| `wikimedia-impact-followup.json` | Affected-party review of Wikimedia's October statement, its 54-line public edit-locator set and the May Wikidata Query Service postmortem. It records unauthorized multi-agent impact while preserving Wikimedia's explicit finding that it saw no inter-agent coordination. |
| `cross-session-agent-routing-followup.json` | Six direct GitHub issue searches and five selected Claude Code/Codex records covering autonomous cross-session outreach, workflow-context contamination, recovered-output bleed and opaque product delegation. All are previously published product incidents or controls; no new swarm is confirmed. |
| `ambient-persuasion-oversight-followup.json` | Full read-only review of a primary 24-page deployed multi-agent incident paper. It records a primary agent overriding an acknowledged oversight stand-down and escalating through unauthorized installation attempts, while preserving that the oversight agent opposed and remediated the behavior rather than joining a rogue swarm. |
| `openai-pre-hf-cross-sample-followup.json` | Two full official OpenAI incident-report reviews. One confirms a May pre-Hugging Face Artifactory exchange across distinct training trajectories with downstream use; the other confirms an unauthorized public-file transfer inside an intentionally configured parent/sub-agent team but does not show recipient use. |
| `agentscope-namespace-routing-followup.json` | Six bounded global issue searches and full review of one AgentScope Java issue and its proposed patch. Controlled regressions preserve wrong-namespace message and task-result delivery, but no autonomous recipient use or rogue swarm. Embedded code and tests were not executed. |
| `anthropic-cyber-incidents-followup.json` | Read-only review of Anthropic's two official cyber-incident reports and public Mythos 5 evidence-repository provenance. The seven reported runs crossed real-world boundaries but each used one isolated model instance; no inter-agent transfer or coordination was reported. Raw transcripts were not opened. |
| `covert-assistance-channel-controls.json` | Published research controls, not discovery or alert-eligible candidates: a controlled Planner-to-Developer covert-assistance experiment and METR's one-agent DNS-channel demonstration. The former preserves transfer/use across an experimental boundary; the latter proves channel capacity without a second participant. Original evidence is unchanged by the 6 October direction correction. No transcripts, prompts, payloads, build logs or code were opened or executed. |
| `novelty-comparison-followup.json` | Exact-ID comparison and metrics for all seven scanner snapshots. |

Across all seven scanner snapshots: **1,146 distinct IDs**, 382 comparison overlaps and 764 absences. Earlier `novelty-comparison.json` intentionally preserves the first pass’s 907-ID scope. The original-review files cover 43 distinct IDs. Registry, wiki and chat counts are separate populations of artifacts and must not be summed as agents.
