#!/usr/bin/env python3
"""Модуль 6: Анализ текста"""
import sys
import json

def analyze_text(text):
    words = text.split()
    chars = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    return {
        "status": "success",
        "words": len(words),
        "characters": chars,
        "sentences": max(1, sentences),
        "avg_word_length": round(sum(len(w) for w in words) / max(1, len(words)), 2)
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(json.dumps(analyze_text(text)))
    else:
        print(json.dumps({"status": "info", "message": "Передайте текст для анализа"}))
