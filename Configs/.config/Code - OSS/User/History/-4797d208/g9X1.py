import requests
from bs4 import *
import flask

def check_username(username, url_template):
    url = url_template.format(username=username)
    response = requests.get(url)
    
    if response.status_code == 200:
        return True  # Kullanıcı var
    else:
        return False  # Kullanıcı yok

platforms = {
    "GitHub": "https://github.com/{username}",
    "Twitter": "https://twitter.com/{username}",
    "Instagram": "https://www.instagram.com/{username}",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
    # Diğer platformlar...
}

username = input("Aramak istediğiniz kullanıcı adı: ")

results = {}

for platform, url_template in platforms.items():
    result = check_username(username, url_template)
    results[platform] = "Mevcut" if result else "Bulunamadı"

for platform, status in results.items():
    print(f"{platform}: {status}")
