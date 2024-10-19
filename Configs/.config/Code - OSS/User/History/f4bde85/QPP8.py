from flask import Flask, render_template, jsonify
import json
import zipfile
from io import BytesIO
from PIL import Image
import base64

app = Flask(__name__)

# Manga verilerini yükleme
def load_manga_data():
    with open('database.json') as f:
        return json.load(f)

# CBZ dosyasını okuma
def read_cbz_images(cbz_file_path):
    images = []
    with zipfile.ZipFile(cbz_file_path, 'r') as cbz:
        for file in cbz.namelist():
            if file.endswith(('jpg', 'jpeg', 'png')):
                with cbz.open(file) as img_file:
                    img = Image.open(img_file)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    images.append(f"data:image/png;base64,{img_str}")
    return images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mangas')
def mangas():
    return jsonify(load_manga_data())

@app.route('/manga/<manga_title>')
def manga(manga_title):
    manga_data = load_manga_data()
    for manga in manga_data:
        if manga['title'] == manga_title:
            images = read_cbz_images(manga['file'])
            return jsonify(images)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
