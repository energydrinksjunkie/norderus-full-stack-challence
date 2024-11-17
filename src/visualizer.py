import pygame

GRID_SIZE = 30
CELL_SIZE = 20

COLOR_RANGES = {
    "water": {"min": 0, "max": 0, "color": "0x0000ff"},
    "low": {"min": 1, "max": 200, "color": "0xffff66"},
    "medium_low": {"min": 201, "max": 300, "color": "0x99ff33"},
    "medium_high": {"min": 301, "max": 400, "color": "0x009900"},
    "high": {"min": 401, "max": 500, "color": "0x994c00"},
    "very_high": {"min": 501, "max": 600, "color": "0x663300"},
    "extreme": {"min": 601, "max": 1000, "color": "0xc0c0c0"},
}

def height_to_color(height):
    for _, range_data in COLOR_RANGES.items():
        if range_data["min"] <= height <= range_data["max"]:
            return range_data["color"]

def render_grid(screen, grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            height = grid[row][col]
            color = height_to_color(height)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def display_message(screen, message, font, color, position):
    text = font.render(message, True, color)
    screen.blit(text, position)

def initialize_screen():
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Nordeus Game')
    return screen