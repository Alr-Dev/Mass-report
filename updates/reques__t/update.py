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
            
            return False  
        
        else:
            
            return False

    except Exception as e:
        
        return False
    

        
import time
import requests
from colorama import Fore, Style
from pystyle import Colorate, Colors, Center



def loop_report(game_url, cookies):
    """Continuously report a game until the script is stopped."""
    print(Colorate.Vertical(Colors.purple_to_blue, f"[!] Started loop reporting for: {game_url}"))
    session = requests.Session()
    
    try:
        while True: 
            for selected_cookie in cookies:
                cookie_string = selected_cookie["value"]
                csrf_token = selected_cookie["xcrftoken"]
                
                reported = False
                while not reported:
                    reported = report_game(session, game_url, "This is not good content", csrf_token, cookie_string)
                    
                    if not reported:
                        time.sleep(0)  
    except KeyboardInterrupt:
        print(Colorate.Vertical(Colors.purple_to_blue, "[!] Loop reporting stopped by the user."))

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
    print(Colorate.Vertical(Colors.purple_to_blue, "Version 0.0.2"))
    print(Colorate.Vertical(Colors.purple_to_blue, "Type: request"))
    
    cookies = load_cookies()

    while True:
        command = input(Colorate.Vertical(Colors.purple_to_blue, "[/] Enter command (!loopreport <gamelink> or !exit): "))
        
        if command.startswith("!loopreport"):
            try:
                _, game_url = command.split(" ", 1)
                loop_report(game_url, cookies)
            except ValueError:
                print(Colorate.Vertical(Colors.purple_to_blue, "[!] Invalid command. Usage: !loopreport <gamelink>"))
        elif command == "!exit":
            print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter("[!] Exiting the script. Goodbye!")))
            break
        else:
            print(Colorate.Vertical(Colors.purple_to_blue, "[!] Unknown command. Try again."))

if __name__ == "__main__":
    main()
