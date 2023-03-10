# Maps column letters to numerical values used by some gspread methods
def map_column(col):
    column_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    return column_ids.index(col.upper()) + 1


def stotupdts():  # string to tuple of date strings
    pass


def stotuphrs():  # string to tuple of hour strings
    pass


def stodict():  # string to dictionary
    pass


def stodicttuphrs():  # string to dictionary of tuples of hour strings
    pass
