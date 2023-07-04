import time
import sys


def update_progress(progress):
    bar_length = 50  # Длина прогресс-бара в символах
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    percent = progress * 100
    progress_string = f'Progress: [{bar}] {percent:.1f}%'

    sys.stdout.write('\r' + progress_string)
    sys.stdout.flush()


# Пример использования
total_iterations = 100

for i in range(total_iterations + 1):
    progress = i / total_iterations
    update_progress(progress)
    time.sleep(0.4)  # Имитация работы

print("\nЗагрузка завершена!")

lst = ["-", "\\", "|", "/"]
for _ in range(1, 100):
    for i in lst:
        time.sleep(1)
        prg = f"{i}"
        sys.stdout.write("\r" + prg)
        sys.stdout.flush()
