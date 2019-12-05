def get_input(day) -> list:
    """
    Gets the data from the input file.

    Parameters:
        day (int): The Current Day number.

    Returns:
        list: Each line that the Input Data contains.
    """
    try:
        file_path = "../resources/Day_" + str(day).rjust(2, "0") + "_Inputs.txt"
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except OSError:
        raise Exception("No Input file for Day: ", day)
