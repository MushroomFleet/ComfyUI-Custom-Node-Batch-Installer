# ComfyUI Custom Node Batch Installer
https://www.youtube.com/watch?v=d0gHYTuA2-I

A collection of scripts to simplify the installation of multiple ComfyUI custom nodes and their dependencies. This tool is particularly useful for ComfyUI Portable users but works with standard ComfyUI installations as well.

## Features

- Batch installation of multiple custom nodes from GitHub repositories
- Automatic handling and installation of dependencies
- Support for ComfyUI Portable's embedded Python
- Simple one-click installation process for Windows users
- Automatic detection and handling of requirements.txt files in any subdirectory
- Automated cleanup after installation
- Support for both standard Python installations and ComfyUI Portable's embedded Python

## Prerequisites

- Python 3.x
- Git
- ComfyUI installed (either Portable or standard version)

## Installation

1. Download or clone this repository into your ComfyUI's `custom_nodes` directory
2. Ensure all required files are present (see File Structure below)
3. Create a file named `comfy-repos.txt` in the same directory
4. Add GitHub repository URLs to `comfy-repos.txt`, one per line

Example `comfy-repos.txt`:
```
https://github.com/user1/comfy-node1
https://github.com/user2/comfy-node2
https://github.com/user3/comfy-node3
```

## Usage

### Windows Users (Recommended)
1. Double-click `start-prep.bat`
2. Wait for the installation process to complete
3. Check the console output for any error messages

### Manual Usage
1. Open a terminal in your ComfyUI's `custom_nodes` directory
2. Run: `python clone-custom-nodes.py`

## How It Works

1. The script reads repository URLs from `comfy-repos.txt`
2. Each repository is cloned into the `custom_nodes` directory
3. The script recursively searches for `requirements.txt` files in each cloned repository
4. For each found `requirements.txt`:
   - Required installation files are copied to the directory
   - Dependencies are automatically installed using the appropriate Python interpreter
   - Temporary installation files are cleaned up
5. Process repeats for each repository in the list

## File Structure

Required files in your `custom_nodes` directory:
```
custom_nodes/
├── clone-custom-nodes.py    # Main installation script
├── package-preparation.py   # Dependency installer
├── start-prep.bat          # Windows launcher
└── comfy-repos.txt         # Your repository list
```

## Troubleshooting

### Common Issues

1. **Python not found**
   - Ensure Python is installed and added to your system's PATH
   - For ComfyUI Portable users, ensure you're using the correct directory structure

2. **Git not found**
   - Install Git from https://git-scm.com/
   - Ensure Git is added to your system's PATH

3. **Permission errors**
   - Run the script with appropriate permissions
   - Ensure you have write access to the custom_nodes directory

4. **Installation files missing**
   - Verify all required files are present in the `custom_nodes` directory
   - Check the File Structure section above for the complete list

### Error Messages

- "Error: This script must be run from the 'custom_nodes' directory!"
  - Make sure you're running the script from ComfyUI's custom_nodes directory

- "Error: comfy-repos.txt not found"
  - Create the comfy-repos.txt file and add your repository URLs

- "Error: package-preparation.py not found in current directory!"
  - Ensure all required files are present in the custom_nodes directory

## Contributing

Feel free to submit issues and enhancement requests!

## Support

If you encounter any problems or have questions, please open an issue on GitHub.
