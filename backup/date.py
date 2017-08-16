import datetime
# now = datetime.date.today().strftime("%Y/%m/%d")
now = datetime.date.today().strftime("%Y/%m/%d")
print now


import datetime
date = datetime.datetime.strptime('02/19/2013', '%m/%d/%Y')
# kl = Dates.query(
#     ndb.AND(Dates.date >= date),
#             Dates.date < date + datetime.timedelta(days=1))



# "{{ now.strftime("dd MM yyyy - HH:ii p").split('.')[0] }}"
# 2017-08-14 22:25:08
print str(datetime.datetime.now()).split('.')[0].split('\d*:')

print datetime.datetime.now().strftime("%d-%m-%Y - %H:%I")
print datetime.datetime.now().strftime("%Y-%m-%d - %H:%M")