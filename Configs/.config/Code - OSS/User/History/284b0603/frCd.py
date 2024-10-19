import json
import time
from datetime import datetime
import notify2
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Bildirim ayarları (Bildirim servisi başlatma)
notify2.init("Görev Bildirimleri")

last_notification_times = {}

def send_notification(task):
    try:
        # Bildirim içeriği
        image_path = os.path.abspath(task["image_url"])
        print(image_path)
        n = notify2.Notification(task["name"], task["description"], task["image_url"])
        n.show()
        print(f"Her gün bildirimi: {task['description']}")
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

        # Görev bilgilerini göster (debug)
        print(f"Görev: {task['name']}, Gün: {task_when}, Zaman: {task_time}")

        # Eğer her gün bildirilecekse
        if task_when == "everyday" and current_hour_minute == task_time:
            if task["name"] not in last_notification_times or last_notification_times[task["name"]] != current_hour_minute:
                send_notification(task['description'], task['image_url'])
            print(f"Her gün bildirimi: {task['description']}")
            send_notification(task['description'], task['image_url'])
        
        # Eğer belirli bir gün bildirilecekse
        elif task_when == current_day and current_hour_minute == task_time:
            print(f"Günlük bildirim: {task['description']}")
            send_notification(task['description'], task['image_url'])

def run_daemon():
    print("Daemon çalışmaya başladı...")
    while True:
        # JSON dosyasını oku
        with open('data.json', 'r') as f:
            tasks = json.load(f)

        # Her bir görevi kontrol et
        for task in tasks:
            task_time = task["time"]
            task_day = task["when"]

            # Eğer "everyday" ise her gün belirtilen saatte bildirimi gönder
            if task_day == "everyday" and check_time(task_time):
                send_notification(task)

            # Eğer belirli bir gün ise, o gün ve saatte bildirimi gönder
            elif task_day == datetime.now().strftime("%A").lower() and check_time(task_time):
                send_notification(task)

            print(f"Görev: {task['name']}, Gün: {task_day}, Zaman: {task_time}")

        # 1 dakika aralıklarla kontrol
        time.sleep(1)

if __name__ == "__main__":
    run_daemon()
