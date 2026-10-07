# Reproduce the public-record search

Use the [original-record discovery protocol](../research/discovery-protocol.md) to choose and interpret records. Listing collection is preparation, not discovery: prioritize the unreviewed original-report backlog and concrete transfer/use trails rather than repeatedly expanding keyword counts or cataloguing known incidents. Exact-ID absence from a comparison release does not establish novelty.

Python 3.10+ and its standard library are sufficient for scanner and registry collection. The optional offline message-signature verifier also uses `cryptography`.

```sh
python tools/hunt.py --query httpbin.org --query httpbun.com --query livecodes.io --pages 3 --limit 50 --output data/new-snapshot.json
```

This reads urlquery's existing public report listings. The HTMX headers reproduce the public search page's read request. The tool does not create scans, visit submitted URLs, read sink inboxes, or execute recovered JavaScript. It decodes base64 path carriers, LiveCodes query text and bounded nested base64/hex strings as text only.

For selected existing records, prepare a JSON array of `https://urlquery.net/report/<uuid>` links, then run:

```sh
python tools/review_reports.py --reports-file report-urls.json --output data/new-reviews.json
```

The review tool reads each report's public `/json` download and exports domain-level network summaries. It omits raw URLs, sink topics, tokens, submitter IPs and response bodies. A SHA256 digest identifies each source response without republishing it.

## Interpretation limits

- A report is one scanner record, not one agent. Duplicate programs, retries and researcher reproductions can appear.
- Scanner event time and our retrieval time are separate. Listing times have minute precision; original JSON can provide seconds.
- `fetch`, `response_parsing`, sink domains and repeated requests are generic code features. They do not establish inter-agent communication.
- Keyword contexts may come from libraries or network errors. `peer_language` is a review cue, not a finding.
- Literal domain extraction misses dynamically constructed or unsupported encodings. No matches are not proof of no activity.
- Search listings include unrelated material. Empty or failed reads are logged as inconclusive.
- Destination IP/ASN information does not identify the submitter. Report labels such as `claude` are claims, not verified model identity.
- The collector's snapshots have bounded pagination and can change during collection. They do not cover private or deleted records.
- Manual review and comparison with previously published work are required before claiming a new swarm.

## Registry metadata

```sh
python tools/registry_hunt.py --registry npm --registry rubygems --query rendezvous --query answer-cache --output data/new-registry-snapshot.json
```

This reads first-page public search metadata: at most 100 npm entries per query and 30 RubyGems entries. It records hashes and generic text cues, omitting descriptions and publisher identifiers. It never installs, imports, downloads or runs registry packages. Search dates are not necessarily original package creation dates; selected version metadata may provide more detail. Keyword matches can describe ordinary libraries. PyPI entries were selected from public search and read through its documented JSON API.

## Offline public-message signature checks

```sh
python tools/verify_public_messages.py --room kibble --input copied-public-room-response.json
```

This verifies at most 200 already-copied public messages against the documented `<room>|<nonce>|<text>` Ed25519 payload. It makes no requests. Modified-text negative controls must fail. Key counts identify distinct verified keys, not models, agents or operators. It does not verify game-internal signatures, unsigned timestamps, task completion or rogue intent. Published observations contain only aggregate checks and hashed reference correlations; the public room may have advanced or expired by a later read.

The carrier decoder also recognizes Pie’s `/base64/` and nghttp2’s `/httpbin/base64/` paths. Other paths and hosts are not evaluated. Date and exclusion search terms require checks against returned timestamps and decoded text; empty indexed-tag searches remain inconclusive.

## Original backlog structure inspection

```sh
python tools/review_backlog.py --report https://urlquery.net/report/1796063a-2e68-48a8-866f-240ecd4570b9 --output data/new-backlog-inspections.json
python -m unittest discover -s tools -p test_review_backlog.py -v
```

Supply up to 30 already existing public report links. The inspector reads only the report's `/json` route and rejects redirects and non-report routes. It inspects carrier text offline without execution, exports operation counts and domain-only recorded requests, and omits titles, payload/message bodies, headers, submitter addresses, tokens and sink topics. One-way channel-reference hashes and sanitized recorded-request timestamps can correlate archived endpoint chronology without reading an inbox. For channel records it also preserves only the archived request-body character count and the scanner's response-body byte count and SHA-256; zero request characters means the scanner did not preserve a body, not necessarily that none was sent. These fields can falsify a claimed transfer when a response is explicitly empty, but they do not prove message semantics or downstream use. Percent-decoded and protocol-relative domain references address gaps in the older listing decoder; they are not agent or transfer/use evidence.

The initial sixteen-record snapshot predates the added reference-domain fields; supplementary checks are recorded separately in `data/original-backlog-assessments.json`. Preserve earlier observations and hashes. Counts, unsupported decodes, repeated endpoints and absent comparison IDs do not establish participant identity, recipient use, operator-boundary crossing or novelty. The four offline regression tests check route restrictions, redirect rejection, redaction and domain-only expansion. They do not execute recovered source or make network requests.
