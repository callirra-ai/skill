# Image Generation Workflow

1. Ask the user for the visual goal or prompt.
2. Run `python3 scripts/callirra_api.py creative` to load curated style and resource knowledge.
3. If the user wants a professional prompt, list templates and enhance:
   ```bash
   python3 scripts/callirra_api.py templates
   python3 scripts/callirra_api.py enhance \
     --template-id product-hero \
     --idea "<user idea>" \
     --kind image
   ```
4. Run `python3 scripts/callirra_api.py models` and choose a suitable image model.
5. If a reference image is needed, run `python3 scripts/callirra_api.py upload --file ./frame.png`.
6. Generate:
   ```bash
   python3 scripts/callirra_api.py generate-image \
     --model nano-banana \
     --prompt "<enhanced prompt>" \
     --size 1024x1024 \
     --out ./output.png
   ```
7. Return the output path or URL and ask whether the user wants revisions.
