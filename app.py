import os
import torch
from flask import Flask, render_template, request, jsonify, send_from_directory
from diffusers import WanPipeline
from diffusers.utils import export_to_video

app = Flask(__name__)

# Configuration
OUTPUT_DIR = "static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🚀 Loading Wan2.1-T2V-1.3B-Diffusers model for Lyra by Muhammad Taqi...")
MODEL_ID = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

# Load pipeline with memory optimization
pipe = WanPipeline.from_pretrained(
    MODEL_ID, 
    torch_dtype=torch.float16
)

# Enable CPU offloading to save VRAM (requires ~6-8GB VRAM)
if torch.cuda.is_available():
    pipe.enable_model_cpu_offload()
    print("✨ Model loaded successfully with CUDA offloading!")
else:
    print("⚠️ CUDA not detected. Running on CPU will be extremely slow.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_video():
    data = request.json
    prompt = data.get("prompt", "").strip()
    
    if not prompt:
        return jsonify({"error": "Prompt cannot be empty!"}), 400

    try:
        print(f"🎬 Generating video for prompt: '{prompt}'")
        
        # Run inference (Wan2.1 default frames usually range around 16-81 depending on configuration)
        # Using concise generation settings for performance
        output = pipe(
            prompt=prompt,
            height=480,
            width=832,
            num_frames=32,
            guidance_scale=5.0,
        ).frames
        
        # Save video file
        filename = f"lyra_{os.urandom(4).hex()}.mp4"
        filepath = os.path.join(OUTPUT_DIR, filename)
        export_to_video(output[0], filepath, fps=16)
        
        print(f"✅ Video successfully saved: {filepath}")
        return jsonify({"success": True, "video_url": f"/static/outputs/{filename}"})

    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
