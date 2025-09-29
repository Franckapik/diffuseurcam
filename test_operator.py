import bpy

# Test si l'opérateur contre-pilier existe
def test_contre_pilier_operator():
    print("🔧 [TEST] Vérification de l'opérateur contre-pilier...")
    
    # Vérifier si l'opérateur existe dans Blender
    try:
        op = bpy.ops.mesh.contre_pilier_moule
        print("✅ [TEST] Opérateur mesh.contre_pilier_moule trouvé!")
        print(f"✅ [TEST] Description: {op.__doc__}")
        return True
    except AttributeError:
        print("❌ [TEST] Opérateur mesh.contre_pilier_moule INTROUVABLE!")
        return False

# Lister tous les opérateurs mesh disponibles
def list_mesh_operators():
    print("🔧 [TEST] Opérateurs mesh disponibles contenant 'pilier':")
    for attr_name in dir(bpy.ops.mesh):
        if 'pilier' in attr_name.lower():
            print(f"  - mesh.{attr_name}")

# Tester les propriétés
def test_properties():
    print("🔧 [TEST] Vérification des propriétés...")
    scene = bpy.context.scene
    
    if hasattr(scene, 'pos_props'):
        pos_props = scene.pos_props
        if hasattr(pos_props, 'contre_pilier_moule_position'):
            print("✅ [TEST] Propriété contre_pilier_moule_position trouvée!")
            print(f"✅ [TEST] Valeur: {pos_props.contre_pilier_moule_position}")
        else:
            print("❌ [TEST] Propriété contre_pilier_moule_position MANQUANTE!")
    else:
        print("❌ [TEST] scene.pos_props MANQUANT!")

if __name__ == "__main__":
    test_contre_pilier_operator()
    list_mesh_operators()
    test_properties()
