# Video Generation Workflow

> ⚠️ **The built-in template catalogue was retired (Sep 2026)**: `PROMPT_TEMPLATES` is now an empty array,
> `GET /api/v1/prompts/templates` returns an empty list, and any `templateId` call returns 404. References to
> built-in templates or `--template-id` below are historical — use the prompt box or `prompts/enhance` instead.

1. Confirm the video concept, duration and aspect ratio.
2. Run `python3 scripts/callirra_api.py creative` to load cinematic vocabulary and style knowledge.
3. If the user wants a professional prompt, enhance with a video template:
   ```bash
   python3 scripts/callirra_api.py templates
   python3 scripts/callirra_api.py enhance \
     --template-id cinematic-city \
     --idea "<user idea>" \
     --kind video
   ```
4. Pick a video model from `python3 scripts/callirra_api.py models`.
5. Submit:
   ```bash
   python3 scripts/callirra_api.py generate-video \
     --model seedance-2.5 \
     --prompt "<enhanced prompt>" \
     --duration 10 \
     --resolution 720p \
     --wait \
     --out clip.mp4
   ```
6. Wait for terminal status and report the job id plus output URL or error.
7. If the task failed, report the error and suggest retry or model change.
