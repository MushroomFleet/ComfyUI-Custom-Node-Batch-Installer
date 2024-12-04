import os
import subprocess
import sys

def get_python_executable():
    """Get the correct Python executable path for ComfyUI Portable."""
    # Try to find the embedded Python executable
    portable_python = os.path.abspath(
        os.path.join('..', '..', '..', 'python_embeded', 'python.exe')
    )
    
    if os.path.exists(portable_python):
        return portable_python
    return sys.executable

def install_requirements():
    """Install requirements using the appropriate Python executable."""
    if not os.path.exists('requirements.txt'):
        print("No requirements.txt found in current directory")
        return
    
    python_exec = get_python_executable()
    print(f"Using Python executable: {python_exec}")
    
    try:
        # Install requirements using pip
        result = subprocess.run(
            [python_exec, '-s', '-m', 'pip', 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error installing requirements: {result.stderr}")
        else:
            print("Requirements installed successfully")
            
    except Exception as e:
        print(f"Error during installation: {str(e)}")

if __name__ == "__main__":
    install_requirements()
