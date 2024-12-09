import datetime
import psutil
import calendar
import sys
import os

LOGFILE = "~/.screen.log"
LOGPATH = os.path.expanduser(LOGFILE)

def get_logtime_end_date():
	now = datetime.datetime.now()
	month = now.month
	day = now.day
	year = now.year
	if (day >= 28):
		month += 1
	if (month > 12):
		year += 1
		month = 1
	end = datetime.datetime(hour=0, minute=0, second=0, day=28, month=month, year=year)
	return end

def get_new_logtime():
	now = datetime.datetime.now()
	if os.path.exists(LOGPATH):
		with open(LOGPATH, "r") as f:
			logs = f.read().split(" ")
			logtime = float(logs[0])
			end = get_logtime_end_date()
			if len(logs) == 1:
				return logtime
			unlocked = datetime.datetime.strptime(logs[1], "%Y:%m:%d:%H:%M:%S")
			if unlocked < end and now > end:
				logtime = (now - end).total_seconds()
			else:
				logtime += (now - unlocked).total_seconds()
			return logtime
	return 0

def get_logtime_by_date(logtime, date):
	try:
		now = datetime.datetime.now()
		target_time = datetime.datetime.strptime(sys.argv[1], "%H:%M")
		day = now.day
		month = now.month
		year = now.year
		if (now.hour > target_time.hour or (now.hour == target_time.hour and now.minute > target_time.minute)):
			day += 1
		if (day) > calendar.monthrange(now.year, now.month)[1]:
			month += 1
			day = 1
		if month > 12:
			year += 1
			month = 1
		target_time = target_time.replace(year=year, month=month, day=day)
		logtime += (target_time - datetime.datetime.now()).total_seconds()
		return logtime
	except ValueError as e:
		print("Invalid format: use HH:MM")
		exit(1)

def main():
	logtime = get_new_logtime()
	if logtime == -1:
		print("No logs found.")
		return

	if len(sys.argv) > 1:
		logtime = get_logtime_by_date(logtime, sys.argv[1])
	
	hours = int(logtime // 3600)
	minutes = int(logtime // 60 % 60)
	seconds = int(logtime % 60)
	print(f"{hours:02}:{minutes:02}:{seconds:02} | {(logtime/(120*60*60))*100:.2f}%")

if __name__ == "__main__":
	main()
