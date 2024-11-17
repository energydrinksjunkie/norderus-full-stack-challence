import pygame
from grid_parser import fetch_and_parse_grid
from visualizer import render_grid, initialize_screen

def main():
    grid = fetch_and_parse_grid()

    screen = initialize_screen()

    render_grid(screen, grid)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
