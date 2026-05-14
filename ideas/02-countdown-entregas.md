# Idea 02 — Countdown de entregas universitarias

**Tipo:** Utilidad  
**Esfuerzo:** Bajo  
**Impacto:** Alto

## Descripción
Agregar una sección de countdowns con fechas límite de tus cursos:

- 📊 Estadística DD1 → ¿para cuándo?
- 🖥️ Sistemas Operativos TB1 → fecha de entrega
- 📱 Apps Móviles → entrega próxima semana
- 🧮 Cálculo II EU2 → fecha del examen

## Cómo implementarlo
1. Agregar un `deadlines.json` manual o parsear desde notas del vault
2. En el HTML, calcular diferencia con `Date.now()` y mostrar:
   - `"Faltan 3 días"` (verde si >7 días)
   - `"Faltan 2 días"` (amarillo si <7 días)
   - `"¡MAÑANA!"` (rojo si <24h)
3. Opcional: barra de progreso visual con porcentaje de tiempo restante

## Ejemplo visual
```
📊 Estadística — DD1
▓▓▓▓▓▓▓░░░░░ 65%
🕐 Faltan 5 días · 09 Mayo
```

## Datos semilla
```json
{
  "deadlines": [
    {"curso": "Estadística Aplicada", "tarea": "DD1", "fecha": "2026-05-15"},
    {"curso": "Sistemas Operativos", "tarea": "TB1", "fecha": "2026-05-20"},
    {"curso": "Apps Móviles", "tarea": "Entrega final", "fecha": "2026-05-18"},
    {"curso": "Cálculo II", "tarea": "EU2", "fecha": "2026-05-25"}
  ]
}
```
