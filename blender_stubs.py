# Stubs pour les modules Blender - elimine les erreurs de lint
# Ce fichier permet à VS Code de reconnaître les modules spécifiques à Blender

try:
    import bpy
    from bpy.types import *
    from bpy.props import *
    from mathutils import *
    from bmesh import *
except ImportError:
    # Stubs pour l'environnement de développement
    class PropertyGroup:
        pass
    
    class Operator:
        pass
    
    def EnumProperty(**kwargs):
        return None
    
    def FloatProperty(**kwargs):
        return None
    
    def IntProperty(**kwargs):
        return None
    
    def BoolProperty(**kwargs):
        return None
    
    def StringProperty(**kwargs):
        return None
    
    # Simuler les modules Blender pour le linter
    class bpy:
        class types:
            PropertyGroup = PropertyGroup
            Operator = Operator
        
        class props:
            EnumProperty = EnumProperty
            FloatProperty = FloatProperty
            IntProperty = IntProperty
            BoolProperty = BoolProperty
            StringProperty = StringProperty
