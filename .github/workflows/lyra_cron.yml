import os
import re
import asyncio
import requests
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# ==========================================
# LYRA AI GENERATOR - Created by Muhammad Taqi
# ==========================================

# User Yahan Apna Any Prompt De Sakta Hai
USER_PROMPT = """
Scene 1:
Visual: A cute toddler sitting on classroom floor next to an adult male teacher in traditional clothes.
Dialogue (Teacher): "Beta, kal ka English ka sabaq yaad hai?"
Dialogue (Baby): "Haan! Aage se hat jao ko kehne ke liye peep peep bolte hain!"

Scene 2:
Visual: Cute toddler wearing glasses sitting on doctor examination table in clinic.
Dialogue (Doctor): "Acha beta, aapka weight kitna hai?"
Dialogue (Baby): "Chashme ke sath 15 kilo, aur bina chashme ke mujhe dikhta kahan!"

Scene 3:
Visual: Cute toddler wearing a black t-shirt looking directly at camera smiling.
Dialogue (Baby): "Ruko ruko! Kahan ja rahe ho? Channel ko subscribe aur video ko like toh kar do!"
"""

WATERMARK_TEXT = "LYRA - Created by Muhammad Taqi"
VOICE_MALE = "ur-PK-AsadNeural"
OUTPUT_VIDEO = "lyra_output.mp4"


def parse_prompt(prompt_text):
    """User prompt se scenes, visuals, aur dialogues extract karta hai."""
    scenes_data = []
    raw_scenes = re.split(r'Scene\s*\d+:', prompt_text, flags=re.IGNORECASE)
    
    for raw_scene in raw_scenes:
        if not raw_scene.strip():
            continue
            
        visual_match = re.search(r'Visual:\s*(.*?)(?=\n|Dialogue|$)', raw_scene, re.IGNORECASE | re.DOTALL)
        visual_prompt = visual_match.group(1).strip() if visual_match else "Cute baby in cinematic realistic lighting"
        
        dialogues = re.findall(r'Dialogue\s*\((.*?)\):\s*"(.*?)"', raw_scene)
        
        if dialogues:
            for speaker, text in dialogues:
                scenes_data.append({
                    "speaker": speaker,
                    "text": text,
                    "visual": visual_prompt
                })
        else:
            # Fallback if no dialogue tags found
            scenes_data.append({
                "speaker": "Speaker",
                "text": raw_scene.strip(),
                "visual": visual_prompt
            })
            
    return scenes_data


async def generate_audio(text, outfile):
    """Edge-TTS se voiceover generate karta hai (No Token)."""
    communicate = edge_tts.Communicate(text, VOICE_MALE)
    await communicate.save(outfile)


def fetch_image(visual_prompt, outfile):
    """Pollinations Public API se prompt ke mutabiq image download karta hai."""
    encoded = requests.utils.quote(f"{visual_prompt}, 8k photorealistic cinematic lighting")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=720&height=1280&nologo=true"
    
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            with open(outfile, 'wb') as f:
                f.write(res.content)
            return
    except Exception as e:
        print(f"Warning fetching image: {e}")
        
    # Fallback image
    img = Image.new('RGB', (720, 1280), color=(40, 40, 50))
    img.save(outfile)


def apply_watermark(image_path):
    """Watermark overlay karta hai."""
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 26)
    except IOError:
        font = ImageFont.load_default()

    x, y = 30, 40
    for offset_x, offset_y in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        draw.text((x + offset_x, y + offset_y), WATERMARK_TEXT, fill="black", font=font)
    
    draw.text((x, y), WATERMARK_TEXT, fill="white", font=font)
    img.save(image_path)


def build_video():
    scenes = parse_prompt(USER_PROMPT)
    video_clips = []
    
    print(f"Total Scenes Detected: {len(scenes)}")
    
    for idx, scene in enumerate(scenes):
        audio_file = f"audio_{idx}.mp3"
        img_file = f"frame_{idx}.jpg"
        
        # Audio & Image generation
        asyncio.run(generate_audio(scene["text"], audio_file))
        fetch_image(scene["visual"], img_file)
        apply_watermark(img_file)
        
        # Clip creation
        audio_clip = AudioFileClip(audio_file)
        img_clip = ImageClip(img_file).set_duration(audio_clip.duration)
        clip = img_clip.set_audio(audio_clip)
        
        video_clips.append(clip)
        
    print("⚡ Merging all scenes into final video...")
    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile(
        OUTPUT_VIDEO,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
    print(f"\n🎉 SUCCESS! Video exported: {OUTPUT_VIDEO}")


if __name__ == "__main__":
    build_video()
