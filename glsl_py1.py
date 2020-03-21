import sys
import numpy as np
import cv2

from OpenGL.GL import *
import glfw

'''
[PythonでVAOによるGLSLシェーダープログラミング！ - CodeLabo](https://codelabo.com/posts/20200228182137)
[OpenGL.GL.glCompileShader Python Example](https://www.programcreek.com/python/example/95527/OpenGL.GL.glCompileShader)
[macos - GLSL: "Invalid call of undeclared identifier 'texture2D'" - Stack Overflow](https://stackoverflow.com/questions/26266198/glsl-invalid-call-of-undeclared-identifier-texture2d)
[glsles - When switching to GLSL 300, met the following error - Stack Overflow](https://stackoverflow.com/questions/26695253/when-switching-to-glsl-300-met-the-following-error)
[OpenGL.GL.glLinkProgram Python Example](https://www.programcreek.com/python/example/95622/OpenGL.GL.glLinkProgram)
'''

if __name__ == '__main__':
    img = cv2.imread('lena.png', 1)
    img_gl = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    vertex_shader_text = '''
#version 410 core

layout(location = 0) in vec3 vPosition;
layout(location = 1) in vec2 vTextureCoord;
out vec2 fTextureCoord;

void main(void) {
    fTextureCoord = vTextureCoord.xy;
    gl_Position = vec4(vPosition, 1.0);
}
'''
    fragment_shader_text = '''
#version 410 core

uniform sampler2D vTexture;
in vec2 fTextureCoord;

out vec4 flagColor;

void main(void) {
    flagColor = texture(vTexture, fTextureCoord).bgra;
}
'''

    glfw.init()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(256, 256, 'Lena', None, None)
    glfw.make_context_current(window)

    print('Vendor :', glGetString(GL_VENDOR))
    print('GPU :', glGetString(GL_RENDERER))
    print('OpenGL version :', glGetString(GL_VERSION))

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_text)
    glCompileShader(vertex_shader)
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        print('Vertex shader is not OK')
        print(glGetShaderInfoLog(vertex_shader))
        sys.exit(1)
    else:
        print('Vertex shader is OK')

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_text)
    glCompileShader(fragment_shader)
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        print('Fragment shader is not OK')
        print(glGetShaderInfoLog(fragment_shader))
        sys.exit(1)
    else:
        print('Fragment shader is OK')

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

    height, width = img.shape[:2]

    texture = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_gl)


    '''
    [pyOpenGLでシェーダープログラミング - Qiita](https://qiita.com/ar90n@github/items/934b1048b3173d2a3b04)
    '''

    vertices = np.array([
        -1.0, -1.0, 0.0,
        -1.0, 1.0, 0.0,
        1.0, 1.0, 0.0,
        1.0, -1.0, 0.0,
    ], dtype=np.float32)
    colors = np.array([
        0.0, 0.0,
        0.0, height,
        width, height,
        width, 0.0,
    ], dtype=np.float32)

    position_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, position_vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    color_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
    glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)

    vbo_indices = np.array([
        0, 1, 2,
        1, 2, 3,
    ], dtype=np.int32)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, position_vbo)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

    index_vbo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_vbo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, vbo_indices, GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    print('go')

    while not glfw.window_should_close(window):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(program)

        TEXTURE0 = 0
        glActiveTexture(GL_TEXTURE0 + TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(glGetUniformLocation(program, 'vTexture'), TEXTURE0)

        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glBindTexture(GL_TEXTURE_2D, 0)

        glfw.swap_buffers(window)
        glfw.poll_events()

        glUseProgram(0)

    glfw.destroy_window(window)
    glfw.terminate()
