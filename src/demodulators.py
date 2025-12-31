import numpy as np

# ==========================================
# DEMODULATOR CLASS (The Receiver)
# ==========================================
class Demodulator:
    def __init__(self, Fs=1000, Fc=5, Amp=1):
        self.Fs = Fs
        self.Fc = Fc
        self.Amp = Amp

    def demodulate_ask(self, signal, T=1):
        """ ASK Demodulator: Checks energy levels """
        decoded_bits = ""
        samples_per_bit = int(self.Fs * T)
        
        for i in range(0, len(signal), samples_per_bit):
            chunk = signal[i : i + samples_per_bit]
            if len(chunk) < samples_per_bit: break # Skip incomplete end chunks
            
            # Calculate Energy (Sum of absolute values)
            energy = np.sum(np.abs(chunk))
            
            # Threshold: Half of the expected max energy
            # Expected Max = Sum(Abs(SineWave)) over T
            ref_wave = self.Amp * np.sin(2 * np.pi * self.Fc * np.arange(0, T, 1/self.Fs))
            threshold = np.sum(np.abs(ref_wave)) / 2
            
            if energy > threshold:
                decoded_bits += "1"
            else:
                decoded_bits += "0"
        return decoded_bits

    def demodulate_psk(self, signal, T=1):
        """ PSK Demodulator: Correlates with reference carrier """
        decoded_bits = ""
        samples_per_bit = int(self.Fs * T)
        # Reference wave (Phase 0)
        t_bit = np.arange(0, T, 1/self.Fs)
        ref_wave = self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)

        for i in range(0, len(signal), samples_per_bit):
            chunk = signal[i : i + samples_per_bit]
            if len(chunk) < samples_per_bit: break
            
            # Dot Product (Correlation)
            correlation = np.sum(chunk * ref_wave)
            
            # If correlated positively, it's Phase 0 ('1'). 
            # If negative, it was Phase 180 ('0').
            if correlation > 0:
                decoded_bits += "1"
            else:
                decoded_bits += "0"
        return decoded_bits

    def demodulate_bfsk(self, signal, T=1, f_dev=2):
        """ BFSK Demodulator: Compare correlation with f1 vs f2 """
        decoded_bits = ""
        samples_per_bit = int(self.Fs * T)
        t_bit = np.arange(0, T, 1/self.Fs)
        
        # Two Reference Waves
        f1 = self.Fc + f_dev
        f2 = self.Fc - f_dev
        ref_wave_1 = np.sin(2 * np.pi * f1 * t_bit)
        ref_wave_0 = np.sin(2 * np.pi * f2 * t_bit)

        for i in range(0, len(signal), samples_per_bit):
            chunk = signal[i : i + samples_per_bit]
            if len(chunk) < samples_per_bit: break

            # Check match with both frequencies
            corr_1 = np.abs(np.sum(chunk * ref_wave_1))
            corr_0 = np.abs(np.sum(chunk * ref_wave_0))
            
            if corr_1 > corr_0:
                decoded_bits += "1"
            else:
                decoded_bits += "0"
        return decoded_bits

    def demodulate_qam(self, signal, T=1):
        """ 4-QAM Demodulator: Correlates with I (cos) and Q (sin) components """
        decoded_bits = ""
        # Symbol period is 2T because QAM encodes 2 bits per symbol
        samples_per_symbol = int(self.Fs * 2 * T)
        t_symbol = np.arange(0, 2*T, 1/self.Fs)
        
        # Reference carriers
        ref_cos = np.cos(2 * np.pi * self.Fc * t_symbol)
        ref_sin = np.sin(2 * np.pi * self.Fc * t_symbol)
        
        for i in range(0, len(signal), samples_per_symbol):
            chunk = signal[i : i + samples_per_symbol]
            if len(chunk) < samples_per_symbol:
                break
            
            # Correlate with I (cosine) and Q (sine) components
            i_corr = np.sum(chunk * ref_cos)
            q_corr = np.sum(chunk * ref_sin)
            
            # Decode I bit: positive correlation -> '1', negative -> '0'
            decoded_bits += "1" if i_corr > 0 else "0"
            # Decode Q bit: negative correlation -> '1' (due to -Q*sin in modulator)
            decoded_bits += "1" if q_corr < 0 else "0"
        
        return decoded_bits
    
    def demodulate_am(self, signal):
        """ AM Demodulator: Simple Envelope Detector """
        # In simulation, we can just take Absolute value + Smoothing (Mean)
        # But to return the original signal, we typically use the envelope.
        # For simplicity in this HW:
        envelope = np.abs(signal)
        # Ideally we subtract the DC offset (The '1' in [1+m(t)])
        demodulated = envelope - np.mean(envelope)
        return demodulated

    def demodulate_fm(self, signal):
        """
        FM Demodulator: Frequency Discriminator
        Uses differentiation to extract instantaneous frequency changes.
        """
        # Compute the analytic signal using Hilbert transform
        # For simplicity, we use differentiation of phase
        
        # Method: Differentiate the signal and look at zero-crossings
        # Simplified approach: use difference to approximate derivative
        diff = np.diff(signal)
        
        # Envelope of the differentiated signal gives frequency info
        envelope = np.abs(diff)
        
        # Low-pass filter (simple moving average)
        window = int(self.Fs / self.Fc / 2)
        if window < 1:
            window = 1
        kernel = np.ones(window) / window
        filtered = np.convolve(envelope, kernel, mode='same')
        
        # Normalize and remove DC
        demodulated = filtered - np.mean(filtered)
        
        # Pad to match original length
        demodulated = np.concatenate([demodulated, [demodulated[-1]]])
        
        return demodulated

    def demodulate_pm(self, signal):
        """
        PM Demodulator: Phase Detector
        Extracts phase information from the signal.
        """
        # Create reference carrier
        t = np.arange(len(signal)) / self.Fs
        ref_cos = np.cos(2 * np.pi * self.Fc * t)
        ref_sin = np.sin(2 * np.pi * self.Fc * t)
        
        # Multiply by reference to extract I and Q components
        I = signal * ref_cos
        Q = signal * ref_sin
        
        # Low-pass filter (moving average)
        window = int(self.Fs / self.Fc)
        if window < 1:
            window = 1
        kernel = np.ones(window) / window
        
        I_filtered = np.convolve(I, kernel, mode='same')
        Q_filtered = np.convolve(Q, kernel, mode='same')
        
        # Extract phase using arctan2
        phase = np.arctan2(Q_filtered, I_filtered)
        
        # Unwrap phase to avoid discontinuities
        phase_unwrapped = np.unwrap(phase)
        
        # Remove carrier phase (linear trend)
        carrier_phase = 2 * np.pi * self.Fc * t
        demodulated = phase_unwrapped - carrier_phase
        
        # Remove DC offset
        demodulated = demodulated - np.mean(demodulated)
        
        return demodulated