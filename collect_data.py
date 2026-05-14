#!/usr/bin/env python3
"""Collect data from Obsidian vault and generate data.json for the dashboard."""

import json
import os
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path

VAULT = Path("/home/samuel/obsidian-notes/obsidian")
OUTPUT = Path("/home/samuel/codigo/sem6-dashboard/data.json")
SEMANA_6 = VAULT / "2026/Mayo/Semana 6"
SEMANA_7 = VAULT / "2026/Mayo/Semana 7"
CONOCIMIENTO = VAULT / "2026/Conocimiento"
UNIVERSIDAD = VAULT / "Universidad"
MAYO = VAULT / "2026/Mayo"


def get_current_semana():
    """Auto-detect current week folder based on date."""
    SEMESTER_START = date(2026, 3, 30)  # Week 1 starts Monday Mar 30
    today = date.today()
    delta_days = (today - SEMESTER_START).days
    if delta_days < 0:
        return 1, None
    
    week_num = (delta_days // 7) + 1
    week_num = max(1, min(week_num, 16))  # Semester is 16 weeks
    
    # Try to find the folder
    for folder_name in [f"Semana {week_num}", f"semana{week_num}", f"Semana{week_num}"]:
        folder = VAULT / "2026/Mayo" / folder_name
        if folder.exists():
            return week_num, folder
        folder = VAULT / "2026" / folder_name
        if folder.exists():
            return week_num, folder
    
    return week_num, None


def week_date_range(week_num):
    """Get date range for a given week number."""
    SEMESTER_START = date(2026, 3, 30)
    week_start = SEMESTER_START + timedelta(weeks=week_num - 1)
    week_end = week_start + timedelta(days=6)
    months_es = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Oct", 11: "Nov", 12: "Dic"
    }
    return f"{week_start.day} {months_es[week_start.month]} - {week_end.day} {months_es[week_end.month]}"


def count_notes(path):
    """Count .md files recursively."""
    return len(list(path.rglob("*.md"))) if path.exists() else 0


DAY_ORDER = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def get_weekly_progress(week_path, week_label):
    """Check which days have checkins, todolists, summaries.
    Always returns all 7 days — missing ones get empty flags."""
    days = {}
    if week_path and week_path.exists():
        day_dirs = {}
        for p in week_path.iterdir():
            if p.is_dir():
                day_dirs[p.name] = p
        for day_name in DAY_ORDER:
            day_dir = day_dirs.get(day_name)
            if day_dir and day_dir.exists():
                files = [f.name for f in day_dir.iterdir() if f.suffix == ".md"]
                days[day_name] = {
                    "checkin": "checkin" in str(files),
                    "todolist": "todolist" in str(files),
                    "summary": "summary" in str(files),
                    "todoreviewer": "todoreviewer" in str(files),
                }
            else:
                days[day_name] = {
                    "checkin": False,
                    "todolist": False,
                    "summary": False,
                    "todoreviewer": False,
                }
    else:
        for day_name in DAY_ORDER:
            days[day_name] = {
                "checkin": False,
                "todolist": False,
                "summary": False,
                "todoreviewer": False,
            }
    return {"label": week_label, "days": days}


def get_total_notes():
    """Count all notes."""
    return count_notes(VAULT)


def get_notes_by_area():
    """Count notes per main folder. Also reports uncategorized notes."""
    areas = {}
    tracked = 0
    for folder in ["2026", "Universidad", "Excalidraw"]:
        p = VAULT / folder
        if p.exists():
            c = count_notes(p)
            areas[folder] = c
            tracked += c
    total = get_total_notes()
    uncategorized = total - tracked
    if uncategorized > 0:
        areas["(otros)"] = uncategorized
    return areas


