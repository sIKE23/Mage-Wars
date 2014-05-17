############################################################################
##########################    v1.6.5.0    ##################################
############################################################################
import time
import re
############################################################################
##########################		Constants		##################################
############################################################################

##########################		Markers			##################################

ActionRed = ("Action", "4dd182d2-6e69-499c-b2ad-38701c0fb60d")
ActionRedUsed = ("Action Used", "2e069a99-1696-4cbe-b6c6-13e1dda29563")
ActionBlue = ("Action", "c980c190-448d-414f-9397-a5f17068ac58")
ActionBlueUsed = ("Action Used", "5926df42-919d-4c63-babb-5bfedd14f649")
ActionGreen = ("Action", "9cd83c4b-91b7-4386-9d9a-70719971f949")
ActionGreenUsed = ("Action Used", "5f20a2e2-cc59-4de7-ab90-cc7d1ced0eee")
ActionYellow = ("Action", "2ec4ddea-9596-45cc-a084-23caa32511be")
ActionYellowUsed = ("Action Used", "7c145c5d-54c3-4f5b-bf66-f4d52f240af6")
Mana = ("Mana", "00000000-0000-0000-0000-000000000002")
Damage = ("Damage", "00000000-0000-0000-0000-000000000004")
BloodReaper = ("BloodReaper","50d83b50-c8b1-47bc-a4a8-8bd6b9b621ce")
Burn = ("Burn", "f9eb0f3a-63de-49eb-832b-05912fc9ec64")
Cripple = ("Cripple", "82df2507-4fba-4c81-a1de-71e70b9a16f5")
Daze = ("Daze","3ef51126-e2c0-44b3-b781-0b3f8476cb20")
DeflectR = ("Deflect Ready", "684fcda0-e69d-426e-861c-5a92bc984f55")
DeflectU = ("Deflect Used", "2c5b85ea-93de-4a99-b64d-da6c48baa205")
Guard = ("Guard", "91ed27dc-294d-4732-ab71-37911f4011f2" )
HolyAvenger = ("Holy Avenger", "99381ac8-7d73-4d75-9787-60e6411d3613" )
Invisible = ("Invisible", "8d994fe9-2422-4a9d-963d-3ad10b2b823d")
Pet = ("Pet", "f4a2d3d3-4a95-4b9a-b899-81ea58293167")
Quick = ("Quick", "11370fe9-41a4-4f05-9249-29a179c0031b")
QuickBack = ("Quick Back", "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd")
Ready = ("Ready", "aaea8e90-e9c5-4fbc-8de3-4bf651d784a7" )
ReadyII = ("Ready II", "73fffebd-a8f0-43bd-a118-6aebc366ecf6" )
Rot = ("Rot", "81360faf-87d6-42a8-a719-c49386bd2ab5" )
Slam = ("Slam", "f7379e4e-8120-4f1f-b734-51f1bd9fbab9" )
Sleep = ("Sleep", "ad0e8e3c-c1af-47b7-866d-427f8908dea4" )
Stun = ("Stun", "4bbac09e-a46c-42de-9272-422e8074533f" )
Taunt = ("Taunt(Sosroku)", "16f03c44-5656-4e9d-9629-90c4ff1765a7" )
TauntT = ("Taunt(Thorg)", "8b5e3fe0-7cb1-44cd-9e9c-dadadbf04ab7" )
Turn = ("Turn", "e0a54bea-6e30-409d-82cd-44a944e591dc")
Used = ("Used", "ab8708ac-9735-4803-ba4d-4932a787540d" )
UsedII = ("Used II", "61bec951-ebb1-48f7-a2ab-0b6364d262e6" )
Veteran = ("Veteran", "72ee460f-adc1-41ab-9231-765001f9e08e" )
Visible = ("Visible", "b9b205a2-a998-44f5-97dc-c7f315afbbe2")
VoltaricON = ("Voltaric ON", "a6e79926-db8d-4095-9aee-e3b46bf24a3f" )
VoltaricOFF = ("Voltaric OFF", "d91aabe0-d9cd-4b7e-b994-4e1c7a51c027")
Weak = ("Weak", "22ef0c9e-6c0b-4e24-a4fa-e9d83f24fcba" )
WoundedPrey = ("Wounded Prey", "42f6cee3-3de4-4c90-a77c-9fb2c432d78d" )
Growth = ("Growth", "c580e015-96ff-4b8c-8905-28688bcd70e8")
Corrode= ("Corrode", "c3de25bf-4845-4d2d-8a28-6c31ad12af46")
Ichthellid = ("Ichthellid Larva", "c8bff05e-e43a-4b23-b467-9c4596050f28")
Zombie = ("Zombie", "de101060-a4b4-4387-a7f8-aab82ecff2c8")
Treebond = ("Treebond", "ced2ce11-5e69-46a9-9fbb-887e96bdf805")
Eternal_Servant = ("Eternal Servant", "86a71cf6-35ce-4728-a2f8-6701b1e29aa4")
EggToken = ("Egg Token","874c7fbb-c566-4f17-b14e-ae367716dce5")
LoadToken = ("Load Token","d32267be-f4c5-48c6-8396-83c0db406942")
MistToken = ("Mist Token","fcc2ffeb-6ae6-45c8-930e-8f3521d326eb")
DissipateToken = ("Dissipate Token","96348698-ae05-4c59-89bb-e79dad50ad1f")
RuneofFortification = ("Rune of Fortification","ae179c85-11ce-4be7-b9c9-352139d0c8f2")
RuneofPower = ("Rune of Power","b3dd4c8e-35a9-407f-b9c8-a0b0ff1d3f07")
RuneofPrecision = ("Rune of Precision","c2a265f9-ad97-4976-a83c-78891a224478")
RuneofReforging = ("Rune of Reforging","d10ada1f-c03b-4077-b6cb-c9667d6b2744")
RuneofShielding = ("Rune of Shielding","e0bb0e90-4831-43c6-966e-27c8dc2d2eef")
Disable = ("Disable","f68b3b5b-0755-40f4-84db-bf3197a667cb")

##########################		Dice-related			########################

Die = [ "DieBlank",
		"DieBlank",
		"Die1",
		"Die2",
		"Die1s",
		"Die2s"]
attackDie = [ ("DieBlank","a1f061ec-efbe-444e-8e06-8d973600696c"),
		("DieBlank","a1f061ec-efbe-444e-8e06-8d973600696c"),
		("Die1","8cc1704a-6f2f-4dbf-a80c-8f79a5a8d165"),
		("Die2","b881f652-9384-43e1-9758-e68b04583b3b"),
		("Die1s","a3d3fff3-bb1c-4469-9a9d-f8dc1f341d39"),
		("Die2s","101976ea-ec22-4496-a762-6fbc0d1a41bb"),
		]
