"""
Command-line interface for Fast-TTS.
"""

import sys
import argparse
from pathlib import Path

from .core import OptimizedTTSSystem


def synthesize_from_file():
    """Synthesize text from a file."""
    parser = argparse.ArgumentParser(description="Fast-TTS CLI")
    parser.add_argument("file", nargs="?", help="File to read from (stdin if omitted)")
    parser.add_argument("-o", "--output", help="Output audio path")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    tts = OptimizedTTSSystem()
    
    if args.file:
        text = Path(args.file).read_text()
    else:
        text = sys.stdin.read().strip()
    
    result = tts.synthesize_with_cache(text)
    
    if args.verbose:
        print(f"Elapsed: {result['elapsed_ms']}ms")
        print(f"Cached: {result['cached']}")
        print(f"Chunks: {result.get('num_chunks', 1)}")
    
    if args.output:
        if result["success"] and result.get("audio_path"):
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(result["audio_path"]).rename(args.output)
    
    return 0 if result["success"] else 1


def clear_cache():
    """Clear the cache."""
    parser = argparse.ArgumentParser(description="Fast-TTS Cache Manager")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation")
    
    args = parser.parse_args()
    
    cache_dir = Path("~/.fast_tts/cache").expanduser()
    
    if not args.yes:
        response = input(f"Clear cache at {cache_dir}? [y/N]: ")
        if response.lower() != "y":
            print("Cancelled.")
            return 0
    
    if cache_dir.exists():
        for f in cache_dir.glob("*.aiff"):
            f.unlink()
        print(f"Cleared {len(list(cache_dir.glob('*.aiff')))} cached files")
    else:
        print("Cache directory does not exist.")
    
    return 0


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Fast-TTS CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Synthesize command
    subparsers.add_parser("synthesize", help="Synthesize text from file or stdin")
    
    # Cache command
    subparsers.add_parser("clear-cache", help="Clear cached audio files")
    
    # Benchmark command
    subparsers.add_parser("benchmark", help="Run performance benchmarks")
    
    args = parser.parse_args()
    
    if args.command == "synthesize":
        sys.exit(synthesize_from_file())
    elif args.command == "clear-cache":
        sys.exit(clear_cache())
    elif args.command == "benchmark":
        from .benchmark import run_benchmark
        run_benchmark()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
