# Garuda Downloader

Garuda Downloader is a Python-based CLI utility that securely pulls internal tools from a private GitLab group repo. It supports split binary files (like `.zip`, `.z01`, `.z02`, and `.tar.zip`) and automatically extracts everything into a structured folder.

---

## 🔧 Features

- 🔐 GitLab authentication (username/password)
- 🧭 Interactive tool & version selection
- 📦 Handles:
  - Split zip archives (`.z01`, `.z02`, `.zip`)
  - Combined `.tar.zip` archives
  - Standalone `.exe` binaries
- 📂 Auto-extracts `.tar` after unzip if present
- 📁 Organizes output in `~/Downloads/<tool>/`
- 📄 Copies relevant PDFs from the `Doc/` folder

---

## 🛠️ Setup

### 1. Clone this repo

```bash
git clone https://github.com/yourusername/garuda-downloader.git
cd garuda-downloader
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Make sure `git` and `7z` are installed

Install 7-Zip (if not already installed):

```bash
sudo apt install p7zip-full  # Debian/Ubuntu
```

---

## 🚀 Usage

```bash
python3 garuda.py
```

You’ll be prompted to:

- Select a tool
- Choose a version (e.g. `v 2-0`, `v 2-0-1`)
- Enter your GitLab credentials

Extracted files will be saved in:  
`~/Downloads/<tool>/`

---

## 📁 Output Example

```
~/Downloads/
└── Antler/
    ├── dummy.bin
    ├── README.pdf
    ├── archive/
    │   ├── test_split.z01
    │   ├── test_split.z02
    │   └── test_split.zip
```

---

## 🧪 Notes

- Version folders can be named like `v 2-0`, `v_2-0`, `v 2-0-1`, etc.
- The script handles case-insensitive folder names like `/Bin` or `/bin`.
- If no valid zip or exe is found, a warning is shown.
- Archive components are preserved in an `archive/` subfolder.

---

## 📄 License

MIT License © 2025 Corey Hughes

---

## 📦 requirements.txt

```
requests
```
