import pygame, sys
from pygame.locals import *
from ScrabbleClasses import *
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

BACKGROUND = pygame.image.load("Scrabble_Images/background.png")
PLAY = pygame.image.load("Scrabble_Images/play_word.png")
SQR = pygame.image.load("Scrabble_Images/scrabble_square.png")
PINK_SQR = pygame.image.load("Scrabble_Images/pink_square.png")
YEL_SQR = pygame.image.load("Scrabble_Images/yellow_square.png")
STAR = pygame.image.load("Scrabble_Images/scrabble_square_star.png")
TRIPW = pygame.image.load("Scrabble_Images/triple_word.png")
DOUBW = pygame.image.load("Scrabble_Images/double_word.png")
TRIPL = pygame.image.load("Scrabble_Images/triple_letter.png")
DOUBL = pygame.image.load("Scrabble_Images/double_letter.png")

triple_word_coord = [0,7,14,105,119,210,217,224]
double_word_coord = [16,28,32,42,48,56,64,70,80,84,96,98,126,128,140,144,154,160,168,176,182,192,196,208]
triple_letter_coord = [20,24,76,80,84,88,136,140,144,148,200,204]
double_letter_coord = [3,11,36,38,45,52,59,92,96,98,102,108,116,122,126,128,132,165,172,179,186,188,213,221]


class ScrabbleGame(ConnectionListener):

    def __init__(self):
        self.clock=pygame.time.Clock()
        self.word_coord = []
        self.score = 0
        #--------------------------------------------------------------------------------ask why 112?--------
        self.tiles_on_board = [112]
        self.board = None
        self.rack = None
        self.rack_letters = None
        self.tile_selected = False
        self.Connect()
        self.running False

        self.gameID = None
        self.player = None

#--------------------------------------------------------------
        #While the game isn't running pump the server
        while not self.running:
			#Check if the user exited the game
			self.check_exit()

			#Pump the server
			self.Pump()
			connection.Pump()
			sleep(0.01)
        pygame.display.set_caption("Game ID: {} - Player: {}".format(self.gameID, self.player))
