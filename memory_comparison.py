
import sys
import os
import psutil
import gc
from dataclasses import dataclass

# Добавляем пути к обеим версиям
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, "telegram_bot"))
sys.path.insert(0, os.path.join(current_dir, "telegram_bot_v2"))

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MiB

# ===== НЕЭФФЕКТИВНАЯ ВЕРСИЯ: словари + мусор =====
def simulate_inefficient_users(n=1000):
    users = {}
    for i in range(n):
        users[f"user_{i}"] = {
            "subscribed": True,
            "state": "main_menu",
            "task1_text": "hello world",
            "task1_result": ["hello", "world"],  # имитация результата
            "temp_data": list(range(100))  # искусственный мусор
        }
    return users

# ===== ЭФФЕКТИВНАЯ ВЕРСИЯ: dataclass без мусора =====
@dataclass
class UserData:
    subscribed: bool
    state: str
    task1_result: list

def simulate_efficient_users(n=1000):
    users = []
    result = ["hello", "world"]
    for _ in range(n):
        users.append(UserData(True, "main_menu", result))
    return users

if __name__ == "__main__":
    gc.collect()
    base = get_memory_usage()
    print(f"Базовое использование: {base:.1f} MiB")

    # Неэффективная версия
    gc.collect()
    data1 = simulate_inefficient_users(1000)
    mem1 = get_memory_usage()
    print(f"Неэффективная версия: {mem1:.1f} MiB (+{mem1 - base:.1f})")

    del data1
    gc.collect()

    # Эффективная версия
    gc.collect()
    data2 = simulate_efficient_users(1000)
    mem2 = get_memory_usage()
    print(f"Эффективная версия: {mem2:.1f} MiB (+{mem2 - base:.1f})")

    print(f"\nЭкономия: {mem1 - mem2:.1f} MiB ({(mem1 - mem2) / mem1 * 100:.1f}%)")