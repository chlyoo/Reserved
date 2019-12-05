from datetime import datetime, timedelta, time
import calendar
"""
rdate=[0 for i in range(26)]

for day in range(7):
    print("dat")
    for hour in range(9,21,1):
        for min in range(2):
            print(str(hour).zfill(2)+":"+str(30*min).zfill(2))


i= calendar.calendar(datetime.now().year)
print(i)


for hour in range(9,21,1):
    for min in ["00","30"]:
        print(datetime(datetime.today().year,12,1,hour,int(min)))

datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+1])#mon
datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+2])#mon
datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+3])#mon
datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+4])#mon
datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+5])#mon
datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+6])#mon
datetime.today().date()-timedelta(days=datetime.today().isocalendar()[2+7])#mon
"""
d=datetime.today()
print(d.date()-timedelta(days=d.isocalendar()[2]))

print(datetime.today().isocalendar()[1]) #week no
print(datetime.today().isocalendar()[2]) # view start of week
#print(datetime.date(datetime.today()).timedelta-datetime.(3))

print(datetime.strptime("2019-12-04 16:00:00","%Y-%m-%d %H:%M:%S"))