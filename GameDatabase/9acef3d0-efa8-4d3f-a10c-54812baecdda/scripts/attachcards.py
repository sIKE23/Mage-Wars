###########################################################################
##########################    v1.13.0.0     #######################################
###########################################################################
############################
# Card Attachment and Alignment
############################

def menuDetachAction(card,x=0,y=0):
	"""This detaches <card> and returns it to its home location"""
	mute()
	if isAttached(card):
		detach(card)
		moveCardToDefaultLocation(card,True)

def attachToTarget(card,x=0,y=0):
	"""This command is used to explicitly attach one card to the card currently being targeted."""
	mute()
	if isAttachCardsEnabled() == "True":
		if card.controller == me:
			target = [cards for cards in table if cards.targetedBy==me]
			if len(target) == 0 or (len(target) == 1 and card in target):
				c,t = detach(card)
				if t:
					notify("{} detaches {} from {}.".format(me,c,t))
			elif len(target) == 1:
				c,t = attach(card, target[0])
				if t:
					notify("{} attaches {} to {}.".format(me,c,t))
			else:
				whisper("Incorrect targets, select up to 1 target.")
				return
	else:
		whisper("AttachCards must be enabled to use this feature")
	return

def attach(card,target):
	"""Controller of <card> may attach it to <target>."""
	mute()
	unbind(card)
	if card.controller == me and canAttach(card,target):
		detachAll(card)
		consolidateAttachments(target)
		setGlobalDictEntry("attachDict",card._id,[target._id,len(getAttachments(target))+1])
		remoteCall(target.controller,'alignAttachments',[target])
		return card,target
	return card,None

def enchantmentAttachCost(card,target): #Target useful for when things like Harshforge Plate are integrated into this.
	discountStr = ''
	discount = 0
	foundDiscounts = []
	infostr = 'Enchantments cost 2 mana to cast.'
	notifyStr = "{} attaches a hidden enchantment on {}, with a base cost of 2 mana.".format(me, target.name)
	for c in table:
		if c.controller == me and c.isFaceUp and "[Casting Discount]" in c.Text and c != card:
			dc = findDiscount(card, c)
			debug("Discount Count Returned from test: {} from card: {}".format(dc, c.Name))
			if dc > 0:
				discountStr = "\nCost reduced by {} due to {}".format(dc, c.name)
				infostr = notifyStr + discountStr
				notifyStr = notifyStr + discountStr
				discount += dc
				foundDiscounts.append(c)
			elif dc < 0:
				discountStr = "\n{} already reached max uses this round.".format(c.name)
				infostr = notifyStr + discountStr
				notifyStr = notifyStr + discountStr
	choice = askChoice('Do you want to cast {} face-down on {}?'.format(card.name,target.name),['Yes, I am casting this as a spell','No, I want to attach it for other reasons'],["#171e78","#de2827"])
	if choice == 1:
		infostr += "\nTotal mana amount to subtract from mana pool?"
	manacost = askInteger(infostr, 2 - discount)
	if manacost == None: return # player closed the window and didn't cast the spell
	elif me.Mana < manacost:
		notify("{} has insufficient mana in pool".format(me))
		return
	for dc in foundDiscounts:
		doDiscount(dc)
	me.Mana -= manacost 
	notify(notifyStr)
				
def detach(card):
	"""Removes <card> from its target, then consolidates remaining cards on target."""
	mute()
	if isAttached(card) and card.controller == me:
		target = getGlobalDictEntry('attachDict',card._id)
		setGlobalDictEntry('attachDict',card._id,None)
		if target:
			target = Card(target[0])
			consolidateAttachments(target)
			if card.controller == me: alignAttachments(target)
			else: remoteCall(target.controller,'alignAttachments',[target])
		return card,target
	return card,None

def alignCards(cardList,xOffset,yOffset):
	"""
	Input is a list of card objects that need to be aligned. The first card in the list is the card against which the second will be aligned.
	This function is recursive. When called, the first call should be on the card to which the rest are attached.
	The input MUST be a list of length at least 2.
	"""
	mute()

	#1: Align the second card in the list with the first
	c0,c1 = cardList[0],cardList[1]
	x0,y0 = c0.position
	x1,y1 = x0 + xOffset, y0 + yOffset

	c1.moveToTable(x1,y1)

	#2: Move the second card beneath the first
	c1.setIndex(c0.getIndex)

	#3: Slice the list. If it is now shorter than 2 cards, we are done.
	cardList = cardList[1:]
	if len(cardList) < 2: return

	#4: Otherwise, the owner of the second card in the new list calls this function.
	nextCard = cardList[1]
	remoteCall(nextCard.controller,"alignCards",[cardList,xOffset,yOffset])

