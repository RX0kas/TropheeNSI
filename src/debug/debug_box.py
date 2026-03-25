from OpenGL.GL import *
from src.math.vectors import *
from src.graphics.shader import Shader

class DebugDraw:
    __shader:Shader|None = None
    __VAO = None
    __VBO = None

    @classmethod
    def load(cls):
        cls.__shader = Shader(contentV="""
        #version 330 core
        layout (location = 0) in vec2 pos;
        uniform mat4 view_projection_matrix;
        void main() {
            gl_Position = view_projection_matrix * vec4(pos, 0.0, 1.0);
        }
        """, contentF="""
        #version 330 core
        out vec4 color;
        uniform vec3 uColor;
        void main() {
            color = vec4(uColor, 1.0);
        }
        """)
        cls.__VAO = glGenVertexArrays(1)
        cls.__VBO = glGenBuffers(1)
        glBindVertexArray(cls.__VAO)
        glBindBuffer(GL_ARRAY_BUFFER, cls.__VBO)
        glBufferData(GL_ARRAY_BUFFER, 8 * 4, None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @classmethod
    def draw_rect(cls, position: Vec2, taille: Vec2,couleur:Vec3=Vec3(0.1,0.9,0.1)):
        if cls.__shader is None:
            return
        from src.core.application import Application

        camera = Application.get_instance().get_camera()

        x, y = position.x, position.y
        w, h = taille.x / 2, taille.y / 2

        from numpy import array, float32
        vertices = array([x - w, y - h, x + w, y - h, x + w, y + h, x - w, y + h], float32)

        cls.__shader.use()
        cls.__shader.setMat4f("view_projection_matrix", camera.get_view_projection_matrix())
        cls.__shader.setVec3f("uColor", couleur)

        glBindVertexArray(cls.__VAO)
        glBindBuffer(GL_ARRAY_BUFFER, cls.__VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)

        # GL_LINE_LOOP dessine le contour
        glDrawArrays(GL_LINE_LOOP, 0, 4)

        glBindVertexArray(0)
        glUseProgram(0)