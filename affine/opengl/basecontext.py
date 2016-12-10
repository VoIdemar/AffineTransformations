from OpenGL import GL
from OpenGL import GLUT

class GLUTBaseContext(object):
    
    WINDOW_TITLE_FORMAT = "{0} - {1} FPS"
    
    def __init__(self, window_name, width, height, display_func):
        self.frame_count = 0
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(GLUT.GLUT_RGB | GLUT.GLUT_DOUBLE | 
                                 GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE)
        
        GLUT.glutInitWindowPosition(100, 100)
        GLUT.glutInitWindowSize(width, height)
        GLUT.glutCreateWindow(window_name)
        
        GL.glClearColor(1, 1, 1, 0)
                
        self.set_projection_mode(width, height)
        
        self.width = width
        self.height = height
        self.window_name = window_name
        
        self.set_display_func(display_func)
        self.set_reshape_func(lambda width, height: None)
        GLUT.glutTimerFunc(0, self.timer_function, 0)
        GLUT.glutIdleFunc(self.idle_function)        
    
    def set_display_func(self, display_func):
        
        def display():
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)        
            display_func()
            GLUT.glutSwapBuffers()
            self.frame_count = self.frame_count + 1
        
        GLUT.glutDisplayFunc(display)
        
    def set_reshape_func(self, reshape_func):
        
        def reshape(width, height):
            reshape_func(width, height)
            self.set_projection_mode(width, height)
            GL.glViewport(0, 0, width, height)
        
        GLUT.glutReshapeFunc(reshape)
        
    def timer_function(self, value):
        if value <> 0:
            GLUT.glutSetWindowTitle(GLUTBaseContext.WINDOW_TITLE_FORMAT.format(self.window_name, self.frame_count*4))
        self.frame_count = 0
        GLUT.glutTimerFunc(250, self.timer_function, 1)
        
    def idle_function(self):
        GLUT.glutPostRedisplay()
        
    def set_projection_mode(self, width, height):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-width/2, width/2, -height/2, height/2, -100, 100)        
        GL.glMatrixMode(GL.GL_MODELVIEW)
        
    def draw(self):
        """
        Calls GLUT main loop
        """
        GLUT.glutMainLoop()