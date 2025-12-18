# app.py
# Run: streamlit run app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import (
	time_vector, ask_modulate, carrier_wave,
	mains_noise, gaussian_noise, impulse_noise,
	compute_fft, compute_psd, compute_snr, compute_bandlimited_snr, notch_filter,
)


st.title("Power Line Channel Noise Analyzer (Simulation)")

# UI controls
fs = st.sidebar.number_input("Sampling Rate (Hz)", value=100_000, step=1000)
duration = st.sidebar.number_input("Duration (s)", value=0.02, format="%.3f")
carrier_freq = st.sidebar.slider("Carrier Freq (Hz)", 1000, 20000, 10000)
use_data = st.sidebar.checkbox("Use ASK data", value=True)
bit_rate = st.sidebar.number_input("Bit rate (bps)", value=1000)
mains_amp = st.sidebar.slider("Mains amplitude", 0.0, 2.0, 0.5)
gauss_sigma = st.sidebar.slider("Gaussian sigma", 0.0, 1.0, 0.2)
impulses = st.sidebar.slider("Number of impulses", 0, 100, 20)
imp_mag = st.sidebar.slider("Impulse magnitude", 0.0, 5.0, 2.0)

t = time_vector(duration, fs)
if use_data:
	np.random.seed(0)
	# Generate at least enough bits to cover the time length after upsampling
	approx_bits_needed = int(np.ceil(duration * bit_rate))
	bits = np.random.randint(0, 2, max(1, approx_bits_needed))
	clean = ask_modulate(bits, bit_rate, carrier_freq, t, fs, amp_low=0.1, amp_high=1.0)
else:
	clean = carrier_wave(carrier_freq, t)

noisy = (
	clean
	+ mains_noise(t, amplitude=mains_amp)
	+ gaussian_noise(t, sigma=gauss_sigma)
	+ impulse_noise(t, num_impulses=impulses, magnitude=imp_mag)
)

snr_db = compute_snr(clean, noisy)
bl_snr_db = compute_bandlimited_snr(clean, noisy, fs, carrier_freq, bandwidth_hz=2000)
st.write(f"Estimated SNR (broadband): **{snr_db:.2f} dB**  | Band-limited: **{bl_snr_db:.2f} dB**")

# plots
fig, ax = plt.subplots(2, 1, figsize=(8, 6))
win = int(0.004 * fs)
ax[0].plot(t[:win] * 1000, clean[:win], label="Clean")
ax[0].plot(t[:win] * 1000, noisy[:win], label="Noisy", alpha=0.7)
ax[0].set_xlabel("Time (ms)")
ax[0].legend()

freqs_n, mag_n = compute_fft(noisy, fs)
freqs_noise, mag_noise = compute_fft(noisy - clean, fs)
eps = 1e-12
ax[1].plot(freqs_n, 20 * np.log10(mag_n + eps), label="Noisy (dB)")
ax[1].plot(freqs_noise, 20 * np.log10(mag_noise + eps), label="Noise-only (dB)", alpha=0.7)
ax[1].axvline(50, color="r", linestyle=":", alpha=0.6, label="50 Hz")
ax[1].axvline(carrier_freq, color="g", linestyle=":", alpha=0.6, label=f"Carrier {carrier_freq} Hz")
ax[1].set_xlim(0, 20000)
ax[1].set_xlabel("Frequency (Hz)")
ax[1].legend(loc="best")

st.pyplot(fig)

if st.button("Apply 50 Hz notch filter and re-evaluate"):
	filtered = notch_filter(noisy, fs, notch_freq=50.0, Q=30)
	st.write(
		f"After notch — Broadband: **{compute_snr(clean, filtered):.2f} dB**, "
		f"Band-limited: **{compute_bandlimited_snr(clean, filtered, fs, carrier_freq, 2000):.2f} dB**"
	)
	fig2, ax2 = plt.subplots(1, 1, figsize=(8, 3))
	freqs_f, mag_f = compute_fft(filtered, fs)
	ax2.plot(freqs_f, 20 * np.log10(mag_f + 1e-12))
	ax2.set_xlim(0, 20000)
	st.pyplot(fig2)

