import numpy as np
from scipy import signal

class ModulationGenerator:
    def __init__(self, fs=1000, duration=1.0):
        """
        Initialize modulation generator
        
        Parameters:
        fs: Sampling frequency (Hz)
        duration: Signal duration (seconds)
        """
        self.fs = fs
        self.duration = duration
        self.t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        
    def generate_binary_data(self, bits=8):
        """Generate random binary data"""
        return np.random.randint(0, 2, bits)
    
    def generate_ask(self, carrier_freq=10, bit_rate=2, amplitude_low=0.3, amplitude_high=1.0):
        """
        Generate Amplitude Shift Keying signal
        
        Parameters:
        carrier_freq: Carrier frequency (Hz)
        bit_rate: Bits per second
        amplitude_low: Amplitude for binary 0
        amplitude_high: Amplitude for binary 1
        """
        bits = self.generate_binary_data()
        samples_per_bit = int(self.fs / bit_rate)
        total_samples = samples_per_bit * len(bits)
        t_signal = np.linspace(0, len(bits)/bit_rate, total_samples, endpoint=False)
        
        # Generate carrier wave
        carrier = np.sin(2 * np.pi * carrier_freq * t_signal)
        
        # Generate modulating signal
        modulating = np.repeat(bits, samples_per_bit)
        modulating = np.where(modulating == 0, amplitude_low, amplitude_high)
        
        # ASK signal
        ask_signal = modulating * carrier
        
        return ask_signal, modulating, carrier[:len(ask_signal)], bits, t_signal
    
    def generate_fsk(self, carrier_freq1=5, carrier_freq2=15, bit_rate=2):
        """
        Generate Frequency Shift Keying signal
        
        Parameters:
        carrier_freq1: Frequency for binary 0 (Hz)
        carrier_freq2: Frequency for binary 1 (Hz)
        bit_rate: Bits per second
        """
        bits = self.generate_binary_data()
        samples_per_bit = int(self.fs / bit_rate)
        total_samples = samples_per_bit * len(bits)
        t_signal = np.linspace(0, len(bits)/bit_rate, total_samples, endpoint=False)
        
        fsk_signal = np.zeros(total_samples)
        
        for i, bit in enumerate(bits):
            start_idx = i * samples_per_bit
            end_idx = (i + 1) * samples_per_bit
            
            if bit == 0:
                freq = carrier_freq1
            else:
                freq = carrier_freq2
                
            fsk_signal[start_idx:end_idx] = np.sin(2 * np.pi * freq * t_signal[start_idx:end_idx])
        
        modulating = np.repeat(bits, samples_per_bit)
        
        return fsk_signal, modulating, bits, t_signal
    
    def generate_psk(self, carrier_freq=10, bit_rate=2):
        """
        Generate Phase Shift Keying signal
        
        Parameters:
        carrier_freq: Carrier frequency (Hz)
        bit_rate: Bits per second
        """
        bits = self.generate_binary_data()
        samples_per_bit = int(self.fs / bit_rate)
        total_samples = samples_per_bit * len(bits)
        t_signal = np.linspace(0, len(bits)/bit_rate, total_samples, endpoint=False)
        
        # Generate modulating signal
        modulating = np.repeat(bits, samples_per_bit)
        
        # PSK signal (phase shift of π for bit 1)
        carrier = np.sin(2 * np.pi * carrier_freq * t_signal)
        phase_shift = np.pi * modulating
        psk_signal = np.sin(2 * np.pi * carrier_freq * t_signal + phase_shift)
        
        return psk_signal, modulating, carrier, bits, t_signal
    
    def mix_signals(self, signal1, signal2, weight1=0.5, weight2=0.5):
        """
        Mix two signals with specified weights
        
        Parameters:
        signal1: First signal array
        signal2: Second signal array
        weight1: Weight for first signal
        weight2: Weight for second signal
        """
        # Ensure signals have the same length
        min_length = min(len(signal1), len(signal2))
        mixed = (weight1 * signal1[:min_length] + weight2 * signal2[:min_length]) / (weight1 + weight2)
        return mixed
