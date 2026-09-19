#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка сайта «Пакт крови» из папки content/.

Результат:
  docs/              — полноценный статический сайт (для GitHub Pages / любого хостинга)
  docs/embed/        — те же страницы без верхнего меню (для «Встроить → По URL» в Google Sites)
  google-sites/      — автономные HTML-сниппеты по одной странице
                       (для «Вставка → Встроить → Код для встраивания» в Google Sites)

Запуск:  python3 build.py
  Локальный просмотр:  python3 build.py --base / && python3 -m http.server -d docs 8000
  На GitHub Pages (репозиторий-сайт) сборка сама берёт путь /bloodpact/ из pages_url.

Зависимостей нет — только стандартная библиотека Python 3.
"""
import argparse
import html
import json
import os
import re
import shutil
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
DOCS = os.path.join(ROOT, "docs")
EMBED = os.path.join(DOCS, "embed")
GS = os.path.join(ROOT, "google-sites")
IMG_DIR = os.path.join(DOCS, "assets", "img")
VIDEO_DIR = os.path.join(DOCS, "assets", "video")

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%F0%9F%A9%B8%3C/text%3E%3C/svg%3E"
)

ARROW_SVG = (
    '<svg role="presentation" viewBox="0 0 38.417 18.592" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M19.208,18.592c-0.241,0-0.483-0.087-0.673-0.261L0.327,1.74c-0.408-0.372-0.438-1.004'
    '-0.066-1.413c0.372-0.409,1.004-0.439,1.413-0.066L19.208,16.24L36.743,0.261c0.411-0.372,1.042'
    '-0.342,1.413,0.066c0.372,0.408,0.343,1.041-0.065,1.413L19.881,18.332C19.691,18.505,19.449,'
    '18.592,19.208,18.592z"/></svg>'
)


def load():
    with open(os.path.join(CONTENT, "pages.json"), encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(CONTENT, "theme.css"), encoding="utf-8") as f:
        css = f.read()
    return data, css


def page_href(page):
    """Имя файла для плоских версий (docs/embed/)."""
    return "index.html" if page["slug"] == "index" else page["slug"] + ".html"


def page_path(page):
    """Путь страницы на сайте — как на Tilda: / , /law/, /squads/ …"""
    return "" if page["slug"] == "index" else page["slug"] + "/"


def site_origin(site):
    """Публичный origin: https://deusofsanguis.github.io/bloodpact  (без хвостового /)."""
    domain = (site.get("domain") or "").strip().lower()
    if domain:
        return "https://" + domain
    return (site.get("pages_url") or "").rstrip("/")


def site_root(site, override=None):
    """Корень сайта на хосте: /bloodpact/ на github.io, / на своём домене.

    Абсолютные-от-хоста пути (/bloodpact/law/) не ломаются, если открыть
    страницу без хвостового слэша — в отличие от относительных ../.
    """
    if override is not None:
        path = override or "/"
        return path if path.endswith("/") else path + "/"
    domain = (site.get("domain") or "").strip()
    if domain:
        return "/"
    path = urlparse(site.get("pages_url") or "/").path or "/"
    if not path.endswith("/"):
        path += "/"
    return path


def resolve_asset(name, data, prefix="", asset_base=None):
    """Локальный файл (если скачан в docs/assets/img) → иначе исходный URL с CDN Tilda."""
    if asset_base:
        return asset_base.rstrip("/") + "/" + name
    if os.path.exists(os.path.join(IMG_DIR, name)):
        return f"{prefix}assets/img/{name}"
    return data["assets"][name]


def local_video_name(page):
    name = page["slug"] + ".mp4"
    path = os.path.join(VIDEO_DIR, name)
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        return name
    return None


def render_fragment(fragment, data, prefix="", asset_base=None):
    def repl(m):
        return resolve_asset(m.group(1), data, prefix, asset_base)
    return re.sub(r"\{\{img:([^}]+)\}\}", repl, fragment)


def render_nav(data, current_page, root="/"):
    site = data["site"]
    items = []
    for p in data["pages"]:
        if not p.get("nav"):
            continue
        cls = ' class="active" aria-current="page"' if p["slug"] == current_page["slug"] else ""
        items.append(f'<li><a href="{root}{page_path(p)}"{cls}>{html.escape(p["nav"])}</a></li>')
    return (
        '<header class="nav">'
        f'<a class="nav__logo" href="{root}">{html.escape(site["home_label"])}</a>'
        '<nav aria-label="Разделы"><ul class="nav__list">' + "".join(items) + "</ul></nav>"
        "</header>"
    )


