import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ANSI Color Codes for Hacker Theme
RED = "\033[1;31m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"
BOLD = "\033[1m"

def hacker_matrix_animation():
    os.system('clear' if os.name == 'posix' else 'cls')
    chars = "01ABCDEFHIJKLMNOPQRSTUVWXYZ#$&*@%+-<>\\/|"
    end_time = time.time() + 3  # 3 seconds duration
    
    while time.time() < end_time:
        line = "".join(random.choice(chars) for _ in range(60))
        print(f"{RED}{line}{RESET}")
        time.sleep(0.05)

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(RED + """
██      ██  ██████  ██      ███████ ███████ 
██  ██  ██ ██    ██ ██      ██      ██      
██ ████ ██ ██    ██ ██      █████   █████   
████  ████ ██    ██ ██      ██      ██      
  ██    ██   ██████  ███████ ███████ ███████ 
    """ + RESET)
    print(f"{GREEN} [+] TOOLS: {BOLD}wolferweb{RESET}")
    print(f"{GREEN} [+] OPERATOR: {BOLD}algriom{RESET}")
    print(f"{YELLOW} [+] STATUS: Dangerous Mode Activated [!] {RESET}\n")

def clone_website(url):
    banner()
    print(f"{CYAN}[+] Connecting to Target: {url}{RESET}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"{RED}[-] Error: Failed to connect. Status Code: {response.status_code}{RESET}")
            return
    except Exception as e:
        print(f"{RED}[-] Critical Error: {e}{RESET}")
        return

    parsed_url = urlparse(url)
    folder_name = parsed_url.netloc.replace(":", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        os.makedirs(os.path.join(folder_name, 'assets'))

    html_path = os.path.join(folder_name, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"{GREEN}[+] Core HTML dumped successfully -> {html_path}{RESET}")

    soup = BeautifulSoup(response.text, 'html.parser')
    resources = {
        'img': 'src',
        'script': 'src',
        'link': 'href'
    }

    print(f"{CYAN}[+] Harvesting assets (CSS, JS, Images)...{RESET}")
    for tag, attr in resources.items():
        for element in soup.find_all(tag):
            res_url = element.get(attr)
            if res_url:
                full_url = urljoin(url, res_url)
                try:
                    res_data = requests.get(full_url, headers=headers)
                    if res_data.status_code == 200:
                        res_name = os.path.basename(urlparse(res_url).path)
                        if not res_name:
                            continue
                        res_path = os.path.join(folder_name, 'assets', res_name)
                        with open(res_path, 'wb') as rf:
                            rf.write(res_data.content)
                except Exception:
                    pass

    print(f"\n{GREEN}[✔] Operation Complete! All assets secured in: {folder_name}{RESET}")

if __name__ == "__main__":
    hacker_matrix_animation()
    banner()
    
    target_url = input(f"{YELLOW}[*] Enter target website URL (e.g., https://example.com): {RESET}").strip()
    
    if target_url:
        if not target_url.startswith("http"):
            target_url = "https://" + target_url
        clone_website(target_url)
    else:
        print(f"{RED}[-] Error: URL cannot be empty!{RESET}")
