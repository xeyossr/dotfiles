from flask import Flask, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

platforms = {
    "GitHub": "https://github.com/{username}",
    "Twitter": "https://twitter.com/{username}",
    "Instagram": "https://www.instagram.com/{username}",
    "LinkedIn": "https://www.linkedin.com/in/{username}",
}

def check_username(username, url_template):
    url = url_template.format(username=username)
    response = requests.get(url)
    return response.status_code == 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('username')
    
    if not username:
        return jsonify({"error": "Username not provided"}), 400
    
    # Arama işlemi tamamlandığında redirect
    return redirect(url_for('results', username=username))

@app.route('/results/<username>')
def results(username):
    results = {}
    
    for platform, url_template in platforms.items():
        result = check_username(username, url_template)
        results[platform] = result
    
    # Sonuçları HTML ile kullanıcıya gösterme
    result_str = f"<h1>{username} için arama sonuçları</h1>"
    for platform, status in results.items():
        status_text = "Mevcut" if status else "Bulunamadı"
        result_str += f"<p><strong>{platform}</strong>: {status_text}</p>"
    
    return result_str

if __name__ == '__main__':
    app.run(debug=True)