DieBlank = ("DieBlank","a1f061ec-efbe-444e-8e06-8d973600696c")
Die1 = ("Die1","8cc1704a-6f2f-4dbf-a80c-8f79a5a8d165")
Die2 = ("Die2","b881f652-9384-43e1-9758-e68b04583b3b")
Die1s = ("Die1s","a3d3fff3-bb1c-4469-9a9d-f8dc1f341d39")
Die2s = ("Die2s","101976ea-ec22-4496-a762-6fbc0d1a41bb")
DieD12 = ("DieD12","3cdf4231-065d-400e-9c74-d0ae669e852c")
diceBank = [1]
diceBankD12 = [0]

##########################		Other			############################

PlayerColor = 	["#de2827", 	# Red 		R=222 G=40  B=39
				"#171e78", 		# Blue		R=23  G=30  B=120
				"#01603e", 		# Green		R=1   G=96  B=62
				"#f7d917"] 		# Yellow 	R=247 G=217 B=23
mycolor = "#800080" # Purple
boardSet = "GameBoard1.png"
debugMode = False
myIniRoll = 0
hasRolledIni = True
deckLoaded = False
discountsUsed = [ ]
roundTimes = []
turn = 0
playerNum = 0
ver = "1.6.5.0"

############################################################################
############################		Events		############################
############################################################################

def onTableLoad():
	global debugMode
	sayVer()
	gameStartTime = time.time()
	#if there's only one player, go into debug mode
	if len(players) == 1:
		debugMode = True
		notify("Enabling debug mode. In debug mode, deck validation is turned off and you can advance to the next phase by yourself.")

def onGameStart():
# reset color picking
	setGlobalVariable("ColorsChosen", "")

#	reset initiative automation
	setGlobalVariable("SetupDone", "")
	setGlobalVariable("OppIniRoll", "")
	setGlobalVariable("IniAllDone", "")

# set Dice Rolling Area, Initative, and Phase Marker Card location 
	setDRAIP()

def onLoadDeck(player, groups):
	mute()
	global deckLoaded
	global debugMode
	global playerNum
	if player == me:
		if debugMode or validateDeck(groups[0]):
			deckLoaded = True
			playerSetup()
			if debugMode:
				mycolor = PlayerColor[0]
				CreateIniToken()
			if getGlobalVariable("SetupDone") == "": #we're the first done with setup
				playerNum = 1
				setGlobalVariable("SetupDone", "x")
			else:	#other guy is done too
				playerNum = 2
				for p in players:
					remoteCall(p, "SetupForIni", [])
				notify("Both players have set up. Please roll for initiative.")
		else:
			#notify and delete deck
			notify("Validation of {}'s spellbook FAILED. Please choose another spellbook.".format(me.name))
			for group in groups:
				for card in group:
					if card.controller == me:
						card.delete()
			#if a deck was already loaded, clear player's chosen color
			if deckLoaded:
				deckLoaded = False
				colorsChosen = getGlobalVariable("ColorsChosen")
				colorChoice = PlayerColor.index(mycolor)
				colorsChosen = colorsChosen.replace(str(colorChoice), '')
				setGlobalVariable("ColorsChosen", colorsChosen)

def SetupForIni():
	mute()
	global hasRolledIni
	global playerNum
	hasRolledIni = False

	if getSetting("AutoRollIni", False):
		effect = 0
		for i in range(playerNum * 2):
			effect = rnd(1, 12)
		notify("Automatically rolling initiative for {}...".format(me))
		hasRolledIni = True
		iniRoll(effect)

def iniRoll(effect):
	notify("{} rolled a {} for initiative".format(me, effect))
	oppRollStr = getGlobalVariable("OppIniRoll")
	oppRoll = 0
	if oppRollStr != "":
		oppRoll = eval(oppRollStr)

	if oppRoll == 0:	#they haven't rolled yet
		setGlobalVariable("OppIniRoll", str(effect))
	elif oppRoll == effect:	#tie!
		notify("Tied initiative roll! Please roll again.")
		for p in players:
			remoteCall(p, "SetupForIni", [])
		setGlobalVariable("OppIniRoll", "0")
	elif effect > oppRoll:	#we won
		AskInitiative()
	else:	#they won
		remoteCall(players[1], "AskInitiative", [])
		
def setDRAIP():
	global dieCardX
	global dieCardY
	global dieCard2X
	global dieCard2Y		
	global phaseX
	global phaseY
	global initX
	global initY
	
	if not getSetting("AutoConfigDRAIP", True):
		#option A
		dieCardX = -570
		dieCardY = -40
		dieCard2X = -510
		dieCard2Y = -40
		phaseX = -510
		phaseY = -150 
		initX = -580
		initY = -150
	else:	
		#option B
		dieCardX = -58
		dieCardY = 330
		dieCard2X = 0 
		dieCard2Y = 330
		phaseX = 65
		phaseY = 330
		initX = -125
		initY = 330		

############################################################################
######################		Group Actions			########################
############################################################################

def playerDone(group, x=0, y=0):
	notify("{} is done".format(me.name))

def rollDice(group, x=0, y=0):
	mute()
	global diceBank
	global diceBankD12
	global hasRolledIni
	global myIniRoll

	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me:
			c.delete()
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
	dieCard2 = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCard2X, dieCard2Y) #dice field 2

	count = min(askInteger("Roll how many red dice?", 3),50) #max 50 dice rolled at once
	if count == None: return

	diceFrom = ""
	if (len(diceBank) < count): #diceBank running low - fetch more
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code for damage dice roll: {}".format(random_org[1]))
		if random_org[1]==200: # OK code received:
			diceBank = random_org[0].splitlines()
			diceFrom = "from Random.org"
		else:
