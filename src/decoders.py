class DigitalDecoder:
    def __init__(self):
        # No specific initialization needed for these algorithms
        pass

    # ==========================================
    #  DIGITAL TO ANALOG (Source Decoding)
    #  Input: String of bits (e.g., "10110")
    #  Output: List of floats (Approximate Analog Signal)
    # ==========================================

    def decode_pcm(self, bits, bit_depth=3, min_val=0.0, max_val=1.0):
        """
        PCM Decoder:
        1. Breaks the bit string into chunks of size 'bit_depth'.
        2. Converts binary chunk to integer level.
        3. Maps integer level back to original voltage range (min_val to max_val).
        
        Args:
            bits: Encoded bit string
            bit_depth: Number of bits per sample
            min_val: Original signal minimum value
            max_val: Original signal maximum value
        """
        if not bits:
            return []
            
        analog_output = []
        num_levels = 2 ** bit_depth
        
        # Process the string in chunks of 'bit_depth'
        # e.g., if depth is 3: "101110" -> "101", "110"
        for i in range(0, len(bits), bit_depth):
            chunk = bits[i : i + bit_depth]
            
            # If we have a partial chunk at the end (error in transmission), ignore it
            if len(chunk) < bit_depth:
                break
                
            # Convert binary string to integer (e.g., "101" -> 5)
            level = int(chunk, 2)
            
            # Convert level back to normalized float (0.0 to 1.0)
            normalized = level / (num_levels - 1)
            
            # Scale back to original range
            voltage = normalized * (max_val - min_val) + min_val
            
            analog_output.append(voltage)
            
        return analog_output

    def decode_delta_modulation(self, bits, step_size=0.1):
        """
        Delta Modulation Decoder:
        Reconstructs the signal by stepping up or down.
        1 -> Add step_size
        0 -> Subtract step_size
        """
        if not bits:
            return []
            
        analog_output = []
        # We assume the signal started at 0 (or a known reference voltage)
        current_value = 0.0
        
        for bit in bits:
            if bit == '1':
                current_value += step_size
            else:
                current_value -= step_size
            
            analog_output.append(current_value)
            
        return analog_output

    # ==========================================
    #  DIGITAL TO DIGITAL (Line Decoding)
    #  Input: List of voltage levels
    #  Output: String of bits
    # ==========================================

    def decode_nrz_l(self, signal):
        """
        NRZ-L Decoder:
        Voltage > 0 (+1) -> '0'
        Voltage < 0 (-1) -> '1'
        """
        decoded_bits = ""
        # We step by 2 because the encoder generated 2 samples per bit
        for i in range(0, len(signal), 2):
            sample = signal[i]
            # Basic Thresholding
            if sample > 0:
                decoded_bits += "0"
            else:
                decoded_bits += "1"
        return decoded_bits

    def decode_nrzi(self, signal):
        """
        NRZI Decoder:
        Compare current voltage level with previous level.
        Change -> '1'
        No Change -> '0'
        """
        decoded_bits = ""
        # The encoder assumed starting High (+1)
        last_level = 1 
        
        for i in range(0, len(signal), 2):
            current_level = signal[i]
            
            # Check for transition
            if current_level != last_level:
                decoded_bits += "1"
            else:
                decoded_bits += "0"
                
            last_level = current_level # Update for next bit
            
        return decoded_bits

    def decode_bipolar_ami(self, signal):
        """
        AMI Decoder:
        0 Volts -> '0'
        Non-Zero (+1 or -1) -> '1'
        """
        decoded_bits = ""
        for i in range(0, len(signal), 2):
            sample = signal[i]
            if sample == 0:
                decoded_bits += "0"
            else:
                decoded_bits += "1"
        return decoded_bits

    def decode_pseudoternary(self, signal):
        """
        Pseudoternary Decoder:
        0 Volts -> '1'
        Non-Zero (+1 or -1) -> '0'
        """
        decoded_bits = ""
        for i in range(0, len(signal), 2):
            sample = signal[i]
            if sample == 0:
                decoded_bits += "1"
            else:
                decoded_bits += "0"
        return decoded_bits

    def decode_manchester(self, signal):
        """
        Manchester Decoder:
        Reads the first half of the bit interval.
        High (+1) -> '0' (0 is High-to-Low)
        Low (-1)  -> '1' (1 is Low-to-High)
        """
        decoded_bits = ""
        for i in range(0, len(signal), 2):
            first_half = signal[i]
            if first_half == 1:
                decoded_bits += "0"
            else:
                decoded_bits += "1"
        return decoded_bits

    def decode_diff_manchester(self, signal):
        """
        Differential Manchester Decoder:
        Compare the START of the current bit with the END of the previous bit.
        Transition at boundary -> '0'
        No Transition at boundary -> '1'
        """
        decoded_bits = ""
        # Assuming the line was previously Low (-1) before transmission started
        prev_end_level = -1
        
        for i in range(0, len(signal), 2):
            current_start_level = signal[i]
            current_end_level = signal[i+1] # We need the end to update state
            
            # If the level changed exactly at the boundary line
            if current_start_level != prev_end_level:
                decoded_bits += "0"
            else:
                decoded_bits += "1"
                
            prev_end_level = current_end_level
            
        return decoded_bits