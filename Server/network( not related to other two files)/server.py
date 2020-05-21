from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from ScrabbleClasses import *

from time import sleep

#Create the channel to deal with our incoming requests from the client
#A new channel is created every time a client connects
class ClientChannel(Channel):

    #Create a function that will respond to a request to move a player
    def Network_move(self, data):

        #Fetch the data top help us identify which game needs to update
        gameID = data['gameID']
        player = data['player']
        x = data['x']
        y = data['y']

        #Call the move function of the server to update this game
        self._server.move_player(x, y, gameID, player)

#Create a new server for our game
class GameServer(Server):

    #Set the channel to deal with incoming requests
    channelClass = ClientChannel()

    #Constructor to initialize the server objects
    def __init__(self, *args, **kwargs):

        #Call the super constructor
        Server.__init__(self, *args, **kwargs)

        #Create the objects to hold our game ID and list of running games
        self.games = []
        self.queue = None
        self.gameIndex = 0

        #Set the velocity of our player

    #Function to deal with new connections
    def Connected(self, channel, addr):
        print("New connection: {}".format(channel))

        #When we receive a new connection
        #Check whether there is a game waiting in the queue
        if self.queue == None:

            #If there isn't someone queueing
            #Set the game ID for the player channel
            #Add a new game to the queue
            channel.gameID = self.gameIndex
            self.queue = Game(channel, self.gameIndex)

        else:

            #Set the game index for the currently connected channel
            channel.gameID = self.gameIndex

            #Set the second player channel
            self.queue.player_channels.append(channel)

            #Send a message to the clients that the game is starting
            for i in range(0, len(self.queue.player_channels)):
				self.queue.player_channels[i].Send({"action":"startgame","player":i,"gameID":self.queue.gameID,"velocity":self.velocity})

            #Add the game to the end of the game list
            self.games.append(self.queue)

            #Empty the queue ready for the next connection
            self.queue = None

            #Increment the game index for the next game
            self.gameIndex += 1

    #Create a function to move the players of a game
    def move_tile(self, x, y, gameID, player):

		#Get the game
		game = self.games[gameID]

		#Update the correct player
		game.players[player].move(x, y)



		#For all the other players send a message to update their position
		for i in range(0, len(game.player_channels)):

			#If we aren't looking at the player that was updated
			if not i == player:

				#Send a message to update
				game.player_channels[i].Send({"action":"position","player":player,"x":g.players[player].x,"y":g.players[player].y})

#Create the game class to hold information about any particular game
class Game(object):

    #Constructor
    def __init__(self, player, gameIndex):

        #Create a list of players
        #Player.turn = true or false if it is their go
        self.players = []
        self.players.append(Player(True))
        self.players.append(Player(False))
        self.players.append(Player(False))
        self.players.append(Player(False))

        #Store the network channel of the first client
        self.player_channels = [player]

        #Set the game id
        self.gameID = gameIndex

#Create a player class to hold all of our information about a single player

class Player:

	def __init__(self,turn = False, name = '', score = 0):
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

	#Create a function to move this player

#--------------------------------------------------------------------------------------------------------------------------------
	def take_turn(self):

		#Update the variables
		self.x += x
		self.y += y

#--------------------------------------------------------------------------------------------------------------------------------



#Start the server, but only if the file wasn't imported
if __name__ == "__main__":

    print("Server starting on LOCALHOST...\n")

    #Create a server
    s = GameServer()

    #Pump the server at regular intervals (check for new requests)
    while True:
        s.Pump()
        sleep(0.0001)
