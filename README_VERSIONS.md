# Gestion des Versions - Diffuseur CAM

## Processus de Release

### 1. Méthode Manuelle

Pour créer une nouvelle version :

```bash
# Incrémente la version patch (1.0.0 → 1.0.1)
python release.py patch

# Incrémente la version minor (1.0.1 → 1.1.0)
python release.py minor

# Incrémente la version major (1.1.0 → 2.0.0)
python release.py major
```

Puis poussez les modifications :
```bash
git push origin main && git push origin v1.0.1
```

### 2. Méthode GitHub Web

1. Allez sur GitHub → Releases → "Create a new release"
2. Choisissez un tag (ex: `v1.0.1`)
3. GitHub Actions créera automatiquement le package

### 3. Versioning Sémantique

- **MAJOR** (1.0.0 → 2.0.0) : Changements incompatibles
- **MINOR** (1.0.0 → 1.1.0) : Nouvelles fonctionnalités compatibles
- **PATCH** (1.0.0 → 1.0.1) : Corrections de bugs

## Interface Utilisateur

L'addon affiche maintenant :
- La version actuelle dans l'UI
- Un bouton pour vérifier les mises à jour
- Un bouton pour mettre à jour depuis Git

## Vérification des Mises à Jour

L'addon vérifie automatiquement les nouvelles versions via l'API GitHub :
- Compare la version locale avec la dernière release GitHub
- Informe l'utilisateur si une mise à jour est disponible

## Structure des Fichiers

```
diffuseurcam/
├── version.py              # Contient la version actuelle
├── release.py              # Script de gestion des versions
├── .github/workflows/
│   └── release.yml         # Automatisation GitHub Actions
└── README_VERSIONS.md      # Cette documentation
```

## Workflow Complet

1. **Développement** → Modifier le code
2. **Test** → Vérifier que tout fonctionne
3. **Version** → `python release.py patch`
4. **Push** → `git push origin main && git push origin v1.0.1`
5. **Release** → GitHub Actions crée automatiquement la release
6. **Distribution** → Les utilisateurs peuvent mettre à jour depuis Blender
