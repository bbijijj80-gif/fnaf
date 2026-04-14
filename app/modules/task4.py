#!/usr/bin/env python3
"""Модуль 4: Генератор случайных чисел"""
import sys
import json
import random

def generate_random(min_val=0, max_val=100, count=1):
    try:
        numbers = [random.randint(min_val, max_val) for _ in range(count)]
        return {"status": "success", "numbers": numbers}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    min_val = 0
    max_val = 100
    count = 1
    if len(sys.argv) >= 3:
        try:
            min_val = int(sys.argv[1])
            max_val = int(sys.argv[2])
        except ValueError:
            pass
    if len(sys.argv) >= 4:
        try:
            count = int(sys.argv[3])
        except ValueError:
            pass
    print(json.dumps(generate_random(min_val, max_val, count)))
