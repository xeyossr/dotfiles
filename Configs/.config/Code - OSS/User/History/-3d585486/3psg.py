from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-task', methods=['POST'])
def add_task():
    # Form verilerini al
    name = request.form['name']
    description = request.form['description']
    when = request.form['when']
    
    # Resim dosyası varsa kaydet
    image_file = request.files.get('image')
    image_path = None
    if image_file:
        image_path = os.path.join('static', 'uploads', image_file.filename)
        image_file.save(image_path)
    
    task = {
        'name': name,
        'description': description,
        'image': image_path,
        'when': when
    }
    
    # Görevi JSON dosyasına yaz
    with open('tasks.json', 'r+') as file:
        tasks = json.load(file)
        tasks.append(task)
        file.seek(0)
        json.dump(tasks, file, indent=4)

    return jsonify(task)

if __name__ == '__main__':
    # Eğer JSON dosyası yoksa oluştur
    if not os.path.exists('tasks.json'):
        with open('tasks.json', 'w') as file:
            json.dump([], file)
    app.run(debug=True)
