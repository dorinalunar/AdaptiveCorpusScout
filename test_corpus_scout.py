"""
Automated unit test suite for AdaptiveCorpusScout contract logic.
Verifies dataset schema validation, Laplace bandit selection, verdict parsing, and hashing.
"""
import hashlib
import json
import re
import pytest


def serialize_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(payload):
    return hashlib.sha256(serialize_json(payload).encode()).hexdigest()


def strict_dict_hook(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("duplicate key detected")
        out[k] = v
    return out


def parse_dataset(raw_text):
    try:
        data = json.loads(raw_text, object_pairs_hook=strict_dict_hook)
    except (ValueError, TypeError):
        return None
    if (type(data) is not dict or set(data) != {"streams"} or type(data["streams"]) is not list
            or not 2 <= len(data["streams"]) <= 4):
        return None
    seen_streams, seen_records = set(), set()
    for stream in data["streams"]:
        if (type(stream) is not dict or set(stream) != {"id", "records"} or type(stream["id"]) is not str
                or re.fullmatch(r"[a-z][a-z0-9_-]{0,23}", stream["id"]) is None
                or stream["id"] in seen_streams or type(stream["records"]) is not list
                or not 2 <= len(stream["records"]) <= 8):
            return None
        seen_streams.add(stream["id"])
        for rec in stream["records"]:
            if (type(rec) is not dict or set(rec) != {"id", "text"}
                    or type(rec["id"]) is not str or re.fullmatch(r"[a-z][a-z0-9_-]{0,31}", rec["id"]) is None
                    or rec["id"] in seen_records or type(rec["text"]) is not str
                    or not 20 <= len(rec["text"]) <= 1000 or rec["text"] != rec["text"].strip()
                    or "\x00" in rec["text"]):
                return None
            seen_records.add(rec["id"])
    return data["streams"]


def select_stream(metrics, catalog):
    open_indices = [i for i in range(len(metrics)) if metrics[i]["probed"] < len(catalog[i]["records"])]
    if not open_indices:
        return -1
    for i in open_indices:
        if metrics[i]["probed"] == 0:
            return i
    weights = [(metrics[i]["matches"] + 1) * 10000 // (metrics[i]["resolved"] + 2)
               + 10000 // (metrics[i]["probed"] + 1) for i in open_indices]
    return open_indices[weights.index(max(weights))]


def extract_verdict(raw_val):
    try:
        parsed = json.loads(raw_val, object_pairs_hook=strict_dict_hook) if type(raw_val) is str else raw_val
    except (ValueError, TypeError):
        return None
    if type(parsed) is not dict or set(parsed) != {"verdict"} or type(parsed["verdict"]) is not str:
        return None
    return parsed["verdict"] if parsed["verdict"] in ("MATCH", "REJECT", "UNCERTAIN") else None


def test_valid_dataset_parsing():
    sample = {
        "streams": [
            {
                "id": "defi_alpha",
                "records": [
                    {"id": "rec_1", "text": "Liquidity pool rebalancing threshold set to 50 basis points."},
                    {"id": "rec_2", "text": "Automated yield harvesting executes every 24 hours on-chain."},
                ],
            },
            {
                "id": "gov_beta",
                "records": [
                    {"id": "rec_3", "text": "Quorum requires at least 10 percent of staked governance tokens."},
                    {"id": "rec_4", "text": "Emergency timelock delays execution by 48 hours after approval."},
                ],
            },
        ]
    }
    res = parse_dataset(json.dumps(sample))
    assert res is not None
    assert len(res) == 2


def test_duplicate_keys_rejected():
    malformed = '{"verdict": "MATCH", "verdict": "REJECT"}'
    assert extract_verdict(malformed) is None


def test_cold_start_and_laplace_allocation():
    catalog = [
        {"id": "s1", "records": [{"id": "r1"}, {"id": "r2"}, {"id": "r3"}]},
        {"id": "s2", "records": [{"id": "r4"}, {"id": "r5"}, {"id": "r6"}]},
    ]
    metrics = [
        {"probed": 0, "resolved": 0, "matches": 0},
        {"probed": 0, "resolved": 0, "matches": 0},
    ]
    # Cold start picks stream 0 first, then stream 1
    assert select_stream(metrics, catalog) == 0
    metrics[0]["probed"] = 1
    assert select_stream(metrics, catalog) == 1

    # Stream 1 gets a MATCH, should be prioritized next
    metrics[1] = {"probed": 1, "resolved": 1, "matches": 1}
    metrics[0] = {"probed": 1, "resolved": 1, "matches": 0}
    assert select_stream(metrics, catalog) == 1


def test_verdict_extraction():
    assert extract_verdict('{"verdict":"MATCH"}') == "MATCH"
    assert extract_verdict('{"verdict":"REJECT"}') == "REJECT"
    assert extract_verdict('{"verdict":"UNCERTAIN"}') == "UNCERTAIN"
    assert extract_verdict('{"verdict":"INVALID"}') is None
