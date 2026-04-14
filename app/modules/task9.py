#!/usr/bin/env python3
"""Модуль 9: Системная информация"""
import sys
import json
import platform
import os
import psutil

def get_system_info():
    try:
        return {
            "status": "success",
            "system": platform.system(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "cpu_count": os.cpu_count(),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_usage_percent": psutil.disk_usage('/').percent
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print(json.dumps(get_system_info()))
