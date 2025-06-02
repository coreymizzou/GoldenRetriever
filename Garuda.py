import os
import requests
import shutil
import zipfile
from bs4 import BeautifulSoup
from tqdm import tqdm
from difflib import get_close_matches

# Config
BASE_URL = "https://localsite.dev/corey/new"
DOWNLOAD_ROOT = "downloads"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

requests.packages.urllib3.disable_warnings()

def get_links(url):
    """Return list of (name, full_url) from a directory page."""
    try:
        r = requests.get(url, verify=False, headers=HEADERS)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing {url}: {e}")
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("/corey/new/"):
            full_url = f"https://localsite.dev{href}"
            name = href.rstrip("/").split("/")[-1]
            links.append((name, full_url))
    return links

def download_file(url, out_folder):
    """Download file from URL into specified folder with progress bar."""
    filename = url.split("/")[-1]
    local_path = os.path.join(out_folder, filename)
    os.makedirs(out_folder, exist_ok=True)

    with requests.get(url, stream=True, verify=False, headers=HEADERS) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(local_path, 'wb') as f, tqdm(
            desc=f"⬇️  {filename}",
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

    return local_path

def combine_split_zips(zip_parts, output_path):
    """Combine split zip parts into one."""
    with open(output_path, 'wb') as combined:
        for part in zip_parts:
            with open(part, 'rb') as pf:
                shutil.copyfileobj(pf, combined)
    print(f"🧩 Combined ZIP written to {output_path}")
    return output_path

def extract_zip(zip_path, extract_to):
    """Extract contents of a .zip archive."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"📦 Extracted: {zip_path} → {extract_to}")
    except zipfile.BadZipFile:
        print(f"❌ Error: {zip_path} is not a valid zip file.")

def process_version(tool_name, version_name):
    version_url = f"{BASE_URL}/{tool_name}/{version_name}"
    working_dir = os.path.join(DOWNLOAD_ROOT, tool_name, version_name.replace(" ", "_"))
    os.makedirs(working_dir, exist_ok=True)

    # BIN
    bin_url = f"{version_url}/bin"
    print(f"\n🔧 Getting binaries from: {bin_url}")
    bin_links = get_links(bin_url)
    bin_files = []

    for name, link in bin_links:
        if any(name.endswith(ext) for ext in ['.zip', '.z01', '.z02', '.z03']):
            path = download_file(link, working_dir)
            bin_files.append(path)

    if bin_files:
        bin_files.sort()
        output_zip = os.path.join(working_dir, f"{tool_name}_{version_name}_combined.zip")
        combine_split_zips(bin_files, output_zip)
        extract_zip(output_zip, working_dir)

    # DOC
    doc_url = f"{version_url}/doc"
    print(f"\n📚 Getting documentation from: {doc_url}")
    doc_links = get_links(doc_url)

    for name, link in doc_links:
        doc_path = download_file(link, working_dir)
        if doc_path.endswith(".zip"):
            extract_zip(doc_path, working_dir)

def fuzzy_input(prompt, options):
    """Allow fuzzy matching for user input."""
    raw = input(prompt).strip()
    matches = get_close_matches(raw, options, n=1, cutoff=0.3)
    return matches[0] if matches else None

def process_tool(tool_name):
    tool_url = f"{BASE_URL}/{tool_name}"
    print(f"\n🔎 Fetching versions for {tool_name}...")
    versions = get_links(tool_url)
    version_names = [name for name, _ in versions]

    if not version_names:
        print("⚠️ No versions found.")
        return

    print("\n📂 Available versions:")
    for i, name in enumerate(version_names):
        print(f"{i+1}: {name}")

    selected = fuzzy_input("\nEnter version to download (or leave blank for latest): ", version_names)
    if not selected:
        selected = sorted(version_names)[-1]
        print(f"🕐 No input given. Using latest version: {selected}")

    process_version(tool_name, selected)

def main():
    print("🔍 Fetching available tools...\n")
    tools = get_links(BASE_URL)
    tool_names = [name for name, _ in tools]

    if not tool_names:
        print("⚠️ No tools found.")
        return

    print("🧰 Available tools:")
    for i, name in enumerate(tool_names):
        print(f"{i+1}: {name}")

    selected = fuzzy_input("\nEnter tool name to download: ", tool_names)
    if not selected:
        print("❌ No valid tool selected.")
        return

    process_tool(selected)

if __name__ == "__main__":
    main()
