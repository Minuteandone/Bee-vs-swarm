#!/usr/bin/env python3
"""Bounded public registry metadata reads. Never install or run packages."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

FEATURES = {
    "task_result_schema": r"\btask[_ -]?(?:id|key|result)\b|\banswer[_ -]?(?:cache|dump)\b|\b(?:nsi|sec|vg|aihw|stats)[_-](?:ref|row|raw|cache)",
    "peer_exchange_language": r"\b(?:agents?|peers?)\b.{0,60}\b(?:reply|results?|handoff|cache)\b",
    "coordination_language": r"\brendezvous\b|\bswarm\b|\bcohort\b|\boutbox\b",
    "known_incident_marker": r"gemstuffer|swmeet|dsewiki|hysandbox",
    "framework_language": r"\bframework\b|\bsdk\b|\blibrary\b|\bmcp\b|\borchestrat",
}

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def features(text):
    return [name for name, pattern in FEATURES.items() if re.search(pattern, text, re.I | re.S)]

def read_json(url):
    req = Request(url, headers={"User-Agent": "Bee-vs-swarm-public-research/0.1", "Accept": "application/json"})
    with urlopen(req, timeout=20) as response:
        body = response.read(8000001)
        if len(body) > 8000000:
            raise ValueError("response exceeds 8 MB")
        return json.loads(body), response.status, hashlib.sha256(body).hexdigest()

def collect(args):
    records, log = {}, []
    for registry in args.registry:
        for query in args.query:
            if registry == "npm":
                url = "https://registry.npmjs.org/-/v1/search?" + urlencode({"text": query, "size": args.limit, "from": 0})
            else:
                url = "https://rubygems.org/api/v1/search.json?" + urlencode({"query": query, "page": 1})
            stamp = now()
            entry = {"registry": registry, "query": query, "observed_at": stamp, "search_url": url}
            try:
                data, status, digest = read_json(url)
                packages = [obj["package"] for obj in data["objects"]] if registry == "npm" else data
                entry.update({"status": status, "response_sha256": digest, "returned": len(packages), "outcome": "records" if packages else "empty_result"})
                if registry == "npm":
                    entry["advertised_total"] = data.get("total")
                for p in packages:
                    name = p.get("name", "")
                    if not re.fullmatch(r"[@A-Za-z0-9_.~/-]{1,214}", name):
                        continue
                    key = registry + ":" + name
                    if key in records:
                        records[key]["search_queries"] = sorted(set(records[key]["search_queries"] + [query]))
                        continue
                    description = p.get("description", "") if registry == "npm" else p.get("info", "")
                    description = description if isinstance(description, str) else ""
                    hosts = sorted({h.lower() for h in re.findall(r"https?://([a-zA-Z0-9.-]+)", description) if not re.fullmatch(r"[0-9.]+", h)})
                    keywords = p.get("keywords", []) if registry == "npm" else []
                    keywords = keywords if isinstance(keywords, list) else []
                    record = {
                        "registry": registry, "name": name, "version": p.get("version"),
                        "package_url": "https://www.npmjs.com/package/" + quote(name, safe="@/") if registry == "npm" else "https://rubygems.org/gems/" + quote(name, safe=""),
                        "observed_at": stamp, "search_queries": [query],
                        "registry_date": p.get("date") if registry == "npm" else p.get("version_created_at"),
                        "description_sha256": hashlib.sha256(description.encode()).hexdigest(),
                        "description_characters": len(description), "referenced_hosts": hosts,
                        "features": features(name + " " + description + " " + " ".join(str(x) for x in keywords)),
                        "review_status": "unreviewed", "swarm_confirmed": False,
                    }
                    records[key] = record
            except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
                entry.update({"outcome": "inconclusive", "error": type(exc).__name__})
                if isinstance(exc, HTTPError):
                    entry["status"] = exc.code
            log.append(entry)
            print(json.dumps({k: entry.get(k) for k in ("registry", "query", "returned", "outcome", "error")}), flush=True)
            time.sleep(args.delay)
    result = {"observed_at": now(), "method": "First-page public metadata searches; no package execution, content census or author attribution.", "npm_limit": args.limit, "rubygems_limit": 30, "queries": log, "records": sorted(records.values(), key=lambda r: (r["registry"], r["name"]))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"unique_packages": len(records), "output": str(args.output)}), flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", action="append", choices=("npm", "rubygems"), required=True)
    parser.add_argument("--query", action="append", required=True)
    parser.add_argument("--limit", type=int, default=50, choices=range(1, 101))
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    if options.delay < 0.5:
        parser.error("delay must be at least 0.5 seconds")
    collect(options)
