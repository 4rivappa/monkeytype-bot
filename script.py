import requests
import json

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
    pass

def main():
    curr_streak = get_curr_streak()
    if curr_streak is None:
        return
    saved_data = get_saved_data()

if __name__ == "__main__":
    main()