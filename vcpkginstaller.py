import os
import subprocess
import platform
import urllib.request
import tempfile
import shutil
import json

def run_command(command):
    """Run a command and print output."""
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        return False
    return True

def check_git():
    """Check if Git is installed and functioning."""
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Git is installed: {result.stdout.strip()}")
            return True
        else:
            print("Git is not installed or not functioning correctly.")
            return False
    except FileNotFoundError:
        print("Git is not installed.")
        return False

def install_git():
    """Install or upgrade Git."""
    os_name = platform.system()

    if os_name == "Windows":
        print("Attempting to install or upgrade Git on Windows using winget...")
        if not run_command("winget install --id Git.Git -e --source winget"):
            print("winget failed. Attempting to download and install Git manually...")
            download_and_install_git_windows()
    elif os_name == "Linux":
        print("Attempting to install or upgrade Git on Linux...")
        run_command("sudo apt-get update")
        run_command("sudo apt-get install git -y")
    elif os_name == "Darwin":
        print("Attempting to install or upgrade Git on macOS...")
        run_command("brew install git")
    else:
        print("Unsupported OS. Please install Git manually.")
        exit(1)

def get_latest_git_installer_url():
    """Get the latest Git for Windows installer URL."""
    api_url = "https://api.github.com/repos/git-for-windows/git/releases/latest"
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            assets = data.get("assets", [])
            for asset in assets:
                if "64-bit.exe" in asset["name"]:
                    return asset["browser_download_url"]
    except Exception as e:
        print(f"Failed to retrieve the latest Git installer URL: {e}")
        return None

def download_and_install_git_windows():
    """Download and install Git on Windows manually."""
    git_installer_url = get_latest_git_installer_url()
    if not git_installer_url:
        print("Could not find the Git installer. Please install Git manually.")
        exit(1)

    temp_dir = tempfile.mkdtemp()
    installer_path = os.path.join(temp_dir, "GitInstaller.exe")

    try:
        print(f"Downloading Git installer from {git_installer_url}...")
        urllib.request.urlretrieve(git_installer_url, installer_path)
        print("Running Git installer...")
        run_command(installer_path + " /VERYSILENT /NORESTART")
    finally:
        shutil.rmtree(temp_dir)

def install_vcpkg():
    """Install vcpkg."""
    
    # Check OS
    os_name = platform.system()

    # Clone vcpkg repository
    if not os.path.exists("vcpkg"):
        print("Cloning vcpkg repository...")
        run_command("git clone https://github.com/microsoft/vcpkg.git")

    # Go to vcpkg directory
    os.chdir("vcpkg")

    # Bootstrap vcpkg
    if os_name == "Windows":
        print("Bootstrapping vcpkg on Windows...")
        run_command(".\\bootstrap-vcpkg.bat")
    else:
        print("Bootstrapping vcpkg on Unix-like system...")
        run_command("./bootstrap-vcpkg.sh")
    
    print("vcpkg installed successfully.")

if __name__ == "__main__":
    if not check_git():
        install_git()
    
    install_vcpkg()
