import pygame
import random
from ScrabbleGame import *


class Square:

    def __init__(self,img):
        self.img = img
        self.tile = None

    def add_tile(self,tile,new_pos):
        self.tile = Tiles(tile)
        self.tile.tile_pos = new_pos

    def remove_tile(self):
        self.tile = None

#class ret_Tile:
    #def __init():
        #return
class Bag:

    def __init__(self, bag ="AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ"):
        self.bag = [Tiles(letter) for letter in bag]

    def amount(self):
        return len(self.bag)

    def take(self, num = 1):
        tiles_taken = []

        if self.amount() == 0:
            return "Bag empty"

        for i in range(0, num):
            num = random.randint(0,self.amount()-1)
            tiles_taken.append((self.bag).pop(num))

        return tiles_taken


class Rack:

    def __init__(self):
        self.bag = Bag()
        self.racktiles = [None] * 7
        self.refill()

    def replace_tile(self,oldtile_index,newtile="",new_pos=0):
        if newtile == "":
            self.racktiles[oldtile_index] = Tiles(None)
            self.racktiles[oldtile_index].tile_pos = oldtile_index 
        else:
            self.racktiles[oldtile_index] = Tiles(newtile)
            self.racktiles[oldtile_index].tile_pos = new_pos

    def refill(self):
            nonecount = 0
            none_idx = []
            for idx,til in enumerate(self.racktiles):
                if til == None:
                    nonecount += 1
                    none_idx.append(idx)

            for i,take in enumerate(self.bag.take(nonecount)):
                self.replace_tile(none_idx[i], take.tile_letter, none_idx[i])

    def rack_len(self):
       return len(self.racktiles)


class Player:

    def __init__(self, name, score = 0):
        self.rack = Rack()
        self.name = name
        self.score = score

    def get_name(n):
        return self.name

    def str_details(self):

        print("-----This is Player 1's name----- \n" + self.name)
        print(self.score)


    def get_rack(self):
        print(self.rack.ret_rack())

    def add_score(self, inc):
        self.score += inc

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
        word_score = 0
        tw = False
        dw = False
        for tile in self.word:
            x = Tiles(tile.upper())
            if position[i] in triple_word_coord:
                tw = True
                word_score += x.value
            elif position[i] in double_word_coord:
                dw = True
                word_score += x.value
            elif position[i] in double_letter_coord:
                word_score += x.value + x.value
            elif position[i] in triple_letter_coord:
                word_score += x.value + x.value + x.value
            else:
                word_score += x.value
            i+=1
        if dw == True:
            return word_score * 2
        elif tw == True:
            return word_score * 3
        else:
            return word_score


class Tiles:

    def __init__(self, tile,img=None):
        self.tile_pos = 0
        self.tile_letter = tile
        self.img = img
        if self.tile_letter == "A":
            self.img = pygame.image.load("Scrabble_Images/tiles/A_tile.png")
            self.value = 1
        if self.tile_letter == "B":
            self.img = pygame.image.load("Scrabble_Images/tiles/B_tile.png")
            self.value = 3
        if self.tile_letter == "C":
            self.img = pygame.image.load("Scrabble_Images/tiles/C_tile.png")
            self.value = 3
        if self.tile_letter == "D":
            self.img = pygame.image.load("Scrabble_Images/tiles/D_tile.png")
            self.value = 2
        if self.tile_letter == "E":
            self.img = pygame.image.load("Scrabble_Images/tiles/E_tile.png")
            self.value = 1
        if self.tile_letter == "F":
            self.img = pygame.image.load("Scrabble_Images/tiles/F_tile.png")
            self.value = 4
        if self.tile_letter == "G":
            self.img = pygame.image.load("Scrabble_Images/tiles/G_tile.png")
            self.value = 2
        if self.tile_letter == "H":
            self.img = pygame.image.load("Scrabble_Images/tiles/H_tile.png")
            self.value = 4
        if self.tile_letter == "I":
            self.img = pygame.image.load("Scrabble_Images/tiles/I_tile.png")
            self.value = 1
        if self.tile_letter == "J":
            self.img = pygame.image.load("Scrabble_Images/tiles/J_tile.png")
            self.value = 8
        if self.tile_letter == "K":
            self.img = pygame.image.load("Scrabble_Images/tiles/K_tile.png")
            self.value = 5
        if self.tile_letter == "L":
            self.img = pygame.image.load("Scrabble_Images/tiles/L_tile.png")
            self.value = 1
        if self.tile_letter == "M":
            self.img = pygame.image.load("Scrabble_Images/tiles/M_tile.png")
            self.value = 3
        if self.tile_letter == "N":
            self.img = pygame.image.load("Scrabble_Images/tiles/N_tile.png")
            self.value = 1
        if self.tile_letter == "O":
            self.img = pygame.image.load("Scrabble_Images/tiles/O_tile.png")
            self.value = 1
        if self.tile_letter == "P":
            self.img = pygame.image.load("Scrabble_Images/tiles/P_tile.png")
            self.value = 3
        if self.tile_letter == "Q":
            self.img = pygame.image.load("Scrabble_Images/tiles/Q_tile.png")
            self.value = 10
        if self.tile_letter == "R":
            self.img = pygame.image.load("Scrabble_Images/tiles/R_tile.png")
            self.value = 1
        if self.tile_letter == "S":
            self.img = pygame.image.load("Scrabble_Images/tiles/S_tile.png")
            self.value = 1
        if self.tile_letter == "T":
            self.img = pygame.image.load("Scrabble_Images/tiles/T_tile.png")
            self.value = 1
        if self.tile_letter == "U":
            self.img = pygame.image.load("Scrabble_Images/tiles/U_tile.png")
            self.value = 1
        if self.tile_letter == "V":
            self.img = pygame.image.load("Scrabble_Images/tiles/V_tile.png")
            self.value = 4
        if self.tile_letter == "W":
            self.img = pygame.image.load("Scrabble_Images/tiles/W_tile.png")
            self.value = 4
        if self.tile_letter == "X":
            self.img = pygame.image.load("Scrabble_Images/tiles/X_tile.png")
            self.value = 8
        if self.tile_letter == "Y":
            self.img = pygame.image.load("Scrabble_Images/tiles/Y_tile.png")
            self.value = 4
        if self.tile_letter == "Z":
            self.img = pygame.image.load("Scrabble_Images/tiles/Z_tile.png")
            self.value = 10
        if self.tile_letter == " ":
            self.img = None
            self.value = 0

    def get_letter(self):
        return str(self.tile_letter)
