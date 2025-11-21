import streamlit as st
import pandas as pd
import numpy as np


tab1, tab3 = st.tabs(["Chart", "Interference"])


carrier_freqs = np.array([20e3, 22e3])  # Hz

ratio = st.slider("Current Ratio", 0.0, 1.0, 0.5)
carrier_amplitudes = np.array([ratio, (1 - ratio)]) * 2e-3  # A

t = np.linspace(start=0, stop=1, num=2000).reshape(-1, 1)  # s
signals = carrier_amplitudes * np.sin(2 * np.pi * carrier_freqs * t)
tab1.line_chart(signals, height=250)

tab3.line_chart(signals.sum(axis=1), height=250)
