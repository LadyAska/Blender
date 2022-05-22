import bpy

for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
#Defining node variables
    nodes = mat.node_tree.nodes
    mixshader = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeMixShader)), None)
    transparent = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeBsdfTransparent)), None)
    light = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeLightPath)), 0)
    emission = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeEmission)), 0)
    image = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeTexImage)), None)
    output = next((n for n in nodes if isinstance(n, bpy.types.ShaderNodeOutputMaterial)), None)
    
#Checking for Mixshader/Output state
    if mixshader is None or output is None:
        continue
    
#Creating Principled node
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    
#Definining and removing Image node output links
    l = image.outputs[0].links[0]
    mat.node_tree.links.remove(l)
    ll = image.outputs[1].links[0]
    mat.node_tree.links.remove(ll)
    
#Definining and removing Light node output links
    lll = light.outputs[0].links[0]
    mat.node_tree.links.remove(lll)
    
#Definining and removing Emission node output links
    llll = emission.outputs[0].links[0]
    mat.node_tree.links.remove(llll)
    
    principled.location = (mixshader.location[0] - 100, mixshader.location[1])    
    
#Connecting Image Node to Principled
    mat.node_tree.links.new(image.outputs[0], principled.inputs[0])
    mat.node_tree.links.new(image.outputs[1], principled.inputs[21])
    
#Connecting Principled node to Output node
    mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    
#Removing unneccessary nodes
    nodes.remove(mixshader)
    nodes.remove(transparent)
    nodes.remove(light)
    nodes.remove(emission)
    
#Fixing image files
try: 
    bpy.data.images['*'].filepath = 'C:/Blender/textures/*.png' 
except:
    pass