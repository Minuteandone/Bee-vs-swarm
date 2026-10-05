#!/usr/bin/env python3
"""Read public report JSON and export bounded metadata, never raw payloads."""
import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, parse_qs
from urllib.request import Request, urlopen
from hunt import BASE64_PREFIXES, nested_text, now, summarize

REPORT = re.compile(r"https://urlquery\.net/report/[0-9a-f-]{36}")

def decoded_source(url):
    parsed = urlsplit(url if url.startswith(("https://", "http://")) else "https://" + url)
    if parsed.hostname == "href.li" and parsed.query.startswith(("https://", "http://")):
        return decoded_source(unquote(parsed.query))
    prefix = BASE64_PREFIXES.get(parsed.hostname)
    if prefix and parsed.path.startswith(prefix):
        token = unquote(parsed.path[len(prefix):])
        if len(token) <= 800000:
            try:
                return base64.b64decode(token + "=" * (-len(token) % 4), altchars=b"-_", validate=True).decode("utf-8")
            except (ValueError, UnicodeError):
                return ""
    if parsed.hostname == "livecodes.io":
        params = parse_qs(parsed.query)
        return "\n".join(v for k in ("html", "js") for v in params.get(k, []))[:800000]
    return ""

def addr(value):
    return value.get("addr", "") if isinstance(value, dict) else value if isinstance(value, str) else ""

def read_report(report_url):
    stamp = now()
    try:
        with urlopen(Request(report_url + "/json", headers={"User-Agent": "Bee-vs-swarm-public-research/0.1"}), timeout=20) as response:
            body = response.read(8000001)
        if len(body) > 8000000:
            raise ValueError("report too large")
        data = json.loads(body)
        submitted = addr(data.get("submit", {}).get("url")) or addr(data.get("url"))
        row = {"cells": ["", "", submitted], "report_urls": [report_url]}
        result = summarize(row, "selected_public_report_review", stamp)
        result["event_at"] = data.get("date")
        result["report_json_sha256"] = hashlib.sha256(body).hexdigest()
        result["claimed_tags"] = [x for x in data.get("tags", []) if x in {"claude", "openai", "oai", "agent", "ai"}]
        source, _ = nested_text(decoded_source(submitted))
        # Small keyword contexts help distinguish 'peer agent' from library/network wording.
        # Remove URLs, email addresses and long opaque strings before exporting.
        contexts = []
        for match in re.finditer(r"\bpeer\b|\bcohort\b|\bswarm\b|\brendezvous\b", source, re.I):
            context = source[max(0, match.start() - 65):match.end() + 65]
            context = re.sub(r"https?://[^\s\"'<>]+", "[URL REDACTED]", context)
            context = re.sub(r"[\w.+-]+@[\w.-]+", "[EMAIL REDACTED]", context)
            context = re.sub(r"[A-Za-z0-9+/_=-]{30,}", "[OPAQUE STRING REDACTED]", context)
            contexts.append(" ".join(context.split()))
        result["peer_keyword_contexts"] = list(dict.fromkeys(contexts))[:6]
        network = Counter()
        for request in data.get("http", []):
            host = request.get("url", {}).get("fqdn")
            if isinstance(host, str) and re.fullmatch(r"[A-Za-z0-9.-]{1,253}", host) and not re.fullmatch(r"[0-9.]+", host):
                method = request.get("request", {}).get("method", "")
                status = str(request.get("response", {}).get("status_code", ""))
                network[(host.lower(), method if method in {"GET", "POST", "OPTIONS", "HEAD"} else "other", status if re.fullmatch(r"[0-9]{3}", status) else "unknown")] += 1
        result["recorded_network_summary"] = [{"host": k[0], "method": k[1], "status": k[2], "count": v} for k, v in sorted(network.items())]
        result["review_status"] = "metadata_read_requires_manual_assessment"
        return result
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {"report_url": report_url, "observed_at": stamp, "review_status": "read_failed", "error": type(exc).__name__, "swarm_confirmed": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports-file", required=True, help="JSON array of public report URLs, maximum 30")
    parser.add_argument("--output", default="data/selected-report-reviews.json")
    args = parser.parse_args()
    urls = json.loads(Path(args.reports_file).read_text())
    if not isinstance(urls, list) or not 1 <= len(urls) <= 30 or not all(isinstance(u, str) and REPORT.fullmatch(u) for u in urls):
        parser.error("expected 1–30 existing public urlquery report URLs")
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(read_report, urls))
    Path(args.output).write_text(json.dumps({"collected_at": now(), "method": "existing public report JSON; offline decoding; domain-only request metadata", "records": records}, indent=2) + "\n")
    for r in records:
        print(json.dumps({k: r.get(k) for k in ("report_url", "event_at", "referenced_hosts", "features", "peer_keyword_contexts", "review_status")}))

if __name__ == "__main__":
    main()
