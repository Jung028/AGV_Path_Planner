# Project Folder Structure
#
# pygame_agv_simulation/
# ├── main.py  # Entry point of the application
# ├── game.py  # Main game logic
# ├── grid.py  # Grid class managing the elements and dropdown
# ├── config.py  # Configuration and constants
# ├── agv.py  # AGV (robot) class for movement
# ├── assets/  # Folder for images and resources
# │   ├── elements/  # Images for different element types
# │   │   ├── turning.png
# │   │   ├── idle.png
# │   │   ├── normal.png
# │   │   ├── charging.png
# │   ├── dropdown/  # Images for dropdown options
# │   │   ├── turning_icon.png
# │   │   ├── idle_icon.png
# │   │   ├── normal_icon.png
# │   │   ├── charging_icon.png
#

import pygame
from config import BLUE, DROPDOWN_BG, DROPDOWN_BORDER, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, RED, GREEN, YELLOW


class Grid:
    def __init__(self, element_images, dropdown_images):
        """
        Initializes the grid with element images and dropdown images.
        """
        self.data = {}  # Store placed elements with exact screen coordinates and type
        self.selected_point = None  # Store selected element position
        self.placing_point = None  # Store placement point while dragging
        self.highlighted_point = None  # Track highlighted selected element
        self.dropdown_options = ["Turning", "Idle", "Normal", "Charging"]
        self.dropdown_active = False  # Track if dropdown should be visible
        self.element_images = element_images  # Dictionary of element type to image
        self.dropdown_images = dropdown_images  # Dictionary of dropdown option to image
        self.dropdown_rects = {}  # Store dropdown option rects for click detection

        # Define border colors for each element type
        self.border_colors = {
            "Turning": BLUE,
            "Idle": YELLOW,
            "Normal": GREEN,
            "Charging": RED
        }

        # Resize images for consistency
        for key in self.element_images:
            self.element_images[key] = pygame.transform.scale(self.element_images[key], (40, 40))
        for key in self.dropdown_images:
            self.dropdown_images[key] = pygame.transform.scale(self.dropdown_images[key], (100, 40))

        # Create a normal point in the middle of the map as the start point
        self.start_point = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.data[self.start_point] = "Normal"

    def start_placing(self, point):
        """ Begins placement mode from a selected element """
        if point in self.data:
            self.selected_point = point
            self.highlighted_point = point  # Highlight selected element
            self.placing_point = None

    def update_placing(self, cursor_pos):
        """ Restricts new placement to x or y axis relative to the selected element """
        if self.selected_point:
            sx, sy = self.selected_point
            cx, cy = cursor_pos
            
            if abs(cx - sx) > abs(cy - sy):  # Lock movement to X-axis
                self.placing_point = (cx, sy)
            else:  # Lock movement to Y-axis
                self.placing_point = (sx, cy)

    def finalize_placement(self, element_type):
        """ Confirms placement and activates dropdown """
        if self.placing_point and element_type in self.element_images:
            self.data[self.placing_point] = element_type  # Store element type
            self.highlighted_point = self.placing_point  # Highlight the new element
            self.dropdown_active = True

    def draw_dropdown(self, screen):
        """ Draws the dropdown menu with properly sized images and colored borders """
        if self.selected_point:
            x, y = self.selected_point  # Use exact screen coordinates
            self.dropdown_rects.clear()
            
            for i, option in enumerate(self.dropdown_options):
                option_image = self.dropdown_images.get(option)
                border_color = self.border_colors.get(option, DROPDOWN_BORDER)  # Get border color
                
                if option_image:
                    option_rect = pygame.Rect(x + 10, y + (i * 50), 100, 40)  # Define rect manually
                    pygame.draw.rect(screen, DROPDOWN_BG, option_rect)  # Background
                    pygame.draw.rect(screen, border_color, option_rect, 3)  # Colored border
                    screen.blit(option_image, option_rect.topleft)  # Render image
                    self.dropdown_rects[option] = option_rect  # Store rect for click detection

    def handle_dropdown_click(self, mouse_pos):
        """ Checks if the user clicked on a dropdown option """
        if self.dropdown_active:
            for option, rect in self.dropdown_rects.items():
                if rect.collidepoint(mouse_pos):
                    self.data[self.selected_point] = option
                    self.dropdown_active = False
                    self.selected_point = None
                    break

    def draw(self, screen):
        """ Draws all elements and UI components on the screen """
        screen.fill(WHITE)  # Clear screen with a plain white background

        for pos, element_type in self.data.items():
            image = self.element_images.get(element_type)
            if image:
                screen.blit(image, (pos[0] - image.get_width() // 2, 
                                    pos[1] - image.get_height() // 2))  # Draw PNG element
        
        if self.highlighted_point:
            highlight_image = self.element_images.get(self.data.get(self.highlighted_point))
            if highlight_image:
                screen.blit(highlight_image, (self.highlighted_point[0] - highlight_image.get_width() // 2, 
                                              self.highlighted_point[1] - highlight_image.get_height() // 2))
        
        if self.placing_point:
            placing_image = self.element_images.get("Normal")  # Use a default placeholder image
            if placing_image:
                screen.blit(placing_image, (self.placing_point[0] - placing_image.get_width() // 2, 
                                            self.placing_point[1] - placing_image.get_height() // 2))
        
        if self.dropdown_active and self.selected_point:
            self.draw_dropdown(screen)
