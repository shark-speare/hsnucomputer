from datetime import datetime as dt
from datetime import timedelta, date, timezone

format = "%H:%M"
now = dt.strptime("06:30",format).time()
end = dt.strptime("08:10",format).time()
tz = timezone(timedelta(hours=8))

if now >= end:
    now = dt.combine(date.today(),now)
    end = dt.combine(date.today(),end) 
    print(now)
    print(end)

    remaining = (end-now).seconds

# hour = remaining//3600
# remaining -= hour*3600

# minute = remaining//60
# content = f"第1節還剩下: {hour}小時{minute}分鐘"

print(remaining)