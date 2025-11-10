"""
Benchmark script for MockDataGenerator performance.

Measures data generation speed to ensure it meets 10 FPS (100ms) requirement.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-10
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.mock_data_generator import MockDataGenerator


def benchmark_generator(iterations: int = 1000) -> dict:
    """
    Benchmark MockDataGenerator performance.

    Args:
        iterations: Number of iterations to run

    Returns:
        Dictionary with benchmark results
    """
    gen = MockDataGenerator()

    # Warm up
    for _ in range(10):
        gen.get_system_metrics()
        gen.get_wifi_info()
        gen.get_network_stats()
        gen.get_devices()
        gen.get_top_apps()

    # Benchmark individual methods
    results = {}

    # System metrics
    start = time.perf_counter()
    for _ in range(iterations):
        gen.get_system_metrics()
    end = time.perf_counter()
    results["system_metrics_ms"] = (end - start) / iterations * 1000

    # WiFi info
    start = time.perf_counter()
    for _ in range(iterations):
        gen.get_wifi_info()
    end = time.perf_counter()
    results["wifi_info_ms"] = (end - start) / iterations * 1000

    # Network stats
    start = time.perf_counter()
    for _ in range(iterations):
        gen.get_network_stats()
    end = time.perf_counter()
    results["network_stats_ms"] = (end - start) / iterations * 1000

    # Devices
    start = time.perf_counter()
    for _ in range(iterations):
        gen.get_devices()
    end = time.perf_counter()
    results["devices_ms"] = (end - start) / iterations * 1000

    # Top apps
    start = time.perf_counter()
    for _ in range(iterations):
        gen.get_top_apps()
    end = time.perf_counter()
    results["top_apps_ms"] = (end - start) / iterations * 1000

    # Full frame (all methods)
    start = time.perf_counter()
    for _ in range(iterations):
        gen.get_system_metrics()
        gen.get_wifi_info()
        gen.get_network_stats()
        gen.get_devices()
        gen.get_top_apps()
    end = time.perf_counter()
    results["full_frame_ms"] = (end - start) / iterations * 1000

    return results


def main():
    """Run benchmark and display results."""
    print("="*60)
    print("MockDataGenerator Performance Benchmark")
    print("="*60)
    print()

    print("Running benchmark (1000 iterations)...")
    results = benchmark_generator(1000)

    print()
    print("Results (average per call):")
    print("-"*60)

    for method, time_ms in results.items():
        name = method.replace("_ms", "").replace("_", " ").title()
        status = "✅" if time_ms < 10 else "⚠️"
        print(f"  {status} {name:20s}: {time_ms:8.4f} ms")

    print()
    print("Performance Analysis:")
    print("-"*60)

    full_frame = results["full_frame_ms"]
    target_frame_time = 100  # 10 FPS = 100ms per frame
    fps = 1000 / full_frame if full_frame > 0 else float('inf')

    print(f"  Full frame time:     {full_frame:.4f} ms")
    print(f"  Target frame time:   {target_frame_time:.2f} ms (10 FPS)")
    print(f"  Actual FPS:          {fps:.1f} FPS")
    print(f"  Performance margin:  {target_frame_time - full_frame:.2f} ms")

    if full_frame < target_frame_time:
        overhead_pct = (full_frame / target_frame_time) * 100
        print(f"  Frame budget used:   {overhead_pct:.2f}%")
        print()
        print(f"✅ PASS: Meets 10 FPS requirement!")
    else:
        print()
        print(f"❌ FAIL: Too slow for 10 FPS!")

    print("="*60)


if __name__ == "__main__":
    main()
