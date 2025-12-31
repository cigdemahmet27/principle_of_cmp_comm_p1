"""
Optimized Modulators - AI-Optimized Version
Uses NumPy vectorization and pre-computed carriers for better performance.
Compare with modulators.py (original non-optimized version).
"""
import numpy as np


class ModulatorOptimized:
    """
    Optimized modulator class using NumPy vectorization.
    Key optimizations:
    - Pre-computed carrier waves
    - Vectorized signal generation using tile/repeat
    - Reduced array concatenation overhead
    """
    
    def __init__(self, Fs=1000, Fc=5, Amp=1):
        self.Fs = Fs
        self.Fc = Fc
        self.Amp = Amp

    def modulate_ask(self, bits, T=1):
        """
        ASK - Fully Vectorized
        Pre-computes carrier and uses tile+multiply
        """
        samples_per_bit = int(self.Fs * T)
        n_bits = len(bits)
        
        # Pre-compute time vector and carrier for one bit period
        t_bit = np.arange(samples_per_bit) / self.Fs
        carrier = self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)
        
        # Create amplitude array: 1 for '1', 0 for '0'
        amplitudes = np.array([1.0 if b == '1' else 0.0 for b in bits])
        
        # Tile carrier and multiply by repeated amplitudes
        signal = np.tile(carrier, n_bits) * np.repeat(amplitudes, samples_per_bit)
        
        return signal

    def modulate_psk(self, bits, T=1):
        """
        PSK/BPSK - Fully Vectorized
        """
        samples_per_bit = int(self.Fs * T)
        n_bits = len(bits)
        
        t_bit = np.arange(samples_per_bit) / self.Fs
        carrier = self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)
        
        # Phase: +1 for '1', -1 for '0'
        phases = np.array([1.0 if b == '1' else -1.0 for b in bits])
        
        signal = np.tile(carrier, n_bits) * np.repeat(phases, samples_per_bit)
        
        return signal

    def modulate_bfsk(self, bits, T=1, f_dev=2):
        """
        BFSK - Optimized with pre-computed dual carriers
        """
        samples_per_bit = int(self.Fs * T)
        n_bits = len(bits)
        
        f1 = self.Fc + f_dev  # Frequency for '1'
        f2 = self.Fc - f_dev  # Frequency for '0'
        
        t_bit = np.arange(samples_per_bit) / self.Fs
        carrier_1 = self.Amp * np.sin(2 * np.pi * f1 * t_bit)
        carrier_0 = self.Amp * np.sin(2 * np.pi * f2 * t_bit)
        
        # Pre-allocate signal array
        signal = np.empty(n_bits * samples_per_bit)
        
        for i, bit in enumerate(bits):
            start = i * samples_per_bit
            end = start + samples_per_bit
            if bit == '1':
                signal[start:end] = carrier_1
            else:
                signal[start:end] = carrier_0
        
        return signal

    def modulate_qam(self, bits, T=1):
        """
        4-QAM - Optimized with vectorized I/Q calculation
        """
        if len(bits) % 2 != 0:
            bits += '0'  # Pad
        
        n_symbols = len(bits) // 2
        samples_per_symbol = int(self.Fs * 2 * T)
        
        t_symbol = np.arange(samples_per_symbol) / self.Fs
        cos_carrier = self.Amp * np.cos(2 * np.pi * self.Fc * t_symbol)
        sin_carrier = self.Amp * np.sin(2 * np.pi * self.Fc * t_symbol)
        
        # Pre-allocate
        signal = np.empty(n_symbols * samples_per_symbol)
        
        for i in range(n_symbols):
            symbol = bits[2*i : 2*i + 2]
            i_amp = 1 if symbol[0] == '1' else -1
            q_amp = 1 if symbol[1] == '1' else -1
            
            start = i * samples_per_symbol
            end = start + samples_per_symbol
            signal[start:end] = i_amp * cos_carrier - q_amp * sin_carrier
        
        return signal

    def modulate_am(self, analog_data):
        """
        AM - Fully Vectorized
        """
        data = np.asarray(analog_data)
        t = np.arange(len(data)) / self.Fs
        carrier = self.Amp * np.cos(2 * np.pi * self.Fc * t)
        
        return (1 + data) * carrier
