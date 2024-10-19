from flask import Flask, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # localhost:5000'den HTML içeriğini al
    response = requests.get('http://localhost:5000')
    html_content = response.text

    # HTML içeriğini render et
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(port=5001)  # Uygulamanı 5001 portunda çalıştır
