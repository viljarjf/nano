"""general utilities"""

def get_input_floats(n: int) -> list:
    """Get a list of n floats from the user.
    entering "pop" removes latest element

    Args:
        n (int): number of floats to get

    Returns:
        list: list of n floats
    """
    res = []
    while len(res) < n:
        i = input("Enter value: ")
        try:
            i = float(i)
            res.append(i)
        except ValueError:
            if "pop" in i:
                print(f"popped {res.pop()}")
            else:
                print("Not recognized, try again")
    return res

