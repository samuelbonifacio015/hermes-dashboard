# Idea 08 — Diseño responsive + tema claro/oscuro

**Tipo:** UI/UX  
**Esfuerzo:** Bajo  
**Impacto:** Medio

## Descripción
Mejorar la experiencia visual:

### ☀️ Modo claro
Agregar un toggle claro/oscuro. El diseño actual es negro, pero un modo claro con fondo blanco y texto oscuro puede ser útil de día.

### 📱 Responsive mejorado
El dashboard ya tiene media queries, pero se puede pulir:
- Tocar el día de hoy en mobile para expandir tareas
- Swipe entre secciones
- Modo "compacto" para ver en pantalla chica

### 🎨 Paletas de color
Opcional: selector de temas:
- **Neón** (actual) — azul/púrpura sobre negro
- **Matrix** — verde sobre negro
- **Warm** — naranja/ámbar sobre crema
- **Minimal** — grises sin color de acento

## Código ejemplo para toggle
```javascript
function toggleTheme() {
  document.body.classList.toggle('light-mode');
  localStorage.setItem('theme', 
    document.body.classList.contains('light-mode') ? 'light' : 'dark'
  );
}

// Al cargar
if (localStorage.getItem('theme') === 'light') {
  document.body.classList.add('light-mode');
}
```
