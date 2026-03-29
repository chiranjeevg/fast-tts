from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="TTS Inference Server", version="0.1.0")


@app.get("/")
async def root():
    return {"status": "ok", "models_available": ["yourtts"]}


@app.post("/tts")
async def generate_speech(text: str, speaker_id: str = "neutral", model: str = "yourtts"):
    """
    Generate speech from text.
    
    Returns audio file or base64-encoded MP3.
    """
    # Placeholder - will be implemented in tts_engine.py
    raise HTTPException(status_code=501, detail="TTS engine not yet implemented")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
