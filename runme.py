from subfunctions import (
    get_room_coordinates,
    read_floorplan_text,
    find_room_labels,
    count_chars_types_per_room,
)
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--filepath",
    type=str,
    default="apartment_plans/rooms.txt",
    help="Enter the relative path to the apartment plan text file",
)

args = parser.parse_args()


walls = ["|", "-", "+", "/"]
target_letters = ["P", "W", "S", "C"]
pattern = re.compile(r"\(([^)]+)\)")

# Step 1: Load and normalize grid
grid, height, width, lines = read_floorplan_text(args.filepath)

# Step 2: Find room labels
label_positions = find_room_labels(lines, pattern)

# Step 3: Flood-fill to collect all coordinates inside rooms and build a dict
room_coordinates = {}
for label, (x, y) in label_positions.items():
    coords = get_room_coordinates(x, y, grid, width, height, walls)
    room_coordinates[label] = coords

# Step 4: Use tuples to collect chairs information
apartmet_chair_requirements = count_chars_types_per_room(
    grid, room_coordinates, target_letters
)

for room, counts in apartmet_chair_requirements.items():
    print(f"{room}:")
    for key, value in counts.items():
        print(f"  {key}: {value}", end=",")
    print("\n")
