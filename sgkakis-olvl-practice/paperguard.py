#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import shutil
from pathlib import Path


def parse_txt_to_json(txt_path: Path, date_hint: str | None = None) -> dict:
    lines = txt_path.read_text(encoding="utf-8", errors="replace").splitlines()
    paper_id = ""
    subjects = {}
    current = None

    for ln in lines:
        if ln.startswith("Paper ID:"):
            paper_id = ln.split(":", 1)[1].strip()
            break

    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        msec = re.match(r"^===\s*(.+?)\s*\(20 Questions\)\s*===$", ln)
        if msec:
            current = msec.group(1).strip()
            subjects[current] = []
            i += 1
            continue

        mq = re.match(r"^(\d+)\.\s*(.+?)\s*\[(\d+)\]\s*$", ln)
        if current and mq:
            q = {
                "type": "short",
                "question": mq.group(2).strip(),
                "marks": int(mq.group(3)),
            }
            # compact inline choices A/B/C/D
            qtext = q["question"]
            if all(x in qtext for x in [" A. ", " B. ", " C. ", " D. "]):
                stem, rest = qtext.split(" A. ", 1)
                mm = re.match(r"(.+?)\s+B\.\s+(.+?)\s+C\.\s+(.+?)\s+D\.\s+(.+)$", rest)
                if mm:
                    q = {
                        "type": "mcq",
                        "question": stem.strip(),
                        "marks": int(mq.group(3)),
                        "choices": [mm.group(1).strip(), mm.group(2).strip(), mm.group(3).strip(), mm.group(4).strip()],
                    }
            subjects[current].append(q)
        i += 1

    if not date_hint:
        mdate = re.search(r"(\d{4}-\d{2}-\d{2})", txt_path.name)
        date_hint = mdate.group(1) if mdate else dt.datetime.utcnow().strftime("%Y-%m-%d")

    return {
        "date": date_hint,
        "paper_id": paper_id or f"paper-{date_hint}",
        "subjects": subjects,
    }


def validate_pair(txt: Path, js: Path) -> tuple[bool, str]:
    if not txt.exists():
        return False, f"missing txt: {txt}"
    if not js.exists():
        return False, f"missing json: {js}"
    try:
        obj = json.loads(js.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"invalid json: {e}"
    if not isinstance(obj, dict) or "subjects" not in obj:
        return False, "json missing subjects"
    return True, "ok"


def publish(src_dir: Path, dst_dir: Path, date_str: str) -> dict:
    txt = src_dir / f"paper-{date_str}.txt"
    js = src_dir / f"paper-{date_str}.json"
    dst_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(txt, dst_dir / txt.name)
    shutil.copy2(js, dst_dir / js.name)
    shutil.copy2(txt, dst_dir / "latest.txt")
    shutil.copy2(js, dst_dir / "latest.json")

    manifest = {
        "date": date_str,
        "txt": txt.name,
        "json": js.name,
        "updatedAtUtc": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }
    (dst_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="PaperGuard: validate/repair/publish daily papers")
    ap.add_argument("--date", help="YYYY-MM-DD (default: latest txt date in source)")
    ap.add_argument("--source", default="/home/node/openclaw/sgkakis-olvl-practice/daily_papers")
    ap.add_argument("--dest", default="/ws/sgdailyhub/public/olvl/daily_papers")
    ap.add_argument("--repair", action="store_true", help="repair missing json from txt")
    ap.add_argument("--publish", action="store_true", help="publish latest + manifest")
    args = ap.parse_args()

    src = Path(args.source)
    dst = Path(args.dest)

    date_str = args.date
    if not date_str:
        txts = sorted(src.glob("paper-*.txt"))
        if not txts:
            print("ERROR: no txt papers found")
            return 2
        m = re.search(r"(\d{4}-\d{2}-\d{2})", txts[-1].name)
        date_str = m.group(1) if m else dt.datetime.utcnow().strftime("%Y-%m-%d")

    txt = src / f"paper-{date_str}.txt"
    js = src / f"paper-{date_str}.json"

    ok, msg = validate_pair(txt, js)
    repaired = False

    if (not ok) and args.repair and txt.exists() and ("missing json" in msg):
        obj = parse_txt_to_json(txt, date_hint=date_str)
        js.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        repaired = True
        ok, msg = validate_pair(txt, js)

    result = {
        "date": date_str,
        "txt": str(txt),
        "json": str(js),
        "valid": ok,
        "status": msg,
        "repaired": repaired,
    }

    if ok and args.publish:
        result["manifest"] = publish(src, dst, date_str)
        result["published_to"] = str(dst)

    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
