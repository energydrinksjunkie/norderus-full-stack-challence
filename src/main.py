from grid_parser import fetch_and_parse_grid
from island_finder import find_all_islands

def main():
    grid = fetch_and_parse_grid()
    islands = find_all_islands(grid)
    for island_id, (avg_height, coordinates) in islands.items():
        print(f"island id: {island_id}, avg height: {avg_height:.2f}, coords: {coordinates}")

if __name__ == "__main__":
    main()