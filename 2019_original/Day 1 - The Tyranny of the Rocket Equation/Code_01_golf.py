f = open("../resources/Day_01_Inputs.txt")
c = lambda m: int(m) // 3 - 2
print(sum(c(l) for l in f))
p = lambda m: p(c(m)) + c(m) if m > 6 else 0
f.seek(0)
print(sum(p(int(l)) for l in f))
