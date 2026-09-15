# Belentani The Judas Experience

Python SaaS GUI for the Belentani ecosystem: immersive glassmorphism, red dream light, Judas Era narrative, and a Studio CMS stub that can grow into a full tenant platform.

Visual language follows [belentani.es](https://belentani.es): absolute black, neon red, blood, frosted crystal, 432 Hz HUD, JUDAS_OS.

## Run (Windows PowerShell)

```powershell
cd C:\Users\USER\belentani-the-judas-experience
.\run.ps1
```

Then open http://127.0.0.1:4320

- Portal `/`
- Judas experience `/judas`
- Studio `/studio`
- Login `/auth/login` — demo `studio@belentani.es` / `omega`

## Stack

FastAPI + Jinja2 + HTMX + CSS/JS. JSON store in `data/omega.json` (tenancy stub). Replace with Postgres when the product scales.

## Routes

| Path | Role |
| --- | --- |
| `/` | Cinematic portal |
| `/judas` | Five-phase experience + archetype gems |
| `/studio` | Artist CMS |
| `/api/health` `/api/hud` `/api/gems` | JSON for future growth |

## Datos abiertos

El directorio [`open-data/`](open-data/) trae un pack abierto de datos de **obras literarias (Open Library)** (fuente publica, sin clave de API).

```bash
python scripts/fetch_open_data.py   # regenera el pack
```

Ver [`open-data/README.md`](open-data/README.md) para fuente y licencia.

## Proyectos open similares

- [Ren'Py](https://github.com/renpy/renpy)
- [Twine](https://github.com/klembot/twinejs)
- [Ink](https://github.com/inkle/ink)
- [ChoiceScript](https://github.com/dfabulich/choicescript)
- [Open Library](https://openlibrary.org)
