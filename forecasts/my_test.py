import datetime

today = datetime.date.today()
print(type(today), today)

yesterday = today - datetime.timedelta(1)
yesterday = yesterday.strftime('%Y%m%d')

print(type(yesterday), yesterday)

now = datetime.datetime.now()
now_time = now.strftime('%H%M')
print(type(now_time), now_time)

one_hour_ago = now - datetime.timedelta(hours=1)
one_hour_ago = one_hour_ago.strftime('%H%M')
print(type(one_hour_ago), one_hour_ago)