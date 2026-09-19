#!/usr/bin/env python3
"""Thin Callirra API CLI for AI agents and terminal users.

Zero third-party dependencies. Uses the same public /v1 endpoints as @callirra/cli.
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = os.environ.get("CALLIRRA_API_BASE", "https://api.callirra.com").rstrip("/")
KEY_PREFIX = "sk-cal-"
CONFIG_FILE = Path.home() / ".config" / "callirra" / "api_key"


def save_key(key: str) -> Path:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(key.strip(), encoding="utf-8")
    return CONFIG_FILE


def load_key(explicit: str | None = None) -> str:
    key = (explicit or os.environ.get("CALLIRRA_API_KEY") or "").strip()
    if not key and CONFIG_FILE.exists():
        key = CONFIG_FILE.read_text(encoding="utf-8").strip()
    if not key:
        raise SystemExit("Missing API key. Run setup-api-key <key> or set CALLIRRA_API_KEY.")
    if not key.startswith(KEY_PREFIX):
        raise SystemExit(f"API key must start with {KEY_PREFIX}.")
    return key


def request(path: str, method: str = "GET", body: dict | None = None, key: str | None = None) -> dict:
    api_key = load_key(key)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            payload = res.read().decode("utf-8")
            return json.loads(payload) if payload else {}
    except urllib.error.HTTPError as err:
        try:
            detail = json.loads(err.read().decode("utf-8"))
            message = detail.get("error", {}).get("message", str(err))
        except Exception:
            message = str(err)
        raise SystemExit(f"Error {err.code}: {message}")


def run_models() -> None:
    data = request("/v1/models")["data"]
    for model in data:
        print(f"{model['id']}\t{model['owned_by']}")


def run_balance() -> None:
    balance = request("/v1/balance")
    print(f"credits: {balance['credits']}")
    print(f"available: {balance['available']}")


def run_usage(limit: int) -> None:
    data = request(f"/v1/usage?limit={limit}")["data"]
    for row in data:
        print(f"{row['created_at']}\t{row['model']}\t{row['category']}\t{row['cost_credits']} credits\t{row['status']}")
    if not data:
        print("No usage found.")


def run_generate_image(args: argparse.Namespace) -> None:
    body = {"model": args.model, "prompt": args.prompt}
    if args.size:
        body["size"] = args.size
    if args.n:
        body["n"] = args.n
    if args.reference:
        body["reference_images"] = [x.strip() for x in args.reference.split(",") if x.strip()]
    if args.image_input:
        body["image_input"] = args.image_input
    if args.nsfw_checker:
        body["nsfw_checker"] = True
    if args.google_search:
        body["google_search"] = True
    result = request("/v1/images/generations", "POST", body)
    images = result.get("data", [])
    urls = [img.get("url") for img in images if img.get("url")]
    first = images[0] if images else {}
    if args.out and first.get("b64_json"):
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(first["b64_json"]))
        print(f"Saved image to {args.out}")
        for url in urls:
            print(url)
    elif args.out and urls:
        # The live API returns signed URLs (no b64) — fetch so --out always
        # writes a file as advertised.
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(urls[0])
        with urllib.request.urlopen(req, timeout=120) as res:
            out.write_bytes(res.read())
        print(f"Saved image to {args.out}")
        for url in urls[1:]:
            print(url)
    elif urls:
        for url in urls:
            print(url)
    else:
        print(json.dumps(result, indent=2))


def download_video(job_id: str, out_path: str) -> None:
    api_key = load_key()
    req = urllib.request.Request(
        f"{API_BASE}/v1/videos/{job_id}/content",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(res.read())


def run_generate_video(args: argparse.Namespace) -> None:
    body = {"model": args.model, "prompt": args.prompt}
    if args.duration:
        body["duration_seconds"] = args.duration
    if args.resolution:
        body["resolution"] = args.resolution
    if args.mode:
        body["mode"] = args.mode
    if args.aspect:
        body["aspect_ratio"] = args.aspect
    if args.generate_audio:
        body["generate_audio"] = True
    if args.frame_image:
        body["frame_images"] = [x.strip() for x in args.frame_image.split(",") if x.strip()]
    if args.input_reference:
        body["input_references"] = [x.strip() for x in args.input_reference.split(",") if x.strip()]
    if args.input_images:
        body["input_images"] = [x.strip() for x in args.input_images.split(",") if x.strip()]
    if args.input_videos:
        body["input_videos"] = [x.strip() for x in args.input_videos.split(",") if x.strip()]
    if args.audio_input:
        body["audio_input"] = [x.strip() for x in args.audio_input.split(",") if x.strip()]
    if args.seed is not None:
        body["seed"] = args.seed
    if args.seedance_mode:
        body["seedance_mode"] = args.seedance_mode
    if args.kling_mode:
        body["kling_mode"] = args.kling_mode
    if args.kling_orientation:
        body["kling_orientation"] = args.kling_orientation
    if args.background_source:
        body["background_source"] = args.background_source
    if args.output_format:
        body["output_format"] = args.output_format
    if args.audio_setting:
        body["audio_setting"] = args.audio_setting
    if args.return_last_frame is not None:
        body["return_last_frame"] = bool(args.return_last_frame)
    if args.camera_fixed is not None:
        body["camera_fixed"] = bool(args.camera_fixed)
    if args.nsfw_checker is not None:
        body["nsfw_checker"] = bool(args.nsfw_checker)
    if args.google_search is not None:
        body["google_search"] = bool(args.google_search)
    job = request("/v1/videos", "POST", body)["job"]
    print(f"Job created: {job['id']} ({job['status']})")
    if args.wait:
        started = time.time()
        while True:
            state = request(f"/v1/videos/{job['id']}")["job"]
            if state["status"] in ("completed", "failed", "cancelled", "expired"):
                print(json.dumps(state, indent=2))
                if state["status"] == "completed":
                    if args.out:
                        download_video(job["id"], args.out)
                        print(f"Saved video to {args.out}")
                else:
                    sys.exit(1)
                break
            if time.time() - started > 900:
                raise SystemExit("Task timed out after 900s.")
            time.sleep(5)
    elif not args.wait and args.out:
        print("--out only applies together with --wait.")


def run_task(task_id: str) -> None:
    print(json.dumps(request(f"/v1/videos/{task_id}")["job"], indent=2))


def run_cancel(task_id: str) -> None:
    print(json.dumps(request(f"/v1/videos/{task_id}/cancel", "POST")["job"], indent=2))


def run_upload(args: argparse.Namespace) -> None:
    data = base64.b64encode(Path(args.file).read_bytes()).decode("utf-8")
    result = request("/v1/media/references", "POST", {
        "data": data,
        "content_type": args.content_type or "image/png",
        "filename": Path(args.file).name,
    })
    print(json.dumps(result, indent=2))


RECIPES_PATH = Path(__file__).resolve().parent.parent / "references" / "prompt-recipes.json"
SCENES_PATH = Path(__file__).resolve().parent.parent / "references" / "scene-recipes.json"


def _load(path: Path) -> dict:
    """The recipe snapshots ship with the skill; nothing to fetch and no key needed."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def run_recipes(args: argparse.Namespace) -> None:
    """List the curated prompt library.

    This replaces the old 'templates' command: the endpoint it called now answers an empty list, so it printed
    nothing. The library itself is alive and is what the site /seedance-prompt-library renders.
    """
    data = _load(RECIPES_PATH)
    rows = [
        r
        for r in data["recipes"]
        if (not args.category or r["category"] == args.category)
        and (not args.scene or r["scene"] == args.scene)
    ]
    print(f"{len(rows)} recipe(s) — categories: {', '.join(sorted(data['byCategory']))}")
    for r in rows[: args.limit]:
        print(f"{r['slug']}\t{r['title']}\t{r['category']}\t{r['scene']}\t{r['credits']} credits")