def get_today_tasks_from_vault():
    """Get today's todolist if it exists. Deduplicates by task text."""
    today = date.today()
    day_name = today.strftime("%A").lower()
    day_map = {
        "monday": "lunes", "tuesday": "martes", "wednesday": "miercoles",
        "thursday": "jueves", "friday": "viernes", "saturday": "sabado", "sunday": "domingo"
    }
    es_day = day_map.get(day_name)
    
    # Check both semana 6 and semana 7
    for semana_path in [SEMANA_6, SEMANA_7]:
        todo_file = semana_path / es_day / f"{es_day}-todolist.md"
        if todo_file.exists():
            content = todo_file.read_text()
            seen = set()
            tasks = []
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("- [ ]"):
                    task_text = stripped[5:].strip()
                    if task_text not in seen:
                        seen.add(task_text)
                        tasks.append({"task": task_text, "done": False})
                elif stripped.startswith("- [x]") or stripped.startswith("- [X]"):
                    task_text = stripped[5:].strip()
                    if task_text not in seen:
                        seen.add(task_text)
                        tasks.append({"task": task_text, "done": True})
            return {"day": es_day, "date": today.isoformat(), "tasks": tasks}
    return None


def get_project_status():
    """Check project notes for status indicators."""
    projects = {}
    
    # MaquinariasJyS
    mjys_dir = CONOCIMIENTO / "MaquinariasJyS"
    if mjys_dir.exists():
        mjys_notes = [f.stem for f in mjys_dir.iterdir() if f.suffix == ".md"]
        projects["MaquinariasJyS"] = {
            "notes": len(mjys_notes),
            "type": "🚧 Prioridad #1"
        }
    
    # QRust
    qrust_dir = CONOCIMIENTO / "QRust"
    if qrust_dir.exists():
        qrust_notes = [f.stem for f in qrust_dir.iterdir() if f.suffix == ".md"]
        projects["QRust / Klippr"] = {
            "notes": len(qrust_notes),
            "type": "🎯 En desarrollo"
        }
    
    # WeTech / La AgencIA
    lacencia = MAYO / "La AgencIA"
    if lacencia.exists():
        wt_notes = [f.stem for f in lacencia.iterdir() if f.suffix == ".md"]
        projects["WeTech / La AgencIA"] = {
            "notes": len(wt_notes),
            "type": "🌱 Semilla"
        }
    
    return projects


def get_university_status():
    """Get university course status from vault."""
    courses = {}
    
    # From memory/user profile
    courses["Cálculo II"] = {"status": "EU1 completado, EU2 pendiente"}
    courses["Sistemas Operativos"] = {"status": "PC2 entregado, TB1 en progreso"}
    courses["Estadística Aplicada"] = {"status": "EU1 examen completado, DD1 pendiente"}
    courses["Aplicaciones Móviles"] = {"status": "Entrega próxima semana"}
    
    return courses


