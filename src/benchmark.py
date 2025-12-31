"""
Simple Benchmark - Quick Performance Comparison
Original vs AI-Optimized Encoders/Modulators
"""
import time
import numpy as np

from encoders import DigitalEncoder
from encoders_optimized import DigitalEncoderOptimized
from modulators import Modulator
from modulators_optimized import ModulatorOptimized


def measure(func, *args, runs=20):
    """Quick time measurement"""
    start = time.perf_counter()
    for _ in range(runs):
        func(*args)
    return (time.perf_counter() - start) / runs * 1000


def main():
    print("\n" + "="*60)
    print("  QUICK BENCHMARK: Original vs Optimized")
    print("="*60)
    
    # Test data
    bits = "10110010101" * 100  # 1100 bits
    
    # Initialize
    enc_orig = DigitalEncoder()
    enc_opt = DigitalEncoderOptimized()
    mod_orig = Modulator()
    mod_opt = ModulatorOptimized()
    
    print(f"\n  Test: {len(bits)} bits, 20 iterations each\n")
    print(f"  {'Algorithm':<20} {'Original':<12} {'Optimized':<12} {'Speedup':<10}")
    print("  " + "-"*54)
    
    results = []
    
    # Encoder tests
    tests = [
        ("NRZ-L Encoder", enc_orig.encode_nrz_l, enc_opt.encode_nrz_l, bits),
        ("Manchester Encoder", enc_orig.encode_manchester, enc_opt.encode_manchester, bits),
        ("AMI Encoder", enc_orig.encode_bipolar_ami, enc_opt.encode_bipolar_ami, bits),
    ]
    
    for name, orig, opt, data in tests:
        t1 = measure(orig, data)
        t2 = measure(opt, data)
        speedup = t1/t2 if t2 > 0 else 0
        print(f"  {name:<20} {t1:>8.3f}ms   {t2:>8.3f}ms   {speedup:>5.2f}x")
        results.append(speedup)
    
    # Modulator tests
    mod_tests = [
        ("ASK Modulator", mod_orig.modulate_ask, mod_opt.modulate_ask, bits[:100]),
        ("PSK Modulator", mod_orig.modulate_psk, mod_opt.modulate_psk, bits[:100]),
    ]
    
    for name, orig, opt, data in mod_tests:
        t1 = measure(orig, data)
        t2 = measure(opt, data)
        speedup = t1/t2 if t2 > 0 else 0
        print(f"  {name:<20} {t1:>8.3f}ms   {t2:>8.3f}ms   {speedup:>5.2f}x")
        results.append(speedup)
    
    # Summary
    avg = sum(results) / len(results)
    print("\n  " + "-"*54)
    print(f"  {'AVERAGE SPEEDUP':<20} {'':<12} {'':<12} {avg:>5.2f}x")
    print("\n" + "="*60)
    print("  Benchmark Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
