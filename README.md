# Noise Analyzer Simulation Tool for PLCC

## Overview
The **Noise Analyzer Simulation Tool** is a Python-based project that models, analyzes, and visualizes the effect of noise on **Power Line Carrier Communication (PLCC)** systems. PLCC allows communication signals to travel over power lines, but these signals are often affected by mains hum (50 Hz), Gaussian noise, and impulse noise.  

This tool demonstrates how noise impacts signal quality, calculates performance metrics like **SNR** and **THD**, and shows how filtering (50 Hz notch filter) can improve communication reliability. It includes an interactive GUI built with **Streamlit** for real-time visualization and experimentation.

---

## Features
- Generate ASK-modulated PLCC signals.
- Add noise: 50 Hz mains hum, Gaussian noise, impulse spikes.
- Analyze in **time and frequency domains** using FFT and Welch PSD.
- Compute **SNR (broadband and band-limited)** and **Total Harmonic Distortion (THD)**.
- Apply a **50 Hz notch filter** and compare improvements.
- Interactive GUI for adjusting signal and noise parameters in real-time.
- Educational and research-oriented tool for understanding PLCC noise behavior.

---

## Project Structure

i will write this later
