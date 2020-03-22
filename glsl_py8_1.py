'''
[python - How to draw with Vertex Array Objects and glDrawElements in PyOpenGL - Stack Overflow](https://stackoverflow.com/questions/14365484/how-to-draw-with-vertex-array-objects-and-gldrawelements-in-pyopengl)

Thanks @NicolBolas. He motivated me to actually take this code and make it work. Instead of theoritizing:) I have removed vertexArrayObject(it's redundand as we already have VBOs for vertices and indices). So you just bind index and vertex buffers(along with attributes) prior to glDraw* call. And of course very important to pass None(null pointer) to glDrawElements indices instead of 0!
'''

from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, \
                                                  glBindVertexArray
import pygame

import numpy as np

def run():
    pygame.init()

    # pygame==2.0.0.dev6
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    screen = pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

    print('Vendor :', glGetString(GL_VENDOR))
    print('GPU :', glGetString(GL_RENDERER))
    print('OpenGL version :', glGetString(GL_VERSION))

    #Create the VBO
    vertices = np.array([[0,1,0],[-1,-1,0],[1,-1,0]], dtype='f')
    vertexPositions = vbo.VBO(vertices)

    #Create the index buffer object
    indices = np.array([[0,1,2]], dtype=np.int32)
    indexPositions = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)

    #Now create the shaders
    VERTEX_SHADER = shaders.compileShader("""
    #version 330 core
    layout(location = 0) in vec4 position;
    void main()
    {
        gl_Position = position;
    }
    """, GL_VERTEX_SHADER)

    FRAGMENT_SHADER = shaders.compileShader("""
    #version 330 core
    out vec4 outputColor;
    void main()
    {
        outputColor = vec4(0.0f, 1.0f, 0.0f, 1.0f);
    }
    """, GL_FRAGMENT_SHADER)

'''
    !! Validation Failed: No vertex array object bound.
'''
    shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

    #The draw loop
    while True:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader)

        indexPositions.bind()

        vertexPositions.bind()
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        #glDrawArrays(GL_TRIANGLES, 0, 3) #This line still works
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None) #This line does work too!

        # Show the screen
        pygame.display.flip()

run()
