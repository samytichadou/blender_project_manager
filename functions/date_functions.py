import datetime

def getDateString():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def getDateYearString():
    return datetime.datetime.now().strftime('%Y')

def getDateMonthString():
    return datetime.datetime.now().strftime('%m')

def getDateDayString():
    return datetime.datetime.now().strftime('%d')
