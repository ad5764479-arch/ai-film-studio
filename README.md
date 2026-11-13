# Free GitHub + Kaggle GPU + Hugging Face AI Film Studio

Is repo se aap **GitHub Actions** ko apna central controller bana kar free mein 25-minute ki AI cinematic film bana sakte hain.

## Architecture
1. **GitHub Actions (Free CPU)**: `edge-tts` se Hindi/English narration + `.vtt` subtitles banata hai, Kaggle GPU job trigger karta hai, aur end mein **FFmpeg** se saari clips stitch karta hai.
2. **Kaggle Notebooks (Free T4 x2 GPU, 30 hrs/week)**: GitHub Actions se automatically trigger hota hai, `scenes.json` padh kar `Wan2.1-T2V-1.3B` se clips render karta hai.
3. **Hugging Face Datasets (Free 100 GB Private Storage)**: Saare rendered MP4 clips, audio, aur final 25-min film yahan store hoti hai (GitHub ki 500 MB artifact limit se bachne ke liye).

## Setup (Sirf 1 Baar)
1. Is folder ko ek naye GitHub repo mein push karein.
2. GitHub Repo **Settings > Secrets and variables > Actions** mein jayein:
   - **Variable** add karein: `HF_DATASET_REPO` = `aapka-hf-username/my-ai-film-assets`
   - **Secrets** add karein:
     - `HF_TOKEN`: Hugging Face write token (`https://huggingface.co/settings/tokens`)
     - `KAGGLE_USERNAME`: Aapka Kaggle username
     - `KAGGLE_KEY`: Aapka Kaggle API key (`kaggle.com/settings` > Create New Token)
3. **Actions** tab mein ja kar **AI Cinematic Film Pipeline** run karein:
   - Step 1: `stage = audio` run karein (saari voiceovers ban jayengi).
   - Step 2: `stage = trigger_kaggle_gpu` run karein (`batch_start=1`, `batch_end=15` — ek batch mein 10-15 clips render karein).
   - Step 3: Saari 250-300 clips complete hone par `stage = stitch_final` run karein — final film aapke Hugging Face Dataset mein save ho jayegi!
