# Idea 04 — Modo "Semana 7" automático

**Tipo:** Automatización  
**Esfuerzo:** Bajo  
**Impacto:** Medio

## Descripción
Que el dashboard detecte automáticamente la semana actual y genere la vista correspondiente sin tener que editar el script cada semana.

## Cómo implementarlo
```python
from datetime import date

def detectar_semana_actual():
    today = date.today()
    # Semana 6: 4-9 Mayo, Semana 7: 11-16 Mayo
    # Usar ISO week number o fechas fijas
    if today >= date(2026, 5, 11) and today <= date(2026, 5, 16):
        return "Semana 7", VAULT / "2026/Mayo/Semana 7"
    elif today >= date(2026, 5, 4) and today <= date(2026, 5, 9):
        return "Semana 6", VAULT / "2026/Mayo/Semana 6"
    # ... etc
```

## Mejora adicional
- Side-by-side: mostrar semana actual y anterior para comparar
- Auto-detectar si la carpeta de la semana existe, si no, sugerir crearla
- Botón "Crear Semana X" desde el mismo dashboard