#			notify("www.random.org not responding (code:{}). Using built-in randomizer".format(random_org[1]))
			diceFrom = "from the native randomizer"
			while (len(diceBank) < 20):
				diceBank.append(rnd(0, 5))

	result = [0,0,0,0,0,0]
	for x in range(count):
		roll = int(diceBank.pop())
		result[roll] += 1
	debug("diceRoller result: {}".format(result))
	notify("{} rolls {} attack dice {}".format(me,count,diceFrom))

	damPiercing = result[4] + 2* result[5]
	damNormal = result[2] + 2* result[3]
	dieCard.markers[attackDie[0]] = result[0]+result[1] #blanks
	dieCard.markers[attackDie[2]] = result[2] #1
	dieCard.markers[attackDie[3]] = result[3] #2
	dieCard2.markers[attackDie[4]] = result[4] #1*
	dieCard2.markers[attackDie[5]] = result[5] #2*

	d12DiceCount = 1
	if (len(diceBankD12) < d12DiceCount): #diceBank running low - fetch more
		d12 = webRead("http://www.random.org/integers/?num=100&min=0&max=11&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code for effect roll: {}".format(d12[1]))
		if d12[1]==200: # OK code received:
			diceBankD12 = d12[0].splitlines()
			notify ("Using die from Random.org")
		else:
			notify ("Using die from the native randomizer")
			while (len(diceBankD12) < 100):
				diceBankD12.append(rnd(1, 12))
	
	effect = int(diceBankD12.pop()) + 1
	dieCard2.markers[DieD12] = effect

	if hasRolledIni:
		notify("{} rolled {} normal damage, {} critical damage, and {} on the effect die".format(me,damNormal,damPiercing,effect))
	else:
		hasRolledIni = True
		iniRoll(effect)

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def playerSetup():
	mute()

	# Players select their color
	global mycolor
	choiceList = ["Red", "Blue", "Green", "Yellow"]
	while (True):
		choice = askChoice("Pick a color:", choiceList, PlayerColor) - 1
		colorsChosen = getGlobalVariable("ColorsChosen")
		if colorsChosen == "":	#we're the first to pick
			setGlobalVariable("ColorsChosen", str(choice))
			mycolor = PlayerColor[choice]
			break
		elif str(choice) not in colorsChosen:	#not first to pick but no one else has taken this yet
			setGlobalVariable("ColorsChosen", colorsChosen + str(choice))
			mycolor = PlayerColor[choice]
			break
		else:	#someone else took our choice
			askChoice("Someone else took that color. Choose a different one.", ["OK"], ["#FF0000"])

	#set initial health and channeling values
	for c in me.hand:
		if c.Type == "Mage":
			stats = c.Stats.split(",")
			break
	for stat in stats:
		debug("stat {}".format(stat))
		statval = stat.split("=")
		if "Channeling" in statval[0]:
			me.Channeling = int(statval[1])
			me.Mana = 10+me.Channeling
			whisper("Channeling set to {} and Mana to {}".format(me.Channeling,me.Mana))
		elif "Life" in statval[0]:
			me.Life = int(statval[1])
			whisper("Life set to {}".format(me.Life))

def createVineMarker(group, x=0, y=0):
	table.create("ed8ec185-6cb2-424f-a46e-7fd7be2bc1e0", 450, -40 )

def createAltBoardCard(group, x=0, y=0):
	table.create("af14ca09-a83d-4185-afa0-bc38a31dbf82", 450, -40 )

