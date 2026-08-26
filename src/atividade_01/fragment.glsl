#version 330 core

in vec3 vColor;
in vec2 vPos;

out vec4 fragColor;

const vec3 STRIPE_COLOR = vec3(216.0, 18.0, 19.0) / 255.0;
const float STRIPE_WIDH = 0.05;

void main() {
    vec3 color = vColor;

    if (vPos.y < STRIPE_WIDH * 2 && vPos.y > 0) {
        // se for menor do que a parte inferior, pinta de vermelho, sim provavelmente é gambiarra, mas não ia reestruturar
        // o buffer só para passar os dados tudo de uma vez, então coloquei a constante aqui mesmo
        color = STRIPE_COLOR;
    }

    if (vPos.x > 0 && vPos.y > 0 - 0.01) {
        // escureça o lado direito da imagem
        color = color * 0.9;
    }

    fragColor = vec4(color, 1.0);
}
