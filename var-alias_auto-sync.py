import re
from pathlib import Path
import os
import yaml
import sys

# === EN-TÊTE : Table de correspondance ===
alias_map = {
    'a': 'cle',
    'b': 'motif',
    'c': 'chemins',
    'd': 'racine',
    'e': 'rmt',
    'f': 'motifs',
    'g': 'cle_pattern_paths',
    'h': 'fl',
}

# Fonction de synchronisation automatique des alias (robuste)
def sync_aliases():
    gbl = sys.modules[__name__].__dict__
    for alias, varname in alias_map.items():
        if varname in gbl:
            gbl[alias] = gbl[varname]

# --- DÉFINITION DES VARIABLES ---
cle = "clé_exemple"
motif = "motif_exemple"
chemins = ["chemin1", "chemin2"]
racine = Path("/chemin/absolu/vers/racine")
fl = """ 
base_path : "bbb"
lauch_sh : r"*.sh"
launch_py : 
latex_file : writing.tex
pdf_file : writing.pdf
path_vault:   example_vault  
path_writing:   ✍Writing  
path_templates:   👨‍💻Automations  
path_table_block_template:   table_block.md  
path_equation_block_template:   equation_block_single.md  
path_equation_blocks:   equation blocks  
path_table_blocks:   table blocks  
path_list_note_paths:   DO_NOT_DELETE__note_paths.txt  
path_BIBTEX:   BIBTEX  
"""

# --- DÉFINITION DES FONCTIONS ET DICTIONNAIRES AVEC ALIAS ---
racine = Path(__file__).resolve().parent
e = rmt = lambda d, b, dossier1st='d': [
    str(item)
    for dossier, sous_dossiers, fichiers in os.walk(Path(d))
    for item in (
        [*(Path(dossier)/d for d in sous_dossiers), *(Path(dossier)/f for f in fichiers)]
        if dossier1st == 'd'
        else [*(Path(dossier)/f for f in fichiers), *(Path(dossier)/d for d in sous_dossiers)]
    )
    if re.search(b, item.name, re.I)
]

# Parsing YAML du string fl
parsed_yaml = yaml.safe_load(fl)

f = motifs = {
    a: (yaml.safe_load(open("fl.md", encoding="utf-8")) 
        if Path("fl.md").is_file() else {}).get(a) 
        or val
    for a, val in parsed_yaml.items()
}

g = cle_pattern_paths = {
    a: f'{a} "{c[0]}"' if (c := e(racine, b)) else f'{a} "affich non trouvé"'
    for a, b in f.items()
}

# Synchronisation initiale des alias (après définition des variables)
sync_aliases()

# --- UTILISATION DES ALIAS PARTOUT ---
print(g)      # ou print(cle_pattern_paths)
print(a)      # alias de cle
print(cle)    # idem
print(f)      # alias de motifs
print(motifs) # idem

# Exemple d'accès à une variable intermédiaire :
for a, b in f.items():
    c = e(d, b)
    print(f"{a}: {c}")

# --- EXEMPLE DE MODIFICATION ET RESYNCHRONISATION ---
cle = "nouvelle_clé"
sync_aliases()
print(a)  # Affiche: "nouvelle_clé"
