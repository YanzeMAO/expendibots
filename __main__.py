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



    return boom_dict


def wall(blackpos):
    #return the points that require to below up the wall
    #check horizontal wall left to right
    recentvertical = {0, 1, 2, 3, 4, 5, 6, 7}
    for i in range(8):
        for p in blackpos:
            newvertical={}
            if p[1]==i and p[2] in recentvertical:
                newvertical.append(p[2])
                if p[2]==0:
                    #hit bottom wall
                    return p
                elif p[2]==7:
                    #hit top wall
                    return p
                else:
                    newvertical.append(p[2]-1)
                    newvertical.append(p[2]+1)
        recentvertical=newvertical
    #check horizontal wall right to left
    recentvertical = {0, 1, 2, 3, 4, 5, 6, 7}
    for i in range(8,-1):
        for p in blackpos:
            newvertical={}
            if p[1]==i and p[2] in recentvertical:
                newvertical.append(p[2])
                if p[2]==0:
                    #hit bottom wall
                    return p
                elif p[2]==7:
                    #hit top wall
                    return p
                else:
                    newvertical.append(p[2]-1)
                    newvertical.append(p[2]+1)
        recentvertical=newvertical
    return None


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

    remove=[]
    for i in range(len(chunks)):
        for piece in chunks[i]:
            if is_close(ppoint, piece):
                remove.append(i)

    for j in range(len(chunks)):
        if j not in remove:
            newchunks.append(chunks[j])


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
    return boom_points

def safezone(chunk, boompoint):
    safedict={}
    for i in range(8):
        for j in range(8):
            point=(0,i,j)
            safedict[(i,j)]=True
            if is_close(point, boompoint):
                safedict[(i, j)] = False
            else:
                for p in chunk:
                    if is_close(point, p):
                        safedict[(i, j)] = False
            

    return safedict

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
    if len(targets)!=len(whites):
        for i in whites:
            npiece=i[0]
            if npiece>1:
                whites.remove(i)
                for n in range(npiece):
                    newpiece=(1,i[1],i[2])
                    whites.append(newpiece)

    #comput sum of all close points input two list of points
    #1 white
    if len(targets)==1:
        return hamming(targets[0],whites[0])

    #2 whites
    elif len(targets) == 2:
        #case1: 1_>1,2_>2
        current =hamming(targets[0],whites[0])+hamming(targets[1],whites[1])
        #case2: 1_ > 2, 2_ > 1
        new= hamming(targets[0],whites[1])+hamming(targets[1],whites[0])
        if new<current:
            current=new
        return current
    #3 whites
    else:
        #case1
        current =hamming(targets[0],whites[0])+hamming(targets[1],whites[1])+hamming(targets[2],whites[2])
        #case2
        new= hamming(targets[0],whites[0]) + hamming(targets[1],whites[2])+hamming(targets[2],whites[1])
        if new < current:
            current = new
        #case=3
        new =hamming(targets[0],whites[1])+hamming(targets[1],whites[2])+hamming(targets[2],whites[0])
        if new < current:
            current = new
        #case4: 1_ > 2, 2_ > 1
        new= hamming(targets[0],whites[2]) + hamming(targets[1],whites[1])+hamming(targets[2],whites[0])
        if new < current:
            current = new
        #case5: 1_>1,2_>2
        new =hamming(targets[0],whites[1])+hamming(targets[1],whites[0])+hamming(targets[2],whites[2])
        if new < current:
            current = new
        #case6: 1_ > 2, 2_ > 1
        new= hamming(targets[0],whites[2]) + hamming(targets[1],whites[2])+hamming(targets[1],whites[0])
        if new < current:
            current = new
        return current



def samepos(nodelist, thisnode):
    if len(nodelist)==0:
        return False
    #check if the state has occurred before
    for n in nodelist:

        if n==thisnode:
            return True
    return False

def pathsearch(targetpoints, whites, blackposition):

    #If can't find a path, return False
	# Initialize both open and closed list
    opened=[]
    close=[]
    start= Node(None, whites)
    start.g=0
    start.h=h(targetpoints,whites)
    start.f=start.g+start.h
    opened.append(start)
    direction=[(0,1),(1,0),(-1,0),(0,-1)]
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
            print(w)
            print(w)
            for d in direction:
                mobility = w[0]
                for m in range(mobility):
                    print("origin")
                    #check in each step size moving
                    newpoints = curent.position.copy()

                    print(newpoints)
                    newpoints.remove(w)
                    newx = w[1]
                    newy = w[2]
                    newx+=d[0]*(1+m)
                    newy+=d[1]*(1+m)
                    hitblack=False
                    #check if the position has been occupied by the black
                    for b in blackposition:
                        if newx==b[1] and newy==b[2]:
                            hitblack=True
                    if newy < 0 or newy >7 or newx<0 or newx>7 or hitblack:
                            continue
                    # check if formed a larger stack
                    newstack=0
                    newmobility =m+1
                    for p in newpoints:
                        if p[1]==newx and p[2]==newy:
                            #merge the stacks to new stack
                            newmobility = p[0]+m+1
                            newpoints.remove(p)

                    print("new point")
                    newposition = (newmobility, newx, newy)
                    print(newposition)
                    #check old position
                    if mobility - (m+1)> 0:
                        oldposition = (mobility - (m+1), w[1], w[2])
                        newpoints.append(oldposition)
                        print("old point")
                        print(oldposition)


                    newpoints.append(newposition)



                    #append in open if the state has not occur before
                    newnode = Node(curent,newpoints)
                    newnode.parent=curent
                    newnode.h=h(targetpoints.copy(),newpoints.copy())
                    newnode.f=curent.f+0.04
                    newnode.g=newnode.h+newnode.f
                    print(newpoints)
                    if not samepos(opened, newnode) and not samepos(close, newnode):
                        opened.append(newnode)
                    #find the route if the new node is the destination
                    elif targetpoints==newpoints:
                        return newnode

        # Remove the current Node from the open
        opened.remove(curent)
        #Add the currentNode to the close
        close.append(curent)


	#print out move list by print move and print boom

    return None

def printaction(endnode):
    action=[]
    n=0
    curent = endnode
    previous= endnode.parent
    curentpos = curent.position
    for i in curentpos:
        x=i[1]
        y=i[2]
        print_boom(x, y)

    while previous is not None:

        curentpos=curent.position
        previouspos=previous.position
        for i in curentpos:
            if i not in previouspos:
                x_b=i[1]
                y_b=i[2]
                n=i[0]
        for j in previouspos:
            if j not in curentpos:
                x_a=j[1]
                y_a=j[2]
        print_move(n, x_a, y_a, x_b, y_b)
        curent=previous
        previous=previous.parent




def main():
    #with open(sys.argv[1]) as file:
    with open("test-level-4.json") as file:
        data = json.load(file)


    position=data["black"]
    blackposition=position.copy()
    whitepos=data["white"]
    board={}
    fail=[]
    whitenum=len(whitepos)
    for p in position:
        i=p[1]
        j=p[2]
        board[(i,j)]=p[0]

    points=find_boom_points(position, whitenum,fail)

    targetpoints=[]
    for p in points:
        P=(1,p[0],p[1])
        targetpoints.append(P)
    white=[]
    for y in whitepos:
        white.append(tuple(y))

    node=pathsearch(targetpoints, white, blackposition)
    printaction(node)
    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()







