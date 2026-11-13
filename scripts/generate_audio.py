import asyncio
import json
from pathlib import Path
import edge_tts

SCENES_FILE = Path("scenes.json")
AUDIO_DIR = Path("assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def synth_scene(scene: dict, voice: str) -> None:
    sid = f"{scene['id']:04d}"
    mp3_path = AUDIO_DIR / f"scene_{sid}.mp3"
    vtt_path = AUDIO_DIR / f"scene_{sid}.vtt"

    communicate = edge_tts.Communicate(scene["narration"], voice)
    submaker = edge_tts.SubMaker()

    with open(mp3_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    with open(vtt_path, "w", encoding="utf-8") as sub_file:
        sub_file.write(submaker.get_srt())
    print(f"Generated {mp3_path} and {vtt_path}")


async def main() -> None:
    data = json.loads(SCENES_FILE.read_text(encoding="utf-8"))
    voice = data.get("voice", "hi-IN-SwaraNeural")
    for scene in data["scenes"]:
        await synth_scene(scene, voice)


if __name__ == "__main__":
    asyncio.run(main())
