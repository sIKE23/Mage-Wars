# functions that I see are not used anywhere, at least that is what I think - delete when we are done

# I am guessing that Cosworth used another game as a jumping point and these fuctions were from that game 


Die = [ "DieBlank",
		"DieBlank",
		"Die1",
		"Die2",
		"Die1s",
		"Die2s"]

DieBlank = ("No Damage","a1f061ec-efbe-444e-8e06-8d973600696c")
Die1 = ("1 Normal Damage","8cc1704a-6f2f-4dbf-a80c-8f79a5a8d165")
Die2 = ("2 Normal Damageface","b881f652-9384-43e1-9758-e68b04583b3b")
Die1s = ("1 Critical Damage","a3d3fff3-bb1c-4469-9a9d-f8dc1f341d39")
Die2s = ("2 Critical Damage","101976ea-ec22-4496-a762-6fbc0d1a41bb")


def inspectCard(card, x = 0, y = 0):
	whisper("{}".format(card))
	for k in card.properties:
		if len(card.properties[k]) > 0:
			whisper("{}: {}".format(k, card.properties[k]))
			

def returnToHand(card): #Return card to your hand
	card.moveTo(me.hand)
	



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


def cardX(card):
	x, y = card.position
	return x

def cardY(card):
	x, y = card.position
	return y


def findCard(group, model):
	for c in group:
		if c.model == model:
			return c
	return None