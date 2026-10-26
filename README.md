# 📊 Calculadora de estadística (Django + Vercel)

Pegás números y devuelve promedio, mediana, moda, mínimo, máximo, rango, varianza y desvío
(muestral y poblacional). Sin base de datos: no guarda nada. Incluye una API JSON.

## Local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
DEBUG=1 python manage.py runserver
python manage.py test
```

## API

```bash
curl -X POST https://TU-APP.vercel.app/api/calcular/ \
  -H "Content-Type: application/json" \
  -d '{"numeros": [8, 7.5, 9, 6, 10, 8]}'
```

## Deploy en Vercel

Vercel detecta Django solo (busca `manage.py` y lee `WSGI_APPLICATION` de `settings.py`).
No hace falta `vercel.json`.

**Opción A: desde GitHub (recomendada)**
1. Subí esta carpeta a un repo.
2. En vercel.com → *Add New → Project* → importá el repo → *Deploy*.
3. En *Settings → Environment Variables* agregá `SECRET_KEY` con un valor largo y aleatorio:
   `python -c "import secrets; print(secrets.token_urlsafe(50))"`
4. Redeploy para que tome la variable.

```

**Variables de entorno**
| Variable | Para qué |
|---|---|
| `SECRET_KEY` | Obligatoria en producción |
| `DOMINIO` | Opcional, si usás dominio propio (ej. `calc.midominio.com`) |
| `DEBUG` | Dejala sin definir en producción |

## Estructura

```
config/            settings, urls, wsgi
estadistica/
  stats.py         lógica pura (parseo + cálculos con el módulo statistics)
  views.py         página + endpoint API
  templates/       index.html (CSS inline, no hay archivos estáticos)
  tests.py
requirements.txt   solo Django
.python-version    3.12
```
