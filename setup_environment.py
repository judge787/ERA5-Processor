import os
import subprocess
import sys 
import webbrowser 

import requests #used for downloading chromedriver
import zipfile #used for unzipping chromedriver

# Define functions to print colored text
def print_green(text):
    print("\033[92m" + text + "\033[0m")

def print_yellow(text):
    print("\033[93m" + text + "\033[0m")

def print_blue(text):
    print("\033[94m" + text + "\033[0m")

def print_red(text):
    print("\033[91m" + text + "\033[0m")


def create_venv(venv_dir='venv'):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_dir):
        print_blue(f"Creating virtual environment in {venv_dir}...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])
    else:
        if 'VIRTUAL_ENV' in os.environ:
            print(f"Virtual environment already exists in {venv_dir} and is running.")
        else:
            print_red(f"Virtual environment already exists in {venv_dir} but is not running.")
            
def install_pip():
    """Install pip if it's not already available."""
    try:
        # Try importing pip to check if it's installed
        import pip
        print("Pip is already installed.")
    except ImportError:
        # Pip is not installed; use ensurepip to install it
        print_blue("Pip is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install(package):
    """Install a Python package using pip if it's not already installed."""
    try:
        # Try importing the package to check if it's installed
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        # The package is not installed; install it
        print_blue(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def download_chromedriver():
    # Define the path where chromedriver is expected to be
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')

    # Check if ChromeDriver already exists at the expected path
    if os.path.exists(chromedriver_path):
        print("ChromeDriver is already available in the current directory.")
        return  # Exit the function early if ChromeDriver is found

    # Send an HTTP GET request to the URL and store the response
    response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
    
    # Extract the text content from the response, which contains the version number
    version = response.text
    
    # Construct the URL to download ChromeDriver using the fetched version number
    url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64.zip"
    
    # Send another HTTP GET request to download the ChromeDriver zip file, enabling stream for large files
    response = requests.get(url, stream=True)
    
    # Check if the response status is OK (HTTP status code 200 means success)
    if response.status_code == 200:
        # Define the path to save the zip file using the current working directory
        zip_path = os.path.join(os.getcwd(), 'chromedriver.zip')
        
        # Open a file at the given path with write-binary mode and write the content of the response to it
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        print("ChromeDriver downloaded successfully.")
        
        # Open the zip file using the zipfile module in read mode
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all contents of the zip file to the current working directory
            zip_ref.extractall(os.getcwd())
        print("ChromeDriver unzipped successfully.")

        # Cleanup by removing the zip file after extraction
        os.remove(zip_path)
        print("Zip file removed after extraction.")
    else:
        # If the download failed, print an error message
        print("Failed to download ChromeDriver.")


def install_chrome():
    """Direct the user to download Chrome if not installed."""
    # Determine the OS and open the download URL for Chrome
    os_name = sys.platform
    if os_name == 'darwin':
        webbrowser.open('https://www.google.com/chrome/')
    elif os_name.startswith('linux'):
        # Command to download and install Chrome on Debian-based systems
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
        subprocess.run(["sudo", "apt", "install", "./google-chrome-stable_current_amd64.deb"])
    elif os_name == 'win32':
        webbrowser.open('https://www.google.com/chrome/')

def main():
    """Main function to orchestrate setup process."""
    
    create_venv()

    # Check if the virtual environment is activated by checking the VIRTUAL_ENV environment variable
    if 'VIRTUAL_ENV' in os.environ:
        # The virtual environment is active; install packages

        # Ensure pip is installed
        install_pip()

        # Install Selenium using pip
        install('selenium')
    else:
        # The virtual environment is not active; instruct the user to activate it
        print_red("The virtual environment is not currently active.")
        print_yellow("Please activate it before running this script.")
        print_yellow(f"source venv/bin/activate")
        sys.exit(1)  # Exit the script because the environment is not active
    
    # Check if Chrome is installed
    try:
        # Attempt to get the version of Chrome to check if it's installed
         version = subprocess.check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
         print(f"Google Chrome is installed: {version.decode()}")
    except FileNotFoundError:
        # Chrome is not found, prompt installation
        print("Google Chrome is not installed. Installing now...")
        install_chrome()

    download_chromedriver()

if __name__ == '__main__':
    main()
