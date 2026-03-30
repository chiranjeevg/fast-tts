"""
Fast-TTS: High-Performance Text-to-Speech Engine

A macOS AVFoundation-based TTS engine with intelligent caching,
parallel chunking, and benchmark-validated performance.
"""

from .core import OptimizedTTSSystem

__version__ = "1.0.0"
__all__ = ["OptimizedTTSSystem"]
