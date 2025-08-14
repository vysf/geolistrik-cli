<p align="center">
<img src="https://raw.githubusercontent.com/vysf/geolistrik-cli/refs/heads/master/assets/geolistrik-cli-logo.png">
</p>

<!-- <h1 align="center">Geolistrik CLI</h1> -->
<p align="center">
    <a href="https://github.com/vysf/geolistrik-cli/releases/latest" alt="Latest Release" style="text-decoration:none;">
        <img src="https://img.shields.io/github/v/release/vysf/geolistrik-cli" />
    </a>
    <a href="https://github.com/vysf/geolistrik-cli/issues" alt="Open Issues" style="text-decoration:none;">
        <img src="https://img.shields.io/github/issues/vysf/geolistrik-cli" />
    </a>
    <a href="https://github.com/vysf/geolistrik-cli/blob/master/LICENSE" alt="License" style="text-decoration:none;">
        <img src="https://img.shields.io/github/license/vysf/geolistrik-cli" />
    </a>
    <a href="https://github.com/vysf/geolistrik-cli?tab=readme-ov-file#contributing" alt="Contributions" style="text-decoration:none;">
        <img src="https://img.shields.io/badge/contributions-welcome-brightgreen" />
    </a>
    <a href="https://github.com/vysf/geolistrik-cli/commits" alt="Last Commit" style="text-decoration:none;">
        <img src="https://img.shields.io/github/last-commit/vysf/geolistrik-cli" />
    </a>
</p>


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
- [Installation Guide](#installation-guide)
  - [Windows](#windows)
  - [Linux](#linux)
- [Usage Example](#usage-example)
   - [Generate Stacking Chart and Measurement Table](#generate-stacking-chart-and-measurement-table)
   - [Generate Only Measurement Tables](#generate-only-measurement-tables)
   - [Custom Output Directory](#custom-output-directory)
- [Local Development](#local-development)
- [Contributing](#contributing)

---

## Introduction

**Geolistrik CLI** is a command-line utility to generate **stacking charts** and **electrode configuration tables** for five common resistivity methods in geophysical survey:

- Wenner-Schlumberger (`ws`)
- Wenner (`wn`)
- Pole-Pole (`pp`)
- Pole-Dipole (`pd`)
- Dipole-Dipole (`dd`)

It saves outputs in `.png` (chart) and `.txt` (data) formats.

---

## Features

✅ Support 5 array types  
✅ CLI options: `--outdir`, `--no-plot`  
✅ Output: `.png` (chart), `.txt` (data)  
✅ Windows & Linux standalone builds  
✅ Easy to use for students, researchers, and engineers

---

## Installation Guide

### Windows

📦 [Download Installer](https://github.com/vysf/geolistrik-cli/releases)

1. Run the installer and follow the wizard.
2. After installation, add the install directory (e.g.):
   ```
   C:\Program Files\Geolistrik 1.0.0   
   ```
   to your [**system PATH**](https://www.bodhost.com/kb/how-to-add-to-the-path-on-windows-10-and-windows-11/) manually.
3. Open CMD and type:
   ```cmd
   geolistrik
   ```
   You'll see the welcome banner:
   ![welcome](docs/welcome-message.png)

4. To uninstall:
   - Use **Control Panel → Uninstall a Program**
   - Remove install path from [**system PATH**](https://www.bodhost.com/kb/how-to-add-to-the-path-on-windows-10-and-windows-11/)

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

## Usage Example

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

### Generate Stacking Chart and Measurement Table
By default, this command produces:
- Image file (`[config]_[min]_[max]_a[space].png`)
- Data table (`[config]_[min]_[max]_a[space].xlsx`)

Example:

```bash
geolistrik ws 0 100 10
```

### Generate Only Measurement Tables
Use `--no-plot` to disable chart generation:

```bash
geolistrik ws 0 100 10 --no-plot
```

### Custom Output Directory
Add `--outdir` to specify output folder:

```bash
geolistrik ws 0 100 10 --outdir "./results"
```

---

## Local Development

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

## Contributing

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
