# Guide de Mise à Jour - Diffuseur CAM

## Pour les Utilisateurs

### Interface de l'Addon

Dans Blender, l'addon Diffuseur CAM affiche maintenant :

1. **Version actuelle** : Visible directement dans l'interface
2. **Bouton "Vérifier"** : Vérifie s'il y a une nouvelle version sur GitHub
3. **Bouton "Mettre à jour"** : Met à jour l'addon depuis Git (si configuré)
4. **Bouton "ℹ"** : Affiche les informations détaillées de l'addon

### Types de Mise à Jour

1. **Mise à jour Git** (Développeurs) :
   - Nécessite que l'addon soit installé depuis Git
   - Met à jour vers la dernière version de développement
   - Plus rapide mais peut contenir des bugs

2. **Mise à jour via GitHub Releases** (Recommandé) :
   - Téléchargement manuel depuis GitHub
   - Versions stables et testées
   - Installation classique via les préférences Blender

### Notifications

L'addon vous informe automatiquement :
- ✅ "Vous avez la dernière version"
- 🔄 "Nouvelle version disponible: X.X.X"
- ❌ Messages d'erreur en cas de problème

## Pour les Développeurs

### Création d'une Nouvelle Version

```bash
# Version patch (corrections de bugs)
python release.py patch

# Version minor (nouvelles fonctionnalités)
python release.py minor

# Version major (changements incompatibles)
python release.py major

# Puis pousser sur GitHub
git push origin main && git push origin v1.0.1
```

### Automatisation GitHub

Le workflow GitHub Actions :
1. Détecte les nouveaux tags `v*`
2. Crée automatiquement une release
3. Génère un package zip téléchargeable
4. Publie les notes de version

### Structure des Versions

- **v1.0.0** : Version stable initiale
- **v1.0.1** : Correction de bugs
- **v1.1.0** : Nouvelles fonctionnalités
- **v2.0.0** : Changements majeurs

## Bonnes Pratiques

### Pour les Utilisateurs
- Vérifiez régulièrement les mises à jour
- Lisez les notes de version avant de mettre à jour
- Sauvegardez vos projets avant les mises à jour majeures

### Pour les Développeurs
- Testez toujours avant de créer une release
- Documentez les changements dans les commits
- Utilisez des versions patch pour les corrections urgentes
- Utilisez des versions minor pour les nouvelles fonctionnalités

## Dépannage

### "Erreur lors de la vérification"
- Vérifiez votre connexion Internet
- Le repository GitHub doit être public
- L'API GitHub peut avoir des limites de taux

### "Le module 'git' n'est pas installé"
- L'addon tente d'installer GitPython automatiquement
- Si ça échoue, installez manuellement : `pip install gitpython`

### "Erreur lors de la mise à jour"
- Vérifiez que le dossier addon est un repository Git
- Assurez-vous d'avoir les permissions d'écriture
- Vérifiez qu'il n'y a pas de conflits Git
