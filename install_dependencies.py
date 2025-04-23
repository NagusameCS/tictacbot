#==================================================
# ___    __     ___       __      __   __  ___
#  |  | /  `     |   /\  /  `    |__) /  \  | 
#  |  | \__,     |  /~~\ \__,    |__) \__/  | 
#==================================================
# NagusameCS
#==================================================
import subprocess
import sys

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    dependencies = ["pyautogui", "opencv-python", "numpy", "pillow"]
    for package in dependencies:
        try:
            print(f"Installing {package}...")
            install(package)
        except Exception as e:
            print(f"Failed to install {package}: {e}")
    print("All dependencies installed.")

