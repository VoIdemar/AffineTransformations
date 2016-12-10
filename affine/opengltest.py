from OpenGLContext import testingcontext
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np

BaseContext = testingcontext.getInteractive()

class TestContext(BaseContext):
    
    VERTEX_SHADER_CODE = """
        #version 120
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
    """
    
    FRAGMENT_SHADER_CODE = """
        #version 120
        void main() {
            gl_FragColor = vec4( 0, 1, 0, 1 );
        }
    """

    def OnInit(self):
        VERTEX_SHADER = shaders.compileShader(TestContext.VERTEX_SHADER_CODE, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(TestContext.FRAGMENT_SHADER_CODE, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.vbo = vbo.VBO(
            np.array([
                [ 0, 1, 0],
                [-1,-1, 0],
                [ 1,-1, 0],
                [ 2,-1, 0],
                [ 4,-1, 0],
                [ 4, 1, 0],
                [ 2,-1, 0],
                [ 4, 1, 0],
                [ 2, 1, 0],
            ],'f')
        )
    
    def Render(self, mode):
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try:
                glEnableClientState(GL_VERTEX_ARRAY);
                glVertexPointerf(self.vbo)
                glDrawArrays(GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY);
        finally:
            shaders.glUseProgram(0)

if __name__ == "__main__":
    TestContext.ContextMainLoop()