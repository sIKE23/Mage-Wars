#######
#v2.0.0.0#
#######

def inspectCard(card, x = 0, y = 0):
	whisper("{}".format(card))
	for k in card.properties:
		if len(card.properties[k]) > 0:
			whisper("{}: {}".format(k, card.properties[k]))
			
#Check see if a card at x1,y1 overlaps a card at x2,y2
#Both have size w, h
def overlaps(x1, y1, x2, y2, w, h):
	#Four checks, one for each corner
	if x1 >= x2 and x1 <= x2 + w and y1 >= y2 and y1 <= y2 + h: return True
	if x1 + w >= x2 and x1 <= x2 and y1 >= y2 and y1 <= y2 + h: return True
	if x1 >= x2 and x1 <= x2 + w and y1 + h >= y2 and y1 <= y2: return True
	if x1 + w >= x2 and x1 <= x2 and y1 + h >= y2 and y1 <= y2: return True
	return False

def cardHere(x, y, stat=""):
	for c in table:
		if c.controller == me:
			cx, cy = c.position
			#if overlaps(x, y, cx, cy, c.width(), c.height()):
			if x >= cx and x <= cx+c.width() and y >= cy and y <= cy+c.height() and stat in c.Stats:
				return c
	return None

def findCard(group, model):
	for c in group:
		if c.model == model:
			return c
	return None
	
def advanceTurn():
	mute()
	nextPlayer = getNextPlayerNum()
	nextPlayerName = getGlobalVariable("P" + str(nextPlayer) + "Name")
	for p in players:
		if p.name == nextPlayerName:
			for p2 in players:
				remoteCall(p2, "setActiveP", [p])

#def setActiveP(p):
#	p.setActive()
