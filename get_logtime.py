import datetime
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

def main():
	logtime = get_new_logtime()
	if logtime == -1:
		print("No logs found.")
		return
	hours = int(logtime // 3600)
	minutes = int(logtime // 60 % 60)
	seconds = int(logtime % 60)
	print(f"{hours:02}:{minutes:02}:{seconds:02} | {(logtime/(120*60*60))*100:.2f}%")

if __name__ == "__main__":
	main()
