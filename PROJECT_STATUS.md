# Project Status

## Completed ✅

- [x] Project structure created
- [x] Voxtral-4B-TTS-2603 analysis (size, quantization potential)
- [x] Alternative lightweight TTS models researched
- [x] Architecture design (iOS + Python backend)
- [x] iOS skeleton app (SwiftUI)
- [x] macOS skeleton app (AppKit)
- [x] Python backend stub (FastAPI + ONNX Runtime)

## Next Steps 📋

1. **Model Selection**: Choose between:
   - YourTTS (15MB, ultra-fast)
   - Microsoft Speech T5 (300MB, good quality)
   - Voxtral-4B-TTS-2603 (1.5GB, high quality but large)

2. **Implement TTS Engine**:
   - Download ONNX model
   - Create `tts_engine.py`
   - Implement streaming/latency optimization

3. **Test with Sample Text**:
   - Run local inference
   - Verify latency (< 300ms target)

4. **Integrate with iOS/macOS**:
   - Implement audio decoding/playback
   - Add offline fallback

## Recommendations

- Start with **YourTTS** for fastest iteration
- Use `onnxruntime` for cross-platform inference
- Consider quantizing to Q4_K_M GGUF if using llama.cpp
