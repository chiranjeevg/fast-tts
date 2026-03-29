# TTS Backend (Python)

## Architecture

```
python/backend/
├── server.py          # FastAPI/uvicorn inference server
├── tts_engine.py      # ONNX model wrapper (YourTTS / Voxtral)
├── requirements.txt
└── models/            # Downloaded quantized models
```

## Design Goals

- **Fast startup** (< 1s)
- **Low memory footprint** (< 500MB RAM)
- **ONNX Runtime** for iOS compatibility (via metal/accelerate)

## Models

| Model | Backend Path |
|-------|--------------|
| YourTTS (default) | `models/yourtts.onnx` |
| Voxtral-4B-TTS-2603 | `models/voxtral-gguf.bin` |

## API

```
POST /tts
{
  "text": "Hello world",
  "speaker_id": "neutral_male",  # optional for voice cloning
  "model": "yourtts"             # or "voxtral"
}

→ audio/base64 or audio/MP3
```
