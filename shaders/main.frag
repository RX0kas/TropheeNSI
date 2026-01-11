#version 330 core

in vec2 TexCoords;
out vec4 vertex;

uniform sampler2D uTexture;
uniform vec3 couleur;

void main()
{
    vertex = vec4(couleur, 1.0) * texture(uTexture, TexCoords);
}