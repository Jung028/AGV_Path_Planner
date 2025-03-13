from flask import Flask, Response
import pygame
import threading
import cv2
import numpy as np

app = Flask(__name__)

# Pygame Simulation Class
class Simulation:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.cell_size = 20
        self.screen = pygame.Surface((self.width, self.height))  # Create a Pygame surface
        self.clock = pygame.time.Clock()

    def update(self):
        self.screen.fill((255, 255, 255))  # Clear the screen
        for row in range(0, self.width, self.cell_size):
            for col in range(0, self.height, self.cell_size):
                pygame.draw.rect(self.screen, (0, 0, 0), (row, col, self.cell_size, self.cell_size), 1)

        pygame.draw.circle(self.screen, (255, 0, 0), (300, 300), 10)  # Example robot position

    def get_frame(self):
        self.update()
        frame = pygame.surfarray.array3d(self.screen)  # Convert to numpy array
        frame = np.rot90(frame)  # Rotate
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR
        _, encoded_image = cv2.imencode('.jpg', frame)  # Encode as JPEG
        return encoded_image.tobytes()

simulation = Simulation()

# Video Streaming Generator
def generate_frames():
    while True:
        frame = simulation.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run Flask in a separate thread
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

if __name__ == "__main__":
    run_flask()