def run_recipe(args: argparse.Namespace) -> None:
    """One recipe in full: the prompt, its settings, the credits, and the deep link."""
    data = _load(RECIPES_PATH)
    found = next((r for r in data["recipes"] if r["slug"] == args.slug), None)
    if found is None:
        raise SystemExit(f"No recipe '{args.slug}'. Run 'recipes' to list them.")
    print(f"{found['title']}\n{found['category']} · {found['scene']} · {found['credits']} credits\n")
    print(found["prompt"])
    print(f"\nSettings: {json.dumps(found['config'])}")
    if found.get("deepLink"):
        print(f"Open in the generator: {found['deepLink']}")


def run_scenes(args: argparse.Namespace) -> None:
    """The six worked Seedance 2.5 scenes: prompt, settings, credits, and what a filtered route refuses."""
    data = _load(SCENES_PATH)
    if not args.slug:
        print(f"{data['count']} worked scenes — {', '.join(data['slugs'])}")
        for s in data["scenes"]:
            st = s["settings"]
            print(f"  {s['slug']:<11} {s['title']}  ({st['modelLabel']} · {st['aspectRatio']} · {st['duration']}s · {st['credits']} credits)")
        print("\nShow one with: scenes <slug>")
        return
    found = next((s for s in data["scenes"] if s["slug"] == args.slug), None)
    if found is None:
        raise SystemExit(f"No scene '{args.slug}'. Available: {', '.join(data['slugs'])}")
    print(f"{found['title']}\n")
    print(found["prompt"])
    print(f"\nSettings: {json.dumps(found['settings'])}")
    print(f"A filtered route refuses: {' | '.join(found['refused'])}")
    print(f"Page: {found['page']}")


