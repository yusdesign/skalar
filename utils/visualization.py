import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class SignalVisualizer:
    def __init__(self):
        self.colors = {
            'signal': '#1f77b4',
            'modulating': '#ff7f0e',
            'carrier': '#2ca02c',
            'mixed': '#d62728'
        }
    
    def plot_modulation(self, modulated_signal, modulating_signal, carrier_signal, 
                       bits, t_signal, title, signal_name):
        """Create interactive plot for modulation visualization"""
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Binary Data', 'Modulated Signal', 'Modulating Signal vs Carrier'),
            vertical_spacing=0.12
        )
        
        # Plot binary data
        samples_per_bit = len(t_signal) // len(bits)
        t_bits = np.arange(len(bits)) / (len(bits) / t_signal[-1]) if len(t_signal) > 0 else np.arange(len(bits))
        
        fig.add_trace(
            go.Scatter(x=t_bits, y=bits, mode='lines+markers', 
                      name='Binary Data', line=dict(color='black', width=2)),
            row=1, col=1
        )
        
        # Plot modulated signal
        fig.add_trace(
            go.Scatter(x=t_signal, y=modulated_signal, mode='lines',
                      name=signal_name, line=dict(color=self.colors['signal'], width=1.5)),
            row=2, col=1
        )
        
        # Plot modulating and carrier signals
        fig.add_trace(
            go.Scatter(x=t_signal, y=modulating_signal[:len(t_signal)], mode='lines',
                      name='Modulating', line=dict(color=self.colors['modulating'], width=1.5)),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=t_signal, y=carrier_signal[:len(t_signal)], mode='lines',
                      name='Carrier', line=dict(color=self.colors['carrier'], width=1)),
            row=3, col=1
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            title_text=title,
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Time (s)", row=1, col=1)
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_xaxes(title_text="Time (s)", row=3, col=1)
        
        fig.update_yaxes(title_text="Bit Value", row=1, col=1, range=[-0.5, 1.5])
        fig.update_yaxes(title_text="Amplitude", row=2, col=1)
        fig.update_yaxes(title_text="Amplitude", row=3, col=1)
        
        return fig
    
    def plot_mixed_signals(self, signal1, signal2, mixed_signal, t_signal, 
                          label1, label2):
        """Create interactive plot for mixed signals visualization"""
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(f'Signal 1 ({label1})', f'Signal 2 ({label2})', 'Mixed Signal'),
            vertical_spacing=0.12
        )
        
        # Ensure all signals have the same length
        min_length = min(len(signal1), len(signal2), len(mixed_signal), len(t_signal))
        t = t_signal[:min_length]
        s1 = signal1[:min_length]
        s2 = signal2[:min_length]
        ms = mixed_signal[:min_length]
        
        # Plot signal 1
        fig.add_trace(
            go.Scatter(x=t, y=s1, mode='lines',
                      name=f'{label1}', line=dict(color=self.colors['signal'], width=1.5)),
            row=1, col=1
        )
        
        # Plot signal 2
        fig.add_trace(
            go.Scatter(x=t, y=s2, mode='lines',
                      name=f'{label2}', line=dict(color=self.colors['carrier'], width=1.5)),
            row=2, col=1
        )
        
        # Plot mixed signal
        fig.add_trace(
            go.Scatter(x=t, y=ms, mode='lines',
                      name='Mixed Signal', line=dict(color=self.colors['mixed'], width=2)),
            row=3, col=1
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            title_text="Signal Mixing Visualization",
            showlegend=True,
            hovermode='x unified'
        )
        
        for i in range(1, 4):
            fig.update_xaxes(title_text="Time (s)", row=i, col=1)
            fig.update_yaxes(title_text="Amplitude", row=i, col=1)
        
        return fig
    
    def plot_spectrum(self, signal, fs, title="Frequency Spectrum"):
        """Plot frequency spectrum of a signal"""
        n = len(signal)
        freq = np.fft.fftfreq(n, 1/fs)
        fft_vals = np.abs(np.fft.fft(signal)) / n
        
        # Only show positive frequencies
        pos_mask = freq >= 0
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(x=freq[pos_mask], y=fft_vals[pos_mask], mode='lines',
                      name='Spectrum', line=dict(color='#9467bd', width=2))
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude",
            height=400,
            showlegend=False,
            hovermode='x unified'
        )
        
        return fig
