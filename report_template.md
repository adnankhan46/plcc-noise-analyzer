## Power Line Channel Noise Analyzer – Report

### Abstract
Briefly describe the goal: simulate a PLCC-like channel, add common noise sources, analyze in time/frequency domains, and compute metrics (SNR, THD, PSD). Provide both script and interactive UI.

### Background
- Power line communications and typical noise sources (mains hum, switching impulses, thermal noise).
- Why analyze: link reliability, bandwidth planning, filter design.

### Methodology
1. Signal generation: carrier at 10 kHz; optional ASK at 1 kbps.
2. Noise models: 50 Hz sinusoidal, Gaussian, random impulses.
3. Sampling: fs=100 kHz, duration ~20 ms.
4. Analysis: FFT magnitude, Welch PSD, SNR, THD.
5. Mitigation: IIR notch filter at 50 Hz.

### Results
- Time-domain snapshots showing clean vs noisy.
- Spectrum highlighting carrier and mains components.
- PSD curves; SNR values before/after notch.
- THD estimate of the clean signal.

### Discussion
- Effects of each noise type and parameter sensitivity.
- Limitations: simple impulse model, finite-length FFT leakage, no channel frequency response modeling.
- Extensions: 60 Hz mains, windowing, FSK/PSK, multi-tone interference, realistic impulsive noise (Bernoulli-Gaussian), adaptive filtering.

### Conclusion
Summarize findings and potential next steps.

### How to Run
Include the basic commands to create venv, install, and run `simulation.py` or `streamlit run app.py`.

