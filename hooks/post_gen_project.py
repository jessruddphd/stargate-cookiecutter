#!/usr/bin/env python
"""Post-generation hook for stargate-cookiecutter template.

This hook runs after the project is generated from the template.
It conditionally removes files based on user choices.
"""
import os
import shutil


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


def main():
    """Main post-generation logic."""
    include_qa = "{{ cookiecutter.include_qa_environment }}"
    
    # If QA environment is not included, remove the QA workflow file
    if include_qa == "no":
        qa_workflow = ".github/workflows/deploy-qa.yml"
        remove_file(qa_workflow)
        print("QA environment excluded - removed QA deployment workflow")
    else:
        print("QA environment included - all workflows retained")


if __name__ == "__main__":
    main()
