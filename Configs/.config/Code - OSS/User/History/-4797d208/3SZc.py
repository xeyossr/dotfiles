from flask import Flask, render_template, request, redirect, url_for
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
        return redirect(url_for('index'))
    return redirect(url_for('results', username=username))

@app.route('/results/<username>')
def results(username):
    results = {}
    for platform, url_template in platforms.items():
        result = check_username(username, url_template)
        results[platform] = result
    return render_template('results.html', username=username, results=results)

if __name__ == '__main__':
    app.run(debug=True)
