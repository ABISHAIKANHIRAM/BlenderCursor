import bpy
import bmesh
import random
import math
from mathutils import Vector, Matrix

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a new collection for our forest
forest_collection = bpy.data.collections.new("Forest")
bpy.context.scene.collection.children.link(forest_collection)

# Set render engine to Cycles for better lighting
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 128

# Function to create terrain
def create_terrain(size=20, subdivisions=20):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=subdivisions, y_subdivisions=subdivisions, size=size)
    terrain = bpy.context.active_object
    terrain.name = "Terrain"
    
    # Add displacement modifier
    disp_mod = terrain.modifiers.new(name="Displace", type='DISPLACE')
    
    # Create new texture for displacement
    tex = bpy.data.textures.new("TerrainTexture", 'CLOUDS')
    tex.noise_scale = 2.0
    
    disp_mod.texture = tex
    disp_mod.strength = 1.0
    disp_mod.mid_level = 0.0
    
    # Apply modifier
    bpy.ops.object.modifier_apply(modifier=disp_mod.name)
    
    # Add slight random displacement to vertices for more natural look
    mesh = terrain.data
    for v in mesh.vertices:
        v.co.z += random.uniform(-0.1, 0.1)
    
    # Create material for terrain
    mat = bpy.data.materials.new(name="TerrainMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.34, 0.52, 0.22, 1.0)  # Green color
    bsdf.inputs["Roughness"].default_value = 0.8
    
    # Assign material
    if terrain.data.materials:
        terrain.data.materials[0] = mat
    else:
        terrain.data.materials.append(mat)
    
    forest_collection.objects.link(terrain)
    bpy.context.collection.objects.unlink(terrain)
    
    return terrain

# Function to create a low-poly pine tree
def create_pine_tree(location, scale_factor=1.0):
    # Create trunk
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.1*scale_factor, depth=1.0*scale_factor, location=location)
    trunk = bpy.context.active_object
    trunk.name = "TreeTrunk"
    
    # Create trunk material
    trunk_mat = bpy.data.materials.new(name="TrunkMaterial")
    trunk_mat.use_nodes = True
    nodes = trunk_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.35, 0.2, 0.1, 1.0)  # Brown
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Assign material to trunk
    if trunk.data.materials:
        trunk.data.materials[0] = trunk_mat
    else:
        trunk.data.materials.append(trunk_mat)
    
    # Create tree top (cone)
    layers = random.randint(2, 4)
    top_height = 0.0
    tree_tops = []
    
    for i in range(layers):
        radius = 0.5 * (layers - i) / layers * scale_factor
        height = 0.6 * scale_factor
        top_loc = Vector(location) + Vector((0, 0, 0.5*scale_factor + top_height))
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=radius, radius2=0, depth=height, location=top_loc)
        tree_top = bpy.context.active_object
        tree_top.name = f"TreeTop_{i}"
        tree_tops.append(tree_top)
        top_height += height * 0.6
    
    # Create foliage material
    foliage_mat = bpy.data.materials.new(name="FoliageMaterial")
    foliage_mat.use_nodes = True
    nodes = foliage_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Randomly vary green color for diversity
    green_value = random.uniform(0.2, 0.4)
    bsdf.inputs["Base Color"].default_value = (0.1, green_value, 0.15, 1.0)  # Dark green
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Assign material to tree tops
    for top in tree_tops:
        if top.data.materials:
            top.data.materials[0] = foliage_mat
        else:
            top.data.materials.append(foliage_mat)
    
    # Join all parts into a single tree
    tree_parts = tree_tops + [trunk]
    bpy.ops.object.select_all(action='DESELECT')
    for part in tree_parts:
        part.select_set(True)
    
    bpy.context.view_layer.objects.active = trunk
    bpy.ops.object.join()
    
    tree = bpy.context.active_object
    tree.name = "PineTree"
    
    # Add tree to forest collection
    forest_collection.objects.link(tree)
    bpy.context.collection.objects.unlink(tree)
    
    return tree

