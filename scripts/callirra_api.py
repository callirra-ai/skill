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


def run_templates() -> None:
    data = request("/api/v1/prompts/templates")
    for item in data.get("templates", []):
        print(f"{item['id']}\t{item['name']}\t{item['tagline']}")


def run_enhance(args: argparse.Namespace) -> None:
    body = {"templateId": args.template_id, "idea": args.idea}
    if args.kind:
        body["kind"] = args.kind
    if args.language:
        body["language"] = args.language
    result = request("/v1/prompts/enhance", "POST", body)
    print(json.dumps(result, indent=2))


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

    sub.add_parser("templates").set_defaults(func=lambda a: run_templates())

    p = sub.add_parser("enhance")
    p.add_argument("--template-id", required=True)
    p.add_argument("--idea", required=True)
    p.add_argument("--kind", choices=["video", "image"])
    p.add_argument("--language", choices=["zh", "en"])
    p.set_defaults(func=run_enhance)

    p = sub.add_parser("creative")
    p.add_argument("--full", action="store_true")
    p.set_defaults(func=run_creative)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
