from __future__ import annotations

import ctypes
import math
from pathlib import Path
from typing import Tuple

import glfw
import numpy as np
import OpenGL.GL.shaders as gls
from OpenGL.GL import *

Vertex = Tuple[float, float, float, float, float]
Color = Tuple[float, float, float]
Position = Tuple[float, float]
VaoId = int
VertexAmount = int
Obj = Tuple[
    VaoId, VertexAmount
]  # Gambiarra para passar os objetos com diferentes primitivas sem quebrar a cabeça


SHADER_DIR = Path(__file__).parent
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
SCREEN_PROPORTION = SCREEN_HEIGHT / SCREEN_WIDTH
STRIDE = 5 * 4
HAT_SIZE = 0.5
HAT_COLOR: Color = (254 / 255, 214 / 255, 48 / 255)
HAT_SHADOW_COLOR: Color = (21 / 255, 129 / 255, 186 / 255)
HAT_BORDER_WITH: float = 10
HAT_BORDER_BEGIN_X = -HAT_SIZE * 1.5 * SCREEN_PROPORTION
HAT_BORDER_END_X = -HAT_BORDER_BEGIN_X
BACKGROUND_COLOR = (22 / 255, 145 / 255, 205 / 255, 1)


def semi_circle(
    precision: int = 30,
    center: Position = (0.0, 0.0),
    size: float = 1.0,
    color: Color = (1.0, 1.0, 1.0),
) -> list[Vertex]:
    vertices: list[Vertex] = [(*center, *color)]

    for i in range(precision + 1):
        angle = math.radians(i * 180 / precision)
        x = math.cos(angle) * size * SCREEN_PROPORTION + center[0]
        y = math.sin(angle) * size + center[1]
        vertices.append((x, y, *color))

    return vertices


def line(
    begin: Position,
    end: Position,
    color: Color = (1.0, 1.0, 1.0),
) -> list[Vertex]:

    begin_ajusted = begin[0] * SCREEN_PROPORTION
    end_ajusted = end[0] * SCREEN_PROPORTION

    v: list[Vertex] = []
    v.append((begin_ajusted, begin[1], *color))
    v.append((end_ajusted, end[1], *color))

    return v


def create_buffers(vertices: np.ndarray) -> int:
    vaoId = glGenVertexArrays(1)
    glBindVertexArray(vaoId)

    vboId = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboId)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, STRIDE, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, STRIDE, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    return vaoId


def init() -> int:
    glClearColor(*BACKGROUND_COLOR)
    return create_shader()


def create_hat_top() -> Obj:
    v: list[Vertex] = semi_circle(precision=40, size=HAT_SIZE, color=HAT_COLOR)

    vaoId = create_buffers(np.array(v, dtype=np.float32))
    return vaoId, len(v)


def create_hat_border() -> Obj:
    v: list[Vertex] = line(
        begin=(-HAT_SIZE * 1.5, 0), end=(HAT_SIZE * 1.5, 0), color=HAT_COLOR
    )

    vaoId = create_buffers(np.array(v, dtype=np.float32))
    return vaoId, len(v)


def create_hat_shadow() -> Obj:
    v: list[Vertex] = [
        # (-HAT_SIZE, 0.0, *HAT_SHADOW_COLOR),
        (HAT_BORDER_BEGIN_X, 0.0, *HAT_SHADOW_COLOR),
        (0.0, 0.0, *HAT_SHADOW_COLOR),
        (0.0, -1.0, *HAT_SHADOW_COLOR),
        (HAT_BORDER_END_X, 0.0, *HAT_SHADOW_COLOR),
        (1.0, -1.0, *HAT_SHADOW_COLOR),
    ]

    vaoId = create_buffers(np.array(v, dtype=np.float32))
    return vaoId, len(v)


def create_hat() -> list[Obj]:
    hat: list[Obj] = [create_hat_top(), create_hat_border(), create_hat_shadow()]

    return hat


def draw_hat_border(obj: Obj):
    glBindVertexArray(obj[0])
    glLineWidth(HAT_BORDER_WITH)
    glDrawArrays(GL_LINES, 0, obj[1])
    glLineWidth(1.0)
    glBindVertexArray(0)


def draw_hat_top(obj: Obj):
    glBindVertexArray(obj[0])
    glDrawArrays(GL_TRIANGLE_FAN, 0, obj[1])
    glBindVertexArray(0)


def draw_hat_shadow(obj: Obj):
    glBindVertexArray(obj[0])
    glDrawArrays(GL_TRIANGLE_STRIP, 0, obj[1])
    glBindVertexArray(0)


def render(shaderId: int, hat: list[Obj]) -> None:
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shaderId)
    draw_hat_shadow(hat[2])
    draw_hat_top(hat[0])
    draw_hat_border(hat[1])
    glUseProgram(0)


def create_shader() -> int:
    vsSource = (SHADER_DIR / "vertex.glsl").read_text()
    fsSource = (SHADER_DIR / "fragment.glsl").read_text()
    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)

    return gls.compileProgram(vsId, fsId)


def main() -> None:
    glfw.init()
    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "one-piece", None, None)
    glfw.make_context_current(window)

    shaderId = init()

    hat = create_hat()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(shaderId, hat)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
