import pygame
import socket
import json
import threading

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Simulation")

# Robot Properties
robot_pos = [WIDTH // 2, HEIGHT // 2]
robot_speed = 5

# Start WebSocket Server for communication
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5001))
server.listen(1)
conn, _ = server.accept()

def receive_commands():
    global robot_pos
    while True:
        data = conn.recv(1024).decode()
        if data:
            command = json.loads(data)
            if command["action"] == "UP":
                robot_pos[1] -= robot_speed
            elif command["action"] == "DOWN":
                robot_pos[1] += robot_speed
            elif command["action"] == "LEFT":
                robot_pos[0] -= robot_speed
            elif command["action"] == "RIGHT":
                robot_pos[0] += robot_speed

threading.Thread(target=receive_commands, daemon=True).start()

# Game Loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Draw Grid
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(screen, (200, 200, 200), (x, y, 20, 20), 1)

    # Draw Robot
    pygame.draw.circle(screen, (255, 0, 0), robot_pos, 10)

    pygame.display.update()
    pygame.time.delay(50)
