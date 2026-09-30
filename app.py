import os
import asyncio
import numpy as np
import requests
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    AudioArrayClip,
    CompositeAudioClip,
    concatenate_videoclips
)

# ==========================================
# CONFIGURATION - LYRA AI
# Created by Muhammad Taqi
# ==========================================
SCRIPT_TEXT = (
    "Hello! Welcome to Lyra AI. "
    "This video, voiceover, and audio setup was automatically generated "
    "using GitHub Actions without requiring any API token."
)
WATERMARK_TEXT = "LYRA - Created by Muhammad Taqi"
VOICE = "en-US-ChristopherNeural"  # Urdu ke liye "ur-PK-AsadNeural" use kar sakte hain
AUDIO_FILE = "voice.mp3"
BGM_FILE = "ambient_bgm.wav"
OUTPUT_VIDEO = "lyra_output.mp4"

# Prompts for scene visuals
PROMPTS = [
    "cinematic shot of glowing AI neural core, futuristic, 8k resolution",
    "cyberpunk city street at night with neon rain reflections",
    "abstract digital universe background, ultra high definition"
]

async def generate_voiceover():
    """Generates natural AI voice using Edge-TTS (No Token)."""
    print("🎙️ Generating AI Voiceover...")
    communicate = edge_tts.Communicate(SCRIPT_TEXT, VOICE)
    await communicate.save(AUDIO_FILE)
    print("✅ Voiceover generated successfully.")

def generate_background_music(duration, output_path=BGM_FILE, sample_rate=44100):
    """Generates ambient ambient background music procedurally (No Token/Files needed)."""
    print("🎵 Synthesizing background music...")
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Ambient chords synthesis (Soft synth pads)
    note1 = 0.05 * np.sin(2 * np.pi * 220 * t)  # A3
    note2 = 0.04 * np.sin(2 * np.pi * 277.18 * t)  # C#4
    note3 = 0.04 * np.sin(2 * np.pi * 329.63 * t)  # E4
    
    audio_data = note1 + note2 + note3
    # Stereo framing
    audio_stereo = np.column_stack((audio_data, audio_data))
    
    bgm_clip = AudioArrayClip(audio_stereo, fps=sample_rate)
    bgm_clip.write_audiofile(output_path, fps=sample_rate, logger=None)
    print("✅ Background music created.")

def fetch_image_public(prompt, filename):
    """Fetches high quality AI images using public endpoints (No Token)."""
    print(f"🖼️ Fetching visual frame for: '{prompt[:30]}...'")
    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"
    
    res = requests.get(url, timeout=40)
    if res.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(res.content)
        print("✅ Frame downloaded.")
    else:
        raise Exception(f"Failed to fetch image: {res.status_code}")

def apply_watermark(image_path):
    """Applies LYRA watermark overlay to each image frame."""
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 26)
    except IOError:
        font = ImageFont.load_default()

    x, y = 30, 30
    # Black text border/shadow
    for offset_x, offset_y in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        draw.text((x + offset_x, y + offset_y), WATERMARK_TEXT, fill="black", font=font)
    
    # White main text
    draw.text((x, y), WATERMARK_TEXT, fill="white", font=font)
    img.save(image_path)

def build_video():
    """Compiles audio, images, and music into final MP4."""
    image_files = []
    for idx, prompt in enumerate(PROMPTS):
        img_name = f"frame_{idx}.jpg"
        fetch_image_public(prompt, img_name)
        apply_watermark(img_name)
        image_files.append(img_name)

    voice_audio = AudioFileClip(AUDIO_FILE)
    total_duration = voice_audio.duration
    
    # Generate BGM matching the voice duration
    generate_background_music(total_duration)
    bgm_audio = AudioFileClip(BGM_FILE).volumex(0.2)  # Low volume for background
    
    # Combine Voiceover + BGM
    final_audio = CompositeAudioClip([voice_audio, bgm_audio])

    # Calculate image duration split
    duration_per_image = total_duration / len(image_files)
    clips = [ImageClip(img).set_duration(duration_per_image) for img in image_files]
    
    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(final_audio)

    print("⚡ Compiling video via FFmpeg...")
    video.write_videofile(
        OUTPUT_VIDEO,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )
    print(f"\n🎉 SUCCESS! Video exported to {OUTPUT_VIDEO}")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
    build_video()
