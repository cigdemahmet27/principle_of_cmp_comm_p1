import numpy as np
import matplotlib.pyplot as plt

# This is our analog signal (continuous-like)
fs_analog = 1_000_000  # 1 million samples per second = high resolution
t = np.linspace(0, 0.01, int(fs_analog * 0.01)) 
analog_signal = np.sin(2 * np.pi * 1000 * t)  # 1 kHz sine wave

plt.plot(t[:2000], analog_signal[:2000])
plt.title("Analog Signal (Simulated)")
plt.show()
