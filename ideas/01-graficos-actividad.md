# Idea 01 — Gráficos de actividad semanal

**Tipo:** Visualización  
**Esfuerzo:** Medio  
**Impacto:** Alto

## Descripción
Agregar gráficos de barras o líneas (usando Canvas o Chart.js) que muestren:

- Notas creadas por día en la última semana
- Checkins completados vs pendientes por semana
- Tendencia de productividad semanal

## Cómo implementarlo
1. El `collect_data.py` debería trackear fechas de creación/modificación de notas por día
2. Usar `<canvas>` nativo o una librería liviana como Chart.js desde CDN
3. Mostrar como gráfico de área con gradiente (estilo neón)

## Código sugerido
```python
# En collect_data.py
from collections import Counter
from datetime import datetime, timedelta

# Contar notas modificadas por día (últimos 7 días)
today = datetime.now()
last_week = today - timedelta(days=7)
notes_by_day = Counter()

for md_file in VAULT.rglob("*.md"):
    mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
    if mtime > last_week:
        day_key = mtime.strftime("%Y-%m-%d")
        notes_by_day[day_key] += 1
```
