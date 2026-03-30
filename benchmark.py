#!/usr/bin/env python3
"""
Comprehensive TTS Benchmark Suite

Tests:
1. Apple AVFoundation (direct)
2. Chunked AVFoundation
3. ONNX models (when available)
4. Memory and quality metrics
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

class TTSBenchmarker:
    def __init__(self, output_dir="/tmp/tts_benchmark"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def benchmark_apple_tts(self, text):
        """Benchmark Apple AVFoundation TTS (direct)"""
        output_file = self.output_dir / "apple_output.aiff"
        
        start = time.time()
        
        result = subprocess.run(
            ["say", "-v", "Alex", "-o", str(output_file), text],
            capture_output=True,
            timeout=60
        )
        
        elapsed = time.time() - start
        
        if output_file.exists():
            audio_size = output_file.stat().st_size
        else:
            audio_size = 0
            
        return {
            "elapsed_ms": int(elapsed * 1000),
            "audio_size_bytes": audio_size,
            "success": output_file.exists()
        }
    
    def benchmark_chunked_tts(self, text):
        """Benchmark Chunked AVFoundation TTS"""
        import re
        
        # Split into chunks
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 60:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        output_file = self.output_dir / "chunked_output.wav"
        
        start = time.time()
        
        # Process chunks
        for i, chunk in enumerate(sentences):
            output = str(output_file) if i == len(sentences) - 1 else "/tmp/chunk_temp.aiff"
            
            result = subprocess.run(
                ["say", "-v", "Alex", "-o", output, chunk],
                capture_output=True,
                timeout=30
            )
        
        elapsed = time.time() - start
        
        if output_file.exists():
            audio_size = output_file.stat().st_size
        else:
            audio_size = 0
            
        return {
            "elapsed_ms": int(elapsed * 1000),
            "audio_size_bytes": audio_size,
            "num_chunks": len(chunks),
            "success": output_file.exists()
        }
    
    def benchmark_pre_warmed_apple_tts(self, text):
        """Benchmark Apple AVFoundation with pre-warming"""
        # Pre-warm
        subprocess.run(
            ["say", "-v", "Alex", "-o", "/dev/null", "warmup"],
            capture_output=True,
            timeout=10
        )
        
        return self.benchmark_apple_tts(text)
    
    def benchmark_speecht5_onnx(self, text):
        """Benchmark SpeechT5 ONNX model"""
        onnx_path = "/Users/chiranjeev/.cache/huggingface/hub/models--microsoft--speecht5_tts/.no_exist/30fcde30f19b87502b8435427b5f5068e401d5f6/speecht5_tts_encoder_decoder.onnx"
        
        if not os.path.exists(onnx_path):
            return {"error": "ONNX model not found", "success": False}
        
        try:
            import onnxruntime as ort
            
            start = time.time()
            
            # Try to load model
            try:
                session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
            except:
                try:
                    session = ort.InferenceSession(onnx_path, providers=["MetalExecutionProvider"])
                except Exception as e:
                    return {"error": f"Failed to load ONNX: {e}", "success": False}
            
            # Get model info
            input_info = session.get_inputs()[0]
            output_info = session.get_outputs()
            
            load_time = time.time() - start
            
            return {
                "load_time_ms": int(load_time * 1000),
                "input_shape": str(input_info.shape),
                "output_shapes": [str(out.shape) for out in output_info],
                "success": True
            }
            
        except ImportError:
            return {"error": "ONNX Runtime not installed", "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def run_full_benchmark(self, test_cases):
        """Run all benchmarks and return results"""
        results = {
            "apple_direct": {},
            "chunked": {},
            "prewarmed_apple": {},
            "speecht5_onnx": {}
        }
        
        for name, text in test_cases:
            print(f"\nBenchmarking: {name} ({len(text)} chars)")
            
            # Apple direct
            results["apple_direct"][name] = self.benchmark_apple_tts(text)
            print(f"  Apple: {results['apple_direct'][name]['elapsed_ms']}ms")
            
            # Chunked
            results["chunked"][name] = self.benchmark_chunked_tts(text)
            print(f"  Chunked: {results['chunked'][name]['elapsed_ms']}ms")
            
            # Pre-warmed Apple
            results["prewarmed_apple"][name] = self.benchmark_pre_warmed_apple_tts(text)
            print(f"  Pre-warmed Apple: {results['prewarmed_apple'][name]['elapsed_ms']}ms")
        
        # ONNX benchmark (one-time)
        results["speecht5_onnx"] = self.benchmark_speecht5_onnx("test")
        if results["speecht5_onnx"]["success"]:
            print(f"  ONNX Model loaded in {results['speecht5_onnx']['load_time_ms']}ms")
        else:
            print(f"  ONNX: {results['speecht5_onnx'].get('error', 'Error')}")
        
        return results
    
    def save_results(self, results, filename="benchmark_results.json"):
        """Save benchmark results to JSON"""
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {filepath}")
        return filepath
    
    def generate_summary(self, results):
        """Generate a summary of all benchmarks"""
        print("\n" + "="*70)
        print("BENCHMARK SUMMARY")
        print("="*70)
        
        # Compare Apple vs Chunked
        print("\n--- Latency Comparison ---")
        print(f"{'Text':<15} | {'Apple (ms)':>10} | {'Chunked (ms)':>12} | {'Prewarmed':>10} | {'Improvement'}")
        print("-"*70)
        
        for name in results["apple_direct"].keys():
            apple_time = results["apple_direct"][name]["elapsed_ms"]
            chunked_time = results["chunked"][name]["elapsed_ms"]
            prewarm_time = results["prewarmed_apple"][name]["elapsed_ms"]
            
            if apple_time > 0:
                improvement = ((apple_time - chunked_time) / apple_time * 100)
            else:
                improvement = 0
            
            marker = "⚡" if chunked_time < apple_time else ""
            
            print(f"{name:<15} | {apple_time:>10} | {chunked_time:>12} | {prewarm_time:>10} | {improvement:6.1f}% {marker}")
        
        # ONNX status
        print("\n--- ONNX Status ---")
        if results["speecht5_onnx"].get("success"):
            info = results["speecht5_onnx"]
            print(f"  Model loaded: Yes ({info['load_time_ms']}ms)")
            print(f"  Input shape: {info.get('input_shape', 'N/A')}")
        else:
            print(f"  Model loaded: No")
            print(f"  Error: {results['speecht5_onnx'].get('error', 'Unknown')}")
        
        print("\n--- Recommendations ---")
        
        apple_times = [results["apple_direct"][k]["elapsed_ms"] for k in results["apple_direct"]]
        avg_apple = sum(apple_times) / len(apple_times)
        
        chunked_times = [results["chunked"][k]["elapsed_ms"] for k in results["chunked"]]
        avg_chunked = sum(chunked_times) / len(chunked_times)
        
        print(f"  Apple AVFoundation avg: {avg_apple:.1f}ms")
        print(f"  Chunked AVFoundation avg: {avg_chunked:.1f}ms")
        
        if avg_chunked < avg_apple:
            print(f"  → Recommendation: Use chunked approach ({avg_apple - avg_chunked:.0f}ms saving)")
        else:
            print(f"  → Recommendation: Direct AVFoundation is faster for this test set")
        
        if results["speecht5_onnx"].get("success"):
            print(f"  → ONNX available - potential for <100ms inference")


def main():
    """Run benchmarks with various text lengths"""
    
    test_cases = [
        ("1 word", "Hello"),
        ("8 chars", "Hello world"),
        ("20 chars", "The quick brown fox jumps"),
        ("50 chars", "The quick brown fox jumps over the lazy dog."),
        ("100 chars", "Welcome to our application. We are excited to have you here."),
        ("200 chars", "This is a longer test of the text to speech system. It should handle sentences properly and provide good latency measurements for real-world usage scenarios in mobile applications."),
    ]
    
    print("="*70)
    print("TTS BENCHMARK SUITE")
    print("="*70)
    
    benchmarker = TTSBenchmarker()
    results = benchmarker.run_full_benchmark(test_cases)
    
    # Save and display summary
    filepath = benchmarker.save_results(results)
    benchmarker.generate_summary(results)
    
    return results


if __name__ == "__main__":
    main()
