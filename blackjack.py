import cmd, textwrap
import random
import math

random.seed(1)
chips = 1000
myPot = 0
inGame = False #gameplay goes bet, play, bet, play, etc.
myCards = []
dealerCards = []
suits = [" of hearts", " of spades", " of clubs", " of diamonds"]
cardNums = {'A': 1, 
			'2': 2, 
			'3': 3, 
			'4': 4, 
			'5': 5, 
			'6': 6, 
			'7': 7, 
			'8': 8, 
			'9': 9, 
			'10': 10,
			'J': 10,
			'Q': 10,
			'K': 10}
allCards = []
deck = []

def displayPot(amount):
	print("You have " + str(amount) + " chips remaining.")

def resetDeck():
	global deck
	for dNum in range(0, 6):
		for i in range(0, 4):
			for card in cardNums:
				deck.append([card, suits[i]])
	random.shuffle(deck)

def calcTotal(cards):
	sum1 = 0
	sum2 = -1
	hasAce = False
	for card in cards:
		sum1 += cardNums[allCards[card][0]]
		if(allCards[card][0] == 'A'):
			hasAce = True
	if(hasAce):	# if you have two aces, they add to 2, 12, or 22 -- don't need the last one 
		sum2 = sum1 + 10
	if(sum2 > 21 or sum2 < 0):
		return [sum1]
	return [sum1, sum2]

def parseTotal(cards):
	total = calcTotal(cards)
	if(len(total) > 1):
		return str(total[0]) + " or " + str(total[1])
	else:
		return str(total[0])

def dealCards():
	if(len(deck) < 3 * 52):
		resetDeck()
	global myCards
	global dealerCards
	cards = []
	nextCard = -1
	#deck is shuffled
	myCards = [deck[0], deck[1]]
	dealerCards = [deck[2], deck[3]]
	deck = deck[4:]

def getCard(num):
	return allCards[num][0] + allCards[num][1]

def displayGame():
	print("Dealer has: ?, " + getCard(dealerCards[1]))
	print("You have: " + getCard(myCards[0]) + ", " + getCard(myCards[1]) + " (totals to " + parseTotal(myCards) + ")")

class BlackjackCmd(cmd.Cmd):
	prompt = '\n> '
	# The default() method is called when none of the other do_*() command methods match.
	def default(self, arg):
		print('I do not understand that command. Type "help" for a list of commands.')

	# A very simple "quit" command to terminate the program:
	def do_quit(self, arg):
		"""Quit the game."""
		return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

	def do_bet(self, arg):
		global myPot
		global chips
		""""bet <amount> - Start the game with this bet."""
		# put this value in a more suitably named variable
		if(not arg.isnumeric()):
			print("You must bet a numeric value.")
			return
		amount = int(arg)
		if(amount > chips or amount <= 0):
			print("Invalid amount, you only have " + str(chips) + " chips to bet!")
			return

		chips -= amount
		myPot += amount
		inGame = True
		print("Successfully bet " + str(myPot) + " chips. You have " + str(chips) + " left.")
		dealCards()
		displayGame()

	def help_bet(self):
		print('You can start a game by betting an amount between 0 and your chip count, ' + str(chips) + '. Use the command \'bet <amount>\'.')

	def help_play(self):
		print('Bet an amount to start the game. During the game, use hit, split, or stand.')

if __name__ == '__main__':
	for num in cardNums:
		for suit in suits:
			allCards.append([num, suit])

	print('Blackjack!')
	print('====================')
	print()
	print('(Type "help" for commands.)')
	print()
	displayPot(chips)
	BlackjackCmd().cmdloop()
	print('Thanks for playing!')