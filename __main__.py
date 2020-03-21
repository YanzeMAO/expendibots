import sys
import json,math
NEGINF=-10000
from search.util import print_move, print_boom, print_board

def is_close(p,i):
    if math.fabs(p[1]-i[1])<=1 and math.fabs(p[2]-i[2])<=1:
        return True
    return False

def find_boom_dict(chunks):
    boom_dict={}
    #find boom value for board
    for i in range(8):
        for j in range(8):
            boom_dict[(i,j)]=0

    for i in range(8):
        for j in range(8):

            point=(0,i,j)
            for c in chunks:
                for p in c:
                    if is_close(p, point):
                        boom_dict[(i,j)]+=1
                        break
                for p in c:
                    if i == p[1] and j == p[2]:
                        boom_dict[(i, j)] = NEGINF


    print_board(boom_dict)
    return boom_dict

def maxpoint(boom_dict):
    #find max value point
    inverse = [value for key, value in boom_dict.items()]
    maxvalue=max(inverse)
    for i in range(8):
        for j in range(8):
            if maxvalue==boom_dict[(i,j)]:
                return (i,j)

def explode(chunks, point):
    newchunks=[]
    ppoint=(0,point[0],point[1])
    print(point)
    remove=[]
    for i in range(len(chunks)):
        for piece in chunks[i]:
            if is_close(ppoint, piece):
                remove.append(i)

    for j in range(len(chunks)):
        if j not in remove:
            newchunks.append(chunks[j])

    print(newchunks)
    return newchunks
def find_boom_points(position, whitenum, fail):
    boom_points=[]
    chunks = []
    newchunk=[]
    newchunk.append(position[0])

    chunks.append(newchunk)
    position.pop(0)

    # Scaning the dictionary to find out number of chunks in the game
    for i in position:
        #create new chunk
        newchunk = []
        newchunk.append(i)
        found=False
        for c in chunks:
            if found:
                break
            for p in c:
                if is_close(p,i):
                    c.extend(newchunk)
                    found=True
                    break
        if not found:
            chunks.append(newchunk)

    find=0
    while find<whitenum:
        boom_dict=find_boom_dict(chunks)
        max_point=maxpoint(boom_dict)
        boom_points.append(max_point)
        #explode all chunks required
        chunks=explode(chunks, max_point)

        find+=1

    #
    return boom_points

def safezone(chunk, boompoint):
    safedict={}
    for i in range(8):
        for j in range(8):
            point=(0,i,j)
            safedict[(i,j)]=True
            if is_close(point,boompoint):
                safedict[(i, j)] = False
            else:
                for p in chunk:
                    if is_close(point, p):
                        safedict[(i, j)] = False
            

    return safedict



def main():
    #with open(sys.argv[1]) as file:
    with open("test-level-4.json") as file:
        data = json.load(file)


    position=data["black"]
    whitepos=data["white"]
    board={}
    fail=[]
    whitenum=len(whitepos)
    for p in position:
        i=p[1]
        j=p[2]
        board[(i,j)]=p[0]
    points=find_boom_points(position, whitenum,fail)
    print(points)
    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()




"""
class Piece:
	def __init__(self, black=True, x, y):
		self.black=black
		self.x=x
		self.y=y
		self.move=[]
		self.stack=1

	def move(x1,y1):
		move.append((x,y))
		self.x=x1
		self.y=y1


class Stack:
	#Assuming all pieces are moved one by one
	#originally in form of [2,5,3]
	def __init__(self, piece):
		self.x=piece.x
		self.y=piece.y
		self.black=piece.black
		self.pieces=[]
		self.pieces.append(piece)
		self.number=1

	def add(piece):
		self.pieces.append(piece)
		self.number+=1

	def move(n, x, y):
		if n >length(pieces):
			return
		for i in range(n):
			pieces[i].move(x,y)
			pieces.pop()

	def explode():


class Board:
	def __init__(self, board_dict):
		self.board=[]
		white_pos=board["white"]
		black_pos=board["black"]
		for i in white_pos:
			board.append(Stack(Piece(False,i[1],i[2])))
		for j in black_pos:
			board.append(Stack(Piece(j[1],j[2])))

"""
def search(Board):
	movelist=[]
	chunknum=0
	chunks=[]
	#Scaning the dictionary to find out number of chunks in the game

	#chunnks are in list of lists of stacks
	#Finding connection points

	#Finding ways to allocate all pieces to the connection points
	#a* algorithms 

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        for k in self.position:
            positionfind=False
            for m in other.position:
                if k==m:
                    positionfind=True
            if not positionfind:
                return False
        return True


