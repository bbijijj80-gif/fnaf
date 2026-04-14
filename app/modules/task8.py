#!/usr/bin/env python3
"""Модуль 8: Управление заметками (файл)"""
import sys
import json
import os

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

def add_note(text):
    notes = load_notes()
    notes.append({"id": len(notes) + 1, "text": text})
    save_notes(notes)
    return {"status": "success", "message": "Заметка добавлена", "id": len(notes)}

def list_notes():
    notes = load_notes()
    return {"status": "success", "notes": notes}

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        print(json.dumps(list_notes(), ensure_ascii=False))
    elif len(sys.argv) >= 2:
        text = " ".join(sys.argv[1:])
        print(json.dumps(add_note(text), ensure_ascii=False))
    else:
        print(json.dumps({"status": "info", "message": "Используйте: add <текст> или list"}))
