#!/usr/bin/env python3
"""
Script de test pour simuler la vérification de version GitHub
"""

import json
import urllib.request
from version import __version__, UPDATE_CHECK_URL

def test_version_check():
    """Test de vérification de version"""
    print(f"Version actuelle: {__version__}")
    print(f"URL de vérification: {UPDATE_CHECK_URL}")
    
    try:
        # Note: Ce test nécessite que le repository GitHub existe et soit public
        print("\nTentative de connexion à l'API GitHub...")
        
        with urllib.request.urlopen(UPDATE_CHECK_URL, timeout=5) as response:
            data = json.loads(response.read().decode())
            
        latest_version = data['tag_name'].lstrip('v')
        print(f"Dernière version sur GitHub: {latest_version}")
        
        # Comparaison des versions
        def compare_versions(v1, v2):
            def version_tuple(v):
                return tuple(map(int, v.split('.')))
            
            v1_tuple = version_tuple(v1)
            v2_tuple = version_tuple(v2)
            
            if v1_tuple > v2_tuple:
                return 1
            elif v1_tuple < v2_tuple:
                return -1
            else:
                return 0
        
        comparison = compare_versions(latest_version, __version__)
        
        if comparison > 0:
            print(f"✅ Nouvelle version disponible: {latest_version}")
        elif comparison < 0:
            print(f"⚠️  Vous avez une version plus récente que la release ({__version__} > {latest_version})")
        else:
            print(f"✅ Vous avez la dernière version: {__version__}")
            
    except urllib.error.URLError as e:
        print(f"❌ Erreur de connexion: {e}")
        print("Vérifiez que le repository GitHub existe et est public")
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    test_version_check()