def hamming(p1,p2):
    return math.fabs(p1[1]-p2[1])+math.fabs(p1[2]-p2[2])

def h(targets, whites):
    #comput sum of all close points
    total=0
    for t in targets:
        curent = -NEGINF
        for j in whites:
            if hamming(t,j)<curent:
                    curent=hamming(t,j)
        total+=curent
    return total

def samepos(nodelist, thisnode):
    #check if the state has occurred before
    for n in nodelist:
        if n==thisnode:
            return True

    return False

def pathsearch(targetpoints, whites, black_position):
    #If can't find a path, return False
	# Initialize both open and closed list
    opened=[]
    close=[]
    start= Node(None, whites)
    start.g=0
    start.h=h(targetpoints,whites)
    start.f=start.g+start.h

    opened.append(start)
    end= [Node(None, targetpoints)]

    #Loop until you find the end
    while len(opened)>0:

        # Get the current node with the smallest f value
        minf=-NEGINF
        curent=None
        for node in opened:
            if node.f<minf:
                curent=node
                minf=node.f
        # add possible moves to the open list
        for w in curent.position:

            newpoints = curent.position.copy()
            newpoints.remove(w)
            mobility = w[0]
            newx = w[1]
            newy = w[2]
            # check move up
            for m in range(mobility):
                newy = w[2] + (1 + m)
                if newy >= 8:
                    continue

                newposition = (mobility, newx, newy)
                # check if formed a larger stack
                for p in whites:
                    if newposition.equals(p):
                        mobility += p[0]
                newposition = (mobility, newx, newy)
                newpoints.append(newposition)
                if not samepos(opened, newpoints) and not samepos(close, newpoints):
                    newnode = Node(newpoints)
                    opened.append(newnode)
                #found the final points
                elif samepos(end,newpoints):
                    return #movelist
            # check move down
            for m in range(mobility):
                newy = w[2] - (1 + m)
                if newy < 0:
                    continue

                newposition = (mobility, newx, newy)
                # check if formed a larger stack
                for p in whites:
                    if newposition.equals(p):
                        mobility += p[0]
                newposition = (mobility, newx, newy)
                newpoints.append(newposition)
                if not samepos(opened, newpoints) and not samepos(close, newpoints):
                    newnode = Node(newpoints)
                    newnode.parant=curent
                    newnode.h=h(end,newposition)
                    newnode.f=curent.f+1
                    newnode.g=newnode.h+newnode.f

                    opened.append(newnode)
                elif samepos(end,newpoints):
                    return #movelist
            # check move right
            for m in range(mobility):
                newx = w[1] + (1 + m)
                if newx >= 8:
                    continue

                newposition = (mobility, newx, newy)
                # check if formed a larger stack
                for p in whites:
                    if newposition.equals(p):
                        mobility += p[0]
                newposition = (mobility, newx, newy)
                newpoints.append(newposition)
                if not samepos(opened, newpoints) and not samepos(close, newpoints):
                    newnode = Node(newpoints)
                    opened.append(newnode)
                elif samepos(end, newpoints):
                    return  # movelist
            # check move left
            for m in range(mobility):
                newx = w[1] - (1 + m)
                if newx < 0:
                    continue

                newposition = (mobility, newx, newy)
                # check if formed a larger stack
                for p in whites:
                    if newposition.equals(p):
                        mobility += p[0]
                newposition = (mobility, newx, newy)
                newpoints.append(newposition)
                if not samepos(opened, newpoints) and not samepos(close, newpoints):
                    newnode = Node(newpoints)
                    opened.append(newnode)
                elif samepos(end, newpoints):
                    return  # movelist
        # Remove the current Node from the open
        opened.remove(curent)
        #Add the currentNode to the close
        close.append(curent)

	#print out move list by print move and print boom







