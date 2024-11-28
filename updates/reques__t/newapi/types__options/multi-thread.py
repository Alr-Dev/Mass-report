import requests
import random
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pystyle import Colorate, Colors, Center
max_w = 20 # Change based on your systems capabilities
def load_cookies():
    with open("saved/accounts.json", "r") as f:
        data = json.load(f)
    return data["cookies"]  


def get_random_user_agent():
    with open("saved/storage/agents.txt", "r") as f:
        agents = f.readlines()
    return random.choice(agents).strip()

def extract_game_id(game_url):
    try:
        return game_url.split("/games/")[1].split("/")[0]
    except IndexError:
        raise ValueError("Invalid game URL format. Please provide a valid Roblox game link.")

def report_game(session, game_id, report_details, csrf_token, cookie_string):
    headers = {
        "User-Agent": get_random_user_agent(),
        "X-CSRF-TOKEN": csrf_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    cookies = {
        ".ROBLOSECURITY": cookie_string
    }

    url = f"https://www.roblox.com/pt/abusereport/asset?id={game_id}"
    data = {
        "categoryId": 8,  
        "comment": report_details
    }

    try:
        response = session.post(url, headers=headers, cookies=cookies, json=data)

        if response.status_code == 200:
            print(Colorate.Vertical(Colors.purple_to_blue, f"[+] Successfully reported the game: {game_id} using cookie: {cookie_string[:10]}..."))
            return True
        elif response.status_code == 403:
            return False
        else:
            return False
    except Exception as e:
        return False


def report_game_thread(session, game_id, cookies, report_details):
    for selected_cookie in cookies:
        cookie_string = selected_cookie["value"]
        csrf_token = selected_cookie["xcrftoken"]

        reported = False
        while not reported:
            reported = report_game(session, game_id, report_details, csrf_token, cookie_string)

            if not reported:
                time.sleep(0)

def loop_report(game_url, cookies):
    print(Colorate.Vertical(Colors.purple_to_blue, f"[!] Started loop reporting for: {game_url}"))
    session = requests.Session()

    try:
        game_id = extract_game_id(game_url)  
    except ValueError as e:
        print(Colorate.Vertical(Colors.red_to_yellow, f"[!] {e}"))
        return

    try:

        with ThreadPoolExecutor(max_workers=max_w) as executor:  
            futures = []
            for i in range(len(cookies)): 
                future = executor.submit(report_game_thread, session, game_id, cookies, "This is not good content")
                futures.append(future)

            
            for future in futures:
                future.result()  

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
    print(Colorate.Vertical(Colors.purple_to_blue, "Version 0.0.3"))
    print(Colorate.Vertical(Colors.purple_to_blue, "Type: multi-thread"))
    print(Colorate.Vertical(Colors.purple_to_blue, "WARN: USE A VPN BEFORE USE THIS, U CAN GET BANNED OR IP BLOCKED."))
    cookies = load_cookies()

    while True:
        command = input(Colorate.Vertical(Colors.purple_to_blue, "[/] Enter command (!loopreport <game_url> or !exit): "))

        if command.startswith("!loopreport"):
            try:
                _, game_url = command.split(" ", 1)
                loop_report(game_url, cookies)
            except ValueError:
                print(Colorate.Vertical(Colors.purple_to_blue, "[!] Invalid command. Usage: !loopreport <game_url>"))
        elif command == "!exit":
            print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter("[!] Exiting the script. Goodbye!")))
            break
        else:
            print(Colorate.Vertical(Colors.purple_to_blue, "[!] Unknown command. Try again."))


if __name__ == "__main__":
    main()
