#==================================================
# ___    __     ___       __      __   __  ___
#  |  | /  `     |   /\  /  `    |__) /  \  | 
#  |  | \__,     |  /~~\ \__,    |__) \__/  | 
#==================================================
# NagusameCS
#==================================================

import platform
import os
import sys
import subprocess

def check_permissions():
    """
    Detects the operating system and attempts to ensure the necessary permissions are granted.
    Provides instructions for permissions that cannot be automated.
    """
    system = platform.system()
    print(f"Detected operating system: {system}")

    if system == "Windows":
        print("Checking permissions on Windows...")
        # On Windows, ensure the script is run as an administrator
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print("Requesting administrator privileges...")
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, __file__, None, 1
                )
                sys.exit(0)
            else:
                print("Administrator privileges confirmed.")
        except Exception as e:
            print(f"Error requesting administrator privileges: {e}")

    elif system == "Darwin":  # macOS
        print("Checking permissions on macOS...")
        # macOS requires Accessibility permissions for mouse control and Screen Recording for screen capture
        print("Attempting to open System Preferences for Accessibility permissions...")
        try:
            subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"])
        except Exception as e:
            print(f"Error opening Accessibility settings: {e}")

        print("Attempting to open System Preferences for Screen Recording permissions...")
        try:
            subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"])
        except Exception as e:
            print(f"Error opening Screen Recording settings: {e}")

        print("Please grant Accessibility and Screen Recording permissions for your terminal or IDE.")
        print("After granting permissions, you may need to restart your terminal or IDE.")

    elif system == "Linux":
        print("Checking permissions on Linux...")
        # On Linux, ensure xdotool is installed for mouse control
        try:
            result = subprocess.run(["xdotool", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print("xdotool is not installed. Attempting to install it...")
                try:
                    subprocess.run(["sudo", "apt", "install", "-y", "xdotool"], check=True)
                    print("xdotool installed successfully.")
                except Exception as e:
                    print(f"Error installing xdotool: {e}")
            else:
                print("xdotool is installed.")
        except FileNotFoundError:
            print("xdotool is not installed and could not be found. Please install it manually.")

        # Ensure the script has access to the X server
        if "DISPLAY" not in os.environ:
            print("The DISPLAY environment variable is not set.")
            print("Ensure you are running this script in a graphical environment.")
        else:
            print("DISPLAY environment variable is set.")

        # Check for xinput for mouse control
        try:
            result = subprocess.run(["xinput", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print("xinput is not installed. Attempting to install it...")
                try:
                    subprocess.run(["sudo", "apt", "install", "-y", "xinput"], check=True)
                    print("xinput installed successfully.")
                except Exception as e:
                    print(f"Error installing xinput: {e}")
            else:
                print("xinput is installed.")
        except FileNotFoundError:
            print("xinput is not installed and could not be found. Please install it manually.")

    else:
        print(f"Unsupported operating system: {system}")
        print("This script currently supports Windows, macOS, and Linux.")

if __name__ == "__main__":
    check_permissions()
