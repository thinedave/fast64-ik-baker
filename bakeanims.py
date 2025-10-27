import bpy

def select_bone_and_constraints(bone):
    bone.bone.select = True
    
    for constraint in bone.constraints:
        if(constraint.type == "IK"):
            if(constraint.target != None): constraint.target.select_set(True)
            if(constraint.pole_target != None): constraint.pole_target.select_set(True)
        elif(constraint.type == "CHILD_OF"):
            if(constraint.target != None): constraint.target.select_set(True)

def bake(isRoot):
    bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start, frame_end=bpy.context.scene.frame_end, visual_keying=True, clear_constraints=True, use_current_action=isRoot, bake_types={"POSE", "OBJECT"}, channel_types=({"ROTATION"} if(not isRoot) else {"LOCATION", "ROTATION"}))
    

def bake_animations(context):
    armature = context.object
    if(not can_bake_animations(armature)): return {"CANCELLED"}

    root_bone = armature.pose.bones[0]
    
    bones_no_root = list(armature.pose.bones)
    bones_no_root.remove(root_bone)
    
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="DESELECT")
    
    for bone in bones_no_root:
        select_bone_and_constraints(bone)
        
    bake(False)
    
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="DESELECT")
    
    select_bone_and_constraints(root_bone)
    
    bake(True)
    
    return {"FINISHED"}

def can_bake_animations(obj):
    if(obj == None): return False
    if(obj.type != "ARMATURE"): return False

    return True
     
class BakeAnimations(bpy.types.Operator):
    """Allows fast baking of animations made with OoT IK rigs"""
    bl_idname = "object.bake_animations"
    bl_label = "(IK) Bake Animations"
    
    @classmethod
    def poll(cls, context):
        return can_bake_animations(context.object)
    
    def execute(self, context):
        return bake_animations(context)
    
def menu_func(self, context):
    self.layout.operator(BakeAnimations.bl_idname, text=BakeAnimations.bl_label)
    
def register():
    bpy.utils.register_class(BakeAnimations)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(BakeAnimations)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
if(__name__) == "__main__":
    register()