import asyncio
import aiohttp
import random
import json
from pystyle import Colorate, Colors, Center

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

async def report_game(session, game_id, report_details, csrf_token, cookie_string):
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
        async with session.post(url, headers=headers, cookies=cookies, json=data) as response:
            if response.status == 200:
                print(Colorate.Vertical(Colors.purple_to_blue, f"[+] Successfully reported the game: {game_id} using cookie: {cookie_string[:10]}..."))
                return True
            elif response.status == 403:
                return False
            else:
                return False
    except Exception as e:
        return False

async def report_game_thread(session, game_id, cookies, report_details):
    tasks = []
    for selected_cookie in cookies:
        cookie_string = selected_cookie["value"]
        csrf_token = selected_cookie["xcrftoken"]

        task = asyncio.ensure_future(report_game(session, game_id, report_details, csrf_token, cookie_string))
        tasks.append(task)
    
   
    await asyncio.gather(*tasks)

async def loop_report(game_url, cookies):
    print(Colorate.Vertical(Colors.purple_to_blue, f"[!] Started loop reporting for: {game_url}"))
    async with aiohttp.ClientSession() as session:
        try:
            game_id = extract_game_id(game_url)  
        except ValueError as e:
            print(Colorate.Vertical(Colors.red_to_yellow, f"[!] {e}"))
            return

        try:
            while True:
                await report_game_thread(session, game_id, cookies, "This is not good content")
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
    print(Colorate.Vertical(Colors.purple_to_blue, "Type: multi-requests"))
    print(Colorate.Vertical(Colors.purple_to_blue, "WARN: USE A VPN BEFORE USE THIS, U CAN GET BANNED OR IP BLOCKED."))
    cookies = load_cookies()

    while True:
        command = input(Colorate.Vertical(Colors.purple_to_blue, "[/] Enter command (!loopreport <game_url> or !exit): "))

        if command.startswith("!loopreport"):
            try:
                _, game_url = command.split(" ", 1)
                asyncio.run(loop_report(game_url, cookies))
            except ValueError:
                print(Colorate.Vertical(Colors.purple_to_blue, "[!] Invalid command. Usage: !loopreport <game_url>"))
        elif command == "!exit":
            print(Colorate.Horizontal(Colors.purple_to_blue, Center.XCenter("[!] Exiting the script. Goodbye!")))
            break
        else:
            print(Colorate.Vertical(Colors.purple_to_blue, "[!] Unknown command. Try again."))


if __name__ == "__main__":
    main()
