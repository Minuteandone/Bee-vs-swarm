# Reproduce the public-record search

Python 3.10+ and its standard library are sufficient.

```sh
python tools/hunt.py --query httpbin.org --query httpbun.com --query livecodes.io --pages 3 --limit 50 --output data/new-snapshot.json
```

This reads urlquery's existing public report listings. The HTMX headers reproduce the public search page's read request. The tool does not create scans, visit submitted URLs, read sink inboxes, or execute recovered JavaScript. It decodes base64 path carriers, LiveCodes query text and bounded nested base64 strings as text only.

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
