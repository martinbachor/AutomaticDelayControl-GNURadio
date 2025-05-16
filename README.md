# Automatic Delay Control in GNU Radio

[![GNU Radio](https://img.shields.io/badge/GNU%20Radio-3.10.9-blue)](https://www.gnuradio.org/)

A real-time delay detection and compensation system for GNU Radio, using cross-correlation in an embedded Python block.

## 🚀 Features
- 🎯 **Delay Detection**: Measures signal offset via cross-correlation
- 🔄 **Feedback Control**: Dynamically adjusts `gr.delay` via message passing
- 🛠️ **Interactive Calibration**: Start/reset buttons for user control
- 📊 **Noise Resilience**: Median filtering of delay measurements

## 🧰 Requirements
- GNU Radio 3.10+  
- Ubuntu 22.04+ (recommended)  

## 📁 Files
- `main.py` – Main GNU Radio block with cross-correlation logic   
- `AutomaticDelayControl.pdf` – Full project documentation

## 🔍 How It Works
The system compares two input signals and estimates the delay between them using cross-correlation.  
It then sends a control message to adjust the delay block dynamically, ensuring both signals stay aligned in real time.


## 📄 Documentation
For a deeper dive into implementation, mathematical background, and use cases, see:  
📘 `AutomaticDelayControl.pdf`

## 👤 Author
Created by [Martin Báchor]  
Project for [FEI STU / IPv6 and IoT]   
May 2025

