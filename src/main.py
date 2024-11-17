import pygame
from grid_parser import fetch_and_parse_grid
from visualizer import render_grid, display_message, initialize_screen
from island_finder import find_all_islands

TRIES = 3

def find_island_with_max_avg_height(islands):
    max_avg_height = -float('inf')
    island_with_max_height = None
    for island_id, (avg_height, _) in islands.items():
        if avg_height > max_avg_height:
            max_avg_height = avg_height
            island_with_max_height = island_id
    return island_with_max_height, max_avg_height

def start_new_game():
    grid = fetch_and_parse_grid()
    islands = find_all_islands(grid)
    island_with_max_height, max_avg_height = find_island_with_max_avg_height(islands)
    return grid, islands, island_with_max_height, max_avg_height

def main():
    pygame.font.init()
    font = pygame.font.SysFont(None, 40)
    screen = initialize_screen()

    grid, islands, island_with_max_height, _ = start_new_game()
    level = 0
    total_clicks = 0
    valid_clicks = 0
    correct_guesses = 0
    attempts = TRIES
    game_over = False
    lost_game = False
    clicked_islands = set()
    needs_redraw = True
    message = ""

    while True:
        if needs_redraw:
            screen.fill((0, 0, 0))
            render_grid(screen, grid)
            display_message(screen, f"Level: {level + 1}", font, (255, 255, 255), (10, 10))
            display_message(screen, f"Attempts left: {attempts}", font, (255, 255, 255), (10, 50))
            accuracy = (correct_guesses / valid_clicks) * 100 if valid_clicks > 0 else 0
            display_message(screen, f"Accuracy: {accuracy:.2f}%", font, (255, 255, 255), (10, 90))
            if message:
                message_color = (255, 0, 0) if "Incorrect" in message or "already clicked" in message or lost_game else (0, 255, 0)
                display_message(screen, message, font, message_color, (10, 130))
            if game_over and lost_game:
                display_message(screen, "Press Q to quit or P to play again.", font, (255, 255, 255), (10, 180))
            pygame.display.update()
            needs_redraw = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // 20, y // 20
                    island_id, _ = find_island_at_position(col, row, islands)

                    if island_id:
                        if island_id in clicked_islands:
                            message = "You already clicked this island!"
                        else:
                            clicked_islands.add(island_id)
                            valid_clicks += 1
                            total_clicks += 1
                            if island_id == island_with_max_height:
                                correct_guesses += 1
                                message = "Success! Press N for next level."
                                game_over = True
                            else:
                                attempts -= 1
                                message = "Incorrect! Try again." if attempts > 0 else "Game Over: You Lost!"
                                if attempts == 0:
                                    lost_game = True
                                    game_over = True
                    else:
                        total_clicks += 1
                    needs_redraw = True

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                if event.key == pygame.K_n and not lost_game:
                    grid, islands, island_with_max_height, _ = start_new_game()
                    level += 1
                    attempts = TRIES
                    clicked_islands.clear()
                    game_over = False
                    lost_game = False
                    message = ""
                    needs_redraw = True
                if event.key == pygame.K_p and lost_game:
                    grid, islands, island_with_max_height, _ = start_new_game()
                    level = 0
                    attempts = TRIES
                    total_clicks = 0
                    valid_clicks = 0
                    correct_guesses = 0
                    clicked_islands.clear()
                    game_over = False
                    lost_game = False
                    message = ""
                    needs_redraw = True

def find_island_at_position(x, y, islands):
    for island_id, (_, coordinates) in islands.items():
        if (y, x) in coordinates:
            return island_id, _
    return None, None

if __name__ == "__main__":
    main()
