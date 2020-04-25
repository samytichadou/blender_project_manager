import datetime

def getDateString():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def getDateYearString():
    return datetime.datetime.now().strftime('%Y')

def getDateMonthString():
    return datetime.datetime.now().strftime('%m')

def getDateDayString():
    return datetime.datetime.now().strftime('%d')

def formatDateFromYrMoDa(yr, mo, da):
    return str(yr) + "-" + str(mo).zfill(2) + "-" + str(da).zfill(2)

def returnPriorDate(date_from, date_to):
    fr_yr = int(date_from.split("-")[0])
    fr_mo = int(date_from.split("-")[1])
    fr_da = int(date_from.split("-")[2])
    to_yr = int(date_to.split("-")[0])
    to_mo = int(date_to.split("-")[1])
    to_da = int(date_to.split("-")[2])

    if fr_yr < to_yr:
        return True
    elif fr_yr == to_yr and fr_mo < to_mo:
        return True
    elif fr_yr == to_yr and fr_mo == to_mo and fr_da < to_da:
        return True

    else:
        return False