import sys

if __name__ == '__main__':
    
    from affine.ui.glcanvas3d import GLCanvas3DForm   
    from affine.datainput.input import read_geometry_from_obj_file
    from affine.datastruct.object3d import Object3D
    	
    vertices, faces = read_geometry_from_obj_file('C:\\Users\\Voldemar\\Desktop\\untitled.obj')    
    obj3d = Object3D(vertices, faces)
    form = GLCanvas3DForm(obj3d, "Affine transformations with GLUT", 1000, 600)
    form.run_context()
