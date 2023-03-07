# =-=-=-= Origin sheet utilities (so specialized for my own old Google Sheet)
import numpy as np

import re  # Python RegEx module

import main

sh_origin = main.gc.open('The Pillsheet')  # This is the "origin sheet" on my Google Drive.


# Get data from the "standard worksheet" on expected pill; worksheet contains names of all tracked meds, their
# identifiers, optional date at which they are to start getting taken, optional dosage information, dosage change
# info & date of each alteration, optional expected intake hours and changes in said intake hours
def getstd():
    worksheet = sh_origin.get_worksheet(1)
    # TODO, plans: Row 1 & 2 irrelevant
    # column A: medname -> string
    # column B: medid -> string
    # column C: hasstartenddates -> boolean
    # column D: startenddates -> tuple (of dates & a "start-or-end" variable)
    #   empty if colD is False
    # column E: hasdosage -> boolean
    # column F: dosagechanges -> dictionary (of change date & dosage strings)
    #   empty if colE is False
    # column G: hasexpectedhours -> boolean
    #   expected hours that are currently in use; latest date tuple from expectedhourchanges
    # column H: expectedhours -> tuple (of hours)
    #   empty if colG is False
    # column I: expectedhourchanges -> dictionary (of change date & hour tuple tuples)
    #   empty if colG is False
    # put everything in a correct separate variables
    osh_standard = np.array(worksheet.get_all_values()[2:], ndmin=2)
    # print(osh_standard[1][3])
    for elem in np.nditer(osh_standard):
        print(elem)  # TODO: https://numpy.org/doc/stable/reference/arrays.nditer.html#arrays-nditer
        # TODO: then put it into a list/dictionary to return

    return []  # TODO idea: return a list of all data you get from the standard sheet


# Get data from the "incidents" column in original sheet.
# The incidents column stores data on hours & minutes of intake of each medicine in the system.
def getincidents(printmode) -> list:
    worksheet = sh_origin.get_worksheet(0)
    dates = worksheet.col_values(main.map_column('A'))  # Get dates from the A column in origin sheet
    weekdays = worksheet.col_values(main.map_column('B'))  # Get weekdays from the B column in the origin sheet
    datalist = list()  # Initialize an empty list to later return

    incidents = worksheet.col_values(main.map_column('Y'))  # Get incidents from the Y column in the origin sheet
    for date, weekday, incident in zip(dates, weekdays, incidents):
        # zip() iterates over several iterables in parallel using tuples in this use case.
        # But zip() specifically takes iterables (any structure you can iterate over) and aggregates each of their
        # element by shared index in a tuple; it works a bit like the "linear combination without the part where you
        # sum all your vectors" - suppose you have two 3-element lists, sapphics = ['Vi', 'Silva', 'Ayin'] and
        # coffee = ['espresso', 'affogato', 'latte'], then you use zip on them like this:
        # favecoffees = zip(sapphics, coffe)
        # The favecoffees is then a list of tuples:
        # [('Vi', 'espresso'), ('Silva', 'affogato'), ('Ayin', 'latte')]
        # Iterables of various types can be aggregated via zip().
        if printmode:
            # Format all relevant data to be presented in a command line nicely.
            if date == 'DATE':
                # The first row needs special treatment, since it just contains the titles at the top of the sheet.
                print(date, 5 * " ", str(weekday).ljust(9, ' '), incident)
                continue
            print(date, weekday.ljust(9, ' '), incident)
        else:
            # Return all relevant data packed in a tuple without printing it.
            tup = (date, str(weekday), incident)
            datalist.append(tup)
    if not printmode:
        return datalist


