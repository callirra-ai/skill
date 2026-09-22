# Video Generation Workflow

> ⚠️ **The built-in template catalogue and `enhance` were retired (Sep 2026) and are not coming back.**
> `PROMPT_TEMPLATES` is an empty array, so there is no `templates` and no `enhance` sub-command. Use the
> bundled recipe library instead — offline, no key.

1. Confirm the video concept, duration and aspect ratio.
2. Run `python3 scripts/callirra_api.py creative` to load cinematic vocabulary and style knowledge.
3. Start from a recipe instead of an empty prompt box:
   ```bash
   python3 scripts/callirra_api.py recipes --category cinematic --limit 40
   python3 scripts/callirra_api.py recipe bridge-pursuit-headlights   # full prompt + settings + credits
   python3 scripts/callirra_api.py scenes                              # the six worked Seedance 2.5 scenes
   python3 scripts/callirra_api.py scenes wedding
   ```
   Adapt the prompt to the user's idea; keep the recipe's `config` (model, duration, aspect, resolution) as
   the starting settings — they are measured, not guessed.
4. Pick a video model from `python3 scripts/callirra_api.py models`.
5. Submit:
   ```bash
   python3 scripts/callirra_api.py generate-video \
     --model seedance-2.5 \
     --prompt "<adapted recipe prompt>" \
     --duration 10 \
     --resolution 720p \
     --wait \
     --out clip.mp4
   ```
6. Wait for terminal status and report the job id plus output URL or error.
7. If the task failed, report the error and suggest retry or model change.
