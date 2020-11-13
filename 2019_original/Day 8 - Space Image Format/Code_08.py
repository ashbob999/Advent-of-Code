from PIL import Image

from aoc import input_handler

lines = input_handler.get_input(8)

pixels = list(map(int, list(lines[0])))


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


w = 25
h = 6
length = len(pixels)
print(length)

# part 1

# rows = chunks(pixels, length//6)
layers = chunks(pixels, w * h)
print(len(layers))

layer_num = -1
fewest_zeros = 100000000

for i, layer in enumerate(layers):
    zero_count = 0
    for num in layer:
        if num == 0:
            zero_count += 1

    if zero_count < fewest_zeros:
        fewest_zeros = zero_count
        layer_num = i

print(layer_num)
print(fewest_zeros)
num_1_mult_2 = layers[layer_num].count(1) * layers[layer_num].count(2)

print("Part 1: ", num_1_mult_2)

# part 2

final_layer = [0] * (w * h)

for i in range(len(final_layer)):
    for layer in layers:
        if layer[i] != 2:
            final_layer[i] = layer[i]
            break

print("Part 2:")

for r in chunks(final_layer, w):
    print("".join(str(e) for e in r).replace("0", " ").replace("1", "\u2588"))

img = Image.new("RGB", (w, h))

pixels = img.load()

for i, v1 in enumerate(chunks(final_layer, w)):
    for j, v2 in enumerate(v1):
        if v2 == 0:
            pixels[j, i] = (0, 0, 0)
        else:
            pixels[j, i] = (255, 255, 255)

img.save("image.png")
