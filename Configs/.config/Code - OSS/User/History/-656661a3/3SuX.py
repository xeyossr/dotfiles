import json
import time
from datetime import datetime
import notify2
import os

# JSON dosyasının bulunduğu dizine geç
os.chdir(os.path.dirname(os.path.abspath(__file__)))

notify2.init("Bildirimler")

# Daha önce bildirim gönderilen ürünler için işaretleyici
notified_tasks = {}

def send_notification(task):
    try:
        # Bildirim içeriği
        image_url = task["image_url"]
        n = notify2.Notification(f"{task['name']} ürününüzün fiyatı düştü!", f"Şuanki fiyat: ${task['current_price']}", image_url)
        n.show()
    except Exception as e:
        print(f"Bildirimi gönderirken hata: {e}")

def check_tasks():
    """data.json'dan görevleri kontrol eder ve uygun olursa bildirim gönderir"""
    global notified_tasks
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
        
        # current_price string olarak gelebilir, kontrol ediyoruz
        try:
            current_price = float(current_price)
        except ValueError:
            print(f"Geçersiz fiyat formatı: {current_price} ({task['name']})")
            continue

        # Fiyat eşit veya düşükse ve daha önce bildirim gönderilmediyse
        if current_price <= price and task['id'] not in notified_tasks:
            send_notification(task)
            notified_tasks[task['id']] = True  # Bildirim gönderilen task'ı işaretle

def run_daemon():
    print("Daemon çalışmaya başladı...")

    while True:
        check_tasks()
        time.sleep(60)  # Her 1 dakikada bir çalışır

if __name__ == "__main__":
    run_daemon()
