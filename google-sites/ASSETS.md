# Шпаргалка для переноса в Google Sites

Файл генерируется автоматически (`python3 build.py`) из `content/pages.json`.

## Страницы

| № | Страница в Google Sites | Заголовок на обложке | Файл с текстом | Исходник на Tilda | Видео на обложке |
|---|---|---|---|---|---|
| 1 | Главная страница | YUFU / Фракция демонов | `google-sites/01-index.html` | https://bloodpact-yufu.tilda.ws/ | https://www.youtube.com/watch?v=2P6JSigJ7xo |
| 2 | Демонический закон | YUFU / Демонический закон | `google-sites/02-law.html` | https://bloodpact-yufu.tilda.ws/law | https://www.youtube.com/watch?v=RMnzGUtdsls |
| 3 | Возвышение крови | YUFU / Возвышение крови | `google-sites/03-elevation.html` | https://bloodpact-yufu.tilda.ws/elevation | https://www.youtube.com/watch?v=Hb7SHEtpigc |
| 4 | Отряды | YUFU / Отряды | `google-sites/04-squads.html` | https://bloodpact-yufu.tilda.ws/squads | https://www.youtube.com/watch?v=Xdbl3z_21P4 |
| 5 | Шрамы | YUFU / Шрамы безотрядных | `google-sites/05-scars.html` | https://bloodpact-yufu.tilda.ws/scars | https://www.youtube.com/watch?v=bMxFePqtYoo |
| 6 | Пределы крови | YUFU / Пределы | `google-sites/06-limits.html` | https://bloodpact-yufu.tilda.ws/limits | https://www.youtube.com/watch?v=XVDBTsir2O4 |
| 7 | Битва крови | YUFU / Битвы крови | `google-sites/07-bloodbattle.html` | https://bloodpact-yufu.tilda.ws/bloodbattle | https://www.youtube.com/watch?v=XJsTQCXAJnY |
| 8 | Территории | YUFU / Территории | `google-sites/08-territories.html` | https://bloodpact-yufu.tilda.ws/territories | https://www.youtube.com/watch?v=ZmU692cglz8 |
| 9 | Поощрения | YUFU / Поощрения | `google-sites/09-incentives.html` | https://bloodpact-yufu.tilda.ws/incentives | https://www.youtube.com/watch?v=W_47yPcLm2U |
| 10 | Рейтинг | YUFU / Рейтинг | `google-sites/10-ranking.html` | https://bloodpact-yufu.tilda.ws/ranking | https://www.youtube.com/watch?v=GADE8Tkaa2Q |
| 11 | Суд | YUFU / Суд | `google-sites/11-court.html` | https://bloodpact-yufu.tilda.ws/court | https://www.youtube.com/watch?v=Sg0vFNo_Qig |

## Картинки

Скачать одной командой: `python3 scripts/fetch_assets.py` (лягут в `docs/assets/img/`).

| Файл | Где используется | Ссылка на оригинал (CDN Tilda) |
|---|---|---|
| `cover.jpg` | фон обложки на всех страницах (поверх — затемнение 70 %) | https://static.tildacdn.pub/tild3736-3037-4334-b863-353562353039/d946dbce69a24e0288d5.jpg |
| `og-image.png` | картинка для превью ссылки (og:image) | https://static.tildacdn.pub/tild6233-3966-4466-b663-643734636462/image.png |
| `territory-1.png` | Территории — после «Зал высших лун» | https://static.tildacdn.pub/tild6631-3432-4730-a366-346236323566/image.png |
| `territory-2.png` | Территории — после «Зал Доумы» | https://static.tildacdn.pub/tild3461-6166-4264-b434-633430366439/image.png |
| `territory-3.png` | Территории — после «Зал низших лун» | https://static.tildacdn.pub/tild6131-6164-4731-a135-663630663437/image.png |
| `territory-4.png` | Территории — после «Отрядные помещения» (1) | https://static.tildacdn.pub/tild3633-6536-4366-a333-396232373936/image.png |
| `territory-5.png` | Территории — после «Отрядные помещения» (2) | https://static.tildacdn.pub/tild3133-6530-4439-b132-306461663261/image.png |
| `champion.webp` | Рейтинг — круглое фото чемпиона (300×300) | https://static.tildacdn.pub/tild3938-6139-4036-a531-623036666330/i.webp |

## Код фонового видео (для блока «Встроить → Код для встраивания»)

В Google Sites нельзя поставить видео фоном баннера, поэтому видео вставляется отдельным блоком
сразу под баннером. Код ниже запускает ролик автоматически, без звука и по кругу.

### Главная страница

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/2P6JSigJ7xo?autoplay=1&mute=1&controls=0&loop=1&playlist=2P6JSigJ7xo&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Демонический закон

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/RMnzGUtdsls?autoplay=1&mute=1&controls=0&loop=1&playlist=RMnzGUtdsls&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Возвышение крови

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/Hb7SHEtpigc?autoplay=1&mute=1&controls=0&loop=1&playlist=Hb7SHEtpigc&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Отряды

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/Xdbl3z_21P4?autoplay=1&mute=1&controls=0&loop=1&playlist=Xdbl3z_21P4&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Шрамы

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/bMxFePqtYoo?autoplay=1&mute=1&controls=0&loop=1&playlist=bMxFePqtYoo&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Пределы крови

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/XVDBTsir2O4?autoplay=1&mute=1&controls=0&loop=1&playlist=XVDBTsir2O4&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Битва крови

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/XJsTQCXAJnY?autoplay=1&mute=1&controls=0&loop=1&playlist=XJsTQCXAJnY&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Территории

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/ZmU692cglz8?autoplay=1&mute=1&controls=0&loop=1&playlist=ZmU692cglz8&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Поощрения

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/W_47yPcLm2U?autoplay=1&mute=1&controls=0&loop=1&playlist=W_47yPcLm2U&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Рейтинг

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/GADE8Tkaa2Q?autoplay=1&mute=1&controls=0&loop=1&playlist=GADE8Tkaa2Q&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```

### Суд

```html
<div style="position:relative;padding-top:56.25%;background:#000;overflow:hidden"><iframe src="https://www.youtube.com/embed/Sg0vFNo_Qig?autoplay=1&mute=1&controls=0&loop=1&playlist=Sg0vFNo_Qig&rel=0&modestbranding=1&playsinline=1" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>
```
