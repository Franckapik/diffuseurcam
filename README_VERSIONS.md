# Gestion des Versions - Diffuseur CAM

## Processus de Release

### 1. Méthode Script Bash (Recommandée)

Le script interactif utilise `release.py` selon la documentation :

```bash
# Lance le script interactif
./versionner.sh
```

Le script vous guide pour :
- Détecter automatiquement la version actuelle
- Choisir le type de version (major/minor/patch)
- Committer les changements en cours
- Créer la release avec release.py
- Pousser vers GitHub avec les tags

### 2. Méthode Python Directe

Pour créer une nouvelle version manuellement :

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

### 3. Méthode GitHub Web

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
├── versionner.sh           # Script bash interactif (utilise release.py)
├── .github/workflows/
│   └── release.yml         # Automatisation GitHub Actions
└── README_VERSIONS.md      # Cette documentation
```

## Workflow Complet

### Méthode Recommandée (Script Bash)
1. **Développement** → Modifier le code
2. **Test** → Vérifier que tout fonctionne  
3. **Version** → `./versionner.sh` (suit automatiquement la documentation)
4. **Distribution** → GitHub Actions crée automatiquement la release

### Méthode Alternative (Python Direct)
1. **Développement** → Modifier le code
2. **Test** → Vérifier que tout fonctionne
3. **Version** → `python release.py patch`
4. **Push** → `git push origin main && git push origin v1.0.1`
5. **Release** → GitHub Actions crée automatiquement la release
6. **Distribution** → Les utilisateurs peuvent mettre à jour depuis Blender
