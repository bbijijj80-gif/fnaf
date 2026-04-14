#!/usr/bin/env python3
"""Модуль 1: Калькулятор"""
import sys
import json

def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        print(json.dumps(calculate(expression)))
    else:
        print(json.dumps({"status": "info", "message": "Калькулятор готов к вычислениям"}))
