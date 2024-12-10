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

def get_new_logtime(logtime, lockscreen):
	now = datetime.datetime.now()
	logtime = float(logtime)
	end = get_logtime_end_date()
	unlocked = datetime.datetime.strptime(lockscreen, "%Y:%m:%d:%H:%M:%S")
	if unlocked < end and now > end:
		logtime = (now - end).total_seconds()
	else:
		logtime += (now - unlocked).total_seconds()
	return logtime

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

def get_logdata():
	if os.path.exists(LOGPATH):
		with open(LOGPATH, "r") as f:
			logs = f.read().split(" ")
			return logs[0], logs[1]
	else:
		print("No", LOGFILE)
		return 0, ""

def set_logtime(logtime):
	logtime_secs = 0
	with open(LOGPATH, "r") as f:
		lockscreen = f.read().split(" ")[1]
	with open(LOGPATH, "w") as f:
		logtime = logtime.split(":")
		if len(logtime) > 1:
			logtime_secs = int(logtime[0]) * 3600 + int(logtime[1]) * 60
		else:
			logtime_secs = int(logtime[0]) * 3600
		f.write(f"{logtime_secs} {lockscreen}")
		return logtime_secs, lockscreen

def main():
	logtime, lockscreen = get_logdata()
	logtime = get_new_logtime(logtime, lockscreen)
	if len(sys.argv) > 1:
		if sys.argv[1] == "s" or sys.argv[1] == "set":
			logtime, lockscreen = set_logtime(sys.argv[2])
			logtime = get_new_logtime(logtime, lockscreen)
		else:
			logtime = get_logtime_by_date(logtime, sys.argv[1])

	hours = int(logtime // 3600)
	minutes = int(logtime // 60 % 60)
	seconds = int(logtime % 60)
	print(f"{hours:02}:{minutes:02}:{seconds:02} | {(logtime/(120*60*60))*100:.2f}%")

if __name__ == "__main__":
	main()
