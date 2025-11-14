# fit2csv

Convert multiple `.FIT` files into `.CSV` with a simple macOS GUI wrapper and a clean Python batch converter.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Platform](https://img.shields.io/badge/platform-macOS-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📚 Background

The idea for this project came from my own training routine. Over the years, my Apple Watch has logged more than 300 workouts, which I explore using the _HealthFit_ app. When I started playing with the idea of building an AI-based personal coach, I realized I needed all my previous workouts in a clean CSV format.

It turned out that no free tool existed for converting large batches of `.FIT` files to `.CSV`.  
So… I built one. With some help from AI.

It’s simple, but it works. And if it helps others too, that’s even better.

---

## 🚀 Features

- Batch convert `.FIT` → `.CSV`
- macOS GUI wrapper using Automator
- Automatic output folder creation (`csv_out`)
- Notifications on completion
- Opens output folder automatically
- Custom duotone runner icon
- Fully documented build instructions

---

## 📦 Installation (Download App)

Download the latest version here:

👉 **https://github.com/olefredrik/fit2csv/releases/latest**

Unzip, run the app, and select your folders.

---

## 🛠 Building the macOS App Yourself

If you want to build the Automator app locally or modify it:

See:  
📄 **[`mac-app/README_APP.md`](mac-app/README_APP.md)**

This document explains:

- How to embed the Python script
- How to apply the custom icon
- How to update `Info.plist`
- How to refresh macOS icon cache

---

## 🧩 Python Script (CLI Use)

If you prefer to run the converter directly:

```bash
pip install fitdecode
python3 src/fit2csv_batch.py <input_dir> --out <output_dir>
```

Example:

```bash
python3 src/fit2csv_batch.py ~/Downloads/FIT --out ~/Desktop/csv
```

---

## 📁 Repository Structure

```
fit2csv/
├── src/
│   └── fit2csv_batch.py
├── mac-app/
│   ├── README_APP.md
│   └── icon.icns
├── CHANGELOG.md
├── LICENSE
└── README.md
```

---

## 🧭 Roadmap

Planned / exploratory ideas:

- Improving the macOS GUI interface
- Optional settings for output naming
- Making the Automator wrapper more interactive

(See `CHANGELOG.md` for detailed version history.)

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open an issue or a pull request.

---

## 📄 License

MIT License.  
See **[`LICENSE`](LICENSE)** for details.

---

## 🎵 Bonus: A Completely Unnecessary Country Ballad

> **“Every good open source project needs documentation.  
> But only the _great_ ones need a heartfelt country love song.”**

Introducing ...

A _romantic_, _over-the-top_, _full-hearted love song_ about FIT-to-CSV conversion.

Complete with:

- acoustic guitar
- soft fiddle
- a man singing his feelings about batch conversion
- and a surprisingly catchy chorus

🎧 **Listen here:**  
👉 https://suno.com/s/Lf6rE0SjtJsMApv8

And yes, the song will get stuck in your head. Sorry. Not sorry.
