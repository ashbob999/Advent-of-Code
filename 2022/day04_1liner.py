
d = [[list(map(int, r.split("-"))) for r in v.split(",")] for v in open("input/day04.txt").read().strip().split("\n")]

p1 = sum(1 for p in d 
	if (p[0][0]>=p[1][0] and p[0][1]<=p[1][1]) 
	or (p[1][0]>=p[0][0] and p[1][1]<=p[0][1]))
print(p1)

p2 = sum(1 for p1, p2 in d 
		if (p1[0]>=p2[0] and p1[0]<=p2[1])
		or (p1[1] >=p2[0] and p1[1] <=p2[1])
		or (p2[0] >=p1[0] and p2[0] <=p1[1])
		or (p2[1] >=p1[0] and p2[1] <=p1[1]))
print(p2)