#--------------------------------------------------------------




    def check_click(self):

		#Get the keys that are being pressed
		click = pygame.mouse.get_pressed()[0]

		#Check which keys were pressed, update the position and notify the server of the update


        #select a tile or choose where you want to move a selected tile
		if click:
            mouse_pos = pygame.mouse.get_pos()

            if self.tile_selected == True:
                self.Send({"action":"tile_moved","x":mouse_pos[0],"y":mouse_pos[1],"player":self.player,"gameID":self.gameID})
            else:
                self.Send({"action":"tile_pos","x":mouse_pos[0],"y":mouse_pos[1],"player":self.player,"gameID":self.gameID})


    def update(self):

        connection.Pump()
        self.Pump()

        self.check_exit()

        self.clock.tick(60)
        #self.screen.fill(0)
        self.draw_board()
        self.draw_rack()

        self.check_click()

        pygame.display.update()


    def Network_startgame(self, data):
		#Get the game ID and player number from the data
		self.gameID = data['gameID']
		self.player = data['player']
		#Set the game to running so that we enter the update loop
		self.running = True


    # def Network_new_tile_position(self, data):
    #
	# 	#Get the player data from the request
	# 	tile_moved_pos = data['tile_moved']
    #
	# 	#Update the player data
	# 	self.players[p].rect.x = data['x']
	# 	self.players[p].rect.y = data['y']



    def check_exit(self):
		#Check if the user exited
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()



    def set_board(self):
    	self.board = [0] * 225
    	for i in range(225):
    		self.board[i] = Square(SQR)
    		if i == 112:
    			self.board[i] = Square(STAR)
    		if i in triple_word_coord:
    			self.board[i] = Square(TRIPW)
    		if i in double_word_coord:
    			self.board[i] = Square(DOUBW)
    		if i in triple_letter_coord:
    			self.board[i] = Square(TRIPL)
    		if i in double_letter_coord:
    			self.board[i] = Square(DOUBL)
    	self.rack = [0] * 7
    	self.rack_letters = Rack().refill()
    	#print(self.rack_letters)
    	for i in range(7):
    		self.rack[i] = Square(YEL_SQR)

        #--------------------------------------------------------------------------------------------returning 2 objects?----------
    	#self.board = board
        #self.rack = rack
        #return board
    	#return rack

    def draw_board(self):
    	row = 0
    	column = 0
    	for i in range(225):
    		if row == 15:
    			column+=1
    			row=0
    		DISPLAY.blit(self.board[i].img, (row * 40, column * 40))
    		row+=1
    	for i in range(0,225):
    		if self.board[i].tile != None:
    			#	print(self.board[i].tile)
    			DISPLAY.blit(self.board[i].tile.picture, (i%15 * 40, i//15 * 40))
    	pygame.display.update()

    def draw_rack(self):
    	self.rack_letters = Rack().refill()
    	#print(self.rack_letters)
    	row = 15
    	column = 4
    	inc=0
    	for j in self.rack_letters:
    		if Rack().bag.amount() != 0:
    			self.rack[inc].tile = Tiles(str(j))
    			inc+=1
    	for i in range(7):
    		DISPLAY.blit(self.rack[i].img, (column * 40, row * 40))
    		if self.rack[i].tile != None:
    			DISPLAY.blit(self.rack[i].tile.picture, (column * 40, row * 40))
    		column +=1
    	pygame.display.update()
    	return self.rack_letters

    # def scrabble_game(self):
    #
    # 		#pygame.event.get()
    # 		pygame.display.update()
    # 		item_pos = int(self.choose_tile())
    # 		#print(item_pos)
    # 		row = (item_pos) //15
    # 		column = (item_pos) % 15
    # 		if row == 15 and column <= 10 and column >= 4:
    # 			if self.rack[item_pos-229].tile != None:
    # 				DISPLAY.blit(PINK_SQR,((column)*40, (row)*40))
    # 				pygame.display.update()
    # 				self.move_tile(item_pos-229,row,column)


    def check_play(self):
        


    def score_valid_word(self):
    	print(self.word_coord)
    	word = ""
    	is_in=False
    	for i in self.word_coord:
    		if i in self.tiles_on_board:
    			is_in=True
    		word=word+ ''.join(self.board[i].tile.tile_letter)
    	if is_in == False:
    		word =""
    	word = Word(word)
    	if word != "" and word.valid():
    		self.score += self.score + word.getScoreWord(self.word_coord)
    		#change_player()
    	print(word,self.score)

    # def change_player(player_num):
    # 	global word_coord
    # 	if curr_player == player_num:
    # 		word_coord = []
    # 		if curr_player == len(player_list):
    # 			curr_player=1
    # 		else:
    # 			curr_player+=1


    #def player_turn():


class Word:

	def __init__(self,word):
		self.word = word

	def valid(self):
		with open('words_alpha.txt') as word_file:
			valid_words = set(word_file.read().split())
		if self.word.lower() in valid_words:
			return True
		else:
			return False

	def getScoreWord(self,position):
		i = 0
		score = 0
		tw = False
		dw = False
		for tile in self.word:
			x = Tiles(tile.upper())
			if position[i] in triple_word_coord:
				tw = True
				score += x.value
			elif position[i] in double_word_coord:
				dw = True
				score += x.value
			elif position[i] in double_letter_coord:
				score += x.value * 2
			elif position[i] in triple_letter_coord:
				score += x.value * 3
			else:
				score += x.value
			i+=1
		if dw == True:
			return score * 2
		elif tw == True:
			return score * 3
		else:
			return score


class Tiles:

	def __init__(self, tile):
		self.tile_pos = 0
		self.tile_letter = tile
		if self.tile_letter == "A":
			self.picture = pygame.image.load("Scrabble_Images/tiles/A_tile.png")
			self.value = 1
		if self.tile_letter == "B":
			self.picture = pygame.image.load("Scrabble_Images/tiles/B_tile.png")
			self.value = 3
		if self.tile_letter == "C":
			self.picture = pygame.image.load("Scrabble_Images/tiles/C_tile.png")
			self.value = 3
		if self.tile_letter == "D":
			self.picture = pygame.image.load("Scrabble_Images/tiles/D_tile.png")
			self.value = 2
		if self.tile_letter == "E":
			self.picture = pygame.image.load("Scrabble_Images/tiles/E_tile.png")
			self.value = 1
		if self.tile_letter == "F":
			self.picture = pygame.image.load("Scrabble_Images/tiles/F_tile.png")
			self.value = 4
		if self.tile_letter == "G":
			self.picture = pygame.image.load("Scrabble_Images/tiles/G_tile.png")
			self.value = 2
		if self.tile_letter == "H":
			self.picture = pygame.image.load("Scrabble_Images/tiles/H_tile.png")
			self.value = 4
		if self.tile_letter == "I":
			self.picture = pygame.image.load("Scrabble_Images/tiles/I_tile.png")
			self.value = 1
		if self.tile_letter == "J":
			self.picture = pygame.image.load("Scrabble_Images/tiles/J_tile.png")
			self.value = 8
		if self.tile_letter == "K":
			self.picture = pygame.image.load("Scrabble_Images/tiles/K_tile.png")
			self.value = 5
		if self.tile_letter == "L":
			self.picture = pygame.image.load("Scrabble_Images/tiles/L_tile.png")
			self.value = 1
		if self.tile_letter == "M":
			self.picture = pygame.image.load("Scrabble_Images/tiles/M_tile.png")
			self.value = 3
		if self.tile_letter == "N":
			self.picture = pygame.image.load("Scrabble_Images/tiles/N_tile.png")
			self.value = 1
		if self.tile_letter == "O":
			self.picture = pygame.image.load("Scrabble_Images/tiles/O_tile.png")
			self.value = 1
		if self.tile_letter == "P":
			self.picture = pygame.image.load("Scrabble_Images/tiles/P_tile.png")
			self.value = 3
		if self.tile_letter == "Q":
			self.picture = pygame.image.load("Scrabble_Images/tiles/Q_tile.png")
			self.value = 10
		if self.tile_letter == "R":
			self.picture = pygame.image.load("Scrabble_Images/tiles/R_tile.png")
			self.value = 1
		if self.tile_letter == "S":
			self.picture = pygame.image.load("Scrabble_Images/tiles/S_tile.png")
			self.value = 1
		if self.tile_letter == "T":
			self.picture = pygame.image.load("Scrabble_Images/tiles/T_tile.png")
			self.value = 1
		if self.tile_letter == "U":
			self.picture = pygame.image.load("Scrabble_Images/tiles/U_tile.png")
			self.value = 1
		if self.tile_letter == "V":
			self.picture = pygame.image.load("Scrabble_Images/tiles/V_tile.png")
			self.value = 4
		if self.tile_letter == "W":
			self.picture = pygame.image.load("Scrabble_Images/tiles/W_tile.png")
			self.value = 4
		if self.tile_letter == "X":
			self.picture = pygame.image.load("Scrabble_Images/tiles/X_tile.png")
			self.value = 8
		if self.tile_letter == "Y":
			self.picture = pygame.image.load("Scrabble_Images/tiles/Y_tile.png")
			self.value = 4
		if self.tile_letter == "Z":
			self.picture = pygame.image.load("Scrabble_Images/tiles/Z_tile.png")
			self.value = 10
		if self.tile_letter == "_":
			self.picture = pygame.image.load("Scrabble_Images/tiles/blank_tile.png")
			self.value = 0



def main():
	global DISPLAY
	pygame.init()
	DISPLAY = pygame.display.set_mode((880,640))
	DISPLAY.blit(BACKGROUND,(0,0))
	DISPLAY.blit(PLAY,(785,560))
	game_start = ScrabbleGame()
	game_start.set_board()

	while(True):
		game_start.update()

def quit_game():
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()
