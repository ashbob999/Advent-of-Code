import heapq
from collections import deque


def main(path):
	with open(path) as infile:
		lines = infile.read().split('\n')  # get input file

	grid = list(map(list, lines))  # converts input to a 2d array

	doors = dict()
	keys = dict()
	start = None

	# finds the keys, doors and player
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			char = grid[y][x]
			if (char.isalpha()):
				if (char.isupper()):
					doors[char] = (x, y)
				else:
					keys[char] = (x, y)
			elif (char == '@'):
				start = (x, y)

	keyNames = sorted(keys.keys())  # gets the sorted key names
	keyIntDict = dict()

	for i in range(len(keyNames)):  # makes the key numa binary number, with 1 bit set
		keyIntDict[keyNames[i]] = 1 << i;

	nodes = ['@', *doors.keys(), *keys.keys()]  # creates nodes of player, keys, doors
	nodesLoc = dict()
	nodesLoc['@'] = start  # stores the located nodes
	for key in keys:
		nodesLoc[key] = keys[key]  # adds the keys
	for door in doors:
		nodesLoc[door] = doors[door]  # adds the doors

	nodeDist = dict()
	for node in nodes:
		nodeDist[node] = dict()

	# make all locations not visited
	visited = [[False for x in range(len(grid[y]))] for y in range(len(grid))]
	toExplore = deque();  # create a queue of locations to explore

	dy = [-1, 0, 1, 0]
	dx = [0, 1, 0, -1]

	def inRange(x, y):  # is position inside the grid
		return x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid)

	# bfs through the maze
	for node in nodes:
		visited = [[False for x in range(len(grid[y]))] for y in range(len(grid))]

		startPos = nodesLoc[node]
		toExplore.append((startPos, 0))
		visited[startPos[1]][startPos[0]] = True
		while (len(toExplore) != 0):
			curPos, curDis = toExplore.popleft()
			curX, curY = curPos
			gridChar = grid[curY][curX]
			if (gridChar in nodes and gridChar != node):
				nodeDist[node][gridChar] = curDis
			else:
				for i in range(4):
					newX = curX + dx[i]
					newY = curY + dy[i]
					if (grid[newY][newX] != '#'):
						if (not visited[newY][newX]):
							visited[newY][newX] = True
							toExplore.append(((newX, newY), curDis + 1))

	for n in nodeDist.keys():
		print(n, nodeDist[n])

	bfDist = dict()
	for node in nodes:
		bfDist[node] = dict()

	pq = [(0, 0, '@')]
	heapq.heapify(pq)
	bfDist['@'][0] = 0

	# compares the given dist
	# and dist from bfs
	def isSmaller(newDist, node, intKeyMap):  # returns if a new path is shorter
		if (intKeyMap not in bfDist[node]):
			return True
		else:
			return newDist < bfDist[node][intKeyMap]

	fullKeys = (1 << len(keys)) - 1  # binary number of 26 1's

	# gets the shortest path, that visits them all
	while (len(pq) != 0):
		curDist, curKeyMap, curNode = heapq.heappop(pq)
		if (curKeyMap == fullKeys):
			print(curDist)
			break
		else:
			for nextNode in nodeDist[curNode]:
				newDist = curDist + nodeDist[curNode][nextNode]
				nextKeyMap = curKeyMap
				if (nextNode.isupper()):  # if the nextNode is a door
					if (keyIntDict[nextNode.lower()] & nextKeyMap == 0):
						# No key
						continue
				elif (nextNode.islower()):  # if the nextnode is a key
					print(nextNode)
					# Add key
					nextKeyMap |= keyIntDict[nextNode]
				if (isSmaller(newDist, nextNode, nextKeyMap)):
					bfDist[nextNode][nextKeyMap] = newDist  # set new shortest dist
					heapq.heappush(pq, (newDist, nextKeyMap, nextNode))


main("Data_18.txt")
# 6162
