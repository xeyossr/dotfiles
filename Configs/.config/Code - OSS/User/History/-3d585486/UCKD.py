from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

# Kayıtlı verilerin tutulduğu dosya (örn: tasks.json)
DATA_FILE = 'data.json'

# Eğer dosya yoksa oluştur
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Ana sayfa, HTML dosyasını render eder
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
    
    # Dosya kontrolü (image file yükleme)
    if 'image_file' in request.files:
        image_file = request.files['image_file']
        if image_file.filename != '':
            image_path = os.path.join('uploads', image_file.filename)
            image_file.save(image_path)
            image_url = image_path  # URL değilse, dosya yolunu image_url olarak ayarla
    
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

if __name__ == '__main__':
    app.run(debug=True)
