# Script pour automatiser la gestion des versions
# À utiliser avec GitHub Actions ou manuellement

import os
import re
import subprocess
import sys
from datetime import datetime

def get_current_version():
    """Lit la version actuelle depuis version.py"""
    try:
        with open('version.py', 'r') as f:
            content = f.read()
            match = re.search(r'__version__ = "([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return "1.0.0"

def increment_version(version, part='patch'):
    """Incrémente la version selon le type (major, minor, patch)"""
    major, minor, patch = map(int, version.split('.'))
    
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    
    return f"{major}.{minor}.{patch}"

def update_version_file(new_version):
    """Met à jour le fichier version.py"""
    version_tuple = tuple(map(int, new_version.split('.')))
    
    content = f'''# Version de l'addon Diffuseur CAM
__version__ = "{new_version}"

# Pour le développement, vous pouvez aussi ajouter:
__version_info__ = {version_tuple}

# Informations sur la release
GITHUB_REPO = "Franckapik/diffuseurcam"
UPDATE_CHECK_URL = f"https://api.github.com/repos/{{GITHUB_REPO}}/releases/latest"
'''
    
    with open('version.py', 'w') as f:
        f.write(content)

def create_git_tag(version):
    """Crée un tag Git pour la nouvelle version"""
    try:
        subprocess.run(['git', 'add', 'version.py'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Version {version}'], check=True)
        subprocess.run(['git', 'tag', f'v{version}'], check=True)
        print(f"Tag v{version} créé avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la création du tag: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python release.py [major|minor|patch]")
        print("Exemple: python release.py minor")
        sys.exit(1)
    
    part = sys.argv[1].lower()
    if part not in ['major', 'minor', 'patch']:
        print("Type de version invalide. Utilisez: major, minor, ou patch")
        sys.exit(1)
    
    current_version = get_current_version()
    new_version = increment_version(current_version, part)
    
    print(f"Version actuelle: {current_version}")
    print(f"Nouvelle version: {new_version}")
    
    # Demande confirmation
    response = input("Continuer ? (y/N): ")
    if response.lower() != 'y':
        print("Annulé")
        sys.exit(0)
    
    # Met à jour les fichiers
    update_version_file(new_version)
    print(f"Version mise à jour vers {new_version}")
    
    # Crée le tag Git
    if create_git_tag(new_version):
        print("Pour publier sur GitHub, exécutez:")
        print(f"git push origin main && git push origin v{new_version}")

if __name__ == "__main__":
    main()
