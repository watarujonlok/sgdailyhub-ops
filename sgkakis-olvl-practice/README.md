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

## Notes

- This is client-side password protection (lightweight gate, not strong security).
- Questions are practice-style MCQs and reshuffled sets.
- For true server-side LLM marking/regeneration, add a backend endpoint (e.g. `/api/generate-set` + `/api/mark`).
- For production deployment under sgkakis subpath, serve this folder as a static route (e.g. `/olvl`).
