import numpy as np

class DigitalEncoder:
    def __init__(self):
        # No specific initialization needed for these algorithms
        pass

    # ==========================================
    #  ANALOG TO DIGITAL (Source Coding)
    #  Input: List of floats (e.g., [0.1, 0.5, -0.2])
    #  Output: String of bits (e.g., "10110")
    # ==========================================

    def encode_pcm(self, analog_samples, bit_depth=3):
        """
        Pulse Code Modulation (PCM):
        1. Normalize signal to 0-1 range.
        2. Quantize into 2^bit_depth levels.
        3. Convert level to binary string.
        """
        if not analog_samples:
            return ""
            
        # 1. Find range to normalize
        min_val = min(analog_samples)
        max_val = max(analog_samples)
        
        # Avoid division by zero if flat line
        if max_val == min_val:
            return "0" * len(analog_samples) * bit_depth

        num_levels = 2 ** bit_depth
        encoded_bits = ""

        for sample in analog_samples:
            # Normalize sample to 0.0 -> 1.0
            normalized = (sample - min_val) / (max_val - min_val)
            
            # Scale to integer level (0 to num_levels - 1)
            # We use min() to ensure we don't exceed max index due to float rounding
            level = int(normalized * (num_levels - 1))
            
            # Convert integer to binary string with fixed length (e.g., 5 -> "101")
            binary_string = format(level, f'0{bit_depth}b')
            encoded_bits += binary_string
            
        return encoded_bits

    def encode_delta_modulation(self, analog_samples, step_size=0.1):
        """
        Delta Modulation (DM):
        Compares current sample to the accumulated value.
        1 -> Signal > Previous Approximation (Step Up)
        0 -> Signal < Previous Approximation (Step Down)
        """
        if not analog_samples:
            return ""

        encoded_bits = ""
        # The 'staircase' approximation starts at the first sample or 0
        current_approximation = 0 
        
        for sample in analog_samples:
            if sample > current_approximation:
                encoded_bits += '1'
                current_approximation += step_size
            else:
                encoded_bits += '0'
                current_approximation -= step_size
                
        return encoded_bits

    # ==========================================
    #  DIGITAL TO DIGITAL (Line Coding)
    #  Input: String of bits (e.g., "10110")
    #  Output: List of voltage levels
    # ==========================================

    def encode_nrz_l(self, bits):
        """
        NRZ-L (Non-Return-to-Zero Level):
        0 -> High (+1)
        1 -> Low (-1)
        """
        signal = []
        for bit in bits:
            if bit == '0':
                signal.extend([1, 1]) # High
            else:
                signal.extend([-1, -1]) # Low
        return signal

    def encode_nrzi(self, bits):
        """
        NRZI (Non-Return-to-Zero Inverted):
        0 -> No transition
        1 -> Transition at the beginning of the interval
        """
        signal = []
        current_level = 1 
        for bit in bits:
            if bit == '1':
                current_level *= -1
            signal.extend([current_level, current_level])
        return signal

    def encode_bipolar_ami(self, bits):
        """
        Bipolar-AMI:
        0 -> Zero voltage
        1 -> Alternating Positive and Negative
        """
        signal = []
        last_one = -1
        for bit in bits:
            if bit == '0':
                signal.extend([0, 0])
            else:
                last_one *= -1
                signal.extend([last_one, last_one])
        return signal

    def encode_pseudoternary(self, bits):
        """
        Pseudoternary:
        1 -> Zero voltage
        0 -> Alternating Positive and Negative
        """
        signal = []
        last_zero = -1
        for bit in bits:
            if bit == '1':
                signal.extend([0, 0])
            else:
                last_zero *= -1
                signal.extend([last_zero, last_zero])
        return signal

    def encode_manchester(self, bits):
        """
        Manchester:
        0 -> High to Low transition
        1 -> Low to High transition
        """
        signal = []
        for bit in bits:
            if bit == '0':
                signal.extend([1, -1]) # High -> Low
            else:
                signal.extend([-1, 1]) # Low -> High
        return signal

    def encode_diff_manchester(self, bits):
        """
        Differential Manchester:
        Always a transition in the middle.
        0 -> Transition at the start
        1 -> No transition at the start
        """
        signal = []
        current_level = -1 
        for bit in bits:
            if bit == '0':
                current_level *= -1
            signal.append(current_level)
            current_level *= -1
            signal.append(current_level)
        return signal