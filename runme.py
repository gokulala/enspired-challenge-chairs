from subfunctions import *
import argparse

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

# Step 1: Load and normalize grid
height, width, lines = read_floorplan_text(args.filepath)
grid = [list(line.ljust(width)) for line in lines]

# Step 2: Find room labels
pattern = re.compile(r"\(([^)]+)\)")
label_positions = find_room_labels(lines, pattern)

# Step 3: Flood-fill to collect all coordinates inside each room and build a dict
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
