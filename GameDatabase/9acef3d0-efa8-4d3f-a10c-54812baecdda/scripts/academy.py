#######
#v2.0.0.0#
#######

def nextPhaseAcademy():
	mute()

def tapCard(card, x=0, y=0):
	mute()
	if card.controller == me and card.orientation == Rot0:
			card.orientation = Rot90
			if card.isFaceUp:
				notify("{} Activates {}".format(me, card.Name))
			else:
				notify("{} Activates a card".format(me))

def resetCards():
	mute()
	for card in table:
		if card.controller == me and card.orientation == Rot90 and ("Wall" not in card.type):
			card.orientation = Rot0
			if card.isFaceUp:
				notify("{} Rotates '{}'".format(me, card.Name))
			else:
				notify("{} Rotates a card".format(me))