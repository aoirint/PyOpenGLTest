'''
Image with shader

'''

import sys
from OpenGL.GL import *
import glfw
import numpy as np
import cv2


vertex_shader_text = '''
#version 410 core

in vec3 vPosition;
in vec2 vTextureVertex;
out vec2 vTextureCoord;

void main(void) {
    // vTextureCoord = vPosition.xy;
    // vTextureCoord = vec2((vPosition.x + 1.0) / 2, (vPosition.y + 1.0) / 2);
    vTextureCoord = vTextureVertex;
    gl_Position = vec4(vPosition, 1.0);
}
'''

fragment_shader_text = '''
#version 410 core

uniform sampler2D vTexture;
in vec2 vTextureCoord;
out vec4 flagColor;

void main(void) {
    flagColor = texture(vTexture, vTextureCoord).bgra;
    // flagColor = vec4(vTextureCoord.x, 0.0, vTextureCoord.y, 1.0);
}
'''

def init_context():
    print('Initializing context..')
    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    global window
    window = glfw.create_window(512, 512, __file__, None, None)
    glfw.make_context_current(window)

    print('Vendor :', glGetString(GL_VENDOR))
    print('GPU :', glGetString(GL_RENDERER))
    print('OpenGL version :', glGetString(GL_VERSION))

def init_texture():
    print('Initializing texture..')

    img = cv2.imread('lena.png', 1)
    img_gl = cv2.cvtColor(img, 0, cv2.COLOR_BGR2RGB)

    global width, height
    height, width = img.shape[:2]

    global texture
    texture = glGenTextures(1)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_gl)

    # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # glGenerateMipMap(GL_TEXTURE_2D)

def init_shader():
    print('Initializing shader..')

    global vertex_shader
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_text)
    glCompileShader(vertex_shader)
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        print('Vertex shader is not OK')
        print(glGetShaderInfoLog(vertex_shader))
        sys.exit(1)
    else:
        print('Vertex shader is OK')

    global fragment_shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_text)
    glCompileShader(fragment_shader)
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        print('Fragment shader is not OK')
        print(glGetShaderInfoLog(fragment_shader))
        sys.exit(1)
    else:
        print('Fragment shader is OK')

    global program
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glDeleteShader(vertex_shader)
    glAttachShader(program, fragment_shader)
    glDeleteShader(fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print('Shader program is not OK')
        print(glGetProgramInfoLog(program))
        sys.exit(1)
    else:
        print('Shader program is OK')

def init_vao():
    print('Initializing vbo..')

    # clockwise
    vertices = np.array([
        1.0, 1.0, 0.0, # right top
        1.0, -1.0, 0.0, # right bottom
        -1.0, -1.0, 0.0, # left bottom

        -1.0, 1.0, 0.0, # left top
        1.0, 1.0, 0.0, # right top
        -1.0, -1.0, 0.0, # left bottom
    ], dtype=np.float32)

    texture_vertices = np.array([
        1.0, 1.0, # right top
        1.0, 0.0, # right bottom
        0.0, 0.0, # left bottom

        0.0, 1.0, # left top
        1.0, 1.0, # right top
        0.0, 0.0, # left bottom
    ], dtype=np.float32)


    global vertex_vbo
    vertex_vbo = glGenBuffers(1)

    global texture_vertex_vbo
    texture_vertex_vbo = glGenBuffers(1)

    global vertex_vao
    vertex_vao = glGenVertexArrays(1)
    glBindVertexArray(vertex_vao)

    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, vertex_vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, texture_vertex_vbo)
    glBufferData(GL_ARRAY_BUFFER, texture_vertices.nbytes, texture_vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

    glBindVertexArray(0)

def draw_quad():
    glBindVertexArray(vertex_vao)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindVertexArray(0)

def render():
    # glEnable(GL_TEXTURE)
    # glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(program)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    location = glGetUniformLocation(program, 'vTexture')
    glUniform1i(location, 0)

    draw_quad()

if __name__ == '__main__':
    init_context()
    init_texture()
    init_shader()
    init_vao()

    print('Start rendering..')
    while not glfw.window_should_close(window):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()
