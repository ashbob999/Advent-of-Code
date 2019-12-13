from util import input_handler
from util.intcode_machine import IntCodeVM

lines = input_handler.get_input(13)

instr = list(map(int, lines[0].split(",")))


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def pad_list(arr, amount):
    for i in range(amount):
        arr.append(0)


# part 1

pad_list(instr, len(instr))

vm = IntCodeVM(instr, [])

vm.run()

output = vm.program_outputs

tile_data = chunks(output, 3)

tiles = {(t[0], t[1]): t[2] for t in tile_data}

# 0: empty
# 1: wall
# 2: block
# 3: horizontal paddle
# 4: ball

block_tile_count = 0

for tile, type in tiles.items():
    if type == 2:
        block_tile_count += 1

print("Part 1: ", block_tile_count)

# part 2

instr[0] = 2

vm = IntCodeVM(instr, [0])
vm.run()

while not vm.finished:
    tile_data = chunks(vm.program_outputs, 3)

    tiles = {(t[0], t[1]): t[2] for t in tile_data}

    ball_pos = None
    paddle_pos = None
    block_count = 0

    for pos, type in tiles.items():
        if type == 3:
            paddle_pos = pos

        if type == 4:
            ball_pos = pos

        if type == 2:
            block_count += 1

    # print("ball: ", ball_pos, "  paddle: ", paddle_pos)
    # print("block count: ", block_count)

    if block_count == 0:
        vm.finished = True
        print("no blocks left")
        break

    joystick_move = 0

    if ball_pos[0] < paddle_pos[0]:
        joystick_move = -1
    else:
        joystick_move = 1

    vm.add_input(joystick_move)

tile_data = chunks(vm.program_outputs, 3)

tiles = {(t[0], t[1]): t[2] for t in tile_data}

score = 0

for pos, type in tiles.items():
    if pos == (-1, 0):
        score = type

print("Part 2: ", score)
