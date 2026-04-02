"""
snapshot_project.py
-------------------
Genere un fichier texte unique contenant tous les fichiers Python du projet.
A placer a la racine du projet et a lancer depuis le terminal :
    python snapshot_project.py

Le fichier snapshot.txt genere peut ensuite etre uploade dans Claude (claude.ai).
"""

import os
from datetime import datetime

# --- Configuration ---
EXTENSIONS = [".py"]                 # Extensions a inclure
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "env", "venv", ".vscode"}
OUTPUT_FILE = "snapshot.txt"
ROOT = "."                            # Racine du projet (dossier courant)
# ---------------------

def generate_snapshot():
    files_found = []

    for root, dirs, files in os.walk(ROOT):
        # Exclure les dossiers inutiles
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in sorted(files):
            if any(file.endswith(ext) for ext in EXTENSIONS):
                filepath = os.path.join(root, file)
                files_found.append(filepath)

    if not files_found:
        print("Aucun fichier trouve.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(f"# SNAPSHOT DU PROJET\n")
        out.write(f"# Genere le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"# Fichiers inclus : {len(files_found)}\n")
        out.write(f"# Extensions : {', '.join(EXTENSIONS)}\n")
        out.write("\n" + "="*60 + "\n")

        for filepath in files_found:
            out.write(f"\n\n# === {filepath} ===\n\n")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"[Erreur de lecture : {e}]\n")

    print(f"Snapshot genere : {OUTPUT_FILE}")
    print(f"{len(files_found)} fichiers inclus :")
    for f in files_found:
        print(f"  {f}")

if __name__ == "__main__":
    generate_snapshot()