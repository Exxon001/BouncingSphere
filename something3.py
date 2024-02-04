import pygame
import sys
import numpy as np
import math

pygame.init()

screen = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption("sphere")

radius = 200
num_segments = 50

gravity = 20
velocity = np.array((0.0,0.0,0.0), dtype=float)
position = np.array((0.0,0.0,0.0), dtype=float)
FIXED_TIME_STEP = 0.016

def calculate_sphere_vertices(radius, num_segments):
    vertices = []
    for i in range(num_segments + 1):
        phi = 2 * math.pi * i / num_segments
        for j in range(num_segments + 1):
            theta = math.pi * j / num_segments
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(theta)
            vertices.append((x, y, z))
    return vertices

def projected_vertices(vertices, width, height):
    project_vertices = []
    for vertex in vertices:
        x = int(vertex[0] + width / 2)
        y = int(height / 2 - vertex[1])
        project_vertices.append((x, y))
    return project_vertices


def rotated_vertices_x(vertices, theta):
    rotation_matrix = np.array([(1, 0, 0),
                                (0, np.cos(theta), -np.sin(theta)),
                                (0, np.sin(theta), np.cos(theta))])
    rotated_vertices = [np.dot(rotation_matrix, np.array(vertex)) for vertex in vertices]
    return rotated_vertices


def rotate_y(vertices, theta):
    rotation_matrix = np.array([(np.cos(theta), 0, np.sin(theta)),
                                (0, 1, 0),
                                (-np.sin(theta), 0, np.cos(theta))])
    rotated_vertices = [np.dot(rotation_matrix, np.array(vertex)) for vertex in vertices]
    return rotated_vertices

def rotate_z(vertices, theta):
    rotation_matrix = np.array([(np.cos(theta), -np.sin(theta), 0),
                                (np.sin(theta), np.cos(theta), 0),
                                (0, 0, 1)])
    rotated_vertices = [np.dot(rotation_matrix, np.array(vertex)) for vertex in vertices]
    return

#C++

#
matrix = [(1, 2, 3), (4, 5, 6)]

held = False
theta_x = 0
theta_y = 0


rotation_speed = 0.9

running = True
clock = pygame.time.Clock()

collision = False
original_sphere_vertices = calculate_sphere_vertices(radius, num_segments)
sphere_vertices = original_sphere_vertices.copy()

substeps = 5

checker = 0
#print(f"{original_sphere_vertices}")
#print(sphere_vertices)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                held = False
        
            

    dt = clock.tick(120) / 1000.0  # Get the time in seconds since the last tick
    rel_y, rel_x = pygame.mouse.get_rel()
    
    keys = pygame.key.get_pressed()
    # Uncomment for key control
    
    if keys[pygame.K_LEFT]:
            theta_y += rotation_speed * dt
    if keys[pygame.K_RIGHT]:
            theta_y -= rotation_speed * dt
    if keys[pygame.K_UP]:
            theta_x += rotation_speed * dt
    if keys[pygame.K_DOWN]:
            theta_x -= rotation_speed * dt
    if keys[pygame.K_a]:
            velocity[0] += -200 * dt
    if keys[pygame.K_d]:
            velocity[0] += 200 * dt
    if keys[pygame.K_SPACE]:
            
            velocity[1] *= 1.07

    
    # Uncomment for mouse control
    if held:
         
        if rel_y:
                theta_y += rel_y * dt

        if rel_x:
                theta_x += rel_x * dt
    
        
    

    rotated_vertices = rotate_y(sphere_vertices, theta_y)
    rotated_vertices = rotated_vertices_x(rotated_vertices, theta_x)
          
    
    gravity_force = np.array((0, -gravity, 0), dtype=float)
    
    velocity += gravity_force
    position += velocity * dt

    velocity *= 0.997
    rotated_vertices = [np.array(vertex) + position for vertex in rotated_vertices]

    
    
    # collision
    print(velocity[1])
    if velocity[1] >= 2000:
         velocity[1] = 2000
    if not collision:
        for i in range(len(rotated_vertices)):
            if rotated_vertices[i][1] < -700:
                velocity[1] = -velocity[1] 
                collision = True
                if velocity[1] <= 130:
                    position[1] = -500
                break
            if rotated_vertices[i][1] > 350:
                 velocity[1] = -velocity[1]
                 collision = True
                 break
                 

        for i in range(len(rotated_vertices)):
            if rotated_vertices[i][0] < -600:
                velocity[0] = -velocity[0]
                break
            if rotated_vertices[i][0] > 600:
                 velocity[0] = -velocity[0]
                 break 

                 
            

    collision = False   
    screen.fill((50, 50, 50))
    sphere_projected = projected_vertices(rotated_vertices, 1200, 600)

    for i in range(num_segments + 1):
        for j in range(num_segments + 1):
            pygame.draw.circle(screen, (100, 255, 23), sphere_projected[i * (num_segments + 1) + j], 1)
            
            

    pygame.display.flip()

