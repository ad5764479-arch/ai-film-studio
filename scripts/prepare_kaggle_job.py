import argparse
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, required=True)
parser.add_argument("--end", type=int, required=True)
parser.add_argument("--repo", type=str, required=True)
parser.add_argument("--hf-repo", type=str, required=True)
args = parser.parse_args()

kaggle_dir = Path("kaggle")
meta_path = kaggle_dir / "kernel-metadata.json"
meta = json.loads(meta_path.read_text(encoding="utf-8"))
username = os.environ["KAGGLE_USERNAME"]
meta["id"] = f"{username}/ai-film-clip-renderer"
meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

script_path = kaggle_dir / "render_clips.py"
code = script_path.read_text(encoding="utf-8")
code = (
    code.replace("__GITHUB_REPO__", args.repo)
    .replace("__HF_DATASET_REPO__", args.hf_repo)
    .replace("__BATCH_START__", str(args.start))
    .replace("__BATCH_END__", str(args.end))
    .replace("__HF_TOKEN__", os.environ["HF_TOKEN"])
)
script_path.write_text(code, encoding="utf-8")
print(f"Prepared Kaggle job for scenes {args.start}..{args.end}")
