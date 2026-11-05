import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def banner():
    print("""
 ██      ██  ██████  ██      ███████ ███████ 
 ██  ██  ██ ██    ██ ██      ██      ██      
 ██ ████ ██ ██    ██ ██      █████   █████   
 ████  ████ ██    ██ ██      ██      ██      
  ██    ██   ██████  ███████ ███████ ███████ 
    """)
    print(" [+] TOOLS: wolferweb")
    print(" [+] OPERATOR: algriom")
    print(" [+] STATUS: Professional Suite Active\n")

def clone_website(url):
    banner()
    print(f"[+] Connecting to Target: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[-] Error: Failed to connect. Status Code: {response.status_code}")
            return
    except Exception as e:
        print(f"[-] Critical Error: {e}")
        return

    parsed_url = urlparse(url)
    folder_name = parsed_url.netloc.replace(":", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        os.makedirs(os.path.join(folder_name, 'assets'))

    html_path = os.path.join(folder_name, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"[+] Core HTML dumped successfully -> {html_path}")

    soup = BeautifulSoup(response.text, 'html.parser')
    resources = {
        'img': 'src',
        'script': 'src',
        'link': 'href'
    }

    print("[+] Harvesting assets (CSS, JS, Images)...")
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

    print(f"\n[✔] Operation Complete! All assets secured in: {folder_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("Enter target website URL: ").strip()
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    clone_website(target_url)
