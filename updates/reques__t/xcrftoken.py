import requests
import random
import json
import time


def get_random_user_agent():
    with open("saved/storage/agents.txt", "r") as f:
        agents = f.readlines()
    return random.choice(agents).strip()
# here
cookie = ''


def load_cookies():
    return [cookie]  

def get_random_user_agent():
    with open("saved/storage/agents.txt", "r") as f:
        agents = f.readlines()
    return random.choice(agents).strip()

def get_xcsrf_token(cookie):
    session = requests.Session()
    user_agent = get_random_user_agent()
    
    
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://www.roblox.com",
        "Referer": "https://www.roblox.com"
    }

    try:
        
        initial_response = session.post(
            "https://auth.roblox.com/v2/logout",
            headers=headers,
            cookies={".ROBLOSECURITY": cookie},
            allow_redirects=True  
        )
        
        
        if 'x-csrf-token' in initial_response.headers:
            headers['X-CSRF-TOKEN'] = initial_response.headers['x-csrf-token']
            print("[+] x-csrf-token:", initial_response.headers['x-csrf-token'])
            return headers
        else:
            print("[!] Error: No x-csrf-token in the response headers")
            return None
    except Exception as e:
        print("[!] Error details:", e)
        return None

def get_token_for_specified_cookie():
    cookie = load_cookies()[0]  
    while True:
        headers = get_xcsrf_token(cookie)
        if headers:
            print("[+] Status: 200")
            break  
        else:
            print("[!] Error, trying another time")
            time.sleep(2) 


get_token_for_specified_cookie()
