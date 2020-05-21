import pygame, sys
from pygame.locals import *
from ScrabbleClasses import *
#from PodSixNet.Connection import ConnectionListener, connection
#from time import sleep

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
double_word_coord = [16,28,32,42,48,56,64,70,80,84,154,160,168,176,182,192,196,208]
triple_letter_coord = [20,24,76,80,84,88,136,140,144,148,200,204]
double_letter_coord = [3,11,36,38,45,52,59,92,96,98,102,108,116,122,126,128,132,165,172,179,186,188,213,221]


class ScrabbleGame():

    def __init__(self):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((880,640))
        self.DISPLAY.blit(BACKGROUND,(0,0))
        self.DISPLAY.blit(PLAY,(785,560))
        self.word_coord = []
        self.tiles_coord = []
        self.score = 0
        self.tiles_on_board = []
        self.set_board()
        self.rack = Rack()
        self.draw_rack()

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

    def draw_board(self):
        row = 0
        column = 0
        for i in range(225):
            if row == 15:
                column+=1
                row=0
            self.DISPLAY.blit(self.board[i].img, (row * 40, column * 40))
            row+=1
        for i in range(0,225):
            if self.board[i].tile != None:
                self.DISPLAY.blit(self.board[i].tile.img, (i%15 * 40, i//15 * 40))
        pygame.display.update()

    def draw_rack(self):
        row = 15
        column = 4
        inc=0
        #-----------------------------------------------------------------------------------------------
        #print([i.get_letter for i in rac])
        for i in range(7):
            self.DISPLAY.blit(YEL_SQR, (column * 40, row * 40))
            if self.rack.racktiles[i] != None:
                self.DISPLAY.blit(self.rack.racktiles[i].img, (column * 40, row * 40))
            column +=1
        pygame.display.update()




    def scrabble_game(self):
        while True:
            self.DISPLAY.blit(BACKGROUND,(0,0))
            self.DISPLAY.blit(PLAY,(785,560))
            self.draw_board()
            self.draw_rack()
            font = pygame.font.Font(None, 25)
            text = font.render("Score: "+ str(self.score), 1, (0,0,1))
            self.DISPLAY.blit(text,(610,10))
            #pygame.event.get()
            pygame.display.update()
            item_pos = int(self.choose_tile())
            #print(item_pos)
            row = (item_pos) //15
            column = (item_pos) % 15
            if row == 15 and column <= 10 and column >= 4:
                if self.rack.racktiles[item_pos-229] != None:
                    self.DISPLAY.blit(PINK_SQR,((column)*40, (row)*40))
                    pygame.display.update()
                    self.move_tile(item_pos-229,row,column)

    def move_tile(self,start_pos,row,column):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    new_pos = int(self.choose_tile())
                    if new_pos <= 224:
                        self.word_coord.append(new_pos)
                        self.tiles_coord.append(start_pos)
                        if self.board[new_pos].tile == None:
                            self.board[new_pos].add_tile(self.rack.racktiles[start_pos].tile_letter, new_pos)
                            self.rack.racktiles[start_pos] = None
                            return True
                        else:
                            return False
                    else:
                        return #scrabble_game()


    def choose_tile(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_game()
                if event.type == MOUSEBUTTONDOWN:
                    column = event.pos[0] // 40
                    row = event.pos[1] // 40
                    if event.pos[0] >= 705 and event.pos[0] <= 880 and event.pos[1] >= 560 and event.pos[1] <= 640:
                        self.score_valid_word()
                    #print(column,row)
                    return (column) + ((row*15))


    def score_valid_word(self):
        word = ""
        self.get_all_coord()

        is_in=False
        for i in self.word_coord:
            if i in self.tiles_on_board or i == 112:
                is_in=True
            if i <= 225:
                if self.board[i].tile != None:
                    word=word+ ''.join(self.board[i].tile.tile_letter)
                elif self.board[i].tile == None:
                    print("missing_letter")
                    self.not_valid_word()
        print(is_in)
        word = Word(word)
        if is_in == False:
            print("word is invalid")
            word=""
            self.not_valid_word()
        if word != "" and word.valid():
            #print(word_coord)
            self.score += word.getScoreWord(self.word_coord)
            print(self.score)
            for i in self.word_coord:
                if i not in self.tiles_on_board:
                    self.tiles_on_board.append(i)
            self.word_coord=[]
            self.tiles_coord=[]
            #change_player()
            self.rack.refill()
            self.draw_rack()
            print("valid word working")
        else:
            print("not valid last loop")
            self.not_valid_word()



    def not_valid_word(self):
        i=0
        print(self.tiles_coord,self.word_coord, "         your word is invalid")

        if len(self.tiles_coord) == 0:
            return
        while i < len(self.tiles_coord):
            for j in self.word_coord:
                if j not in self.tiles_on_board:
                    self.rack.replace_tile(self.tiles_coord[i], self.board[j].tile.tile_letter, self.tiles_coord[i])
                    self.board[j].remove_tile()
                    i+=1

        self.word_coord=[]
        self.tiles_coord=[]


    def get_all_coord(self):
        ins = self.word_coord[:]
        for i in self.tiles_on_board:
            for j in self.word_coord:
                if j+1 == i:
                    ins.insert(self.word_coord.index(j)+1, i)
                if j == self.word_coord[0] and j-1 == i:
                    ins.insert(self.word_coord.index(j), i)
                if j+15 == i:
                    ins.insert(self.word_coord.index(j)+1, i)
                if j == self.word_coord[0] and j-15 == i:
                    ins.insert(self.word_coord.index(j), i)
        self.word_coord = list(ins)



def main():
    game_instance = ScrabbleGame()
    while(True):
        game_instance.scrabble_game()

def quit_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()



#cd Desktop\Implementation\updated\
