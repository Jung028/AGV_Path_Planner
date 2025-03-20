import pygame
from config import BLUE, DROPDOWN_BG, DROPDOWN_BORDER, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, RED, GREEN, YELLOW

class Grid:
    def __init__(self, element_images, dropdown_images, grid_size=40):
        self.grid_size = grid_size  # Size of each grid square
        self.data = {}  # Store placed elements
        self.selected_point = None
        self.placing_point = None
        self.highlighted_point = None
        self.dropdown_active = False
        self.dropdown_options = ["Turning", "Idle", "Normal", "Charging"]
        self.element_images = element_images
        self.dropdown_images = dropdown_images
        self.dropdown_rects = {}
        self.robot_position = None  # Stores AGV position
        self.target_position = None  # Target position for movement
        self.moving = False  # Track AGV movement

        self.border_colors = {
            "Turning": BLUE,
            "Idle": YELLOW,
            "Normal": GREEN,
            "Charging": RED
        }

        for key in self.element_images:
            self.element_images[key] = pygame.transform.scale(self.element_images[key], (40, 40))
        for key in self.dropdown_images:
            self.dropdown_images[key] = pygame.transform.scale(self.dropdown_images[key], (100, 40))

    def get_grid_position(self, pos):
        """Convert pixel coordinates to grid coordinates."""
        x, y = pos
        return (x // self.grid_size * self.grid_size, y // self.grid_size * self.grid_size)

    def start_placing(self, point):
        """Begins placement mode from any clicked point."""
        self.selected_point = self.get_grid_position(point)
        self.dropdown_active = True

    def finalize_placement(self, element_type, distance):
        """Places the selected element at the specified distance, aligned to X/Y axis."""
        if self.selected_point and element_type in self.element_images:
            sr, sc = self.selected_point
            dr, dc = 0, 0
            
            if distance % self.grid_size == 0:  # Ensure it aligns with the grid
                if self.placing_point:
                    er, ec = self.placing_point
                    dr, dc = (er - sr, ec - sc)
                    if dc != 0:
                        self.placing_point = (sr, sc + distance)
                    elif dr != 0:
                        self.placing_point = (sr + distance, sc)

            self.data[self.placing_point] = element_type
            self.dropdown_active = False
            self.selected_point = None

    def start_moving_robot(self, point):
        """Places the robot or sets a target for movement."""
        grid_point = self.get_grid_position(point)
        if not self.robot_position:
            self.robot_position = grid_point
        else:
            self.target_position = grid_point
            self.moving = True

    def update_robot_movement(self):
        """Moves the robot step by step toward the target."""
        if self.moving and self.robot_position and self.target_position:
            rx, ry = self.robot_position
            tx, ty = self.target_position
            
            if rx < tx:
                rx += self.grid_size
            elif rx > tx:
                rx -= self.grid_size
            elif ry < ty:
                ry += self.grid_size
            elif ry > ty:
                ry -= self.grid_size
            
            self.robot_position = (rx, ry)
            if self.robot_position == self.target_position:
                self.moving = False

    def draw(self, screen):
        """Draws the grid, elements, and UI components."""
        screen.fill(WHITE)
        for pos, element_type in self.data.items():
            image = self.element_images.get(element_type)
            if image:
                screen.blit(image, pos)
        
        if self.robot_position:
            pygame.draw.circle(screen, RED, self.robot_position, 20)
        if self.dropdown_active and self.selected_point:
            self.draw_dropdown(screen)

    def draw_dropdown(self, screen):
        """Draws the dropdown menu."""
        x, y = self.selected_point
        self.dropdown_rects.clear()
        for i, option in enumerate(self.dropdown_options):
            option_image = self.dropdown_images.get(option)
            border_color = self.border_colors.get(option, DROPDOWN_BORDER)
            
            if option_image:
                option_rect = pygame.Rect(x + 10, y + (i * 50), 100, 40)
                pygame.draw.rect(screen, DROPDOWN_BG, option_rect)
                pygame.draw.rect(screen, border_color, option_rect, 3)
                screen.blit(option_image, option_rect.topleft)
                self.dropdown_rects[option] = option_rect

    def handle_dropdown_click(self, mouse_pos):
        """Handles dropdown selection and sets the distance."""
        if self.dropdown_active:
            for option, rect in self.dropdown_rects.items():
                if rect.collidepoint(mouse_pos):
                    try:
                        distance = int(input("Enter distance (multiples of grid size): "))
                        if distance % self.grid_size == 0:
                            self.finalize_placement(option, distance)
                    except ValueError:
                        pass
