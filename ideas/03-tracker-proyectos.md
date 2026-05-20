# Idea 03 — Tracker de proyectos con milestones

**Tipo:** Gestión de proyectos  
**Esfuerzo:** Medio  
**Impacto:** Muy alto

## Descripción
Convertir la sección de proyectos en un tracker visual con:

- **Milestones** - hitos cumplidos vs pendientes
- **Última actividad** - cuándo se tocó el proyecto por última vez
- **Progreso** - barra de avance estimada
- **Branch activa** - si el repo tiene cambios sin commitear

## Proyectos a trackear
| Proyecto | Último cambio | Próximo hito |
|---|---|---|
| 🚧 MaquinariasJyS | Hoy | Deploy backend + DB |
| 🎯 QRust / Klippr | Semana 6 | TB1 |
| 🌱 LlamIA | Abril | Definición inicial |
| 📖 Manga Lore | — | Empezar HTML/CSS |

## Cómo implementarlo
1. El `collect_data.py` ya cuenta notas por proyecto
2. Agregar detección de `mtime` más reciente por carpeta de proyecto
3. En el HTML, renderizar como cards con barra de progreso

```html
<div class="project-card">
  <div class="project-header">
    <span class="project-name">MaquinariasJyS</span>
    <span class="project-badge">#1</span>
  </div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 65%"></div>
  </div>
  <div class="project-meta">
    <span>🕐 Último: hoy</span>
    <span>🎯 Deploy backend</span>
  </div>
</div>
```
