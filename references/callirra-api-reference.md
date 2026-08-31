# Callirra API Reference

Base URL: `https://api.callirra.com`

Authentication: `Authorization: Bearer sk-cal-...`

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/v1/models` | List models |
| GET | `/v1/balance` | Balance and available credits |
| GET | `/v1/usage` | Recent usage |
| POST | `/v1/images/generations` | Generate an image |
| POST | `/v1/videos` | Create a video task |
| GET | `/v1/videos/{id}` | Get task status |
| GET | `/v1/videos/{id}/content` | Download completed video |
| POST | `/v1/videos/{id}/cancel` | Cancel task |
| POST | `/v1/media/references` | Upload reference media |

## Image Example

```bash
curl https://api.callirra.com/v1/images/generations \
  -H "Authorization: Bearer sk-cal-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana",
    "prompt": "A cinematic product hero shot",
    "size": "1024x1024",
    "n": 1
  }'
```

## Video Example

```bash
curl -X POST https://api.callirra.com/v1/videos \
  -H "Authorization: Bearer sk-cal-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2.5",
    "prompt": "A drone shot over snowy mountains",
    "duration_seconds": 10,
    "resolution": "720p"
  }'
```

## Common Models

| Model | Type |
|---|---|
| `nano-banana` | Image |
| `gpt-image-2` | Image |
| `seedream-5-pro` | Image |
| `seedance-2.5` | Video |
| `kling-3.0` | Video |
| `minimax-h3` | Video |
