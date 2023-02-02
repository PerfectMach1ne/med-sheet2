import gspread
import cmd

import oshutil

# End User OAuth Client for all spreadsheets
gc = gspread.oauth()


# Maps column letters to numerical values used by some gspread methods
def map_column(col):
    column_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    return column_ids.index(col.upper()) + 1


class MedSheet(cmd.Cmd):
    intro = '\n'.join(['MedSheet357 command line shell.',
                       'For assisting tracking medicine intake via Google Sheets API.',
                       'Type \'?\' or \'help\' to list all the commands.'
                       ])
    prompt = '> '

    # Default implementation repeats last command. This overrides that to do nothing.
    def emptyline(self) -> bool:
        return

    def do_osh(self, line):
        'Manage origin spreadsheet.'
        sline = line.split()
        if sline[0] in {'getincidents', 'getinc'}:
            if len(sline) == 1:
                oshutil.getincidents(False)
            elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
                oshutil.getincidents(True)
        elif sline[0] in {'getiddata', 'getdata'}:
            if len(sline) == 1:
                oshutil.getiddata(False)
            elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
                oshutil.getiddata(True)
        elif sline[0] in {'validateincidents', 'validateinc'}:
            if len(sline) == 1:
                oshutil.validateincidents()
            elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
                oshutil.validateincidents()
        elif sline[0] in {'validateiddata', 'validatedata'}:
            if len(sline) == 1:
                oshutil.validateiddata(False)
            elif len(sline) > 1 and sline[1] in {"--print", "--pr", "--p"}:
                oshutil.validateiddata(True)
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
                elif choice.lower() == 'n':
                    return
            except ValueError:
                pass

    def do_exit(self, line):
        'Exit the command line.'
        return True


if __name__ == "__main__":
    MedSheet().cmdloop()