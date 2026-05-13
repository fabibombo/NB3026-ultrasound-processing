# README – Biomolecular Imaging Lab: Ultrasound Contrast Analysis

This repository contains a Jupyter notebook for analyzing ultrasound phantom data. The notebook guides you through processing raw ultrasound data, computing contrast-to-noise ratio (CNR) for gas vesicle (GV) contrast agents, and evaluating collapse pressure measurements.

## Learning Goals

1. Understand how an ultrasound (US) image is formed from raw beamformed data.
2. Quantify the level of contrast produced by GV contrast agents using CNR analysis.

---

## Prerequisites

You need a Python 3 environment with the required packages. Two recommended ways to set it up:

### Option 1: Using `uv` (fast, recommended)

```bash
# Install uv (if not already installed)
pip install uv

# Create environment and install dependencies
uv venv
uv pip install -r requirements.txt
```

### Option 2: Using `venv` + `pip`

```bash
# Create virtual environment
python -m venv biomol_env

# Activate it (Linux/Mac)
source biomol_env/bin/activate
# Or on Windows:
# biomol_env\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

After setting up the environment, you can launch the notebook:

```bash
jupyter notebook lab_ultrasound.ipynb
```

> **Note:** Keep the data files located in a `data/` subfolder. Adjust paths if needed.

---

## Task Checklist

### 0. Open the Jupyter Notebook

Launch the notebook as described above. The notebook is pre‑filled with code stubs; your task is to complete and execute them.

### 1. Load Phantom Data (Observe Nonlinear Signal in AM)

Load the raw ultrasound phantom data. The data contains signals acquired in **Amplitude Modulation (AM)** and **Brightness (B)** mode.

### 2. Envelope Detection of the Phantom Data

Compute the **envelope** of the complex beamformed data. This step extracts the magnitude of the ultrasound echoes.

### 3. Convert to dB Scale (see Lecture 2, slide 30)

Convert the envelope data to **decibels (dB)**. Refer to slide 30 of Lecture 2 for formula.

### 4. Compute Contrast-to-Noise Ratio (CNR) of the GV Wells

For each GV well, define a **region of interest (ROI)** inside the well and a **background region** outside the well. Then calculate CNR.

### 5. Plot CNR vs. Voltage for Each Well

Create a scatter or line plot showing **CNR** (y‑axis) against **transmit voltage** (x‑axis) for each individual well.

### 6. Compare Wild Type and Stripped GV Curves in One Plot

Overlay the CNR‑vs‑Voltage curves for **Wild Type (WT)** GVs and **Stripped (ST)** GVs on the same plot.

### 7. Load Excel Data and Find Hydrostatic Collapse Pressure

Load the provided Excel file containing collapse measurements for each GV sample. For each sample, determine the **hydrostatic collapse pressure** – the pressure at which the GV population collapses. Plot the collapse curves and annotate the collapse pressure values.