import math
import obj_detection as utils
import ev3
import cv2
import time

# global variables
maxRow = 10	
maxCol = 10
obs = [[0] * maxCol for x in range(maxRow)] # keep track of obstacles
rhs = [[math.inf] * maxCol for x in range(maxRow)]
pred = [[0] * maxCol for x in range(maxRow)] # keep track of whether element is predecessor or not
g = [[math.inf] * maxCol for x in range(maxRow)]
Sstart = []
Sgoal = []
Scurrent = []
openList = [] # holds vertices to be evaluated, s = [rhs, row, columm] for each s in openList
P = [] # current predecessors
tCost = [1, 1.4] # transition cost
SEARCHING = True

ev3_1 = ev3.ev3("10.0.2.5", 5000) #laura (steering)
ev3_2 = ev3.ev3("10.0.2.1", 5001) #cthulu (speed)

def calculate(Scurrent):

	minElem = math.inf
	node = [0,0]
	for i in range(Scurrent[0] - 1, Scurrent[0] + 2):
		for j in range(Scurrent[1] - 1, Scurrent[1] + 2):
			if i < 0 or j < 0 or i >= maxRow or j >= maxCol: # outside of workspace boundary
				continue;
			else:
				if rhs[i][j] < minElem:
					minElem = rhs[i][j]
					# print(minElem)
					node[0] = i
					node[1] = j
	return node

def initialize(target, start):
	global rhs

	for i in range(2):
		Sgoal.append(target[i])
		Sstart.append(start[i])
	rhs[Sgoal[0]][Sgoal[1]] = 0
	openList.append([0, Sgoal[0], Sgoal[1]])
	return

def predCheck(i, j):
	# returns True if element already is a predecessor, else returns False
	if i < 0 or j < 0 or i >= maxRow or j >= maxCol:
		return False
	elif pred[i][j] == 0:
		return True
	else:
		return False

def updateObstacles(coord):
	global obs
	# coord is obstacle, update S
	# set all obstacles to infinity
	m = coord[0] 
	n = coord[1] 
	obs[m][n] = math.inf
	return

def updateVertex(s): 
	global rhs
	global g
	# find and check all predecessors
	findPredecessors(s)
	while len(P) > 0:
		elem = P.pop(0)
		if elem[0] < 0 or elem[1] < 0 or elem[0] >= maxRow or elem[1] >= maxCol or obs[elem[0]][elem[1]] != 0:
			continue
		else:
			if elem[2] == 0: # cost = 1
				rhs[elem[0]][elem[1]] = g[s[1]][s[2]] + tCost[0]
			else:
				rhs[elem[0]][elem[1]] = g[s[1]][s[2]] + tCost[1]
			if g[elem[0]][elem[1]] != rhs[elem[0]][elem[1]]: # if inconsistent, add to openlist
				temp = [rhs[elem[0]][elem[1]], elem[0], elem[1]]
				if temp not in openList: # check if already exists in openList
					openList.append(temp)
	return
def findPredecessors(s):
	# not quite right yet
	# need to figure out way of each node being predecessor to another, yet each node may have multiple successors
	global SEARCHING
	global P
	global pred

	i = s[1]
	j = s[2]
	if i < Sstart[0] and j < Sstart[1]:
		if predCheck(i, j + 1):
			P.append([i, j + 1, 0])
			pred[i][j + 1] = 1
		if predCheck(i + 1, j):
			P.append([i + 1, j, 0])
			pred[i + 1][j] = 1
		if predCheck(i + 1, j + 1):
			P.append([i + 1, j + 1, 1])
			pred[i + 1][j + 1] = 1
	elif i > Sstart[0] and j > Sstart[1]:
		if predCheck(i, j - 1):
			P.append([i, j - 1, 0])
			pred[i][j - 1] = 1
		if predCheck(i - 1, j):
			P.append([i - 1, j, 0])
			pred[i - 1][j] = 1
		if predCheck(i - 1, j - 1):
			P.append([i - 1, j - 1, 1])
			pred[i - 1][j - 1] = 1
	elif i < Sstart[0] and j > Sstart[1]:
		if predCheck(i, j - 1):
			P.append([i, j - 1, 0])
			pred[i][j - 1] = 1
		if predCheck(i + 1, j):	
			P.append([i + 1, j, 0])
			pred[i + 1][j] = 1
		if predCheck(i + 1, j - 1):
			P.append([i + 1, j - 1, 1])
			pred[i + 1][j - 1] = 1
	elif i > Sstart[0] and j < Sstart[1]:
		if predCheck(i, j + 1):
			P.append([i, j + 1, 0])
			pred[i][j + 1] = 1
		if predCheck(i - 1, j):
			P.append([i - 1, j, 0])
			pred[i - 1][j] = 1
		if predCheck(i - 1, j + 1):
			P.append([i - 1, j + 1, 1])
			pred[i - 1][j + 1] = 1
	elif i < Sstart[0] and j == Sstart[1]:
		if predCheck(i + 1, j - 1):
			P.append([i + 1, j - 1, 1])
			pred[i + 1][j - 1] = 1
		if predCheck(i + 1, j):
			P.append([i + 1, j, 0])
			pred[i + 1][j] = 1
		if predCheck(i + 1, j + 1):
			P.append([i + 1, j + 1, 1])
			pred[i + 1][j + 1] = 1
	elif i > Sstart[0] and j == Sstart[1]:
		if predCheck(i - 1, j - 1):
			P.append([i - 1, j - 1, 1])
			pred[i - 1][j - 1] = 1
		if predCheck(i - 1, j):
			P.append([i - 1, j, 0])
			pred[i - 1][j] = 1
		if predCheck(i - 1, j + 1):
			P.append([i - 1, j + 1, 1])
			pred[i - 1][j + 1] = 1
	elif i == Sstart[0] and j > Sstart[1]:
		if predCheck(i, j - 1):
			P.append([i, j - 1, 0])
			pred[i][j - 1] = 1
		if predCheck(i + 1, j - 1):
			P.append([i + 1, j - 1, 1])
			pred[i + 1][j - 1] = 1
		if predCheck(i - 1, j - 1):
			P.append([i - 1, j - 1, 1])
			pred[i - 1][j - 1] = 1
	elif i == Sstart[0] and j < Sstart[1]:
		if predCheck(i, j + 1):
			P.append([i, j + 1, 0])
			pred[i][j + 1] = 1
		if predCheck(i - 1, j + 1):
			P.append([i - 1, j + 1, 1])
			pred[i - 1][j + 1] = 1
		if predCheck(i + 1, j + 1):
			P.append([i + 1, j + 1, 1])
			pred[i + 1][j + 1] = 1
	else:
		print("found starting point")
		P.append([i, j, 1])
		pred[i][j] = 1
		SEARCHING = False
	return
