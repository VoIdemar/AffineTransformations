from OpenGL import GLUT
from basecontext import GLUTBaseContext

class GLUTInteractiveContext(GLUTBaseContext):
    
    def __init__(self, window_name, width, height, display_func):
        super(GLUTInteractiveContext, self).__init__(
          window_name, 
          width, 
          height, 
          display_func
        )
        
    def set_keyboard_func(self, keyboard_func):
        
        def keyboard(key, x, y):
            keyboard_func(key, x, y)
            GLUT.glutPostRedisplay()
            
        GLUT.glutKeyboardFunc(keyboard)
        
    def set_mouse_func(self, mouse_func):
        
        def mouse(button, state, x, y):
            mouse_func(button, state, x, y)
            GLUT.glutPostRedisplay()
            
        GLUT.glutMouseFunc(mouse)
    
    def set_mouse_wheel_func(self, mouse_wheel_func):
        
        def mouse_wheel(button, state, x, y):
            mouse_wheel_func(button, state, x, y)
            GLUT.glutPostRedisplay()
            
        GLUT.glutMouseWheelFunc(mouse_wheel)
        
    def set_mouse_move_func(self, mouse_move_func):
        
        def mouse_wheel(x, y):
            mouse_move_func(x, y)
            GLUT.glutPostRedisplay()
            
        GLUT.glutMotionFunc(mouse_move_func)