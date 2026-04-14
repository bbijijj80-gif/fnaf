#!/usr/bin/env python3
"""Модуль 2: Генератор паролей"""
import sys
import json
import random
import string

def generate_password(length=12, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    return {"status": "success", "password": password}

if __name__ == "__main__":
    length = 12
    use_special = True
    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
        except ValueError:
            pass
    if len(sys.argv) > 2 and sys.argv[2].lower() == "false":
        use_special = False
    print(json.dumps(generate_password(length, use_special)))
