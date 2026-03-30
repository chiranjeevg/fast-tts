"""
Benchmark utilities for Fast-TTS.
"""

from .core import OptimizedTTSSystem


def run_benchmark():
    """Run predefined benchmarks."""
    
    # Realistic WhatsApp command group test cases
    test_cases = [
        ("Short command", "Hello"),
        ("Welcome message", "Welcome to our service! Thank you for joining us."),
        ("Question response", "How can I help you today?"),
        ("Order confirmation", "Your order has been confirmed and will arrive within 24 hours."),
        ("Long notification", "Important update: Your request has been processed. The new status is 'active' and will remain so for 7 days."),
    ]
    
    print("=" * 75)
    print("OPTIMIZED TTS SYSTEM BENCHMARK")
    print("=" * 75)
    
    system = OptimizedTTSSystem()
    results = system.run_benchmark(test_cases)
    system.generate_summary(results)


if __name__ == "__main__":
    run_benchmark()
