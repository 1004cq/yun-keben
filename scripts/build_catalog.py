#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

OWNER = "TapXWorld"
REPO = "ChinaTextbook"
BRANCH = "master"
OUT = Path(__file__).resolve().parent.parent / "web" / "catalog.json"
STAGE_ORDER = ["小学", "小学（五•四学制）", "初中", "初中（五•四学制）", "高中", "大学", "习题"]


def api(url: str) -> dict:
    headers = {"User-Agent": "yun-keben-catalog", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def fetch_tree() -> list:
    meta = api(f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{BRANCH}?recursive=1")
    if meta.get("truncated"):
        print("警告: tree truncated")
    return meta.get("tree", [])


def parse_split(name: str):
    m = re.match(r"^(.*\.pdf)\.(\d+)$", name, re.I)
    if m:
        return m.group(1), int(m.group(2))
    return name, None


def classify(path: str):
    parts = path.split("/")
    top = parts[0] if parts else ""
    if top.startswith("学数学"):
        return "习题", parts[1] if len(parts) > 1 else "练习", ""
    if top in STAGE_ORDER:
        subject = parts[1] if len(parts) > 1 else ""
        edition = parts[2] if len(parts) > 2 and not parts[2].lower().endswith((".pdf", ".1", ".2", ".3")) else ""
        return top, subject, edition
    return top or "其他", "", ""


def build(tree):
    groups = {}
    for node in tree:
        if node.get("type") != "blob":
            continue
        path = node["path"]
        if path.startswith("."):
            continue
        name = path.split("/")[-1]
        if not re.search(r"\.pdf(\.\d+)?$", name, re.I):
            continue
        base_name, part = parse_split(name)
        parent = path.rsplit("/", 1)[0] if "/" in path else ""
        key = f"{parent}/{base_name}"
        g = groups.setdefault(key, {"path": f"{parent}/{base_name}" if parent else base_name, "name": base_name, "size": 0, "parts": []})
        g["size"] += int(node.get("size") or 0)
        if part is not None:
            g["parts"].append({"n": part, "path": path})
    books = []
    for g in groups.values():
        stage, subject, edition = classify(g["path"])
        parts = [p["path"] for p in sorted(g["parts"], key=lambda x: x["n"])]
        books.append({
            "id": g["path"],
            "name": g["name"].replace(".pdf", "").replace(".PDF", ""),
            "file": g["name"],
            "path": g["path"],
            "stage": stage,
            "subject": subject,
            "edition": edition,
            "size": g["size"],
            "split": bool(parts),
            "parts": parts,
        })
    books.sort(key=lambda b: (STAGE_ORDER.index(b["stage"]) if b["stage"] in STAGE_ORDER else 99, b["subject"], b["edition"], b["name"]))
    stages = defaultdict(set)
    for b in books:
        stages[b["stage"]].add(b["subject"])
    return {
        "source": f"{OWNER}/{REPO}",
        "branch": BRANCH,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(books),
        "stages": {k: sorted(v) for k, v in stages.items()},
        "books": books,
    }


def main():
    print("fetch tree")
    catalog = build(fetch_tree())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
    print("wrote", OUT, "count", catalog["count"])


if __name__ == "__main__":
    main()
