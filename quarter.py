"""
Quarter.py
by Phil Cote
Description: Generates spiral curves using quaternions.
Status:
The basic idea is there and working.  It could probably use some
additional touches though.

"""
import bpy
import bmesh
from mathutils import Quaternion, Vector
from math import pi
from bpy.props import IntProperty

def get_mesh_data(rad=5, point_count=10):
    axis = [0,0,-1]
    quats = [ Quaternion(axis, x) for x in range(1, point_count)] 
    
    vecs = [q * Vector((rad,0,0)) for q in quats]   
    vecs = []
    for q in quats:
        vec = q * Vector((rad,0,0))
        vecs.append(vec)
        rad+=.25
    
    coords = [(v.x,v.y,v.z) for v in vecs]
    return coords


class QuatOperator(bpy.types.Operator):
    bl_idname = "mesh.primitive_quat_add"
    bl_label = "Add Quat"
    bl_options = {'REGISTER', 'UNDO'}
    
    pc = IntProperty(
        name = "Point Count", description = "Point Count",
        min = 5, max = 50, default = 5)
    radius = IntProperty(
        name = "Radius", description = "Radius",
        min = 1, max = 10, default = 5)

    def execute(self, context):
        # set up the mesh data to be more suitable for curve objects.
        mesh_data = get_mesh_data(rad=self.radius, point_count = self.pc)
        flat_list = []
        for md in mesh_data:
            flat_list.extend(md)
            
        # build the curve
        crv = bpy.data.curves.new("crv", type="CURVE")
        spln = crv.splines.new(type="BEZIER")
        points = spln.bezier_points
        points.add(self.pc - 2)
        
        points.foreach_set("co", flat_list)
        for point in points:
            point.handle_left_type = "AUTO"
            point.handle_right_type = "AUTO"
            
        ob = bpy.data.objects.new("quat_ob", crv)        
        bpy.context.scene.objects.link(ob)
        
        return {'FINISHED'}
        
        

def menu_func(self, context):
    self.layout.operator(QuatOperator.bl_idname)


def register():
    bpy.utils.register_class(QuatOperator)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(QuatOperator)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()