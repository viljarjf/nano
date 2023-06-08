"""
Script to remove the solution part of exercises, 
since the provided files already contain the solution
"""

import json
from pathlib import Path
from nbformat import v4 as nb


DEEP_LEARNING_DIR = Path(__file__).parent


def clear_codeblock(cell: dict[str]):
    """Clear contents of code block cell. Does nothing if block is not code

    :param cell: 
    :type cell: dict[str]
    """
    if cell["cell_type"] != "code":
        return
    cell["source"] = []
    cell["execution_count"] = None
    cell["outputs"] = []


def remove_images(cell: dict[str]):
    """Find and remove images. Does nothing if no images were found, or if cell is not markdown

    :param cell: 
    :type cell: dict[str]
    """
    if cell["cell_type"] != "markdown":
        return
    for i, line in enumerate(cell["source"]):
        # Remove entire line if the image is the only thing on the line
        if "<img" in line and line.index("<img") == 0:
            cell["source"][i] = "\n"
        # TODO also remove images that are not on their own lines


def codify_markdown(cell: dict[str]) -> list[dict[str]]:
    """Turn markdown codeblocks into proper codeblocks, and return a list of new cells

    :param cell: cell to split
    :type cell: dict[str]
    :return: list of cells with the code integrated in-place
    :rtype: list[dict[str]]
    """

    if cell["cell_type"] != "markdown":
        return [cell]
    source = cell["source"].split("\n")
    cells = []

    markdown_start_line = 0
    code_start_line = -1

    code = []
    
    for i, line in enumerate(source):

        # Check if we have found a code block
        if line.strip() == "```python":
            code_start_line = i

        # Add the code to a list
        elif code_start_line > 0:
            code.append(line)

        # Check if we are done
        if line.strip() == "```" and code_start_line > 0:
            code.pop() # overcounting

            # First, add a markdown cell with the text above the code
            md = "\n".join(source[markdown_start_line:code_start_line])
            md_cell = nb.new_markdown_cell(md)
            cells.append(md_cell)

            # Then, add a code cell
            code_cell = nb.new_code_cell("\n".join(code))
            cells.append(code_cell)

            # Finally, ensure correct iteration state
            markdown_start_line = i + 1
            code_start_line = -1
            code = []

    # Add the final markdown cell
    if markdown_start_line < len(source):
        md = "\n".join(source[markdown_start_line:])
        if md.strip(): # dont bother if the cell would be empty
            md_cell = nb.new_markdown_cell(md)
            cells.append(md_cell)

    return cells


def main():
    
    print("This script clears all images and codeblocks of content for a given Jupyter notebook.")
    filepath = DEEP_LEARNING_DIR / "03"#input("Enter filename: ")
    filepath = filepath.with_suffix(".ipynb")

    if not filepath.exists():
        raise FileNotFoundError("Given file does not exist")
    
    # Load the data
    with open(filepath, "r") as file:
        notebook = nb.reads(file.read())

    # clean cells
    cleaned_cells = []
    for cell in notebook["cells"]:
        clear_codeblock(cell)
        remove_images(cell)
        cleaned_cells += codify_markdown(cell)
    notebook["cells"] = cleaned_cells

    # Save the data
    with open(filepath, "w") as file:
        json.dump(notebook, file, indent=4)
    print("Done")

if __name__ == "__main__":
    main()
