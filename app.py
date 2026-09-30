import os
import time
import gradio as ui
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

def generate_lyra_video(user_prompt, use_audio):
    model_target = "Lightricks/LTX-2.5"
    try:
        response = client.post(
            model=model_target,
            json={
                "inputs": user_prompt,
                "parameters": {
                    "num_inference_steps": 30,
                    "guidance_scale": 7.0,
                    "height": 480,
                    "width": 832,
                    "with_audio": use_audio
                }
            }
        )
        output_path = "lyra_output.mp4"
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
        return f"❌ Error: {response.text}"
    except Exception as e:
        return f"⚠️ Timeout: {str(e)}"

with ui.Blocks(theme=ui.themes.Soft(primary_hue="purple", secondary_hue="indigo")) as lyra_app:
    ui.Markdown("# 🌌 LYRA Engine App Live Console")
    prompt_input = ui.Textbox(label="Enter Prompt", lines=3)
    audio_toggle = ui.Checkbox(label="Voice Output", value=True)
    generate_btn = ui.Button("🚀 Generate Video", variant="primary")
    video_preview = ui.Video(label="Download Preview")
    
    generate_btn.click(fn=generate_lyra_video, inputs=[prompt_input, audio_toggle], outputs=video_preview)

if __name__ == "__main__":
    # Link ko catch karke local text file mein likhna
    import threading
    def save_link():
        time.sleep(5)
        if lyra_app.share_url:
            with open("gradio_url.txt", "w") as f:
                f.write(lyra_app.share_url)
            print(f"🔗 Saved URL: {lyra_app.share_url}")
            
    threading.Thread(target=save_link, daemon=True).start()
    # App ko block karke running chhor dena
    lyra_app.launch(share=True, prevent_thread_lock=False)
    
    # GitHub Action 6 ghante tak active rahega
    print("⏳ Keeping instance alive for 6 Hours...")
    time.sleep(21300) # 5.9 Ghante tak server ko active rakhega
