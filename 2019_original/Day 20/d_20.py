import heapq
from collections import deque


def main(path):
	with open(path) as infile:
		line = infile.read().split('\n')

	rawmap = list(map(list, line))

	portals = dict()

	# Checks the 4 outer edges, -1 to flag as outer portal
	# Top Edge
	for x in range(len(rawmap[0])):
		mapchar = rawmap[0][x]
		if (mapchar.isalpha()):
			portalName = mapchar + rawmap[1][x]
			portals[(portalName, -1)] = (x, 2)

	# Bottom Edge
	for x in range(len(rawmap[-1])):
		mapchar = rawmap[-1][x]
		if (mapchar.isalpha()):
			portalName = rawmap[-2][x] + mapchar
			portals[(portalName, -1)] = (x, len(rawmap) - 3)

	# Left Edge
	for y in range(len(rawmap)):
		mapchar = rawmap[y][0]
		if (mapchar.isalpha()):
			portalName = mapchar + rawmap[y][1]
			portals[(portalName, -1)] = (2, y)

	# Right Edge
	for y in range(len(rawmap)):
		mapchar = rawmap[y][-1]
		if (mapchar.isalpha()):
			portalName = rawmap[y][-2] + mapchar
			portals[(portalName, -1)] = (len(rawmap[y]) - 3, y)

	# Checks the 4 inner edges, 1 to flag as inner portal

	# Top Edge
	for y in range(2, len(rawmap) - 2):
		foundLetters = False
		for x in range(2, len(rawmap[y]) - 2):
			mapchar = rawmap[y][x]
			if (mapchar.isalpha()):
				portalName = mapchar + rawmap[y + 1][x]
				portals[(portalName, 1)] = (x, y - 1)
			if (mapchar == " "):
				foundLetters = True
		if (foundLetters):
			break
	# Bottom Edge
	for y in range(len(rawmap) - 3, 1, -1):
		foundLetters = False
		for x in range(2, len(rawmap[y]) - 2):
			mapchar = rawmap[y][x]
			if (mapchar.isalpha()):
				portalName = rawmap[y - 1][x] + mapchar
				portals[(portalName, 1)] = (x, y + 1)
			if (mapchar == " "):
				foundLetters = True
		if (foundLetters):
			break

	# Left Edge
	for x in range(2, len(rawmap[0]) - 2):
		foundLetters = False
		for y in range(2, len(rawmap) - 2):
			mapchar = rawmap[y][x]
			if (mapchar.isalpha()):
				portalName = mapchar + rawmap[y][x + 1]
				portals[(portalName, 1)] = (x - 1, y)
				foundLetters = True
			if (mapchar == " "):
				foundLetters = True
		if (foundLetters):
			break

	# Right Edge
	for x in range(len(rawmap[0]) - 3, 1, -1):
		foundLetters = False
		for y in range(2, len(rawmap) - 2):
			mapchar = rawmap[y][x]
			if (mapchar.isalpha()):
				portalName = rawmap[y][x - 1] + mapchar
				portals[(portalName, 1)] = (x + 1, y)
				foundLetters = True
			if (mapchar == " "):
				foundLetters = True
		if (foundLetters):
			break

	# Reflags AA/ZZ as 0, then creates a reverse mapping
	portals[("AA", 0)] = portals[("AA", -1)]
	portals[("ZZ", 0)] = portals[("ZZ", -1)]
	portals.pop(("AA", -1))
	portals.pop(("ZZ", -1))

	coordToPortal = dict()
	for portalTuple in portals:
		coordToPortal[portals[portalTuple]] = portalTuple

	# Gets the distance from portal to portal (after going through the second portal if not AA/ZZ)
	dist = dict()
	visited = [[-1 for _ in enumerate(rawmap[y])] for (y, _) in enumerate(rawmap)]
	toExplore = deque([])
	dx = (0, 1, 0, -1)
	dy = (-1, 0, 1, 0)

	# Iterates over both inner and outer portals
	for (idx, portalTuple) in enumerate(portals):
		startPos = portals[portalTuple]
		toExplore.append((startPos, 0))
		visited[startPos[1]][startPos[0]] = idx

		dist[portalTuple] = dict()

		while (len(toExplore) != 0):
			(curX, curY), curDist = toExplore.popleft()
			if ((curX, curY) in coordToPortal and (curX, curY) != startPos):
				currentPortal = coordToPortal[(curX, curY)]
				if (currentPortal == ('ZZ', 0) or currentPortal == ('AA', 0)):
					dist[portalTuple][currentPortal] = curDist
				else:
					nextPortal = (currentPortal[0], currentPortal[1] * -1)
					dist[portalTuple][nextPortal] = curDist + 1
			for i in range(4):
				newX = curX + dx[i]
				newY = curY + dy[i]
				if (rawmap[newY][newX] == '.'):
					if (visited[newY][newX] != idx):
						visited[newY][newX] = idx
						toExplore.append(((newX, newY), curDist + 1))

	# ----------------PART 1--------------------#
	# Does dijkstra without considering the levels
	pq = []
	distance1 = dict()

	def isSmaller1(portalTuple, distance):
		if (portalTuple not in distance1):
			return True
		else:
			return distance1[portalTuple] < distance

	heapq.heappush(pq, (0, ("AA", 0)))
	while (len(pq) != 0):
		(distance, portalTuple) = heapq.heappop(pq)
		if (portalTuple == ("ZZ", 0)):
			print(distance)
			break
		else:
			for nextPortalTuple in dist[portalTuple]:
				nextPortal, _ = nextPortalTuple
				newDist = distance + dist[portalTuple][nextPortalTuple]
				if (isSmaller1(nextPortalTuple, newDist)):
					heapq.heappush(pq, (newDist, nextPortalTuple))
					distance1[nextPortalTuple] = newDist

	# ----------------PART 2---------------------#

	pq = []
	distance2 = dict()

	def isSmaller2(portalTuple, level, distance):
		if ((portalTuple, level) not in distance2):
			return True
		else:
			return distance2[(portalTuple, level)] < distance

	heapq.heappush(pq, (0, ("AA", 0), 0))
	while (len(pq) != 0):
		(distance, portalTuple, level) = heapq.heappop(pq)
		if (portalTuple == ("ZZ", 0) and level == 0):
			print(distance)
			break
		else:
			for nextPortalTuple in dist[portalTuple]:
				nextPortal, dLevel = nextPortalTuple
				# End up at opposite portal, so -dLevel instead
				newLevel = level - dLevel
				newDist = distance + dist[portalTuple][nextPortalTuple]
				if (newLevel < 0 or (nextPortal == "ZZ" and newLevel != 0) or (nextPortal == "AA")):
					# Illegal moves
					continue
				if (isSmaller2(nextPortalTuple, newLevel, newDist)):
					heapq.heappush(pq, (newDist, nextPortalTuple, newLevel))
					distance2[(nextPortalTuple, newLevel)] = newDist


main("Data_20.txt")