def alignAttachments(card):
	"""
	Aligns the attachments of input card.
	Requires that input card belong to calling player

	"""
	mute()

	#1: Retrieve attachments and end function if there are none.
	attachments = getAttachments(card)

	if not attachments: return

	#2: Controller of first attachment calls alignCards
	cardList = [card] + attachments
	firstAttachment = attachments[0]

	remoteCall(firstAttachment.controller,"alignCards",[cardList,0,-12])

	#3: Profit??? Seriously, the previous method was way too convoluted.

def detachAll(card):
	"""Removes all attachments from <card> and places them in front of their owners"""
	mute()
	attachments = getAttachments(card)
	for c in attachments:
		if c.controller == me:
			detach(c)
			moveCardToDefaultLocation(c,True)
		else:
			remoteCall(c.controller,'detach',[c])
			remoteCall(c.controller,'moveCardToDefaultLocation',[c,True])
		rnd(0,0)

def unbindAll(card):
	"""Like detachAll, but for bound spells"""
	mute()
	c = getBound(card)
	if c:
		if c.controller == me:
			unbind(c)
			moveCardToDefaultLocation(c,True)
		else:
			remoteCall(c.controller,'unbind',[c])
			remoteCall(c.controller,'moveCardToDefaultLocation',[c,True])
		rnd(0,0)

def dismountAll(card):
	"""Like detachAll, but for mounteds"""
	mute()
	c = getMounted(card)
	if c:
		if c.controller == me:
			dismount(c)
		else:
			remoteCall(c.controller,'dismount',[c])
		rnd(0,0)


def isAttached(card):
	"""Determines whether <card> is attached to anything."""
	mute()
	if getGlobalDictEntry('attachDict',card._id) and card in table:
		return True
	return False

def consolidateAttachments(card):
	return
	"""Reorders attachments on target card to eliminate gaps between indices"""
	mute()
	aDict = eval(getGlobalVariable("attachDict"))
	attachments=getAttachments(card)
	count = 1
	for c in attachments:
		aDict[c._id] = [card,count]
		count +=1
	setGlobalVariable("attachDict",str(aDict))

def getAttachments(card):
	"""Returns a list of cards that are attached to <card>, sorted by their attachment order"""
	mute()
	aDict = eval(getGlobalVariable("attachDict"))
	attachList = [key for key in aDict if aDict[key] and int(aDict[key][0]) == card._id]
	attachList.sort(key=lambda k: aDict[k][1])
	return [Card(key) for key in attachList if Card(key) in table]

def getAttachTarget(card):
	mute()
	result = getGlobalDictEntry('attachDict',card._id)
	if result and card in table: return Card(result[0])

def getGlobalDictEntry(dictionary,key):
	"""Dictionary is input as a string. If the value is empty, returns False"""
	mute()
	gDict = eval(getGlobalVariable(dictionary))
	if key in gDict:
		return gDict[key]
	return None

def setGlobalDictEntry(dictionary,key,value):
	"""Note that dictionary is input as a string"""
	mute()
	gDict = eval(getGlobalVariable(dictionary))
	gDict[key] = value
	setGlobalVariable(dictionary,str(gDict))

