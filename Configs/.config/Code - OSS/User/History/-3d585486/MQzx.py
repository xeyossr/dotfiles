from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

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
@app.route('/submit', methods=['POST'])
def submit_form():
    # Formdan gelen verileri alalım
    name = request.form.get('name')
    description = request.form.get('description')
    image_url = request.form.get('image_url')  # URL ya da dosya olabilir
    when = request.form.get('when')
    time = request.form.get('time')  # saat ve dakika kısmı
    
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

    # Dosya kontrolü (image file yükleme)
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file.filename != '':
            # uploads klasörü yoksa oluştur
            if not os.path.exists('static/uploads'):
                os.makedirs('static/uploads')

            # Tam dosya yolunu oluştur
            image_path = os.path.abspath(os.path.join('static/uploads', image_file.filename))
            image_file.save(image_path)
            
            # `image_url` olarak tam dosya yolunu `data.json`'a kaydederiz
            image_url = image_path  # Sunucu yolu yerine tam dosya yolunu alıyoruz

            
    # Verileri JSON formatında yazalım
    new_task = {
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
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'status': 'success', 'message': 'Veri kaydedildi!'})

# Task'ları JSON dosyasından okuyup frontend'e gönderir
@app.route('/tasks', methods=['GET'])
def get_tasks():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete_task():
    task_name = request.json.get('name')

    # Verileri yükleyelim ve belirtilen görevi silelim
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Belirtilen görevi bul ve sil
    data = [task for task in data if task['name'] != task_name]

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'status': 'success', 'message': 'Görev silindi!'})


@app.route('/update', methods=['POST'])
def update_task():
    old_name = request.json.get('oldName')
    new_task = request.json.get('newTask')

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Eski görevi bul ve güncelle
    for task in data:
        if task['name'] == old_name:
            task.update(new_task)
            break

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'status': 'success', 'message': 'Görev güncellendi!'})


if __name__ == '__main__':
    app.run(debug=True)