# Get data from the "ID data" column in original sheet.
# The ID data column stores weird ID data that tries to give every single pill a "statistical" identifier.
def getiddata(printmode):
    worksheet = sh_origin.get_worksheet(0)
    dates = worksheet.col_values(main.map_column('A'))  # Get dates from the A column in origin sheet
    weekdays = worksheet.col_values(main.map_column('B'))  # Get weekdays from the B column in the origin sheet
    datalist = list()  # Initialize an empty list to later return

    iddata = worksheet.col_values(main.map_column('Z'))  # # Get ID data from the Z column in the origin sheet
    for date, weekday, data in zip(dates, weekdays, iddata):
        # What zip() does exactly has been explained in a getincidents() comment.
        if printmode:
            # Format all relevant data to be presented in a command line nicely.
            if date == 'DATE':
                # The first row needs special treatment, since it just contains the titles at the top of the sheet.
                print(date, 5 * " ", weekday.ljust(9, ' '), data)
                continue
            print(date, weekday.ljust(9, ' '), data)
        else:
            # Return all relevant data packed in a tuple without printing it.
            tup = (date, str(weekday), data)
            datalist.append(tup)
    if not printmode:
        return datalist


# Transform incident data from getincidents() into "functionally useful" data.
def transformincidents():
    inclist = getincidents(False)  # Get a list of incidents (printmode == False)
    inclist.pop(0) # Remove the index with redundant label cell data
    for inc in inclist:
        # According to the standard, here's what each of the 3 incident formats mean with examples:
        # E2=16:17 - 2nd Estradiol pill taken at 16:17
        # AA=P(17:21) - Antiandrogen pill taken probably at 17:21 (there's unspecified uncertainty)
        # M=Pr(23:30-00:15) - Melatonin pill taken anywhere between 23:30 and 00:15
        rex = re.findall(r"E[1-3]=P?\(?[0-2]?\d:[0-5]\d\)?|"  # Catches E[1-3]=hh:mm and E[1-3]=P(hh:mm)
                         r"AA=P?\(?[0-2]?\d:[0-5]\d\)?|"  # Catches AA=hh:mm and AA=P(hh:mm)
                         r"M=P?\(?[0-2]?\d:[0-5]\d\)?|"  # Catches M=hh:mm and M=P(hh:mm)
                         # P(hh:mm) means there's uncertainty surrounding this hour of intake
                         r"E[1-3]=Pr\([0-2]?\d:[0-5]\d-[0-2]?\d:[0-5]\d\)|"  # Catches  E[1-3]=Pr(hh:mm-hh:mm)
                         r"AA=Pr\([0-2]?\d:[0-5]\d-[0-2]?\d:[0-5]\d\)"  # Catches AA=Pr(hh:mm-hh:mm)
                         r"M=Pr\([0-2]?\d:[0-5]\d-[0-2]?\d:[0-5]\d\)"  # Catches M=Pr(hh:mm-hh:mm)
                         # Pr(hh:mm-hh:mm) specifies the time period between which lies the hour of intake
                         , inc[2])

        print(inc[0] + " " + str(rex))


# Transform ID data from getiddata() into "functionally useful" data.
# TODO: 'TypeError' - it doesn't work because of being dependent on getmedinfo(). Revise, document and rewrite.
def transformiddata(printmode):
    iddatalist = getiddata(False)  # Get a list of ID data (printmode == False)
    iddatalist.pop(0)  # Remove the index with redundant label cell data
    if printmode:
        # For the AA meds
        aalist = list()
        for data in iddatalist:
            rex = re.findall(r"A-\d+-\d+CPA", data[2])
            if len(rex) == 1:
                aalist.append(rex[0])
            print(data[0] + " " + str(rex))
        # For the E meds
        elist = list()
        for data in iddatalist:
            rex = re.findall(r"E-\d+-\d+EFM", data[2])
            match (len(rex)):
                case 3:
                    tup = (rex[0], rex[1], rex[2])
                    elist.append(tup)
                case 2:
                    tup = (rex[0], rex[1])
                    elist.append(tup)
                case 1:
                    tup = (rex[0])
                    elist.append(tup)
                case _:
                    pass
            print(data[0] + " " + str(rex))
    else:
        medinfo = getmedinfo(False)
        # For the AA meds
        aalist = list()
        for data in iddatalist:
            rex = re.findall(r"A-\d+-\d+CPA", data[2])
            if len(rex) == 1:
                tup = (data[0], rex[0])
                aalist.append(tup)
        aadosagedata = medinfo[1]
        aa_i = 0
        for i in range(0, len(aadosagedata)):
            if aadosagedata[0] < aalist[aa_i][0] < aadosagedata[1]:
                if aadosagedata[2] == '*':
                    pass
                elif aadosagedata[2] == '/':
                    pass
        # For the E meds
        elist = list()
        for data in iddatalist:
            rex = re.findall(r"E-\d+-\d+EFM", data[2])
            match (len(rex)):
                case 3:
                    tup = (data[0], rex[0], rex[1], rex[2])
                    elist.append(tup)
                case 2:
                    tup = (data[0], rex[0], rex[1])
                    elist.append(tup)
                case 1:
                    tup = (data[0], rex[0])
                    elist.append(tup)
                case _:
                    pass
        edosagedata = medinfo[0]
        for i in range(0, len(edosagedata)):
            pass


