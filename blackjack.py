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
		sum1 += cardNums[card[0]]
		if(card[0] == 'A'):
			hasAce = True
	if(hasAce):	# if you have two aces, they add to 2, 12, or 22 -- don't need the last one 
		sum2 = sum1 + 10
		return [sum1, sum2] #returns two if they have an ace	
	return [sum1]
	

def parseTotal(cards):
	total = calcTotal(cards)
	if(len(total) > 1 and total[1] <= 21):
		return str(total[0]) + " or " + str(total[1])
	else:
		return str(total[0])

def dealInitialCards():
	global myCards
	global dealerCards
	global deck
	if(len(deck) < 3 * 52):
		resetDeck()
	#deck is shuffled
	myCards = [deck[0], deck[1]]
	dealerCards = [deck[2], deck[3]]
	deck = deck[4:]

def getCard(card):
	return card[0] + card[1]

def displayGame(showDealerCards = False):
	global chips
	if(not inGame):
		print("\nYou have " + str(chips) + " to bet. Use \'bet <amount>\' to start playing!")
		return
	myCardString = ""
	for card in myCards:
		myCardString += getCard(card) + ", "
	myCardString = myCardString[:-2] #remove last comma

	dealerCardString = ""
	for card in dealerCards:
		dealerCardString += getCard(card) + ", "
	dealerCardString = dealerCardString[:-2] #remove last comma

	if(showDealerCards):
		print("Dealer has: " + dealerCardString + " (totals to " + parseTotal(dealerCards) + ")")
	else:
		print("Dealer has: ?, " + getCard(dealerCards[1]))
	print("You have: " + myCardString + " (totals to " + parseTotal(myCards) + ")")

def getFinalScores():
	dTotal = calcTotal(dealerCards)
	myTotal = calcTotal(myCards)
	dFinal = dTotal[0]
	myFinal = myTotal[0]
	if((len(dTotal) > 1) and (dTotal[1] <= 21)):
		dFinal = dTotal[1]
	if((len(myTotal) > 1) and (myTotal[1] <= 21)):
		myFinal = myTotal[1]
	return [dFinal, myFinal]

def clearCurrentGame():
	global myPot
	global inGame
	global myCards
	global dealerCards
	myPot = 0
	myCards = []
	dealerCards = []
	inGame = False
	
def dealerPlay():
	global deck
	global chips
	total = calcTotal(dealerCards)
	while(total[-1] <= 16):
		print("\nDealer hits!")
		dealerCards.append(deck[0])
		deck = deck[1:]
		displayGame(1)
		total = calcTotal(dealerCards)

	print("\nDealer stands!")
	displayGame(1)
	
	scores = getFinalScores()
	if(scores[0] > 21):
		print("\nDealer busts!")
	if(scores[0] < scores[1] or scores[0] > 21):
		print("\nYou win! You get " + str(myPot * 2) + " chips!")
		chips += myPot * 2
	elif(scores[1] < scores[0]):
		print("\nYou lose!")
		# chips += myPot * 2
	elif(scores[0] == scores[1]):
		print("\nYou tie! You get " + str(myPot) + " chips!")
		chips += myPot
	clearCurrentGame()

def bust():
	clearCurrentGame()

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
		global inGame
		""""bet <amount> - Start the game with this bet."""
		if(inGame):
			print("In game! Must hit or stand.")
			return
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
		dealInitialCards()
		displayGame()
		total = calcTotal(myCards)
		if(total[0] == 21 or (len(total) > 1 and total[1] == 21)):
			print("Blackjack!")
			dealerPlay()
			displayGame()

	def do_hit(self, arg):
		global inGame
		global myCards
		global deck
		if(not inGame):
			print("Cannot hit if not in game!")
			return
		total = calcTotal(myCards)
		if(total[0] >= 21):
			print("Cannot hit!")
			return
		global deck
		myCards.append(deck[0])
		deck = deck[1:]
		total = calcTotal(myCards)
		print("You hit!")
		if(total[0] > 21):
			displayGame()
			print("Bust!")
			bust()
		if(total[0] == 21 or (len(total) > 1 and total[1] == 21)):
			displayGame()
			print("Blackjack!")
			dealerPlay()
		displayGame()
		return

	def do_stand(self, arg):
		global inGame
		if(not inGame):
			print("Cannot stand if not in game!")
			return
		displayGame(1)
		dealerPlay()
		displayGame()

	def help_bet(self):
		print('You can start a game by betting an amount between 0 and your chip count, ' + str(chips) + '. Use the command \'bet <amount>\'.')

	def help_play(self):
		print('Bet an amount to start the game. During the game, use hit, split, or stand.')

if __name__ == '__main__':
	for num in cardNums:
		for suit in suits:
			allCards.append([num, suit])

	print('Play Blackjack!')
	print('====================')
	print()
	print('(Type "help" for commands.)')
	print()
	displayGame()
	BlackjackCmd().cmdloop()
	print('Thanks for playing!')