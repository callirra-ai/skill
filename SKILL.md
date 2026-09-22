---
name: callirra-media-generator-skill
description: Generate and monitor Callirra image and video tasks end-to-end. Use when work involves Callirra /v1 endpoints for listing models, uploading reference media, generating images or videos, polling task status, checking credits, or saving generated media.
---

# Callirra Media Generator Skill

## Overview

> ⚠️ **The built-in template catalogue and the `enhance` flow were retired (Sep 2026) and are not coming back.**
> `PROMPT_TEMPLATES` is an empty array, `GET /api/v1/prompts/templates` answers an empty list, and
> `POST /v1/prompts/enhance` requires a `templateId` that no longer exists — it answers 404. There is no
> `templates` and no `enhance` sub-command; the same goes for the one-click `/v1/templates/generate` entry.
>
> **Use the bundled recipe library instead** — it ships with this skill, needs no API key and no network:
> `recipes` lists 172 curated recipes, `recipe <slug>` prints one in full (prompt, settings, credits, deep
> link), and `scenes` covers the six worked Seedance 2.5 scenes. These prompts are video-oriented; for
> **image** prompts use an Image Prompts Studio template from the website and paste it into `--prompt`.

Use this skill to call Callirra APIs reliably, create image and video generation tasks, and return final media results with credit-aware behavior.

Callirra is an OpenAI-compatible AI media gateway. It supports top image and video models through one API key (`sk-cal-...`).

## Setup

Recommended one-time setup:

```bash
python3 scripts/callirra_api.py setup-api-key "<your-api-key>"
```

Or via environment:

```bash
export CALLIRRA_API_KEY="<your-api-key>"
```

The script stores the key at `~/.config/callirra/api_key`.

## Standard Flow

1. Discover available models and creative knowledge.
2. If the user wants a professional prompt, start from the bundled recipe library (`recipes`, `recipe <slug>`, `scenes`) — it ships with the skill and needs no key.
3. Upload reference images when the task needs local image inputs.
4. Create an image or video task.
5. Poll task status until final state.
6. Report the output URL or saved file.

## Core Commands

```bash
# List models
python3 scripts/callirra_api.py models

# Balance and usage
python3 scripts/callirra_api.py balance
python3 scripts/callirra_api.py usage --limit 10

# Generate an image
python3 scripts/callirra_api.py generate-image \
  --model nano-banana-2 \
  --prompt "A cinematic product hero shot" \
  --size 1024x1024 \
  --out hero.png

# Create a video and wait
python3 scripts/callirra_api.py generate-video \
  --model seedance-2.5 \
  --prompt "A drone shot over mountains" \
  --duration 10 \
  --resolution 720p \
  --wait \
  --out clip.mp4

# Inspect or cancel a task
python3 scripts/callirra_api.py task <TASK_ID>
python3 scripts/callirra_api.py cancel <TASK_ID>

# Upload a reference image
python3 scripts/callirra_api.py upload --file ./frame.png --content-type image/png

# Curated prompt library (bundled with the skill — offline, no key needed)
python3 scripts/callirra_api.py recipes
python3 scripts/callirra_api.py recipes --category cinematic --limit 40
python3 scripts/callirra_api.py recipe bridge-pursuit-headlights

# The six worked Seedance 2.5 scenes (prompt, settings, credits, and what a filtered route refuses)
python3 scripts/callirra_api.py scenes
python3 scripts/callirra_api.py scenes wedding

# Creative knowledge base (models, styles, resources)
python3 scripts/callirra_api.py creative
```

## API Reference

See `references/callirra-api-reference.md` for endpoint details and model examples.
See `references/creative-knowledge.json` for the full curated creative knowledge base (art, design, image, video resources, styles and cinematic vocabulary). It contains 110 resources, 8 categories and 39 style keywords.

## Error Handling

- `invalid_api_key`: verify key and re-run `setup-api-key`.
- `insufficient_quota`: check `/v1/balance`; ask the user to purchase a subscription or credit pack.
- `model_not_found`: list models and pick a supported slug.
- `upstream_error`: retry with backoff; report the upstream message if it persists.
- `not_found`: verify task id or model slug.

## Rules

- Send auth via `Authorization: Bearer <key>`.
- Use `sk-cal-` keys only.
- Prefer the special Callirra media endpoints for image/video, not generic chat models.
- For video tasks, always wait or poll until a terminal status before reporting success.
- Preserve the exact task id for audit traces.
