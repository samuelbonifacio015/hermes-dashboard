# Idea 07 — Dashboard como skill de Hermes

**Tipo:** Automatización  
**Esfuerzo:** Bajo  
**Impacto:** Muy alto

## Descripción
Crear una skill de Hermes llamada `sem6-dashboard` que permita:

- `hermes sem6-dashboard update` → ejecuta el update.sh
- `hermes sem6-dashboard show` → abre el dashboard en el navegador
- Que Samuel pueda pedirme "actualiza el dashboard" y yo lo haga automáticamente
- Opcional: enviar snapshot del dashboard a Telegram automáticamente cada mañana

## Cómo implementarlo
1. Crear skill que contenga las rutas y comandos
2. Agregar al `~/.hermes/skills/` como `sem6-dashboard/SKILL.md`
3. Incluir instrucciones para que Hermes ejecute el update antes de mostrar datos

## Comandos sugeridos
```bash
# Actualizar datos
cd ~/codigo/sem6-dashboard && python3 collect_data.py

# Abrir dashboard
xdg-open ~/codigo/sem6-dashboard/dashboard.html
```

## Extra: Cron diario
Configurar un cron job que ejecute `./update.sh` cada mañana a las 8am para que el dashboard siempre esté fresco sin que Samuel tenga que acordarse.
