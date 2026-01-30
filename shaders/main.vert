#version 330 core

layout (location = 0) in vec2 position;

layout (location = 1) in mat3 model_matrix;
layout (location = 4) in float u0;
layout (location = 5) in float v0;
layout (location = 6) in float u1;
layout (location = 7) in float v1;

uniform mat4 view_projection_matrix;

out vec2 TexCoords;

void main() {
    TexCoords = vec2(u0,v0);

    // coord Model -> coord Monde
    vec3 world_pos = model_matrix * vec3(position, 1.0);

    // deplacement du monde pour simuler une camera
    gl_Position = view_projection_matrix * vec4(world_pos.xy, 0.0, 1.0);
}