#!/usr/bin/env python3
"""Модуль 7: Таймер и секундомер (симуляция)"""
import sys
import json
import time

def run_timer(seconds):
    start = time.time()
    time.sleep(min(seconds, 5))  # Симуляция, максимум 5 сек
    elapsed = time.time() - start
    return {"status": "success", "requested": seconds, "elapsed": round(elapsed, 2)}

def run_stopwatch():
    start = time.time()
    time.sleep(1)
    elapsed = time.time() - start
    return {"status": "success", "time": round(elapsed, 3)}

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "stopwatch":
        print(json.dumps(run_stopwatch()))
    elif len(sys.argv) >= 2:
        try:
            seconds = int(sys.argv[1])
            print(json.dumps(run_timer(seconds)))
        except ValueError:
            print(json.dumps({"status": "error", "message": "Укажите число секунд"}))
    else:
        print(json.dumps({"status": "info", "message": "Используйте: timer <секунды> или stopwatch"}))
