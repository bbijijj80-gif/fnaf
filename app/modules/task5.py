#!/usr/bin/env python3
"""Модуль 5: Проверка погоды (симуляция)"""
import sys
import json
import random

WEATHER_CONDITIONS = ["Солнечно", "Облачно", "Дождь", "Снег", "Туман"]

def get_weather(city="Москва"):
    temp = random.randint(-20, 35)
    condition = random.choice(WEATHER_CONDITIONS)
    humidity = random.randint(30, 90)
    return {
        "status": "success",
        "city": city,
        "temperature": temp,
        "condition": condition,
        "humidity": humidity
    }

if __name__ == "__main__":
    city = "Москва"
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    print(json.dumps(get_weather(city)))
