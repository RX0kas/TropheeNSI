#version 330 core

layout (location = 0) in vec4 vertex;

out vec2 TexCoords;

uniform mat4 view_projection_matrix;

void main() {
    vec3 p = (view_projection_matrix * vec4(vertex.xy, 0.0, 1.0)).xyz;
    gl_Position = vec4(p,1.0);
    TexCoords = vertex.zw;
}