from collections import deque


def sort_tuples(coords):
    return sorted(coords, key=lambda t: (t[0], t[1]))


def get_room_coordinates(x, y, grid, width, height, walls):
    visited = set()
    coords = []

    # initial point of flood flow
    q = deque([(x, y)])

    while q:  # iterate until all possible points are explored
        cx, cy = q.popleft()
        if (cx, cy) in visited:  # Don't revisit already ecaluated points
            continue
        if not (0 <= cx < width and 0 <= cy < height):  # Don't go outof bounds
            continue
        char = grid[cy][cx]
        if char in walls:  # Do not add wall characters to room coordinates
            continue
        # add evaluated points to visited for optimization
        visited.add((cx, cy))
        coords.append(
            (cx, cy)
        )  # itertively collect coordinates for all points in the room

        # Explore in 4 directions left, right, top, bottom
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            q.append((cx + dx, cy + dy))

    return sort_tuples(coords)  # return sorted coordinates


def find_room_labels(lines, pattern):
    label_positions = {}
    # finding the positions of room names
    for y, line in enumerate(lines):
        for match in pattern.finditer(line):
            label = match.group(1).strip().lower()
            x = match.start()
            label_positions[label] = (x, y)  # every position of '('
    return label_positions


def read_floorplan_text(file):
    with open(file, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    # computing height for later use
    height = len(lines)
    # computing width of the plan for later use
    width = max(len(line) for line in lines)
    # saving all characters of the plan in 2d list of lists for easier access
    grid = [list(line.ljust(width)) for line in lines]

    return grid, height, width, lines


def count_chars_types_per_room(grid, room_coordinates, target_letters):
    total_count = {item: 0 for item in target_letters}
    appartmet_chair_requirements = {}
    for room, coords in room_coordinates.items():
        counts = {letter: 0 for letter in target_letters}
        char_array = []
        # parse contents of the room using coordinates
        for entry in coords:
            char_array.append(grid[entry[1]][entry[0]])

        counts = {letter: 0 for letter in target_letters}

        # Loop through the list and count specific letters
        for c in char_array:
            if c in target_letters:
                counts[c] += 1
        appartmet_chair_requirements[room] = counts
    # count toal no of chairs of each type required
    for sub_dict in appartmet_chair_requirements.values():
        for key in total_count:
            total_count[key] += sub_dict.get(key, 0)
    appartmet_chair_requirements["total"] = total_count
    # sort room names alphabetically
    appartmet_chair_requirements = {
        key: appartmet_chair_requirements[key]
        for key in sorted(appartmet_chair_requirements)
    }
    return appartmet_chair_requirements
