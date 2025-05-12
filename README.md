# Ella - Simple Version Control System

Ella is a lightweight version control system implemented in Python. It provides basic functionality to track changes in files, similar to Git, but with a simplified design. This project is intended for educational purposes and demonstrates how version control systems work under the hood.

## Features

- Initialize a repository
- Add files to the staging area
- Commit changes
- View commit logs
- Show differences between file versions

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/14elias/custom_git
   cd ella
   ```
2. Ensure you have Python 3 installed on your system.

Add the ella command to your PATH:

3. On Windows: Add the directory containing ella.bat to your system's PATH environment variable.
   On Linux/Mac: Add the directory containing ella.py to your PATH and make it executable:
   chmod +x ella.py

Usage

Ella provides a command-line interface. Below are the available commands:

# Initialize a Repository

ella init
This command initializes a new Ella repository in the current directory.

# Add a File

ella add <file>
Adds a file to the staging area.

# Commit Changes

ella commit <message>
Commits the staged changes with a message.

# View Commit Logs

ella log
Displays the history of commits.

# Show Differences

ella show-diff <commit_hash>

Displays the differences between the current version of a file and its previous version in the specified commit.

# Project Structure

- main.py: Core implementation of the Ella version control system.
- ella.py: Command-line interface for interacting with Ella.
- .ella/: Directory created by Ella to store repository data, including objects, index, and HEAD.

# Limitations

- Ella does not support branching or merging.
- Only tracks changes to files, not directories.
- Designed for educational purposes and may not handle edge cases robustly.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

You can copy and paste this directly into a `README.md` file for your project. Let me know if you need further adjustments!
