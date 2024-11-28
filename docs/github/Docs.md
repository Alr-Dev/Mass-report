# Mass report

This are a python tool script maked for login at accounts from cookie and report a specific game.

---

## Requirements

- Python 3.x
- Selenium (`pip install selenium`)
- ChromeDriver (compatible with the installed Chrome version)
- Cookies saved in JSON format, with each account containing a username and `.ROBLOSECURITY` cookie.

---

## Setup

### 1. Install Required Packages

pip install selenium

### 2. Configure ChromeDriver

- Download ChromeDriver and place it in the `webdriver` folder.
- Update the `chromedriver_path` variable if necessary:

chromedriver_path = r'webdriver\chromedriver.exe'

### 3. Prepare Cookies

Save the Roblox account cookies in JSON format in the `saved` folder, e.g., `accounts.json`:

{
    "cookies": [
        {
            "username": "your_username",
            "value": "your_.ROBLOSECURITY_cookie_here"
        }
    ]
}

---

## Usage

Run the script:

python script_name.py

The script will prompt for the game link to report. Type the URL of the game and press Enter. To exit, type `!exit`.

---

## Code Overview

### `login_and_report(driver, game_url, cookie_string, report_details, username)`

Logs into a Roblox account using a provided `.ROBLOSECURITY` cookie, navigates to the specified game, and submits a report.

#### Parameters:

- `driver`: Selenium WebDriver instance.
- `game_url`: URL of the Roblox game to report.
- `cookie_string`: `.ROBLOSECURITY` cookie string for authentication.
- `report_details`: Text describing the report details.
- `username`: The account's username (used for logging).

#### Workflow:

1. Opens Roblox homepage and adds `.ROBLOSECURITY` cookie.
2. Navigates to the specified game URL.
3. Opens the report dialog, selects the report category, enters a comment, and submits the report.

### `load_cookies(cookies_file)`

Loads account cookies from the specified JSON file.

#### Parameters:

- `cookies_file`: Path to the JSON file containing account cookies.

#### Returns:

- Parsed JSON data containing account cookies.

### `main()`

Main loop for executing the reporting process. Prompts for a game URL and iterates through each account to report the specified game.

#### Workflow:

1. Prompts user for the game URL.
2. For each account in `accounts.json`, logs in and submits a report.
3. Repeats until the user types `!exit`.

---

## Example

python script_name.py

[/] Game link: https://www.roblox.com/games/123456789/Example-Game
[!] Started
[!] Login at account: user1
[!] Reported game!
[+] Changing for next cookie:
[+] Finished reporting.
[/] Enter game link or say !exit to exit:

---

## Notes

- **Cookies**: Ensure the `.ROBLOSECURITY` cookie is valid for each account.
- **Chrome Options**: The script uses headless Chrome mode. Modify `options` as needed.
- **Error Handling**: Basic error handling is included in the `login_and_report` function. Modify for more robust logging or retry logic as needed.

---


## Disclaimer

This tool is intended for educational and ethical purposes only. I dont responsable why how u used this tool.