def get_deadlines():
    """Get all course deadlines from syllabi and vault."""
    today = date.today()
    current_year = today.year
    
    # Semester start: March 30, 2026 (Week 1)
    # Week mapping: 1=Mar30-Apr5, 2=Apr6-12, 3=Apr13-19, 4=Apr20-26,
    #               5=Apr27-May3, 6=May4-10, 7=May11-17, 8=May18-24,
    #               9=May25-31, 10=Jun1-7, 11=Jun8-14, 12=Jun15-21,
    #               13=Jun22-28, 14=Jun29-Jul5, 15=Jul6-12, 16=Jul13-19

    deadlines = [
        # ---- ESTADÍSTICA APLICADA ----
        {
            "curso": "Estadística Aplicada",
            "tarea": "DD1 — Fin evaluación",
            "fecha": f"{current_year}-05-10",
            "tipo": "🔴 Entrega",
            "peso": "15%",
        },
        {
            "curso": "Estadística Aplicada",
            "tarea": "Primer avance del Trabajo",
            "fecha": f"{current_year}-05-11",
            "tipo": "📄 Avance",
            "peso": "—",
        },
        # ---- SISTEMAS OPERATIVOS ----
        {
            "curso": "Sistemas Operativos",
            "tarea": "TB1 — Trabajo 1",
            "fecha": f"{current_year}-05-17",  # Week 7 ends Sunday
            "tipo": "📄 Trabajo",
            "peso": "5%",
        },
        {
            "curso": "Sistemas Operativos",
            "tarea": "EA1 — Evaluación Parcial",
            "fecha": f"{current_year}-05-24",  # Week 8 ends Sunday
            "tipo": "📝 Examen",
            "peso": "10%",
        },
        # ---- APLICACIONES MÓVILES ----
        {
            "curso": "Aplicaciones Móviles",
            "tarea": "TB1 — Trabajo 1",
            "fecha": f"{current_year}-05-17",  # Week 7 ends Sunday
            "tipo": "📄 Trabajo",
            "peso": "15%",
        },
        {
            "curso": "Aplicaciones Móviles",
            "tarea": "EA1 — Evaluación Parcial",
            "fecha": f"{current_year}-05-24",  # Week 8 ends Sunday
            "tipo": "📝 Examen",
            "peso": "15%",
        },
        # ---- CÁLCULO II ----
        {
            "curso": "Cálculo II",
            "tarea": "DD2 / EU2 — Evaluación Unidad 2",
            "fecha": f"{current_year}-05-24",  # Estimated Week 8
            "tipo": "📝 Examen",
            "peso": "25%",
        },
    ]
    
    # Sort by date
    deadlines.sort(key=lambda d: d["fecha"])
    
    # Calculate days remaining and status
    for d in deadlines:
        try:
            dl_date = datetime.strptime(d["fecha"], "%Y-%m-%d").date()
            delta = (dl_date - today).days
            d["dias_restantes"] = delta
            
            if delta < 0:
                d["status"] = "vencido"
                d["label"] = f"⚠️ ¡VENCIDO!"
            elif delta == 0:
                d["status"] = "hoy"
                d["label"] = "🔴 ¡HOY!"
            elif delta == 1:
                d["status"] = "urgente"
                d["label"] = "🔴 ¡MAÑANA!"
            elif delta <= 3:
                d["status"] = "muy_proximo"
                d["label"] = f"🟡 En {delta} días"
            elif delta <= 7:
                d["status"] = "proximo"
                d["label"] = f"🟡 En {delta} días"
            else:
                d["status"] = "lejano"
                d["label"] = f"📌 En {delta} días"
        except:
            d["dias_restantes"] = 999
            d["status"] = "desconocido"
            d["label"] = "—"
    
    return deadlines


