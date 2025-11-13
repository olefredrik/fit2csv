# fit2csv

<p align="left">
  <a href="https://github.com/olefredrik/fit2csv/releases/latest">
    <img src="https://img.shields.io/github/v/release/olefredrik/fit2csv?label=Latest%20Release&color=2ea44f" />
  </a>
  <img src="https://img.shields.io/badge/Platform-macOS-blue" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
  <img src="https://img.shields.io/github/downloads/olefredrik/fit2csv/total?label=Downloads" />
  <img src="https://img.shields.io/badge/Python-3.x-blue" />
</p>

A simple open-source tool for batch converting `.FIT` files (Garmin, Polar, Wahoo, etc.) into `.CSV` files.

This project contains:

- A **Python script** (`fit2csv_batch.py`) that performs the actual FIT → CSV conversion
- A **macOS Automator application** (optional) that provides a simple GUI and wraps the Python script
- Documentation on how to build the macOS app

The goal is to provide a minimal, reliable, and flexible tool for anyone who wants to work with their own training data.

---

## ✨ Features

- Convert entire folders of `.fit` files to `.csv`
- Preserve original filenames
- Output folder selection (or automatic `csv_out` folder)
- macOS Automator app:
  - Choose input/output folders via GUI
  - Shows a “Conversion finished” notification
  - Opens output folder automatically
  - Embeds the Python script inside the `.app` bundle

---

## 📦 Repository Structure

```text
fit2csv/
│
├── src/
│   └── fit2csv_batch.py          # Main Python conversion script
│
├── mac-app/
│   └── README_APP.md             # Instructions to build the Automator app
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🐍 Python Script

The main script lives in:

```
src/fit2csv_batch.py
```

It expects:

- an **input folder** containing `.fit` files
- an **output folder** (created automatically if missing)

### Example usage:

```bash
python3 src/fit2csv_batch.py /path/to/fit-files --out /path/to/output
```

### Requirements

Install dependencies:

```bash
pip install fitdecode
```

---

## 🍏 macOS Application (optional)

The Automator application wraps the Python script and allows you to:

- Select input folder
- Select output folder
- Run the conversion without using Terminal

### Building the macOS app yourself

See:

```
mac-app/README_APP.md
```

This explains how to:

- embed `fit2csv_batch.py` inside the `.app`
- use an AppleScript wrapper to call the Python script
- build your own standalone `fit2csv.app`

The Automator app **is not stored directly in this repository** (best practice).  
Instead, you can download prebuilt versions via **GitHub Releases**.

---

## 🛠 Planned improvements

- Windows and Linux packaging
- Optional progress output
- Native Python GUI version (Tkinter / PyQt)
- FIT → Parquet support
- Better error handling and logging

Pull requests are welcome!

---

## 📝 License

This project is released under the **MIT License**.  
See [`LICENSE`](LICENSE) for full text.

---

## 👤 Author

Ole Fredrik Lie  
GitHub: https://github.com/olefredrik

---

## 💬 Feedback / Contributions

Pull requests and issues are welcome! If you build something cool on top of this tool — GUI, CLI enhancements, better FIT parsing — please consider contributing it back.
