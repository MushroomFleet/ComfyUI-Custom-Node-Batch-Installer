import os
import subprocess
import sys
from pathlib import Path
import shutil

def read_repo_urls(filename):
    """Read repository URLs from a text file."""
    try:
        with open(filename, 'r') as f:
            # Strip whitespace and filter out empty lines
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        sys.exit(1)

def clone_repository(url):
    """Clone a git repository and return the path to the cloned directory."""
    try:
        # Extract repository name from URL
        repo_name = url.split('/')[-1].replace('.git', '')
        
        # Check if directory already exists
        if os.path.exists(repo_name):
            print(f"Repository {repo_name} already exists, skipping...")
            return repo_name
        
        # Clone the repository
        result = subprocess.run(['git', 'clone', url], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode != 0:
            print(f"Error cloning {url}: {result.stderr}")
            return None
            
        return repo_name
    except Exception as e:
        print(f"Error while cloning {url}: {str(e)}")
        return None

def find_requirements_txt(repo_path):
    """Find all requirements.txt files in the repository."""
    requirements_files = []
    for path in Path(repo_path).rglob('requirements.txt'):
        requirements_files.append(str(path))
    return requirements_files

def copy_installation_files(target_dir):
    """Copy necessary installation files to the target directory."""
    try:
        # Copy package-preparation.py
        shutil.copy2('package-preparation.py', target_dir)
        print(f"Copied installation files to {target_dir}")
        return True
    except Exception as e:
        print(f"Error copying installation files to {target_dir}: {str(e)}")
        return False

def main():
    # Ensure we're in the custom_nodes directory
    if not os.path.basename(os.getcwd()) == 'custom_nodes':
        print("Error: This script must be run from the 'custom_nodes' directory!")
        sys.exit(1)

    # Check if package-preparation.py exists
    if not os.path.exists('package-preparation.py'):
        print("Error: package-preparation.py not found in current directory!")
        sys.exit(1)

    # Read repository URLs
    urls = read_repo_urls('comfy-repos.txt')
    print(f"Found {len(urls)} repositories to process")

    # Process each repository
    for url in urls:
        print(f"\nProcessing repository: {url}")
        
        # Clone the repository
        repo_name = clone_repository(url)
        if not repo_name:
            continue

        # Find requirements.txt files
        requirements_files = find_requirements_txt(repo_name)
        
        # For each requirements.txt found, copy installation files and run the package preparation script
        for req_file in requirements_files:
            req_dir = os.path.dirname(req_file)
            print(f"Found requirements.txt in {req_dir}")
            
            # Copy necessary files to the requirements.txt directory
            if copy_installation_files(req_dir):
                try:
                    # Run the package preparation script
                    subprocess.run([sys.executable, 'package-preparation.py'],
                                 cwd=req_dir,
                                 check=True)
                    
                    # Clean up - remove the copied files after installation
                    try:
                        os.remove(os.path.join(req_dir, 'package-preparation.py'))
                    except Exception as e:
                        print(f"Warning: Could not remove temporary files from {req_dir}: {str(e)}")
                        
                except subprocess.CalledProcessError as e:
                    print(f"Error running package-preparation.py in {req_dir}: {str(e)}")
            else:
                print(f"Skipping installation for {req_dir} due to file copy error")

if __name__ == "__main__":
    main()
