import datetime

def getDateString():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def getDateYearString():
    return datetime.datetime.now().strftime('%Y')
