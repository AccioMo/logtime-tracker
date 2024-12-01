import datetime
import psutil
import calendar
import sys
import os

def get_new_logtime():
	now = datetime.datetime.now()
	log_path = os.path.expanduser("~/.screen.log")
	if os.path.exists(log_path):
		with open(log_path, "r") as f:
			logs = f.read().split(" ")
			logtime = float(logs[0])
			if len(logs) == 1:
				return logtime
			unlocked = datetime.datetime.strptime(logs[1], "%Y:%m:%d:%H:%M:%S")
			logtime += (now - unlocked).total_seconds()
			return logtime
	return -1

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
