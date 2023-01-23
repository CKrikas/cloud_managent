from datetime import timedelta
from datetime import datetime

stringdate = '2022-12-24T06:56:00Z'
stringdate2 = '2022-12-27T18:39:00Z'
first_time = datetime.strptime(stringdate, '%Y-%m-%dT%H:%M:%SZ')
later_time = datetime.strptime(stringdate2, '%Y-%m-%dT%H:%M:%SZ')
newtime = datetime.now().day
print(newtime)

Current_Date = datetime.today() #432000
print (Current_Date.day)
Previous_Date = datetime.today() - timedelta(days=5)
diff = abs(later_time - Current_Date)
print(diff.total_seconds())
