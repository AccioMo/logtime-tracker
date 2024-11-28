import requests
import dotenv
import json
import datetime
import time
import os

CLIENT_ID = dotenv.get_key('.env', 'CLIENT_ID')
CLIENT_SECRET = dotenv.get_key('.env', 'CLIENT_SECRET')

def get_current_date():
	start_date = datetime.datetime.now()
	if (start_date.day < 28):
		start_date.replace(month=start_date.month-1)
	start_date = start_date.replace(day=28)
	end_date = start_date.replace(month=start_date.month+1)
	return f"{start_date.strftime('%Y-%m-%d')}T00:00:00.000Z", f"{end_date.strftime('%Y-%m-%d')}T00:00:00.000Z"

def get_access_token():
	response = requests.post('https://api.intra.42.fr/oauth/token', {
	'grant_type': 'client_credentials',
	'client_id': CLIENT_ID,
	'client_secret': CLIENT_SECRET,
	})
	response.raise_for_status()
	return response.json()['access_token']

def get_campus_id(campus_name, access_token):
	response = requests.get(f"https://api.intra.42.fr/v2/campus?filter[name]={campus_name}", 
		headers={"Authorization": "Bearer " + access_token})
	if response.status_code == 200:
		return (response.json()[0]["id"])
	else:
		return (f"Error: {response.status_code}")

def get_user_id(username, access_token):
	response = requests.get(f"https://api.intra.42.fr/v2/users?filter[login]={username}", 
		headers={"Authorization": "Bearer " + access_token})
	if response.status_code == 200:
		return (response.json()[0]["id"])
	else:
		return (f"Error: {response.status_code}")

def get_logged_time(user_id, access_token):
	start_date, end_date = get_current_date()
	response = requests.get(f"https://api.intra.42.fr/v2/locations?filter[user_id]={user_id}&range[begin_at]={start_date},{end_date}", 
		headers={"Authorization": "Bearer " + access_token})
	print(f"https://api.intra.42.fr/v2/locations?filter[user_id]={user_id}&range[begin_at]={start_date},{end_date}")
	if response.status_code == 200:
		return (response.json())
	else:
		return (f"Error: {response.status_code}")

def calculate_logged_time(data):
	total_time = 0
	for i in data:
		start_date = datetime.datetime.strptime(i["begin_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
		if i["end_at"]:
			end_date = datetime.datetime.strptime(i["end_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
		else:
			end_date = datetime.datetime.now()
		total_time += (end_date - start_date).total_seconds()
	print(f"Total time logged: {total_time/3600} hours")

def write_to_file(log_path, data):
	if ('~' in log_path):
		log_path = os.path.expanduser(log_path)
	if os.path.exists(log_path):
		print("File exists")
		with open(log_path, "a") as f:
			f.write(data + "\n")
	else:
		with open(log_path, "w+") as f:
			f.write(data + "\n")

access_token = get_access_token()
time.sleep(0.2)
campus_id = get_campus_id("Khouribga", access_token)
time.sleep(0.2)
user_id = get_user_id("mzeggaf", access_token)
time.sleep(0.2)
data = get_logged_time(user_id, access_token)
calculate_logged_time(data)

write_to_file("log", "Screen locked: " + get_current_date()[0])

# with open("data.json", "w") as f:
# 	json_data = json.dumps(data)
# 	f.write(json_data)

# print(f"{get_current_date()}")