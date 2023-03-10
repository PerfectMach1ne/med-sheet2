# Maps column letters to numerical values used by some gspread methods
def map_column(col):
    column_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    return column_ids.index(col.upper()) + 1


def stotup(string: str) -> tuple:  # string to tuple
    return eval(string)


def stodict(string: str) -> dict:  # string to dictionary
    return eval(string)
