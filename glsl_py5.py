'''
Triangle (Right bottom)

[Suspected fragment shader problem, No color, OpenGL 4, GLFW 3, GLEW - OpenGL / OpenGL: Basic Coding - Khronos Forums](https://community.khronos.org/t/suspected-fragment-shader-problem-no-color-opengl-4-glfw-3-glew/70399)
'''

import sys
from OpenGL.GL import *
import glfw
import numpy as np
import cv2


vertex_shader_text = '''
#version 410 core

in vec3 vPosition;

void main(void) {
    gl_Position = vec4(vPosition, 1.0);
}
'''

fragment_shader_text = '''
#version 410 core

out vec4 flagColor;

void main(void) {
    flagColor = vec4(0.5, 0.5, 0.5, 1.0);
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
    window = glfw.create_window(512, 512, 'My Window', None, None)
    glfw.make_context_current(window)

    print('Vendor :', glGetString(GL_VENDOR))
    print('GPU :', glGetString(GL_RENDERER))
    print('OpenGL version :', glGetString(GL_VERSION))

# def init_texture():
#     print('Initializing texture..')
#
#     img = cv2.imread('lena.png', 1)
#     img_gl = cv2.cvtColor(img, 0, cv2.COLOR_BGR2RGB)
#
#     global width, height
#     height, width = img.shape[:2]
#
#     glActiveTexture(GL_TEXTURE0)
#     texture = glGenTextures(1)
#
#     glBindTexture(GL_TEXTURE_2D, texture)
#     glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_gl)
#
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#
#     # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
#     # glGenerateMipMap(GL_TEXTURE_2D)
#
#     return texture

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
    print('Initializing vao..')

    # clockwise
    vertices = np.array([
        1.0, 1.0, 0.0, # right top
        1.0, -1.0, 0.0, # right bottom
        -1.0, -1.0, 0.0, # left bottom
        -1.0, 1.0, 0.0, # left top
    ], dtype=np.float32)

    colors = np.array([
        0.0, 0.0,
        0.0, height,
        width, height,
        width, 0.0,
    ], dtype=np.float32)

    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    global vertex_vao
    vertex_vao = glGenVertexArrays(1)
    glBindVertexArray(vertex_vao)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_vao)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

def draw_quad():
    glBindVertexArray(vertex_vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)

def render():
    # glEnable(GL_TEXTURE)
    # glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(program)

    # location = glGetUniformLocation(program, 'vTexture')
    # glUniform1i(location, 1)

    draw_quad()

if __name__ == '__main__':
    init_context()
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
