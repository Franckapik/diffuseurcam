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

modulesNames = ['ops', 'ui', 'props']

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def ensure_gitpython_installed():
    """Vérifie et installe GitPython si nécessaire."""
    try:
        importlib.import_module("git")
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])
            print("GitPython installé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'installation de GitPython : {e}")
            raise ImportError("GitPython n'a pas pu être installé automatiquement.")


def register():
    ensure_gitpython_installed()  # Vérifie GitPython avant d'enregistrer les modules
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
