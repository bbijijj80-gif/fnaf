#!/usr/bin/env python3
"""Модуль 3: Конвертер валют (условный)"""
import sys
import json

RATES = {
    "USD": 1.0,
    "EUR": 0.85,
    "GBP": 0.73,
    "RUB": 75.0,
    "JPY": 110.0
}

def convert(amount, from_currency, to_currency):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency not in RATES or to_currency not in RATES:
        return {"status": "error", "message": "Неизвестная валюта"}
    amount_usd = amount / RATES[from_currency]
    result = amount_usd * RATES[to_currency]
    return {"status": "success", "result": round(result, 2), "from": from_currency, "to": to_currency}

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        try:
            amount = float(sys.argv[1])
            print(json.dumps(convert(amount, sys.argv[2], sys.argv[3])))
        except ValueError:
            print(json.dumps({"status": "error", "message": "Неверное число"}))
    else:
        print(json.dumps({"status": "info", "currencies": list(RATES.keys())}))
