#!/bin/bash

echo "=== Script de versionnement DiffuseurCam ==="
echo

# Fonction pour extraire la version actuelle depuis version.py
get_current_version() {
    if [ -f version.py ]; then
        grep '^__version__ = ' version.py | sed 's/__version__ = "\(.*\)"/\1/'
    else
        echo "0.0.0"
    fi
}

# Fonction pour mettre à jour la version dans version.py
update_version_file() {
    local new_version=$1
    if [ -f version.py ]; then
        # Met à jour __version__
        sed -i "s/^__version__ = .*/__version__ = \"$new_version\"/" version.py
        
        # Met à jour __version_info__ si elle existe
        IFS='.' read -r major minor patch <<< "$new_version"
        sed -i "s/^__version_info__ = .*/__version_info__ = ($major, $minor, $patch)/" version.py
        
        echo "✓ Fichier version.py mis à jour"
    else
        echo "⚠ Fichier version.py non trouvé"
    fi
}

# Récupère la version actuelle
current_version=$(get_current_version)
echo "Version actuelle : $current_version"

# Demande le type de version
echo "Types de version disponibles :"
echo "  major : Changements incompatibles (1.0.0 → 2.0.0)"
echo "  minor : Nouvelles fonctionnalités compatibles (1.0.0 → 1.1.0)"
echo "  patch : Corrections de bugs (1.0.0 → 1.0.1)"
echo
read -p "Type de version (major/minor/patch) ? " version_type

# Calcule la nouvelle version
IFS='.' read -r major minor patch <<< "$current_version"

case "$version_type" in
  major)
    major=$((major+1))
    minor=0
    patch=0
    ;;
  minor)
    minor=$((minor+1))
    patch=0
    ;;
  patch)
    patch=$((patch+1))
    ;;
  *)
    echo "❌ Type de version inconnu : $version_type"
    echo "Utilisez : major, minor ou patch"
    exit 1
    ;;
esac

new_version="$major.$minor.$patch"
echo
echo "🚀 Nouvelle version : $new_version"
echo

# Demande le message de commit
read -p "📝 Message de commit ? " commit_msg

if [ -z "$commit_msg" ]; then
    echo "❌ Message de commit requis"
    exit 1
fi

# Vérifie si il y a des changements
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo
    echo "📁 Changements détectés, mise à jour en cours..."
    
    # Met à jour la version dans le fichier
    update_version_file "$new_version"
    
    # Ajoute tous les changements
    git add .
    
    # Commit avec le message
    echo "💾 Création du commit..."
    git commit -m "v$new_version: $commit_msg"
    
    echo "✅ Commit créé : v$new_version"
    
    # Tag optionnel
    echo
    read -p "🏷️  Créer un tag git pour cette version ? (y/n) " tag_ok
    if [ "$tag_ok" = "y" ] || [ "$tag_ok" = "Y" ]; then
        git tag "v$new_version"
        echo "✅ Tag v$new_version créé"
    fi
    
    # Proposition de push
    echo
    read -p "🌐 Pousser vers le repository distant ? (y/n) " push_ok
    if [ "$push_ok" = "y" ] || [ "$push_ok" = "Y" ]; then
        git push
        if [ "$tag_ok" = "y" ] || [ "$tag_ok" = "Y" ]; then
            git push --tags
            echo "✅ Code et tags poussés vers le repository"
        else
            echo "✅ Code poussé vers le repository"
        fi
    fi
    
else
    echo "⚠️  Aucun changement détecté. Rien à committer."
    exit 1
fi

echo
echo "🎉 Versionnement terminé avec succès !"
echo "   Version : $current_version → $new_version"
