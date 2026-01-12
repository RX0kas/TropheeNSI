#version 330 core

in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D uTexture;
uniform vec3 couleur;

void main()
{
    FragColor = vec4(couleur, 1.0) * texture(uTexture, TexCoords);
}
