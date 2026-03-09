#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path('/home/node/openclaw/sgkakis-olvl-practice/daily_papers')
DST = Path('/ws/sgdailyhub/public/olvl/daily_papers')
if not DST.exists():
    ALT = Path('/var/lib/docker/volumes/openclaw-z9bb_openclaw_workspace/_data/sgdailyhub/public/olvl/daily_papers')
    if ALT.exists():
        DST = ALT


def iso(ts: float | None):
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def newest(pattern: str, root: Path):
    items = list(root.glob(pattern))
    if not items:
        return None

    # For dated paper files, prefer lexical date order from filename.
    if pattern.startswith('paper-'):
        item = sorted(items, key=lambda p: p.name)[-1]
    else:
        item = sorted(items, key=lambda p: p.stat().st_mtime)[-1]

    return {
        'path': str(item),
        'name': item.name,
        'mtimeUtc': iso(item.stat().st_mtime),
        'size': item.stat().st_size,
    }


def main():
    out = {
        'generatedAtUtc': datetime.now(timezone.utc).isoformat(),
        'sourceDir': str(SRC),
        'destDir': str(DST),
        'latestSourceTxt': newest('paper-*.txt', SRC),
        'latestSourceJson': newest('paper-*.json', SRC),
        'latestPublishedTxt': newest('latest.txt', DST),
        'latestPublishedJson': newest('latest.json', DST),
        'manifest': None,
        'status': 'ok',
        'alerts': [],
    }

    manifest = DST / 'manifest.json'
    if manifest.exists():
        try:
            out['manifest'] = json.loads(manifest.read_text(encoding='utf-8'))
        except Exception as e:
            out['alerts'].append(f'manifest invalid json: {e}')
    else:
        out['alerts'].append('manifest missing')

    if not out['latestPublishedJson'] or not out['latestPublishedTxt']:
        out['alerts'].append('published latest files missing')

    if out['alerts']:
        out['status'] = 'warn'

    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
