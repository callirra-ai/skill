# Callirra API Reference

Base URL: `https://api.callirra.com`

Authentication: `Authorization: Bearer sk-cal-...` (API keys are created in the Callirra console → API Keys).

## Endpoints

Auth split: **`/v1/*`** = API-key endpoints (OpenAI-compatible; use your `sk-cal-` key). **`/api/v1/*`** = the web session endpoints (Bearer token from the web app) — the CLI/MCP/Skill work exclusively with `/v1/*` where available.

| Method | Path | Purpose |
|---|---|---|
| GET | `/v1/models` | List models (id/owned_by only; quotes live on the web `/api/v1/models`) |
| GET | `/v1/balance` | Balance and available credits |
| GET | `/v1/usage` | Recent usage |
| POST | `/v1/images/generations` | Generate an image (sync; returns `data[].url`) |
| POST | `/v1/videos` | Create a video task (returns `{ job }`) |
| GET | `/v1/videos` | List your recent video jobs (`{ data: [...] }`) |
| GET | `/v1/videos/{id}` | Get task status (`{ object, job }`) |
| GET | `/v1/videos/{id}/content` | Download completed video (key-authenticated) |
| POST | `/v1/videos/{id}/cancel` | Cancel task |
| POST | `/v1/media/references/upload` | Upload reference media (multipart, field `file`; image ≤20MB, audio ≤15MB, video ≤100MB) |
| POST | `/v1/media/references` | Upload reference media (base64 JSON, ≤~6MB binary) |
| GET | `/api/v1/prompts/templates` | ⚠️ retired — answers an empty list; use the bundled recipe snapshot (`recipes`, `recipe <slug>`, `scenes`) instead |
| POST | `/v1/prompts/enhance` | ⚠️ retired with the template catalogue: it needs a `templateId` that no longer exists, so it answers 404 |
| GET | `/api/v1/creative` | Get full curated creative knowledge base (public route; the skill script still needs a key configured before it will call anything) |
| POST | `/v1/templates/generate` | ⚠️ retired — the one-click entry point over an empty catalogue, so no template can be selected |

## Image Example

```bash
curl https://api.callirra.com/v1/images/generations \
  -H "Authorization: Bearer sk-cal-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana-2",
    "prompt": "A cinematic product hero shot",
    "size": "1024x1024",
    "n": 1,
    "nsfw_checker": true,
    "google_search": false
  }'
```

Returns `{ "data": [{ "url": "https://callirra.com/api/v1/media/reference/..." }] }` — **image URLs are HMAC-signed and expire after 24 hours; download/persist them promptly.**

## Video Example

```bash
curl -X POST https://api.callirra.com/v1/videos \
  -H "Authorization: Bearer sk-cal-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2.5",
    "prompt": "A drone shot over snowy mountains",
    "duration_seconds": 10,
    "resolution": "720p",
    "mode": "text-to-video",
    "aspect_ratio": "16:9",
    "generate_audio": true,
    "return_last_frame": false,
    "nsfw_checker": true,
    "google_search": false
  }'
```

Full video options include: `mode` (`text-to-video` | `image-to-video` | `video-to-video`), `duration_seconds`, `resolution`, `aspect_ratio`, `generate_audio`, `frame_images[]` (first/last frames), `input_references[]` (i2v refs), `input_images[]` + `input_videos[]` + `audio_input[]` (v2v reference media), `seed`, `seedance_mode`, `kling_mode`, `minimax_h3_mode`, `camera_fixed`, `kling_orientation`, `background_source`, `output_format` (`mp4`|`mov`), `return_last_frame`, `audio_setting` (`auto`|`origin`), `nsfw_checker`, `google_search`.

## Common Models

| Model | Type |
|---|---|
| `nano-banana-2` / `nanobanana-2-lite` / `nanobanana-pro` | Image |
| `gpt-image-2` | Image |
| `seedream-5-pro` / `seedream-5-lite` | Image |
| `z-image` | Image |
| `grok-imagine-image-2` | Image |
| `seedance-2.5` | Video |
| `seedance-2.0` (`seedance-2-toapi`) / `seedance-2.0-fast` / `seedance-2.0-mini` | Video |
| `seedance-1.0-pro` / `seedance-1.0-lite` / `seedance-1.0-pro-fast` | Video |
| `kling-3.0` / `kling-2.6` / `kling-o3` | Video |
| `kling-3.0-motion-control` | Video (v2v) |
| `kling-2.5-pro` | Video (i2v, tail frame) |
| `minimax-h3` | Video |
| `hailuo-2.3-standard` / `hailuo-2.3-pro` | Video (i2v) |
| `veo-3.1-fast` / `veo-3.1-quality` | Video |
| `gemini-omni-video` | Video |
| `grok-imagine-video-1.5-preview` | Video (i2v) |
| `happyhorse-1.0` / `happyhorse-1.0-first-frame` / `happyhorse-1.0-reference` / `happyhorse-1.0-video-edit` | Video |

Run `callirra models` (or `GET /v1/models`) for the authoritative live list.

## Notes

- All image/video generation requests are content-moderated before and after generation.
- `nsfw_checker` defaults to `true` (provider-side output filtering); the web UI exposes it per generation.
- Do not attempt to generate NSFW, deepfakes, hate speech, child-unsafe content, or copyright-infringing material.
- Failed/cancelled video tasks automatically refund reserved credits.
- Video output download: use `GET /v1/videos/{id}/content` with your API key (never expires, unlike image URLs).
