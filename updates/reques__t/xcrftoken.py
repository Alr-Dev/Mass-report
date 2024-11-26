import requests
import random
import json
import time


def get_random_user_agent():
    with open("saved/storage/agents.txt", "r") as f:
        agents = f.readlines()
    return random.choice(agents).strip()
# here
cookie = 'E4EAE6FC537BCBF3D4274848F67ACC452B56ABB768F71CB0B15B37D602954D700EB1823B5C29E752ADEB12B267237F47ED8C9AF74B0F524F5C9AA677B37783777C0624E0388FF26B6178E3FA9DA84D3E762FB8E541E9DCADFAC6464AAE0DA9CA6FD252A4055BD593BC628356A9797468D9C6960D088A407A479C56DE5D28DC1C7CF27C643606CA097E7099A0FEBD04D0612087A40792FDA041B2B294D577F9A893D9925DCF03DF493E20EDAF416FF80C4468F0BDB5BD4A9591D7DDE3FA0FC34155B9BA587B458A2F4E5BE0358D225A02740456FCBD2B1C27B43D649071995633947F9E2C12AD88561DDC7C0309248BB41495FD8D2AF1A06BF1C121D542FD963B4BC591B3DC949E86DB1F2B2EC8BB9D667083D02B9C9D57022E55DCF79BC98399205B8AC030BA855F676FA82DB2E8B391C04A3053795D15E5EE624067AFE189E5FB2EEFEEBBA3CB3BA59F6BE8EA89F4153D99F8B035991C689082DB3EA1A33A5E27F33AB568236BBEA9FD74E368FF16B936076AF581602BC803EA2AC927394762590A5DCECAA32C9DDEB7A4DBFBBD066F343DC4C58AACD332630B565451E9B0B0B551BAE3ABBFDE991532B41D159FC2855F4A3D9436BD23452D321E19A3D549092E13C8E05E7E30A6F8D6E32A6A0CBACB8C0C9191C808E2DFB72DBD3363D9E452084C53AFC4B47E48288E631D01EACE3B66EF757A88C1937ADA55EF818854F60401372998E900870708CCDDED96CCB290A75C7ADBDCCB6EB2A5474E3C09088E9F2919C131C0FAB52C607A87CB65CFCFF087A03163C818B0B5170B93D64A3550EE3A993CC5A3EBE84B355198CAB35AD70783FB9DC3FC956D2765C56BA43908BCD84F3321ADE49896A0E4602E1BFA30D567DA4C1FCB5EB1193A159E88046FC81C3E55673C4465D84EE2E48BDC254C13413DAE547F9BE0EA46C67C9C4E44902002C9868846676C7E661E5DE2BA15F0B3DB0346B8177B4506260EE09CB5F50AA66264B3A0A68B0E6AA6C774CD3F4DDB4CDAFBF38EB1DA1FCA7D99815F39498CA7BF514C7C7E2062FBF444C11FC7614F9A67949BCF2D507E2D81F0715CC93B55608B8C23DD2F696C8D2EAA4FE80E6B272CBE783126C2E151E09FD606B0C3F3403C1F37B8EAD98865B484B6485DFA27CA68996C7DD2423D78A91A74B95FCC201DBB5F2B87798949'


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
