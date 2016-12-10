from OpenGL import GL
import numpy as np
import affine.affine2d.basic as basic

def draw_axis(width, height, r=0, g=0, b=0):
    GL.glColor3f(r, g, b)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2d(-width/2, 0)
    GL.glVertex2d(width/2, 0)
    GL.glVertex2d(0, -height/2)
    GL.glVertex2d(0, height/2)
    GL.glEnd()
    
def draw_planar_figure(figure, r=0, g=0, b=0):
    """
    Draws planar figure using OpenGL routines. OpenGL context should have been initialized by the moment
    you call this function.
    """
    coords = figure.get_cartesian_coords()
    GL.glBegin(GL.GL_LINE_LOOP)
    GL.glColor3f(r, g, b)
    for point in coords:
        x, y = point
        GL.glVertex2d(x, y)
    GL.glEnd()
    
def draw_3d_object(object3d, r=0, g=0, b=0, projection_matr=None, line_width=1):
    projection = (object3d.get_projection() if projection_matr is None else 
                  object3d.get_custom_projection(projection_matr))    
    points = np.apply_along_axis(basic.to_cartesian, axis=0, arr=projection)
    GL.glColor3f(r, g, b)
    GL.glLineWidth(line_width)
    GL.glBegin(GL.GL_LINES)
    for (i1, i2) in object3d.get_all_edges():
        (x1, y1), (x2, y2) = points[:,i1], points[:,i2]
        GL.glVertex2d(x1, y1)
        GL.glVertex2d(x2, y2)
    GL.glEnd()