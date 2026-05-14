#!/usr/bin/env python3
"""Loop que genera ideas frescas para el dashboard cada cierto tiempo."""
import json
import os
import random
from datetime import datetime
from pathlib import Path

IDEAS_DIR = Path("/home/samuel/codigo/sem6-dashboard/ideas")
VAULT = Path("/home/samuel/obsidian-notes/obsidian")

# Banco de ideas para combinar
TOPICOS = [
    "productividad", "visualización", "automatización", "gamificación",
    "integración", "UI/UX", "datos", "IA", "mobile", "colaboración"
]

ANGULOS = [
    "Agregar un widget de", "Crear un dashboard anidado para",
    "Implementar seguimiento de", "Visualizar métricas de",
    "Automatizar la generación de", "Integrar datos de",
    "Añadir un timeline de", "Convertir en gráfico interactivo"
]

OBJETOS = [
    "checkins diarios", "tareas completadas", "horas de estudio",
    "proyectos activos", "entregas universitarias", "notas del vault",
    "commits de Git", "estado de ánimo semanal", "tiempo por curso",
    "enlaces rotos del vault", "crecimiento del vault", "racha de productividad"
]

FRAGMENTOS = [
    "con barras de progreso animadas",
    "con un calendario tipo GitHub",
    "con tarjetas expandibles",
    "con un radar chart",
    "usando emojis como indicadores",
    "con datos históricos comparativos",
    "con filtros por semana/mes",
    "con exportación a PDF"
]

def generar_idea():
    topico = random.choice(TOPICOS)
    angulo = random.choice(ANGULOS)
    objeto = random.choice(OBJETOS)
    fragmento = random.choice(FRAGMENTOS)
    
    titulo = f"{angulo} {objeto} {fragmento}"
    
    cuerpo = f"""# {titulo}

**Tipo:** {topico.capitalize()}  
**Generada:** {datetime.now().strftime('%d-%m-%Y %H:%M')}

## Descripción
{angulo} **{objeto}** {fragmento}. Esto ayudaría a tener una vista más completa del progreso y la actividad diaria.

## Posible implementación
1. Identificar la fuente de datos en el vault
2. Agregar función en `collect_data.py` para extraer la información
3. Renderizar en el HTML como una nueva card o sección

## Valor para Samuel
- 📊 Mejor visibilidad de {objeto}
- ⏱️ Sin esfuerzo manual adicional
- 🎯 Decisiones más informadas sobre dónde enfocarse
"""
    return titulo, cuerpo

def guardar_idea(titulo, cuerpo):
    # Sanitizar título para filename
    filename = titulo.lower()
    filename = filename.replace(" ", "-")
    filename = "".join(c for c in filename if c.isalnum() or c in "-_")
    filename = filename[:60] + ".md"
    
    filepath = IDEAS_DIR / filename
    if not filepath.exists():
        filepath.write_text(cuerpo)
        return f"✅ {filepath.name}"
    return None

def main():
    print(f"🧠 Generador de ideas — {datetime.now().isoformat()}")
    print(f"📂 Directorio: {IDEAS_DIR}")
    
    existentes = len(list(IDEAS_DIR.glob("*.md")))
    print(f"📊 Ideas existentes: {existentes}")
    
    if existentes >= 25:
        print("🎯 Ya hay suficientes ideas (25+). No genero más.")
        return
    
    ciclos = random.randint(2, 4)
    generadas = 0
    
    for _ in range(ciclos):
        titulo, cuerpo = generar_idea()
        resultado = guardar_idea(titulo, cuerpo)
        if resultado:
            print(f"  {resultado}")
            generadas += 1
    
    total = len(list(IDEAS_DIR.glob("*.md")))
    print(f"\n📈 Total de ideas ahora: {total}")
    print(f"✨ Generadas esta ronda: {generadas}")

if __name__ == "__main__":
    main()
