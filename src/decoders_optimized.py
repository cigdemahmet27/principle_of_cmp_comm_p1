"""
Optimized Decoders - AI-Optimized Version
Uses NumPy vectorization for better performance.
Compare with decoders.py (original non-optimized version).
"""
import numpy as np


class DigitalDecoderOptimized:
    """
    Optimized decoder class using NumPy vectorization.
    """
    
    def __init__(self):
        pass

    # ==========================================
    #  DIGITAL TO ANALOG (Source Decoding)
    # ==========================================

    def decode_pcm(self, bits, bit_depth=3):
        """PCM Decoder - Vectorized Version"""
        if not bits:
            return []
        
        num_levels = 2 ** bit_depth
        num_samples = len(bits) // bit_depth
        
        # Vectorized conversion
        levels = np.array([
            int(bits[i:i + bit_depth], 2) 
            for i in range(0, num_samples * bit_depth, bit_depth)
        ])
        
        voltages = levels / (num_levels - 1)
        return voltages.tolist()

    def decode_delta_modulation(self, bits, step_size=0.1):
        """Delta Modulation Decoder - Vectorized"""
        if not bits:
            return []
        
        # Convert bits to steps: '1' -> +step, '0' -> -step
        steps = np.array([step_size if b == '1' else -step_size for b in bits])
        
        # Cumulative sum gives the reconstructed signal
        return np.cumsum(steps).tolist()

    # ==========================================
    #  DIGITAL TO DIGITAL (Line Decoding)
    # ==========================================

    def decode_nrz_l(self, signal):
        """NRZ-L Decoder - Vectorized"""
        signal = np.asarray(signal)
        samples = signal[::2]
        bits = np.where(samples > 0, '0', '1')
        return ''.join(bits)

    def decode_nrzi(self, signal):
        """NRZI Decoder - Vectorized"""
        signal = np.asarray(signal)
        samples = signal[::2]
        
        # Detect transitions
        prev_samples = np.concatenate([[1], samples[:-1]])
        transitions = samples != prev_samples
        
        bits = np.where(transitions, '1', '0')
        return ''.join(bits)

    def decode_bipolar_ami(self, signal):
        """AMI Decoder - Vectorized"""
        signal = np.asarray(signal)
        samples = signal[::2]
        bits = np.where(samples == 0, '0', '1')
        return ''.join(bits)

    def decode_pseudoternary(self, signal):
        """Pseudoternary Decoder - Vectorized"""
        signal = np.asarray(signal)
        samples = signal[::2]
        bits = np.where(samples == 0, '1', '0')
        return ''.join(bits)

    def decode_manchester(self, signal):
        """Manchester Decoder - Vectorized"""
        signal = np.asarray(signal)
        first_halves = signal[::2]
        bits = np.where(first_halves == 1, '0', '1')
        return ''.join(bits)

    def decode_diff_manchester(self, signal):
        """Differential Manchester Decoder - Optimized"""
        signal = np.asarray(signal)
        n_bits = len(signal) // 2
        bits = np.empty(n_bits, dtype='U1')
        
        prev_end_level = -1
        for i in range(n_bits):
            current_start = signal[2*i]
            current_end = signal[2*i + 1]
            
            bits[i] = '0' if current_start != prev_end_level else '1'
            prev_end_level = current_end
        
        return ''.join(bits)
