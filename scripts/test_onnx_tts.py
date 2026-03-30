#!/usr/bin/env python3
"""
Test ONNX TTS models for latency and quality.
"""

import time

print("=== Testing Available ONNX TTS Models ===")

# Try different model sources
models = [
    "microsoft/speecht5_tts",
    "facebook/mms-tts", 
    "IlyaGusev/glow_tts_ru",
]

import huggingface_hub as hf

for model_id in models:
    print(f"\n--- Testing: {model_id} ---")
    try:
        files = hf.list_repo_files(model_id)
        onnx_files = [f for f in files if '.onnx' in f]
        print(f"  ONNX files: {len(onnx_files)}")
        
        # Try to download first ONNX file if available
        if onnx_files:
            print(f"  Available: {onnx_files[:3]}")
            
            # Test download
            try:
                local_path = hf.hf_hub_download(model_id, onnx_files[0], repo_type="model")
                print(f"  ✓ Downloaded: {local_path}")
            except Exception as e:
                print(f"  ⚠️ Download failed: {str(e)[:100]}")
    except Exception as e:
        print(f"  Error: {str(e)[:100]}")

print("\n=== Conclusion ===")
print("For low-latency TTS, we should:")
print("1. Use Apple's AVSpeechSynthesizer (built-in, instant startup)")
print("2. Or use ONNX Runtime with pre-converted models")
print("3. Or implement voice conversion on top of existing audio")
