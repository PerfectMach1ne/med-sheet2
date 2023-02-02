# Origin sheet utilities (so specialized for my own old Google Sheet)
import re

import main

sh_origin = main.gc.open("The Plan") # This is the "origin sheet" on my Google Drive.


def getincidents(printmode):
    worksheet = sh_origin.sheet1
    dates = worksheet.col_values(main.map_column('A'))
    weekdays = worksheet.col_values(main.map_column('B'))
    datalist = list()

    incidents = worksheet.col_values(main.map_column('Y'))  # The Y column/Incidents column
    for date, weekday, incident in zip(dates, weekdays, incidents):
        # zip iterates over several iterables in parallel using tuples
        if printmode:
            if date == 'DATE':
                print(date, 5 * " ", str(weekday).ljust(9, ' '), incident)
                continue
            print(date, weekday.ljust(9, ' '), incident)
        else:
            tup = (date, str(weekday), incident)
            datalist.append(tup)
    if not printmode:
        return datalist


def getiddata(printmode):
    worksheet = sh_origin.sheet1
    dates = worksheet.col_values(main.map_column('A'))
    weekdays = worksheet.col_values(main.map_column('B'))
    datalist = list()

    iddata = worksheet.col_values(main.map_column('Z'))  # The Z column/ID Data column
    for date, weekday, data in zip(dates, weekdays, iddata):
        if printmode:
            if date == 'DATE':
                print(date, 5 * " ", weekday.ljust(9, ' '), data)
                continue
            print(date, weekday.ljust(9, ' '), data)
        else:
            tup = (date, str(weekday), data)
            datalist.append(tup)
    if not printmode:
        return datalist


def validateincidents():
    inclist = getincidents(False)
    inclist.pop(0) # Remove the index with redundant label cell data
    for inc in inclist:
        rex = re.findall(r"E[1-3]=P?\(?[0-2]?\d:[0-5]\d\)?|"  # Catches E[1-3]=hh:mm and E[1-3]=P(hh:mm)
                         r"AA=P?\(?[0-2]?\d:[0-5]\d\)?|"  # Catches AA=hh:mm and AA=P(hh:mm)
                         # P(hh:mm) means there's uncertainty surrounding this hour of intake
                         r"E[1-3]=Pr\([0-2]?\d:[0-5]\d-[0-2]?\d:[0-5]\d\)|"  # Catches  E[1-3]=Pr(hh:mm-hh:mm)
                         r"AA=Pr\([0-2]?\d:[0-5]\d-[0-2]?\d:[0-5]\d\)", inc[2])  # Catches AA=Pr(hh:mm-hh:mm)
                         # P(hh:mm-hh:mm) specifies the time period between which lies the hour of intake
        print(inc[0] + " " + str(rex))


def validateiddata(printmode):
    iddatalist = getiddata(False)
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
    # Note: gspread's get() returns cell data in a matrix, implemented as a list of lists. Example:
    # [['Ibooprofen']]
    worksheet = sh_origin.sheet1

    if printmode:
        print(worksheet.get("C1")[0][0])
        print(worksheet.get("G1")[0][0])
    else:
        return worksheet.get("C1")[0][0], worksheet.get("G1")[0][0]


def getmedinfo(printmode):
    worksheet = sh_origin.sheet1
    dates = worksheet.col_values(main.map_column('A'))
    weekdays = worksheet.col_values(main.map_column('B'))

    if printmode:
        print(12 * '=')
        print('Date'.ljust(10, ' '), 'Weekday'.ljust(9, ' '), "E  ", "AA")
        for date, weekday in zip(dates, weekdays):
            datetup = date.split('/')
            if datetup[0] == 'DATE':
                continue
            if datetup[2] == '2022' and datetup[1] == '05' and (int(datetup[0]) in range(1, 14 + 1)):
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


def exportoshtocsv():
    pass