def run_creative(args: argparse.Namespace) -> None:
    data = request("/api/v1/creative")
    if args.full:
        print(json.dumps(data, indent=2))
        return
    print(f"version: {data.get('version')}")
    print(f"categories: {len(data.get('categories', []))}")
    print(f"resources: {len(data.get('resources', []))}")
    print(f"styles: {len(data.get('styles', []))}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="callirra-api", description="Callirra API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup-api-key")
    p.add_argument("key")
    p.set_defaults(func=lambda a: print(f"API key saved to {save_key(a.key)}"))

    sub.add_parser("models").set_defaults(func=lambda a: run_models())
    sub.add_parser("balance").set_defaults(func=lambda a: run_balance())

    p = sub.add_parser("usage")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=lambda a: run_usage(a.limit))

    p = sub.add_parser("generate-image")
    p.add_argument("--model", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--size")
    p.add_argument("--n", type=int)
    p.add_argument("--reference")
    p.add_argument("--image-input")
    p.add_argument("--nsfw-checker", action="store_true")
    p.add_argument("--google-search", action="store_true")
    p.add_argument("--out")
    p.set_defaults(func=run_generate_image)

    p = sub.add_parser("generate-video")
    p.add_argument("--model", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--duration", type=int)
    p.add_argument("--resolution")
    p.add_argument("--mode")
    p.add_argument("--aspect", "--aspect-ratio", dest="aspect")
    p.add_argument("--generate-audio", action="store_true")
    p.add_argument("--frame-image")
    p.add_argument("--input-reference")
    p.add_argument("--input-images")
    p.add_argument("--input-videos")
    p.add_argument("--audio-input")
    p.add_argument("--seed", type=int)
    p.add_argument("--seedance-mode")
    p.add_argument("--kling-mode")
    p.add_argument("--kling-orientation")
    p.add_argument("--background-source")
    p.add_argument("--output-format")
    p.add_argument("--audio-setting")
    p.add_argument("--return-last-frame", action="store_true")
    p.add_argument("--camera-fixed", action="store_true")
    p.add_argument("--nsfw-checker", action="store_true")
    p.add_argument("--google-search", action="store_true")
    p.add_argument("--out")
    p.add_argument("--wait", action="store_true")
    p.set_defaults(func=run_generate_video)

    p = sub.add_parser("task")
    p.add_argument("id")
    p.set_defaults(func=lambda a: run_task(a.id))

    p = sub.add_parser("cancel")
    p.add_argument("id")
    p.set_defaults(func=lambda a: run_cancel(a.id))

    p = sub.add_parser("upload")
    p.add_argument("--file", required=True)
    p.add_argument("--content-type")
    p.set_defaults(func=run_upload)

    p = sub.add_parser("recipes", help="List the curated prompt library (172 recipes)")
    p.add_argument("--category")
    p.add_argument("--scene", choices=["text-to-video", "image-to-video"])
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=run_recipes)

    p = sub.add_parser("recipe", help="Show one recipe in full")
    p.add_argument("slug")
    p.set_defaults(func=run_recipe)

    p = sub.add_parser("scenes", help="Show the six worked Seedance 2.5 scene recipes")
    p.add_argument("slug", nargs="?")
    p.set_defaults(func=run_scenes)

    p = sub.add_parser("creative")
    p.add_argument("--full", action="store_true")
    p.set_defaults(func=run_creative)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
