# Python cmd module for creating custom command line interpreters.
import cmd

import commands as cl


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

    # 'gsh' command
    def do_gsh(self, line):
        """Manage a spreadsheet."""
        cl.gsh(line)

    # 'osh' command
    def do_osh(self, line):
        """Manage origin spreadsheet."""
        # TODO: Describe the "subcommand" functionality (maybe research how other CLIs do it too).
        cl.osh(line)

    def do_createsh(self, line):
        """Creates a new spreadsheet."""
        cl.createsh(line)

    def do_exit(self, line):
        """Exit the command line."""
        return True


if __name__ == "__main__":
    MedSheet().cmdloop()
