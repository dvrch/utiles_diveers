import ast
import astunparse  # Installe-le avec : pip install astunparse

# 1. Définis ton alias_map
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
source_path = r"C:\Users\user_name\Straightforward-Obsidian2Latex\Straightforward-Obsidian2Latex-main\src\var-alias_auto-sync.py"
target_path = r"C:\Users\user_name\Straightforward-Obsidian2Latex\Straightforward-Obsidian2Latex-main\src\var-alias_auto-sync_long.py"
class AliasRenamer(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id in alias_map:
            return ast.copy_location(ast.Name(id=alias_map[node.id], ctx=node.ctx), node)
        return node

    def visit_arg(self, node):
        if node.arg in alias_map:
            node.arg = alias_map[node.arg]
        return node

    def visit_FunctionDef(self, node):
        # Renomme les arguments de fonction
        node.args = self.visit(node.args)
        # Renomme le nom de la fonction si besoin
        if node.name in alias_map:
            node.name = alias_map[node.name]
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        # Ne remplace pas les attributs d'objet (ex: obj.a)
        self.generic_visit(node)
        return node

# 2. Lis le code source
with open(source_path, encoding="utf-8") as f:
    code = f.read()

# 3. Parse l'AST
tree = ast.parse(code)

# 4. Transforme l'AST
renamer = AliasRenamer()
new_tree = renamer.visit(tree)
ast.fix_missing_locations(new_tree)

# 5. Re-génère le code source modifié
new_code = astunparse.unparse(new_tree)

# 6. Sauvegarde ou affiche le résultat
with open(target_path, "w", encoding="utf-8") as f:
    f.write(new_code)

print("Conversion AST terminée ! Le code long est dans ton_script_long.py")
