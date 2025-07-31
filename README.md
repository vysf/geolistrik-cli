<p align="center">
<img src="https://raw.githubusercontent.com/vysf/geolistrik-cli/master/docs/icon.png" width="128">
</p>

<h1 align="center">Geolistrik CLI</h1>
<p align="center">
Generate geoelectrical stacking chart and observation tables from the terminal.
</p>

<p align="center">
<a href="https://github.com/vysf/geolistrik-cli/blob/master/README.md">English</a> |
<a href="https://github.com/vysf/geolistrik-cli/blob/master/docs/indonesian.md">Bahasa Indonesia</a>
</p>


---

## 📑 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Download & Install](#download--install)
  - [Windows](#windows)
  - [Linux](#linux)
- [CLI Usage](#cli-usage)
- [Development Guide](#development-guide)
- [Contribution](#contribution)

---

## Introduction

**Geolistrik CLI** is a command-line utility to generate **stacking charts** and **electrode configuration tables** for five common resistivity methods in geophysical survey:

- Wenner-Schlumberger (`ws`)
- Wenner (`wn`)
- Pole-Pole (`pp`)
- Pole-Dipole (`pd`)
- Dipole-Dipole (`dd`)

It saves outputs in `.png` (chart) and `.txt` (data) formats, with no Python runtime required.

---

## Features

✅ Support 5 array types  
✅ CLI options: `--outdir`, `--no-plot`  
✅ Output: `.png` (chart), `.txt` (data)  
✅ Windows & Linux standalone builds  
✅ Easy to use for students, researchers, and engineers

---

## Download & Install

### Windows

📦 [Download Installer](https://github.com/vysf/geolistrik-cli/releases)

1. Run the installer and follow the wizard.
2. After installation, add the install directory (e.g.):
   ```
   C:\Program Files\Geolistrik 1.0.0   
   ```
   to your **system PATH** manually.
3. Open CMD and type:
   ```cmd
   geolistrik
   ```
   You'll see the welcome banner:
   ![welcome](docs/welcome-message.png)

4. To uninstall:
   - Use **Control Panel → Uninstall a Program**
   - Remove install path from system environment if needed

---

### Linux

📦 [Download Linux binary](https://github.com/vysf/geolistrik-cli/releases)

```bash
chmod +x geolistrik-linux
sudo mv geolistrik-linux /usr/local/bin/geolistrik
```

Then use it anywhere:
```bash
geolistrik ws 0 100 10 --outdir results/
```

---

## CLI Usage

```bash
geolistrik [config] [min] [max] [spacing] [--outdir DIR] [--no-plot]
```

### Configuration Codes:

| Code | Configuration        |
|------|----------------------|
| ws   | Wenner-Schlumberger |
| wn   | Wenner              |
| pp   | Pole-Pole           |
| pd   | Pole-Dipole         |
| dd   | Dipole-Dipole       |

### Options:

| Option       | Description                                |
|--------------|--------------------------------------------|
| `--outdir`   | Set output directory for files             |
| `--no-plot`  | Skip plotting `.png`, just generate data   |
| `--version`  | Show app version                           |
| `--about`    | Show app metadata                          |

---

## Development Guide

1. Clone this repository:
   ```bash
   git clone https://github.com/vysf/geolistrik-cli
   cd geolistrik-cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run locally:
   ```bash
   python -m geolistrik --help
   ```

4. Build with Nuitka:
   See `build.bat` or use:

   ```bash
   nuitka --standalone --onefile --include-package=geolistrik --output-dir=build geolistrik/__main__.py
   ```

5. Compile Windows Installer:
   - Requires [Inno Setup](https://jrsoftware.org/isinfo.php)
   - Run:
     ```bash
     ISCC geolistrik_setup.iss
     ```

---

## Contribution

PRs are welcome!

### How to contribute:
- Fork this repository
- Commit changes to a branch
- Submit a pull request
- Or open an issue to report bugs/suggestions

---

📫 Contact: **Yusuf Umar Al Hakim**  
✉️ yusufumaralhakim@fmipa.untan.ac.id   
🌐 [GitHub Project](https://github.com/vysf/geolistrik-cli)
