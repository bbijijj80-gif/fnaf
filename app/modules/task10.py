#!/usr/bin/env python3
"""Модуль 10: QR-код генератор (симуляция текстом)"""
import sys
import json
import hashlib

def generate_qr_data(data):
    hash_id = hashlib.md5(data.encode()).hexdigest()[:8]
    return {
        "status": "success",
        "data": data,
        "qr_hash": hash_id,
        "message": f"QR-код сформирован для: {data}"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = " ".join(sys.argv[1:])
        print(json.dumps(generate_qr_data(data), ensure_ascii=False))
    else:
        print(json.dumps({"status": "info", "message": "Передайте данные для QR-кода"}))
