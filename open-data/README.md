# open-data

Pack de datos abiertos de **obras literarias (Open Library)**.

- **Fuente:** <https://openlibrary.org/search.json?q=judas&limit=100&fields=key,title,author_name,first_publish_year,language>
- **Clave de API:** no requiere.
- **Generado:** ver `meta.generated_at` en `open-books.json`.

## Ficheros

| Fichero | Descripcion |
|---|---|
| `open-books.json` | Registros con metadatos + bloque `meta` |
| `open-books.csv` | El mismo pack en tabla |

## Regenerar

```bash
python scripts/fetch_open_data.py
```

Usa solo la libreria estandar.

## Licencia

Datos de Open Library (Internet Archive). Codigo del pack: MIT.
