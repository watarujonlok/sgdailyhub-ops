# SG O/N-Level Practice (Password Protected)

Simple standalone static site:
- Password: `eva`
- Subject picker (English, EMath, AMath, Combined Science, Pure Chem, Pure Phys, Pure Bio, Humanities, POA)
- MCQ paper generation (reshuffled each run)
- Instant marking + score
- Type `ok` to regenerate a new set

## Run locally

```bash
cd sgkakis-olvl-practice
python3 -m http.server 8080
```

Open `http://localhost:8080`.

## Ops utilities

### PaperGuard (validate / repair / publish)

```bash
python3 paperguard.py --date 2026-03-09 --repair --publish
```

Useful flags:
- `--repair` regenerate missing `paper-YYYY-MM-DD.json` from `.txt`
- `--publish` update destination `latest.txt`, `latest.json`, and `manifest.json`
- `--source` / `--dest` override directories

### Ops Pulse (status snapshot)

```bash
python3 ops_pulse.py
```

Outputs a JSON status summary of latest source files, published files, and manifest health.

## Notes

- This is client-side password protection (lightweight gate, not strong security).
- Questions are practice-style MCQs and reshuffled sets.
- For true server-side LLM marking/regeneration, add a backend endpoint (e.g. `/api/generate-set` + `/api/mark`).
- For production deployment under sgkakis subpath, serve this folder as a static route (e.g. `/olvl`).
