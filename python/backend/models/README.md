# TTS Model Storage

This directory contains quantized models for local inference.

## Download Models

### YourTTS (ONNX - Recommended)
```bash
huggingface-cli download myshell-ai/OpenVoiceV2 --include "yourtts.onnx" --local-dir models/
```

### Voxtral-4B-TTS-2603 (GGUF - For Mac)
```bash
huggingface-cli download mistralai/Voxtral-4B-TTS-2603 --include "*.gguf" --local-dir models/
```

## Size Target

- iOS: < 100MB total (including model)
- Mac: < 500MB acceptable