def canAttach(card,target):
	"""Determines whether <card> may be attached to <target>"""
	tType = target.Type
	if (card==target
		or not target in table
		or not card in table
		or tType not in ['Conjuration','Creature','Conjuration-Wall','Equipment','Mage']
		or not target.isFaceUp
		or isAttached(target)
		or getAttachments(card)): return False
	cName = card.Name
	tName = target.Name
	cTargetBar = card.Target
	cType = card.Type
	attachments = getAttachments(target)
	cController = card.controller
	tController = target.controller
	for a in attachments:
		if (a.isFaceUp or a.controller == me) and a.Name == cName: return False
	traits = computeTraits(target)
	for s in card.Subtype.split(', '):
		if s in traits.get('Immunity',[]): return False
	if cName in ['Force Hold','Force Crush','Tanglevine','Stranglevine'] and traits.get('Uncontainable'): return False
	if cType == 'Enchantment':
		if ((cName == 'Harmonize' and 'Channeling' in target.Stats) or
			(cName == 'Barkskin' and tName == 'Druid') or
			(cName == 'Forcefield' and tName == 'Forcemaster') or
			(cTargetBar == 'Corporeal Creature' and tType in ['Creature','Mage'] and traits.get('Corporeal')) or
			(cTargetBar == 'Corporeal Conjuration or Creature' and tType in ['Creature','Mage','Conjuration'] and traits.get('Corporeal')) or
			(cTargetBar == 'Creature' and tType in ['Creature','Mage']) or			
			(cTargetBar == 'Paladin Mage' and tType in ['Mage'] and tName == 'Paladin') or
			(cTargetBar == 'Friendly Living Creature' and tType in ['Creature','Mage'] and traits.get('Living') and tController == cController) or
			(cTargetBar == 'Enemy Creature' and tType in ['Creature','Mage'] and tController != cController) or
			(cTargetBar == 'Friendly, Soldier Creature' and tType in ['Creature','Mage'] and 'Soldier' in target.Subtype and tController == cController) or
			(cTargetBar == 'Demon Creature' and tType in ['Creature'] and 'Demon' in target.Subtype) or
			(cTargetBar == 'Incorporeal Creature' and tType in ['Creature','Mage'] and traits.get('Incorporeal')) or
			(cTargetBar == 'Living Creature' and tType in ['Creature','Mage'] and traits.get('Living')) or
			(cTargetBar == 'Living Non-Aquatic Creature' and tType in ['Creature','Mage'] and traits.get('Living') and not traits.get('Aquatic')) or
			(cTargetBar == 'Living Non-Mage Creature' and tType == 'Creature' and traits.get('Living')) or
			(cTargetBar == 'Minor Creature' and tType == 'Creature' and target.Level <= 2) or
			(cTargetBar == 'Minor Corporeal Creature' and tType == 'Creature' and traits.get('Corporeal') and target.Level <= 2) or
			(cTargetBar == 'Minor Living Creature' and tType == 'Creature' and traits.get('Living') and target.Level <= 2) or
			(cTargetBar == 'Minor Living Animal Creature' and tType == 'Creature' and traits.get('Living') and target.Level <= 2 and 'Animal' in target.Subtype) or
			(cTargetBar == 'Knight Creature' and tType in ['Creature'] and 'Knight' in target.Subtype) or
			(cTargetBar == 'Living Holy Creature' and tType in ['Creature'] and 'Holy' in target.School and traits.get('Living')) or
			(cTargetBar == 'Holy Creature' and tType in ['Creature'] and 'Holy' in target.School and traits.get('Living')) or
			(cTargetBar == 'Mage' and tType == 'Mage') or
			(cTargetBar == 'Non-Flying Creature' and tType in ['Creature','Mage'] and not traits.get('Flying')) or
			(cTargetBar == 'Nonliving Corporeal Conjuration' and 'Conjuration' in tType and traits.get('Corporeal')) or
			(cTargetBar == 'Non-Mage Corporeal Creature' and tType=='Creature' and traits.get('Corporeal')) or
			(cTargetBar == 'Non-Mage Creature' and tType=='Creature') or
			(cTargetBar == 'Non-Mage Living Creature' and tType=='Creature' and traits.get('Living')) or
			(cTargetBar == 'Non-Mage, Non-Epic Living Creature' and tType=='Creature' and traits.get('Living') and not traits.get('Epic')) or
			(cTargetBar == 'Non-Mage Object' and tType!='Mage') or
			(cTargetBar == 'Zone or Object') or
			(cTargetBar == 'Object or Zone')): return True
	elif ((cType == 'Equipment' and tType == 'Mage') or
		(cName in ['Tanglevine','Stranglevine','Quicksand'] and tType in ['Creature','Mage'] and not traits.get('Flying'))): return True
	return False

def isAttachCardsEnabled():
	"""Checks whether the attachCards module is turned on."""
	return getSetting("attachCards", "True")

############################################################################
##########################  Bound Spells  ##################################
############################################################################
"""We will make a distinction between attached cards and bound cards (for familiars,
spawnpoints, and spellbind objects"""

