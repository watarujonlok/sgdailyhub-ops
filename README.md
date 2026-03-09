# sgdailyhub-ops

Automation and maintenance workspace for SGDailyHub content pipelines, publishing flows, and O-Level practice assets.

## What this repo does

- Maintains daily content/update workflows
- Publishes exam/practice paper artifacts (`.txt` / `.json`)
- Tracks operational automation via scheduled jobs
- Stores scripts/config/docs used for ongoing site ops

## Key paths

- `sgkakis-olvl-practice/` — practice-site assets and paper outputs
- `sgkakis-olvl-practice/daily_papers/` — generated daily papers
- `AGENTS.md`, `SOUL.md`, `TOOLS.md` — assistant operating docs

## Operations model

- Default: proactive maintenance and fixes
- Approval required for high-risk/sensitive changes
- Weekly autonomous activity report delivered via cron

## Notes

- Sensitive local runtime files are ignored via `.gitignore`.
- Use least-privilege tokens and rotate any exposed credentials.