def render_cover(page, data, prefix="", asset_base=None, with_arrow=True, with_video=True):
    bg = resolve_asset("cover.jpg", data, prefix, asset_base)
    video = ""
    if with_video:
        local = local_video_name(page)
        yt = page.get("youtube") or ""
        if local:
            src = f"{prefix}assets/video/{local}"
            video = (
                '<div class="cover__video cover__video--file" aria-hidden="true">'
                '<video autoplay muted loop playsinline preload="auto" '
                "disablepictureinpicture>"
                f'<source src="{html.escape(src, quote=True)}" type="video/mp4">'
                "</video></div>"
            )
        elif yt:
            src = (
                f"https://www.youtube.com/embed/{yt}?autoplay=1&mute=1&controls=0&loop=1"
                f"&playlist={yt}&rel=0&modestbranding=1&playsinline=1&disablekb=1"
                f"&iv_load_policy=3&fs=0"
            )
            video = (
                '<div class="cover__video cover__video--yt" aria-hidden="true">'
                f'<iframe src="{src}" title="Фоновое видео" tabindex="-1" loading="lazy" '
                'allow="autoplay; encrypted-media" referrerpolicy="strict-origin-when-cross-origin"></iframe>'
                "</div>"
            )
    arrow = f'<div class="cover__arrow" aria-hidden="true">{ARROW_SVG}</div>' if with_arrow else ""
    return (
        f'<section class="cover" style="background-image:url(\'{bg}\')">'
        f"{video}"
        '<div class="cover__filter"></div>'
        '<div class="cover__content">'
        f'<p class="cover__uptitle">{html.escape(page["cover_uptitle"])}</p>'
        f'<h1 class="cover__title">{html.escape(page["cover_title"])}</h1>'
        "</div>"
        f"{arrow}"
        "</section>"
    )


def render_document(page, data, body, css_link=None, css_inline=None, prefix="",
                    asset_base=None, body_class=""):
    site = data["site"]
    title = site["name"] if page["slug"] == "index" else f'{page["title"]} — {site["name"]}'
    og = resolve_asset("og-image.png", data, prefix, asset_base)
    parsed = urlparse(site_origin(site) or "")
    if parsed.scheme and parsed.netloc and og.startswith("/"):
        og = f"{parsed.scheme}://{parsed.netloc}{og}"
    head_css = (
        f'<link rel="stylesheet" href="{css_link}">' if css_link else f"<style>\n{css_inline}\n</style>"
    )
    body_attr = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="{site['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(site['description'])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(site['description'])}">
