# old api, probably dont working
import requests
import random
import json
import time
from pystyle import Colorate, Colors, Center

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
            print(Colorate.Vertical(Colors.purple_to_blue, f"[+] Successfully reported the game: {game_url} using cookie: {cookie_string[:10]}..."))
            return True  
        
        elif response.status_code == 403:
            print(Colorate.Vertical(Colors.purple_to_blue, f"[!] Forbidden (403). Retrying with the same account: {cookie_string[:10]}..."))
            return False  
        
        else:
            print(Colorate.Vertical(Colors.purple_to_blue, f"[-] Failed to report game: {game_url}. Status code: {response.status_code}"))
            return False

    except Exception as e:
        print(Colorate.Vertical(Colors.purple_to_blue, f"[!] Error occurred while reporting: {e}"))
        return False

def main():
    
    ascii_art = """
███╗░░░███╗░█████╗░░██████╗░██████╗  ██████╗░███████╗██████╗░░█████╗░██████╗░████████╗
████╗░████║██╔══██╗██╔════╝██╔════╝  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
██╔████╔██║███████║╚█████╗░╚█████╗░  ██████╔╝█████╗░░██████╔╝██║░░██║██████╔╝░░░██║░░░
██║╚██╔╝██║██╔══██║░╚═══██╗░╚═══██╗  ██╔══██╗██╔══╝░░██╔═══╝░██║░░██║██╔══██╗░░░██║░░░
██║░╚═╝░██║██║░░██║██████╔╝██████╔╝  ██║░░██║███████╗██║░░░░░╚█████╔╝██║░░██║░░░██║░░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚═════╝░  ╚═╝░░╚═╝╚══════╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░
    """


    print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter(ascii_art)))  

    # 
    print(Colorate.Vertical(Colors.purple_to_blue, "Version 0.0.2"))  


    print(Colorate.Vertical(Colors.purple_to_blue, "Type: request"))

    cookies = load_cookies()

    
    game_url = input(Colorate.Vertical(Colors.purple_to_blue, "[/] Game link: "))

    print(Colorate.Vertical(Colors.purple_to_blue, "[!] Started reporting using all available cookies..."))

    session = requests.Session()

    for selected_cookie in cookies:
        cookie_string = selected_cookie["value"]
        csrf_token = selected_cookie["xcrftoken"]
        
        reported = False
        while not reported:
            reported = report_game(session, game_url, "This is not good content", csrf_token, cookie_string)
            
            if not reported:
                time.sleep(0)  

    
    user_input = input(Colorate.Vertical(Colors.purple_to_blue, "All accounts have finished reporting. Type '!exit' to stop or press Enter to exit: "))
    if user_input.lower() == "!exit":
        print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter("[!] Exiting the reporting process.")))  
        return  

if __name__ == "__main__":
    main()