import pygame
import pywavefront
import numpy as np
import math
import time
import sys

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
SPEED = 1

Vl = -WINDOW_HEIGHT/2
Vb = WINDOW_HEIGHT/2
Vt = -WINDOW_WIDTH/2
Vr = WINDOW_WIDTH/2


def NDCToScreen(matrix):
    return np.matmul(
        np.array([
            [(Vr-Vl)/2, 0, 0, (Vr+Vl)/2],
            [0, (Vt-Vb)/2, 0, (Vt+Vb)/2],
            [0, 0, 1/2, 1/2],
            [0, 0, 0, 1],
        ]),
        matrix
    )


def translate(matrix, x, y, z):
    return np.matmul(
            np.array([
                [1, 0, 0, x],
                [0, 1, 0, y],
                [0, 0, 1, z],
                [0, 0, 0, 1]
            ]),
            matrix
    )


def scale(matrix, number):
    return np.matmul(
            np.array([
                [number, 0, 0, 0],
                [0, number, 0, 0],
                [0, 0, number, 0],
                [0, 0, 0, number]
            ]),
            matrix
    )


def rotate(matrix, phi, psi, theta):
    cos = math.cos
    sin = math.sin
    return np.matmul(
            np.array([
                [cos(theta)*cos(psi), -cos(phi)*sin(psi)+sin(phi)*sin(theta)*cos(psi), sin(phi)*sin(psi)+cos(phi)*sin(theta)*cos(psi), 0],
                [cos(theta)*sin(psi), cos(phi)*cos(psi)+sin(phi)*sin(theta)*sin(psi), -sin(phi)*cos(psi)+cos(phi)*sin(theta)*sin(psi), 0],
                [-sin(theta), sin(psi)*cos(theta), cos(psi)*sin(theta), 0],
                [0, 0, 0, 1]
            ]),
            matrix
    )


def perspective(matrix, c):
    return np.matmul(
        np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, -1/c, 1]
        ]),
        matrix
    )


def project(matrix):
    for i in range(3):
        matrix[i] = np.divide(matrix[i], matrix[3])
    return matrix


def getScreenCoordsFromNDC(coords):
    return (
        (coords[0] + 1)/2 * WINDOW_WIDTH,
        WINDOW_HEIGHT - ((coords[1] + 1)/2 * WINDOW_HEIGHT)
    )


def getFacesAndVerticesFromOBJ(filename):
    vectors = []
    vectors.append([])
    handler = pywavefront.Wavefront(
        filename,
        create_materials=True,
        collect_faces=True
    )
    for name, material in handler.materials.items():
        index = 0
        for i, val in enumerate(material.vertices):
            vectors[-1].append(val)
            index += 1
            if index == 3 and i != len(material.vertices)-1:
                vectors.append([])
                index = 0
    return handler.mesh_list[0].faces, handler.vertices


def run():
    if len(sys.argv) == 1:
        print("Usage: python3 renderer.py <.obj filename>")
        exit()
    start_time = time.time()
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = 1
    
    faces, vectors = getFacesAndVerticesFromOBJ(sys.argv[1]) 
    print(faces)
    print(vectors)
    x, y, z = (0, 0, 3)
    psi, phi, theta = (0, 0, 0)
    npVectors = [
        [],
        [],
        [],
        [],
    ]
    for vector in vectors:
        npVectors[0].append(
            vector[0]
        )
        npVectors[1].append(vector[1])
        npVectors[2].append(vector[2])
        npVectors[3].append(1)

    font = pygame.font.SysFont("mono", 20)

    r = 0
    while running:
        disVectors = NDCToScreen( 
            scale(
                project(
                    perspective(
                        translate(
                            rotate(
                                npVectors, 
                                psi,
                                phi,
                                theta
                            ), 
                            x,
                            y,
                            z,
                        ), 
                        10
                    )
                ),
                0.2,
            )
        )
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
 
        screen.fill((0, 0, 0))
        """
        for i in range(len(disVectors[0])):
            for j in range(len(disVectors[0])):
                drawNDCLine(screen, (255, 0, 0), 
                            [disVectors[0][i], disVectors[1][i]], 
                            [disVectors[0][j], disVectors[1][j]])
        """

        disVectors[0] += WINDOW_WIDTH/2
        disVectors[1] += WINDOW_HEIGHT/2
        for face in faces:
            pygame.draw.lines(
                screen, 
                (255, 0, 0), 
                True,
                [
                    (disVectors[0][face[0]], disVectors[1][face[0]]), 
                    (disVectors[0][face[1]], disVectors[1][face[1]]),
                    (disVectors[0][face[2]], disVectors[1][face[2]]),
                ],
            )

        pygame.event.pump()  # Allow pygame to handle internal actions.
        dt = time.time() - start_time
        freq = 1/dt
        text = font.render(str(int(freq)) + " FPS", True, (255, 255, 255))
        screen.blit(text, (0, 0))
        start_time = time.time()
        key = pygame.key.get_pressed()
        if key[pygame.K_z]:
            y += SPEED * dt
        if key[pygame.K_s]:
            y -= SPEED * dt
        if key[pygame.K_q]:
            x -= SPEED * dt
        if key[pygame.K_d]:
            x += SPEED * dt
        if key[pygame.K_a]:
            z -= SPEED * dt
        if key[pygame.K_e]:
            z += SPEED * dt
        
        if key[pygame.K_i]:
            psi += SPEED * dt
        if key[pygame.K_k]:
            psi -= SPEED * dt
        if key[pygame.K_j]:
            theta += SPEED * dt
        if key[pygame.K_l]:
            theta -= SPEED * dt
        if key[pygame.K_u]:
            phi += SPEED * dt
        if key[pygame.K_o]:
            phi -= SPEED * dt
        
        pygame.display.flip()


run()
