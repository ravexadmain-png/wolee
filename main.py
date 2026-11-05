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

def cinematic_hacker_intro():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    logs = [
        "Initializing kernel exploit...",
        "Bypassing firewall security layers...",
        "Injecting malicious payload into target cluster...",
        "Establishing encrypted socket connection...",
        "Access Granted: Welcome to Wolee Secure Enclave..."
    ]
    
    for log in logs:
        print(f"{RED}[!] {log}{RESET}")
        time.sleep(0.3)
    
    time.sleep(0.5)
    os.system('clear' if os.name == 'posix' else 'cls')

    chars = "01ABCDEFHIJKLMNOPQRSTUVWXYZ#$&*@%+-<>\\/|§¶"
    end_time = time.time() + 3.5
    
    while time.time() < end_time:
        chunk = ""
        for _ in range(3):
            line = "".join(random.choice(chars) for _ in range(50))
            chunk += f"{RED}{line}{RESET}\n"
        print(chunk, end="")
        time.sleep(0.04)
        
    os.system('clear' if os.name == 'posix' else 'cls')

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
    print(f"{YELLOW} [+] STATUS: Elite Hacker Mode Active [!] {RESET}\n")

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
    
    # Check and setup Phone Storage path (Download Folder)
    phone_download_path = os.path.expanduser("~/storage/shared/Download")
    if os.path.exists(phone_download_path):
        target_dir = os.path.join(phone_download_path, folder_name)
    else:
        target_dir = folder_name # Fallback to local if storage permission not given

    assets_dir = os.path.join(target_dir, 'assets')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        os.makedirs(assets_dir)

    html_path = os.path.join(target_dir, 'index.html')
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
                        res_path = os.path.join(assets_dir, res_name)
                        with open(res_path, 'wb') as rf:
                            rf.write(res_data.content)
                except Exception:
                    pass

    print(f"\n{GREEN}[✔] Operation Complete! Saved directly to Phone Storage -> Download/{folder_name}{RESET}")

if __name__ == "__main__":
    cinematic_hacker_intro()
    banner()
    
    target_url = input(f"{YELLOW}[*] Enter target website URL (e.g., https://example.com): {RESET}").strip()
    
    if target_url:
        if not target_url.startswith("http"):
            target_url = "https://" + target_url
        clone_website(target_url)
    else:
        print(f"{RED}[-] Error: URL cannot be empty!{RESET}")
