#!/usr/bin/env python
"""Post-generation hook for stargate-cookiecutter template.

This hook runs after the project is generated from the template.
It conditionally removes files based on user choices and optionally
initializes Git repository with branches.
"""
import os
import shutil
import subprocess


def remove_file(filepath):
    """Remove a file if it exists."""
    if os.path.isfile(filepath):
        os.remove(filepath)
        print(f"Removed: {filepath}")


def remove_dir(dirpath):
    """Remove a directory if it exists."""
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        print(f"Removed: {dirpath}")


def init_git_repo():
    """Initialize Git repository with dev and main branches."""
    try:
        # Initialize git repo
        subprocess.run(["git", "init"], check=True, capture_output=True)
        print("✓ Initialized Git repository")
        
        # Add all files
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        # Create initial commit on main
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from stargate-cookiecutter"],
            check=True,
            capture_output=True
        )
        print("✓ Created initial commit on main branch")
        
        # Create and checkout dev branch
        subprocess.run(["git", "checkout", "-b", "dev"], check=True, capture_output=True)
        print("✓ Created dev branch and set as default")
        
        print("\nGit repository initialized with branches:")
        print("  - main (initial commit)")
        print("  - dev (current branch)")
        
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not initialize Git repository: {e}")
        print("You can manually initialize Git with:")
        print("  git init")
        print("  git add .")
        print("  git commit -m 'Initial commit'")
        print("  git checkout -b dev")
    except FileNotFoundError:
        print("Warning: Git not found. Please install Git and initialize manually.")


def main():
    """Main post-generation logic."""
    include_qa = "{{ cookiecutter.include_qa_environment }}"
    init_git = "{{ cookiecutter.initialize_git_repo }}"
    
    # If QA environment is not included, remove the QA workflow file
    if include_qa == "no":
        qa_workflow = ".github/workflows/deploy-qa.yml"
        remove_file(qa_workflow)
        print("QA environment excluded - removed QA deployment workflow")
    else:
        print("QA environment included - all workflows retained")
    
    print()  # Empty line for readability
    
    # Initialize Git repository if requested
    if init_git == "yes":
        init_git_repo()
    else:
        print("Git initialization skipped. To initialize manually:")
        print("  cd {{ cookiecutter.repo_name }}")
        print("  git init")
        print("  git add .")
        print("  git commit -m 'Initial commit'")
        print("  git checkout -b dev")


if __name__ == "__main__":
    main()
