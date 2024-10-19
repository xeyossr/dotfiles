import json
import time
from datetime import datetime
import notify2
import os

# JSON dosyasının bulunduğu dizine geç
os.chdir(os.path.dirname(os.path.abspath(__file__)))

current_dir = os.path.dirname(os.path.abspath(__file__))

notify2.init("Bildirimler")

def send_notification(task):
    try:
        # Bildirim içeriği
        image_url = task["image_url"]
        n = notify2.Notification(f"{task["name"]} ürününüzün fiyatı düştü!", f"Şuanki fiyat: ${task["current_price"]}", image_url)
        n.show()
    except Exception as e:
        print(f"Bildirimi gönderirken hata: {e}")


def check_tasks():
    """data.json'dan görevleri kontrol eder ve zamanında bildirimi gönderir"""
    try:
        # data.json dosyasını aç
        with open('data.json', 'r') as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"JSON dosyasını okurken hata: {e}")
        return

    for task in tasks:
        price = task['price'] 
        current_price = task['current_price']  
        if current_price <= price:
            send_notification(task)

def run_daemon():
    print("Daemon çalışmaya başladı...")
    last_checked_minute = None

    while True:
        check_tasks()
        time.sleep(60)

if __name__ == "__main__":
    run_daemon()
