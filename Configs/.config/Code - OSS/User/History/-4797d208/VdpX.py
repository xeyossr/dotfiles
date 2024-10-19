from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

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

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username not provided"}), 400
    
    results = {}
    
    for platform, url_template in platforms.items():
        result = check_username(username, url_template)
        results[platform] = result
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
