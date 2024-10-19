from flask import Flask, send_from_directory, request, jsonify, render_template
import os
import json
import requests
from bs4 import BeautifulSoup

def save_task_data(tasks):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

app = Flask(__name__)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# JSON dosyaları
DATA_FILE = 'data.json'
SETTINGS = 'settings.json'

# Eğer dosya yoksa oluştur
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# HTML dosyasını render eder
@app.route('/')
def home():
    return render_template('index.html')

# Verileri işleyen fonksiyon
@app.route('/submit', methods=['POST'])
def submit_form():

    pull()
    print(template)
    name_element = soup.find(class_=templates[template]['name_div'])
    price_element = soup.find(class_=templates[template]['price_div'])
    image_element = soup.find(class_=templates[template]['image_div'])
    name_tag = name_element.find(templates[template]['name_tag'])
    
    if name_element and price_element and image_element:
        # İçeriği al ve HTML etiketlerini kaldır
        name = name_tag.get_text(strip=True)
        price = price_element.get_text(strip=True)
        image_url = image_element.find('img').get('href')

        print(name,price,image_url)
    # Verileri alalım
    url = request.form.get('url')
    price = request.form.get('price')
    #image_url = request.form.get('image_url')
    template = request.form.get('template')

    # Mevcut verileri yükleyelim
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # ID'yi oluşturmak için mevcut en yüksek ID'yi bulalım
    if data:
        max_id = max(task['id'] for task in data)  # En büyük ID'yi bul
        new_max_id = max_id + 1
    else:
        max_id = 0  # Eğer hiç task yoksa, ilk ID 1 olacak
        new_max_id = max_id + 1
    
    # Verileri JSON formatında yazalım
    new_task = {
        'id': new_max_id,
        'url': url,
        'template': template,
        'price': price,
        'image_url': image_url
    }

    print(new_task)
    # Mevcut verileri yükleyelim ve yeni veriyi ekleyelim
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    data.append(new_task)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify({'status': 'success', 'message': 'Veri kaydedildi!'})

# Task'ları JSON dosyasından okuyup frontend'e gönderir
@app.route('/tasks', methods=['GET'])
def get_tasks():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete_task():
    task_id_str = request.json.get('id')
    task_id = int(task_id_str)

    # Verileri yükleyelim ve belirtilen görevi silelim
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Belirtilen görevi bul ve sil
    data = [task for task in data if task['id'] != task_id]
    print(task_id)
    print(type(task_id))

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'status': 'success', 'message': 'Görev silindi!'})

@app.route('/edit-task', methods=['POST'])
def edit_task():
    data = request.json  # Frontend'den gelen verileri al
    task_id = data.get('id')  # Güncellenen task'ın id'sini al
    print(task_id)

    with open('data.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)  # Tüm task'ları yükle

    # Task listesinde düzenlenecek task'ı bul
    for task in tasks:
        if task['id'] == task_id:
            task['url'] = data.get('url')
            task['template'] = data.get('template')
            task['price'] = data.get('price')
            break
    
    # Güncellenen task listesiyle tekrar yaz
    save_task_data(tasks)

    return jsonify({'status': 'success'})


@app.route('/get-task', methods=['GET'])
def get_task():
    with open('data.json') as file:
        tasks = json.load(file)
    return jsonify(tasks)


@app.route('/data.json')
def serve_data():
    try:
        return send_from_directory('', 'data.json')  # Eğer data.json kök dizindeyse
    except Exception as e:
        print(f"Hata: {e}")
        return "Hata oluştu", 500  # Hata mesajı döndür

@app.route('/update', methods=['POST'])
def update_task():
    updated_task = request.json
    # data.json dosyasını oku
    with open('data.json', 'r') as f:
        tasks = json.load(f)

    # Güncellenen görevi bul ve değiştir
    for task in tasks:
        if task['url'] == updated_task['url']:
            task.update(updated_task)
            break

    # Güncellenmiş verileri dosyaya yaz
    with open('data.json', 'w') as f:
        json.dump(tasks, f)

    return jsonify({'status': 'success'})


def pull():
    # Web sayfasını çekin
    response = requests.get(url)

    with open(SETTINGS, 'r') as f:
        templates = json.load(f)

    # Eğer istek başarılıysa
    if response.status_code == 200:
        # HTML içeriğini BeautifulSoup ile analiz edin
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"İstek başarısız oldu: {response.status_code}")




if __name__ == '__main__':
    app.run(port=2000,debug=True)
