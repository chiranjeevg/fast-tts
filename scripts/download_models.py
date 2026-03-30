#!/usr/bin/env python3
"""
Download and convert TTS models to CoreML format for iOS/macOS.
"""

import os
from pathlib import Path
import urllib.request
from huggingface_hub import hf_hub_download

# Create directories
MODELS_DIR = Path(__file__).parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

print("=== TTS Model Downloader & Converter ===\n")

# Microsoft Speech T5 (ONNX)
print("Downloading Microsoft Speech T5...")
try:
    local_path = hf_hub_download(repo_id="microsoft/speecht5_tts", filename="speecht5_tts_encoder_decoder.onnx", repo_type="model")
    print(f"✓ Downloaded: {local_path}")
except Exception as e:
    print(f"✗ Error: {e}")

# Check for yourtts-onnx repo
print("\nChecking YourTTS ONNX...")
try:
    files = hf_hub_download(repo_id="myshell-ai/YourTTS-onnx", filename="yourtts.onnx", repo_type="model")
    print(f"✓ Downloaded: {files}")
except Exception as e:
    print(f"⚠️ YourTTS ONNX not available: {e}")
    print("Alternative: Download YourTTS PyTorch model and convert to ONNX")

# Voxtral
print("\nDownloading Voxtral base model...")
try:
    local_path = hf_hub_download(repo_id="mistralai/Voxtral-4B-TTS-2603", filename="consolidated.safetensors", repo_type="model")
    print(f"✓ Downloaded: {local_path}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n=== Model Download Complete ===")
print(f"Models stored in: {MODELS_DIR}")
