#!/usr/bin/env python3
"""
Convert YourTTS ONNX to CoreML for iOS/macOS

Usage:
    python convert_yourtts.py yourtts.onnx [--output yourtts.mlmodelc]

Dependencies:
    pip install coremltools
"""

import sys
import argparse
import torch
import coremltools as ct

def convert_yourtts_to_coreml(onnx_path: str, output_path: str = None) -> str:
    """
    Convert YourTTS ONNX model to CoreML format.
    
    Args:
        onnx_path: Path to yourtts.onnx
        output_path: Output CoreML path (default: temp directory)
    
    Returns:
        Path to converted model
    """
    if output_path is None:
        import tempfile
        output_path = str(tempfile.mktemp(suffix=".mlmodelc"))
    
    print(f"Converting {onnx_path} to CoreML...")
    
    # Load ONNX model
    try:
        import onnx
        onnx_model = onnx.load(onnx_path)
        print(f"✅ Loaded ONNX model: {onnx_model.graph.input[0].name}")
    except Exception as e:
        raise RuntimeError(f"Failed to load ONNX: {e}")
    
    # Convert to CoreML
    try:
        # Define input shape (text length, phoneme embed dim)
        inputs = [
            ct.TensorType(
                name="text",
                shape=(1, None),  # variable length text
                dtype=np.float32,
            )
        ]
        
        # Convert
        coreml_model = ct.convert(
            onnx_model,
            convert_to="coreml",
            inputs=inputs,
        )
        
        # Save
        coreml_model.save(output_path)
        print(f"✅ Saved CoreML model to: {output_path}")
        
        # Compile for Apple Silicon (optional, faster)
        from coremltools.converters.mil import Builder as mb
        
        return output_path
    except Exception as e:
        raise RuntimeError(f"Conversion failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert YourTTS ONNX to CoreML")
    parser.add_argument("onnx_path", help="Path to yourtts.onnx")
    parser.add_argument("--output", "-o", default=None, help="Output path for CoreML model")
    args = parser.parse_args()
    
    try:
        output = convert_yourtts_to_coreml(args.onnx_path, args.output)
        print(f"\n🚀 Ready to use: {output}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
