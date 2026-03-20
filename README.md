# 🔍 OSINT Developer Footprint Scanner

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f538d.svg?style=for-the-badge&logo=python&logoColor=white)
![OSINT](https://img.shields.io/badge/Category-OSINT-e74c3c.svg?style=for-the-badge)
![Requests](https://img.shields.io/badge/HTTP-Requests-2ecc71.svg?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

A powerful **OSINT (Open Source Intelligence)** desktop tool that scans multiple platforms to check whether a username exists across the internet.

Built using **Python + CustomTkinter**, this tool helps you quickly map a developer’s or user's digital footprint across coding platforms, social media, and more.

---

## 🚀 Features

* 🔎 **Cross-Platform Username Search**
* ⚡ **Multithreaded Scanning** (fast results)
* 📊 **Real-time Progress Tracking**
* 🎯 **Category-based Filtering**
* 🌙 **Dark / Light Mode Toggle**
* 🔗 **Direct Profile Access (Open in Browser)**
* 💾 **Export Results (CSV / JSON)**
* 🧠 **Smart Detection (avoids false positives & soft 404s)**

---

## 🌐 Supported Platforms

### 👨‍💻 Coding

* Codeforces
* LeetCode
* CodeChef
* AtCoder
* HackerRank
* TopCoder
* SPOJ
* PyPI

### 🗂 Version Control

* GitHub
* GitLab
* DockerHub
* Replit

### 🤖 AI / ML

* Kaggle
* HuggingFace

### ✍️ Blogging

* Medium
* Dev.to
* Hashnode

### 🎮 Gaming

* Steam
* Chess.com
* Lichess

### 📱 Social Media

* Instagram
* Twitter
* Reddit
* Pinterest

### 🔐 Cybersecurity

* TryHackMe

---

## 🖥️ UI Preview

> Clean, modern UI built with **CustomTkinter**

* Scrollable results panel
* Color-coded status:

  * ✅ Found
  * ❌ Not Found

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/footprint-scanner.git
cd footprint-scanner
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install customtkinter requests
```

---

## ▶️ Usage

Run the application:

```bash
python main.py
```

### Steps:

1. Enter a username
2. Click **"Scan Network"**
3. View results in real-time
4. Filter by category (optional)
5. Export results if needed

---

## 🧠 How It Works

* Uses **HTTP requests + platform-specific APIs** where possible
* Applies:

  * Status code checks
  * URL validation
  * Soft 404 detection
* Runs scans concurrently using:

  * `ThreadPoolExecutor`

---

## 📁 Export Format

### CSV / JSON includes:

* Platform
* Category
* Exists (Yes/No)
* Profile URL

---

## ⚠️ Disclaimer

This tool is intended for:

* Educational purposes
* Ethical OSINT investigations

❗ Do **not** use it for:

* Harassment
* Stalking
* Privacy violations

Always respect platform policies and user privacy.

---

## 🛠️ Tech Stack

* Python 🐍
* CustomTkinter 🎨
* Requests 🌐
* Concurrent Futures ⚡

---

## 💡 Future Improvements

* 🔍 Email / phone OSINT support
* 📊 Analytics dashboard
* 🌍 Proxy / Tor support
* 🧾 Report generation (PDF)
* 🔔 Notifications for matches

---
