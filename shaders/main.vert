#version 330 core

layout (location = 0) in vec2 aPos;     // position du triangle de base
layout (location = 1) in vec2 iPos;     // position de l'instance
layout (location = 2) in vec2 iScale;
layout (location = 3) in float iRot;
layout (location = 4) in vec4 iUV;      // u0 v0 u1 v1

uniform mat4 view_projection_matrix;

out vec2 TexCoords;

vec2 rotate(vec2 v, float a) {
    float c = cos(a);
    float s = sin(a);
    return vec2(
        c * v.x - s * v.y,
        s * v.x + c * v.y
    );
}

void main() {
    vec2 local = aPos * iScale;
    vec2 coordMonde = rotate(local, iRot) + iPos;
    vec3 p = (view_projection_matrix * vec4(coordMonde, 0.0, 1.0)).xyz;
    gl_Position = vec4(p,1.0);

    vec2 uvLocal = aPos + vec2(0.5);
    TexCoords = mix(iUV.xy, iUV.zw, uvLocal);
}