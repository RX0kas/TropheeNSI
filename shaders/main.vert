#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in vec2 tex_coords;


out vec2 texture_coords;

uniform mat3 model_matrix;
uniform mat4 view_projection_matrix;

void main() {
    texture_coords = tex_coords;

    // coord Model -> coord Monde
    vec3 pos = model_matrix * vec3(position, 1.0);

    // deplacement du monde pour simuler une camera
    gl_Position = view_projection_matrix * vec4(pos.xy, 0.0, 1.0);
}