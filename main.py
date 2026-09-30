from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from gradio_client import Client
import requests

app = FastAPI()

# Futuristic HTML Interface Design
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lyra AI - Futuristic Video Generator</title>
    <style>
        :root {
            --bg-color: #0b0c10;
            --card-bg: #1f2833;
            --accent-neon: #66fcf1;
            --accent-dim: #45a29e;
            --text-main: #c5c6c7;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 100vh;
        }
        .container {
            width: 90%;
            max-width: 600px;
            text-align: center;
            margin-top: 50px;
        }
        h1 {
            font-size: 3rem;
            color: #ffffff;
            margin-bottom: 5px;
            letter-spacing: 2px;
            text-shadow: 0 0 10px var(--accent-neon), 0 0 20px var(--accent-neon);
        }
        .subtitle {
            color: var(--accent-dim);
            font-size: 1rem;
            margin-bottom: 40px;
            text-transform: uppercase;
            letter-spacing: 3px;
        }
        .input-box {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(4px);
        }
        textarea {
            width: 100%;
            height: 100px;
            background: #121821;
            border: 1px solid var(--accent-dim);
            border-radius: 8px;
            color: #fff;
            padding: 12px;
            font-size: 1rem;
            resize: none;
            box-sizing: border-box;
            outline: none;
            transition: 0.3s;
        }
        textarea:focus {
            border-color: var(--accent-neon);
            box-shadow: 0 0 10px rgba(102, 252, 241, 0.5);
        }
        button {
            background: linear-gradient(45deg, var(--accent-dim), var(--accent-neon));
            color: #000;
            border: none;
            padding: 14px 30px;
            font-size: 1.1rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 20px;
            width: 100%;
            transition: 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 252, 241, 0.4);
        }
        #resultContainer {
            margin-top: 30px;
            display: none;
        }
        .loader {
            display: none;
            margin: 20px auto;
            border: 4px solid #121821;
            border-radius: 50%;
            border-top: 4px solid var(--accent-neon);
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        video {
            width: 100%;
            border-radius: 12px;
            border: 2px solid var(--accent-neon);
            box-shadow: 0 0 15px rgba(102, 252, 241, 0.3);
        }
        footer {
            margin-bottom: 20px;
            font-size: 0.9rem;
            color: #888;
            letter-spacing: 1px;
        }
        footer span {
            color: var(--accent-neon);
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>LYRA AI</h1>
        <div class="subtitle">Next-Gen Video Generation</div>
        
        <div class="input-box">
            <textarea id="promptInput" placeholder="Describe the video you want Lyra to generate... (e.g., A beautiful futuristic floating city)"></textarea>
            <button id="genBtn" onclick="generateVideo()">Create Magic</button>
            
            <div class="loader" id="loader"></div>
            
            <div id="resultContainer">
                <p style="color: var(--accent-neon); font-weight: 500;" id="statusText"></p>
                <video id="videoPlayer" controls autoplay loop src=""></video>
            </div>
        </div>
    </div>

    <footer>
        Created with ❤️ by <span>Muhammad Taqi</span>
    </footer>

    <script>
        async function generateVideo() {
            const prompt = document.getElementById('promptInput').value;
            const btn = document.getElementById('genBtn');
            const loader = document.getElementById('loader');
            const resultContainer = document.getElementById('resultContainer');
            const videoPlayer = document.getElementById('videoPlayer');
            const statusText = document.getElementById('statusText');

            if (!prompt.trim()) {
                alert("Please enter a prompt first!");
                return;
            }

            // UI Changes for Loading State
            btn.disabled = true;
            btn.innerText = "Lyra is thinking...";
            loader.style.display = "block";
            resultContainer.style.display = "none";

            try {
                const response = await fetch(`/api/generate?prompt=${encodeURIComponent(prompt)}`);
                const data = await response.json();

                if (data.status.includes("Success")) {
                    videoPlayer.src = data.video_url;
                    statusText.innerText = `Status: ${data.status}`;
                    resultContainer.style.display = "block";
                } else {
                    alert("Error: " + data.message);
                }
            } catch (error) {
                alert("Something went wrong with Lyra's core.");
            } finally {
                btn.disabled = false;
                btn.innerText = "Create Magic";
                loader.style.display = "none";
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return html_content

@app.get("/api/generate")
def generate_video(prompt: str):
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # 1. Main AI Engine (Hugging Face Free Space)
    try:
        hf_client = Client("kingnish/instant-video") 
        result = hf_client.predict(
            prompt=prompt,
            base_model="Diffusion",
            motion_model="Default",
            steps=20,
            api_name="/instant_video"
        )
        if result and isinstance(result, dict) and 'video' in result:
            return {
                "status": "Success (AI Generated by Lyra)",
                "video_url": result['video']['url']
            }
    except Exception:
        pass
            
    # 2. Backup Engine (If AI is sleeping/busy)
    try:
        search_url = f"https://pexels.com{prompt}&per_page=1"
        headers = {"Authorization": "53307735b2d8cd1d44794c472286522c"} 
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('videos'):
                return {
                    "status": "Success (Lyra Cloud Sync)",
                    "video_url": data['videos'][0]['video_files'][0]['link']
                }
    except Exception:
        pass

    return {"status": "Error", "message": "All engines are currently busy. Try again!"}
