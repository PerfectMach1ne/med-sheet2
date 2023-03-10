import oshutil


def gsh(line):
    sline = line.split()  # Split the line string into a list (default separator is whitespace ' ').
    if len(sline) == 0:  # Prevents an IndexError when no argument is passed.
        print("Placeholder text for no argument 'gsh' command.")
    elif sline[0] in {''}:
        pass


def osh(line):
    # TODO: Describe the "subcommand" functionality (maybe research how other CLIs do it too).
    sline = line.split()  # Split the line string into a list (default separator is whitespace ' ').
    if len(sline) == 0:  # Prevents an IndexError when no argument is passed.
        print("Placeholder text for no argument 'osh' command.")
    elif sline[0] in {'getincidents', 'getinc'}:  # oshutil.py/getincidents(bool) -> list
        if len(sline) == 1:
            oshutil.getincidents(False)
            # print(oshutil.getincidents(False))
        elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
            oshutil.getincidents(True)
    elif sline[0] in {'getiddata', 'getdata'}:  # oshutil.py/getiddata(bool) -> list
        if len(sline) == 1:
            oshutil.getiddata(False)
            # print(oshutil.getiddata(False))
        elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
            oshutil.getiddata(True)
    elif sline[0] in {'transformincidents', 'transforminc'}:
        if len(sline) == 1:
            oshutil.transformincidents()
        elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
            oshutil.transformincidents()
    elif sline[0] in {'transformiddata', 'transformdata'}:
        if len(sline) == 1:
            oshutil.transformiddata(False)
        elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
            oshutil.transformiddata(True)
    elif sline[0] in {'getmeds', 'listmeds'}:
        if len(sline) == 1:
            print(oshutil.getmeds(False))
        elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
            oshutil.getmeds(True)
    elif sline[0] == 'getmedinfo':
        if len(sline) == 1:
            print(oshutil.getmedinfo(False))
        elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
            oshutil.getmedinfo(True)
    elif sline[0] == 'getstd':
        oshutil.getstd()


def createsh(line):
    while True:
        try:
            choice = input('Are you sure you want to create a new spreadsheet? (y/N) ')
            if choice.lower() == 'y':
                print('where doing it man\nwhere MAKING THIS HAPEN')
                return
            elif choice.lower() in {'n', ''}:  # N being capital means it's the default option
                print('Spreadsheet creation has been cancelled.')
                return
        except ValueError:
            pass
