import requests
import json
from datetime import datetime, timedelta
import os
import telebot
from dotenv import load_dotenv

def get_curr_streak():
    api = "https://api.monkeytype.com/users/4rivappa/profile"
    response = requests.get(api)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        curr_streak = data['data']['streak']
        print(curr_streak)
        return curr_streak
    else:
        return None

def get_saved_data():
    url = "https://raw.githubusercontent.com/4rivappa/monkeytype-bot/data/data.json"
    response = requests.get(url)
    if response.status_code == 200:
        saved_data = json.loads(response.content.decode('utf-8'))
        saved_date = datetime.fromtimestamp(int(saved_data['date']) / 1000)
        saved_streak = int(saved_data['streak'])
        return saved_date, saved_streak
    else:
        return None, None

def create_new_data(timestamp, streak):
    tobe_saved_data = {'date': timestamp, 'streak': streak}

    if not os.path.exists('exports'):
        os.makedirs('exports')
    
    with open('./exports/data.json', "w") as json_file:
        json.dump(tobe_saved_data, json_file, indent=4)
    return

def freakout_ari():
    current_utc = datetime.utcnow() + timedelta(hours=5, minutes=30)
    target_utc = current_utc.replace(hour=5, minute=30, second=0, microsecond=0)
    strength = 0
    if current_utc.hour < 23 and current_utc.hour > 5:
        strength = current_utc.hour - 5
    else:
        strength = current_utc.hour + 24 - 5
    
    for _ in range(strength):
        bot.send_message(chat_id=arivappa_id, text='Nope ..... STREAK')
    return

def intimate_ari():
    bot.send_message(chat_id=arivappa_id, text='You are on STREAK')
    return

def main():
    curr_streak = get_curr_streak()
    if curr_streak is None:
        return
    saved_date, saved_streak = get_saved_data()
    if saved_date is None or saved_streak is None:
        return
    
    if curr_streak == 0:
        freakout_ari()
        create_new_data((datetime.utcnow() + timedelta(hours=5, minutes=30) - timedelta(days=1)).timestamp() * 1000, curr_streak)
        return
    if curr_streak == saved_streak:
        current_utc = datetime.utcnow() + timedelta(hours=5, minutes=30)
        target_utc = current_utc.replace(hour=5, minute=30, second=0, microsecond=0)
        if current_utc < target_utc and (current_utc - saved_date).days < 1:
            intimate_ari()
            create_new_data(saved_date.timestamp() * 1000, curr_streak)
            return
        if current_utc > target_utc and saved_date > target_utc and (current_utc - saved_date).days < 1:
            intimate_ari()
            create_new_data(saved_date.timestamp() * 1000, curr_streak)
            return
        print("success")
        freakout_ari()
        create_new_data(saved_date.timestamp() * 1000, curr_streak)
        return
    if curr_streak == saved_streak + 1:
        intimate_ari()
        create_new_data((datetime.utcnow() + timedelta(hours=5, minutes=30)).timestamp() * 1000, curr_streak)
        return

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    arivappa_id = os.getenv('ARIVAPPA_ID')
    bot = telebot.TeleBot(API_KEY)
    main()