def shortestPath(obstacles):
	global g
	global Sgoal
	global SEARCHING

	for obstacle in obstacles:
		updateObstacles(obstacle)
	openList.sort()
	if len(openList) == 0:
		SEARCHING = False
		return
	s = openList.pop(0)  # pop min item on stack
	if g[s[1]][s[2]] != rhs[s[1]][s[2]]:
		g[s[1]][s[2]] = rhs[s[1]][s[2]]
	updateVertex(s)
	return 


def find_path():
	global Sstart

	path = []
	print("Grabbing target and obstacle coordinates...\n")

	objects, frame = utils.detector() #returns list of objects, first is robot, second is target, the rest is values
	print(objects)
	start = objects[0]
	target = objects[1]
	obstacles = objects[2:]
	initialize(target, start)
	shortestPath(obstacles)
	while SEARCHING is True:
		if g[Sstart[0]][Sstart[1]] == rhs[Sstart[0]][Sstart[1]] and rhs[Sstart[0]][Sstart[1]] < openList[0][0]: # conditions satisfied, optimal path found
			break
		else:
			shortestPath(obstacles)
		
	Scurrent = Sstart
	while Sgoal != Scurrent:
		node = calculate(Scurrent)
		path.append(node)
		Scurrent = node
	# Now move motors to values along path (or skip every second value or some shit for larger subgoals)
	#print(path)
	# print(obs)
	# print(g)
	# print(openList)
	#print(rhs)
	print("Start: " + str(Sstart))
	print("Goal: " + str(Sgoal))
	return Sstart, path, frame


def main():
	ev3_1.connect() #LAURA (STEERING)
	ev3_2.connect() #CTHULU (SPEED)
	

	start, path, frame = find_path()
	print(path)
	position = start

	for point in path:
		direction = [position[0]-point[0], position[1]-point[1]]
		cases(direction)
		position = point
	ev3_1.disconnect()
	ev3_2.disconnect()
	print("Done")
	return 

def cases(direction):

	

	if (direction==[0,1]):
		#Straight forward
		ev3_2.forward(700) #straight (1150) diagonal (1650)
		time.sleep(5)
	elif (direction==[-1,0]):
		#Go right
		ev3_1.turnRight()
		time.sleep(1)
		ev3_2.forward(700)
		time.sleep(5)
		ev3_1.turnLeft()
		time.sleep(1)
	elif (direction==[1,0]):
		#Go left
		ev3_1.turnLeft()
		time.sleep(1)
		ev3_2.forward(700)
		time.sleep(5)
		ev3_1.turnRight()
		time.sleep(1)
	elif (direction == [-1,1]):
		#Go diag right
		ev3_1.turnRightDiag()
		time.sleep(1)
		ev3_2.forward(1000)
		time.sleep(6)
		ev3_1.turnLeftDiag()
		time.sleep(1)
	elif (direction == [1,1]):
		#Go diag left
		ev3_1.turnLeftDiag()
		time.sleep(1)
		ev3_2.forward(1000)
		time.sleep(6)
		ev3_1.turnRightDiag()
		time.sleep(1)
	else:
		print("Your Trash there is an error")
		print(direction)

if __name__ == '__main__':
	main()
