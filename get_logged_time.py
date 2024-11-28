import datetime
import os

logtime = 0

log_path = os.path.expanduser("~/.screen.log")
if os.path.exists(log_path):
	with open(log_path, "r") as f:
		lines = f.readlines()
		start = datetime.datetime.strptime(lines[0].strip()[7:], "%Y-%m-%d %H:%M:%S")
		end = start
		for line in lines:
			line = line.strip()
			if "unlocked" in line[:8]:
				start = datetime.datetime.strptime(line[9:], "%Y-%m-%d %H:%M:%S")
			elif "locked" in line[:7]:
				end = datetime.datetime.strptime(line[7:], "%Y-%m-%d %H:%M:%S")
				logtime += (end - start).total_seconds()
	if start > end:
		logtime += (datetime.datetime.now() - start).total_seconds()
	print(f"Total time logged: {logtime/60} minutes")