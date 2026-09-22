# Image Generation Workflow

> ⚠️ **The built-in template catalogue and `enhance` were retired (Sep 2026) and are not coming back.**
> `PROMPT_TEMPLATES` is an empty array, so there is no `templates` and no `enhance` sub-command.

1. Ask the user for the visual goal or prompt.
2. Run `python3 scripts/callirra_api.py creative` to load curated style and resource knowledge.
3. For a ready-made professional **image** prompt, take a template from the website's Image Prompts Studio
   (`https://callirra.com/image-prompts-studio` — 30 templates, each with several prompt sets) and use it as
   the `--prompt` text. The bundled recipe library is video-oriented, so it is not the place to look here:
   ```bash
   python3 scripts/callirra_api.py recipes   # video recipes — listed for completeness, not for stills
   ```
4. Run `python3 scripts/callirra_api.py models` and choose a suitable image model.
5. If a reference image is needed, run `python3 scripts/callirra_api.py upload --file ./frame.png`.
6. Generate:
   ```bash
   python3 scripts/callirra_api.py generate-image \
     --model nano-banana-2 \
     --prompt "<template prompt adapted to the user idea>" \
     --size 1024x1024 \
     --out ./output.png
   ```
7. Return the output path or URL and ask whether the user wants revisions.
