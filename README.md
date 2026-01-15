# Communication System Simulator

A Python-based simulation of data transmission between two computers, demonstrating encoding, modulation, and demodulation techniques used in digital and analog communication systems.

## 📋 Project Overview

This project simulates the complete communication pipeline between **Computer A (Sender)** and **Computer B (Receiver)** using four fundamental transmission modes:

| Mode | Description | Example Algorithms |
|------|-------------|-------------------|
| **Digital-to-Digital** | Line coding for digital channels | NRZ-L, NRZI, Manchester, Bipolar-AMI |
| **Digital-to-Analog** | Modulation for analog channels | ASK, PSK, BFSK, QAM |
| **Analog-to-Digital** | Source coding (digitization) | PCM, Delta Modulation |
| **Analog-to-Analog** | Analog modulation | AM, FM, PM |

The application features an interactive GUI that visualizes the entire transmission process in real-time.

## 🗂️ Project Structure

```
pcom_p1/
├── src/
│   ├── main.py                  # GUI application (Tkinter)
│   ├── encoders.py              # Line coding encoders
│   ├── encoders_optimized.py    # AI-optimized encoders (NumPy)
│   ├── decoders.py              # Signal decoders
│   ├── decoders_optimized.py    # AI-optimized decoders
│   ├── modulators.py            # Digital & analog modulators
│   ├── modulators_optimized.py  # AI-optimized modulators
│   ├── demodulators.py          # Signal demodulators
│   ├── demodulators_optimized.py# AI-optimized demodulators
│   └── benchmark.py             # Performance comparison script
├── report.tex                   # LaTeX project report
├── report.pdf                   # Compiled report
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed with the following packages:

```bash
pip install numpy matplotlib
```

> **Note:** Tkinter comes pre-installed with Python on most systems. If not, install it via your package manager.

### Running the Application

1. **Navigate to the source directory:**
   ```bash
   cd pcom_p1/src
   ```

2. **Run the main application:**
   ```bash
   python main.py
   ```

3. **The GUI will open** - select a transmission mode, algorithm, and click **Run Simulation**.

### Running the Benchmark

To compare performance between original and optimized implementations:

```bash
cd pcom_p1/src
python benchmark.py
```

Or use the **Run Benchmark** button in the GUI.

## 🎮 How to Use

1. **Select Transmission Mode:**
   - Digital-to-Digital: Enter binary data (e.g., `01001100011`)
   - Digital-to-Analog: Enter binary data
   - Analog-to-Digital: Uses simulated sine wave
   - Analog-to-Analog: Uses simulated sine wave

2. **Select Algorithm** from the dropdown

3. **Click "Run Simulation"**

4. **View the results** in three panels:
   - **Top:** Input signal
   - **Middle:** Transmitted/Encoded signal
   - **Bottom:** Received/Decoded signal

## 📊 Implemented Algorithms

### Line Coding (Digital-to-Digital)
- **NRZ-L** - Non-Return-to-Zero Level
- **NRZI** - Non-Return-to-Zero Inverted
- **Bipolar-AMI** - Alternate Mark Inversion
- **Pseudoternary** - Inverse of Bipolar-AMI
- **Manchester** - Self-clocking with mid-bit transitions
- **Differential Manchester** - Transition-based encoding

### Digital Modulation (Digital-to-Analog)
- **ASK** - Amplitude Shift Keying
- **PSK/BPSK** - Phase Shift Keying
- **BFSK** - Binary Frequency Shift Keying
- **4-QAM** - Quadrature Amplitude Modulation

### Source Coding (Analog-to-Digital)
- **PCM** - Pulse Code Modulation
- **Delta Modulation** - Difference encoding

### Analog Modulation (Analog-to-Analog)
- **AM** - Amplitude Modulation
- **FM** - Frequency Modulation
- **PM** - Phase Modulation

## ⚡ AI Optimization

The project includes optimized versions of encoders and modulators using NumPy vectorization:

| Algorithm | Original | Optimized | Speedup |
|-----------|----------|-----------|---------|
| NRZ-L Encoder | 0.188 ms | 0.178 ms | 1.05x |
| ASK Modulator | 5.066 ms | 1.812 ms | **2.79x** |
| PSK Modulator | 4.611 ms | 1.759 ms | **2.62x** |

## 📝 Building the Report

To compile the LaTeX report:

```bash
cd pcom_p1
pdflatex report.tex
```

## 👤 Author

**Ahmet Enes Çiğdem** - 150220079

## 📚 References

- Forouzan, B. A. (2012). *Data Communications and Networking*. McGraw-Hill.
- Haykin, S. (2001). *Communication Systems*. Wiley.
