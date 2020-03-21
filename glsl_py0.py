import cv2
from OpenGL.GL import *
import glfw

if __name__ == '__main__':
    img = cv2.imread('lena.png', 1)
    img_gl = cv2.cvtColor(cv2.flip(img, 0), cv2.COLOR_BGR2RGB)

    glfw.init()

    # These parameters need to be changed according to your environment.
    # Mac: https://support.apple.com/ja-jp/HT202823
    # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    width = img.shape[1]
    height = img.shape[0]
    window = glfw.create_window(width, height, 'Lena', None, None)
    glfw.make_context_current(window)

    print('Vendor :', glGetString(GL_VENDOR))
    print('GPU :', glGetString(GL_RENDERER))
    print('OpenGL version :', glGetString(GL_VERSION))

    while not glfw.window_should_close(window):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDrawPixels(width, height, GL_RGB, GL_UNSIGNED_BYTE, img_gl)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()