def bind(card,target):
	"""Controller of <card> may attach it to <target>."""
	mute()
	detach(card)
	if card.controller == me:
		b = getBound(target)
		if b: unbind(b)
		detachAll(card)
		setGlobalDictEntry("bindDict",card._id,target._id)
		remoteCall(target.controller,'alignBound',[target])
		return card,target
	return card,None

def unbind(card):
	"""Unbinds <card> from its target."""
	mute()
	if card.controller == me:
		target = getGlobalDictEntry('bindDict',card._id)
		setGlobalDictEntry('bindDict',card._id,None)
		return card,target
	return card,None

def getBound(card):
	"""Returns the card bound to <card>"""
	mute()
	bDict = eval(getGlobalVariable("bindDict"))
	bound = map(lambda key: Card(key),[k for k in bDict if bDict[k]==card._id])
	if bound and bound[0] in table: return bound[0]

def getBindTarget(card):
	mute()
	result = getGlobalDictEntry('bindDict',card._id)
	if result and card in table: return Card(result)

def alignBound(card):
	"""
	Aligns the card bound to input card.
	Requires that input card belong to calling player

	"""
	mute()

	#1: Retrieve bound card and end function if there are none.
	bound = getBound(card)
	if not bound: return

	#2: Align the cards
	cardList = [card,bound]
	alignCards(cardList,0,30)

def canBind(card,target):
	"""Determines whether <card> may be attached to <target>"""
	if (card==target
		or not target in table
		or not card in table
		or isAttached(target)
		or getAttachments(card)
		or getBound(card)
		or getBound(target)
		or not target.isFaceUp): return False
	tName = target.Name
#Familiars
	if ((tName == 'Goblin Builder' and 'Conjuration' in card.Type and card.Name not in['Tanglevine','Stranglevine','Quicksand'])
		or (tName == 'Thoughtspore' and card.Type in ['Attack','Incantation'] and sum([int(i) for i in card.level.split('+')])<=2)
		or (tName == 'Wizard\'s Tower' and card.Type == 'Attack' and 'Epic' not in card.Traits and card.Action == 'Quick')
		or (tName == 'Sersiryx, Imp Familiar' and ((card.Type == 'Attack' and 'Fire' in card.School) or (card.Type == 'Enchantment' and 'Curse' in card.Subtype)) and sum([int(i) for i in card.level.split('+')])<=2)
		or (tName == 'Fellella, Pixie Familiar' and card.Type == 'Enchantment')
		or (tName == 'Huginn, Raven Familiar' and card.Type == 'Incantation' and sum([int(i) for i in card.level.split('+')])<=2)
		or (tName == 'Gurmash, Orc Sergeant' and 'Command' in card.Subtype)
		or (tName == 'Sectarus, Dark Rune Sword' and (card.Type == 'Enchantment' and 'Curse' in card.Subtype))
		or (tName == 'Cassiel, Shield of Asyra' and (card.Subtype == 'Healing' or card.Subtype == 'Protection'))
		or (tName == 'The Squire' and card.Type == 'Equipment')
		or (tName ==  'Naiya' and card.School == 'Water' and not 'Creature' in card.Type)
#Spawnpoints
		or (tName == 'Barracks' and card.Type == 'Creature' and 'Soldier' in card.Subtype and target.markers[Mana] >= 2)
		or (tName == 'Battle Forge' and card.Type == 'Equipment')
		or (tName == 'Gate to Voltari' and card.Type == 'Creature' and 'Arcane' in card.School and not ("Incorporeal" in card.Traits) and target.markers[Mana] >= 3)
		or (tName == 'Lair' and card.Type == 'Creature' and 'Animal' in card.Subtype)
		or (tName == 'Pentagram' and card.Type == 'Creature' and 'Dark' in card.School and not ('Nonliving' in card.Traits or 'Incorporeal' in card.Traits) and target.markers[Mana] >= 2)
		or (tName == 'Temple of Asyra' and card.Type == 'Creature' and 'Holy' in card.School and target.markers[Mana] >= 2)
		or (tName == 'Graveyard' and card.Type == 'Creature' and 'Dark' in card.School and ('Nonliving' in card.Traits or 'Incorporeal' in card.Traits))
		or (tName == 'Seedling Pod' and card.Type in ['Creature','Conjuration','Conjuration-Wall'] and 'Plant' in card.Subtype and target.markers[Mana] >= 3)
		or (tName == 'Samara Tree' and card.Name == 'Seedling Pod')
		or (tName == 'Vine Tree' and card.Type in ['Creature','Conjuration','Conjuration-Wall'] and 'Vine' in card.Subtype)
		or (tName == 'Libro Mortuos' and card.Type == 'Creature' and 'Undead' in card.Subtype)
		or (tName == 'Triton\'s Horn' and card.Type == 'Creature' and 'Water' in card.School)
#Spellbind (only)
		or (tName == 'Helm of Command' and card.Type == 'Incantation' and 'Epic' not in card.Traits and 'Command' in card.Subtype)
		or (tName == 'Elemental Wand' and card.Type == 'Attack' and 'Epic' not in card.Traits)
		or (tName == 'Mage Wand' and card.Type == 'Incantation' and 'Epic' not in card.Traits)):
		return True
	return False

