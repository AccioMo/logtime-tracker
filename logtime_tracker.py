from Foundation import NSObject, NSDistributedNotificationCenter
from PyObjCTools import AppHelper
import datetime
import psutil
import objc
import os

LOGFILE = "~/.screen.log"
LOGPATH = os.path.expanduser(LOGFILE)

def is_script_running(script_name):
	current_pid = os.getpid()
	for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
		try:
			if proc.info['pid'] != current_pid and proc.info['cmdline'] != None and any(script_name in cmd for cmd in proc.info['cmdline']):
				print(f"Script is already running with PID: {proc.info['pid']}")
				return True
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return False

def get_current_time():
	return datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")

def get_logtime():
	if os.path.exists(LOGPATH):
		with open(LOGPATH, "r") as f:
			return float(f.read().split(" ")[0])
	else:
		return 0

def get_new_logtime():
	now = datetime.datetime.now()
	if os.path.exists(LOGPATH):
		with open(LOGPATH, "r") as f:
			logs = f.read().split(" ")
			logtime = float(logs[0])
			if len(logs) == 1:
				return logtime
			unlocked = datetime.datetime.strptime(logs[1], "%Y:%m:%d:%H:%M:%S")
			logtime += (now - unlocked).total_seconds()
	return logtime

class ScreenLockObserver(NSObject):
	def screenLocked_(self, notification):
		logtime = get_new_logtime()
		with open(LOGPATH, "w") as f:
			f.write(f"{logtime}")

	def screenUnlocked_(self, notification):
		logtime = get_logtime()
		with open(LOGPATH, "w") as f:
			f.write(f"{logtime} {get_current_time()}")

	def userLoggedOut_(self, notification):
		logtime = get_new_logtime()
		with open(LOGPATH, "w") as f:
			f.write(f"{logtime}")

def main():
	if is_script_running("logtime_tracker.py"):
		return
	observer = ScreenLockObserver.new()
	notification_center = NSDistributedNotificationCenter.defaultCenter()

	notification_center.addObserver_selector_name_object_(
		observer,
		"screenLocked:",
		"com.apple.screenIsLocked",
		None,
	)
	notification_center.addObserver_selector_name_object_(
		observer,
		"screenUnlocked:",
		"com.apple.screenIsUnlocked",
		None,
	)
	notification_center.addObserver_selector_name_object_(
		observer,
		"userLoggedOut:",
		"com.apple.logoutInitiated",
		None,
	)

	print("Listening for screen lock/unlock events...")
	logtime = get_logtime()
	with open(LOGPATH, "w") as f:
		f.write(f"{logtime} {get_current_time()}")
	AppHelper.runConsoleEventLoop()

if __name__ == "__main__":
	main()
