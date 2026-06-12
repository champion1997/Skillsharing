#!/usr/bin/env python3
"""Agnes Image Generation - 仅返回URL，不下载"""
import requests
import yaml
import sys
import json

def load_config():
    with open("/home/admin/.hermes/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["model"]["api_key"], config["model"]["base_url"]

def generate_image(prompt, size="1024x1024", model="agnes-image-2.1-flash"):
    api_key, base_url = load_config()
    url = f"{base_url}/images/generations"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "extra_body": {"response_format": "url"}
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} {r.text}")
        sys.exit(1)
    result = r.json()
    if result.get("data") and result["data"][0].get("url"):
        img_url = result["data"][0]["url"]
        revised_prompt = result["data"][0].get("revised_prompt", prompt)
        print(f"URL: {img_url}")
        print(f"Prompt: {revised_prompt}")
    else:
        print(f"ERROR: No image in response")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: agnes_image.py '<prompt>' [size] [model]")
        sys.exit(1)
    prompt = sys.argv[1]
    size = sys.argv[2] if len(sys.argv) > 2 else "1024x1024"
    model = sys.argv[3] if len(sys.argv) > 3 else "agnes-image-2.1-flash"
    generate_image(prompt, size, model)
