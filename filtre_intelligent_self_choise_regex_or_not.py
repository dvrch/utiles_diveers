import re
from typing import List

def find_matching_files(pattern: str, paths: List[str]) -> List[str]:
    """
    Trouve les fichiers correspondant au motif, en auto-détectant si c'est une regex ou un texte simple.
    - Si le motif contient des caractères regex spéciaux non échappés => traité comme regex
    - Sinon => traité comme texte simple (insensible à la casse)
    """
    # Détection automatique du type de motif
    if looks_like_regex(pattern):
        compiled_re = re.compile(pattern, re.IGNORECASE)
        return [p for p in paths if compiled_re.search(p)]
    else:
        pattern_lower = pattern.lower()
        return [p for p in paths if pattern_lower in p.lower()]

def looks_like_regex(pattern: str) -> bool:
    """Détecte si le motif semble être une regex (contient des caractères spéciaux non littéraux)."""
    regex_chars = {'\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(', ')'}
    i = 0
    while i < len(pattern):
        if pattern[i] == '\\':
            i += 1  # Skip le prochain caractère (échappement)
        elif pattern[i] in regex_chars:
            return True
        i += 1
    return False
# %%
all_paths = all_paths_in_folder() or [
    'C:/dossier/fl.md',
    'C:/autre/dossier/FL.MD',
    'C:/test.txt',
    'C:/notes/literature.md'
]

# Recherche textuelle automatique
print(find_matching_files('fl.md', all_paths)) 
# ['C:/dossier/fl.md', 'C:/autre/dossier/FL.MD']

# Recherche regex automatique
print(find_matching_files(r'\.md$', all_paths)) 
# ['C:/dossier/fl.md', 'C:/autre/dossier/FL.MD', 'C:/notes/literature.md']

# Mixte : texte avec caractère spécial échappé
print(find_matching_files(r'literature\.md', all_paths))
# ['C:/notes/literature.md']

