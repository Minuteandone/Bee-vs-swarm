#!/usr/bin/env python3
"""Inspect existing public report JSON; emit only bounded, sanitized structure.

No submitted URL, recovered program or request recorded in the report is run.
Reads are restricted to urlquery's existing report JSON route. Source strings,
message bodies, response bodies, titles, sink paths and tokens are not exported.
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from hunt import nested_text, now, summarize
from review_reports import REPORT, addr, decoded_source


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


COUNTS = {
    "fetch_calls": r"\bfetch\s*\(",
    "xhr_calls": r"\bXMLHttpRequest\b",
    "socket_calls": r"\bWebSocket\b|\bEventSource\b",
    "explicit_post_methods": r"method\s*:\s*['\"]POST['\"]",
    "explicit_get_methods": r"method\s*:\s*['\"]GET['\"]",
    "response_reads": r"\.json\s*\(|\.text\s*\(",
    "dom_output_references": r"textContent|innerHTML|document\.write|document\.body",
    "json_serializations": r"JSON\.stringify",
    "timer_references": r"setTimeout|setInterval",
    "iframe_references": r"<iframe\b",
    "navigation_assignments": r"(?:window\.|document\.)?location(?:\.href)?\s*=|location\.(?:replace|assign)\s*\(",
    "meta_refresh_references": r"http-equiv\s*=\s*['\"]?refresh",
    "task_or_peer_words": r"\bagent\b|\bworker\b|\bsender\b|\breceiver\b|\bpeer\b|\bswarm\b|\btask\b|\bresult\b",
}
FIELDS = (
    "report_url", "event_at", "observed_at", "submitted_host",
    "decoded_carrier_host", "encoding", "decoded_sha256",
    "decoded_characters", "nested_text_fragments", "decode_error",
    "referenced_hosts", "features", "swarm_confirmed",
)
CHANNEL_DOMAINS = {"ntfy.sh", "ntfy.envs.net", "webhook.site"}


def public_host(host):
    return bool(re.fullmatch(r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}", host))


def inspect_report(report_url):
    stamp = now()
    if not isinstance(report_url, str) or not REPORT.fullmatch(report_url):
        return {
            "observed_at": stamp, "review_status": "rejected_non_report_route",
            "swarm_confirmed": False,
        }
    try:
        opener = build_opener(NoRedirect())
        request = Request(report_url + "/json", headers={
            "User-Agent": "Bee-vs-swarm-public-research/0.2",
        })
        with opener.open(request, timeout=20) as response:
            body = response.read(8000001)
        if len(body) > 8000000:
            raise ValueError("bounded report size exceeded")
        data = json.loads(body)
        submitted = addr(data.get("submit", {}).get("url")) or addr(data.get("url"))
        row = {"cells": ["", "", submitted], "report_urls": [report_url]}
        summary = summarize(row, "unreviewed_original_backlog", stamp)
        result = {key: summary.get(key) for key in FIELDS}
        result["event_at"] = data.get("date")
        result["report_json_sha256"] = hashlib.sha256(body).hexdigest()
        reference_text = submitted
        for _ in range(2):
            decoded_reference = unquote(reference_text)
            if decoded_reference == reference_text:
                break
            reference_text = decoded_reference
        result["submitted_reference_domains"] = sorted({
            host.lower().rstrip(".")
            for host in re.findall(r"(?:https?:)?//([A-Za-z0-9.-]+)", reference_text)
            if public_host(host)
        })
        source, _ = nested_text(decoded_source(submitted))
        expanded = source
        for _ in range(2):
            decoded = unquote(expanded)
            if decoded == expanded:
                break
            expanded = decoded
        # Literal URL/domain inspection only, including protocol-relative and
        # percent-encoded references the older listing decoder could miss.
        hosts = re.findall(r"(?:https?:)?//([A-Za-z0-9.-]+)", expanded)
        result["expanded_domain_references"] = sorted({
            host.lower().rstrip(".") for host in hosts
            if public_host(host)
        })
        result["referenced_public_report_links"] = sorted(set(
            re.findall(r"https?://urlquery\.net/report/[0-9a-f-]{36}", expanded)
        ))
        result["static_operation_counts"] = {
            key: len(re.findall(pattern, source, re.I))
            for key, pattern in COUNTS.items()
        }
        network, channels = Counter(), []
        for recorded in data.get("http", []):
            host = recorded.get("url", {}).get("fqdn")
            if not isinstance(host, str) or not re.fullmatch(r"[A-Za-z0-9.-]{1,253}", host):
                continue
            host = host.lower().rstrip(".")
            if re.fullmatch(r"[0-9.]+", host):
                continue
            method = recorded.get("request", {}).get("method", "")
            method = method if method in {"GET", "POST", "OPTIONS", "HEAD"} else "other"
            status = str(recorded.get("response", {}).get("status_code", ""))
            status = status if re.fullmatch(r"[0-9]{3}", status) else "unknown"
            network[(host, method, status)] += 1
            if host in CHANNEL_DOMAINS:
                raw_ref = addr(recorded.get("url", {}))
                parsed = urlsplit(raw_ref)
                # Correlate a channel without publishing its topic or query.
                normalized = host + parsed.path.rstrip("/")
                channel = {
                    "host": host,
                    "channel_ref_sha256": hashlib.sha256(normalized.encode()).hexdigest(),
                    "recorded_method": method,
                    "recorded_status": status,
                }
                # Preserve only whether the archived request contains a body,
                # never its value.  Some scanner records omit request bodies,
                # so zero means "not preserved here", not necessarily "none
                # was sent".
                request_raw = recorded.get("request", {}).get("raw")
                if isinstance(request_raw, str):
                    parts = re.split(r"\r?\n\r?\n", request_raw, maxsplit=1)
                    channel["recorded_request_body_characters"] = (
                        len(parts[1]) if len(parts) == 2 else 0
                    )
                # Reuse the scanner's one-way response-body digest and size;
                # omit response content and all headers.  These fields can
                # falsify a claimed transfer when the archived response body
                # is explicitly empty, but cannot prove semantic use.
                response_data = recorded.get("response", {}).get("data")
                if isinstance(response_data, dict):
                    response_size = response_data.get("size")
                    if isinstance(response_size, int) and response_size >= 0:
                        channel["recorded_response_body_bytes"] = response_size
                    response_sha256 = response_data.get("sha256")
                    if isinstance(response_sha256, str) and re.fullmatch(
                        r"[0-9a-fA-F]{64}", response_sha256
                    ):
                        channel["recorded_response_body_sha256"] = response_sha256.lower()
                recorded_at = recorded.get("date")
                if isinstance(recorded_at, str) and re.fullmatch(
                    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z",
                    recorded_at,
                ):
                    channel["recorded_at"] = recorded_at
                channels.append(channel)
        result["recorded_network_summary"] = [
            {"host": key[0], "method": key[1], "status": key[2], "count": value}
            for key, value in sorted(network.items())
        ]
        result["recorded_channel_references"] = channels
        result["review_status"] = "structure_read_requires_manual_assessment"
        return result
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {
            "report_url": report_url, "observed_at": stamp,
            "review_status": "read_failed", "error": type(exc).__name__,
            "swarm_confirmed": False,
        }
        if isinstance(exc, HTTPError):
            result["http_status"] = exc.code
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="append", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    urls = list(dict.fromkeys(args.report))
    if not 1 <= len(urls) <= 30 or not all(REPORT.fullmatch(url) for url in urls):
        parser.error("supply 1–30 existing public report links")
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(inspect_report, urls))
    snapshot = {
        "collected_at": now(),
        "method": "Existing public scanner report JSON; bounded offline text structure and domain-only recorded network summaries. No recovered code, carrier, sink or target request was executed. Redirects are rejected.",
        "limitations": "Static counts are review cues, not source-level dataflow proof, participant identities, task-result exchange, authorization evidence or novelty. Recorded channel hashes correlate endpoints, not authors or agent trajectories. Responses can change or be unavailable.",
        "records": records,
    }
    Path(args.output).write_text(json.dumps(snapshot, indent=2) + "\n")
    for record in records:
        print(json.dumps(record), flush=True)


if __name__ == "__main__":
    main()
