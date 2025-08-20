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

It saves outputs in `.png` (chart) and `.xlsx` (data) formats.

---

## Features

✅ Support 5 array types  
✅ CLI options: `--outdir`, `--no-plot`  
✅ Output: `.png` (chart), `.xlsx` (data)  
✅ Windows & Linux standalone builds  
✅ Easy to use for students, researchers, and engineers

---

## Installation Guide

### Windows

📦 [Download Installer](https://github.com/vysf/geolistrik-cli/releases)

1. Run the installer and follow the instructions.
2. After the installation is complete, manually add the following folder:
   ```
   C:\Program Files (x86)\Geolistrik
   ```
   to your [**system PATH**](https://www.bodhost.com/kb/how-to-add-to-the-path-on-windows-10-and-windows-11/) manually. This the tutorial:   
   - Click Start, type "env", and select `Edit the system environment variables`
   ![system environment variables](/docs/search_env.png)
   - In the System Properties window, click the `Environment Variables…` button
   ![system properties](/docs/system_properties.png)
   - Under the System Variables section, find `Path` and click `Edit`
   ![system variable section](/docs/system_variable_section.png)
   - In the Edit Environment Variable window, click New to add a new path
   ![modify environtment variable](/docs/modify_environtment_variable_new.png)
   - Close all dialogue boxes by clicking `OK` to save your changes
   - Restart terminal to ensure the PATH changes take effect
3. Open CMD and type:
   ```cmd
   geolistrik
   ```
   You'll see the welcome banner:
   ![welcome](docs/welcome-message.png)

4. Uninstall:
   - Uninstall via **Control Panel → Uninstall a Program**
   - Remove the path entry from the [**system PATH**](https://www.bodhost.com/kb/how-to-add-to-the-path-on-windows-10-and-windows-11/)

---

### Linux

📦 [Download Linux binary](https://github.com/vysf/geolistrik-cli/releases)

1. Make the file executable   
For example, if the file is in the `~/Downloads` folder:
   ```bash
   chmod +x ~/Downloads/geolistrik-linux-1.0.0.bin
   ```

2. Move the file to a directory in your PATH
Typically this would be `~/.local/bin` (for local install) or `/usr/local/bin` (for global install).
   - Global installation (for all users):
      ```bash
      sudo mv ~/Downloads/geolistrik-linux-1.0.0.bin /usr/local/bin/geolistrik
      ```
   - Local installation (for current user only):
      First, ensure `~/.local/bin` is included in your `$PATH`. Check with:
      ```bash
      echo $PATH
      ```
      If it’s not included, add it to your `.bashrc` or `.zshrc`:
      ```bash
      echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
      source ~/.bashrc
      ```
      If it is already included, simply run:
      ```bash
      mkdir -p ~/.local/bin
      mv ~/Downloads/geolistrik-linux-1.0.0.bin ~/.local/bin/geolistrik
      ```
      Now you can use the CLI from anywhere:
      ```bash
      geolistrik
      ```
      Just like on Windows, you should see a welcome banner.
3. Uninstall   
   Simply delete the binary from your system:
   ```bash
   sudo rm /usr/local/bin/geolistrik
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
| `--update`   | Update app                                 |

### Generate Stacking Chart and Measurement Table
By default, this command produces:
- Image file (`[config]_[min]_[max]_a[space].png`)
- Data table (`[config]_[min]_[max]_a[space].xlsx`)

Example:

```bash
geolistrik ws 0 100 10
```
This is how the data acquisition process in the field corresponds to the table created:
![stacking_chart_animation](https://raw.githubusercontent.com/vysf/geolistrik-cli/refs/heads/master/docs/stacking_chart_animation.gif)


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
✉️ yusufumaralhakim@gmail.com   
🌐 [GitHub Project](https://github.com/vysf/geolistrik-cli)
