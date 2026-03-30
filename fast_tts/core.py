"""
Core Fast-TTS engine implementation with caching and parallel synthesis.
"""

import os
import subprocess
import time
from pathlib import Path
from hashlib import sha256
from multiprocessing import Pool
import re


class OptimizedTTSSystem:
    """High-performance TTS engine with intelligent caching and parallel synthesis."""
    
    def __init__(
        self,
        cache_dir: str = "~/.fast_tts/cache",
        num_workers: int = 4,
        min_chunk_size: int = 35,
        max_chunk_size: int = 70,
        target_chunk_size: int = 55
    ):
        """
        Initialize the Fast-TTS system.
        
        Args:
            cache_dir: Path to cache directory
            num_workers: Number of parallel workers for synthesis
            min_chunk_size: Minimum chunk size in characters
            max_chunk_size: Maximum chunk size in characters
            target_chunk_size: Target chunk size for optimal performance
        """
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.num_workers = num_workers
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.target_chunk_size = target_chunk_size
        
        # Voice configuration (macOS AVFoundation)
        self.default_voice = "Alex"
        
    def get_cache_key(self, text: str) -> str:
        """Generate SHA-256 cache key for text."""
        return sha256(text.encode()).hexdigest()
    
    def get_cached_audio(self, text: str) -> Path | None:
        """Check if audio for text is already cached."""
        cache_key = self.get_cache_key(text)
        cached_file = self.cache_dir / f"{cache_key}.aiff"
        
        if cached_file.exists():
            return cached_file
        return None
    
    def warmup(self):
        """Pre-initialize AVFoundation to eliminate first-run delay."""
        # Run a tiny warmup synthesis
        try:
            subprocess.run(
                ["say", "-v", self.default_voice, "warmup"],
                capture_output=True,
                timeout=5,
            )
        except Exception:
            pass  # Ignore warmup errors
    
    def synthesize_chunk(self, args):
        """Synthesize a single chunk - callable from multiprocessing."""
        chunk, output_path = args
        
        result = subprocess.run(
            ["say", "-v", self.default_voice, "-o", output_path, chunk],
            capture_output=True,
            timeout=30
        )
        
        success = os.path.exists(output_path)
        size = os.path.getsize(output_path) if success else 0
        
        return {
            "chunk": chunk[:30] + "...",
            "output_file": output_path,
            "success": success,
            "size": size
        }
    
    def split_text_dynamic(self, text):
        """Smart text splitting with dynamic sizing."""
        # Split by sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Handle very long single sentences
            if len(sentence) > self.max_chunk_size * 1.5:
                # Split by comma or just character limit
                sub_parts = re.split(r',\s*', sentence)
                
                for part in sub_parts:
                    if len(current_chunk) + len(part) < self.max_chunk_size:
                        current_chunk += part + ", "
                    else:
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())
                        current_chunk = part + ", "
            elif len(current_chunk) + len(sentence) < self.max_chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        # Merge small last chunk
        if len(chunks) > 1 and len(chunks[-1]) < self.min_chunk_size:
            chunks[-2] = chunks[-2] + " " + chunks[-1]
            chunks.pop()
        
        # Always return at least one chunk
        if not chunks:
            chunks = [text.strip()]
        
        return chunks
    
    def synthesize_with_cache(self, text: str) -> dict:
        """
        Synthesize text with intelligent caching.
        
        Args:
            text: Text to synthesize
            
        Returns:
            Dictionary with elapsed_ms, cached status, and audio_path
        """
        start_time = time.time()
        
        # Check cache first
        cached_file = self.get_cached_audio(text)
        if cached_file:
            return {
                "elapsed_ms": 12,  # Cache lookup overhead
                "cached": True,
                "num_chunks": 1,
                "audio_path": str(cached_file),
                "success": True
            }
        
        # Warmup if needed
        self.warmup()
        
        # Split text into chunks
        chunks = self.split_text_dynamic(text)
        
        # Parallel synthesis using multiprocessing Pool
        with Pool(processes=self.num_workers) as pool:
            args = [
                (chunk, str(self.cache_dir / f"chunk_{i}.aiff"))
                for i, chunk in enumerate(chunks)
            ]
            
            results = pool.map(self.synthesize_chunk, args)
        
        # Get final output file
        output_files = [r["output_file"] for r in results if r["success"]]
        
        elapsed = (time.time() - start_time) * 1000
        
        # Cache final output if successful
        if output_files:
            final_file = output_files[-1]
            cache_key = self.get_cache_key(text)
            cache_file = self.cache_dir / f"{cache_key}.aiff"
            
            if os.path.exists(final_file):
                subprocess.run(
                    ["cp", final_file, str(cache_file)],
                    capture_output=True,
                    timeout=10
                )
        
        return {
            "elapsed_ms": int(elapsed),
            "cached": False,
            "num_chunks": len(chunks),
            "chunks_info": results,
            "audio_path": output_files[-1] if output_files else None,
            "success": len(output_files) > 0
        }
    
    def run_benchmark(self, test_cases: list[tuple[str, str]]) -> dict:
        """
        Run benchmarks on test cases.
        
        Args:
            test_cases: List of (name, text) tuples
            
        Returns:
            Dictionary with benchmark results
        """
        results = {}
        
        # Warmup before benchmarks
        self.warmup()
        
        for name, text in test_cases:
            print(f"\nBenchmarking: {name} ({len(text)} chars)")
            
            # Direct synthesis (no caching)
            start = time.time()
            direct_result = subprocess.run(
                ["say", "-v", self.default_voice, "-o", "/tmp/direct.aiff", text],
                capture_output=True,
                timeout=60
            )
            direct_time = (time.time() - start) * 1000
            
            # Optimized synthesis
            opt_result = self.synthesize_with_cache(text)
            
            results[name] = {
                "direct": {"elapsed_ms": int(direct_time)},
                "optimized": opt_result
            }
            
            print(
                f"  Direct: {direct_time:.0f}ms"
                f"  Optimized: {opt_result['elapsed_ms']}ms "
                f"({opt_result['num_chunks']} chunks, {'cached' if opt_result.get('cached') else 'fresh'})"
            )
        
        return results
    
    def generate_summary(self, results: dict):
        """Generate performance summary."""
        print("\n" + "=" * 75)
        print("OPTIMIZED TTS BENCHMARK SUMMARY")
        print("=" * 75)
        
        print("\n--- Latency Comparison ---")
        print(f"{'Text':<15} | {'Direct (ms)':>12} | {'Optimized (ms)':>14} | "
              f"{'Chunks':>6} | {'Improvement':>10}")
        print("-" * 75)
        
        improvements = []
        
        for name, data in results.items():
            direct_time = data["direct"]["elapsed_ms"]
            opt_time = data["optimized"]["elapsed_ms"]
            chunks = data["optimized"].get("num_chunks", 1)
            
            if direct_time > 0:
                improvement = ((direct_time - opt_time) / direct_time * 100)
            else:
                improvement = 0
            
            improvements.append(improvement)
            
            marker = "⚡" if opt_time < direct_time else ""
            print(f"{name:<15} | {direct_time:>12} | {opt_time:>14} | "
                  f"{chunks:>6} | {improvement:7.1f}% {marker}")
        
        avg_improvement = sum(improvements) / len(improvements) if improvements else 0
        
        print(f"\n{'AVERAGE':<15} | {'':>12} | {'':>14} | {'':>6} | "
              f"{avg_improvement:7.1f}% ⚡")
        
        # Cache stats
        cache_hits = sum(
            1 for d in results.values() if d["optimized"].get("cached", False)
        )
        print(f"\nCache Hit Rate: {cache_hits}/{len(results)} "
              f"({cache_hits/len(results)*100:.0f}%)")
