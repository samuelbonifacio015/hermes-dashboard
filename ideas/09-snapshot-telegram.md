# Idea 09 — Snapshot automático a Telegram

**Tipo:** Integración  
**Esfuerzo:** Medio  
**Impacto:** Muy alto

## Descripción
Que el dashboard se envíe automáticamente a Telegram como imagen cada mañana.

## Cómo funciona
1. Hermes ejecuta `./update.sh` para datos frescos
2. Toma screenshot con Playwright o browser tool
3. Envía la imagen al chat de Telegram

## Comando sugerido para screenshot sin Playwright
```bash
# Usando Chromium headless si está instalado
chromium-browser --headless --screenshot=/tmp/dashboard.png \
  --window-size=1280,2000 file:///home/samuel/codigo/sem6-dashboard/dashboard.html
```

## Cron job sugerido
```yaml
# Todos los días a las 8:00 AM
schedule: "0 8 * * *"
prompt: >
  Ejecuta ./update.sh en ~/codigo/sem6-dashboard/,
  abre el dashboard en el navegador, toma screenshot,
  y envíalo al chat de Telegram de Samuel.
deliver: "telegram"
```

Esto haría que Samuel reciba su dashboard cada mañana sin hacer nada  🤖✨
