![Golden Retriever Logo](golden_retriever_logo.png)

# Golden Retriever

Golden Retriever is a Python-based CLI utility that securely pulls internal tools from a private GitLab group repo. It supports split binary files (like `.zip`, `.z01`, `.z02`, and `.tar.zip`) and automatically extracts everything into a structured folder.

---

## 🔧 Features

- GitLab authentication (username/password)
- Interactive tool & version selection
- Optionally include source code (`/Src`) in output
- Handles:
  - Split zip archives (`.z01`, `.z02`, `.zip`)
  - Combined `.tar.zip` archives
  - Standalone `.exe` binaries
- Auto-extracts `.tar` after unzip if present
- Organizes output in `~/Downloads/<tool>/`
- Copies relevant PDFs from `Doc/` folder

---

## 🛠 Setup

### 1. Clone this repo

```bash
git clone https://github.com/yourusername/golden-retriever.git
cd golden-retriever
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Make sure `git` and `7z` are installed

Install 7-Zip if needed:

```bash
sudo apt install p7zip-full  # Debian/Ubuntu
```

---

## 🚀 Usage

```bash
python3 golden_retriever.py
```

You’ll be prompted to:

- Select a tool
- Choose a version (e.g. `v 2-0`, `v 2-0-1`)
- Enter your GitLab credentials
- Choose whether to include the `/Src` directory in the output

All extracted files will be saved in `~/Downloads/<tool>`.

---

## 📁 Output Example

```
~/Downloads/
└── Antler/
    ├── dummy.bin
    ├── README.pdf
    ├── Src/                 # if chosen to include
    │   ├── source1.py
    │   └── source2.py
    ├── archive/
    │   ├── test_split.z01
    │   ├── test_split.z02
    │   └── test_split.zip
```

---

## 🧪 Notes

- The version folder format can be `v 2-0`, `v_2-0`, `v 2-0-1`, etc.
- The script is case-insensitive and supports `/Bin`, `/bin`, etc.
- If no zip or exe found, a warning is printed.
- All archive parts are preserved in an `archive/` subfolder.

---

## 📄 License

MIT License © 2025 Corey Hughes

---

### requirements.txt

```
requests
```
