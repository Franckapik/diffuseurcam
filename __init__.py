import bpy
import sys
import importlib
import subprocess

bl_info = {
    "name": "Diffuseur CAM",
    "description": "Génération de plans de diffuseurs",
    "author": "Franckapik",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "support": "COMMUNITY",
    "category": "Generic",
}

modulesNames = ["ops", "ui", "props"]

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = "{}.{}".format(__name__, currentModuleName)

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], "modulesNames", modulesFullNames)


def ensure_gitpython_installed():
    """Vérifie et installe GitPython si nécessaire."""
    try:
        importlib.import_module("git")
        print("[INFO] Le package 'gitpython' est déjà installé.")
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])
            print("GitPython installé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'installation de GitPython : {e}")
            raise ImportError("GitPython n'a pas pu être installé automatiquement.")


def register():
    print("[INFO] Enregistrement de l'addon...")
    ensure_gitpython_installed()  # Vérifie GitPython avant d'enregistrer les modules

    # Importer les modules après vérification des dépendances
    try:
        for currentModuleName in modulesFullNames.values():
            if currentModuleName in sys.modules:
                if hasattr(sys.modules[currentModuleName], "register"):
                    sys.modules[currentModuleName].register()
                    print("[INFO] Les modules ont été importés et enregistrés avec succès.")
    except Exception as e:
        print(f"[ERREUR] Une erreur est survenue lors de l'import ou de l'enregistrement des modules : {e}")


# Fonction pour désenregistrer l'addon
def unregister():
    print("[INFO] Désenregistrement de l'addon...")
    try:
        for currentModuleName in modulesFullNames.values():
            if currentModuleName in sys.modules:
                if hasattr(sys.modules[currentModuleName], "unregister"):
                    sys.modules[currentModuleName].unregister()
        print("[INFO] Les modules ont été désenregistrés avec succès.")
    except Exception as e:
        print(f"[ERREUR] Une erreur est survenue lors du désenregistrement des modules : {e}")


if __name__ == "__main__":
    register()

