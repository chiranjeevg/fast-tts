# Project Progress: Low-Latency TTS App

## Completed ✅

- [x] Project structure (iOS + macOS + Rust backend)
- [x] Rust Cargo.toml with ort + tract dependencies
- [x] Rust inference modules (yourtts.rs, voxtral.rs)
- [x] Swift SwiftUI app skeleton
- [x] Build script for cross-platform compilation

## Next Steps 📋

### Phase 1: Model Download & Conversion
```bash
# Install Python dependencies
pip install onnxruntime-coreml coremltools

# Convert YourTTS ONNX to CoreML
huggingface-cli download myshell-ai/OpenVoiceV2 --include "*.onnx" --local-dir models/
```

### Phase 2: Rust Backend Implementation
1. Implement YourTTS inference using ONNX Runtime
2. Implement Voxtral inference using llama.cpp or ort with GGUF support

### Phase 3: Swift Integration
1. Create Objective-C bridge (TTSBridge.h/c)
2. Link Rust library to Swift app
3. Test audio playback

### Phase 4: Benchmarking
- Compare YourTTS vs Voxtral latency
- Measure memory usage on device

## Architecture Summary

```
Swift UI → Rust (FFI) → ONNX Runtime / llama.cpp → Audio Output
```

### Model Options

| Model | Size (Quantized) | Latency (iPhone) |
|-------|-----------------|------------------|
| YourTTS | ~15MB | ~40ms |
| Voxtral Q4_K_M | ~1.5GB | ~200ms |