def setNoGameBoard(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard0.png"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard1(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard1.png"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard2(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard2.png"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard3(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard3.png"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard4(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard4.png"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])
		
def setGameBoard5(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard5.png"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])


def sayVer():
	notify("{} is running v.{} of the Mage Wars module.".format(me, ver))

def setGameBoard(bset):
	mute()
	global boardSet
	boardSet = bset
	table.setBoardImage("GameBoards\\{}".format(boardSet))

def AskInitiative():
	mute()
	notify("{} is choosing whether or not to go first.".format(me))
	choiceList = ['Yes', 'No']
	colorsList = ['#FF0000', '#0000FF']
	choice = askChoice("You have won initiative! Would you like to go first?", choiceList, colorsList)
	if choice == 1:
		notify("{} has elected to go first!".format(me))
		CreateIniToken()
	else:
		notify("{} has elected NOT to go first! {} has first initiative.".format(me, players[1]))
		remoteCall(players[1], "CreateIniToken", [])

def CreateIniToken():
	mute()
	card = table.create("6a71e6e9-83fa-4604-9ff7-23c14bf75d48", phaseX, phaseY ) #phase token
	card.switchTo("Planning") #skips upkeep for first turn
	init = table.create("8ad1880e-afee-49fe-a9ef-b0c17aefac3f", initX, initY ) #initiative token
	if mycolor == PlayerColor[0]:
		init.switchTo("")
	elif mycolor == PlayerColor[1]:
		init.switchTo("B")
	elif mycolor == PlayerColor[2]:
		init.switchTo("C")
	elif mycolor == PlayerColor[3]:
		init.switchTo("D")
	setGlobalVariable("IniAllDone", "x")
	setGlobalVariable("RoundNumber", "1")
	notify("Setup is complete!")

def nextPhase(group, x=-360, y=-150):
	global mycolor
	global roundTimes
	if getGlobalVariable("IniAllDone") == "": # Player setup is not done yet.
		return
	mute()
	card = None
	for c in table: #find phase card
		if c.model == "6a71e6e9-83fa-4604-9ff7-23c14bf75d48":
			card = c
			break
	if card.alternate == "":
		switchPhase(card,"Planning","Planning Phase")
	elif card.alternate == "Planning":
		switchPhase(card,"Deploy","Deploy Phase")
	elif card.alternate == "Deploy":
		switchPhase(card,"Quick","First Quickcast Phase")
	elif card.alternate == "Quick":
		switchPhase(card,"Actions","Actions Phase")
	elif card.alternate == "Actions":
		switchPhase(card,"Quick2","Final Quickcast Phase")
	elif card.alternate == "Quick2":
		if switchPhase(card,"","Upkeep Phase") == True: #Back to Upkeep
			for p in players:
				remoteCall(p,"resetDiscounts",[])
			turn = int(getGlobalVariable("RoundNumber")) + 1
			setGlobalVariable("RoundNumber", str(turn))
			rTime = time.time()
			roundTimes.append(rTime)
			notify("Round {} Start Time: {}".format(time.ctime(roundTimes[-1])))
			notify("Ready Stage for Round #" + str(turn) + ":  Performing Initiative, Reset, and Channeling Phases")
			init = [card for card in table if card.model == "8ad1880e-afee-49fe-a9ef-b0c17aefac3f"][0]
			if init.controller == me:
				flipcard(init)
			else:
				remoteCall(init.controller, "flipcard", [init])
			for p in players:
				p.Mana += p.Channeling
				notify("{} channels {}".format(p.name,p.Channeling))
			for c in table:
				if c.isFaceUp: #don't waste time on facedown cards
					#reset markers
					if c.controller == me:
						resetMarkers(c)
					else:
						remoteCall(players[1], "resetMarkers", [c])
					#resolve channeling cards (harmonize, spawnpoints, familiars)
					if c.controller == me:
						resolveChanneling(c)
					else:
						remoteCall(players[1], "resolveChanneling", [c])
			#resolve other autometed items
			for p in players:
				remoteCall(p, "resolveBurns", [])
				remoteCall(p, "resolveRot", [])
				remoteCall(p, "resolveDissipate", [])
#				remoteCall(p, "resolveLoadTokens", [])

	update() #attempt to resolve phase indicator sometimes not switching

def resetDiscounts():
	#reset discounts used
	for tup in discountsUsed:
		discountsUsed.remove(tup)
		discountsUsed.append((tup[0],tup[1],0))

def resetMarkers(c):
	mute()
	if c.markers[ActionRedUsed] == 1:
		c.markers[ActionRedUsed] = 0
		c.markers[ActionRed] = 1
	if c.markers[ActionBlueUsed] == 1:
		c.markers[ActionBlueUsed] = 0
		c.markers[ActionBlue] = 1
	if c.markers[ActionGreenUsed] == 1:
		c.markers[ActionGreenUsed] = 0
		c.markers[ActionGreen] = 1
	if c.markers[ActionYellowUsed] == 1:
		c.markers[ActionYellowUsed] = 0
		c.markers[ActionYellow] = 1
	if c.markers[QuickBack] == 1:
		c.markers[QuickBack] = 0
		c.markers[Quick] = 1
	if c.markers[Used] == 1:
		c.markers[Used] = 0
		c.markers[Ready] = 1
	if c.markers[UsedII] == 1:
		c.markers[UsedII] = 0
		c.markers[ReadyII] = 1
	if c.markers[VoltaricON] == 1:
		c.markers[VoltaricON] = 0
		c.markers[VoltaricOFF] = 1
	if c.markers[DeflectU] == 1:
		c.markers[DeflectU] = 0
		c.markers[DeflectR] = 1
	if c.markers[Visible] == 1:
		c.markers[Visible] = 0
		c.markers[Invisible] = 1
	debug("card,stats,subtype {} {} {}".format(c.name,c.Stats,c.Subtype))

def resolveBurns():
	mute()

	#is the setting on?
	if not getSetting("AutoResolveBurns", True):
		return

	cardsWithBurn = [c for c in table if c.markers[Burn] and c.controller == me]
	if len(cardsWithBurn) > 0:
		notify("Resolving Burns for {}...".format(me))	#found at least one
		for card in cardsWithBurn:
			numMarkers = card.markers[Burn]
			burnDamage = 0
			burnsRemoved = 0
			for i in range(0, numMarkers):
				roll = rnd(0, 2)
				if roll == 0:
					card.markers[Burn] -= 1
					burnsRemoved += 1
				elif roll == 1:
					burnDamage += 1
				elif roll == 2:
					burnDamage += 2
			#apply damage
			if card.Type == "Mage":
				card.controller.Damage += burnDamage
			elif card.Type == "Creature" or "Conjuration" in card.Type:
				card.markers[Damage] += burnDamage
			notify("{} damage added to {}. {} Burns removed.".format(burnDamage, card.Name, burnsRemoved))
		notify("Finished auto-resolving Burns for {}.".format(me))

def resolveRot():
	mute()

	#is the setting on?
	if not getSetting("AutoResolveRot", True):
		return

	cardsWithRot = [c for c in table if c.markers[Rot] and c.controller == me]
	if len(cardsWithRot) > 0:
		notify("Resolving Rot for {}...".format(me))	#found at least one
		for card in cardsWithRot:
			rotDamage = (card.markers[Rot])
			 #apply damage
			if card.Type == "Mage":
				card.controller.Damage += rotDamage
			elif card.Type == "Creature" or "Conjuration" in card.Type:
				card.markers[Damage] += rotDamage
			notify("{} damage added to {}.".format(rotDamage, card.Name))
		notify("Finished auto-resolving Rot for {}.".format(me))

def resolveDissipate():
	mute()

#is the setting on?
	if not getSetting("AutoResolveDissipate", True):
		return

	cardsWithDissipate = [c for c in table if c.markers[DissipateToken] and c.controller == me]
	if len(cardsWithDissipate) > 0:
		notify("Resolving Dissipate for {}...".format(me))	#found at least one
		for card in cardsWithDissipate:
			notify("Removing 1 Dissipate Token from {}...".format(card.Name))
			card.markers[DissipateToken] -= 1 # Remove Token
			if card.markers[DissipateToken] == 0 and card.Name == "Rolling Fog": # Only discard Rolling Fog for now
				notify("{} discards {} as it no longer has Dissipate Tokens".format(me, card.Name))
				card.moveTo(me.piles['Discard'])
			notify("Finished auto-resolving Dissipate for {}.".format(me))

def resolveChanneling(c):
	mute()
	if c.Stats != None and c.Type != "Mage":
		if "Channeling=" in c.Stats: #let's add mana for spawnpoints etc.
			channel = getStat(c.Stats,"Channeling")
			debug("Found Channeling stat {} in card {}".format(channel,c.name))
			for x in range(channel):
				addMana(c)
	if c.name == "Barracks": #has the channeling=X stat
		debug("Found Barracks")
		x = 0
		for c2 in table:
			if c2.isFaceUp and c2.Subtype != "" and c2.Subtype != None:
				#debug("owners {} {}".format(c.owner,c2.owner))
				if "Outpost" in c2.Subtype and c.owner == c2.owner:
					debug("Found Outpost")
					addMana(c)
					x += 1
			if x == 3: #max 3 outpost count.
				break
	if c.name == "Harmonize":
		c2 = cardHere(cardX(c)-1,cardY(c)-1,"Channeling=")
		if c2 != None and c2.Type != "Mage":
			debug("Overlap found (top left) {}".format(c2.name))
			addMana(c2)
			whisper("Harmonize found and Mana added to channeling card")
		else:
			c2 = cardHere(cardX(c)+c.width()+1,cardY(c)+c.height()+1,"Channeling=")
			if c2 != None and c2.Type !="Mage":
				debug("Overlap found (bottom right) {}".format(c2.name))
				addMana(c2)
				whisper("Harmonize found and Mana added to channeling card")
			else:
				c2 = cardHere(cardX(c)-1,cardY(c)+c.height(),"Channeling=")
				if c2 != None and c2.Type !="Mage":
					debug("Overlap found (bottom left) {}".format(c2.name))
					addMana(c2)
					whisper("Harmonize found and Mana added to channeling card")
				else:
					c2 = cardHere(cardX(c)+c.width()+1,cardY(c),"Channeling=")
					if c2 != None and c2.Type !="Mage":
						debug("Overlap found (top right) {}".format(c2.name))
						addMana(c2)
						whisper("Harmonize found and Mana added to channeling card")
					else:
						whisper("Harmonize found but no Mana added")


def toggleDebug(group, x=0, y=0):
	global debugMode
	debugMode = not debugMode
	if debugMode:
		notify("{} turns on debug".format(me))
	else:
		notify("{} turns off debug".format(me))

def toggleResolveBurns(group, x=0, y=0):
	autoResolveBurns = getSetting("AutoResolveBurns", True)
	setSetting("AutoResolveBurns", not autoResolveBurns)
	if autoResolveBurns:
		whisper("You have disabled automatic resolution of Burn tokens on your cards.")
	else:
		whisper("You have enabled automatic resolution of Burn tokens on your cards.")
		
def toggleConfigDRAIP(group, x=0, y=0):
	AutoConfigDRAIP = getSetting("AutoConfigDRAIP", True)
	setSetting("AutoConfigDRAIP", not AutoConfigDRAIP)
	if AutoConfigDRAIP:
		notify("Player 1 has configured the Dice Rolling Area, Initative, and Phase markers positions to the Left of the Board.")
	else:
		notify("Player 1 has configured the Dice Rolling Area, Initative, and Phase markers positions to the to the Bottom of the Board.")

		
def toggleResolveRot(group, x=0, y=0):
	autoResolveRot = getSetting("AutoResolveRot", True)
	setSetting("AutoResolveRot", not autoResolveRot)
	if autoResolveRot:
		whisper("You have disabled automatic resolution of Rot tokens on your cards.")
	else:
		whisper("You have enabled automatic resolution of Rot tokens on your cards.")
		
def toggleResolveDissipate(group, x=0, y=0):
	autoResolveDissipate = getSetting("AutoResolveDissipate", True)
	setSetting("AutoResolveDissipate", not autoResolveDissipate)
	if autoResolveDissipate:
		whisper("You have disabled automatic resolution of Dissipate tokens on your cards.")
	else:
		whisper("You have enabled automatic resolution of Dissipate tokens on your cards.")

def toggleEnchantRevealPrompt(group, x=0, y=0):
	prompt = getSetting("EnchantPromptReveal", False)
	setSetting("EnchantPromptReveal", not prompt)
	if prompt:
		whisper("You have disabled the enchantment reveal prompt.")
	else:
		whisper("You have enabled the enchantment reveal prompt.")

def toggleAutoRollInitiative(group, x=0, y=0):
	autoRoll = getSetting("AutoRollIni", False)
	setSetting("AutoRollIni", not autoRoll)
	if autoRoll:
		whisper("You have disabled automatically rolling initiative.")
	else:
		whisper("You have enabled automatically rolling initiative.")

def concede(group=table,x=0,y=0):
	mute()
	if confirm("Are you sure you want to concede this game?"):
		gameEndTime = time.time()
#		reportGame('Conceded')
		notify("{} has conceded the game".format(me))
	else:
		notify("{} was about to concede the game, but thought better of it...".format(me))

############################################################################
######################		Chat Actions			################################
############################################################################
def sayYes(group, x=0, y=0):
	notify("{} says Yes".format(me.name))

def sayNo(group, x=0, y=0):
	notify("{} says No".format(me.name))

def sayPass(group, x=0, y=0):
	notify("{} says Pass".format(me.name))

def sayThinking(group, x=0, y=0):
	notify("{} says I am thinking....".format(me.name))

def askThinking(group, x=0, y=0):
	notify("{} are you thinking?".format(me.name))

def askYourTurn(group, x=0, y=0):
	notify("{} asks is it your turn?".format(me.name))

def askMyTurn(group, x=0, y=0):
	notify("{} asks is it my turn?".format(me.name))

def askRevealEnchant(group, x=0, y=0):
	notify("{} asks do you wish to Reveal your Enchantment?".format(me.name))

############################################################################
######################		Card Actions			################################
############################################################################

##########################     Add Tokens     ##############################

def addDamage(card, x = 0, y = 0):
    addToken(card, Damage)

def addBurn(card, x = 0, y = 0):
	addToken(card, Burn)

def addCripple(card, x = 0, y = 0):
    addToken(card, Cripple)

def addCorrode(card, x = 0, y = 0):
    addToken(card, Corrode)

def addRot(card, x = 0, y = 0):
    addToken(card, Rot)

def addDisable(card, x = 0, y = 0):
    addToken(card, Disable)

def addDaze(card, x=0, y=0):
	addToken(card, Daze)

def addMana(card, x = 0, y = 0):
	addToken(card, Mana)

def addStun(card, x=0, y=0):
	addToken(card, Stun)

def addSlam(card, x=0, y=0):
	addToken(card, Slam)

def addWeak(card, x=0, y=0):
	addToken(card, Weak)

def addOther(card, x = 0, y = 0):
	marker, qty = askMarker()
	if qty == 0: return
	card.markers[marker] += qty

##########################     Toggle Actions/Tokens     ##############################

def toggleAction(card, x=0, y=0):
	global mycolor
	mute()
	if mycolor == "#800080":
		whisper("Please perform player setup to initialize player color")
	elif mycolor == PlayerColor[0]: # Red
		if card.markers[ActionRedUsed] > 0:
			card.markers[ActionRed] = 1
			card.markers[ActionRedUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionRed] = 0
			card.markers[ActionRedUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[1]: # Blue
		if card.markers[ActionBlueUsed] > 0:
			card.markers[ActionBlue] = 1
			card.markers[ActionBlueUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionBlue] = 0
			card.markers[ActionBlueUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[2]: #Green
		if card.markers[ActionGreenUsed] > 0:
			card.markers[ActionGreen] = 1
			card.markers[ActionGreenUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionGreen] = 0
			card.markers[ActionGreenUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[3]: #Yellow
		if card.markers[ActionYellowUsed] > 0:
			card.markers[ActionYellow] = 1
			card.markers[ActionYellowUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionYellow] = 0
			card.markers[ActionYellowUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))

def toggleBloodReaper(card, x=0, y=0):
	toggleToken(card, BloodReaper)

def toggleDeflect(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[DeflectR] > 0:
		card.markers[DeflectR] = 0
		card.markers[DeflectU] = 1
		notify("'{}' uses deflect".format(card.Name))
	else:
		card.markers[DeflectR] = 1
		card.markers[DeflectU] = 0
		notify("'{}' readies deflect".format(card.Name))

def toggleGuard(card, x=0, y=0):
	toggleToken(card, Guard)

def toggleInvisible(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[Invisible] > 0:
		card.markers[Invisible] = 0
		card.markers[Visible] = 1
		notify("'{}' becomes visible".format(card.Name))
	else:
		card.markers[Invisible] = 1
		card.markers[Visible] = 0
		notify("'{}' becomes invisible".format(card.Name))

def toggleReady(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[Ready] > 0:
		card.markers[Ready] = 0
		card.markers[Used] = 1
		notify("'{}' spends the Ready Marker on '{}'".format(me, card.Name))
	else:
		card.markers[Ready] = 1
		card.markers[Used] = 0
		notify("'{}' readies the Ready Marker on '{}'".format(me, card.Name))

def toggleReadyII(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[ReadyII] > 0:
		card.markers[ReadyII] = 0
		card.markers[UsedII] = 1
		notify("'{}' spends the Ready Marker II on '{}'".format(me, card.Name))
	else:
		card.markers[ReadyII] = 1
		card.markers[UsedII] = 0
		notify("'{}' readies the Ready Marker II on '{}'".format(me, card.Name))

def togglePet(card, x=0, y=0):
	toggleToken(card, Pet)

def toggleTaunt(card, x=0, y=0):
	toggleToken(card, Taunt)

def toggleTauntT(card, x=0, y=0):
	toggleToken(card, TauntT)

def toggleQuick(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[Quick] > 0:
		card.markers[Quick] = 0
		card.markers[QuickBack] = 1
		notify("'{}' spends Quick Cast action".format(card.Name))
	else:
		card.markers[Quick] = 1
		card.markers[QuickBack] = 0
		notify("'{}' readies Quick Cast action".format(card.Name))

def toggleVoltaric(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[VoltaricON] > 0:
		card.markers[VoltaricON] = 0
		card.markers[VoltaricOFF] = 1
		notify("'{}' disables Voltaric shield".format(card.Name))
	else:
		card.markers[VoltaricON] = 1
		card.markers[VoltaricOFF] = 0
		notify("'{}' enables Voltaric shield".format(card.Name))

######################     Remove Tokens     ###########################

def subDamage(card, x = 0, y = 0):
    subToken(card, Damage)

def subBurn(card, x = 0, y = 0):
    subToken(card, Burn)

def subCripple(card, x = 0, y = 0):
    subToken(card, Cripple)

def subCorrode(card, x = 0, y = 0):
    subToken(card, Corrode)

def subDaze(card, x = 0, y = 0):
    subToken(card, Daze)

def subMana(card, x = 0, y = 0):
    subToken(card, Mana)

def subStun(card, x = 0, y = 0):
    subToken(card, Stun)

def subSlam(card, x = 0, y = 0):
	subToken(card, Slam)

def subWeak(card, x = 0, y = 0):
    subToken(card, Weak)

def subRot(card, x = 0, y = 0):
    subToken(card, Rot)

def subDisable(card, x = 0, y = 0):
    subToken(card, Disable)

def clearTokens(card, x = 0, y = 0):
	mute()
	for tokenType in card.markers:
		card.markers[tokenType] = 0
	notify("{} removes all tokens from '{}'".format(me, card.Name))




############################################################################
######################		Other  Actions		################################
############################################################################

def rotateCard(card, x = 0, y = 0):
	# Rot90, Rot180, etc. are just aliases for the numbers 0-3
	mute()
	if card.controller == me:
		card.orientation = (card.orientation + 1) % 4
		if card.isFaceUp:
			notify("{} Rotates '{}'".format(me, card.Name))
		else:
			notify("{} Rotates a card".format(me))

def flipcard(card, x = 0, y = 0):
	mute()
	if "Vine" in card.name and card.controller == me:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")
		notify("{} Flips Vine Marker.".format(me))
	elif "Alt Zone" in card.name and card.controller == me:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")
		notify("{} Flips Zone Marker.".format(me))
	elif card.isFaceUp == False:
		card.isFaceUp = True
		notify("{} turns '{}' face up.".format(me, card.Name))
		if card.Type != "Enchantment"  and "Conjuration" not in card.Type: #leaves the highlight around Enchantments and Conjurations
			card.highlight = None
		if card.Type == "Mage" or card.Type == "Creature": #places action marker on card
			toggleAction(card)
		if card.Type == "Mage": #once more to flip action to active side
			toggleAction(card)
			toggleQuick(card)
			if "Wizard" in card.name:
					card.markers[VoltaricOFF] = 1
			if "Forcemaster" == card.name:
					card.markers[DeflectR] = 1
			if "Beastmaster" == card.name:
					card.markers[Pet] = 1
			if "Beastmaster (Johktari)" == card.name:
					card.markers[WoundedPrey] = 1
			if "Priest" == card.name:
					card.markers[HolyAvenger] = 1
			if "Druid" == card.name:
					card.markers[Treebond] = 1
			if "Necromancer" == card.name:
					card.markers[Eternal_Servant] = 1
		if card.Type == "Creature":
			if "Invisible Stalker" == card.name:
					card.markers[Invisible] = 1
			if "Thorg, Chief Bodyguard" == card.name:
					card.markers[TauntT] = 1
			if "Sosruko, Ferret Companion" == card.name:
					card.markers[Taunt] = 1
			if "Ichthellid" == card.name:
					card.markers[EggToken] = 1
		if card.Type == "Conjuration":
			if "Ballista" == card.name:
  				card.markers[LoadToken] = 1
			if "Akiro's Hammer" == card.name:
  				card.markers[LoadToken] = 1
			if "Corrosive Orchid" == card.name:
  				card.markers[MistToken] = 1
			if "Nightshade Lotus" == card.name:
  				card.markers[MistToken] = 1
			if "Rolling Fog" == card.name:
  				card.markers[DissipateToken] = 3 
		if "Defense" in card.Stats:
			if "1x" in card.Stats:
				card.markers[Ready] = 1
			if "2x" in card.Stats:
				card.markers[Ready] = 1
				card.markers[ReadyII] = 1
		if "[ReadyMarker]" in card.Text:
			card.markers[Ready] = 1
  	elif card.alternates is not None and "B" in card.alternates: #flip the initiative card
		colorsChosen = getGlobalVariable("ColorsChosen")
		if "0" in colorsChosen and "1" in colorsChosen: #red and blue
			if card.alternate == "B":
				card.switchTo("")
			else:
				card.switchTo("B")
		elif "0" in colorsChosen and "2" in colorsChosen: #red and green
			if card.alternate == "C":
				card.switchTo("")
			else:
				card.switchTo("C")
		elif "0" in colorsChosen and "3" in colorsChosen: #red and yellow
			if card.alternate == "D":
				card.switchTo("")
			else:
				card.switchTo("D")
		elif "1" in colorsChosen and "2" in colorsChosen: #blue and green
			if card.alternate == "C":
				card.switchTo("B")
			else:
				card.switchTo("C")
		elif "1" in colorsChosen and "3" in colorsChosen: #blue and yellow
			if card.alternate == "D":
				card.switchTo("B")
			else:
				card.switchTo("D")
		elif "2" in colorsChosen and "3" in colorsChosen: #green and yellow
			if card.alternate == "D":
				card.switchTo("C")
			else:
				card.switchTo("D")
		#notify("{} turns '{}' face up.".format(me, card.Name))
	elif card.isFaceUp:
		notify("{} turns '{}' face down.".format(me, card.Name))
		card.isFaceUp = False
		card.peek()

def discard(card, x=0, y=0):
	mute()
	if card.controller != me:
		whisper("{} does not control '{}' - discard cancelled".format(me, card))
		return
	card.isFaceUp = True

	card.moveTo(me.piles['Discard'])
	notify("{} discards '{}'".format(me, card))

def obliterate(card, x=0, y=0):
	mute()
	if card.controller != me:
		whisper("{} does not control '{}' - card obliteration cancelled".format(me, card))
		return
	card.isFaceUp = True

	card.moveTo(me.piles['Obliterate Pile'])
	notify("{} obliterates '{}'".format(me, card))

def defaultAction(card, x = 0, y = 0):
	mute()
	if card.controller == me:
		if not card.isFaceUp:
			#is this a face-down enchantment? if so, prompt before revealing
			if card.Type == "Enchantment":
				if getSetting("EnchantPromptReveal", False):
					choiceList = ['Yes', 'No']
					colorsList = ['#0000FF', '#FF0000']
					choice = askChoice("Would you like to reveal this hidden enchantment?", choiceList, colorsList)
					if choice == 0 or choice == 2:
						return

			flipcard(card, x, y)
			castSpell(card, x, y)
		else:
			castSpell(card, x, y)


############################################################################
######################		Utility Functions		########################
############################################################################

def addToken(card, tokenType):
	mute()
	card.markers[tokenType] += 1
	if card.isFaceUp:
		notify("{} added to '{}'".format(tokenType[0], card.Name))
	else:
		notify("{} added to face-down card.".format(tokenType[0]))

def subToken(card, tokenType):
	mute()
	card.markers[tokenType] -= 1
	if card.isFaceUp:
		notify("{} removed from '{}'".format(tokenType[0], card.Name))
	else:
		notify("{} removed from face-down card.".format(tokenType[0]))

def toggleToken(card, tokenType):
	mute()
	if card.markers[tokenType] > 0:
		card.markers[tokenType] = 0
		if card.isFaceUp:
			notify("{} removes a {} from '{}'".format(me, tokenType[0], card.Name))
		else:
			notify("{} removed from face-down card.".format(tokenType[0]))
	else:
		card.markers[tokenType] = 1
		if card.isFaceUp:
			notify("{} adds a {} to '{}'".format(me, tokenType[0], card.Name))
		else:
			notify("{} added to face-down card.".format(tokenType[0]))

def playCardFaceDown(card, x=0, y=0):
	global mycolor
	offset=0
	occupied = True
	if mycolor == PlayerColor[0]:
		x = -595
		y = -240
	elif mycolor == PlayerColor[1]:
		x = 460
		y = 120
	elif mycolor == PlayerColor[2]:
		x = -595
		y = 120
	elif mycolor == PlayerColor[3]:
		x = 460
		y = -240
	while occupied:
		occupied = False
		for c in table:
			if c.controller == me:
				posx, posy = c.position
				debug("c.position {}".format(c.position))
				if posx == x+offset and posy == y:
					occupied = True
					break
		if occupied:
			offset -=-70
	card.moveToTable(x+offset, y, True)
	mute()
	card.peek()
	card.highlight = mycolor

def debug(str):
	global debugMode
	if debugMode:
		whisper(str)

def moveCard(model, x, y):
	for c in table:
		if c.model == model:
			c.moveToTable(x, y)
			return c
	return table.create(model, x, y)

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


#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

#---------------------------------------------------------------------------
# Workflow routines
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def getStat(stats, stat): #searches stats string for stat and extract value
	statlist = stats.split(",")
	for statitem in statlist:
		statval = statitem.split("=")
		if statval[0] == stat:
			try:
				return int(statval[1])
			except:
				return 0
	return 0

def switchPhase(card, phase, phrase):
	global mycolor
	mute()
	if debugMode:	#debuggin'
		card.switchTo(phase)
		notify("Phase changed to the {}".format(phrase))
		return True
	elif card.highlight == None: #other player not done yet
		if card.controller == me:
			card.highlight = mycolor
		else:
			remoteCall(card.controller, "remoteHighlight", [card, mycolor])
		notify("{} is done with the {}".format(me.name,card.name))
		return False
	elif card.highlight != mycolor: #ready to go
		if card.controller == me:
			card.highlight = None
			card.switchTo(phase)
		else:
			remoteCall(card.controller, "remoteHighlight", [card, None])
			remoteCall(card.controller, "remoteSwitchPhase", [card, phase, phrase])
		notify("Phase changed to the {}".format(phrase))
		return True

def remoteHighlight(card, color):
	card.highlight = color

def remoteSwitchPhase(card, phase, phrase):
	card.switchTo(phase)

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def castingDiscount(cspell,cdiscount): #test if spell satisfies requirements of discount card
	#build test list from spell
	testlist = cspell.Type.split(",")
	testlist += cspell.Subtype.split(",")
	testlist += cspell.School.split(",")
	for i in range(len(testlist)):
		testlist[i] = testlist[i].strip().strip("]").strip("[")
	debug("casting discount testlist: {}".format(testlist))

	discount = 0
	found = False
	lines = cdiscount.Text.split("[Casting Discount]")
	debug("lines: {}".format(lines))
	if len(lines)>1: #line found - now process it
		cells = lines[1].split(']')
		for i in range(len(cells)):
			cells[i] = cells[i].strip().strip("]").strip("[")
			debug("cell entry: {}".format(cells[i]))
		try:
			discount = int(cells[0])
		except ValueError:
			debug("no discount value found")
			return 0
		reqstr = cells[1] #discount requirements should be here
		reqs = reqstr.split("/")
		for req in reqs:
			debug("testing req {}".format(req))
			for r in req.split("/"):
				if r in testlist:
					#Ring of Asyra is enchants and incants only
					if "Asyra" in cdiscount.Name:
						if "Incantation" in cspell.Type or "Enchantment" in cspell.Type:
							found = True
					#Ring of Beasts is creatures only
					elif "Beasts" in cdiscount.Name:
						if "Creature" in cspell.Type:
							found = True
					else:
						found = True

	if not found:
		return 0
	else:
		tuplist = [tup for tup in discountsUsed if tup[0] == cdiscount.Name]
		if len(tuplist) > 0:
			if tuplist[0][2] < tuplist[0][1]:
				discountsUsed.remove(tuplist[0])
				discountsUsed.append((tuplist[0][0],tuplist[0][1],tuplist[0][2]+1))
			else:
				return -1
		else:
			newtup = (cdiscount.Name,int(cells[2].strip("x")),1)
			discountsUsed.append(newtup)
	return discount

def castSpell(card, x = 0, y = 0):
	if card.Cost != "" and card.Cost != None:
		notify("Printed casting cost of {} is {}".format(card,card.Cost))
		castingcosts = card.Cost.split("+")
		try:
			castingcost = int(card.Cost)
		except ValueError:
			if "X" in card.Cost: #e.g. Dispel
				castingcost = 0
			elif "+" in card.Cost: #a x+y cost as in enchantments. We want the reveal cost
				try:
					castingcost = int(castingcosts[1]) #reveal cost is the second one
				except ValueError:
					castingcost = 0
				#target code
			else:
				castingcost = 0

		#TODO Who is casting the spell?
		infostr = ""
		if "Enchantment" in card.Type:
			infostr= "Printed casting cost is {}".format(castingcosts[1])
		else:
			infostr= "Printed casting cost is {}".format(card.Cost)
		# find any discounts from equipment(School, Type, Subtype, Targetbased?)
		discount = 0
		for c in table:
			if c.controller == me and c.isFaceUp and "[Casting Discount]" in c.Text and c != card:
				dc = castingDiscount(card,c)
				if dc > 0:
					infostr += "\nCost reduced by {} due to {}".format(dc,c.name)
					discount += dc
				elif dc < 0:
					infostr += "\n{} already reached max uses this round.".format(c.name)
		infostr += "\nTotal mana amount to subtract from mana pool?"
		manacost = askInteger(infostr,castingcost-discount)
		if manacost == None:
			return
		if me.Mana < manacost:
			notify("{} has insufficient mana in pool".format(me))
			return
		me.Mana -= manacost
		notify("{} payed {} mana from pool for {}".format(me.name,manacost,card.name))

def inspectCard(card, x = 0, y = 0):
    whisper("{}".format(card))
    for k in card.properties:
        if len(card.properties[k]) > 0:
            whisper("{}: {}".format(k, card.properties[k]))

def validateDeck(deck):
	for c in deck:
		if c.Type == "Mage":
			stats = c.Stats.split(",")
			schoolcosts = c.MageSchoolCost.split(",")
			break

	debug("Stats {}".format(stats))
	spellbook = {"Dark":2,"Holy":2,"Nature":2,"Mind":2,"Arcane":2,"War":2,"Earth":2,"Water":2,"Air":2,"Fire":2,"Creature":0}

	#get spellbook point limit
	for stat in stats:
		debug("stat {}".format(stat))
		statval = stat.split("=")
		if "Spellbook" in statval[0]:
			spellbook["spellpoints"] = int(statval[1])
			break

	#get school costs
	for schoolcost in schoolcosts:
		debug("schoolcost {}".format(schoolcost))
		costval = schoolcost.split("=")
		if "Spellbook" in costval[0]:
			spellbook["spellpoints"] = int(costval[1])
		elif "Dark" in costval[0]:
			spellbook["Dark"] = int(costval[1])
		elif "Holy" in costval[0]:
			spellbook["Holy"] = int(costval[1])
		elif "Nature" in costval[0]:
			spellbook["Nature"] = int(costval[1])
		elif "Mind" in costval[0]:
			spellbook["Mind"] = int(costval[1])
		elif "Arcane" in costval[0]:
			spellbook["Arcane"] = int(costval[1])
		elif "War" in costval[0]:
			spellbook["War"] = int(costval[1])
		elif "Earth" in costval[0]:
			spellbook["Earth"] = int(costval[1])
		elif "Water" in costval[0] and c.name != "Druid":
			spellbook["Water"] = int(costval[1])
		elif "Air" in costval[0]:
			spellbook["Air"] = int(costval[1])
		elif "Fire" in costval[0]:
			spellbook["Fire"] = int(costval[1])
	debug("Spellbook {}".format(spellbook))
	#spellbook["Dark"] = sumLevel("Dark")
	levels = {}
	booktotal = 0
	epics = ["", "three"]
	cardCounts = { }
	for card in deck: #run through deck adding levels
		if "Novice" in card.Traits: #Novice cards cost 1 spellpoint
			debug("novice {}".format(card))
			booktotal += 1
		elif "Talos" in card.Name: #Talos costs nothing
			debug("Talos")
		elif "+" in card.School: #and clause
			debug("and {}".format(card))
			schools = card.School.split("+")
			level = card.Level.split("+")
			i = 0
			for s in schools:
				try:
					levels[s] += int(level[i])
				except:
					levels[s] = int(level[i])
				i += 1
		elif "/" in card.School: #or clause
			debug("or {}".format(card))
			schools = card.School.split("/")
			level = card.Level.split("/")
			i = -1
			s_low = schools[0]
			for s in schools:
				i += 1
				if spellbook[s] < spellbook[s_low]: #if trained in one of the schools use that one
					s_low = s
					break
			try:
				levels[s_low] += int(level[i])
			except:
				levels[s_low] = int(level[i])
		elif card.School != "": # only one school
			debug("single {}".format(card))
			try:
				levels[card.School] += int(card.Level)
			except:
				levels[card.School] = int(card.Level)

		if card.Type == "Creature" and c.name == "Forcemaster": #check for the forcemaster rule
			debug("FM creature test")
			if "Mind" not in card.School:
				if "+" in card.School:
					level = card.Level.split("+")
					for l in level:
						booktotal += int(l)
				elif "/" in card.School:
					level = card.Level.split("/")
					booktotal += int(level[0])
				elif card.School != "": # only one school
					booktotal += int(card.Level)

		if "Water" in card.School and c.name == "Druid": #check for the druid rule
			if "1" in card.Level:
				debug("Druid Water test: {}".format(card.name))
				if "+" in card.School:
					schools = card.School.split("+")
					level = card.Level.split("+")
					i = 0
					for s in schools:
						if s == "Water" and 1 == int(level[i]): #if water level 1 is here only pay 1 spell book point for it.
							levels[s] -= 1
							booktotal += 1
						i += 1
				elif "/" in card.School: #this rule will calculate wrong if water is present as level 1 but wizard is trained in another element of the same spell too
					level = card.Level.split("/")
					levels[card.School] -= 1
					booktotal += 1
				elif card.School != "": # only one school
					levels[card.School] -= 1
					booktotal += 1
				debug("levels {}".format(levels))

		if "Epic" in card.Traits:	#check for multiple epic cards
			if card.Name in epics:
				notify("*** ILLEGAL ***: multiple copies of Epic card {} found in spellbook".format(card.Name))
				return False
			epics.append(card.Name)

		if "Only" in card.Traits:	#check for school/mage restricted cards
			ok = False
			magename = c.Name
			if "Beastmaster" in magename:
				magename = "Beastmaster"
			if "Wizard" in magename:
				magename = "Wizard"
			if magename in card.Traits:	#mage restriction
				ok = True
			for s in [school for school in spellbook if spellbook[school] == 1]:
				if s + " Mage" in card.Traits:
					ok = True
			if not ok:
				notify("*** ILLEGAL ***: the card {} is not legal in a {} deck.".format(card.Name, c.Name))
				return False

		l = 0	#check spell number restrictions
		if card.Level != "":
			if cardCounts.has_key(card.Name):
				cardCounts.update({card.Name:cardCounts.get(card.Name)+1})
			else:
				cardCounts.update({card.Name:1})
			if "+" in card.Level:
				level = card.Level.split("+")
				for s in level:
					l += int(s)
			elif "/" in card.Level:
				level = card.Level.split("/")
				l = int(level[0])
			else:
				l = int(card.Level)
			if (l == 1 and cardCounts.get(card.Name) > 6) or (l >= 2 and cardCounts.get(card.Name) > 4):
				notify("*** ILLEGAL ***: there are too many copies of {} in {}'s deck.".format(card.Name, me))
				return False

	debug("levels {}".format(levels))
	for level in levels:
		debug("booktotal {}, level {}".format(booktotal,level))
		booktotal += spellbook[level]*levels[level]
	notify("Spellbook of {} calculated to {} points".format(me,booktotal))

	if (booktotal > spellbook["spellpoints"]):
		return False

	#all good!
	return True
