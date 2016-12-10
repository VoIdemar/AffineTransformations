from PyQt4.QtOpenGL import QGLWidget

import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

class QtOpenGLWidget(QGLWidget):
    
    width, height = 1000, 600
    
    def __init__(self):
        super(QtOpenGLWidget, self).__init__()
        self.rendered_data = None
        self.vertex_buffer = None
        self.vertex_count = 0
    
    def set_rendered_data(self, data):
        self.rendered_data = data
        count, _ = data.shape
        self.vertex_count = count
        self.initializeGL()
        
    def initializeGL(self):
        if not self.rendered_data is None:
            # Setting background color
            gl.glClearColor(0, 0, 0, 0)
            # Creating vertex buffer
            self.vertex_buffer = glvbo.VBO(self.rendered_data)
        
    def paintGL(self):
        if not self.vertex_buffer is None:
            # Clear buffer
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            # Set rendering color
            gl.glColor(1, 1, 0)
            # Bind the VBO
            self.vertex_buffer.bind()
            # tell OpenGL that the VBO contains an array of vertices
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            # these vertices contain 2 double precision coordinates
            gl.glVertexPointer(2, gl.GL_DOUBLE, 0, self.vertex_buffer)
            # draw "count" points from the VBO
            gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.vertex_count)
            
    def resizeGL(self, width, height):
        # update the window size
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, width, height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(-1, 1, -1, 1, -1, 1)