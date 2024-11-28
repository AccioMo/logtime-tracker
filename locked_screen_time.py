from Foundation import NSObject, NSDistributedNotificationCenter
from PyObjCTools import AppHelper
import datetime
import objc
import os

def get_current_time():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_to_file(data):
	log_path = os.path.expanduser("~/.screen.log")
	if os.path.exists(log_path):
		with open(log_path, "a") as f:
			f.write(data + "\n")
	else:
		with open(log_path, "w+") as f:
			f.write(data + "\n")

class ScreenLockObserver(NSObject):
	def screenLocked_(self, notification):
		write_to_file("locked " + get_current_time())

	def screenUnlocked_(self, notification):
		write_to_file("unlocked " + get_current_time())

def main():
	observer = ScreenLockObserver.new()
	notification_center = NSDistributedNotificationCenter.defaultCenter()

	# Listen for screen lock and unlock events
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

	print("Listening for screen lock/unlock events...")
	write_to_file("unlocked " + get_current_time())
	AppHelper.runConsoleEventLoop()

if __name__ == "__main__":
	main()
