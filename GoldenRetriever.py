import os
import re
import subprocess
import shutil
from getpass import getpass
from urllib.parse import quote
import requests

# Config
GITLAB_URL = "http://gitlab.local"
GITLAB_API = f"{GITLAB_URL}/api/v4"
GROUP_PATH = "corey/tools"
PRIVATE_TOKEN = "glpat-f99FG_hTyQpyUqKhLxZo"
DOWNLOAD_ROOT = os.path.join(os.path.expanduser("~"), "Downloads")
TMP_CLONE_PATH = "/tmp/garuda_clone"

# Suppress insecure warnings
requests.packages.urllib3.disable_warnings()

HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

def get_json(url):
    response = requests.get(url, headers=HEADERS, verify=False)
    response.raise_for_status()
    return response.json()

def list_projects():
    print("\U0001F4E1 Fetching list of tools...\n")
    url = f"{GITLAB_API}/groups/{quote(GROUP_PATH, safe='')}/projects?per_page=100"
    projects = get_json(url)
    return [proj['name'] for proj in projects]
    #proj_list.sort(lambda a: a['name'])     where proj_list is a list of dictionaries

def choose(prompt, options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    idx = int(input(f"\n{prompt} (1-{len(options)}): ")) - 1
    return options[idx]

def find_versions(project_path):
    versions = []
    for entry in os.listdir(project_path):
        if os.path.isdir(os.path.join(project_path, entry)) and re.match(r'^v[\s\d\-_.]+$', entry, re.IGNORECASE):
            versions.append(entry)
    return sorted(versions)

def combine_and_extract(bin_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    bin_files = os.listdir(bin_path)

    # Identify split zip parts and full zip
    zips = [f for f in bin_files if re.search(r'\.z\d{2,3}$', f)]
    main_zip = next((f for f in bin_files if f.endswith('.zip')), None)

    if zips and main_zip:
        print(f"\n\U0001F527 Extracting split archive from: {main_zip} with parts {zips}\n")
        zip_path = os.path.join(bin_path, main_zip)

        # Test archive
        test_result = subprocess.run(["7z", "t", zip_path], capture_output=True, text=True)
        if test_result.returncode != 0:
            print("\n❌ Archive test failed:")
            print(test_result.stdout + test_result.stderr)
            return

        # Extract archive
        subprocess.run(["7z", "x", zip_path, f"-o{output_folder}"], check=True)

        # Extract .tar files if needed
        for item in os.listdir(output_folder):
            if item.endswith(".tar"):
                subprocess.run(["7z", "x", os.path.join(output_folder, item), f"-o{output_folder}"], check=True)

        # Move parts to archive folder
        archive_dir = os.path.join(output_folder, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        for f in [main_zip] + zips:
            shutil.copy(os.path.join(bin_path, f), archive_dir)

    elif main_zip:
        print(f"\n\U0001F527 Extracting standalone zip: {main_zip}\n")
        zip_path = os.path.join(bin_path, main_zip)

        test_result = subprocess.run(["7z", "t", zip_path], capture_output=True, text=True)
        if test_result.returncode != 0:
            print("\n❌ Archive test failed:")
            print(test_result.stdout + test_result.stderr)
            return

        subprocess.run(["7z", "x", zip_path, f"-o{output_folder}"], check=True)

        for item in os.listdir(output_folder):
            if item.endswith(".tar"):
                subprocess.run(["7z", "x", os.path.join(output_folder, item), f"-o{output_folder}"], check=True)

        archive_dir = os.path.join(output_folder, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        shutil.copy(zip_path, archive_dir)

    else:
        for f in bin_files:
            if f.endswith(".exe"):
                shutil.copy(os.path.join(bin_path, f), output_folder)
                return
        print("\n⚠ No valid zip or exe found to extract.\n")

def copy_docs(doc_path, output_folder):
    for f in os.listdir(doc_path):
        if f.endswith(".pdf"):
            shutil.copy(os.path.join(doc_path, f), output_folder)

def main():
    projects = list_projects()
    project = choose("Select a tool", projects)

    if os.path.exists(TMP_CLONE_PATH):
        shutil.rmtree(TMP_CLONE_PATH, ignore_errors=True)

    print(f"\n\U0001F9E0 Cloning {project} from GitLab (shallow)...")
    username = input("Username for GitLab: ")
    password = getpass("Password: ")

    subprocess.run([
        "git", "clone", "--depth", "1",
        f"http://{username}:{password}@gitlab.local/{GROUP_PATH}/{project}.git",
        TMP_CLONE_PATH
    ], check=True)

    versions = find_versions(TMP_CLONE_PATH)
    if not versions:
        print(f"\n⚠  No version folders found for '{project}'.")
        return

    version = choose("Select a version", versions)

    bin_path = os.path.join(TMP_CLONE_PATH, version, "Bin")
    doc_path = os.path.join(TMP_CLONE_PATH, version, "Doc")
    dest_folder = os.path.join(DOWNLOAD_ROOT, project)
    include_src = input("Include source files from /Src directory? (y/N): ").strip().lower() == 'y'

    combine_and_extract(bin_path, dest_folder)
    copy_docs(doc_path, dest_folder)

    if include_src:
    src_path = os.path.join(TMP_CLONE_PATH, version, "Src")
    dest_src_path = os.path.join(dest_folder, "Src")
    if os.path.exists(src_path):
        shutil.copytree(src_path, dest_src_path, dirs_exist_ok=True)
    else:
        print("⚠️  No /Src directory found.")

    shutil.rmtree(TMP_CLONE_PATH, ignore_errors=True)

    print(f"\n✅ Done! Files available at: {dest_folder}")

if __name__ == "__main__":
    main()
