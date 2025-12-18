# utils.py
# Reusable functions: signals, noises, FFT/PSD analysis, SNR, THD, notch filter

import numpy as np
from scipy.signal import iirnotch, filtfilt, welch


def time_vector(duration_s: float, fs: float) -> np.ndarray:
	"""Return a time vector for duration (seconds) sampled at fs (Hz)."""
	N = int(duration_s * fs)
	return np.linspace(0, duration_s, N, endpoint=False)


def carrier_wave(freq_hz: float, t: np.ndarray, amplitude: float = 1.0, phase: float = 0.0) -> np.ndarray:
	return amplitude * np.sin(2 * np.pi * freq_hz * t + phase)


def make_bitstream(num_bits: int) -> np.ndarray:
	return np.random.randint(0, 2, size=num_bits)


def ask_modulate(
	bits: np.ndarray,
	bit_rate: float,
	carrier_freq: float,
	t: np.ndarray,
	fs: float,
	amp_low: float = 0.0,
	amp_high: float = 1.0,
) -> np.ndarray:
	"""Simple ASK: map bits to amplitude (amp_low/amp_high). Robust to any bit_rate.

	Ensures the repeated bit sequence covers the entire time vector length.
	"""
	# Compute samples per bit using rounding to handle non-integer fs/bit_rate
	samples_per_bit = int(np.round(fs / float(bit_rate)))
	if samples_per_bit < 1:
		samples_per_bit = 1

	num_samples = len(t)
	# Ensure enough bits to cover all samples
	required_bits = int(np.ceil(num_samples / samples_per_bit))
	if bits is None or len(bits) == 0:
		bits = np.zeros(required_bits, dtype=int)
	elif len(bits) < required_bits:
		# Repeat last bit to reach required length
		pad_len = required_bits - len(bits)
		bits = np.concatenate([bits, np.full(pad_len, bits[-1], dtype=bits.dtype)])

	bit_samples = np.repeat(bits, samples_per_bit)
	# Trim to exactly match t length
	bit_samples = bit_samples[:num_samples]

	carrier = np.sin(2 * np.pi * carrier_freq * t)
	return carrier * (amp_low + (amp_high - amp_low) * bit_samples)


# ---------------- Noise models ----------------
def mains_noise(t: np.ndarray, amplitude: float = 0.5, mains_freq: float = 50.0) -> np.ndarray:
	return amplitude * np.sin(2 * np.pi * mains_freq * t)


def gaussian_noise(t: np.ndarray, sigma: float = 0.3) -> np.ndarray:
	return sigma * np.random.normal(size=len(t))


def impulse_noise(t: np.ndarray, num_impulses: int = 20, magnitude: float = 2.0, rng: np.random.Generator | None = None) -> np.ndarray:
	rng = rng or np.random.default_rng()
	x = np.zeros_like(t)
	positions = rng.integers(0, len(t), size=num_impulses)
	signs = rng.choice([-1.0, 1.0], size=num_impulses)
	x[positions] = signs * magnitude
	return x


# ---------------- Analysis ----------------
def compute_fft(signal: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
	N = len(signal)
	X = np.fft.fft(signal)
	freqs = np.fft.fftfreq(N, 1 / fs)
	half = N // 2
	return freqs[:half], np.abs(X[:half]) / N


def compute_psd(signal: np.ndarray, fs: float, nperseg: int = 1024) -> tuple[np.ndarray, np.ndarray]:
	f, Pxx = welch(signal, fs=fs, nperseg=nperseg)
	return f, Pxx


def compute_snr(clean_signal: np.ndarray, noisy_signal: np.ndarray) -> float:
	noise = noisy_signal - clean_signal
	signal_power = np.mean(clean_signal ** 2)
	noise_power = np.mean(noise ** 2)
	if noise_power == 0:
		return float("inf")
	return 10 * np.log10(signal_power / noise_power)


def compute_bandlimited_snr(
	clean_signal: np.ndarray,
	noisy_signal: np.ndarray,
	fs: float,
	center_freq_hz: float,
	bandwidth_hz: float,
) -> float:
	"""Compute SNR using only power within a frequency band around center.

	- Signal power: power of clean signal within [center - BW/2, center + BW/2]
	- Noise power: power of (noisy-clean) within the same band
	"""
	N = len(clean_signal)
	if len(noisy_signal) != N:
		raise ValueError("Signals must have same length for SNR computation")

	# FFTs
	C = np.fft.fft(clean_signal)
	E = np.fft.fft(noisy_signal - clean_signal)
	freqs = np.fft.fftfreq(N, 1.0 / fs)

	# Band mask (both positive and negative freqs)
	low = center_freq_hz - bandwidth_hz / 2.0
	high = center_freq_hz + bandwidth_hz / 2.0
	band_mask = ((freqs >= low) & (freqs <= high)) | ((freqs <= -low) & (freqs >= -high))

	signal_band_power = np.sum(np.abs(C[band_mask]) ** 2) / (N ** 2)
	noise_band_power = np.sum(np.abs(E[band_mask]) ** 2) / (N ** 2)
	if noise_band_power == 0:
		return float("inf")
	return 10.0 * np.log10(signal_band_power / noise_band_power)


def compute_thd(signal: np.ndarray, fs: float, fundamental_freq: float, n_harmonics: int = 5) -> tuple[float, float]:
	"""
	Estimate THD using FFT peaks: sqrt(sum(P_harmonics)/P_fundamental)
	Returns (ratio, dB)
	"""
	freqs, mag = compute_fft(signal, fs)
	power = mag ** 2
	idx_f = int(np.argmin(np.abs(freqs - fundamental_freq)))
	P_f = power[idx_f]
	P_h = 0.0
	for h in range(2, n_harmonics + 1):
		idx_h = int(np.argmin(np.abs(freqs - fundamental_freq * h)))
		P_h += float(power[idx_h])
	if P_f == 0:
		return float("nan"), float("nan")
	thd_ratio = float(np.sqrt(P_h / P_f))
	thd_db = 20 * np.log10(thd_ratio)
	return thd_ratio, float(thd_db)


# ---------------- Filters ----------------
def notch_filter(signal: np.ndarray, fs: float, notch_freq: float = 50.0, Q: float = 30) -> np.ndarray:
	"""IIR notch filter to remove mains frequency."""
	b, a = iirnotch(notch_freq, Q, fs)
	y = filtfilt(b, a, signal)
	return y

