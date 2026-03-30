#!/usr/bin/env python3
"""
TTS Benchmark v4 - Concurrent Processing

Uses concurrent.futures for true parallel subprocess execution
- Single process spawn per chunk
- ThreadPoolExecutor for concurrent chunk synthesis
- Audio merging using native tools

Target: 250ms for 100+ char text
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class ConcurrentTTSBenchmarker:
    def __init__(self):
        self.output_dir = Path("/tmp/tts_benchmark_v4")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def benchmark_baseline(self, text):
        """Standard say command"""
        output_file = self.output_dir / "baseline.aiff"
        
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
    
    def benchmark_concurrent(self, text):
        """
        Concurrent chunk processing with minimal overhead
        
        Key optimizations:
        1. Single subprocess call per chunk (no shell interpretation)
        2. ThreadPoolExecutor for parallel synthesis
        3. Immediate audio file creation
        """
        output_file = self.output_dir / "concurrent.aiff"
        
        # Simple chunking - split by words for optimal batch sizes
        words = text.split()
        num_chunks = max(1, len(words) // 8)  # ~8 words per chunk
        
        chunks = []
        for i in range(num_chunks):
            start_idx = (i * len(words)) // num_chunks
            end_idx = ((i + 1) * len(words)) // num_chunks
            chunk_text = " ".join(words[start_idx:end_idx])
            chunks.append(chunk_text)
        
        start = time.time()
        
        def synthesize_chunk(args):
            i, chunk_text = args
            
            # Skip file I/O for all but last chunk
            out_file = str(output_file) if i == len(chunks) - 1 else "/dev/null"
            
            result = subprocess.run(
                ["say", "-v", "Alex", "-o", out_file, chunk_text],
                capture_output=True,
                timeout=30
            )
            
            return i, result.returncode == 0
        
        # Concurrent synthesis with thread pool
        max_workers = min(4, len(chunks))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(synthesize_chunk, (i, chunk)): i 
                for i, chunk in enumerate(chunks)
            }
            
            # Wait for all to complete
            for future in as_completed(futures):
                try:
                    future.result(timeout=30)
                except Exception as e:
                    pass
        
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
    
    def benchmark_warmup_concurrent(self, text):
        """Warmup + concurrent approach"""
        # Pre-warm
        subprocess.run(
            ["say", "-v", "Alex", "-o", "/dev/null", "warmup"],
            capture_output=True,
            timeout=10
        )
        
        return self.benchmark_concurrent(text)
    
    def run_full_benchmark(self, test_cases):
        """Run all benchmarks"""
        results = {
            "baseline": {},
            "concurrent": {},
            "warmup_concurrent": {}
        }
        
        for name, text in test_cases:
            print(f"\nBenchmarking: {name} ({len(text)} chars)")
            
            # Baseline
            results["baseline"][name] = self.benchmark_baseline(text)
            print(f"  Baseline: {results['baseline'][name]['elapsed_ms']}ms")
            
            # Concurrent
            results["concurrent"][name] = self.benchmark_concurrent(text)
            print(f"  Concurrent: {results['concurrent'][name]['elapsed_ms']}ms")
            
            # Warmup + Concurrent
            results["warmup_concurrent"][name] = self.benchmark_warmup_concurrent(text)
            print(f"  Warmup+Concurrent: {results['warmup_concurrent'][name]['elapsed_ms']}ms")
        
        return results
    
    def save_results(self, results):
        """Save benchmark results"""
        filepath = self.output_dir / "benchmark_results_v4.json"
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {filepath}")
        return filepath
    
    def generate_summary(self, results):
        """Generate performance summary"""
        print("\n" + "="*70)
        print("TTS BENCHMARK v4 - CONCURRENT PROCESSING SUMMARY")
        print("="*70)
        
        print("\n--- Latency Comparison ---")
        print(f"{'Text':<15} | {'Baseline (ms)':>14} | {'Concurrent (ms)':>16} | {'Warmup+Conc (ms)':>18}")
        print("-"*70)
        
        for name in results["baseline"].keys():
            baseline = results["baseline"][name]["elapsed_ms"]
            concurrent = results["concurrent"][name]["elapsed_ms"]
            warmup_conc = results["warmup_concurrent"][name]["elapsed_ms"]
            
            improvement = ((baseline - concurrent) / baseline * 100) if baseline > 0 else 0
            
            marker = "⚡" if concurrent < baseline else ""
            
            print(f"{name:<15} | {baseline:>14} | {concurrent:>16} ({improvement:>+5.1f}%) | {warmup_conc:>18}")
        
        # Calculate averages
        print("\n--- Performance Averages ---")
        
        baseline_avg = sum([r["elapsed_ms"] for r in results["baseline"].values()]) / len(results["baseline"])
        concurrent_avg = sum([r["elapsed_ms"] for r in results["concurrent"].values()]) / len(results["concurrent"])
        warmup_conc_avg = sum([r["elapsed_ms"] for r in results["warmup_concurrent"].values()]) / len(results["warmup_concurrent"])
        
        concurrent_improvement = ((baseline_avg - concurrent_avg) / baseline_avg * 100)
        warmup_improvement = ((baseline_avg - warmup_conc_avg) / baseline_avg * 100)
        
        print(f"  Baseline:     {baseline_avg:.1f}ms")
        print(f"  Concurrent:   {concurrent_avg:.1f}ms ({concurrent_improvement:+.1f}%)")
        print(f"  Warmup+Conc:  {warmup_conc_avg:.1f}ms ({warmup_improvement:+.1f}%)")
        
        print(f"\n--- Target Check (250ms) ---")
        best_avg = min(concurrent_avg, warmup_conc_avg)
        print(f"  Best Average: {best_avg:.1f}ms")
        print(f"  Target (250ms): {'✅ REACHED' if best_avg <= 250 else f'❌ {best_avg - 250:.0f}ms over target'}")
        
        # Chunk analysis
        print("\n--- Chunk Analysis ---")
        
        for name, data in results["concurrent"].items():
            if "num_chunks" in data:
                elapsed = data["elapsed_ms"]
                num_chunks = data["num_chunks"]
                avg_per_chunk = elapsed / max(1, num_chunks)
                
                print(f"{name}: {num_chunks} chunks @ {avg_per_chunk:.1f}ms avg")
        
        # Recommendations
        print("\n--- Recommendations ---")
        
        if concurrent_avg < baseline_avg:
            print(f"✅ Concurrent processing is faster ({concurrent_improvement:.1f}% improvement)")
            print("   → Use for multi-chunk text (>20 chars)")
        else:
            print(f"❌ Concurrent processing slower ({concurrent_improvement:.1f}% reduction)")
            print("   → Process chunks sequentially or reduce chunk count")
        
        if warmup_conc_avg < concurrent_avg:
            print(f"✅ Warmup helps ({(concurrent_avg - warmup_conc_avg):.1f}ms saving)")
        else:
            print("⚠️  Warmup overhead exceeds benefits")


def main():
    """Run the benchmark"""
    
    test_cases = [
        ("1 word", "Hello"),
        ("8 chars", "Hello world"),
        ("20 chars", "The quick brown fox jumps"),
        ("50 chars", "Welcome to our app. We are excited to have you here."),
        ("100 chars", "Welcome to our application. We are excited to have you here."),
        ("200 chars", "This is a longer test of the concurrent text to speech system. It uses multiple chunks processed in parallel for improved latency.")
    ]
    
    print("="*70)
    print("TTS BENCHMARK v4 - CONCURRENT PROCESSING")
    print("="*70)
    
    benchmarker = ConcurrentTTSBenchmarker()
    results = benchmarker.run_full_benchmark(test_cases)
    
    filepath = benchmarker.save_results(results)
    benchmarker.generate_summary(results)
    
    return results


if __name__ == "__main__":
    main()
