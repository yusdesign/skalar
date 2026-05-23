import streamlit as st
import numpy as np
from utils.modulation import ModulationGenerator
from utils.visualization import SignalVisualizer

# Page configuration
st.set_page_config(
    page_title="Modulation Visualizer",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize classes
@st.cache_resource
def init_classes():
    return ModulationGenerator(), SignalVisualizer()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<p class="main-header">📡 Digital Modulation Visualizer</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Global parameters
    st.subheader("Global Parameters")
    fs = st.slider("Sampling Frequency (Hz)", 100, 5000, 1000, 100)
    duration = st.slider("Duration (seconds)", 0.5, 5.0, 1.0, 0.1)
    
    st.markdown("---")
    
    # Mode selection
    st.subheader("Operation Mode")
    mode = st.radio(
        "Select Mode",
        ["Single Modulation", "Signal Mixing"],
        help="Choose between viewing individual modulations or mixing signals"
    )

# Initialize generator with selected parameters
mod_gen = ModulationGenerator(fs=fs, duration=duration)
visualizer = SignalVisualizer()

if mode == "Single Modulation":
    # Modulation type selection
    st.markdown('<p class="sub-header">🎯 Single Modulation Mode</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**About Digital Modulation**")
        st.markdown("""
        - **ASK**: Amplitude Shift Keying - varies amplitude
        - **FSK**: Frequency Shift Keying - varies frequency  
        - **PSK**: Phase Shift Keying - varies phase
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col1:
        modulation_type = st.selectbox(
            "Select Modulation Type",
            ["ASK (Amplitude Shift Keying)", 
             "FSK (Frequency Shift Keying)", 
             "PSK (Phase Shift Keying)"]
        )
    
    st.markdown("---")
    
    # Parameters based on modulation type
    if "ASK" in modulation_type:
        st.subheader("ASK Parameters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            carrier_freq = st.number_input("Carrier Frequency (Hz)", 1, 100, 10)
        with col2:
            bit_rate = st.number_input("Bit Rate (bps)", 1, 20, 2)
        with col3:
            show_spectrum = st.checkbox("Show Spectrum", value=True)
        
        col4, col5 = st.columns(2)
        with col4:
            amp_low = st.slider("Amplitude for 0", 0.0, 1.0, 0.3, 0.1)
        with col5:
            amp_high = st.slider("Amplitude for 1", 0.0, 2.0, 1.0, 0.1)
        
        if st.button("Generate ASK Signal", type="primary"):
            with st.spinner("Generating ASK signal..."):
                ask_signal, modulating, carrier, bits, t_signal = mod_gen.generate_ask(
                    carrier_freq=carrier_freq,
                    bit_rate=bit_rate,
                    amplitude_low=amp_low,
                    amplitude_high=amp_high
                )
                
                # Plot modulation
                fig = visualizer.plot_modulation(
                    ask_signal, modulating, carrier, bits, t_signal,
                    "Amplitude Shift Keying (ASK)", "ASK Signal"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Plot spectrum if requested
                if show_spectrum:
                    st.subheader("Frequency Spectrum")
                    spectrum_fig = visualizer.plot_spectrum(
                        ask_signal, fs, "ASK Signal Spectrum"
                    )
                    st.plotly_chart(spectrum_fig, use_container_width=True)
                
                # Display information
                st.success(f"Generated ASK signal with {len(bits)} bits: {bits}")
    
    elif "FSK" in modulation_type:
        st.subheader("FSK Parameters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            freq0 = st.number_input("Frequency for 0 (Hz)", 1, 100, 5)
        with col2:
            freq1 = st.number_input("Frequency for 1 (Hz)", 1, 100, 15)
        with col3:
            bit_rate = st.number_input("Bit Rate (bps)", 1, 20, 2)
        
        show_spectrum = st.checkbox("Show Spectrum", value=True)
        
        if st.button("Generate FSK Signal", type="primary"):
            with st.spinner("Generating FSK signal..."):
                fsk_signal, modulating, bits, t_signal = mod_gen.generate_fsk(
                    carrier_freq1=freq0,
                    carrier_freq2=freq1,
                    bit_rate=bit_rate
                )
                
                # Generate a reference carrier for visualization
                carrier = np.sin(2 * np.pi * ((freq0 + freq1) / 2) * t_signal[:len(fsk_signal)])
                
                # Plot modulation
                fig = visualizer.plot_modulation(
                    fsk_signal, modulating, carrier, bits, t_signal,
                    "Frequency Shift Keying (FSK)", "FSK Signal"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                if show_spectrum:
                    st.subheader("Frequency Spectrum")
                    spectrum_fig = visualizer.plot_spectrum(
                        fsk_signal, fs, "FSK Signal Spectrum"
                    )
                    st.plotly_chart(spectrum_fig, use_container_width=True)
                
                st.success(f"Generated FSK signal with {len(bits)} bits: {bits}")
    
    elif "PSK" in modulation_type:
        st.subheader("PSK Parameters")
        col1, col2 = st.columns(2)
        
        with col1:
            carrier_freq = st.number_input("Carrier Frequency (Hz)", 1, 100, 10)
        with col2:
            bit_rate = st.number_input("Bit Rate (bps)", 1, 20, 2)
        
        show_spectrum = st.checkbox("Show Spectrum", value=True)
        
        if st.button("Generate PSK Signal", type="primary"):
            with st.spinner("Generating PSK signal..."):
                psk_signal, modulating, carrier, bits, t_signal = mod_gen.generate_psk(
                    carrier_freq=carrier_freq,
                    bit_rate=bit_rate
                )
                
                # Plot modulation
                fig = visualizer.plot_modulation(
                    psk_signal, modulating, carrier, bits, t_signal,
                    "Phase Shift Keying (PSK)", "PSK Signal"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                if show_spectrum:
                    st.subheader("Frequency Spectrum")
                    spectrum_fig = visualizer.plot_spectrum(
                        psk_signal, fs, "PSK Signal Spectrum"
                    )
                    st.plotly_chart(spectrum_fig, use_container_width=True)
                
                st.success(f"Generated PSK signal with {len(bits)} bits: {bits}")

else:  # Signal Mixing mode
    st.markdown('<p class="sub-header">🔄 Signal Mixing Mode</p>', unsafe_allow_html=True)
    
    st.info("Generate two different modulated signals and mix them together!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Signal 1 Configuration")
        mod_type1 = st.selectbox(
            "Modulation Type for Signal 1",
            ["ASK", "FSK", "PSK"],
            key="mod1"
        )
        
        if mod_type1 == "ASK":
            carrier1 = st.number_input("Carrier Freq 1 (Hz)", 1, 100, 8, key="c1")
            bit_rate1 = st.number_input("Bit Rate 1 (bps)", 1, 20, 2, key="br1")
            amp_low1 = st.slider("Amplitude Low 1", 0.0, 1.0, 0.3, key="al1")
            amp_high1 = st.slider("Amplitude High 1", 0.0, 2.0, 1.0, key="ah1")
        elif mod_type1 == "FSK":
            freq0_1 = st.number_input("Freq for 0 (Hz)", 1, 100, 5, key="f01")
            freq1_1 = st.number_input("Freq for 1 (Hz)", 1, 100, 12, key="f11")
            bit_rate1 = st.number_input("Bit Rate (bps)", 1, 20, 2, key="br1")
        else:  # PSK
            carrier1 = st.number_input("Carrier Freq (Hz)", 1, 100, 10, key="c1")
            bit_rate1 = st.number_input("Bit Rate (bps)", 1, 20, 2, key="br1")
    
    with col2:
        st.subheader("Signal 2 Configuration")
        mod_type2 = st.selectbox(
            "Modulation Type for Signal 2",
            ["ASK", "FSK", "PSK"],
            key="mod2"
        )
        
        if mod_type2 == "ASK":
            carrier2 = st.number_input("Carrier Freq 2 (Hz)", 1, 100, 15, key="c2")
            bit_rate2 = st.number_input("Bit Rate 2 (bps)", 1, 20, 2, key="br2")
            amp_low2 = st.slider("Amplitude Low 2", 0.0, 1.0, 0.3, key="al2")
            amp_high2 = st.slider("Amplitude High 2", 0.0, 2.0, 0.8, key="ah2")
        elif mod_type2 == "FSK":
            freq0_2 = st.number_input("Freq for 0 (Hz)", 1, 100, 8, key="f02")
            freq1_2 = st.number_input("Freq for 1 (Hz)", 1, 100, 18, key="f12")
            bit_rate2 = st.number_input("Bit Rate (bps)", 1, 20, 2, key="br2")
        else:  # PSK
            carrier2 = st.number_input("Carrier Freq (Hz)", 1, 100, 15, key="c2")
            bit_rate2 = st.number_input("Bit Rate (bps)", 1, 20, 2, key="br2")
    
    st.markdown("---")
    st.subheader("Mixing Parameters")
    
    col3, col4 = st.columns(2)
    with col3:
        weight1 = st.slider("Weight for Signal 1", 0.0, 1.0, 0.5, 0.1)
    with col4:
        weight2 = st.slider("Weight for Signal 2", 0.0, 1.0, 0.5, 0.1)
    
    if st.button("Generate and Mix Signals", type="primary"):
        with st.spinner("Generating and mixing signals..."):
            # Generate signal 1
            if mod_type1 == "ASK":
                sig1, mod1, carr1, bits1, t1 = mod_gen.generate_ask(
                    carrier_freq=carrier1, bit_rate=bit_rate1,
                    amplitude_low=amp_low1, amplitude_high=amp_high1
                )
            elif mod_type1 == "FSK":
                sig1, mod1, bits1, t1 = mod_gen.generate_fsk(
                    carrier_freq1=freq0_1, carrier_freq2=freq1_1,
                    bit_rate=bit_rate1
                )
            else:  # PSK
                sig1, mod1, carr1, bits1, t1 = mod_gen.generate_psk(
                    carrier_freq=carrier1, bit_rate=bit_rate1
                )
            
            # Generate signal 2
            if mod_type2 == "ASK":
                sig2, mod2, carr2, bits2, t2 = mod_gen.generate_ask(
                    carrier_freq=carrier2, bit_rate=bit_rate2,
                    amplitude_low=amp_low2, amplitude_high=amp_high2
                )
            elif mod_type2 == "FSK":
                sig2, mod2, bits2, t2 = mod_gen.generate_fsk(
                    carrier_freq1=freq0_2, carrier_freq2=freq1_2,
                    bit_rate=bit_rate2
                )
            else:  # PSK
                sig2, mod2, carr2, bits2, t2 = mod_gen.generate_psk(
                    carrier_freq=carrier2, bit_rate=bit_rate2
                )
            
            # Mix signals
            mixed = mod_gen.mix_signals(sig1, sig2, weight1, weight2)
            
            # Plot mixed signals
            t_mixed = np.linspace(0, len(mixed)/fs, len(mixed), endpoint=False)
            
            fig = visualizer.plot_mixed_signals(
                sig1, sig2, mixed, t_mixed,
                f"{mod_type1} Signal", f"{mod_type2} Signal"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show spectrums
            st.subheader("Frequency Spectrums")
            
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                spec1 = visualizer.plot_spectrum(sig1, fs, f"{mod_type1} Spectrum")
                st.plotly_chart(spec1, use_container_width=True)
            
            with col_s2:
                spec2 = visualizer.plot_spectrum(sig2, fs, f"{mod_type2} Spectrum")
                st.plotly_chart(spec2, use_container_width=True)
            
            with col_s3:
                spec_mixed = visualizer.plot_spectrum(mixed, fs, "Mixed Signal Spectrum")
                st.plotly_chart(spec_mixed, use_container_width=True)
            
            st.success(f"""
            Generated and mixed signals successfully!
            - Signal 1 ({mod_type1}): {len(bits1)} bits
            - Signal 2 ({mod_type2}): {len(bits2)} bits
            - Mixing weights: {weight1:.1f} / {weight2:.1f}
            """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Digital Modulation Visualizer | "
    "Built with Streamlit | Educational Tool for Signal Processing</p>",
    unsafe_allow_html=True
)
