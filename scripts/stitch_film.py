import json
import subprocess
from pathlib import Path

SCENES_FILE = Path("scenes.json")
CLIPS_DIR = Path("assets/clips")
AUDIO_DIR = Path("assets/audio")
OUT_DIR = Path("output")
WORK_DIR = Path("work_segments")

OUT_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

data = json.loads(SCENES_FILE.read_text(encoding="utf-8"))
concat_list = []

for scene in data["scenes"]:
    sid = f"{scene['id']:04d}"
    clip = CLIPS_DIR / f"scene_{sid}.mp4"
    audio = AUDIO_DIR / f"scene_{sid}.mp3"
    seg = WORK_DIR / f"seg_{sid}.mp4"

    if not clip.exists() or not audio.exists():
        print(f"Skipping scene {sid} (missing clip or audio)")
        continue

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(clip),
        "-i", str(audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(data.get("fps", 24)),
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(seg),
    ]
    subprocess.run(cmd, check=True)
    concat_list.append(f"file '{seg.resolve()}'")

if not concat_list:
    raise RuntimeError("No valid segments found to stitch.")

list_file = WORK_DIR / "concat.txt"
list_file.write_text("\n".join(concat_list), encoding="utf-8")

final_mp4 = OUT_DIR / "final_film.mp4"
subprocess.run(
    [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c", "copy",
        str(final_mp4),
    ],
    check=True,
)
print(f"Final film ready: {final_mp4}")
