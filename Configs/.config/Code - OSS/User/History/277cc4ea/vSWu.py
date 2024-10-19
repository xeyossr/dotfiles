import psutil
import time

def get_processes_by_name(task_names):
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in task_names:
            processes.append(proc)
    return processes

def print_process_info(processes):
    print(f"{'PID':<10}{'TASK NAME':<20}{'CPU (%)':<10}{'MEMORY (MB)':<15}")
    print("-" * 55)
    for process in processes:
        try:
            cpu_usage = process.cpu_percent(interval=1)
            memory_usage = process.memory_info().rss / (1024 * 1024)
            print(f"{process.pid:<10}{process.name():<20}{cpu_usage:<10}{memory_usage:.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(f"{process.pid:<10}{process.name():<20}{'N/A':<10}{'N/A':<15}")

if __name__ == "__main__":
    task_names = input("Enter task names (comma separated): ").split(',')
    task_names = [task.strip() for task in task_names]  # İsimleri temizle
    processes = get_processes_by_name(task_names)
    
    if not processes:
        print("No matching processes found.")
    else:
        while True:
            print_process_info(processes)
            time.sleep(1)  # Her saniyede bir güncelleme yap
