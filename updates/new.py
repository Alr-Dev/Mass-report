import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chromedriver_path = r'webdriver\chromedriver.exe'
cookies_file = r'saved\accounts.json'


options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu') 
options.add_argument('--headless')  
options.add_argument('--no-sandbox') 
options.add_argument('--disable-extensions') 
options.add_argument('--disable-plugins') 
options.add_argument('--disable-images')  

service = Service(chromedriver_path)

def login_and_report(driver, game_url, cookie_string, report_details, username):
    print(f"[!] Login at account: {username}")  
    driver.get("https://www.roblox.com/")

    cookie = {
        "name": ".ROBLOSECURITY",
        "value": cookie_string,
        "domain": "roblox.com",
        "path": "/",
        "httpOnly": True,
        "secure": True
    }
    driver.add_cookie(cookie)
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*")))


    driver.get(game_url)

    try:
       
        link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="game-details-about-tab-container"]/div/div[1]/div[4]/a'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", link_element)
        driver.execute_script("arguments[0].click();", link_element)

       
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportCategory"]'))
        ).click()
        driver.find_element(By.XPATH, '//*[@id="ReportCategory"]/option[8]').click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Comment"]'))
        ).send_keys(report_details)

        
        report_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="report-abuse"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", report_button)
        report_button.click()

        print("[!] Reported game!")
    except Exception as e:
        print(f"[!] Error while reporting: {e}")


def load_cookies(cookies_file):
    with open(cookies_file, 'r') as f:
        return json.load(f)

def main():
    print(r"""
 ███▄ ▄███▓ ▄▄▄        ██████   ██████     ██▀███  ▓█████  ██▓███   ▒█████   ██▀███  ▄▄▄█████▓
▓██▒▀█▀ ██▒▒████▄    ▒██    ▒ ▒██    ▒    ▓██ ▒ ██▒▓█   ▀ ▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒
▓██    ▓██░▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄      ▓██ ░▄█ ▒▒███   ▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░
▒██    ▒██ ░██▄▄▄▄██   ▒   ██▒  ▒   ██▒   ▒██▀▀█▄  ▒▓█  ▄ ▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░ 
▒██▒   ░██▒ ▓█   ▓██▒▒██████▒▒▒██████▒▒   ░██▓ ▒██▒░▒████▒▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░ 
░ ▒░   ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░   ░ ▒▓ ░▒▓░░░ ▒░ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░   
░  ░      ░  ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░     ░▒ ░ ▒░ ░ ░  ░░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░    ░    
░      ░     ░   ▒   ░  ░  ░  ░  ░  ░       ░░   ░    ░   ░░       ░ ░ ░ ▒    ░░   ░   ░      
       ░         ░  ░      ░        ░        ░        ░  ░             ░ ░     ░                  
    """)

    while True:
        game_url = input("[/] Game link: ")

        if game_url.lower() == "!exit":
            print("[+] Finished reportings.")
            break

        print("[!] Started")

 
        driver = webdriver.Chrome(service=service, options=options)

        data = load_cookies(cookies_file)

        for account in data["cookies"]:
            username = account["username"]  
            cookie_string = account["value"]
            login_and_report(driver, game_url, cookie_string, 'not good content', username)
            print(f"[!] Logged in as: {username}")
            print(f"[!] Reported game!")

           
            print("[+] Changing for next cookie:")

        driver.quit()
        print("[+] Finished reporting.\n")
        print("[/] Enter game link or say !exit to exit:")

if __name__ == "__main__":
    main()
