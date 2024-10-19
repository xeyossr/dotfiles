import json
import schedule
import time
import notify2
from datetime import datetime

# Bildirim ayarları
notify2.init("Görev Bildirimleri")

def send_notification(description, image_url):
    try:
        n = notify2.Notification("Görev Zamanı", description)
        n.set_icon(image_url)  # Resim önizlemesi
        n.show()
    except Exception as e:
        print(f"Bildirimi gönderirken hata: {e}")

def check_tasks():
    try:
        with open('data.json', 'r') as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"JSON dosyasını okurken hata: {e}")
        return

    current_time = datetime.now()
    current_day = current_time.strftime("%A")  # Hafta günü

    for task in tasks:
        task_time = task['time']
        task_when = task['when']

        # Zaman kontrolü
        if task_when == "Every day":
            schedule_time = task_time
        elif task_when == current_day:
            schedule_time = task_time
        else:
            continue

        if current_time.strftime("%H:%M") == schedule_time:
            send_notification(task['description'], task['image_url'])

def run_daemon():
    schedule.every(1).minutes.do(check_tasks)  # Her dakika kontrol et

    while True:
        schedule.run_pending()
        time.sleep(1)  # 1 saniye bekle

if __name__ == "__main__":
    run_daemon()
