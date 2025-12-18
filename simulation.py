# simulation.py
# Runs a simulation: generates a carrier + optional ASK data, adds noises, calculates metrics, and plots.

import numpy as np
import matplotlib.pyplot as plt
from utils import (
	time_vector, carrier_wave, ask_modulate,
	mains_noise, gaussian_noise, impulse_noise,
	compute_fft, compute_psd, compute_snr, compute_bandlimited_snr, compute_thd, notch_filter,
)


def run_example() -> None:
	np.random.seed(0)
	fs = 100_000
	duration = 0.02
	t = time_vector(duration, fs)

	carrier_freq = 10_000
	use_data = True
	bit_rate = 1000

	if use_data:
		bits = np.random.randint(0, 2, int(bit_rate * duration))
		clean = ask_modulate(bits, bit_rate, carrier_freq, t, fs, amp_low=0.1, amp_high=1.0)
	else:
		clean = carrier_wave(carrier_freq, t)

	mains = mains_noise(t, amplitude=0.5, mains_freq=50.0)
	gauss = gaussian_noise(t, sigma=0.2)
	impulses = impulse_noise(t, num_impulses=25, magnitude=2.0)

	noisy = clean + mains + gauss + impulses

	snr_db = compute_snr(clean, noisy)
	# Band-limited SNR around carrier (e.g., 2 kHz bandwidth)
	bl_snr_db = compute_bandlimited_snr(clean, noisy, fs, carrier_freq, bandwidth_hz=2000)
	thd_ratio, thd_db = compute_thd(clean, fs, carrier_freq, n_harmonics=6)

	print(f"SNR (clean vs noisy): {snr_db:.2f} dB")
	print(f"Band-limited SNR (~2 kHz): {bl_snr_db:.2f} dB")
	print(f"THD (of clean approx): ratio={thd_ratio:.4f}, {thd_db:.2f} dB")

	freqs_clean, mag_clean = compute_fft(clean, fs)
	freqs_noisy, mag_noisy = compute_fft(noisy, fs)
	# Noise-only spectrum helps reveal low-level components next to a strong carrier
	freqs_noise, mag_noise = compute_fft(noisy - clean, fs)

	f_psd, Pxx = compute_psd(noisy, fs)

	plt.figure(figsize=(12, 8))
	plt.subplot(3, 1, 1)
	plt.title("Time domain (first 4 ms)")
	window_samples = int(0.004 * fs)
	plt.plot(t[:window_samples] * 1000, clean[:window_samples], label="Clean")
	plt.plot(t[:window_samples] * 1000, noisy[:window_samples], label="Noisy", alpha=0.7)
	plt.xlabel("Time (ms)")
	plt.legend()

	plt.subplot(3, 1, 2)
	plt.title("Frequency Spectrum (dB)")
	eps = 1e-12
	plt.plot(freqs_clean, 20 * np.log10(mag_clean + eps), label="Clean (dB)")
	plt.plot(freqs_noisy, 20 * np.log10(mag_noisy + eps), label="Noisy (dB)", alpha=0.7)
	plt.plot(freqs_noise, 20 * np.log10(mag_noise + eps), label="Noise-only (dB)", alpha=0.7)
	plt.xlim(0, 20000)
	plt.xlabel("Frequency (Hz)")
	# Annotate mains and carrier
	plt.axvline(50, color="r", linestyle=":", alpha=0.6, label="50 Hz")
	plt.axvline(carrier_freq, color="g", linestyle=":", alpha=0.6, label=f"Carrier {carrier_freq} Hz")
	plt.legend(loc="best")

	plt.subplot(3, 1, 3)
	plt.title("PSD (Welch)")
	plt.semilogy(f_psd, Pxx)
	plt.xlim(0, 20000)
	plt.xlabel("Frequency (Hz)")

	plt.tight_layout()
	plt.show()

	filtered = notch_filter(noisy, fs, notch_freq=50.0, Q=30)
	print("SNR after notch (broadband):", compute_snr(clean, filtered))
	print("SNR after notch (band-limited):", compute_bandlimited_snr(clean, filtered, fs, carrier_freq, bandwidth_hz=2000))


if __name__ == "__main__":
	run_example()