def get_recent_activity():
    """Get notes modified in the last 3 days."""
    import subprocess
    try:
        result = subprocess.run(
            ["find", str(VAULT), "-name", "*.md", "-newer", 
             os.popen("date -d '3 days ago' +%s").read().strip()+"c", 
             "-printf", "%T@\\t%p\\n"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        recent = []
        for line in sorted(lines, reverse=True)[:15]:
            if "\t" in line:
                ts, path = line.split("\t", 1)
                try:
                    dt = datetime.fromtimestamp(float(ts))
                    rel_path = os.path.relpath(path, str(VAULT))
                    recent.append({"path": rel_path, "modified": dt.isoformat()})
                except:
                    pass
        return recent
    except:
        # Fallback: use git log or just stat
        return []


def get_vault_structure():
    """Get top-level folder structure."""
    structure = []
    for item in sorted(VAULT.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            md_count = count_notes(item)
            if md_count > 0:
                structure.append({"name": item.name, "notes": md_count})
    return structure


def get_syllabus():
    """Return structured syllabus data for the current week.
    Move this from the inline JS SYLLABUS object so it's data-driven."""
    return {
        "calculo": {
            "name": "Cálculo II",
            "code": "1AMA0263",
            "credits": 6,
            "hours": "6h/sem (4h teoría + 2h práctica)",
            "prof": "Joel Rojas (coord.)",
            "color": "#22d3ee",
            "weeks": 16,
            "currentWeek": 7,
            "weekRange": "11 MAY – 16 MAY",
            "thisWeek": "Integrales triples en coordenadas rectangulares. Actividad colaborativa AAA2. Evaluación del AAA2 (hasta lun 18 may).",
            "units": [
                {"name": "Unidad 1: Geometría del espacio", "weeks": "1-5", "evals": "EU1 ✅ (sem 5)"},
                {"name": "Unidad 2: Integrales dobles y triples", "weeks": "6-10", "evals": "CV2 esta sem · EU2 (sem 10)"},
                {"name": "Unidad 3: Cálculo vectorial", "weeks": "11-16", "evals": "CV3 · EU3 · TF"},
            ],
            "evalFormula": "DD2 = 15% ACT2 + 15% CV2 + 70% EU2",
            "evalDetail": "ACT2 = GNP2 + PEC2 + EAAA2 + APC2 + AAD2 (AAD2: participación semanas 6 y 7)",
            "finalFormula": "PF = 0.15×DD1 + 0.25×DD2 + 0.30×DD3 + 0.30×ZB",
            "nextDeadline": {"name": "CV2 (Control Virtual 2)", "date": "Semana 7", "weight": "15% de DD2", "urgent": False},
        },
        "estadistica": {
            "name": "Estadística Aplicada",
            "code": "1AMA0741",
            "credits": 4,
            "hours": "4h/sem (3h sesión + 1h AAD)",
            "prof": "—",
            "color": "#fbbf24",
            "weeks": 16,
            "currentWeek": 7,
            "weekRange": "11 MAY – 17 MAY",
            "thisWeek": "Primer avance del trabajo (debía entregarse lun 11 Mayo). Variable aleatoria discreta. Probabilidad condicional, total y teorema de Bayes.",
            "units": [
                {"name": "DD1: Estadística descriptiva", "weeks": "1-5", "evals": "Eval 1 ✅ (sem 5) · Tareas 1-4"},
                {"name": "DD2: Probabilidad y muestreo", "weeks": "6-14", "evals": "Eval 2 (sem 12) · Tareas 5-11"},
                {"name": "ZB: Trabajo Final", "weeks": "14-16", "evals": "Entrega + Sustentación"},
            ],
            "evalFormula": "DD1 = 25% Eval 1 + 10% Prom Tareas 1-4",
            "evalDetail": "DD2 = 25% Eval 2 + 10% Prom Tareas 5-11 · ZB = 15% Entrega + 25% Sustentación",
            "finalFormula": "PF = 30% DD1 + 30% DD2 + 40% ZB",
            "nextDeadline": {"name": "Primer avance del trabajo", "date": "11 MAY (vencido ⚠️)", "weight": "—", "urgent": True},
        },
        "so": {
            "name": "Sistemas Operativos",
            "code": "1ASI0726",
            "credits": 4,
            "hours": "4h/sem",
            "prof": "Robert Zubieta Cardenas",
            "color": "#a78bfa",
            "weeks": 16,
            "currentWeek": 7,
            "weekRange": "11 MAY – 17 MAY",
            "thisWeek": "Unidad 2: Estructura y Fundamentos (sem 4-8). TB1 entregado ✅. Preparar EA1 (sem 8).",
            "units": [
                {"name": "Unidad 1: Overview", "weeks": "1-3", "evals": "PC1 ✅"},
                {"name": "Unidad 2: Estructura y Fundamentos", "weeks": "4-8", "evals": "PC2 ✅ · TB1 ✅ · EA1 (sem 8)"},
                {"name": "Unidad 3: Administración", "weeks": "9-12", "evals": "PC3 (sem 9-12)"},
                {"name": "Unidad 4: SO Principales", "weeks": "13-14", "evals": "PC4"},
                {"name": "Unidad 5: Outcome ABET 6", "weeks": "15-16", "evals": "DD1 · EB1 · TB2"},
            ],
            "evalFormula": "NF = 0.10 PC1 + 0.10 PC2 + 0.05 TB1 + 0.10 EA1 + 0.10 PC3 + 0.10 PC4 + 0.15 DD1 + 0.15 TB2 + 0.15 EB1",
            "evalDetail": "TB1 = 5% ✅ ya entregado",
            "finalFormula": "NF = 0.10 PC1 + 0.10 PC2 + 0.05 TB1 + 0.10 EA1 + 0.10 PC3 + 0.10 PC4 + 0.15 DD1 + 0.15 TB2 + 0.15 EB1",
            "nextDeadline": {"name": "EA1 — Evaluación Parcial", "date": "24 MAY (sem 8)", "weight": "10%", "urgent": False},
        },
        "appsMoviles": {
            "name": "Aplicaciones Móviles",
            "code": "1ACC0238",
            "credits": 4,
            "hours": "4h/sem",
            "prof": "Eduardo Martin Reyes Rodriguez",
            "color": "#34d399",
            "weeks": 16,
            "currentWeek": 7,
            "weekRange": "11 MAY – 17 MAY",
            "thisWeek": "Unidad 2: Native Mobile Development (sem 3-8). TB1 en progreso (~70%). Deploy backend Klippr pendiente.",
            "units": [
                {"name": "Unidad 1: Overview", "weeks": "1-2", "evals": "PC1"},
                {"name": "Unidad 2: Native Mobile Development", "weeks": "3-8", "evals": "TB1 entrega esta sem · EA Parcial 1"},
                {"name": "Unidad 3: Cross-Platform (Flutter)", "weeks": "9-12", "evals": "PC2"},
                {"name": "Unidad 4: iOS + Complementarios", "weeks": "13-16", "evals": "DD1 · EF1 · TB2"},
            ],
            "evalFormula": "PC1 + TB1 + EA Parcial + PC2 + DD1 + EF1 + TB2",
            "evalDetail": "Evaluaciones: PC1 (sem 1-2), TB1 (sem 3-8), EA Parcial, PC2 (sem 9-12), DD1, EF1, TB2",
            "finalFormula": "Evaluación por competencias (Pensamiento Innovador N2 + ABET 7 N2)",
            "nextDeadline": {"name": "TB1 — Trabajo 1 (entrega)", "date": "17 MAY (domingo)", "weight": "—", "urgent": True},
        },
    }


def main():
    current_week_num, current_week_path = get_current_semana()
    prev_week_num = current_week_num - 1 if current_week_num > 1 else 1
    
    # Try to find previous week folder
    prev_week_path = None
    for folder_name in [f"Semana {prev_week_num}", f"semana{prev_week_num}", f"Semana{prev_week_num}"]:
        p = VAULT / "2026/Mayo" / folder_name
        if p.exists():
            prev_week_path = p
            break
        p = VAULT / "2026" / folder_name
        if p.exists():
            prev_week_path = p
            break
    
    week_current_data = get_weekly_progress(current_week_path, f"Semana {current_week_num} ({week_date_range(current_week_num)})") if current_week_path else {"label": f"Semana {current_week_num}", "days": {}}
    week_prev_data = get_weekly_progress(prev_week_path, f"Semana {prev_week_num} ({week_date_range(prev_week_num)})") if prev_week_path else {"label": f"Semana {prev_week_num}", "days": {}}
    
    data = {
        "generated_at": datetime.now().isoformat(),
        "total_notes": get_total_notes(),
        "notes_by_area": get_notes_by_area(),
        "vault_structure": get_vault_structure(),
        "weekly_progress_current": week_current_data,
        "weekly_progress_prev": week_prev_data,
        "current_week": current_week_num,
        "today_tasks": get_today_tasks_from_vault(),
        "projects": get_project_status(),
        "university": get_university_status(),
        "deadlines": get_deadlines(),
        "recent_activity": get_recent_activity(),
        "syllabus": get_syllabus(),
    }
    
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"✅ Dashboard data generated: {OUTPUT}")
    print(f"   Total notes: {data['total_notes']}")
    print(f"   Projects: {len(data['projects'])}")
    print(f"   Recent activity: {len(data['recent_activity'])} files")


if __name__ == "__main__":
    main()
