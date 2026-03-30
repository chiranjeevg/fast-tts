from huggingface_hub import hf_hub_download, list_repo_files
import os
from pathlib import Path

MODELS_DIR = Path("/Users/chiranjeev/Developer/hermes/tts-mobile/models")
MODELS_DIR.mkdir(exist_ok=True)

print("=== Finding Working TTS Models for Testing ===\n")

# Try Coqui TTS (popular open-source)
print("1. Checking Coqui TTS VITS...")
try:
    files = list_repo_files("tts_models/en/ljspeech/tacotron2-DDC")
    print(f"   Files: {files[:5]}")
except Exception as e:
    print(f"   Error: {e}")

# Microsoft Speech T5 (try different filename)
print("\n2. Checking Microsoft Speech T5 variants...")
models_to_check = [
    "microsoft/speecht5_tts",
    "microsoft/speecht5_asr",
]

for model in models_to_check:
    try:
        files = list_repo_files(model)
        onnx_files = [f for f in files if '.onnx' in f]
        print(f"   {model}: ONNX={len(onnx_files)}")
    except Exception as e:
        print(f"   Error: {e}")

# Test with basic TTS model for quick validation
print("\n3. Testing minimal TTS model (fast_pitch)...")
try:
    local_path = hf_hub_download(
        repo_id="phymind/FastPitch_opuskt", 
        filename="fast_pitch_opuskt.onnx",
        repo_type="model"
    )
    print(f"   ✓ Downloaded: {local_path}")
except Exception as e:
    print(f"   ⚠️ FastPitch: {e}")

# Try ESPnet TTS
print("\n4. Checking ESPnet TTS models...")
try:
    files = list_repo_files("zenos0819/ESPnet_TTS_en")
    onnx_files = [f for f in files if '.onnx' in str(f)]
    print(f"   ONNX files found: {len(onnx_files)}")
except Exception as e:
    print(f"   Error: {e}")
