import gradio as gr
import os
import subprocess
import sys
from pathlib import Path
import shutil
import logging
import re
from typing import Tuple, Optional
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'installer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class CustomNodeInstaller:
    def __init__(self):
        self.required_files = [
            'clone-custom-nodes.py',
            'package-preparation.py',
            'start-prep.bat'
        ]

    def validate_path(self, path: str) -> Tuple[bool, str]:
        """
        Validate if the path is a valid ComfyUI custom_nodes directory.
        
        Args:
            path: String path to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not path or not path.strip():
                return False, "Path cannot be empty!"
            
            path_obj = Path(path)
            
            # Check if path exists
            if not path_obj.exists():
                return False, f"Path does not exist: {path}"
            
            # Check if it's a directory
            if not path_obj.is_dir():
                return False, f"Path is not a directory: {path}"
            
            # Check if it's named 'custom_nodes'
            if path_obj.name != "custom_nodes":
                return False, "Directory must be named 'custom_nodes'"
            
            # Check if it appears to be a ComfyUI custom_nodes directory
            parent_dir = path_obj.parent
            if not (parent_dir / "main.py").exists():
                return False, "Directory does not appear to be a ComfyUI installation (main.py not found in parent directory)"
            
            return True, "Path is valid"
            
        except Exception as e:
            logging.error(f"Path validation error: {str(e)}")
            return False, f"Error validating path: {str(e)}"

    def validate_github_urls(self, urls_text: str) -> Tuple[bool, str, list]:
        """
        Validate a list of GitHub repository URLs.
        
        Args:
            urls_text: String containing newline-separated URLs
            
        Returns:
            Tuple of (is_valid, error_message, valid_urls)
        """
        if not urls_text or not urls_text.strip():
            return False, "No repository URLs provided", []
        
        urls = [url.strip() for url in urls_text.splitlines() if url.strip()]
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            # GitHub URL validation pattern
            pattern = r'^https://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-._]+/?$'
            if re.match(pattern, url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            return False, f"Invalid GitHub URLs found:\n{chr(10).join(invalid_urls)}", valid_urls
        
        return True, "All URLs are valid", valid_urls

    def copy_required_files(self, target_path: Path) -> Tuple[bool, str]:
        """
        Copy required installation files to the target directory.
        
        Args:
            target_path: Path object pointing to the target directory
            
        Returns:
            Tuple of (success, message)
        """
        try:
            current_dir = Path(__file__).parent
            
            for file in self.required_files:
                source = current_dir / file
                if not source.exists():
                    return False, f"Required file not found: {file}"
                shutil.copy2(source, target_path / file)
            
            return True, "Required files copied successfully"
            
        except Exception as e:
            logging.error(f"Error copying files: {str(e)}")
            return False, f"Error copying required files: {str(e)}"

    def save_repos(self, repos_text: str, custom_nodes_path: str) -> str:
        """Save repository URLs and prepare installation files."""
        logging.info(f"Attempting to save repositories to {custom_nodes_path}")
        
        # Validate path
        path_valid, path_msg = self.validate_path(custom_nodes_path)
        if not path_valid:
            return f"Error: {path_msg}"
        
        # Validate URLs
        urls_valid, urls_msg, valid_urls = self.validate_github_urls(repos_text)
        if not urls_valid:
            return f"Error: {urls_msg}"
        
        try:
            target_path = Path(custom_nodes_path)
            
            # Copy required files
            copy_success, copy_msg = self.copy_required_files(target_path)
            if not copy_success:
                return f"Error: {copy_msg}"
            
            # Save repositories
            with open(target_path / 'comfy-repos.txt', 'w') as f:
                f.write('\n'.join(valid_urls))
            
            logging.info("Repository list saved successfully")
            return "Repository list and required files saved successfully!"
            
        except Exception as e:
            logging.error(f"Error saving repositories: {str(e)}")
            return f"Error saving repositories: {str(e)}"

    def load_repos(self, custom_nodes_path: str) -> str:
        """Load existing repositories from comfy-repos.txt."""
        if not custom_nodes_path or not custom_nodes_path.strip():
            return ""
            
        path_valid, path_msg = self.validate_path(custom_nodes_path)
        if not path_valid:
            return ""
        
        try:
            repo_file = Path(custom_nodes_path) / 'comfy-repos.txt'
            if not repo_file.exists():
                return ""
                
            with open(repo_file, 'r') as f:
                return f.read()
                
        except Exception as e:
            logging.error(f"Error loading repositories: {str(e)}")
            return ""

    def install_nodes(self, custom_nodes_path: str) -> str:
        """Run the node installation process."""
        logging.info(f"Starting node installation in {custom_nodes_path}")
        
        # Validate path
        path_valid, path_msg = self.validate_path(custom_nodes_path)
        if not path_valid:
            return f"Error: {path_msg}"
        
        try:
            script_path = Path(custom_nodes_path) / 'clone-custom-nodes.py'
            if not script_path.exists():
                return "Error: clone-custom-nodes.py not found! Please save repository list first."
            
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=custom_nodes_path,
                capture_output=True,
                text=True
            )
            
            # Log the complete output
            if result.stdout:
                logging.info(f"Installation output: {result.stdout}")
            if result.stderr:
                logging.error(f"Installation errors: {result.stderr}")
            
            # Parse the output to extract the summary
            output_lines = result.stdout.split('\n')
            summary_start = -1
            for i, line in enumerate(output_lines):
                if line.startswith("="*50):
                    summary_start = i
                    break
            
            formatted_output = ""
            if result.stdout:
                formatted_output += result.stdout + "\n"
            if result.stderr:
                formatted_output += "\nErrors:\n" + result.stderr
            
            # Add a clear visual separator and completion message
            formatted_output += "\n" + "="*50 + "\n"
            formatted_output += "Installation process completed!"
            
            logging.info("Installation process completed!")
            return formatted_output.strip()
            
        except Exception as e:
            error_msg = f"Installation error: {str(e)}"
            logging.error(error_msg)
            return error_msg

def create_ui():
    """Create and configure the Gradio interface."""
    installer = CustomNodeInstaller()
    
    with gr.Blocks(title="ComfyUI Custom Node Installer") as app:
        gr.Markdown("""
        # ComfyUI Custom Node Installer
        This tool helps you install multiple custom nodes for ComfyUI from GitHub repositories.
        
        1. Enter the path to your ComfyUI's custom_nodes directory
        2. Add GitHub repository URLs (one per line)
        3. Click "Save Repository List" to prepare the installation
        4. Click "Install Custom Nodes" to perform the installation
        """)
        
        with gr.Column():
            path_input = gr.Textbox(
                label="Path to ComfyUI custom_nodes folder",
                placeholder="C:/path/to/ComfyUI/custom_nodes",
                info="Enter the full path to your ComfyUI's custom_nodes directory"
            )
            
            repo_input = gr.TextArea(
                label="GitHub Repositories",
                placeholder="https://github.com/user/repo\nhttps://github.com/user/another-repo",
                info="Enter one repository URL per line"
            )
        
        with gr.Row():
            validate_button = gr.Button("Validate Path", variant="secondary")
            save_button = gr.Button("Save Repository List")
            install_button = gr.Button("Install Custom Nodes", variant="primary")
        
        output = gr.Textbox(
            label="Output",
            lines=10,
            max_lines=20,
            interactive=False
        )
        
        # Event handlers
        def validate_path_handler(path):
            valid, msg = installer.validate_path(path)
            return f"Path validation: {msg}"
        
        validate_button.click(
            fn=validate_path_handler,
            inputs=[path_input],
            outputs=[output]
        )
        
        path_input.change(
            fn=installer.load_repos,
            inputs=[path_input],
            outputs=[repo_input]
        )
        
        save_button.click(
            fn=installer.save_repos,
            inputs=[repo_input, path_input],
            outputs=[output]
        )
        
        install_button.click(
            fn=installer.install_nodes,
            inputs=[path_input],
            outputs=[output]
        )
    
    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )