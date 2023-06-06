"""
Script to remove the solution part of exercises, 
since the provided files already contain the solution
"""

import json
from pathlib import Path

DEEP_LEARNING_DIR = Path(__file__).parent


def main():
    
    print("This script clears all codeblocks of content for a given Jupyter notebook.")
    filepath = DEEP_LEARNING_DIR / input("Enter filename: ")
    filepath = filepath.with_suffix(".ipynb")

    if not filepath.exists():
        raise FileNotFoundError("Given file does not exist")
    
    # Load the data
    with open(filepath, "r") as file:
        notebook = json.load(file)

    # Search for and modify the codecells
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            cell["source"] = []
            cell["execution_count"] = None
            cell["outputs"] = []

    # Save the data
    with open(filepath, "w") as file:
        json.dump(notebook, file)
    
    print("Done")

if __name__ == "__main__":
    main()
