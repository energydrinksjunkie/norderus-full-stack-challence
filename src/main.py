import pygame
from grid_parser import fetch_and_parse_grid
from visualizer import render_grid, display_message, initialize_screen
from island_finder import find_all_islands

def find_island_with_max_avg_height(islands):
    max_avg_height = -float('inf')
    island_with_max_height = None
    for island_id, (avg_height, _) in islands.items():
        if avg_height > max_avg_height:
            max_avg_height = avg_height
            island_with_max_height = island_id
    return island_with_max_height, max_avg_height

def main():
    pygame.font.init()
    font = pygame.font.SysFont(None, 40)
    screen = initialize_screen()

    def start_new_game():
        grid = fetch_and_parse_grid()
        islands = find_all_islands(grid)
        island_with_max_height, max_avg_height = find_island_with_max_avg_height(islands)
        return grid, islands, island_with_max_height, max_avg_height, 3

    grid, islands, island_with_max_height, max_avg_height, tries = start_new_game()
    running = True
    game_over = False
    incorrect_message = False
    try_again_message = False
    incorrect_timer = None
    success_message = False
    needs_redraw = True

    while running:
        if needs_redraw:
            render_grid(screen, grid)
            display_message(screen, f"Attempts left: {tries}", font, (255, 255, 255), (10, 10))

            if incorrect_message:
                display_message(screen, "Incorrect!", font, (255, 0, 0), (10, 50))

            if game_over:
                if success_message:
                    display_message(screen, f"Success! Highest avg height: {max_avg_height:.2f}.", font, (0, 255, 0), (10, 50))
                else:
                    display_message(screen, "Game Over: You Lost!", font, (255, 0, 0), (10, 50))
                display_message(screen, "Press Q to quit or P to try again.", font, (255, 255, 255), (10, 90))

            pygame.display.update()
            needs_redraw = False

        if incorrect_timer and pygame.time.get_ticks() > incorrect_timer:
            incorrect_message = False
            incorrect_timer = None
            needs_redraw = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    col = x // 20
                    row = y // 20
                    island_id, avg_height = find_island_at_position(col, row, islands)
                    if island_id:
                        if island_id == island_with_max_height:
                            game_over = True
                            success_message = True
                            try_again_message = True
                            needs_redraw = True
                        else:
                            tries -= 1
                            if tries > 0:
                                incorrect_message = True
                                incorrect_timer = pygame.time.get_ticks() + 1500
                                needs_redraw = True
                            else:
                                game_over = True
                                success_message = False
                                try_again_message = True
                                needs_redraw = True

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_p:
                        grid, islands, island_with_max_height, max_avg_height, tries = start_new_game()
                        game_over = False
                        incorrect_message = False
                        try_again_message = False
                        incorrect_timer = None
                        success_message = False
                        needs_redraw = True

    pygame.quit()

def find_island_at_position(x, y, islands):
    for island_id, (avg_height, coordinates) in islands.items():
        if (y, x) in coordinates:
            return island_id, avg_height
    return None, None

if __name__ == "__main__":
    main()
