# Build Guide

## Prerequisites

### For Rust Backend
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### For CoreML Conversion
```bash
pip install coremltools numpy
```

## Build Steps

### 1. Download Models
```bash
# YourTTS (ONNX)
python3 python/download_yourtts.py

# Voxtral (GGUF)
python3 python/download_voxtral.py
```

### 2. Convert Models

```bash
# YourTTS to CoreML
python3 python/convert_yourtts.py /tmp/yourtts.onnx

# Voxtral to GGUF (requires llama.cpp)
cd /path/to/llama.cpp
make quantize
./quantize /tmp/consolidated.safetensors /tmp/voxtral-q4_k_m.gguf Q4_K_M
```

### 3. Build Rust Backend

```bash
cd rust
cargo build --release
```

### 4. Build Swift App

Open `swift.xcodeproj` in Xcode and build.

## Run on Device

1. Connect iPhone/Mac
2. Select device in Xcode
3. Click Run

## Benchmarks

| Model | Size | Latency (iPhone 15) | Latency (Mac M2) |
|-------|------|---------------------|------------------|
| YourTTS | 15MB | ~40ms | ~20ms |
| Voxtral (Q4_K_M) | 1.5GB | ~200ms | ~80ms |