# Function to create a low-poly rock
def create_rock(location, scale_factor=1.0):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.5*scale_factor, location=location)
    rock = bpy.context.active_object
    rock.name = "Rock"
    
    # Deform rock to make it more irregular
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(rock.data)
    for v in bm.verts:
        v.co += Vector((
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15)
        )) * scale_factor
    bmesh.update_edit_mesh(rock.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Scale rock to make it less spherical
    random_scale = (
        random.uniform(0.8, 1.2),
        random.uniform(0.8, 1.2),
        random.uniform(0.5, 0.8)
    )
    rock.scale = Vector(random_scale) * scale_factor
    
    # Rotate rock randomly
    rock.rotation_euler = (
        random.uniform(0, 3.14),
        random.uniform(0, 3.14),
        random.uniform(0, 3.14)
    )
    
    # Create rock material
    rock_mat = bpy.data.materials.new(name="RockMaterial")
    rock_mat.use_nodes = True
    nodes = rock_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Randomly vary gray color
    gray_value = random.uniform(0.3, 0.7)
    bsdf.inputs["Base Color"].default_value = (gray_value, gray_value, gray_value, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Assign material
    if rock.data.materials:
        rock.data.materials[0] = rock_mat
    else:
        rock.data.materials.append(rock_mat)
    
    # Add rock to forest collection
    forest_collection.objects.link(rock)
    bpy.context.collection.objects.unlink(rock)
    
    return rock

# Function to create river
def create_river(terrain):
    # Create a curved path for the river
    bpy.ops.curve.primitive_bezier_curve_add()
    river_path = bpy.context.active_object
    river_path.name = "RiverPath"
    
    # Set curve points
    curve = river_path.data
    points = curve.splines[0].bezier_points
    
    # Only two points for simplicity
    points[0].co = Vector((-10, 0, 0.2))
    points[1].co = Vector((10, 0, 0.2))
    
    # Add control points for curve
    points[0].handle_right = Vector((-5, 2, 0.2))
    points[1].handle_left = Vector((5, -2, 0.2))
    
    # Create river mesh using the curve
    bpy.ops.mesh.primitive_plane_add(size=1)
    river = bpy.context.active_object
    river.name = "River"
    
    # Add curve modifier
    curve_mod = river.modifiers.new(name="Curve", type='CURVE')
    curve_mod.object = river_path
    curve_mod.deform_axis = 'POS_X'
    
    # Scale river width
    river.scale = (10, 1, 1)
    
    # Apply modifier
    bpy.ops.object.modifier_apply(modifier=curve_mod.name)
    
    # Create river material
    river_mat = bpy.data.materials.new(name="WaterMaterial")
    river_mat.use_nodes = True
    nodes = river_mat.node_tree.nodes
    links = river_mat.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create nodes for water material
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set water properties
    principled.inputs["Base Color"].default_value = (0.1, 0.3, 0.7, 1.0)  # Blue
    principled.inputs["Roughness"].default_value = 0.1
    principled.inputs["Specular"].default_value = 0.8
    principled.inputs["IOR"].default_value = 1.33
    principled.inputs["Transmission"].default_value = 0.8
    
    # Connect nodes
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    
    # Assign material
    if river.data.materials:
        river.data.materials[0] = river_mat
    else:
        river.data.materials.append(river_mat)
    
    # Add river to forest collection
    forest_collection.objects.link(river)
    bpy.context.collection.objects.unlink(river)
    
    # Hide curve path from render
    river_path.hide_render = True
    
    return river

# Function to setup lighting for a morning look
def setup_lighting():
    # Create sun
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.name = "Sun"
    
    # Orient sun for morning light
    sun.rotation_euler = (math.radians(60), math.radians(30), math.radians(15))
    
    # Set light properties
    sun.data.energy = 2.0
    sun.data.angle = 0.1
    sun.data.color = (1.0, 0.95, 0.8)  # Warm morning light
    
    # Add ambient light (HDRI)
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create world background nodes
    output = nodes.new(type='ShaderNodeOutputWorld')
    background = nodes.new(type='ShaderNodeBackground')
    
    # Connect nodes
    links = world.node_tree.links
    links.new(background.outputs["Background"], output.inputs["Surface"])
    
    # Set blue sky color
    background.inputs["Color"].default_value = (0.5, 0.7, 1.0, 1.0)
    background.inputs["Strength"].default_value = 0.5
    
    # Add fog for morning atmosphere
    bpy.context.scene.eevee.use_volumetric_lights = True
    bpy.context.scene.eevee.volumetric_start = 0
    bpy.context.scene.eevee.volumetric_end = 100
    
    return sun

# Function to set up camera
def setup_camera():
    bpy.ops.object.camera_add(location=(15, -15, 8))
    camera = bpy.context.active_object
    camera.name = "ForestCamera"
    
    # Point camera at scene center
    track_to = camera.constraints.new(type='TRACK_TO')
    track_to.target = bpy.data.objects.get("Terrain")
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    # Set camera properties for better forest view
    camera.data.lens = 35  # Slightly wide angle
    
    return camera

# Create scene
def create_forest_scene():
    print("Creating low-poly forest scene...")
    
    # Create terrain first
    terrain = create_terrain(size=30, subdivisions=30)
    
    # Create river
    river = create_river(terrain)
    
    # Place trees
    num_trees = 60
    for i in range(num_trees):
        # Keep trees away from the river that runs through center
        while True:
            x = random.uniform(-12, 12)
            y = random.uniform(-12, 12)
            
            # River avoidance (crude estimation of river area)
            if abs(y) > 2.5 or (abs(x) > 10):
                break
        
        # Get height from terrain
        z = 0
        for v in terrain.data.vertices:
            world_co = terrain.matrix_world @ Vector((v.co.x, v.co.y, v.co.z))
            if abs(world_co.x - x) < 0.5 and abs(world_co.y - y) < 0.5:
                z = world_co.z
                break
        
        # Vary tree size
        scale = random.uniform(0.7, 1.5)
        create_pine_tree((x, y, z), scale)
    
    # Place rocks
    num_rocks = 25
    for i in range(num_rocks):
        # Place some rocks near the river
        near_river = random.random() < 0.4
        
        if near_river:
            x = random.uniform(-10, 10)
            y = random.uniform(-2.5, 2.5)
        else:
            x = random.uniform(-12, 12)
            y = random.uniform(-12, 12)
            if abs(y) < 2.5 and abs(x) < 10:
                continue  # Skip if in river area
        
        # Get height from terrain
        z = 0
        for v in terrain.data.vertices:
            world_co = terrain.matrix_world @ Vector((v.co.x, v.co.y, v.co.z))
            if abs(world_co.x - x) < 0.5 and abs(world_co.y - y) < 0.5:
                z = world_co.z
                break
        
        # Vary rock size
        scale = random.uniform(0.3, 1.0)
        create_rock((x, y, z), scale)
    
    # Setup lighting and camera
    sun = setup_lighting()
    camera = setup_camera()
    
    # Set render properties
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = False
    
    print("Forest scene created successfully!")

# Execute the scene creation
create_forest_scene()