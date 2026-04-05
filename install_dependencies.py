from subprocess import run # Executes shell commands (such as pip)
import sys # Gets the current interpreter being used to run the script
import importlib # Checks the libraries have been installed

# Reworked it into a dictionary to ensure Kivy v2.3.1 is installed without force installing it if it's already there, as KivyMD requires Kivy v2.3.1 and installing it again would cause issues with KivyMD
dependencies = {
    "kivy": "kivy==2.3.1",
    "requests": "requests",
    "google.genai": "google-genai"
}
    
def check_and_install_dependencies_not_kivymd():
    for library, value in dependencies.items():
        try: # Tries to import it
            importlib.import_module(library)
            print(f"{library} is installed")
        except ImportError: # If module is not found, hence giving an import error
            print(f"{library} is not installed, installing now...")
            run([sys.executable, "-m", "pip", "install", value])

def check_and_install_kivymd():
    try: # Tries to import it
        importlib.import_module("kivymd")
        print("KivyMD is installed")
    except ImportError: # If module is not found, hence giving an import error
        run([sys.executable, "-m", "pip", "install", "https://github.com/kivymd/KivyMD/archive/master.zip"])

check_and_install_dependencies_not_kivymd()
check_and_install_kivymd()