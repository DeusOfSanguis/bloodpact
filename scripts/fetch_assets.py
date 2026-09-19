#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скачивает все картинки сайта с CDN Tilda в docs/assets/img/,
чтобы сайт не зависел от Tilda (после удаления проекта на Tilda картинки пропадут).

Запуск из корня репозитория:
    python3 scripts/fetch_assets.py
затем пересоберите сайт:
    python3 build.py
"""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "docs", "assets", "img")

with open(os.path.join(ROOT, "content", "pages.json"), encoding="utf-8") as f:
    assets = json.load(f)["assets"]

os.makedirs(IMG_DIR, exist_ok=True)
failed = 0
for name, url in assets.items():
    dest = os.path.join(IMG_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"уже есть  {name}")
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as out:
            out.write(r.read())
        print(f"скачано   {name}  ({os.path.getsize(dest) // 1024} КБ)")
    except Exception as e:  # noqa: BLE001
        failed += 1
        print(f"ОШИБКА    {name}: {e}", file=sys.stderr)
        if os.path.exists(dest):
            os.remove(dest)

print()
if failed:
    print(f"Не удалось скачать файлов: {failed}. Скачайте их вручную по ссылкам из content/pages.json "
          f"и положите в docs/assets/img/ под теми же именами.")
    sys.exit(1)
print("Готово. Теперь выполните: python3 build.py")
