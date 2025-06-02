# Garuda# 🦅 Garuda

**Garuda** is a fast, intelligent Python utility for interactively downloading, combining, and extracting versioned binaries and documentation from a self-hosted GitLab repository.

Inspired by _Garuda_, the mighty bird-like being and mount of Vishnu in Hindu mythology, this tool embodies **speed, strength, and precision** — fetching your tools like a divine courier from the digital heavens.

---

## ✨ Features

- 🔍 **Fuzzy search** for tool and version names (e.g., "ant" matches "Antler")
- 🕐 **Auto-selects latest version** if left blank
- 📦 **Combines multipart `.zip`, `.z01`, `.z02` files**
- 📚 **Downloads and extracts `.pdf` and `.zip` documentation**
- 📊 **Progress bars** for downloads with `tqdm`
- 📂 **Organized output structure** per tool and version

---

## 📁 Expected GitLab Structure

```
https://localsite.dev/corey/new/
├── Antler/
│   ├── v 2-0/
│   │   ├── bin/
│   │   │   ├── Antler.z01
│   │   │   ├── Antler.z02
│   │   │   ├── Antler.zip
│   │   └── doc/
│   │       ├── guide.pdf
│   │       ├── examples.zip
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/garuda.git
cd garuda
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧑‍💻 Usage

```bash
python garuda.py
```

You'll be prompted to:

1. **Select a tool** (e.g., `Antler`)
2. **Select a version** (e.g., `v 2-0`, or press Enter to use the latest)
3. Garuda will:
   - Download and combine `.z01`, `.z02`, `.zip` from `/bin`
   - Extract the combined archive
   - Download and extract documentation files from `/doc`

---

## 📂 Output Structure

```bash
downloads/
└── Antler/
    └── v_2-0/
        ├── Antler.z01
        ├── Antler.z02
        ├── Antler.zip
        ├── Antler_v 2-0_combined.zip
        ├── guide.pdf
        ├── examples.zip
        ├── [extracted binaries]
        └── [extracted docs]
```

---

## ⚙️ Configuration

Update these variables in `garuda.py` to match your environment:

```python
BASE_URL = "https://localsite.dev/corey/new"
DOWNLOAD_ROOT = "downloads"
```

---

## 🦅 Why "Garuda"?

> In Hindu mythology, **Garuda** is the eagle-like mount of Lord Vishnu — a symbol of **strength, vigilance, and speed**.  
> This tool, like its namesake, flies fast, strikes precisely, and delivers your payloads without fail.

---

## 📜 License

MIT License — use it freely, improve it boldly.

---

## 🤝 Contribute or Ask Questions

Open an issue or submit a pull request — we welcome contributions and suggestions.
