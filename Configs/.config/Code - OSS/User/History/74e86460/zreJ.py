from flask import Flask, send_from_directory, request, jsonify, render_template
import os, json, requests, threading, time, re
from bs4 import BeautifulSoup

app = Flask(__name__)

# Dosya yolları
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = 'data.json'
SETTINGS = 'settings.json'

# Eğer data.json dosyası yoksa oluştur
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# JSON dosyasını kaydeden yardımcı fonksiyon
def save_task_data(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# Fiyatları temizleyen ve float'a çeviren fonksiyon
def clean_price(price_str):
    clean_price_str = re.sub(r'[^\d,\.]', '', price_str)
    if ',' in clean_price_str:
        clean_price_str = clean_price_str.replace(',', '.')
    try:
        return float(clean_price_str)
    except ValueError:
        return None

# Ana sayfa render fonksiyonu
@app.route('/')
def home():
    return render_template('index.html')

# Form gönderme ve verileri işleme fonksiyonu
@app.route('/submit', methods=['POST'])
def submit_form():
    url = request.form.get('url')
    template = request.form.get('template')
    price = request.form.get('price')

    # Web sayfasını çek
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'status': 'error', 'message': f"İstek başarısız: {response.status_code}"})

    soup = BeautifulSoup(response.content, 'html.parser')

    with open(SETTINGS, 'r') as f:
        templates = json.load(f)

    # Elementleri bul
    name_element = soup.find(class_=templates[template]['name_class'])
    price_element = soup.find(class_=templates[template]['price_class'])
    image_element = soup.find(class_=templates[template]['image_class'])

    if name_element and price_element and image_element:
        if templates[template]['name_tag_in_class']:
            name_element = name_element.find(templates[template]['name_tag'])

        if templates[template]['image_tag_in_class']:
            image_element = image_element.find(templates[template]['image_tag'])
        
        image_url = image_element.find('img').get('src')
        if templates[template]['image_url_join']:
            image_url = templates[template]['site_url'] + image_url

        if templates[template]['price_tag_in_class']:
            current_price = price_element.find(templates[template]['price_tag']).get_text(strip=True)
        else:
            current_price = price_element.get_text(strip=True)

        # Fiyatı temizle ve float'a dönüştür
        current_price = clean_price(current_price)

        name = name_element.get_text(strip=True) if name_element else "Bilinmeyen"
    else:
        return jsonify({'status': 'error', 'message': 'Gerekli elementler bulunamadı!'})

    # Yeni görev için ID belirle
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    new_id = max([task['id'] for task in data], default=0) + 1

    # Yeni görevi ekle
    new_task = {
        'id': new_id,
        'name': name,
        'url': url,
        'template': template,
        'price': int(price),
        'current_price': current_price,
        'image_url': image_url
    }
    data.append(new_task)
    save_task_data(data)

    return jsonify({'status': 'success', 'message': 'Veri kaydedildi!'})

# Görevleri frontend'e JSON olarak gönderir
@app.route('/tasks', methods=['GET'])
def get_tasks():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

# Görev silme fonksiyonu
@app.route('/delete', methods=['POST'])
def delete_task():
    task_id = int(request.json.get('id'))

    # Verileri yükle ve görevi sil
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    data = [task for task in data if task['id'] != task_id]

    save_task_data(data)
    return jsonify({'status': 'success', 'message': 'Görev silindi!'})

# Görevi düzenleme fonksiyonu
@app.route('/edit-task', methods=['POST'])
def edit_task():
    data = request.json
    task_id = data.get('id')

    with open(DATA_FILE, 'r') as f:
        tasks = json.load(f)

    # Görevi bul ve güncelle
    for task in tasks:
        if task['id'] == task_id:
            task['url'] = data.get('url')
            task['template'] = data.get('template')
            task['price'] = data.get('price')
            break

    save_task_data(tasks)
    return jsonify({'status': 'success'})

# Fiyatları güncelleyen fonksiyon
def update_prices():
    while True:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
            with open(SETTINGS, 'r') as f:
                templates = json.load(f)

            # Her URL için bilgileri güncelle
            for task in tasks:
                url = task['url']
                template = task['template']
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    name_element = soup.find(class_=templates[template]['name_class'])
                    price_element = soup.find(class_=templates[template]['price_class'])
                    image_element = soup.find(class_=templates[template]['image_class'])

                    if name_element and price_element and image_element:
                        name_tag = name_element.find(templates[template]['name_tag'])
                        image_tag = image_element.find(templates[template]['image_tag'])
                        current_price = price_element.get_text(strip=True)
                        
                        # Fiyatı temizle ve float'a dönüştür
                        current_price = clean_price(current_price)

                        # Verileri güncelle
                        task['name'] = name_tag.get_text(strip=True) if name_tag else task['name']
                        task['current_price'] = current_price
                        task['image_url'] = templates[template]['site_url'] + image_tag.find('img').get('src')

            save_task_data(tasks)
        except Exception as e:
            print(f"Fiyat güncelleme hatası: {e}")
        
        time.sleep(60)  # 1 dakika bekle

if __name__ == '__main__':
    # Fiyat güncelleme fonksiyonunu ayrı bir thread'de başlat
    update_thread = threading.Thread(target=update_prices)
    update_thread.daemon = True
    update_thread.start()

    # Flask uygulamasını başlat
    app.run(port=2005, debug=True)