def getmeds(printmode):
    # NOTE: gspread's get() returns cell data in a matrix, implemented as a list of lists. Example:
    # [['Iboobprofen']]
    worksheet = sh_origin.get_worksheet(0)

    if printmode:
        print(worksheet.get("C1")[0][0])
        print(worksheet.get("G1")[0][0])
    else:
        return worksheet.get("C1")[0][0], worksheet.get("G1")[0][0]


# TODO: This is a mess that can be handled better by a special sheet with "med standard info" containing all the data on
#  when and how much the medicine should be taken, given IF you have to take it at specific hours to begin with. Also,
#  gotta manually clean up some data. Both the "intake standards" and the old incidents (spare yourself from ID data tho
#  pls plz plssss plzzzzzzzz)
def getmedinfo(printmode):
    worksheet = sh_origin.get_worksheet(0)
    dates = worksheet.col_values(main.map_column('A'))  # Get dates from the A column in origin sheet
    weekdays = worksheet.col_values(main.map_column('B'))  # Get weekdays from the B column in origin sheet

    if printmode:
        print(12 * '=')
        print('Date'.ljust(10, ' '), 'Weekday'.ljust(9, ' '), "E  ", "AA")
        for date, weekday in zip(dates, weekdays):
            datetup = date.split('/')
            if datetup[0] == 'DATE':
                continue
            if datetup[2] == '2022' and datetup[1] == '05' and (int(datetup[0]) in range(1, 14 + 1)):
                # Oh my fucking god I pulled a JavaCalendar there
                # We NEED a new sheet-based standard system pls future me PLS
                if int(datetup[0]) in range(1, 6 + 1):
                    print(date, weekday.ljust(9, ' '), "n/a", end='')
                elif int(datetup[0]) in range(7, 10 + 1):
                    print(date, weekday.ljust(9, ' '), "×1", end='')
                elif int(datetup[0]) in range(11, 14 + 1):
                    print(date, weekday.ljust(9, ' '), "×2", end='')
            else:
                print(date, weekday.ljust(9, ' '), "×3", end='')

            if datetup[2] == '2022' and datetup[1] == '05' and (int(datetup[0]) in range(1, 7 + 1)):
                print(" ÷4")
            else:
                print(" ÷2")
        print(12 * '=')
    else:
        medinfo = list()
        medinfo.append([
            ((5, 1), (5, 6), '*0'),  # Format: tuple = (month, day)
            ((5, 7), (5, 10), '*1'),
            ((5, 11), (5, 14), '*2'),
            ((5, 15), (999, 999), '*3')  # (999, 999) represents no end date
        ])
        medinfo.append([
            ((5, 1), (5, 7), '/4'),
            ((5, 8), (999, 999), '/2')
        ])
        return medinfo


# For future .csv import-export functionality.
# Exports data from spreadsheet into [Google Sheet/variable in memory].
def exportoshtocsv():
    # TODO: Learn pandas for this lol
    pass
