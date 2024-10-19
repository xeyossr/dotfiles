import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Hedef URL
url = 'http://localhost:5000'

# URL'den HTML içeriğini çek
response = requests.get(url)
html_content = response.text

# BeautifulSoup ile HTML içeriğini parse et
soup = BeautifulSoup(html_content, 'html.parser')

# CSS ve JS dosyalarını bul
css_files = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
js_files = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs]

# Dosyaları kaydetmek için klasör oluştur
output_dir = 'downloaded_assets'
os.makedirs(output_dir, exist_ok=True)

# HTML dosyasını kaydet
with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
    file.write(soup.prettify())

# CSS dosyalarını kaydet
for css_file in css_files:
    css_url = urljoin(url, css_file)
    css_response = requests.get(css_url)
    css_filename = os.path.join(output_dir, os.path.basename(css_file))
    with open(css_filename, 'w', encoding='utf-8') as file:
        file.write(css_response.text)

# JS dosyalarını kaydet
for js_file in js_files:
    js_url = urljoin(url, js_file)
    js_response = requests.get(js_url)
    js_filename = os.path.join(output_dir, os.path.basename(js_file))
    with open(js_filename, 'w', encoding='utf-8') as file:
        file.write(js_response.text)

print('Tüm içerik başarıyla kaydedildi!')
