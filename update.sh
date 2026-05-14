#!/bin/bash
# sem6-dashboard: Refresh vault data
cd "$(dirname "$0")"
echo "🔍 Escaneando vault de Obsidian..."
python3 collect_data.py
echo "📊 Dashboard actualizado. Abrí dashboard.html en tu navegador."
