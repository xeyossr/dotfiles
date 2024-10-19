import json
import time
from datetime import datetime
import notify2
import os

# Bildirim ayarları (Bildirim servisi başlatma)
notify2.init("Görev Bildirimleri")

def send_notification(description, image_url):
    """Bildirimi gönderir"""
    try:
        n = notify2.Notification("Görev Zamanı", description)
        n.set_icon(image_url)  # Resim önizlemesi
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

    current_time = datetime.now()
    current_hour_minute = current_time.strftime("%H:%M")  # 'HH:MM' formatında zaman
    current_day = current_time.strftime("%A").lower()  # Hafta gününü küçük harflerle al

    for task in tasks:
        task_time = task['time']  # 'HH:MM' formatında
        task_when = task['when']  # "everyday" ya da bir hafta günü

        # Görev bilgilerini göster (debug)
        print(f"Görev: {task['name']}, Gün: {task_when}, Zaman: {task_time}")

        # Eğer her gün bildirilecekse
        if task_when == "everyday" and current_hour_minute == task_time:
            print(f"Her gün bildirimi: {task['description']}")
            send_notification(task['description'], task['image_url'])
        
        # Eğer belirli bir gün bildirilecekse
        elif task_when == current_day and current_hour_minute == task_time:
            print(f"Günlük bildirim: {task['description']}")
            send_notification(task['description'], task['image_url'])

def run_daemon():
    """Daemon'ı çalıştırır ve her dakika görevleri kontrol eder"""
    print("Daemon çalışmaya başladı...")
    while True:
        check_tasks()  # Görevleri her dakika kontrol et
        time.sleep(60)  # Bir dakika bekle

if __name__ == "__main__":
    run_daemon()
