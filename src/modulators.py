import numpy as np

# ==========================================
# MODULATOR CLASS (The Transmitter)
# ==========================================
class Modulator:
    def __init__(self, Fs=1000, Fc=5, Amp=1):
        """
        :param Fs: Sampling Frequency (Hz)
        :param Fc: Carrier Frequency (Hz)
        :param Amp: Amplitude of the carrier
        """
        self.Fs = Fs
        self.Fc = Fc
        self.Amp = Amp

    def modulate_ask(self, bits, T=1):
        """ Amplitude Shift Keying (Digital -> Analog) """
        signal = np.array([])
        t_bit = np.arange(0, T, 1/self.Fs)
        
        for bit in bits:
            if bit == '1':
                wave = self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)
            else:
                wave = 0 * t_bit
            signal = np.concatenate((signal, wave))
        return signal

    def modulate_psk(self, bits, T=1):
        """ Phase Shift Keying / BPSK (Digital -> Analog) """
        signal = np.array([])
        t_bit = np.arange(0, T, 1/self.Fs)
        
        for bit in bits:
            if bit == '1': # Phase 0
                wave = self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)
            else:          # Phase 180 (Multiply by -1)
                wave = -1 * self.Amp * np.sin(2 * np.pi * self.Fc * t_bit)
            signal = np.concatenate((signal, wave))
        return signal

    def modulate_bfsk(self, bits, T=1, f_dev=2):
        """ Binary Frequency Shift Keying (Digital -> Analog) """
        signal = np.array([])
        t_bit = np.arange(0, T, 1/self.Fs)
        f1 = self.Fc + f_dev # High Freq
        f2 = self.Fc - f_dev # Low Freq
        
        for bit in bits:
            if bit == '1':
                wave = self.Amp * np.sin(2 * np.pi * f1 * t_bit)
            else:
                wave = self.Amp * np.sin(2 * np.pi * f2 * t_bit)
            signal = np.concatenate((signal, wave))
        return signal

    def modulate_qam(self, bits, T=1):
        """ 4-QAM (Digital -> Analog) - Groups 2 bits """
        if len(bits) % 2 != 0: bits += '0' # Pad
        signal = np.array([])
        t_symbol = np.arange(0, 2*T, 1/self.Fs) # Duration is 2T for 2 bits
        
        for i in range(0, len(bits), 2):
            symbol = bits[i:i+2]
            # Map bits to amplitude: 0->-1, 1->+1
            i_amp = 1 if symbol[0] == '1' else -1
            q_amp = 1 if symbol[1] == '1' else -1
            
            # I*cos - Q*sin
            wave = (i_amp * self.Amp * np.cos(2 * np.pi * self.Fc * t_symbol)) - \
                   (q_amp * self.Amp * np.sin(2 * np.pi * self.Fc * t_symbol))
            signal = np.concatenate((signal, wave))
        return signal

    def modulate_am(self, analog_data):
        """ Amplitude Modulation (Analog -> Analog) """
        # Formula: s(t) = [1 + m(t)] * Carrier
        # We assume analog_data is normalized (-1 to 1)
        t = np.arange(0, len(analog_data)/self.Fs, 1/self.Fs)
        # Ensure t matches data length exactly due to floating point precision
        t = t[:len(analog_data)] 
        
        carrier = self.Amp * np.cos(2 * np.pi * self.Fc * t)
        modulated_signal = (1 + analog_data) * carrier
        return modulated_signal

    def modulate_fm(self, analog_data, kf=5):
        """
        Frequency Modulation (Analog -> Analog)
        :param analog_data: Input message signal
        :param kf: Frequency sensitivity (Hz per unit amplitude)
        Formula: s(t) = A * cos(2*pi*Fc*t + 2*pi*kf * integral(m(t)))
        """
        t = np.arange(0, len(analog_data)/self.Fs, 1/self.Fs)
        t = t[:len(analog_data)]
        
        # Integrate the message signal (cumulative sum * dt)
        dt = 1 / self.Fs
        integral = np.cumsum(analog_data) * dt
        
        # Instantaneous phase
        phase = 2 * np.pi * self.Fc * t + 2 * np.pi * kf * integral
        modulated_signal = self.Amp * np.cos(phase)
        
        return modulated_signal

    def modulate_pm(self, analog_data, kp=np.pi/2):
        """
        Phase Modulation (Analog -> Analog)
        :param analog_data: Input message signal
        :param kp: Phase sensitivity (radians per unit amplitude)
        Formula: s(t) = A * cos(2*pi*Fc*t + kp * m(t))
        """
        t = np.arange(0, len(analog_data)/self.Fs, 1/self.Fs)
        t = t[:len(analog_data)]
        
        # Phase is directly proportional to message signal
        phase = 2 * np.pi * self.Fc * t + kp * analog_data
        modulated_signal = self.Amp * np.cos(phase)
        
        return modulated_signal