############################################################################
##########################     Mounts     ##################################
############################################################################

def mount(card,target):
	"""
	Mounts <card> upon <target>
	"""
	mute()
	dismount(card)
	if card.controller == me:
		b = getMounted(target)
		if b: dismount(b)
		setGlobalDictEntry("mountDict",card._id,target._id)
		remoteCall(target.controller,'alignMounted',[target])
		return card,target
	return card,None

def dismount(card):
	"""
	Removes <card> from its mount
	"""
	mute()
	if card.controller == me:
		target = getGlobalDictEntry('mountDict',card._id)
		setGlobalDictEntry('mountDict',card._id,None)
		return card,target
	return card,None

def getMounted(card):
	"""Returns the card mounted upon <card>"""
	mute()
	mDict = eval(getGlobalVariable("mountDict"))
	mounted = [Card(key) for key in mDict if mDict[key]==card._id]
	if mounted and mounted[0] in table: return mounted[0]

def getMount(card):
	"""Returns <card>'s mount"""
	mute()
	result = getGlobalDictEntry('mountDict',card._id)
	if result and card in table: return Card(result)

def alignMounted(card):
	"""
	Aligns the card mounted upon input card.
	Requires that input card belong to calling player
	"""
	mute()

	#1: Retrieve bound card and end function if there are none.
	mounted = getMounted(card)
	if not mounted: return

	#2: Align the cards
	cardList = [card,mounted]
	alignCards(cardList,card.width()-20,0) #For now, we will simply put the cards side by side.

def canMount(card,target):
	return card.Name == "Paladin" and target.Name == "Pegasus"

############################################################################
##########################    Zones       ##################################
############################################################################

def createMap(I,J,zoneArray,tileSize):
	mapDict = {'I' : I,
			   'J' : J,
			   'tileSize' : tileSize,
			   'x' : -tileSize*I/2,
			   'y' : -tileSize*J/2,
			   'X' : tileSize*I,
			   'Y' : tileSize*J}
	array = list(zoneArray)
	zoneList = []
	for i in range(len(zoneArray)):
		for j in range(len(zoneArray[0])):
			z = (createZone(i,j,mapDict['x'],mapDict['y'],mapDict['tileSize']) if zoneArray[i][j] else {})
			array[i][j] = z 
			if z: zoneList.append(z)
	mapDict['zoneArray'] = array
	mapDict['zoneList'] = zoneList
	return mapDict

def createZone(i,j,mapX,mapY,size):
	return  {'i' : i,
			 'j' : j,
			 'x' : mapX+i*size,
			 'y' : mapY+j*size,
			 'size' : size}

def zoneContains(zone,card): #returns whether an object is inside the zone
	x,y = card.position
	X,Y = card.width(),card.height()
	if getAttachTarget(card):
		return zoneContains(zone,getAttachTarget(card))
	else:
		if ((zone.get('x') < x < zone.get('x') + zone.get('size') - X) and
			(zone.get('y') < y < zone.get('y') + zone.get('size') - Y)): return True
	return False

def zoneBorders(zone,card): #returns whether an object overlaps the zone border
	x,y = card.position
	X,Y = card.width(),card.height()
	if (zoneContains(zone,card) or
		(x > zone.get('x') + zone.get('size')) or (x < zone.get('x') - X) or
		(y > zone.get('y') + zone.get('size')) or (y < zone.get('y') - Y)): return False
	return True

