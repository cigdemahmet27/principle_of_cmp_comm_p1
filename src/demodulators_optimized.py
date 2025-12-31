"""
Optimized Demodulators - AI-Optimized Version
Uses NumPy vectorization and batch processing for better performance.
Compare with demodulators.py (original non-optimized version).
"""
import numpy as np


class DemodulatorOptimized:
    """
    Optimized demodulator class using NumPy vectorization.
    Key optimizations:
    - Batch processing with reshape
    - Pre-computed reference carriers
    - Vectorized correlation
    """
    
    def __init__(self, Fs=1000, Fc=5, Amp=1):
        self.Fs = Fs
        self.Fc = Fc
        self.Amp = Amp

    def demodulate_ask(self, signal, T=1):
        """ASK Demodulator - Batch Processing Version"""
        signal = np.asarray(signal)
        samples_per_bit = int(self.Fs * T)
        num_bits = len(signal) // samples_per_bit
        
        # Reshape for batch processing
        signal_reshaped = signal[:num_bits * samples_per_bit].reshape(num_bits, samples_per_bit)
        
        # Calculate energy for each bit
        energies = np.sum(np.abs(signal_reshaped), axis=1)
        
        # Reference threshold
        t_bit = np.arange(samples_per_bit) / self.Fs
        ref_energy = np.sum(np.abs(self.Amp * np.sin(2 * np.pi * self.Fc * t_bit))) / 2
        
        bits = np.where(energies > ref_energy, '1', '0')
        return ''.join(bits)

    def demodulate_psk(self, signal, T=1):
        """PSK Demodulator - Batch Processing Version"""
        signal = np.asarray(signal)
        samples_per_bit = int(self.Fs * T)
        num_bits = len(signal) // samples_per_bit
        
        # Reference carrier
        t_bit = np.arange(samples_per_bit) / self.Fs
        ref_wave = self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)
        
        # Reshape and correlate in batch
        signal_reshaped = signal[:num_bits * samples_per_bit].reshape(num_bits, samples_per_bit)
        correlations = np.sum(signal_reshaped * ref_wave, axis=1)
        
        bits = np.where(correlations > 0, '1', '0')
        return ''.join(bits)

    def demodulate_bfsk(self, signal, T=1, f_dev=2):
        """BFSK Demodulator - Batch Processing Version"""
        signal = np.asarray(signal)
        samples_per_bit = int(self.Fs * T)
        num_bits = len(signal) // samples_per_bit
        
        t_bit = np.arange(samples_per_bit) / self.Fs
        f1 = self.Fc + f_dev
        f2 = self.Fc - f_dev
        
        ref_wave_1 = np.sin(2 * np.pi * f1 * t_bit)
        ref_wave_0 = np.sin(2 * np.pi * f2 * t_bit)
        
        # Batch correlation
        signal_reshaped = signal[:num_bits * samples_per_bit].reshape(num_bits, samples_per_bit)
        corr_1 = np.abs(np.sum(signal_reshaped * ref_wave_1, axis=1))
        corr_0 = np.abs(np.sum(signal_reshaped * ref_wave_0, axis=1))
        
        bits = np.where(corr_1 > corr_0, '1', '0')
        return ''.join(bits)

    def demodulate_qam(self, signal, T=1):
        """4-QAM Demodulator - Optimized Version"""
        signal = np.asarray(signal)
        samples_per_symbol = int(self.Fs * 2 * T)
        num_symbols = len(signal) // samples_per_symbol
        
        t_symbol = np.arange(samples_per_symbol) / self.Fs
        ref_cos = np.cos(2 * np.pi * self.Fc * t_symbol)
        ref_sin = np.sin(2 * np.pi * self.Fc * t_symbol)
        
        # Batch processing
        signal_reshaped = signal[:num_symbols * samples_per_symbol].reshape(num_symbols, samples_per_symbol)
        i_corr = np.sum(signal_reshaped * ref_cos, axis=1)
        q_corr = np.sum(signal_reshaped * ref_sin, axis=1)
        
        # Decode I and Q bits
        i_bits = np.where(i_corr > 0, '1', '0')
        q_bits = np.where(q_corr < 0, '1', '0')
        
        # Interleave I and Q bits
        result = ''.join([i + q for i, q in zip(i_bits, q_bits)])
        return result

    def demodulate_am(self, signal):
        """AM Demodulator - Fully Vectorized"""
        signal = np.asarray(signal)
        envelope = np.abs(signal)
        return envelope - envelope.mean()
