import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, snapshot_download

REPO_ID = os.environ.get("HF_DATASET_REPO")
TOKEN = os.environ.get("HF_TOKEN")

if not REPO_ID or not TOKEN:
    raise RuntimeError("HF_DATASET_REPO and HF_TOKEN must be set.")

api = HfApi(token=TOKEN)


def upload(local_dir: str, path_in_repo: str) -> None:
    api.create_repo(repo_id=REPO_ID, repo_type="dataset", exist_ok=True, private=True)
    api.upload_folder(
        folder_path=local_dir,
        path_in_repo=path_in_repo,
        repo_id=REPO_ID,
        repo_type="dataset",
    )
    print(f"Uploaded {local_dir} -> hf://datasets/{REPO_ID}/{path_in_repo}")


def download(path_in_repo: str, local_dir: str) -> None:
    Path(local_dir).mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=REPO_ID,
        repo_type="dataset",
        allow_patterns=f"{path_in_repo}/*",
        local_dir=".",
        token=TOKEN,
    )
    src = Path(path_in_repo)
    if src.exists() and str(src) != local_dir:
        for item in src.glob("*"):
            target = Path(local_dir) / item.name
            item.replace(target)
    print(f"Downloaded {path_in_repo} -> {local_dir}")


if __name__ == "__main__":
    action, arg1, arg2 = sys.argv[1], sys.argv[2], sys.argv[3]
    if action == "upload":
        upload(arg1, arg2)
    elif action == "download":
        download(arg1, arg2)
    else:
        raise ValueError("Usage: sync_hf.py [upload|download] <src> <dst>")
