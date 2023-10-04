import sys
from pygame_gui.ui_manager import UIManager
import pygame_gui
import pygame
import random

# Constants

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class GameOfLife:
    def __init__(self, width, height, tile_size, fps):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid_width = width // tile_size
        self.grid_height = height // tile_size
        self.fps = fps
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.positions = set()
        self.playing = False
        self.counter = 0
        self.update_rate = 120
        # Creating UI manager to handle GUI elements
        pygame.init()
        self.ui_manager = UIManager((self.width, self.height))

    def draw_grid(self, positions):
        """
            Draw the grid based on the provided positions of live cells.

            Parameters:
            positions (set): A set of (col, row) positions representing live cells to be drawn.

            This function iterates through the provided positions and draws yellow rectangles for live cells,
            and black grid lines to create a visual representation of the Game of Life grid on the screen.
            """
        for pos in positions:
            col, row = pos
            top_left = (col * self.tile_size, row * self.tile_size)
            pygame.draw.rect(self.screen, GREEN, (*top_left, self.tile_size, self.tile_size))

        for row in range(self.grid_height):
            pygame.draw.line(self.screen, GRAY, (0, row * self.tile_size), (self.width, row * self.tile_size)) # In pygame, the 0.0 coordinate is in the top left corner (y increases as you go down, which is the opposite of the Cartesian plane)
        for col in range(self.grid_width):
            pygame.draw.line(self.screen, GRAY, (col * self.tile_size, 0), (col * self.tile_size, self.height))

    def gen_positions(self, num_positions):
        """
        Generate a set of random positions within the grid.

        Parameters:
        num_positions (int): The number of positions to generate.

        Returns:
        set: A set containing randomly generated positions as (col, row) tuples.

        This function takes the desired number of positions and generates a set of random positions within
        the grid. Each position is represented as a tuple (col, row), where 'col' is the column index and 'row'
        is the row index. The positions are randomly selected within the grid's dimensions (GRID_WIDTH and GRID_HEIGHT).
        """
        return set([(random.randrange(0, self.grid_height), random.randrange(0, self.grid_width)) for _ in range(num_positions)])

    def adjust_grid(self, positions):
        """
            Apply Conway's Game of Life rules to adjust the positions of live cells based on their neighbors.

            Parameters:
            positions (set): A set of (col, row) positions representing live cells.

            Returns:
            set: A set containing the adjusted positions of live cells after applying the rules.

            This function takes a set of positions representing live cells and applies the rules of Conway's
            Game of Life to determine which cells should survive, die, or be born in the next generation.
            It considers the neighboring cells and returns a set containing the adjusted positions.
            """
        all_neighbors = set()
        new_positions = set()

        for position in positions:
            neighbors = self.get_neighbors(position)
            all_neighbors.update(neighbors)

            neighbors  = list(filter(lambda x: x in positions, neighbors))

            if len(neighbors) in [2, 3]:
                new_positions.add(position)

        for position in all_neighbors:
            neighbors = self.get_neighbors(position)
            neighbors = list(filter(lambda x: x in positions, neighbors))

            if len(neighbors) == 3:
                new_positions.add(position)

        return new_positions

    def get_neighbors(self, position):
        """
        Calculate and return a set of neighboring positions for a given position within the grid.

        Parameters:
        position (tuple): A tuple (col, row) representing the input position.

        Returns:
        list: A list of neighboring positions as (col, row) tuples.

        This function takes a position represented as a tuple (col, row) and calculates its neighboring
        positions within the grid. Neighbors are determined by moving in all eight possible directions:
        north, south, east, west, and diagonally. The resulting positions are returned as a list of tuples.
        """
        x, y = position
        neighbors = []
        for dx in [-1, 0, 1]:
            if x + dx < 0 or x + dx > self.grid_width:
                continue
            for dy in [-1, 0, 1]:
                if y + dy < 0 or y + dy > self.grid_height:
                    continue
                if dx == 0 and dy == 0:
                    continue
                neighbors.append((x + dx, y + dy))

        return neighbors

    def run(self):
        """
                Run the main loop for Conway's Game of Life.

                This function initializes game variables and enters the main game loop. It manages user interactions,
                grid updates, and rendering. The loop continues until the user closes the game window (QUIT event).
                During the game, the user can interact with the grid using the mouse and keyboard controls.

                Keyboard Controls:
                - SPACE: Pause/unpause the simulation.
                - C: Clear the grid.
                - N: Generate a random pattern on the grid.

                Mouse Controls:
                - Left-click: Toggle cell state (alive/dead) at the clicked position.

                The game continuously updates the grid's state based on the rules of Conway's Game of Life and
                displays it on the screen.
                """
        running = True
        playing = False
        self.counter = 0
        update_rate = 120
        positions = set()
        settings = Settings()

        while running:
            self.clock.tick(self.fps)

            if playing:
                self.counter += 1

            if self.counter >= update_rate:
                self.counter = 0
                positions = self.adjust_grid(positions)

            pygame.display.set_caption("Playing" if playing else "Paused")

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // self.tile_size
                    row = y // self.tile_size
                    pos = (col, row)

                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        playing = not playing

                    if event.key == pygame.K_c:
                        positions = set()
                        playing = False
                        self.counter = 0

                    if event.key == pygame.K_n:
                        positions = self.gen_positions(random.randrange(3, 10) * self.grid_width)

                    if event.key == pygame.K_s:  # Show settings menu
                        self.show_settings_menu(settings)

                    if event.key == pygame.K_q:
                        running = False

            # Draw the background
            self.screen.fill(BLACK)

            # Draw the grid
            self.draw_grid(positions)

            pygame.display.update()

        pygame.quit()

    def show_settings_menu(self, settings):
        font = pygame.font.Font(None, 36)
        text_speed = ''
        text_cell_color = ''
        text_bg_color = ''

        input_rect_speed = pygame.Rect(200, 100, 140, 32)
        input_rect_cell_color = pygame.Rect(200, 200, 140, 32)
        input_rect_bg_color = pygame.Rect(200, 300, 140, 32)

        color_active = pygame.Color('lightskyblue3')
        color_inactive = pygame.Color('dodgerblue2')

        entry_speed = pygame_gui.elements.UITextEntryLine(relative_rect=input_rect_speed, manager=self.ui_manager)
        entry_speed.set_text(text_speed)

        entry_cell_color = pygame_gui.elements.UITextEntryLine(relative_rect=input_rect_cell_color,
                                                               manager=self.ui_manager)
        entry_cell_color.set_text(text_cell_color)

        entry_bg_color = pygame_gui.elements.UITextEntryLine(relative_rect=input_rect_bg_color, manager=self.ui_manager)
        entry_bg_color.set_text(text_bg_color)

        button_apply = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 400), (100, 32)), text="Apply",
                                                    manager=self.ui_manager)
        button_cancel = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 400), (100, 32)), text="Cancel",
                                                     manager=self.ui_manager)

        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == button_apply:
                            # Handle apply button action
                            try:
                                settings.update_speed(int(entry_speed.get_text()))
                            except ValueError:
                                pass

                            try:
                                cell_color = pygame.Color(entry_cell_color.get_text())
                                settings.update_colors(cell_color, settings.background_color)
                            except ValueError:
                                pass

                            try:
                                bg_color = pygame.Color(entry_bg_color.get_text())
                                settings.update_colors(settings.cell_color, bg_color)
                            except ValueError:
                                pass

                            # Close the settings menu
                            return
                        elif event.ui_element == button_cancel:
                            # Close the settings menu without applying changes
                            return
                # Process GUI events
                self.ui_manager.process_events(event)

            # Update GUI elements
            self.ui_manager.update(time_delta)

            # Draw the settings menu
            self.screen.fill(settings.background_color)

            # Draw text entry boxes and labels
            color = color_active if entry_speed.is_focused else color_inactive
            pygame.draw.rect(self.screen, color, input_rect_speed, 2)
            text_surface = font.render('Game Speed (ms):', True, color)
            self.screen.blit(text_surface, (10, 100))
            input_rect_speed.w = max(200, text_surface.get_width() + 10)

            color = color_active if entry_cell_color.is_focused else color_inactive
            pygame.draw.rect(self.screen, color, input_rect_cell_color, 2)
            text_surface = font.render('Cell Color (e.g., R,G,B):', True, color)
            self.screen.blit(text_surface, (10, 200))
            input_rect_cell_color.w = max(200, text_surface.get_width() + 10)

            color = color_active if entry_bg_color.is_focused else color_inactive
            pygame.draw.rect(self.screen, color, input_rect_bg_color, 2)
            text_surface = font.render('Background Color (e.g., R,G,B):', True, color)
            self.screen.blit(text_surface, (10, 300))
            input_rect_bg_color.w = max(200, text_surface.get_width() + 10)

            # Draw GUI elements
            self.ui_manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()


class Settings:
    def __init__(self):
        self.game_speed = 120  # Initial game speed
        self.cell_color = GREEN  # Initial cell color
        self.background_color = BLACK  # Initial background color

    def update_speed(self, speed):
        self.game_speed = speed

    def update_colors(self, cell_color, background_color):
        self.cell_color = cell_color
        self.background_color = background_color
