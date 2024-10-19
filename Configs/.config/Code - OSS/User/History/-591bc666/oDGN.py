from flask import Flask, render_template_string
import requests
from flaskwebgui import FlaskUI

app = Flask(__name__)

@app.route('/')
def index():
    # localhost:5000'den HTML içeriğini al
    response = requests.get('http://localhost:5000')
    html_content = response.text
    return render_template_string(html_content)

if __name__ == '__main__':
    # Flask uygulamasını FlaskWebGUI ile çalıştır
    FlaskUI(app).run()
