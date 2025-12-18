# Noise Analysis and Filtering in PLCC – Simulation Tool

**Project Type:** Simulation & Signal Processing  
**Organization:** Chhattisgarh State Power Transmission Company Limited (CSPTCL)  
**Domain:** Power Line Carrier Communication (PLCC)

---
<img width="1765" height="892" alt="Screenshot 2025-09-15 182126" src="https://github.com/user-attachments/assets/aa025e16-e5f3-43a5-8eb5-d888e21ec901" />

<img width="1901" height="940" alt="Screenshot 2025-09-15 182035" src="https://github.com/user-attachments/assets/ec80a31e-1829-4322-88c4-a09154bf7f08" />

## 1. Introduction
Power Line Carrier Communication (PLCC) is a widely used technique for communication in power systems. It allows transmission of high-frequency communication signals over the same power lines that carry electrical energy, thus eliminating the need for dedicated cables.

While PLCC is cost-effective and robust, its performance is significantly influenced by noise such as mains hum (50 Hz), switching impulses, and background Gaussian noise [web:2]. These noise sources can degrade the quality of communication and impact protection signaling and load dispatch.

To address this issue, this project focuses on analyzing and mitigating noise in PLCC signals. A Python-based **Noise Analyzer Simulation Tool** was developed to model PLCC channels, visualize the impact of noise in both time and frequency domains, and demonstrate filtering techniques for improving signal-to-noise ratio (SNR).

This project serves as an educational and research tool that supports power system engineers in understanding and improving the quality of PLCC communication.

## 2. Company Overview
The project was carried out at **Chhattisgarh State Power Transmission Company Limited (CSPTCL), Raipur**, a leading organization responsible for power transmission and communication infrastructure in the state.

CSPTCL relies on PLCC for communication between substations and dispatch centers. However, maintaining high-quality PLCC communication is often challenged by the presence of noise on transmission lines. This project aligns with CSPTCL’s initiative to improve communication reliability by providing a simulation-based tool for analyzing and mitigating noise in PLCC signals.

## 3. Problem Statement
One of the major challenges in PLCC-based communication is noise interference from various sources such as mains frequency, switching impulses, and background Gaussian noise. These interferences:

- Reduce the Signal-to-Noise Ratio (SNR).
- Cause distortion in transmitted data and protection signals.
- Limit the efficiency and reliability of communication between substations.

To address these challenges, this project developed a **Noise Analyzer Simulation Tool** that:
1. Models PLCC signal transmission with noise.
2. Computes SNR and Total Harmonic Distortion (THD).
3. Demonstrates the effect of 50 Hz notch filtering in improving communication quality.

## 4. Title and Objective of the Project

### Title
**Noise Analysis and Filtering in PLCC – Simulation Tool**

### Objectives
- To simulate PLCC signal transmission using Amplitude Shift Keying (ASK).
- To introduce mains (50 Hz), Gaussian, and impulse noise into the channel.
- To analyze signal characteristics in time and frequency domains.
- To compute SNR and THD before and after filtering.
- To demonstrate the effectiveness of a 50 Hz notch filter in reducing noise.
- To provide an interactive Python-based GUI for visualization and experimentation.

## 5. Hardware and Software Requirements

### Hardware Requirements
- No specialized hardware was required for this project as it focused on simulation.
- *(Note: The approach can be extended to hardware testing using SDRs or Arduino-based PLCC modems.)*

### Software Requirements
- **Language:** Python 3.x
- **Libraries:**
  - `NumPy` & `SciPy` (signal processing and analysis)
  - `Matplotlib` (visualization of signals and spectra)
  - `Streamlit` (GUI development)
- **Environment:** Jupyter Notebook / VS Code

## 6. Development Process

### Requirement Analysis
Identified key noise sources affecting PLCC communication, specifically 50 Hz mains hum, Gaussian noise, and impulse spikes.

### Signal Generation
- Generated a clean **10 kHz carrier wave** with optional ASK modulation.
- Used a **100 kHz sampling frequency** for accurate digital representation.

### Noise Addition
Added synthetic 50 Hz mains hum, Gaussian random noise, and switching impulses to the clean signal to simulate real-world channel conditions.

### Analysis
- Performed **FFT (Fast Fourier Transform)** and **Welch PSD (Power Spectral Density)** to visualize spectral characteristics and noise distribution.
- Computed **SNR** (broadband and band-limited) and **THD** (Total Harmonic Distortion).

### Filtering
- Applied a **50 Hz notch filter (Q = 30)** to specifically reduce mains interference.
- Measured the quantitative improvement in SNR after filtering.

### Tool Development
- **`utils.py`**: Organized core signal processing functions.
- **`simulation.py`**: Built static simulations for testing.
- **`app.py`**: Designed an interactive GUI using **Streamlit** with sliders for real-time parameter adjustments.

## 7. Snapshots
*(Placeholder for project images)*
- **Time-domain plots:** Visual comparison of clean vs. noisy signals.
- **Frequency-domain plots:** FFT and PSD graphs showing distinct noise peaks.
- **Comparison charts:** SNR values before and after filtering.
- **GUI Screenshot:** Interface of the Streamlit-based Noise Analyzer Tool.

## 8. Conclusion
The project successfully demonstrated that noise significantly affects the quality of PLCC communication and that applying appropriate filtering techniques can lead to substantial improvement in SNR and overall reliability.

The Python-based **Noise Analyzer Tool** proved to be an effective educational and research platform for understanding noise behavior in PLCC channels. The results highlight the importance of targeted signal processing in enhancing the performance of PLCC systems used in power grids.

## 9. Future Enhancements
- Extend the tool to include **FSK** and **PSK** modulation schemes.
- Implement **BER (Bit Error Rate) vs SNR** analysis for communication performance.
- Integrate with hardware platforms (**SDRs**, **Arduino**) for real-world validation.
- Use **machine learning-based noise classifiers** for adaptive filtering.
- Automate reporting and provide an advanced dashboard for researchers and students.

## 10. Bibliography
1. Bruce Carlson, *Communication Systems: An Introduction to Signals and Noise in Electrical Communication*.
2. *IEEE Transactions on Power Delivery and Communication Systems*.
3. IEC Standards for PLCC (IEC 60495, IEC 60870).
4. Documentation for Python libraries (NumPy, SciPy, Matplotlib, Streamlit).
5. Chhattisgarh State Power Transmission Co. Ltd. (CSPTCL) field knowledge and training experience.
