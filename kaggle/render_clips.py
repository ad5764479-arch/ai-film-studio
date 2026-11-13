# Runs automatically on Kaggle free T4 x2 GPU when pushed from GitHub Actions
import json
import os
import subprocess
from pathlib import Path

GITHUB_REPO = "__GITHUB_REPO__"
HF_DATASET_REPO = "__HF_DATASET_REPO__"
HF_TOKEN = "__HF_TOKEN__"
BATCH_START = int("__BATCH_START__")
BATCH_END = int("__BATCH_END__")

subprocess.run(["pip", "install", "-q", "diffusers", "transformers", "accelerate", "huggingface_hub", "imageio-ffmpeg"], check=True)

import torch
from diffusers import WanPipeline
from diffusers.utils import export_to_video
from huggingface_hub import HfApi

# 1. Pull latest scenes.json from GitHub
subprocess.run(["git", "clone", f"https://github.com/{GITHUB_REPO}.git", "repo"], check=True)
scenes_data = json.loads(Path("repo/scenes.json").read_text(encoding="utf-8"))

# 2. Load lightweight Wan2.1 1.3B model (fits on free 16GB T4 GPU)
pipe = WanPipeline.from_pretrained("Wan-AI/Wan2.1-T2V-1.3B-Diffusers", torch_dtype=torch.float16)
pipe.to("cuda")

out_dir = Path("rendered_clips")
out_dir.mkdir(exist_ok=True)
api = HfApi(token=HF_TOKEN)

for scene in scenes_data["scenes"]:
    sid = scene["id"]
    if not (BATCH_START <= sid <= BATCH_END):
        continue
    print(f"Rendering scene {sid:04d}...")
    output = pipe(
        prompt=scene["visual_prompt"],
        negative_prompt="blurry, low quality, distorted, watermark, text",
        height=480,
        width=832,
        num_frames=81,
        guidance_scale=5.0,
    ).frames[0]

    mp4_path = out_dir / f"scene_{sid:04d}.mp4"
    export_to_video(output, str(mp4_path), fps=16)

    api.upload_file(
        path_or_fileobj=str(mp4_path),
        path_in_repo=f"clips/scene_{sid:04d}.mp4",
        repo_id=HF_DATASET_REPO,
        repo_type="dataset",
    )
    print(f"Uploaded scene_{sid:04d}.mp4 to Hugging Face Dataset")
