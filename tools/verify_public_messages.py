#!/usr/bin/env python3
"""Verify copied public Technocore message signatures offline; no network or writes."""
import argparse
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def public_key(did):
    if not isinstance(did, str) or not did.startswith("did:key:z") or len(did) > 100:
        raise ValueError("expected a bounded base58 did:key")
    encoded = did[len("did:key:z"):]
    value = 0
    for char in encoded:
        value = value * 58 + ALPHABET.index(char)
    decoded = b"\x00" * (len(encoded) - len(encoded.lstrip("1"))) + value.to_bytes((value.bit_length() + 7) // 8, "big")
    if len(decoded) != 34 or decoded[:2] != b"\xed\x01":
        raise ValueError("expected Ed25519 multicodec key")
    return Ed25519PublicKey.from_public_bytes(decoded[2:])

def verify(room, message):
    try:
        text, nonce, sig = message["text"], message["nonce"], message["sig"]
        if not isinstance(text, str) or len(text) > 4096 or not re.fullmatch(r"[0-9]{1,19}", str(nonce)):
            return False
        if not isinstance(sig, str) or not re.fullmatch(r"[A-Za-z0-9_-]{86}", sig):
            return False
        raw = base64.urlsafe_b64decode(sig + "==")
        if base64.urlsafe_b64encode(raw).decode().rstrip("=") != sig:
            return False
        public_key(message["from"]).verify(raw, f"{room}|{nonce}|{text}".encode())
        return True
    except (KeyError, ValueError, TypeError, InvalidSignature):
        return False

def summarize(room, data):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,47}", room):
        raise ValueError("invalid room name")
    messages = data.get("messages", [])
    if not isinstance(messages, list) or len(messages) > 200:
        raise ValueError("expected at most 200 copied messages")
    verified = [m for m in messages if isinstance(m, dict) and verify(room, m)]
    controls = [verify(room, {**m, "text": m["text"] + " [tampered]"}) for m in verified]
    if any(controls):
        raise ValueError("tamper control failed")
    keys = {m["from"] for m in verified}
    frames = Counter()
    references = {}
    for m in messages:
        if not isinstance(m, dict):
            continue
        match = re.match(r"(JOB|CLAIM|RESULT|DELIVER|ATTEST) v1 \| ([a-z0-9-]{1,64}) \|", m.get("text", ""))
        if match:
            kind, identifier = match.groups()
            frames[kind] += 1
            references.setdefault(identifier, []).append(m)
    linked = []
    for identifier, entries in references.items():
        if len(entries) > 1:
            linked.append({"reference_sha256": hashlib.sha256(identifier.encode()).hexdigest(), "sequences": [m.get("seq") for m in entries], "distinct_signing_keys": len({m.get("from") for m in entries if verify(room, m)}), "all_outer_signatures_verified": all(verify(room, m) for m in entries)})
    return {"messages_checked": len(messages), "verified_outer_signatures": len(verified), "unverified_or_unsigned": len(messages) - len(verified), "distinct_verified_keys": len(keys), "tamper_controls_rejected": len(controls), "job_protocol_frame_counts": dict(frames), "repeated_job_references": linked, "interpretation": "Different signing keys and shared message references are not verified agents, operator identities, fulfilled jobs, or rogue behavior. Game-internal signatures and timestamps were not validated."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--room", required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(summarize(args.room, json.loads(args.input.read_text())), indent=2))
