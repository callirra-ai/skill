# Callirra Media Generator Skill

An open-source AI agent skill for generating and monitoring Callirra image and video tasks.

Works with Claude Code, Codex, Cursor and other skill-enabled AI coding platforms.

## Quick Start

```bash
python3 scripts/callirra_api.py setup-api-key "<your-api-key>"
```

Then ask your agent to use `$callirra-media-generator-skill` to create images or videos.

## Commands

```bash
python3 scripts/callirra_api.py models
python3 scripts/callirra_api.py balance
python3 scripts/callirra_api.py templates
python3 scripts/callirra_api.py enhance --template-id cinematic-city --idea "Rainy Tokyo street" --kind video
python3 scripts/callirra_api.py creative
python3 scripts/callirra_api.py generate-image --model nano-banana --prompt "A cinematic hero shot" --out hero.png
python3 scripts/callirra_api.py generate-video --model seedance-2.5 --prompt "A drone shot" --duration 10 --wait
```

## Content

- `SKILL.md` — main skill instructions
- `scripts/callirra_api.py` — zero-dependency Python CLI
- `references/callirra-api-reference.md` — API reference
- `references/creative-knowledge.json` — full curated creative knowledge base (110 resources, 8 categories, 39 styles)
- `workflows/` — reusable recipe workflows

---

→ Start free at [callirra.com](https://callirra.com?utm_source=github-skill)
