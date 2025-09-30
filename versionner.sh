#!/bin/bash

echo "=== Script de versionnement DiffuseurCam ==="
echo "📋 Utilise release.py selon la documentation officielle"
echo

# Vérifie si release.py existe
if [ ! -f release.py ]; then
    echo "❌ Fichier release.py non trouvé"
    echo "Ce script nécessite release.py pour fonctionner selon la documentation"
    exit 1
fi

# Vérifie si Python est disponible
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python non trouvé"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Fonction pour extraire la version actuelle depuis version.py
get_current_version() {
    if [ -f version.py ]; then
        grep '^__version__ = ' version.py | sed 's/__version__ = "\(.*\)"/\1/'
    else
        echo "0.0.0"
    fi
}

# Récupère la version actuelle
current_version=$(get_current_version)
echo "Version actuelle : $current_version"

# Demande le type de version
echo
echo "Types de version disponibles :"
echo "  major : Changements incompatibles (1.0.0 → 2.0.0)"
echo "  minor : Nouvelles fonctionnalités compatibles (1.0.0 → 1.1.0)"
echo "  patch : Corrections de bugs (1.0.0 → 1.0.1)"
echo
read -p "Type de version (major/minor/patch) ? " version_type

# Valide le type de version
case "$version_type" in
  major|minor|patch)
    ;;
  *)
    echo "❌ Type de version inconnu : $version_type"
    echo "Utilisez : major, minor ou patch"
    exit 1
    ;;
esac

# Vérifie si il y a des changements à committer
if git diff --quiet && git diff --cached --quiet; then
    echo "⚠️  Aucun changement détecté. Rien à committer."
    echo "Ajoutez vos modifications avant de créer une nouvelle version."
    exit 1
fi

echo
echo "📁 Changements détectés dans le repository"

# Demande un message de commit personnalisé (optionnel)
read -p "📝 Message de commit supplémentaire (optionnel) ? " extra_msg

# Commit les changements actuels avant la release
echo
echo "💾 Commit des changements en cours..."
if [ -n "$extra_msg" ]; then
    git add .
    git commit -m "$extra_msg"
    echo "✅ Changements committés avec le message personnalisé"
fi

# Exécute release.py selon la documentation
echo
echo "🚀 Création de la release avec release.py..."
echo "y" | $PYTHON_CMD release.py $version_type

if [ $? -eq 0 ]; then
    new_version=$(get_current_version)
    echo
    echo "✅ Release créée avec succès : v$new_version"
    echo
    
    # Proposition de push selon la documentation
    read -p "🌐 Pousser vers GitHub selon la documentation ? (y/n) " push_ok
    if [ "$push_ok" = "y" ] || [ "$push_ok" = "Y" ]; then
        echo "📤 Push en cours..."
        git push origin main && git push origin v$new_version
        
        if [ $? -eq 0 ]; then
            echo "✅ Release poussée vers GitHub"
            echo "🎯 GitHub Actions va maintenant créer automatiquement le package"
            echo "🔗 Vérifiez : https://github.com/Franckapik/diffuseurcam/releases"
        else
            echo "❌ Erreur lors du push"
            exit 1
        fi
    fi
    
    echo
    echo "🎉 Versionnement terminé avec succès !"
    echo "   Version : $current_version → $new_version"
    echo "   Méthode : release.py (documentée)"
    
else
    echo "❌ Erreur lors de la création de la release"
    exit 1
fi
