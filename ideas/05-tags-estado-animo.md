# Idea 05 — Tags y estado de ánimo semanal

**Tipo:** Dashboard personal  
**Esfuerzo:** Medio  
**Impacto:** Alto

## Descripción
Extraer los tags y el estado de ánimo de los checkins diarios y mostrarlos como:

- **Tag cloud** - palabras clave más repetidas (MaquinariasJyS, Cálculo, fútbol, etc.)
- **Estado de ánimo semanal** - gráfico de cómo fue cada día
- **Logro principal del día** - extraído de la sección "🐒 Nota de cierre"

## Datos a parsear
Del `lunes-checkin.md` se puede extraer:
```yaml
---
tags: [daily-checkin]
fecha: 2026-05-04
dia: lunes
estado: avance-reportado
---
```

Y de la sección de cierre:
```markdown
## 🐒 Nota de cierre
- Logro principal del día: **MaquinariasJyS** — frontend catálogo...
- Sensación honesta: **día productivo**
```

## Visualización
- Tag cloud con tamaño de fuente = frecuencia
- Timeline semanal con emojis 💪😴😐🔥
- Cards con el "Logro del día" de cada jornada