def zoneClosest(zoneList,card): #finds closest zone from a list. If border is enabled, returns
	x,y = card.position
	X,Y = card.width(),card.height()
	x += X/2
	y += Y/2
	zone = zoneList[0]
	for z in zoneList:
		zX, zY = z.get('x')+z.get('size')/2,z.get('y')+z.get('size')/2
		zoneX, zoneY = zone.get('x')+zone.get('size')/2,zone.get('y')+zone.get('size')/2
		if abs(zX-x)+abs(zY-y) < abs(zoneX-x)+abs(zoneY-y): zone = z
	return zone

def zoneGetContain(zone,card): # Finds the closest straight-line place to move the object so it is contained.
	x,y = card.position
	X,Y = card.width(),card.height()
	coordinates = [x,y]
	if (x <= zone.get('x')): coordinates[0] = zone.get('x') + 1
	if (x + X >= zone.get('x')+zone.get('size')): coordinates[0] = zone.get('x') + zone.get('size') - X - 1
	if (y <= zone.get('y')): coordinates[1] = zone.get('y') + 1
	if (y + Y >= zone.get('y')+zone.get('size')): coordinates[1] = zone.get('y') + zone.get('size') - Y - 1
	return (coordinates[0],coordinates[1])

def zoneGetBorder(zone,card): #like getContain, but for borders. Snaps to the nearest border.
	x,y = card.position
	X,Y = card.width(),card.height()
	borders = [[(zone['x']),(zone['y'] + zone['size']/2)],
			   [(zone['x'] + zone['size']/2),(zone['y'])],
			   [(zone['x'] + zone['size']),(zone['y'] + zone['size']/2)],
			   [(zone['x'] + zone['size']/2),(zone['y'] + zone['size'])]]
	c = [x+X/2,y+Y/2]
	border = borders[0]
	for b in list(borders):
		if (abs(b[0]-c[0]) + abs(b[1]-c[1])) < (abs(border[0]-c[0]) + abs(border[1]-c[1])): border = b
	return (border[0]-X/2,border[1]-Y/2)

def cardGetDistance(card1,card2):
	zone1 = getZoneContaining(card1)
	zone2 = getZoneContaining(card2)
	return zoneGetDistance(zone1,zone2)

def zoneGetDistance(zone1,zone2):
	return abs(zone1['i']-zone2['i']) + abs(zone1['j']-zone2['j'])

def getZoneContaining(card): #returns the zone occupied by the card. If attached, will return zone occupied by attachee.
	if not getGlobalVariable("Map"): return
	if getAttachTarget(card): return getZoneContaining(getAttachTarget(card))
	mapDict = eval(getGlobalVariable("Map"))
	x,X,y,Y = mapDict.get('x'),mapDict.get('X'),mapDict.get('y'),mapDict.get('Y')
	tileSize = mapDict.get('tileSize')
	zoneArray = mapDict.get('zoneArray')
	cx,cy = card.position
	cX,cY = (card.width(),card.height())
	if not (x<cx+cX/2<x+X and y<cy+cY/2<y+Y): return None
	i,j = int(float(cx+cX/2-x)/tileSize),int(float(cy+cY/2-y)/tileSize)
	if zoneArray[i][j]: return zoneArray[i][j]

def getZonesBordering(card): #returns list of zones bordered by card
	if not getGlobalVariable("Map"): return
	mapDict = eval(getGlobalVariable("Map"))
	zoneList = []
	for z in list(mapDict.get('zoneList',[])):
		if zoneBorders(z,card): zoneList.append(z)
	return zoneList

def getCardsInZone(zone): #returns a list of cards in the zone
	cardList = []
	for c in table:
		if getZoneContaining(c) == zone: cardList.append(c)
	return cardList

def snapToZone(card):
	zoneList = getZonesBordering(card)
	if zoneList:
			zone = zoneClosest(zoneList,card)
			if card.Target == 'Zone' or card.Type == 'Mage' or not card.isFaceUp: #snap to zone
					snapX,snapY = zoneGetContain(zone,card)
					card.moveToTable(snapX,snapY)
			elif card.type == 'Conjuration-Wall': #snap to zone border
					snapX,snapY = zoneGetBorder(zone,card)
					card.moveToTable(snapX,snapY)

