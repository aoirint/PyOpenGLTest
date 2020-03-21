"""
https://stackoverflow.com/questions/34348669/mapping-a-texture-onto-a-quad-with-opengl-4-python-and-vertex-shaders

Open a window that displays a quad with an image on it.

"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from math import *
from time import *


class MyApplication:
    """ Main application class. """

    def __init__(self):
        self.vao = 0

    def load_texture(self, file_name):
        image  = Image.open(file_name)
        width  = image.size[0]
        height = image.size[1]
        image_bytes  = image.convert("RGBA").tobytes ( "raw", "RGBA", 0, -1)
        texture = glGenTextures(1)

        glBindTexture     ( GL_TEXTURE_2D, texture )
        glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
        glTexParameterf   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
        glTexParameteri   ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR )
        glTexParameteri   ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR )

        gluBuild2DMipmaps ( GL_TEXTURE_2D, GL_RGBA, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image_bytes )

        return texture

    def compile_shaders(self):
        """ Get the shaders ready. """

        # Create a triangle with three (x, y, z, ?) points.
        vertex_shader_source = """
        #version 410 core
        void main( void)
        {
            // Declare a hard-coded array of positions
            const vec4 vertices[4] = vec4[4](vec4(-0.5,  0.5, 0.5, 1.0),
                                             vec4( 0.5,  0.5, 0.5, 1.0),
                                             vec4( 0.5, -0.5, 0.5, 1.0),
                                             vec4(-0.5, -0.5, 0.5, 1.0));

            // Index into our array using gl_VertexID
            gl_Position = vertices[gl_VertexID];
            }
        """

        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_source)
        glCompileShader(vertex_shader)

        # Specify the color of our fragment (RGBA)

        texture = self.load_texture("lena.png")

        fragment_shader_source = """
        #version 410 core
        uniform sampler2D s;
        out vec4 color;
        void main(void)
        {
            color = texture(s, gl_FragCoord.xy / textureSize(s, 0));
        }
        """

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_source)
        glCompileShader(fragment_shader)

        # --- Create a program
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        glGenVertexArrays(1, self.vao)
        glBindVertexArray(self.vao)

        # --- Clean up now that we don't need these shaders anymore.
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return program

    def startup(self):
        self.rendering_program = self.compile_shaders()
        self.vertex_array_object = GLuint()
        glCreateVertexArrays(1, self.vertex_array_object)

    def render(self):
        # Support transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Get a color based on the time
        color = (sin(time()), cos(time()), 0)

        # Clear the screen
        glClearBufferfv(GL_COLOR, 0, color)

        # Tell the computer what to render
        glUseProgram(self.rendering_program)
        glDrawArrays(GL_QUADS, 0, 4)

        # Display
        glutSwapBuffers()

    def animate(self):
        glutPostRedisplay()

    def run(self):
        glutInit(sys.argv)
        glutInitContextFlags(GLUT_FORWARD_COMPATIBLE)
        glutInitContextProfile(GLUT_CORE_PROFILE)
        glutInitContextVersion(4, 1)

        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(500, 500)
        glutInitWindowPosition(0, 0)

        glutCreateWindow(b"Simple PyOpenGL example")

        print('Vendor :', glGetString(GL_VENDOR))
        print('GPU :', glGetString(GL_RENDERER))
        print('OpenGL version :', glGetString(GL_VERSION))

        self.startup()

        glutIdleFunc(self.animate)
        glutDisplayFunc(self.render)

        glutMainLoop()


my_application = MyApplication()
my_application.run()
