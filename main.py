import pygame
import pywavefront
import numpy as np
import math

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


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

    return interm / interm[3][0]

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


def getVectorsFromOBJ(filename):
    vectors = []
    vectors.append([])
    handler = pywavefront.Wavefront(filename)
    for name, material in handler.materials.items():
        index = 0
        for i, val in enumerate(material.vertices):
            vectors[-1].append(val)
            index += 1
            if index == 3 and i != len(material.vertices)-1:
                vectors.append([])
                index = 0
    return vectors


def run():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = 1
    
    vectors = getVectorsFromOBJ("teapot.obj.1") 
    # vectors = getVectorsFromOBJ("cube.obj")
    
    npVectors = []
    for vector in vectors:
        npVectors.append(
                np.array([[vector[0]], [vector[1]], [vector[2]], [1]])
            )
    
    scaleFactor = 1
    while running:
        scaleFactor += 0.1
        disVectors = []
        for i in range(len(npVectors)):
            disVectors.append(
                scale(
                    project(
                        translate(
                            rotate(
                                npVectors[i], 
                                scaleFactor
                            ), 
                            0,
                            0,
                            3,
                        ), 
                        1
                    ),
                    0.2
                )
            )
        print(scaleFactor)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
 
        screen.fill((0, 0, 0))
        drawNDCLine(screen, (0, 255, 0), 
            [disVectors[0][0], disVectors[0][1], disVectors[0][2]], 
            [disVectors[-1][0], disVectors[-1][1], disVectors[-1][2]],
        )
        for i in range(len(disVectors)-1):
            drawNDCLine(screen, (0, 255, 0), 
                [disVectors[i][0], disVectors[i][1], disVectors[i][2]], 
                [disVectors[i+1][0], disVectors[i+1][1], disVectors[i+1][2]],
            )
        pygame.display.flip()


run()
