#!/usr/bin/env python3
"""Главное приложение с интерфейсом для управления 10 модулями"""
import subprocess
import json
import sys
import os

MODULES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules")

MODULES = {
    "1": {"name": "Калькулятор", "file": "task1.py", "desc": "Выполняет математические вычисления"},
    "2": {"name": "Генератор паролей", "file": "task2.py", "desc": "Создаёт случайные пароли"},
    "3": {"name": "Конвертер валют", "file": "task3.py", "desc": "Конвертирует между валютами"},
    "4": {"name": "Генератор случайных чисел", "file": "task4.py", "desc": "Генерирует случайные числа"},
    "5": {"name": "Погода", "file": "task5.py", "desc": "Показывает погоду (симуляция)"},
    "6": {"name": "Анализ текста", "file": "task6.py", "desc": "Анализирует текст"},
    "7": {"name": "Таймер", "file": "task7.py", "desc": "Таймер и секундомер"},
    "8": {"name": "Заметки", "file": "task8.py", "desc": "Управление заметками"},
    "9": {"name": "Системная информация", "file": "task9.py", "desc": "Информация о системе"},
    "10": {"name": "QR-генератор", "file": "task10.py", "desc": "Генерация QR-кодов"}
}

def run_module(module_key, args=None):
    module = MODULES.get(module_key)
    if not module:
        return {"status": "error", "message": "Модуль не найден"}
    
    cmd = [sys.executable, os.path.join(MODULES_DIR, module["file"])]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.stdout:
            return json.loads(result.stdout)
        elif result.stderr:
            return {"status": "error", "message": result.stderr}
        return {"status": "error", "message": "Нет ответа от модуля"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Тайм-аут выполнения"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def show_menu():
    print("\n" + "="*50)
    print("   ГЛАВНОЕ МЕНЮ - УПРАВЛЕНИЕ МОДУЛЯМИ")
    print("="*50)
    for key, mod in MODULES.items():
        print(f"{key}. {mod['name']} - {mod['desc']}")
    print("0. Выход")
    print("="*50)

def main():
    while True:
        show_menu()
        choice = input("\nВыберите модуль (0-10): ").strip()
        
        if choice == "0":
            print("Выход из программы. До свидания!")
            break
        
        if choice not in MODULES:
            print("Неверный выбор. Попробуйте снова.")
            continue
        
        print(f"\n>>> Запуск модуля: {MODULES[choice]['name']}")
        
        args = []
        if choice == "1":
            expr = input("Введите выражение (например, 2+2*2): ").strip()
            if expr:
                args = expr.split()
        elif choice == "2":
            length = input("Длина пароля (12): ").strip() or "12"
            args = [length]
        elif choice == "3":
            amount = input("Сумма: ").strip() or "100"
            from_cur = input("Из валюты (USD): ").strip() or "USD"
            to_cur = input("В валюту (EUR): ").strip() or "EUR"
            args = [amount, from_cur, to_cur]
        elif choice == "4":
            min_v = input("Мин (0): ").strip() or "0"
            max_v = input("Макс (100): ").strip() or "100"
            count = input("Количество (1): ").strip() or "1"
            args = [min_v, max_v, count]
        elif choice == "5":
            city = input("Город (Москва): ").strip() or "Москва"
            args = [city]
        elif choice == "6":
            text = input("Текст для анализа: ").strip()
            if text:
                args = text.split()
        elif choice == "7":
            mode = input("Режим (timer/stopwatch): ").strip() or "stopwatch"
            if mode == "timer":
                sec = input("Секунды (5): ").strip() or "5"
                args = [sec]
            else:
                args = ["stopwatch"]
        elif choice == "8":
            action = input("Действие (add/list): ").strip() or "list"
            if action == "add":
                text = input("Текст заметки: ").strip()
                args = [text]
            else:
                args = ["list"]
        elif choice == "10":
            data = input("Данные для QR: ").strip() or "Hello"
            args = [data]
        
        result = run_module(choice, args if args else None)
        
        print("\n--- Результат ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("-----------------\n")
        
        input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана.")
