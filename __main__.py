import sys
import json

from search.util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()

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


def search(Board):
	movelist=[]
	chunknum=0
	chunks=[]
	#Scaning the dictionary to find out number of chunks in the game

	#chunnks are in list of lists of stacks
	#Finding connection points

	#Finding ways to allocate all pieces to the connection points

	#print out move list by print move and print boom
	





