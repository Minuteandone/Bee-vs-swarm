#!/usr/bin/env python3
"""Read existing urlquery listings and decode carrier text offline. Never submit scans."""
import argparse
import base64
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, unquote, urlencode, urlsplit
from urllib.request import Request, urlopen

class Listing(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.row = {"cells": [], "report_urls": []}
        if tag == "td":
            self.cell = []
        if tag == "a" and self.row is not None:
            href = attrs.get("href", "")
            if re.fullmatch(r"/report/[0-9a-f-]{36}", href):
                self.row["report_urls"].append("https://urlquery.net" + href)
    def handle_data(self, value):
        if self.cell is not None:
            self.cell.append(value)
    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            if self.row is not None:
                self.row["cells"].append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        if tag == "tr" and self.row is not None:
            if self.row["report_urls"] and len(self.row["cells"]) >= 3:
                self.rows.append(self.row)
            self.row = None

CARRIERS = {"httpbin.org", "eu.httpbin.org", "httpbun.com", "httpbingo.org", "pie.dev"}
BASE64_PREFIXES = {host: "/base64/" for host in CARRIERS}
BASE64_PREFIXES["nghttp2.org"] = "/httpbin/base64/"
PATTERNS = {
    "fetch": r"\bfetch\s*\(",
    "xhr": r"XMLHttpRequest",
    "websocket": r"WebSocket|EventSource",
    "sink_domain": r"webhook\.site|ntfy\.sh|pipedream\.net",
    "repeated_requests": r"setInterval|setTimeout",
    "peer_language": r"\bcohort\b|\bpeer\b|\bswarm\b|\brendezvous\b",
    "response_parsing": r"\.json\s*\(|\.text\s*\(",
}

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def nested_text(text):
    """Inspect at most two layers of quoted base64/hex text, without evaluating code."""
    seen, parts, frontier = {text}, [text], [text]
    for _ in range(2):
        following = []
        for part in frontier:
            for token in re.findall(r"['\"]([A-Za-z0-9+/_=-]{80,100000})['\"]", part):
                candidates = []
                try:
                    candidates.append(base64.b64decode(token + "=" * (-len(token) % 4), altchars=b"-_", validate=True).decode("utf-8"))
                except (ValueError, UnicodeError):
                    pass
                if len(token) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", token):
                    try:
                        candidates.append(bytes.fromhex(token).decode("utf-8"))
                    except UnicodeError:
                        pass
                for candidate in candidates:
                    if candidate not in seen and re.search(r"https?://|<script|\bfetch\s*\(|document\.", candidate):
                        if sum(map(len, parts)) + len(candidate) > 800000:
                            return "\n".join(parts), len(parts) - 1
                        seen.add(candidate)
                        parts.append(candidate)
                        following.append(candidate)
        frontier = following
    return "\n".join(parts), len(parts) - 1

def summarize(row, query, retrieved_at):
    submitted = row["cells"][2].strip()
    parsed = urlsplit(submitted if submitted.startswith(("http://", "https://")) else "https://" + submitted)
    submitted_host = parsed.hostname
    parameter_names = sorted(parse_qs(parsed.query, keep_blank_values=True))
    safe_parameter_names = [key for key in parameter_names if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", key)]
    # href.li carries the destination as an entire query, not as a parameter name.
    # Decode its text locally; do not open the destination.
    if parsed.hostname == "href.li" and parsed.query.startswith(("https://", "http://")):
        parsed = urlsplit(unquote(parsed.query))
    decoded = ""
    error = None
    encoding = None
    prefix = BASE64_PREFIXES.get(parsed.hostname)
    if prefix and parsed.path.startswith(prefix):
        encoding = "base64_path"
        payload = unquote(parsed.path[len(prefix):])
        try:
            if len(payload) > 800000:
                raise ValueError("payload too large")
            raw = base64.b64decode(payload + "=" * (-len(payload) % 4), altchars=b"-_", validate=True)
            decoded = raw.decode("utf-8")
        except (ValueError, UnicodeError) as exc:
            error = type(exc).__name__
    elif parsed.hostname == "livecodes.io":
        params = parse_qs(parsed.query, keep_blank_values=True)
        parts = [value for key in ("html", "js") for value in params.get(key, [])]
        if parts:
            encoding = "url_query_text"
            decoded = "\n".join(parts)
            if len(decoded) > 800000:
                decoded, error = "", "payload_too_large"
    analyzed, nested_count = nested_text(decoded)
    hosts = sorted(set(re.findall(r"https?://([a-zA-Z0-9.-]+)", analyzed)))
    # Domain-level references only: never export sink paths, topics, tokens, or payload URLs.
    hosts = sorted({h.lower() for h in hosts if not re.fullmatch(r"[0-9.]+", h)})
    title = re.search(r"<title[^>]*>([^<]{1,100})</title>", decoded, re.I)
    safe_title = title.group(1) if title and re.fullmatch(r"[a-zA-Z0-9_. :/-]{1,100}", title.group(1)) else None
    features = [name for name, pattern in PATTERNS.items() if re.search(pattern, analyzed, re.I)]
    event = row["cells"][0]
    event_at = event.replace(" ", "T") + ":00Z" if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", event) else None
    return {
        "report_url": row["report_urls"][0],
        "event_at": event_at,
        "observed_at": retrieved_at,
        "search_queries": [query],
        "submitted_host": submitted_host,
        "decoded_carrier_host": parsed.hostname if encoding else None,
        "query_parameter_names": safe_parameter_names,
        "omitted_parameter_names": len(parameter_names) - len(safe_parameter_names),
        "encoding": encoding,
        "is_base64_carrier": bool(decoded) and encoding == "base64_path",
        "decoded_sha256": hashlib.sha256(decoded.encode()).hexdigest() if decoded else None,
        "decoded_characters": len(decoded),
        "nested_text_fragments": nested_count,
        "decode_error": error,
        "page_title": safe_title,
        "referenced_hosts": hosts,
        "features": features,
        "review_status": "unreviewed",
        "swarm_confirmed": False,
    }

def collect(args):
    records, log = {}, []
    for query in args.query:
        for page in range(args.pages):
            params = {"q": query, "type": "reports", "limit": args.limit, "offset": page * args.limit, "view": "list"}
            endpoint = "https://urlquery.net/api/htmx/search/?" + urlencode(params)
            public_url = "https://urlquery.net/search?" + urlencode({"q": query})
            headers = {"User-Agent": "Bee-vs-swarm-public-research/0.1", "HX-Request": "true", "HX-Current-URL": public_url}
            stamp = now()
            entry = {"query": query, "page": page, "observed_at": stamp, "search_url": public_url}
            try:
                with urlopen(Request(endpoint, headers=headers), timeout=20) as response:
                    body = response.read(8000001)
                    if len(body) > 8000000:
                        raise ValueError("listing too large")
                    entry["http_status"] = response.status
                    entry["body_sha256"] = hashlib.sha256(body).hexdigest()
                    parser = Listing()
                    parser.feed(body.decode("utf-8"))
                    entry["parsed_records"] = len(parser.rows)
                    entry["outcome"] = "records" if parser.rows else "inconclusive_empty_response"
                    for row in parser.rows:
                        item = summarize(row, query, stamp)
                        previous = records.get(item["report_url"])
                        if previous:
                            previous["search_queries"] = sorted(set(previous["search_queries"] + [query]))
                        else:
                            records[item["report_url"]] = item
            except (HTTPError, URLError, ValueError, UnicodeError, TimeoutError) as exc:
                entry["outcome"] = "read_failed"
                entry["error"] = type(exc).__name__
                entry["http_status"] = exc.code if isinstance(exc, HTTPError) else None
            log.append(entry)
            print(json.dumps(entry), flush=True)
            time.sleep(args.delay)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"collected_at": now(), "method": "public existing listings; offline text decode; no submitted URL visited", "records": list(records.values()), "query_log": log}, indent=2) + "\n")
    print(f"Saved {len(records)} unique report summaries to {output}", flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", action="append", required=True)
    parser.add_argument("--pages", type=int, default=1, choices=range(1, 4))
    parser.add_argument("--limit", type=int, default=24, choices=range(1, 51))
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--output", default="data/public-report-summaries.json")
    args = parser.parse_args()
    if args.delay < 1:
        parser.error("delay must be at least one second")
    collect(args)

if __name__ == "__main__":
    main()
