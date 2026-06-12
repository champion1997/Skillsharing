#!/usr/bin/env python3
"""Agnes Video Generation CLI - 通过 Agnes AI 生成视频"""
import requests
import yaml
import sys
import json
import os
import time

def load_config():
    with open("/home/admin/.hermes/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config["model"]["api_key"], config["model"]["base_url"]

def poll_video(video_id, api_key, base_url, timeout=300, interval=5):
    """轮询等待视频生成完成"""
    # 注意: /agnesapi 不带 /v1 前缀
    poll_base = base_url.replace("/v1", "")
    url = f"{poll_base}/agnesapi"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{url}?video_id={video_id}", headers=headers, timeout=30)
        if r.status_code != 200:
            return None, f"Poll error: {r.status_code} {r.text}"
        result = r.json()
        status = result.get("status", "")
        print(f"  状态: {status} ({int(time.time()-start)}s)")
        if status == "completed":
            return result.get("remixed_from_video_id"), None
        elif status == "failed":
            return None, result.get("error", "Unknown error")
        elif status in ("queued", "in_progress"):
            time.sleep(interval)
        else:
            return None, f"Unknown status: {status}"
    return None, "Timeout"

def generate_video(prompt, width=1152, height=768, num_frames=121, frame_rate=24, 
                   save_dir=None, mode="ti2vid", image_url=None):
    api_key, base_url = load_config()
    
    # Step 1: 提交任务
    # /videos endpoint (base_url already includes /v1)
    url = f"{base_url}/videos"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    payload = {
        "model": "agnes-video-v2.0",
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_frames": num_frames,
        "frame_rate": frame_rate,
        "mode": mode
    }
    
    if image_url and mode in ("ti2vid", "keyframes"):
        payload["extra_body"] = {"image": [image_url], "mode": mode}
    
    print("提交任务...")
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} {r.text}")
        sys.exit(1)
    
    task = r.json()
    video_id = task.get("video_id")
    task_id = task.get("task_id")
    print(f"任务已提交: video_id={video_id}, task_id={task_id}")
    
    # Step 2: 轮询结果
    print("等待生成中...")
    video_url, err = poll_video(video_id, api_key, base_url)
    if err:
        print(f"ERROR: {err}")
        sys.exit(1)
    
    print(f"\n视频生成完成!")
    print(f"URL: {video_url}")
    
    # Step 3: 下载视频到本地 (optional)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        import hashlib
        fname = hashlib.md5(prompt.encode()).hexdigest()[:12] + ".mp4"
        video_path = os.path.join(save_dir, fname)
        print(f"正在下载到: {video_path}")
        vdata = requests.get(video_url, timeout=120).content
        with open(video_path, "wb") as f:
            f.write(vdata)
        print(f"SAVED: {video_path}")
        print(f"文件大小: {len(vdata)/1024/1024:.1f} MB")
    
    return video_url

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  文生视频: agnes_video.py '<prompt>' [width] [height] [frames] [fps] [save_dir]")
        print("  图生视频: agnes_video.py '<prompt>' --image <url> [save_dir]")
        print("Example: agnes_video.py '一只猫在海滩上散步' 1152 768 121 24")
        sys.exit(1)
    
    prompt = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 1152
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 768
    num_frames = int(sys.argv[4]) if len(sys.argv) > 4 else 121
    frame_rate = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    
    # Parse optional args
    image_url = None
    save_dir = None
    mode = "ti2vid"
    i = 6
    while i < len(sys.argv):
        if sys.argv[i] == "--image" and i + 1 < len(sys.argv):
            image_url = sys.argv[i+1]
            mode = "ti2vid"
            i += 2
        elif sys.argv[i] == "--keyframes":
            mode = "keyframes"
            i += 1
        else:
            save_dir = sys.argv[i]
            i += 1
    
    generate_video(prompt, width, height, num_frames, frame_rate, save_dir, mode, image_url)