<meta property="og:image" content="{og}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
{head_css}
</head>
<body{body_attr}>
{body}
</body>
</html>
"""


def youtube_bg_iframe(yt):
    """Короткий код фонового автоплей-видео — удобно вставлять в Google Sites отдельным блоком."""
    src = (
        f"https://www.youtube.com/embed/{yt}?autoplay=1&mute=1&controls=0&loop=1"
        f"&playlist={yt}&rel=0&modestbranding=1&playsinline=1"
    )
    return (
        '<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden">'
        f'<iframe src="{src}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" '
        'allow="autoplay; encrypted-media" allowfullscreen></iframe></div>'
    )


def write_cheatsheet(data):
    """google-sites/ASSETS.md — шпаргалка для ручного переноса: страницы, видео, картинки."""
    lines = [
        "# Шпаргалка для переноса в Google Sites",
        "",
        "Файл генерируется автоматически (`python3 build.py`) из `content/pages.json`.",
        "",
        "## Страницы",
        "",
        "| № | Страница в Google Sites | Заголовок на обложке | Файл с текстом | Исходник на Tilda | Видео на обложке |",
        "|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(data["pages"], 1):
        yt = f"https://www.youtube.com/watch?v={p['youtube']}"
        lines.append(
            f"| {i} | {p['title']} | {p['cover_uptitle'].upper()} / {p['cover_title']} | "
            f"`google-sites/{i:02d}-{p['slug']}.html` | {p['source']} | {yt} |"
        )
    lines += [
        "",
        "## Картинки",
        "",
        "Скачать одной командой: `python3 scripts/fetch_assets.py` (лягут в `docs/assets/img/`).",
        "",
        "| Файл | Где используется | Ссылка на оригинал (CDN Tilda) |",
        "|---|---|---|",
    ]
    usage = {
        "cover.jpg": "фон обложки на всех страницах (поверх — затемнение 70 %)",
        "og-image.png": "картинка для превью ссылки (og:image)",
        "territory-1.png": "Территории — после «Зал высших лун»",
        "territory-2.png": "Территории — после «Зал Доумы»",
        "territory-3.png": "Территории — после «Зал низших лун»",
        "territory-4.png": "Территории — после «Отрядные помещения» (1)",
        "territory-5.png": "Территории — после «Отрядные помещения» (2)",
        "champion.webp": "Рейтинг — круглое фото чемпиона (300×300)",
    }
    for name, url in data["assets"].items():
        lines.append(f"| `{name}` | {usage.get(name, '')} | {url} |")
    lines += [
        "",
        "## Код фонового видео (для блока «Встроить → Код для встраивания»)",
        "",
        "В Google Sites нельзя поставить видео фоном баннера, поэтому видео вставляется отдельным блоком",
        "сразу под баннером. Код ниже запускает ролик автоматически, без звука и по кругу.",
        "",
    ]
    for p in data["pages"]:
        lines += [f"### {p['title']}", "", "```html", youtube_bg_iframe(p["youtube"]), "```", ""]
    with open(os.path.join(GS, "ASSETS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def build(asset_base=None, base_override=None):
    data, css = load()

    # чистим и создаём выходные папки
    # (docs/assets — картинки/видео не трогаем)
    keep_in_docs = {"assets"}
    for d in (DOCS, GS):
        if os.path.isdir(d):
            for name in os.listdir(d):
                p = os.path.join(d, name)
                if d == DOCS and name in keep_in_docs:
                    continue
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(EMBED, exist_ok=True)
    os.makedirs(GS, exist_ok=True)

    with open(os.path.join(DOCS, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(css)
    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    site = data["site"]
    root = site_root(site, override=base_override)
    origin = site_origin(site)

    # свой домен не пишем, пока поле domain пустое (CNAME ломает github.io)
    domain = (site.get("domain") or "").strip().lower()
    if domain:
        with open(os.path.join(DOCS, "CNAME"), "w", encoding="utf-8") as f:
            f.write(domain + "\n")

    footer = f'<footer class="footer">{html.escape(site["name"])} · {html.escape(site["short"])}</footer>'

    if asset_base:
        snippet_base = asset_base
    elif origin:
        snippet_base = origin + "/assets/img"
    else:
        snippet_base = None

    for i, page in enumerate(data["pages"]):
        with open(os.path.join(CONTENT, page["slug"] + ".html"), encoding="utf-8") as f:
            fragment = f.read().strip()

        # 1) полноценная страница сайта: пути от корня хоста (/bloodpact/…)
        body = (
            render_nav(data, page, root=root)
            + render_cover(page, data, prefix=root)
            + '<main id="content">\n' + render_fragment(fragment, data, prefix=root) + "\n</main>\n"
            + footer
        )
        out = render_document(page, data, body, css_link=f"{root}assets/style.css", prefix=root)
        out_dir = os.path.join(DOCS, page_path(page))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(out)

        # 2) embed-версия без меню — те же абсолютные-от-хоста пути
        body = (
            render_cover(page, data, prefix=root, with_arrow=False)
            + '<main id="content">\n' + render_fragment(fragment, data, prefix=root) + "\n</main>\n"
        )
        out = render_document(page, data, body, css_link=f"{root}assets/style.css",
                              prefix=root, body_class="embed")
        with open(os.path.join(EMBED, page_href(page)), "w", encoding="utf-8") as f:
            f.write(out)

        # 3) автономный сниппет: картинки по абсолютным https://…/assets/img/
        body = (
            render_cover(page, data, asset_base=snippet_base, with_arrow=False)
            + '<main id="content">\n' + render_fragment(fragment, data, asset_base=snippet_base) + "\n</main>\n"
        )
        out = render_document(page, data, body, css_inline=css, asset_base=snippet_base, body_class="embed")
        name = f"{i + 1:02d}-{page['slug']}.html"
        with open(os.path.join(GS, name), "w", encoding="utf-8") as f:
            f.write(out)

    write_404(data, css, root=root)
    write_cheatsheet(data)

    print("Собрано страниц:", len(data["pages"]))
    print("Корень сайта (href/src):", root)
    for p in data["pages"]:
        print(f"  /{page_path(p):14s}  docs/{page_path(p)}index.html  ←  {p['source']}")
    local_n = sum(1 for p in data["pages"] if local_video_name(p))
    print(f"Обложки со своим видео: {local_n} из {len(data['pages'])}")
    if domain:
        print("Свой домен (docs/CNAME):", domain)
    else:
        print("Свой домен не задан — сайт на GitHub Pages:", origin or "(pages_url пуст)")


def write_404(data, css, root="/"):
    """docs/404.html — GitHub Pages показывает её для несуществующих адресов."""
    body = (
        '<section class="cover" style="--cover-h:100vh">'
        '<div class="cover__filter"></div>'
        '<div class="cover__content">'
        '<p class="cover__uptitle">404</p>'
        '<h1 class="cover__title">Такой страницы нет</h1>'
        f'<p style="margin-top:30px"><a href="{root}" style="font-size:18px">← На главную</a></p>'
        "</div></section>"
    )
    page = {"slug": "404", "title": "Страница не найдена", "cover_uptitle": "404",
            "cover_title": "Такой страницы нет", "youtube": ""}
    out = render_document(page, data, body, css_inline=css)
    with open(os.path.join(DOCS, "404.html"), "w", encoding="utf-8") as f:
        f.write(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--asset-base", default=None,
                    help="абсолютный URL папки с картинками для сниппетов google-sites/ "
                         "(например https://deusofsanguis.github.io/bloodpact/assets/img).")
    ap.add_argument("--base", default=None,
                    help="префикс путей на сайте. По умолчанию берётся из pages_url "
                         "(/bloodpact/ на github.io). Для локального просмотра: --base /")
    args = ap.parse_args()
    build(asset_base=args.asset_base, base_override=args.base)
