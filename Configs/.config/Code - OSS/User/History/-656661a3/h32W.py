import json
import time
from datetime import datetime
import notify2
import os

# JSON dosyasının bulunduğu dizine geç
os.chdir(os.path.dirname(os.path.abspath(__file__)))

current_dir = os.path.dirname(os.path.abspath(__file__))

notify2.init("Bildirimler")

# Bildirimlerin en son hangi zamanlarda gönderildiğini tutacak sözlük
last_notification_times = {}

def send_notification(task):
    try:
        # Bildirim içeriği
        image_url = task["image_url"]
        n = notify2.Notification(task["name"], task["description"], image_url)
        n.show()
        print(f"Bildirim gönderildi: {task['description']}")
    except Exception as e:
        print(f"Bildirimi gönderirken hata: {e}")

# Zaman kontrol fonksiyonu
def check_time(task_time):
    current_time = datetime.now().strftime("%H:%M")
    return current_time == task_time

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

        # İlk kez çalıştırılıyorsa her görev için last_notification_times'a başlangıç değeri ver
        if task["name"] not in last_notification_times:
            last_notification_times[task["name"]] = None

        # Eğer her gün bildirilecekse
        if task_when == "everyday" and current_hour_minute == task_time:
            if last_notification_times[task["name"]] != current_hour_minute:
                send_notification(task)
                last_notification_times[task["name"]] = current_hour_minute

        # Eğer belirli bir gün bildirilecekse
        elif task_when == current_day and current_hour_minute == task_time:
            if last_notification_times[task["name"]] != current_hour_minute:
                send_notification(task)
                last_notification_times[task["name"]] = current_hour_minute

def run_daemon():
    print("Daemon çalışmaya başladı...")
    last_checked_minute = None

    while True:
        current_minute = datetime.now().strftime("%H:%M")

        # Eğer yeni bir dakikaya girildiyse görevleri kontrol et
        if current_minute != last_checked_minute:
            check_tasks()
            last_checked_minute = current_minute

        # Her saniye döngüyü kontrol et
        time.sleep(1)

if __name__ == "__main__":
    run_daemon()
