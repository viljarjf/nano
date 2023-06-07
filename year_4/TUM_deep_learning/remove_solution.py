"""
Script to remove the solution part of exercises, 
since the provided files already contain the solution
"""

import json
from pathlib import Path

DEEP_LEARNING_DIR = Path(__file__).parent


def main():
    
    print("This script clears all images and codeblocks of content for a given Jupyter notebook.")
    filepath = DEEP_LEARNING_DIR / input("Enter filename: ")
    filepath = filepath.with_suffix(".ipynb")

    if not filepath.exists():
        raise FileNotFoundError("Given file does not exist")
    
    # Load the data
    with open(filepath, "r") as file:
        notebook = json.load(file)

    for cell in notebook["cells"]:
        # Search for and modify the codecells
        if cell["cell_type"] == "code":
            cell["source"] = []
            cell["execution_count"] = None
            cell["outputs"] = []
        # Search for and remove image tags
        elif cell["cell_type"] == "markdown":
            for i, line in enumerate(cell["source"]):
                # Remove entire line if the image is the only thing on the line
                if "<img" in line and line.index("<img") == 0:
                    cell["source"][i] = "\n"
                # TODO also remove images that are not on their own lines

    # Save the data
    with open(filepath, "w") as file:
        json.dump(notebook, file)
    
    print("Done")

if __name__ == "__main__":
    main()
