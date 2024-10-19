from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Platformlar ve kullanıcı URL şablonları
platforms = {
    "GitHub": "https://github.com/{username}",
    "Twitter": "https://twitter.com/{username}",
    "Instagram": "https://www.instagram.com/{username}",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
}

# Kullanıcı adını kontrol eden fonksiyon
def check_username(username, url_template):
    url = url_template.format(username=username)
    try:
        response = requests.get(url)
        return response.status_code == 200  # Eğer 200 dönerse kullanıcı adı mevcut
    except Exception as e:
        return False

# Ana sayfa: HTML arayüzü render ediyor
@app.route('/')
def index():
    return render_template('index.html')

# Arama işlemi ve sonuçların JSON olarak geri dönülmesi
@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('username')
    
    if not username:
        return jsonify({"error": "Username not provided"}), 400
    
    results = {}
    
    for platform, url_template in platforms.items():
        result = check_username(username, url_template)
        results[platform] = result
    
    return jsonify(results)  # JSON olarak sonuçları frontend'e dön

if __name__ == '__main__':
    app.run(debug=True)
