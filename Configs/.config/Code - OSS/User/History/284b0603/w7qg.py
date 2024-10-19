import json
import schedule
import time
import notify2
from datetime import datetime

# Bildirim ayarları
notify2.init("Görev Bildirimleri")

def send_notification(description, image_url):
    # Bildirim oluşturma
    n = notify2.Notification("Görev Zamanı", description)
    n.set_icon(image_url)  # Resim önizlemesi
    n.show()

def check_tasks():
    # Görevleri yükle
    with open('data.json', 'r') as f:
        tasks = json.load(f)

    current_time = datetime.now()
    current_day = current_time.strftime("%A")  # Hafta günü

    for task in tasks:
        # Zaman kontrolü
        task_time = task['time']
        task_when = task['when']

        # Gün kontrolü
        if task_when == "Every day":
            schedule_time = task_time
        elif task_when == current_day:
            schedule_time = task_time
        else:
            continue  # Diğer günleri atla

        # Şu anki zamanla karşılaştırma
        if current_time.strftime("%H:%M") == schedule_time:
            send_notification(task['description'], task['image_url'])

def run_daemon():
    schedule.every(1).minutes.do(check_tasks)  # Her dakika kontrol et

    while True:
        schedule.run_pending()
        time.sleep(1)  # 1 saniye bekle

if __name__ == "__main__":
    run_daemon()
