from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# File paths
chromedriver_path = r'webdriver\chromedriver.exe'
cookies_file = r'saved\accounts.json'
game_url = "https://www.roblox.com/pt/games/7300121704/Prison-Life-Testing"
report_details = 'not good content'

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu') 
#options.add_argument('--headless')  # Optional: Run in headless mode to speed up without GUI
options.add_argument('--no-sandbox') 
options.add_argument('--disable-extensions') 
options.add_argument('--disable-plugins') 
options.add_argument('--disable-images')  # Disable images to speed up loading

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Load cookies from JSON file
with open(cookies_file, 'r') as f:
    data = json.load(f)

# Function to login and report for each account
def login_and_report(cookie_string):
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

    # Navigate to game page
    driver.get(game_url)

    try:
        # Wait for the report link to be clickable and click it
        link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="game-details-about-tab-container"]/div/div[1]/div[5]/a'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", link_element)
        driver.execute_script("arguments[0].click();", link_element)

        # Select report category and enter details
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ReportCategory"]'))
        ).click()
        driver.find_element(By.XPATH, '//*[@id="ReportCategory"]/option[8]').click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Comment"]'))
        ).send_keys(report_details)

        # Click the report abuse button
        report_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="report-abuse"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", report_button)
        report_button.click()

    except Exception as e:
        print(f"Error while reporting: {e}")

# Iterate through the cookies and execute login and report
for account in data["cookies"]:
    cookie_string = account["value"]
    login_and_report(cookie_string)

# Sleep to keep the browser open to check results or logs
time.sleep(10)
driver.quit()
