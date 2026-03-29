# Lightweight Low-Latency TTS for iOS/macOS

A minimal, local-first Text-to-Speech system optimized for iPhone and Mac.

## Architecture Overview

```
tts-mobile/
├── ios/               # iOS Swift app (Xcode project)
├── macos/             # macOS Swift app
├── python/
│   ├── backend/       # Inference server (llama.cpp / ONNX Runtime)
│   └── frontend/      # Client SDK for iOS/macOS
└── models/            # Downloaded and quantized models
```

## Goals

- **Low latency** (< 300ms end-to-end on device)
- **Small footprint** (< 50MB model size)
- **Offline-first** (no cloud dependency)

## Model Candidates

| Model | Size | Latency | Quantized | iOS Friendly |
|-------|------|---------|-----------|--------------|
| [Voxtral-4B-TTS-2603](https://huggingface.co/mistralai/Voxtral-4B-TTS-2603) | ~2.7GB (FP16) | ? | Yes (GGUF) | ⚠️ Needs testing |
| [Microsoft Speech T5](https://huggingface.co/microsoft/speecht5_tts) | ~300MB | Very Low | Yes (ONNX) | ✅ |
| [VITS (Chinese)](https://huggingface.co/FunAudioLLM/CosyVoice2) | ~1GB | Medium | Yes (GGUF) | ⚠️ |
| [YourTTS](https://huggingface.co/yourtts) | ~15MB | Ultra Low | Yes (ONNX) | ✅✅ |

## Next Steps

1. Analyze Voxtral-4B-TTS-2603
2. Quantize and benchmark latency
3. Compare with alternatives
4. Build iOS/macOS client
