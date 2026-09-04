# AI SEO Visual Pipeline

Generate a consistent set of images for an SEO article or landing page.

1. Generate an article outline or key section topics.
2. For each section, use `enhance` with a suitable template to create a visual prompt.
3. Generate a cover image:
   ```bash
   python3 scripts/callirra_api.py generate-image \
     --model nano-banana-2 \
     --prompt "<cover prompt>" \
     --size 1024x1024 \
     --out ./cover.png
   ```
4. Generate supporting section images with the same style keywords.
5. Keep a consistent style by reusing one style block across prompts.
