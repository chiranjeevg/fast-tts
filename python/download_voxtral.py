#!/usr/bin/env python3
"""
Download and quantize Voxtral-4B-TTS to GGUF format

Usage:
    python download_voxtral.py [--output voxtral-q4_k_m.gguf]

Dependencies:
    pip install huggingface_hub
"""

import sys
import argparse
from pathlib import Path
from huggingface_hub import hf_hub_download

def download_and_quantize_voxtral(output_path: str = None):
    """
    Download Voxtral safetensors and quantize to GGUF Q4_K_M
    
    Args:
        output_path: Output GGUF path (default: /tmp/voxtral-q4_k_m.gguf)
    """
    if output_path is None:
        import tempfile
        output_path = str(tempfile.mktemp(suffix="-q4_k_m.gguf"))
    
    model_id = "mistralai/Voxtral-4B-TTS-2603"
    output_path = Path(output_path)
    
    print(f"Downloading {model_id}...")
    
    # Step 1: Download safetensors
    print("  - consolidated.safetensors")
    safetensors_path = hf_hub_download(
        repo_id=model_id,
        filename="consolidated.safetensors",
        local_dir="/tmp"
    )
    
    # Step 2: Download params.json
    print("  - params.json")
    params_path = hf_hub_download(
        repo_id=model_id,
        filename="params.json",
        local_dir="/tmp"
    )
    
    # Step 3: Download tekken.json
    print("  - tekken.json")
    tekken_path = hf_hub_download(
        repo_id=model_id,
        filename="tekken.json",
        local_dir="/tmp"
    )
    
    print(f"\n✅ Downloaded files:")
    print(f"  - {safetensors_path}")
    print(f"  - {params_path}")
    print(f"  - {tekken_path}")
    
    # Step 4: Quantize (requires llama.cpp)
    print("\n📝 Next steps:")
    print(f"  1. Clone llama.cpp: git clone https://github.com/ggml-org/llama.cpp")
    print(f"  2. Build quantize_tool:")
    print(f"     cd llama.cpp && make quantize")
    print(f"  3. Quantize model:")
    print(f"     ./quantize {safetensors_path} {output_path} Q4_K_M")
    
    print(f"\n🚀 Quantized model will be: {output_path}")
    
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and quantize Voxtral to GGUF")
    parser.add_argument("--output", "-o", default=None, help="Output GGUF path")
    args = parser.parse_args()
    
    try:
        output = download_and_quantize_voxtral(args.output)
        print(f"\nDownload complete!")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
