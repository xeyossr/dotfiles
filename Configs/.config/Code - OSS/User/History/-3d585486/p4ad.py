from flask import Flask, send_from_directory, request, jsonify, render_template
import os
import json

def save_task_data(tasks):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

app = Flask(__name__)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Kayıtlı verilerin tutulduğu dosya (örn: tasks.json)
DATA_FILE = 'data.json'

# Eğer dosya yoksa oluştur
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# HTML dosyasını render eder
@app.route('/')
def home():
    return render_template('index.html')

# Formdan gelen verileri işleyen fonksiyon
@app.route('/submit', methods=['POST'])
def submit_form():
    # Formdan gelen verileri alalım
    name = request.form.get('name')
    description = request.form.get('description')
    image_url = request.form.get('image_url')  # URL ya da dosya olabilir
    when = request.form.get('when')
    time = request.form.get('time')  # saat ve dakika kısmı

    # Mevcut verileri yükleyelim
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # ID'yi oluşturmak için mevcut en yüksek ID'yi bulalım
    if data:
        max_id = max(task['id'] for task in data)  # En büyük ID'yi bul
        new_max_id = max_id + 1
    else:
        max_id = 0  # Eğer hiç task yoksa, ilk ID 1 olacak
    
    # Dosya kontrolü (image file yükleme)
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file.filename != '':
            # uploads klasörü yoksa oluştur
            if not os.path.exists('static/uploads'):
                os.makedirs('static/uploads')

            image_path = os.path.join('static/uploads', image_file.filename)
            image_file.save(image_path)
            image_url = f"/static/uploads/{image_file.filename}"  # Sunucu yolu ile URL oluştur
            
    # Verileri JSON formatında yazalım
    new_task = {
        'id': new_max_id,
        'name': name,
        'description': description,
        'image_url': image_url,
        'when': when,
        'time': time
    }

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
            task['name'] = data.get('name')
            task['description'] = data.get('description')
            task['image_url'] = data.get('image_url')
            task['when'] = data.get('when')
            task['time'] = data.get('time')
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
        if task['name'] == updated_task['name']:
            task.update(updated_task)
            break

    # Güncellenmiş verileri dosyaya yaz
    with open('data.json', 'w') as f:
        json.dump(tasks, f)

    return jsonify({'status': 'success'})



if __name__ == '__main__':
    app.run(debug=True)
