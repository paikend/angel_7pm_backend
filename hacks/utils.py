from datetime import datetime, timedelta, date
from pytz import timezone

def move_two_days(date=datetime.now(timezone('Asia/Seoul'))):
  date = datetime.now(timezone('Asia/Seoul')) + timedelta(days=2)
  return date