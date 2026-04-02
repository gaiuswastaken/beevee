from subprocess import run # Executes shell commands (such as pip)
import sys # Gets the current interpreter being used to run the script
import importlib # Checks the libraries have been installed

dependencies = ["kivy", "requests", "google_genai"]
    
def check_and_install_dependencies_not_kivymd():
    for i in range (len(dependencies)):
        try: # Tries to import it
            # Force installs Kivy 2.3.1 regardless of install state
            run([sys.executable, "-m", "pip", "install", "kivy==2.3.1"])
            importlib.import_module(dependencies[i])
            print(f"{dependencies[i]} is installed")
        except ImportError: # If module is not found, hence giving an import error
            if dependencies[i] == "kivy":
                run([sys.executable, "-m", "pip", "install", "kivy==2.3.1"])
            else:
                run([sys.executable, "-m", "pip", "install", dependencies[i]])

def check_and_install_kivymd():
    try: # Tries to import it
        importlib.import_module("kivymd")
        print("KivyMD is installed")
    except ImportError: # If module is not found, hence giving an import error
        run([sys.executable, "-m", "pip", "install", "https://github.com/kivymd/KivyMD/archive/master.zip"])

check_and_install_dependencies_not_kivymd()
check_and_install_kivymd()