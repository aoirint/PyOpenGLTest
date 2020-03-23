'''
## Image with Fisheye shader

### Requirements

PyOpenGL==3.1.5
glfw==1.11.0

Vendor : b'Intel Inc.'
GPU : b'Intel Iris OpenGL Engine'
OpenGL version : b'4.1 INTEL-14.4.23'


[processing-docs/FishEye.glsl at 0c4cdc27af14727413189dd0660773c6b928ebf4 · processing/processing-docs](https://github.com/processing/processing-docs/blob/0c4cdc27af14727413189dd0660773c6b928ebf4/content/examples/Topics/Shaders/GlossyFishEye/data/FishEye.glsl)
[FisheyeCalibration - Kota Yamaguchi's Wiki](http://ishikawa-vision.org/~kyamagu/cgi-bin/moin.cgi/FisheyeCalibration/)
[魚眼カメラモデル (fisheye camera model)](http://www.sanko-shoko.net/note.php?id=wvb7)
[OpenGL - Textures](https://open.gl/textures)
'''

import sys
from OpenGL.GL import *
import glfw
import numpy as np
import cv2


vertex_shader_text = '''
#version 410 core

in vec3 vPosition;
out vec3 vFragmentPosition;

void main(void) {
    vFragmentPosition = vec3(vPosition.x, vPosition.y, vPosition.z);
    gl_Position = vec4(vPosition.x, vPosition.y, vPosition.z, 1.0);
}
'''

fragment_shader_text = '''
#version 410 core

const float PI = 3.141592653589793;
const float S = 1024;

uniform sampler2D vTexture;
in vec3 vFragmentPosition;
out vec4 flagColor;

float atan2(in float y, in float x) {
    return x == 0.0 ? sign(y)*PI/2 : atan(y, x);
}

void main(void) {
    float k1 = 1.0;
    float k2 = 1.0;
    float k3 = 1.0;
    float k4 = 1.0;

    float x = (gl_FragCoord.x/S - 0.5) * 2.0;
    float y = (gl_FragCoord.y/S - 0.5) * 2.0;

    float n = length(vec2(x, y));
    if (n > 1) {
        flagColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
    else {
        float z = sqrt(1.0 - n*n);

        float r = atan2(n, z);
        float theta = atan2(y, x);

        float r2 = r*r;
        float r4 = r2*r2;
        float r6 = r2*r4;
        float r8 = r4*r4;

        float r_d = r * (1 + k1 * r2 + k2 * r4 + k3 * r6 + k4 * r8);

        float x_d = r_d * cos(theta);
        float y_d = r_d * sin(theta);

        vec2 vTexCoord = vec2((x_d + 1.0) / 2.0, (y_d + 1.0) / 2.0);

        flagColor = texture(vTexture, vTexCoord).rgba;
    }

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
    img_gl = cv2.cvtColor(cv2.flip(img, 0), cv2.COLOR_BGR2RGB)

    global width, height
    height, width = img.shape[:2]

    global texture
    texture = glGenTextures(1)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # https://open.gl/textures
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_gl)

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

    # anti-clockwise
    vertices = np.array([
        -1.0, -1.0, 0.0, # left bottom
        1.0, -1.0, 0.0, # right bottom
        -1.0, 1.0, 0.0, # left top

        -1.0, 1.0, 0.0, # left top
        1.0, -1.0, 0.0, # right bottom
        1.0, 1.0, 0.0, # right top
    ], dtype=np.float32)

    global vertex_vbo
    vertex_vbo = glGenBuffers(1)

    global vertex_vao
    vertex_vao = glGenVertexArrays(1)
    glBindVertexArray(vertex_vao)

    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, vertex_vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

    glBindVertexArray(0)

def render():
    glUseProgram(program)

    glUniform1i(glGetUniformLocation(program, 'vTexture'), 0)

    glBindVertexArray(vertex_vao)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindVertexArray(0)

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
