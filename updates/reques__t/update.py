import requests
import random
import json
import time


def load_cookies():
    with open("saved/accounts.json", "r") as f:
        data = json.load(f)
    return data["cookies"]  


def get_random_user_agent():
    with open("saved/storage/agents.txt", "r") as f:
        agents = f.readlines()
    return random.choice(agents).strip()


def report_game(session, game_url, report_details, csrf_token, cookie_string):
    
    headers = {
        "User-Agent": get_random_user_agent(),
        "X-CSRF-TOKEN": csrf_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

   
    cookies = {
        ".ROBLOSECURITY": cookie_string
    }

    
    game_id = game_url.split("/")[-1]  
    data = {
        "categoryId": 8,  
        "comment": report_details,
        "gameId": game_id,
    }

    try:
        response = session.post(
            "https://www.roblox.com/api/v1/game/report",  
            headers=headers,
            cookies=cookies,
            json=data
        )
        

        if response.status_code == 200:
            print(f"[+] Successfully reported the game: {game_url} using cookie: {cookie_string[:10]}...")
            return True  
        
      
        elif response.status_code == 403:
            print(f"[!] Forbidden (403). Retrying with the same account: {cookie_string[:10]}...")
            return False  
        
        else:
            print(f"[-] Failed to report game: {game_url}. Status code: {response.status_code}")
            return False

    except Exception as e:
        print(f"[!] Error occurred while reporting: {e}")
        return False

print(r"""
 ███▄ ▄███▓ ▄▄▄        ██████   ██████     ██▀███  ▓█████  ██▓███   ▒█████   ██▀███  ▄▄▄█████▓
▓██▒▀█▀ ██▒▒████▄    ▒██    ▒ ▒██    ▒    ▓██ ▒ ██▒▓█   ▀ ▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒
▓██    ▓██░▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄      ▓██ ░▄█ ▒▒███   ▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░
▒██    ▒██ ░██▄▄▄▄██   ▒   ██▒  ▒   ██▒   ░██▀▀█▄  ▒▓█  ▄ ▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░ 
▒██▒   ░██▒ ▓█   ▓██▒▒██████▒▒▒██████▒▒   ░██▓ ▒██▒░▒████▒▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░ 
░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░   ░ ▒▓ ░▒▓░░░ ▒░ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░   
░  ░      ░  ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░     ░▒ ░ ▒░ ░ ░  ░░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░    ░    
░      ░     ░   ▒   ░  ░  ░  ░  ░  ░       ░░   ░    ░   ░░       ░ ░ ░ ▒    ░░   ░   ░      
       ░         ░  ░      ░        ░        ░        ░  ░             ░ ░     ░                  

    """)
print('version 0.0.2')
print('type: request')
cookies = load_cookies()

game_url = input("[/] Game link: ")

print("[!] Started reporting using all available cookies...")

session = requests.Session()

for selected_cookie in cookies:
        cookie_string = selected_cookie["value"]
        csrf_token = selected_cookie["xcrftoken"]
        
        reported = False
        while not reported:
           
            user_input = input("Type '!exit' to stop or press Enter to continue reporting: ")
            if user_input.lower() == "!exit":
                print("[!] Exiting the reporting process.")
                return  
            
            reported = report_game(session, game_url, "This is not good content", csrf_token, cookie_string)
            
            if not reported:
                time.sleep(2)  

if __name__ == "__main__":
    main()