from PIL import Image, ImageOps

from util import input_handler
from util.intcode_machine import IntCodeVM

lines = input_handler.get_input(11)

instr = list(map(int, lines[0].split(",")))


def pad_list(arr, amount):
    for i in range(amount):
        arr.append(0)


# part 1
# print(instr)
pad_list(instr, len(instr) * 2)
inp = 1
vm = IntCodeVM(instr, [inp])

robot_pos = [0, 0]
visited = {}
# black = 0
# white = 1

dirs = ["up", "right", "down", "left"]
dir = "up"

vm.run()
while not vm.finished:
    outputs = vm.program_outputs[-2:]
    # if tuple(robot_pos) in visited:
    visited[tuple(robot_pos)] = outputs[0]

    if outputs[1] == 0:  # turn left
        dir_index = dirs.index(dir) - 1
        if dir_index < 0:
            dir_index = len(dirs) - 1
    else:  # turn right
        dir_index = dirs.index(dir) + 1
        if dir_index >= len(dirs):
            dir_index = 0

    dir = dirs[dir_index]

    if dir == "up":
        robot_pos = [robot_pos[0], robot_pos[1] + 1]
    elif dir == "right":
        robot_pos = [robot_pos[0] + 1, robot_pos[1]]
    elif dir == "down":
        robot_pos = [robot_pos[0], robot_pos[1] - 1]
    elif dir == "left":
        robot_pos = [robot_pos[0] - 1, robot_pos[1]]

    if tuple(robot_pos) in visited:
        colour = visited[tuple(robot_pos)]
    else:
        colour = 0

    vm.add_input(colour)

# print(visited)
print("Part 1: ", len(visited))

# part 2

min_x = min(visited, key=lambda x: x[0])[0]
min_y = min(visited, key=lambda x: x[1])[1]

max_x = max(visited, key=lambda x: x[0])[0]
max_y = max(visited, key=lambda x: x[1])[1]

img_width = abs(max_x - min_x)
img_height = abs(max_y - min_y)

print("width: ", img_width, "  height: ", img_height)

img = Image.new("RGB", (img_width + 5, img_height + 5))

pixels_to_add = {}
for k, v in visited.items():
    new_pos = [k[0] + abs(min_x), k[1] + abs(min_y)]
    pixels_to_add[tuple(new_pos)] = v

# print(min(pixels_to_add, key=lambda x: x[0]))

pixels = img.load()

for k, v in pixels_to_add.items():
    if v == 1:
        # print(k)
        pixels[k[0], k[1]] = (255, 255, 255)

img = ImageOps.flip(img)

img.save("image.png")
