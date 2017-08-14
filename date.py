import datetime
# now = datetime.date.today().strftime("%Y/%m/%d")
now = datetime.date.today().strftime("%Y/%m/%d")
print now


import datetime
date = datetime.datetime.strptime('02/19/2013', '%m/%d/%Y')
kl = Dates.query(
    ndb.AND(Dates.date >= date),
            Dates.date < date + datetime.timedelta(days=1))