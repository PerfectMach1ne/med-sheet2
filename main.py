import gspread
# Python cmd module for creating custom command line interpreters.
import cmd

import oshutil

# =-=-= End User OAuth Client for all spreadsheets
# Requires a 'credentials.json' file to be present in '%appdata%\gspread' (Roaming folder), otherwise it might throw a
# FileNotFoundError.
# IMPORTANT NOTE: The JSON file obtained from Google Cloud console's 'IAM and admin' > 'Service accounts' > 'Keys' >
# 'Add key' (and/or something with 'Manage service accounts' > [Something about 'MedSheet357']) will NOT work and will
# likely throw a 'ValueError: Client secrets must be for a web or installed app.'.
# The JSON required for gspread & Google Sheets integration can be found under 'APIs and services' > 'Credentials' >
# 'OAuth 2.0 Client IDs' > 'Actions' tab > {Download icon} ('Download OAuth client') > 'DOWNLOAD JSON'.
gc = gspread.oauth()


# Maps column letters to numerical values used by some gspread methods
def map_column(col):
    column_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    return column_ids.index(col.upper()) + 1


# For cmd implementation reference best go to: https://docs.python.org/3/library/cmd.html
class MedSheet(cmd.Cmd):
    intro = '\n'.join(['MedSheet357 command line shell.',
                       'For assisting tracking medicine intake via Google Sheets API.',
                       'Type \'?\' or \'help\' to list all the commands.'
                       ])
    prompt = '> '

    # Default implementation repeats last command when an empty line is entered 'as a command'. This overrides that
    # to do nothing in case I accidentally mess something up (remote sheet control can be fragile).
    def emptyline(self) -> bool:
        return

    # 'osh' command
    def do_osh(self, line):
        'Manage origin spreadsheet.'
        # TODO: Describe the "subcommand" functionality (maybe research how other CLIs do it too).
        sline = line.split()  # Split the line string into a list (default separator is whitespace ' ').
        if sline[0] in {'getincidents', 'getinc'}:  # oshutil.py/getincidents(bool) -> list
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

    def do_createsh(self, line):
        'Creates a new spreadsheet.'
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

    def do_exit(self, line):
        'Exit the command line.'
        return True


if __name__ == "__main__":
    MedSheet().cmdloop()
