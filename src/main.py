import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import sys
import os

# Import your custom classes
# Ensure your encoders.py and decoders.py contain the updated classes I provided previously!
from encoders import DigitalEncoder
from decoders import DigitalDecoder
from modulators import Modulator
from demodulators import Demodulator

class CommunicationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Communication System Simulator")
        self.root.geometry("1200x800")

        # --- Backend Systems ---
        self.Fs = 1000
        self.Fc = 5
        self.enc = DigitalEncoder()
        self.dec = DigitalDecoder()
        self.mod = Modulator(Fs=self.Fs, Fc=self.Fc)
        self.demod = Demodulator(Fs=self.Fs, Fc=self.Fc)

        # --- UI Layout ---
        self.create_widgets()
        
    def create_widgets(self):
        # 1. Control Panel (Top)
        control_frame = ttk.LabelFrame(self.root, text="Configuration")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Input Data
        ttk.Label(control_frame, text="Binary Input:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_input = ttk.Entry(control_frame, width=30)
        self.entry_input.insert(0, "01001100011") # Default value
        self.entry_input.grid(row=0, column=1, padx=5, pady=5)

        # Transmission Mode
        ttk.Label(control_frame, text="Transmission Mode:").grid(row=0, column=2, padx=5, pady=5)
        self.combo_mode = ttk.Combobox(control_frame, values=[
            "Digital-to-Digital", 
            "Digital-to-Analog",
            "Analog-to-Analog",
            "Analog-to-Digital"  # <--- ADDED NEW MODE
        ], state="readonly", width=20)
        self.combo_mode.current(0)
        self.combo_mode.bind("<<ComboboxSelected>>", self.update_algorithms)
        self.combo_mode.grid(row=0, column=3, padx=5, pady=5)

        # Algorithm Selection
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=4, padx=5, pady=5)
        self.combo_algo = ttk.Combobox(control_frame, state="readonly", width=20)
        self.combo_algo.grid(row=0, column=5, padx=5, pady=5)
        
        # Run Button
        self.btn_run = ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        self.btn_run.grid(row=0, column=6, padx=10, pady=5)
        
        # Benchmark Button
        self.btn_benchmark = ttk.Button(control_frame, text="Run Benchmark", command=self.run_benchmark)
        self.btn_benchmark.grid(row=0, column=7, padx=10, pady=5)

        # Initialize Algorithms
        self.update_algorithms(None)

        # 2. Plotting Area (Center)
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Matplotlib Figure
        self.fig, self.axs = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_algorithms(self, event):
        """Updates the Algorithm dropdown based on the Mode selection."""
        mode = self.combo_mode.get()
        
        if mode == "Digital-to-Digital":
            self.combo_algo['values'] = ["NRZ-L", "NRZI", "Bipolar-AMI", "Pseudoternary", "Manchester", "Diff. Manchester"]
            self.entry_input.config(state="normal")
            
        elif mode == "Digital-to-Analog":
            self.combo_algo['values'] = ["ASK", "PSK", "BFSK", "4-QAM"]
            self.entry_input.config(state="normal")
            
        elif mode == "Analog-to-Analog":
            self.combo_algo['values'] = ["AM (Amplitude Mod)", "FM (Frequency Mod)", "PM (Phase Mod)"]
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, "(Simulated Sine Wave)")
            self.entry_input.config(state="disabled") 
            
        elif mode == "Analog-to-Digital": # <--- NEW LOGIC
            self.combo_algo['values'] = ["PCM (Pulse Code Mod)", "Delta Modulation"]
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, "(Simulated Sine Wave)")
            self.entry_input.config(state="disabled")

        self.combo_algo.current(0)

    def run_benchmark(self):
        """Launch the benchmark script in a new terminal window."""
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            benchmark_path = os.path.join(script_dir, "benchmark.py")
            
            # Run benchmark in new terminal window
            if sys.platform == "win32":
                subprocess.Popen(["start", "cmd", "/k", sys.executable, benchmark_path], shell=True)
            else:
                subprocess.Popen([sys.executable, benchmark_path])
            
            messagebox.showinfo("Benchmark", "Benchmark started in a new terminal window!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start benchmark: {e}")

    def run_simulation(self):
        """Main execution logic."""
        mode = self.combo_mode.get()
        algo = self.combo_algo.get()
        input_bits = self.entry_input.get()

        # Clear previous plots
        for ax in self.axs: ax.clear()

        try:
            if mode == "Digital-to-Digital":
                self.run_digital_digital(algo, input_bits)
            elif mode == "Digital-to-Analog":
                self.run_digital_analog(algo, input_bits)
            elif mode == "Analog-to-Analog":
                self.run_analog_analog(algo)
            elif mode == "Analog-to-Digital": # <--- NEW HANDLER
                self.run_analog_digital(algo)
            
            # Refresh Canvas
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- SIMULATION LOGIC ---

    def run_digital_digital(self, algo, bits):
        # 1. Visualization of Input
        self.plot_input_bits(bits, ax_index=0, title="Input Data")

        # 2. Encoding (Sender)
        if algo == "NRZ-L": signal = self.enc.encode_nrz_l(bits)
        elif algo == "NRZI": signal = self.enc.encode_nrzi(bits)
        elif algo == "Bipolar-AMI": signal = self.enc.encode_bipolar_ami(bits)
        elif algo == "Pseudoternary": signal = self.enc.encode_pseudoternary(bits)
        elif algo == "Manchester": signal = self.enc.encode_manchester(bits)
        elif algo == "Diff. Manchester": signal = self.enc.encode_diff_manchester(bits)

        # Plot Encoded Signal
        t = np.arange(0, len(signal)/2, 0.5) 
        self.axs[1].plot(t, signal, drawstyle='steps-post', color='blue')
        self.axs[1].set_title(f"Transmitted Signal (Encoded: {algo})")
        self.axs[1].grid(True)

        # 3. Decoding (Receiver)
        if algo == "NRZ-L": decoded = self.dec.decode_nrz_l(signal)
        elif algo == "NRZI": decoded = self.dec.decode_nrzi(signal)
        elif algo == "Bipolar-AMI": decoded = self.dec.decode_bipolar_ami(signal)
        elif algo == "Pseudoternary": decoded = self.dec.decode_pseudoternary(signal)
        elif algo == "Manchester": decoded = self.dec.decode_manchester(signal)
        elif algo == "Diff. Manchester": decoded = self.dec.decode_diff_manchester(signal)

        # 4. Visualization of Output
        self.plot_output_bits(decoded)
        self.axs[2].set_title(f"Receiver Output: {decoded}")

    def run_digital_analog(self, algo, bits):
        # 1. Visualization of Input
        self.plot_input_bits(bits, ax_index=0, title="Input Data")

        # 2. Modulation (Sender)
        if algo == "ASK": signal = self.mod.modulate_ask(bits)
        elif algo == "PSK": signal = self.mod.modulate_psk(bits)
        elif algo == "BFSK": signal = self.mod.modulate_bfsk(bits)
        elif algo == "4-QAM": signal = self.mod.modulate_qam(bits)

        # Plot Modulated Signal
        self.axs[1].plot(signal, color='green', linewidth=0.8)
        self.axs[1].set_title(f"Transmitted Signal (Modulated: {algo})")
        self.axs[1].grid(True)

        # 3. Demodulation (Receiver)
        if algo == "ASK": decoded = self.demod.demodulate_ask(signal)
        elif algo == "PSK": decoded = self.demod.demodulate_psk(signal)
        elif algo == "BFSK": decoded = self.demod.demodulate_bfsk(signal)
        elif algo == "4-QAM": decoded = self.demod.demodulate_qam(signal)

        # 4. Visualization of Output
        self.plot_output_bits(decoded)
        self.axs[2].set_title(f"Receiver Output: {decoded}")

    def run_analog_analog(self, algo):
        # 1. Generate Dummy Analog Input
        t = np.arange(0, 1, 1/self.Fs)
        input_signal = 0.5 * np.sin(2 * np.pi * 2 * t) 

        self.axs[0].plot(t, input_signal, color='orange')
        self.axs[0].set_title("Input: Analog Source (2Hz Sine Wave)")
        self.axs[0].grid(True)

        # 2. Modulation
        if "AM" in algo:
            transmitted = self.mod.modulate_am(input_signal)
            mod_name = "AM - Amplitude Modulation"
        elif "FM" in algo:
            transmitted = self.mod.modulate_fm(input_signal)
            mod_name = "FM - Frequency Modulation"
        elif "PM" in algo:
            transmitted = self.mod.modulate_pm(input_signal)
            mod_name = "PM - Phase Modulation"

        self.axs[1].plot(t, transmitted, color='green')
        self.axs[1].set_title(f"Transmitted Signal ({mod_name})")
        self.axs[1].grid(True)

        # 3. Info panel (no demodulation shown for analog signals)
        self.axs[2].text(0.5, 0.5, f"Analog-to-Analog: {mod_name}\nCarrier Freq: {self.Fc} Hz", 
                         ha='center', va='center', fontsize=12, transform=self.axs[2].transAxes)
        self.axs[2].set_title("Transmission Complete")
        self.axs[2].axis('off')

    def run_analog_digital(self, algo):
        """
        New Handler for PCM and Delta Modulation
        """
        # 1. Generate Input (Analog Sine Wave)
        # Use fewer points to make the staircase effect visible
        t = np.linspace(0, 2*np.pi, 50) 
        input_signal = np.sin(t)
        
        # Shift signal to be positive (0 to 2) for easier PCM/Delta logic
        input_signal = input_signal + 1.2 

        self.axs[0].plot(t, input_signal, color='orange', marker='o', markersize=4)
        self.axs[0].set_title("Input: Analog Signal (Sampled)")
        self.axs[0].grid(True)

        # 2. Encode (Analog -> Digital Bits)
        encoded_bits = ""
        if "PCM" in algo:
            # bit_depth=3 means 3 bits per sample
            encoded_bits = self.enc.encode_pcm(input_signal.tolist(), bit_depth=3)
        elif "Delta" in algo:
            # step_size determines how fast it can track changes
            encoded_bits = self.enc.encode_delta_modulation(input_signal.tolist(), step_size=0.4)

        # Plot the Bits (Middle Graph)
        # We reuse the existing bit plotter, but title it differently
        self.plot_input_bits(encoded_bits, ax_index=1, title=f"Encoded Digital Stream ({algo})")

        # 3. Decode (Digital Bits -> Analog)
        reconstructed_signal = []
        if "PCM" in algo:
            reconstructed_signal = self.dec.decode_pcm(encoded_bits, bit_depth=3)
        elif "Delta" in algo:
            reconstructed_signal = self.dec.decode_delta_modulation(encoded_bits, step_size=0.4)

        # 4. Plot Output (Bottom Graph)
        # We plot it against the original time 't' to see the overlap
        self.axs[2].step(t, reconstructed_signal, where='post', color='purple', linewidth=2, label='Reconstructed')
        self.axs[2].plot(t, input_signal, color='orange', alpha=0.3, label='Original') # Show original faint in background
        self.axs[2].set_title(f"Receiver Output (Analog Reconstructed)")
        self.axs[2].legend()
        self.axs[2].grid(True)

    # --- HELPER FUNCTIONS ---
    def plot_input_bits(self, bits, ax_index=0, title="Input Data"):
        """Draws binary bits as a simple square wave."""
        x = []
        y = []
        # Protect against empty bit strings
        if not bits: 
            return

        for i, bit in enumerate(bits):
            val = 1 if bit == '1' else 0
            x.extend([i, i+1])
            y.extend([val, val])
        
        self.axs[ax_index].plot(x, y, color='black', linewidth=2)
        self.axs[ax_index].set_ylim(-0.5, 1.5)
        self.axs[ax_index].set_title(f"{title}: {bits[:30]}..." if len(bits)>30 else f"{title}: {bits}")
        self.axs[ax_index].grid(True)

    def plot_output_bits(self, bits):
        """Draws output bits."""
        x = []
        y = []
        if not bits: return

        for i, bit in enumerate(bits):
            val = 1 if bit == '1' else 0
            x.extend([i, i+1])
            y.extend([val, val])
        self.axs[2].plot(x, y, color='blue', linewidth=2, linestyle='--')
        self.axs[2].set_ylim(-0.5, 1.5)
        self.axs[2].grid(True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CommunicationSimulator(root)
    root.mainloop()