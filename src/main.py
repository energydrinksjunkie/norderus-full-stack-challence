import requests

def fetch_and_parse_grid():
    url = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"
    response = requests.get(url)
    raw_data = response.text.strip()
    
    grid = [
        list(map(int, row.split()))
        for row in raw_data.split('\n')
    ]
    return grid

def find_all_islands(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    islands = {}

    def dfs(row, col, island_id):
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col] or grid[row][col] == 0:
            return 0, 0, []

        visited[row][col] = True
        size = 1
        height_sum = grid[row][col]
        coordinates = [(row, col)]

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            sub_size, sub_sum, sub_coords = dfs(row + dr, col + dc, island_id)
            size += sub_size
            height_sum += sub_sum
            coordinates.extend(sub_coords)

        return size, height_sum, coordinates

    island_id = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and grid[r][c] > 0:
                size, height_sum, coordinates = dfs(r, c, island_id)
                if size > 0:
                    avg_height = height_sum / size
                    island_id += 1
                    islands[island_id] = (avg_height, coordinates)

    return islands
grid = fetch_and_parse_grid()

islands = find_all_islands(grid)

for island_id, (avg_height, coords) in islands.items():
    print(f"island id {island_id}: avg height = {avg_height}, coords = {coords}")
