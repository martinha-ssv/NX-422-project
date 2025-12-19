import streamlit as st
import pandas as pd
import numpy as np
import argparse
from matplotlib.animation import FuncAnimation, FFMpegWriter
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Amplitude Modulation')
parser.add_argument('--simulation', type=str, choices=['app', 'ani'], default='app', help='Simulation type: app or ani')
args = parser.parse_args()

def app():
    tab1, tab3 = st.tabs(["Chart", "Interference"])


    carrier_freqs = np.array([20e3, 22e3])  # Hz

    ratio = st.slider("Current Ratio", 0.0, 1.0, 0.5)
    carrier_amplitudes = np.array([ratio, (1 - ratio)]) * 2e-3  # A

    t = np.linspace(start=0, stop=1, num=2000).reshape(-1, 1)  # s
    signals = carrier_amplitudes * np.sin(2 * np.pi * carrier_freqs * t)
    tab1.line_chart(signals, height=250)

    tab3.line_chart(signals.sum(axis=1), height=250)

def ani():
    plt.style.use('custom_dark_bg.mplstyle')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), layout='constrained')
        
    carrier_freqs = np.array([20e3, 22e3])  # Hz
    t = np.linspace(start=0, stop=1, num=2000).reshape(-1, 1)  # s
        
    line1, = ax1.plot([], [], label='Signal 1')
    line2, = ax1.plot([], [], label='Signal 2')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-2.5e-3, 2.5e-3)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude (A)')
    ax1.set_title('Individual Signals')
    ax1.legend(loc='upper right')
    ax1.grid(True)
        
    line3, = ax2.plot([], [], color='purple', alpha=0.7,label='Sum')
    envelope_upper, = ax2.plot([], [], color='white', label='Envelope')
    envelope_lower, = ax2.plot([], [], color='white')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-2.5e-3, 2.55e-3)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude (A)')
    ax2.set_title('Sum of Signals')
    ax2.legend(loc='upper right')
    ax2.grid(True)
        
    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        line3.set_data([], [])
        envelope_upper.set_data([], [])
        envelope_lower.set_data([], [])
        return line1, line2, line3, envelope_upper, envelope_lower
        
    def update(frame):
        ratio = frame / 200  # ratio from 0 to 1
        carrier_amplitudes = np.array([ratio, (1 - ratio)]) * 2e-3  # A
        signals = carrier_amplitudes * np.sin(2 * np.pi * carrier_freqs * t)
        summed_signal = signals.sum(axis=1)
        
        # Calculate envelope: amplitude modulation envelope
        delta_f = carrier_freqs[1] - carrier_freqs[0]  # Hz
        envelope = np.sqrt(
            carrier_amplitudes[0]**2
            + carrier_amplitudes[1]**2
            + 2 * carrier_amplitudes[0] * carrier_amplitudes[1]
            * np.cos(2 * np.pi * delta_f * t.flatten())
        )
            
        line1.set_data(t.flatten(), signals[:, 0])
        line2.set_data(t.flatten(), signals[:, 1])
        line3.set_data(t.flatten(), summed_signal)
        envelope_upper.set_data(t.flatten(), envelope)
        envelope_lower.set_data(t.flatten(), -envelope)
            
        return line1, line2, line3, envelope_upper, envelope_lower
        
    anim = FuncAnimation(fig, update, frames=401, init_func=init, blit=True, interval=50)
        
    writer = FFMpegWriter(fps=20)
    anim.save('amplitude_modulation.gif', writer=writer)

if __name__ == "__main__":
    if args.simulation == 'app':
        app()
    elif args.simulation == 'ani':
        ani()