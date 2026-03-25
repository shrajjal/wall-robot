from collections import deque


# -------------------------------
# 🔹 CHECK OBSTACLE
# -------------------------------
def is_obstacle(x, y, obstacles):
    for obs in obstacles:
        if (
            obs.x <= x < obs.x + obs.width and
            obs.y <= y < obs.y + obs.height
        ):
            return True
    return False


# -------------------------------
# 🔹 VALID CELL
# -------------------------------
def is_valid(x, y, width, height, obstacles):
    return (
        0 <= x < width and
        0 <= y < height and
        not is_obstacle(x, y, obstacles)
    )


# -------------------------------
# 🔹 BFS → NEAREST UNVISITED CELL
# -------------------------------
def bfs_to_nearest_unvisited(start, width, height, obstacles, visited):
    queue = deque([start])
    seen = set([start])
    parent = {}

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        x, y = queue.popleft()

        # 🔥 found nearest unvisited
        if (x, y) not in visited and not is_obstacle(x, y, obstacles):
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < width and
                0 <= ny < height and
                not is_obstacle(nx, ny, obstacles) and
                (nx, ny) not in seen
            ):
                seen.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return []


# -------------------------------
# 🔥 MAIN FUNCTION (OPTIMIZED CPP)
# -------------------------------
def generate_path(width, height, obstacles):
    path = []
    visited = set()

    # 🔹 find start (first free cell)
    start = None
    for y in range(height):
        for x in range(width):
            if not is_obstacle(x, y, obstacles):
                start = (x, y)
                break
        if start:
            break

    if not start:
        return []

    current = start
    path.append([current[0], current[1]])
    visited.add(current)

    # 🔹 movement priority (tunable)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    # right → down → left → up (good for sweeping)

    while True:
        moved = False

        # -----------------------
        # 🔹 LOCAL GREEDY MOVE
        # -----------------------
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy

            if (
                is_valid(nx, ny, width, height, obstacles)
                and (nx, ny) not in visited
            ):
                current = (nx, ny)
                path.append([nx, ny])
                visited.add((nx, ny))
                moved = True
                break

        if moved:
            continue

        # -----------------------
        # 🔹 GLOBAL RECONNECT (BFS)
        # -----------------------
        route = bfs_to_nearest_unvisited(
            current, width, height, obstacles, visited
        )

        if not route:
            break  # all reachable cells covered

        for px, py in route:
            current = (px, py)
            path.append([px, py])
            visited.add((px, py))

    # -----------------------
    # 🔍 DEBUG CHECK (optional)
    # -----------------------
    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]

        if abs(x1 - x2) + abs(y1 - y2) != 1:
            print("❌ TELEPORT:", (x1, y1), "→", (x2, y2))

    total_steps = len(path)

    unique_cells = len(set((x, y) for x, y in path))

    revisits = total_steps - unique_cells

    print("Total steps:", total_steps)
    print("Unique cells:", unique_cells)
    print("Revisits:", revisits)        
    return path