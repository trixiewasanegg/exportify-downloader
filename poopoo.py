
from datetime import datetime

dateTimeObj = datetime.now()

datestamp = dateTimeObj.strftime("%Y-%m-%d")

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


from datetime import datetime

dateTimeObj = datetime.now()

datestamp = dateTimeObj.strftime("%Y-%m-%d")

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


print (days_between(datestamp, '1900-01-01'))