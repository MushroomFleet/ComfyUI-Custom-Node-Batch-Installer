# ComfyUI Custom Node Batch Installer

A user-friendly web interface tool to simplify the installation of multiple ComfyUI custom nodes and their dependencies. This tool works with both standard ComfyUI installations and ComfyUI Portable.

## Features

- Easy-to-use web interface for managing custom node installations
- Batch installation of multiple custom nodes from GitHub repositories
- Path configuration for flexible installation locations
- Automatic handling and installation of dependencies
- Support for ComfyUI Portable's embedded Python
- Virtual environment support to prevent conflicts with system Python
- Detailed logging for troubleshooting
- Path validation and repository URL verification
- Simple one-click installation process

## Prerequisites

- Python 3.x
- Git

## First-Time Setup

1. Download or clone this repository to any location on your computer
2. Run `install.bat` to create the virtual environment and install dependencies
3. Run `start-web.bat` to launch the web interface
4. In the web interface, specify your ComfyUI's `custom_nodes` directory path
5. Add your desired GitHub repository URLs
6. Click "Save Repository List" followed by "Install Custom Nodes"

## File Structure

```
project_root/
├── install.bat              # First-time installation and dependency setup
├── start-web.bat           # Web interface launcher
├── requirements.txt        # Python package dependencies
├── gradio_wrapper.py      # Web interface implementation
├── clone-custom-nodes.py   # Core node installation script
├── package-preparation.py  # Dependency installer
└── README.md              # This documentation
```

## Using the Web Interface

1. Launch the interface by running `start-web.bat`
2. The web interface will open automatically in your default browser
3. Enter the full path to your ComfyUI's `custom_nodes` directory
4. Click "Validate Path" to ensure the path is correct
5. Add GitHub repository URLs (one per line) in the text area
6. Click "Save Repository List" to validate URLs and prepare for installation
7. Click "Install Custom Nodes" to begin the installation process
8. Monitor the output box for installation progress and any error messages

## Example Repository URLs

```
https://github.com/ltdrdata/ComfyUI-Manager
https://github.com/user/custom-node-repository
```

## Logging

The installer creates detailed logs in the project directory with timestamp-based filenames (e.g., `installer_20241206_123456.log`). These logs are useful for troubleshooting installation issues.

## Troubleshooting

### Common Issues

1. **Virtual environment not found**
   - Run `install.bat` to create the virtual environment and install dependencies
   - Ensure Python is installed and added to your system's PATH

2. **Git not found**
   - Install Git from https://git-scm.com/
   - Ensure Git is added to your system's PATH

3. **Invalid path errors**
   - Ensure the path points to a valid ComfyUI custom_nodes directory
   - The directory must be named exactly "custom_nodes"
   - ComfyUI's main.py should exist in the parent directory
   - Use forward slashes (/) or escaped backslashes (\\) in paths

4. **Permission errors**
   - Run the scripts with appropriate permissions
   - Ensure you have write access to both the installation directory and target custom_nodes directory

5. **Invalid repository URLs**
   - URLs must start with "https://github.com/"
   - URLs must point to valid GitHub repositories
   - Check for typos and correct formatting

6. **Web interface won't start**
   - Ensure you've run `install.bat` first
   - Check if port 7860 is available
   - Look for error messages in the console window

### Checking Logs

If you encounter issues:
1. Check the console output for immediate error messages
2. Look for the latest `installer_*.log` file in the project directory
3. Open the log file with a text editor to view detailed error information

## Security Notes

- The web interface runs locally only (127.0.0.1)
- No public URL sharing is enabled
- Path validation prevents directory traversal attempts
- Dependencies are isolated in a virtual environment

## Contributing

Feel free to submit issues and enhancement requests! Please include:
- Detailed description of the issue or enhancement
- Steps to reproduce any problems
- Relevant log files
- Your system configuration

## License

[Add your chosen license here]

## Support

If you encounter any problems or have questions:
1. Check the troubleshooting section above
2. Look through existing GitHub issues
3. Create a new issue with:
   - Detailed description of your problem
   - Relevant log files
   - Your system configuration
   - Steps to reproduce the issue
