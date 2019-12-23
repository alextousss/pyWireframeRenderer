import pygame
import pywavefront
import numpy as np
import math
import time
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
SPEED=1

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


def rotate(matrix, angle):
    return np.matmul(
            np.array([
                [1, 0, 0, 0],
                [0, math.cos(angle), -math.sin(angle), 0],
                [0, math.sin(angle), math.cos(angle), 0],
                [0, 0, 0, 1]
            ]),
            matrix
    )


def project(matrix, c):
    interm = np.matmul(
            np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, -1/c, 1]
            ]),
            matrix
    )
    for i in range(3):
        for j in range(len(interm[0])):
            interm[i][j] /= interm[3][j]
    return interm



def getScreenCoordsFromNDC(coords):
    return (
        (coords[0] + 1)/2 * WINDOW_WIDTH,
        WINDOW_HEIGHT - ( (coords[1] + 1)/2 * WINDOW_HEIGHT )
    )


def drawNDCLine(screen, color, fromCoords, toCoords):
    pygame.draw.line(
        screen, 
        color, 
        getScreenCoordsFromNDC(fromCoords), 
        getScreenCoordsFromNDC(toCoords), 
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
    start_time = time.time()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = 1
    
    faces, vectors = getFacesAndVerticesFromOBJ("cube.obj") 
    print(faces)
    print(vectors)
    # vectors = getVectorsFromOBJ("cube.obj")
    x, y, z = (0, 0, 3)
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
    
    r = 0
    while running:
        disVectors = scale(
                project(
                    translate(
                        rotate(
                            npVectors, 
                            r,
                        ), 
                        x,
                        y,
                        z,
                    ), 
                    10
                ),
                0.2
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
        for face in faces:
            drawNDCLine(screen, (255, 0, 0), 
                        [disVectors[0][face[0]], disVectors[1][face[0]]], 
                        [disVectors[0][face[1]], disVectors[1][face[1]]])
            drawNDCLine(screen, (0, 255, 0), 
                        [disVectors[0][face[1]], disVectors[1][face[1]]], 
                        [disVectors[0][face[2]], disVectors[1][face[2]]])
            drawNDCLine(screen, (0, 0, 255), 
                        [disVectors[0][face[2]], disVectors[1][face[2]]], 
                        [disVectors[0][face[0]], disVectors[1][face[0]]])
        pygame.display.flip()

        pygame.event.pump()  # Allow pygame to handle internal actions.
        dt = time.time() - start_time
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
        if key[pygame.K_r]:
            r += SPEED * dt
run()
