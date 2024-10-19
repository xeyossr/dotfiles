from flask import Flask, jsonify, render_template
import requests
import json
from datetime import datetime

app = Flask(__name__)

# Ezan vakitlerini çek ve muezzin.json dosyasına kaydet
def fetch_prayer_times():
    api_url = "https://api.diyanet.gov.tr/vakitler"  # Varsayımsal API
    city = "Istanbul"  # Şehir örneği
    response = requests.get(f"{api_url}/{city}")
    if response.status_code == 200:
        data = response.json()
        with open('data/muezzin.json', 'w') as f:
            json.dump(data, f)
    else:
        print("API'den veri çekilemedi")

# Arayüzü yöneten rota
@app.route('/')
def index():
    return render_template('app.html')

if __name__ == '__main__':
    fetch_prayer_times()
    app.run(debug=True)
