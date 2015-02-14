############################################################################
##########################    v1.11.2.0    ##################################
############################################################################
import time
import re
import sys
sys.path.append(wd("lib"))
import os
############################################################################
##########################		Constants		##################################
############################################################################

##########################		Markers			##################################
ActionBlue = ("Action", "c980c190-448d-414f-9397-a5f17068ac58" )
ActionBlueUsed = ("Action Used", "5926df42-919d-4c63-babb-5bfedd14f649" )
ActionGreen = ("Action", "9cd83c4b-91b7-4386-9d9a-70719971f949" )
ActionGreenUsed = ("Action Used", "5f20a2e2-cc59-4de7-ab90-cc7d1ced0eee" )
ActionRed = ("Action", "4dd182d2-6e69-499c-b2ad-38701c0fb60d" )
ActionRedUsed = ("Action Used", "2e069a99-1696-4cbe-b6c6-13e1dda29563" )
ActionYellow = ("Action", "2ec4ddea-9596-45cc-a084-23caa32511be" )
ActionYellowUsed = ("Action Used", "7c145c5d-54c3-4f5b-bf66-f4d52f240af6" )
ActionGrey = ("Action", "623f07fb-9cfb-4b4b-a350-6b208f0ef29e" )
ActionGreyUsed = ("Action Used", "99bd454e-fab9-47c6-9f59-54a112eeb2da" )
ActionPurple = ("Action", "edb61e00-a666-480a-81f3-20eb9944b0ea")
ActionPurpleUsed = ("Action Used", "158f738b-6034-4c6d-b4ca-5abcf159ed9f" )
Armor = ("Armor +1", "b3b6b5d3-4bda-4769-9bac-6ed48f7eb0fc" )
Bleed = ("Bleed", "df8e1a68-9fc3-46be-ac4f-7d9c61805cf5" )
BloodReaper = ("BloodReaper","50d83b50-c8b1-47bc-a4a8-8bd6b9b621ce" )
Burn = ("Burn", "f9eb0f3a-63de-49eb-832b-05912fc9ec64" )
Corrode= ("Corrode", "c3de25bf-4845-4d2d-8a28-6c31ad12af46" )
Cripple = ("Cripple", "82df2507-4fba-4c81-a1de-71e70b9a16f5" )
Damage = ("Damage", "00000000-0000-0000-0000-000000000004" )
Daze = ("Daze","3ef51126-e2c0-44b3-b781-0b3f8476cb20" )
DeflectR = ("Deflect Ready", "684fcda0-e69d-426e-861c-5a92bc984f55" )
DeflectU = ("Deflect Used", "2c5b85ea-93de-4a99-b64d-da6c48baa205" )
Disable = ("Disable", "f68b3b5b-0755-40f4-84db-bf3197a667cb" )
DissipateToken = ("Dissipate Token","96348698-ae05-4c59-89bb-e79dad50ad1f" )
EternalServant = ("Eternal Servant", "86a71cf6-35ce-4728-a2f8-6701b1e29aa4" )
EggToken = ("Egg Token","874c7fbb-c566-4f17-b14e-ae367716dce5" )
FFToken = ("Forcefield Token", "fc23dce7-d58a-4c7d-a1b2-af9e23f5f29b" )
Growth = ("Growth", "c580e015-96ff-4b8c-8905-28688bcd70e8" )
Guard = ("Guard", "91ed27dc-294d-4732-ab71-37911f4011f2" )
HolyAvenger = ("Holy Avenger", "99381ac8-7d73-4d75-9787-60e6411d3613" )
Ichthellid = ("Ichthellid Larva", "c8bff05e-e43a-4b23-b467-9c4596050f28" )
Invisible = ("Invisible", "8d994fe9-2422-4a9d-963d-3ad10b2b823d" )
LoadToken = ("Load Token","d32267be-f4c5-48c6-8396-83c0db406942" )
Mana = ("Mana", "00000000-0000-0000-0000-000000000002" )
Melee = ("Melee +1", "e96b3791-fbcf-40a2-9c11-106342703db9" )
MistToken = ("Mist Token","fcc2ffeb-6ae6-45c8-930e-8f3521d326eb" )
Pet = ("Pet", "f4a2d3d3-4a95-4b9a-b899-81ea58293167" )
Quick = ("Quick", "11370fe9-41a4-4f05-9249-29a179c0031b" )
QuickBack = ("Quick Back", "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" )
Ranged = ("Ranged +1","cfb394b2-8571-439a-8833-476122a9eaa5")
Ready = ("Ready", "aaea8e90-e9c5-4fbc-8de3-4bf651d784a7" )
ReadyII = ("Ready II", "73fffebd-a8f0-43bd-a118-6aebc366ecf6" )
Rot = ("Rot", "81360faf-87d6-42a8-a719-c49386bd2ab5" )
RuneofFortification = ("Rune of Fortification","ae179c85-11ce-4be7-b9c9-352139d0c8f2" )
RuneofPower = ("Rune of Power","b3dd4c8e-35a9-407f-b9c8-a0b0ff1d3f07" )
RuneofPrecision = ("Rune of Precision","c2a265f9-ad97-4976-a83c-78891a224478" )
RuneofReforging = ("Rune of Reforging","d10ada1f-c03b-4077-b6cb-c9667d6b2744" )
RuneofShielding = ("Rune of Shielding","e0bb0e90-4831-43c6-966e-27c8dc2d2eef" )
Slam = ("Slam", "f7379e4e-8120-4f1f-b734-51f1bd9fbab9" )
Sleep = ("Sleep", "ad0e8e3c-c1af-47b7-866d-427f8908dea4" )
SpikedPitTrap = ("Spiked Pit Trap", "8731f61b-2af8-41f7-8474-bb9be0f32926")
StormToken = ("Storm Token", "6383011a-c544-443d-b039-9f7ba8de4c6b")
Stuck = ("Stuck", "a01e836f-0768-4aba-94d8-018982dfc122" )
Stun = ("Stun", "4bbac09e-a46c-42de-9272-422e8074533f" )
Tainted = ("Tainted", "826e81c3-6281-4a43-be30-bac60343c58f" )
Taunt = ("Taunt(Sosroku)", "16f03c44-5656-4e9d-9629-90c4ff1765a7" )
TauntT = ("Taunt(Thorg)", "8b5e3fe0-7cb1-44cd-9e9c-dadadbf04ab7" )
Treebond = ("Treebond", "ced2ce11-5e69-46a9-9fbb-887e96bdf805" )
Turn = ("Turn", "e0a54bea-6e30-409d-82cd-44a944e591dc" )
Used = ("Used", "ab8708ac-9735-4803-ba4d-4932a787540d" )
UsedII = ("Used II", "61bec951-ebb1-48f7-a2ab-0b6364d262e6" )
Veteran = ("Veteran", "72ee460f-adc1-41ab-9231-765001f9e08e" )
Visible = ("Visible", "b9b205a2-a998-44f5-97dc-c7f315afbbe2" )
VoltaricON = ("Voltaric ON", "a6e79926-db8d-4095-9aee-e3b46bf24a3f" )
VoltaricOFF = ("Voltaric OFF", "d91aabe0-d9cd-4b7e-b994-4e1c7a51c027" )
Weak = ("Weak", "22ef0c9e-6c0b-4e24-a4fa-e9d83f24fcba" )
WoundedPrey = ("Wounded Prey", "42f6cee3-3de4-4c90-a77c-9fb2c432d78d" )
Zombie = ("Zombie", "de101060-a4b4-4387-a7f8-aab82ecff2c8" )

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
diceBank = []
diceBankD12 = []

##########################		Other			############################

PlayerColor = 	["#de2827", 	# Red 		R=222 G=40  B=39
				"#171e78", 		# Blue		R=23  G=30  B=120
				"#01603e", 		# Green		R=1   G=96  B=62
				"#f7d917", 		# Yellow 	R=247 G=217 B=23
				"#c680b4",		# Purple
				"#c0c0c0"]		# Grey
mycolor = "#800080" # default
boardSet = "GameBoard1.png"
debugMode = False
myIniRoll = 0
hasRolledIni = False
deckLoaded = False
iniTokenCreated = False
currentPhase = ""
gameIsOver = False
discountsUsed = [ ]
gameStartTime = ""
gameEndTime = ""
roundTimes = []
gameTurn = 0
playerNum = 0
Magebind = ""
mageRevealCost = ""
infostr = ""
gameNum = ""

############################################################################
############################		Events		##################################
############################################################################

def onTableLoad():
	setGlobalVariable("TableSetup", False)
	global debugMode
	global playerNum
	global hasRolledIni
	global mycolor
	global gameNum
	gameNum = 1
	#log in chat screen what version of the game definiton the player is using
	notify("{} is running v.{} of the Mage Wars module.".format(me, gameVersion))
	#if there's only one player, go into debug mode
	if len(players) == 1:
		debugMode = True
		playerNum = 2
		mycolor = PlayerColor[0]
		CreateIniToken()
		players[0].setActivePlayer()
		hasRolledIni = True
		setGlobalVariable("IniAllDone", "x")
		notify("No need to roll for initative for {}...".format(me))
		notify("Enabling debug mode. In debug mode, deck validation is turned off and you can advance to the next phase by yourself.")

def onGameStart():
        mute()
	# reset color picking
	setGlobalVariable("ColorsChosen", "")

	# reset initiative automation
	setGlobalVariable("SetupDone", "")
	setGlobalVariable("OppIniRoll", "")
	setGlobalVariable("IniAllDone", "")
	setGlobalVariable("GameReset", "")
	setGlobalVariable('DiceAndPhaseCardsDone','True')

	#Set default map
	mapDict = createMap(4,3,[[1 for j in range(3)] for i in range(4)],250)
	mapDict.get('zoneArray')[0][0]['startLocation'] = '1'
	mapDict.get('zoneArray')[3][2]['startLocation'] = '2'
	setGlobalVariable('Map',str(mapDict))

	# reset python Global Variables
	for p in players:
		remoteCall(p, "setClearVars",[])

	#create a dictionary of attachments
	setGlobalVariable("attachDict",str({}))

        #set global event lists for rounds and single actions
	setGlobalVariable("roundEventList",str([]))
	setGlobalVariable("turnEventList",str([]))
	
	initializeGame()

        

def setUpDiceAndPhaseCards():
	mute()
	TableSetup = getGlobalVariable("TableSetup")
	if TableSetup == "False" and me.name == Player(1).name:
		dieCardX = -580
		dieCardY = -40
		card = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field
		card.anchor = (True)
		card = table.create("6a71e6e9-83fa-4604-9ff7-23c14bf75d48", (dieCardX + 75), (dieCardY - 55)) #Phase token/Next Phase Button
		card.switchTo("Planning") #skips upkeep for first turn
		card.anchor = (True)
		setGlobalVariable("TableSetup", True)

def onLoadDeck(player, groups):
	mute()
	global deckLoaded
	global debugMode
	global playerNum
	global iniTokenCreated
	if not bool(getGlobalVariable('diceAndPhaseCardsDone')):
                setUpDiceAndPhaseCards()
                setGlobalVariable('DiceAndPhaseCardsDone','True')
	if player == me:
		#if a deck was already loaded, reset the game
		if deckLoaded:
			notify ("{} has attempted to load a second Spellbook, the game will be reset".format(me))
			for p in players:
				remoteCall(p, "setClearVars",[])
			gameNum += 1
			resetGame()
		elif debugMode or validateDeck(groups[0]):
			deckLoaded = True
			playerSetup()
			if debugMode:
				# set Dice Rolling Area, Initative, and Phase Marker Card location
				setDRAIP(1)
				CreateIniToken()
			elif len(getGlobalVariable("SetupDone")) != len(players) - 1: #we're not the last done with setup
				playerNum = len(getGlobalVariable("SetupDone")) + 1
				setGlobalVariable("P" + str(playerNum) + "Name", me.name)
				setGlobalVariable("SetupDone", getGlobalVariable("SetupDone") + "x")
				if playerNum == 1:
					# set Dice Rolling Area, Initative, and Phase Marker Card location
					AskDiceRollArea()
			else:	#other guy is done too
				playerNum = len(getGlobalVariable("SetupDone")) + 1
				setGlobalVariable("P" + str(playerNum) + "Name", me.name)
				for p in players:
					remoteCall(p, "SetupForIni", [])
				notify("All players have set up. Please roll for initiative.")
		else:
			#notify and delete deck
			notify("Validation of {}'s spellbook FAILED. Please choose another spellbook.".format(me.name))
			for group in groups:
				for card in group:
					if card.controller == me:
						card.delete()

def onMoveCard(player,card,fromGroup,toGroup,oldIndex,index,oldX,oldY,x,y,isScriptMove):
	"""This event triggers whenever a card is moved. Currently, it is only used with the attachCards module
	to simplify the process of moving and attaching cards."""
	mute()
	if card.controller == me and fromGroup == table: #Does not trigger when	moving cards onto the table
		if not isScriptMove:
			c,t = detach(card)
			actionType = None
			if t:
				actionType = ['detaches','from']
			hasAttached = False
                        for a in table:
                                if getSetting('AutoAttach',True) and canAttach(card,a) and (cardX(a)-x)**2 + (cardY(a)-y)**2 < 400:
                                        c,t = attach(card,a)
                                        if t:
                                                actionType = ['attaches','to']
                                                hasAttached = True
                                                break
                        if not hasAttached and toGroup == table: snapToZone(card) #snap to zone
			if actionType:
				notify("{} {} {} {} {}.".format(me,actionType[0],c,actionType[1],t))
		if toGroup != table:
			detachAll(card)
		if not ((oldIndex != index and oldX==x and oldY==y) or isAttached(card) or toGroup != table): #Do not realign ifit is  only the index that is changing. Prevents recursions.
			alignAttachments(card)

def setClearVars():
	global deckLoaded
	global iniTokenCreated
	global hasRolledIni
	global gameNum
	if gameNum == 1: return
	deckLoaded = False
	iniTokenCreated = False
	hasRolledIni = False

def SetupForIni():
	mute()
	global hasRolledIni
	global myIniRoll
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
	global playerNum
	global myIniRoll

	myIniRoll = effect
	notify("{} rolled a {} for initiative".format(me, effect))
	myRollStr = (str(playerNum) + ":" + str(effect) + ";")
	setGlobalVariable("OppIniRoll", getGlobalVariable("OppIniRoll") + myRollStr)

	if getGlobalVariable("OppIniRoll").count(";") == len(players):
		#all initiatives rolled, see who had highest
		rollString = getGlobalVariable("OppIniRoll")
		rollStringList = rollString.split(";")
		max = 0
		timesMaxRolled = 0
		victoriousPlayerNum = 0
		for roll in rollStringList:
			if roll == "":
				continue
			temp = roll.split(":")
			if int(temp[1]) > max:
				max = int(temp[1])
				timesMaxRolled = 1
				victoriousPlayerNum = int(temp[0])
			elif int(temp[1]) == max:
				timesMaxRolled += 1

		if timesMaxRolled > 1:
			# we got a tie in there somewhere. determine winner randomly from high rollers
			notify("High roll tied! Randomly determining initiative...")
			highRollerPlayerNums = []
			for roll in rollStringList:
				if roll == "":
					continue
				temp = roll.split(":")
				if int(temp[1]) == max:
					highRollerPlayerNums.append(int(temp[0]))
			victoriousPlayerNum = highRollerPlayerNums[rnd(0, len(highRollerPlayerNums) - 1)]
			debug(str(victoriousPlayerNum))

		for p in players:
			remoteCall(p, "AskInitiative", [victoriousPlayerNum])

def setDRAIP(location):
	global dieCardX
	global dieCardY
	global dieCard2X
	global dieCard2Y
	global phaseX
	global phaseY
	global initX
	global initY

	if location == 1:
		#option A
		dieCardX = -580
		dieCardY = -40
		dieCard2X = -510 # = dieCardX + 60
		dieCard2Y = -40 # = dieCardY
		phaseX = -510 # = dieCardX + 60
		phaseY = -150
		initX = -580
		initY = -150 #= phaseY
	else:
		#option B
		dieCardX = -58 # -570 + 512
		dieCardY = 330 # -40 + 370
		dieCard2X = 0 # -510 + 510
		dieCard2Y = 330 # -40 + 370
		phaseX = 65 # -510 + 575
		phaseY = 330 # -150 + 480
		initX = -125 # -580 + 455
		initY = 330 # -150 + 480

############################################################################
######################		Group Actions			########################
############################################################################

def playerDone(group, x=0, y=0):
	notify("{} is done".format(me.name))
	mageStatus()

def attackTarget(attacker, x=0, y=0):
        mute()
        if attacker.controller == me and canDeclareAttack(attacker) and getSetting('BattleCalculator',True):
                snapToZone(attacker)
                target = [c for c in table if c.targetedBy==me]
                aTraitDict = computeTraits(attacker)
                if len(target) == 1:
                        defender = target[0]
                        if defender.controller == me: snapToZone(defender)
                        else: remoteCall(defender.controller,'snapToZone',[defender])
                        dTraitDict = computeTraits(defender)
                        attack = diceRollMenu(attacker,defender)
                        if attack:
                                if defender.controller == me: initializeAttackSequence(aTraitDict,attack,dTraitDict)
                                else: remoteCall(defender.controller,'initializeAttackSequence',[aTraitDict,attack,dTraitDict])
                elif len(target) == 0: #Untargeted attack
                        attack = diceRollMenu(attacker,None)
                        dice = attack.get('Dice',-1)
                        if dice >= 0:
                                notify("{} attacks with {}".format(me,attacker))
                                roll,effect = rollDice(dice)
        else: genericAttack(table) #If the card you are targeting cannot attack, or the battle calculator is off, just go to the generic attack menu

def genericAttack(group, x=0, y=0):
	target = [cards for cards in table if cards.targetedBy==me]
	defender = (target[0] if len(target) == 1 else None)
        dice = diceRollMenu(None,defender).get('Dice',-1)
        if dice >=0: rollDice(dice)

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
	choiceList = ["Red", "Blue", "Green", "Yellow", "Purple", "Grey"]
	if not debugMode:
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

def createCompassRose(group, x=0, y=0):
	table.create("7ff8ed79-159c-46e5-9e87-649b3269a931", 450, -40 )

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
	boardSet = "GameBoard1.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard2(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard2.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard3(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard3.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard4(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard4.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard5(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard5.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard9(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard9.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard10(group, x=0, y=0):
	global boardSet
	boardSet = "GameBoard10.jpg"
	mute()
	for p in players:
		remoteCall(p, "setGameBoard", [boardSet])

def setGameBoard(bset):
	mute()
	global boardSet
	boardSet = bset
	table.setBoardImage("GameBoards\\{}".format(boardSet))

def AskInitiative(pNum):
	global playerNum
	if playerNum != pNum:
		return
	mute()
	notify("{} is choosing whether or not to go first.".format(me))
	choiceList = ['Yes', 'No']
	colorsList = ['#FF0000', '#0000FF']
	choice = askChoice("You have won initiative! Would you like to go first?", choiceList, colorsList)
	if choice == 1:
		notify("{} has elected to go first!".format(me))
		CreateIniToken()
		players[0].setActivePlayer()
	else:
		#randomly determine who else should go first (in a 2 player game, this will always choose the other player)
		pNum = rnd(1, len(players) - 1)
		notify("{} has elected NOT to go first! {} has first initiative.".format(me, players[pNum]))
		remoteCall(players[pNum], "CreateIniToken", [])
		players[pNum].setActivePlayer()

def AskDiceRollArea():
	mute()
	notify("{} is choosing where the Dice Roll Area will be placed.".format(me))
	choiceList = ['Side', 'Bottom']
	colorsList = ['#FF0000', '#0000FF']
	choice = askChoice("Would you like to place the Dice Roll Area, Initative Marker, and Phase Marker to the Side or Botton of the Gameboard?", choiceList, colorsList)
	if choice == 0 or choice == 1:
		notify("{} has elected to place the Dice Roll Area to the Side.".format(me))
	else:
		notify("{} has elected to place the Dice Roll Area to the Bottom.".format(me))
	setDRAIP(choice)
	for p in players:
		remoteCall(p, "setDRAIP", [choice])

def CreateIniToken():
	global gameStartTime
	global iniTokenCreated
	global currentPhase
	mute()
	dieCardX = -570
	dieCardY = -40
	if not iniTokenCreated:
		iniTokenCreated = True
		init = table.create("8ad1880e-afee-49fe-a9ef-b0c17aefac3f", (dieCardX + 5) , (dieCardY - 75 ) ) #initiative token
		init.anchor = (True)
		init.switchTo({
                        PlayerColor[0]:"",
                        PlayerColor[1]:"B",
                        PlayerColor[2]:"C",
                        PlayerColor[3]:"D",
                        PlayerColor[4]:"E",
                        PlayerColor[5]:"F"
                        }[mycolor])
		setGlobalVariable("IniAllDone", "x")
		setGlobalVariable("RoundNumber", "1")
		setGlobalVariable("PlayerWithIni", str(playerNum))
		gameStartTime = time.time()
		currentPhase = "Planning"
		notify("Setup is complete!")

def nextPhase(group, x=-360, y=-150):
	global mycolor
	global roundTimes
	global gameTurn
	global gameIsOver
	if gameIsOver:	#don't advance phase once the game is done
		return
	if getGlobalVariable("IniAllDone") == "": # Player setup is not done yet.
		return
	mute()
	mageStatus()
	card = None
	for c in table: #find phase card
		if c.model == "6a71e6e9-83fa-4604-9ff7-23c14bf75d48":
			card = c
			break
	if card.alternate == "":
		switchPhase(card,"Planning","Planning Phase")
	elif card.alternate == "Planning":
		switchPhase(card,"Deploy","Deployment Phase")
	elif card.alternate == "Deploy":
		switchPhase(card,"Quick","First Quickcast Phase")
	elif card.alternate == "Quick":
		switchPhase(card,"Actions","Actions Phase")
	elif card.alternate == "Actions":
		switchPhase(card,"Quick2","Final Quickcast Phase")
	elif card.alternate == "Quick2":
		if switchPhase(card,"","Upkeep Phase") == True: # "New Round" begins time to perform the Intiative, Reset, Channeling and Upkeep Phases
                        setEventList('Round',[])
                        setEventList('Turn',[])#Clear event list for new round
			gTurn = getGlobalVariable("RoundNumber")
			gameTurn = int(gTurn) + 1
			setGlobalVariable("RoundNumber", str(gameTurn))
			rTime = time.time()
			roundTimes.append(rTime)
			notify("Round {} Start Time: {}".format(str(gameTurn),time.ctime(roundTimes[-1])))
			notify("Ready Stage for Round #" + str(gameTurn) + ":  Performing Initiative, Reset, and Channeling Phases")
			init = [card for card in table if card.model == "8ad1880e-afee-49fe-a9ef-b0c17aefac3f"][0]
			if init.controller == me:
				flipcard(init)
			else:
				remoteCall(init.controller, "flipcard", [init])

			#resolve other automated items
			for p in players:
				remoteCall(p,"resetDiscounts",[])
				remoteCall(p, "resetMarkers", [])
				remoteCall(p, "resolveChanneling", [])
				remoteCall(p, "resolveBurns", [])
				remoteCall(p, "resolveRot", [])
				remoteCall(p, "resolveBleed", [])
				remoteCall(p, "resolveDissipate", [])
				remoteCall(p, "resolveLoadTokens", [])
				remoteCall(p, "resolveStormTokens", [])
				remoteCall(p, "resolveUpkeep", [])

	update() #attempt to resolve phase indicator sometimes not switching

def resetDiscounts():
	#reset discounts used
	for tup in discountsUsed:
		discountsUsed.remove(tup)
		discountsUsed.append((tup[0],tup[1],0))

def advanceTurn():
	mute()
	nextPlayer = getNextPlayerNum()
	nextPlayerName = getGlobalVariable("P" + str(nextPlayer) + "Name")
	for p in players:
		if p.name == nextPlayerName:
			for p2 in players:
				remoteCall(p2, "setActiveP", [p])

def setActiveP(p):
	p.setActivePlayer()

def resetMarkers():
	mute()
	for c in table:
		if c.targetedBy == me:
			c.target(False)
		if c.isFaceUp: #don't waste time on facedown cards
			mDict = {ActionRedUsed : ActionRed,
		                ActionBlueUsed : ActionBlue,
		                ActionGreenUsed : ActionGreen,
		                ActionYellowUsed : ActionYellow,
		                ActionPurpleUsed : ActionPurple,
		                ActionGreyUsed : ActionGrey,
		                QuickBack : Quick,
		                Used : Ready,
		                UsedII : ReadyII,
		                VoltaricON : VoltaricOFF,
		                DeflectU : DeflectR,
		                Visible : Invisible}
			for key in mDict:
		                if c.markers[key] == 1:
		                        c.markers[key] = 0
		                        c.markers[mDict[key]] = 1
	notify("{} reset's all Action, Ability, Quickcast, and Ready Markers on the Mages cards by flipping them to their active side.".format(me.name))
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
				burnDamage += roll
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

def resolveBleed():
	mute()

	#is the setting on?
	if not getSetting("AutoResolveBleed", True):
		return
	cardsWithBleed = [c for c in table if c.markers[Bleed] and c.controller == me]
	if len(cardsWithBleed) > 0:
		notify("Resolving Bleed for {}...".format(me))	#found at least one
		for card in cardsWithBleed:
			bleedDamage = (card.markers[Bleed])
			 #apply damage
			if card.Type == "Mage":
				card.controller.Damage += bleedDamage
			elif card.Type == "Creature" or "Conjuration" in card.Type:
				card.markers[Damage] += bleedDamage
			notify("{} damage added to {}.".format(bleedDamage, card.Name))
		notify("Finished auto-resolving Bleed for {}.".format(me))

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
				notify("{} discards {} as it no longer has any Dissipate Tokens".format(me, card.Name))
				card.moveTo(me.piles['Discard'])
			notify("Finished auto-resolving Dissipate for {}.".format(me))
			
	#use the logic for Dissipate for Disable Markers
	cardsWithDisable = [c for c in table if c.markers[Disable] and c.controller == me]
	if len(cardsWithDisable) > 0:
		notify("Resolving Disable Markers for {}...".format(me))	#found at least one
		for card in cardsWithDisable:
			notify("{} removes a Disable Marker from '{}'".format(me, c.name))	#found at least one
			card.markers[Disable] -= 1 # Remove Marker
			notify("Finished auto-resolving Disable Markers for {}.".format(me))
			
def resolveLoadTokens():
	mute()
	loadTokenCards = [card for card in table if card.Name in ["Ballista", "Akiro's Hammer"] and card.controller == me and card.isFaceUp ]
	for card in loadTokenCards:
		notify("Resolving Load Tokens for {}...".format(me))	#found at least one
		if card.markers[LoadToken] == 0:
			notify("Placing the First Load Token on {}...".format(card.Name)) #found no load token on card
			card.markers[LoadToken] = 1
		elif card.markers[LoadToken] == 1:
			notify("Placing the Second Load Token on {}...".format(card.Name)) #found one load token on card
			card.markers[LoadToken] = 2
		notify("Finished adding Load Tokens for {}.".format(me))
		
def resolveStormTokens():
	mute()
	stormTokenCards = [card for card in table if card.Name in ["Staff of Storms"] and card.controller == me and card.isFaceUp ]
	for card in stormTokenCards:
		if card.markers[StormToken] ==4:
			return
		notify("Resolving Storm Tokens for {}...".format(me))	#found at least one
		if card.markers[StormToken] == 0 or card.markers[StormToken] < 4:
			notify("Placing a Storm Token on the '{}'...".format(card.Name)) #Card needs a load token
			card.markers[StormToken] += 1
		notify("Finished adding Storm Tokens for {}.".format(me))

def resolveChanneling():
	mute()
	
	channelExtraMana4Mage = 0
	for c in table:
		if c.isFaceUp and c.controller == me: #don't waste time on facedown cards
			for card in me.piles['Discard']:
				if c == card:
					return
			
		if c.isFaceUp and c.controller == me:
			if c.name == "Mana Flower" or c.name == "Mana Crystal":
				channelExtraMana4Mage +=1
				whisper("Mana added to {} from {}".format(me,c))
			elif c.name == "Harmonize":
				c2 = getAttachTarget(c)
				if c2 and c2.Type in ['Mage','Magestats'] and c.controller == me: #Mages
					channelExtraMana4Mage +=1
					whisper("Mana added to {} from {}".format(me,c))
		
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
	                if c.isFaceUp and isAttached(c): #Harmonize is attached to something; add mana to that thing
	                        c2 = getAttachTarget(c)
	                        if c2 and 'Channeling' in c2.Stats and not c2.Type in ['Mage','Magestats']: #Not Mages
	                                addMana(c2)
	                                whisper("Mana added to {} from {}".format(c2,c))

	me.Mana += me.Channeling + channelExtraMana4Mage # Mage channels his mana
	notify("{} Channels {} Mana into the mages Mana supply.".format(me.name,me.Channeling + channelExtraMana4Mage))

def resolveUpkeep():
	mute()
	PsiOrbDisc = 0
	#is the setting on?
	if not getSetting("AutoResolveUpkeep", True):
		return

	for card in table:
		if "Psi-Orb" == card.name and card.isFaceUp and card.controller == me: # if the player has Psi-Orb in play set Discount to 3
		 	PsiOrbDisc = 3

	for card in table:
		for c in me.piles['Discard']: # if the card was discarded below we are done processing it
	 		if c == card:
		 		return
	 	if "Mordok's Obelisk" == card.Name: # process players cards for Mordok's Upkeep on all non-Mage Creatures
	 		for c in table:
	 			if c.Type == "Creature" and c.isFaceUp and c.controller == me:
	 				if me.Mana < 1:
	 					c.moveTo(me.piles['Discard'])
	 					notify("{} was unable to pay Upkeep cost for {} from {} effect and has placed {} in the discard pile.".format(me, c.Name, card.Name, c.Name))
	 					return
	 				else:
	 					choiceList = ['Yes', 'No']
	 					colorsList = ['#0000FF', '#FF0000']
	 					choice = askChoice("Do you wish to pay the Upkeep +1 cost for {} from {} effect?".format(c.Name, card.Name), choiceList, colorsList)
	 					if choice == 1:
	 						me.Mana -= 1
	 						notify("{} pays the Upkeep cost of 1 for {} from {} effect.".format(me, c.Name, card.Name))
	 					else:
	 						c.moveTo(me.piles['Discard'])
	 						notify("{} has chosen not to pay the Upkeep cost for {} effect on {} and has placed {} in the discard pile.".format(me, card.Name, c.Name, c.Name))
	 						return
	 	else:
	 		if card.controller == me and "Upkeep" in card.Traits and card.isFaceUp and card.type != "Internal":
	 			debug("Debug3: {} me.Mana:{}".format(me.name,me.Mana))
	 		 	if me.Mana < 1:
	 		 		notify("{} discards {} as you do not have sufficent mana to pay for the Upkeep costs.".format(me, card.Name))
	 		 		card.moveTo(me.piles['Discard'])
	 		 		return
	 		 	else:
	 		 		TraitValue, TraitStr = getTraitValue(card, "Upkeep")
	 		 		notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(TraitValue, card.Name)
	 		 		debug("Psi-Orb Discount: {} and Card Name: {} Card School: {}".format(str(PsiOrbDisc),card.name, card.school))
					if PsiOrbDisc > 0 and "Mind" == card.school:
						PsiOrbDisc -= 1
						notify("{} - Psi-Orb Discount was used to pay 1 Mana point towards the Upkeep cost for '{}', there are '{}' remaining Upkeep discounts left this Round.".format(me,card.name,PsiOrbDisc))
						TraitValue = TraitValue - 1
						notifystr = "Do you wish to pay the Upkeep +{} cost for {} after the 1 Mana Discount from the Psi-Orb?".format(TraitValue, card.Name)

	 		 		if TraitValue >= 1:
	 		 			choiceList = ['Yes', 'No']
	 					colorsList = ['#0000FF', '#FF0000']
	 					choice = askChoice("{}".format(notifystr), choiceList, colorsList)
	 					if choice == 1:
	 						if me.Mana >= TraitValue:
	 							me.Mana -= TraitValue
	 							notify("{} pays the Upkeep cost of {} for {}.".format(me, TraitValue, card.Name))
	 							if "Forcefield" == card.Name:
	 								notify("Resolving Forcefield Tokens for {}...".format(me))
	 								if card.markers[FFToken] == 0:
	 									notify("Placing the First Forcefield Token on {}...".format(card.Name)) #found no token on card
	 									card.markers[FFToken] = 1
	 								elif card.markers[FFToken] == 1:
	 									notify("Placing the Second Forcefield Token on {}...".format(card.Name)) #found one token on card
	 									card.markers[FFToken] = 2
	 								elif card.markers[FFToken] == 2:
	 									notify("Placing the Third Forcefield Token on {}...".format(card.Name)) #found two tokens on card
	 									card.markers[FFToken] = 3
	 								notify("Finished adding Forcefield Tokens for {}.".format(me))
	 					else:
	 						notify("{} has chosen not to pay the Upkeep cost for {} and has discarded it.".format(me, card.Name))
	 						card.moveTo(me.piles['Discard'])
	 						return

def mageStatus():
	global gameEndTime
	mute()
	if not me.Damage >= me.Life:
		return
	for c in table:
		if c.Type == "Mage" and c.controller == me:
			c.orientation = 1
	gameEndTime = time.time()
	#	playSoundFX('Winner')
	for p in players:
		remoteCall(p, "reportDeath",[me])
#	reportGame('MageDeath')

def reportDeath(deadmage):
	global gameIsOver
	global gameEndTime
	endofGameTurn = getGlobalVariable("RoundNumber")
	gameIsOver = True
	gameEndTime = time.time()
	choiceList = ['OK']
	colorsList = ['#de2827']
	whisper("'{}' has fallen in the arena! At {} after {} Rounds.".format(deadmage, time.ctime(gameEndTime), endofGameTurn))
	choice = askChoice("{} has fallen in the arena! At {} after {} Rounds.".format(deadmage, time.ctime(gameEndTime), endofGameTurn), choiceList, colorsList)
	if choice == 0 or choice == 1:
		return

def checkMageDeath(player, counter, oldvalue):
	global currentPhase
	if getGlobalVariable("IniAllDone") == "x" and (counter.name == "Damage" or counter.name == "Life"):
		if me.Damage >= me.Life and currentPhase == "Actions":
			if not confirm("                       Your Mage has fallen in the Arena! \n\nDo you wish to continue playing until the end of the current creatures Action Phase?"):
				mageStatus()

def concede(group=table, x = 0, y = 0):
	global gameEndTime
	global gameIsOver
	global gameTurn
	mute()
	if confirm("Are you sure you want to concede this game?"):
		gameIsOver = True
		for c in table:
			if c.Type == "Mage" and c.controller == me:
				c.orientation = 1
		gameEndTime = time.time()
#		reportGame('Conceded')
		notify("'{}' has conceded the game".format(me))
	else:
		notify("'{}' was about to concede the game, but thought better of it...".format(me))

"""
Format:
[function name, setting name, message, default]
"""

fGenToggleSettingsList = [['ResolveBurns','AutoResolveBurns',"You have {} automatic resolution of Burn tokens on your cards.",True],
                          ['SoundFX','AutoConfigSoundFX',"You have {} Sound Effects.",True],
                          ["ResolveRot","AutoResolveRot","You have {} automatic resolution of Rot tokens on your cards.",True],
                          ["FFTokens","AutoResolveFFTokens","You have {} automatic resolution of Forcefield tokens on your cards.",True],
                          ["ResolveBleed","AutoResolveBleed","You have {} automatic resolution of Bleed markers on your cards.",True],
                          ["ResolveDissipate","AutoResolveDissipate","You have {} automatic resolution of Dissipate tokens on your cards.",True],
                          ["EnchantRevealPrompt","EnchantPromptReveal","You have {} the enchantment reveal prompt.",False],
                          ["AutoRollInitiative","AutoRollIni","You have {} automatically rolling initiative.",False],
                          ["AutoResolveUpkeep","ResolveUpkeep","You have {} automatically caculating Upkeep costs.",False],
                          ["AutoAttach","AutoAttach","You have {} automatically attaching cards.",True],
                          ["ComputeProbabilities","AutoConfigProbabilities","You have {} battle computations on targeted cards.",True],
                          ["DiceButtons","AutoConfigDiceButtons","You have {} dice selection buttons.",True],
                          ["BattleCalculator","BattleCalculator","You have {} the battle calculator.",True]]

for fGen in fGenToggleSettingsList:
        exec(
'def toggle'+fGen[0]+'(group,x=0,y=0):\n\t'+
        'state=getSetting("'+fGen[1]+'",'+str(fGen[3])+')\n\t'+
        'setSetting("'+fGen[1]+'", not state)\n\t'+
        'if state:\n\t\twhisper("'+fGen[2].format('disabled')+'")\n\t'+
        'else:\n\t\twhisper(":'+fGen[2].format('enabled')+'")')

def toggleDebug(group, x=0, y=0):
	global debugMode
	debugMode = not debugMode
	if debugMode:
		notify("{} turns on debug".format(me))
	else:
		notify("{} turns off debug".format(me))

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
	notify("{} asks are you thinking?".format(me.name))

def askYourTurn(group, x=0, y=0):
	notify("{} asks is it your turn?".format(me.name))

def askMyTurn(group, x=0, y=0):
	notify("{} asks is it my turn?".format(me.name))

def askRevealEnchant(group, x=0, y=0):
	notify("{} asks do you wish to Reveal your Enchantment?".format(me.name))

############################################################################
######################		Card Actions			################################
############################################################################

##########################     Add/Subtract Tokens     ##############################

tokenList=['Armor',
           'Bleed',
           'Burn',
           'Cripple',
           'Corrode',
           'Disable',
           'Daze',
           'Growth',
           'Mana',
           'Melee',
           'Rot',
           'Slam',
           'Stun',
           'Stuck',
           'Tainted',
           'Veteran',
           'Weak',
           'Zombie'
           ]

for token in tokenList:
        exec('def add'+token+'(card, x = 0, y = 0):\n\taddToken(card,'+token+')')
        exec('def sub'+token+'(card, x = 0, y = 0):\n\tsubToken(card,'+token+')')

def addDamage(card, x = 0, y = 0):
	if "Mage" in card.Type and card.controller == me:
		me.Damage += 1
	else:
		addToken(card, Damage)

def addOther(card, x = 0, y = 0):
	marker, qty = askMarker()
	if qty == 0:
		return
	card.markers[marker] += qty

def subDamage(card, x = 0, y = 0):
	if "Mage" in card.Type and card.controller == me:
			me.Damage -= 1
	else:
		subToken(card, Damage)

def clearTokens(card, x = 0, y = 0):
	mute()
	for tokenType in card.markers:
		card.markers[tokenType] = 0
	notify("{} removes all tokens from '{}'".format(me, card.Name))

##########################     Toggle Actions/Tokens     ##############################
typeIgnoreList = ['Internal','Phases','Diceroll']

def toggleAction(card, x=0, y=0):
	global mycolor
	mute()
	if card.Type in typeIgnoreList or not card.isFaceUp: return
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
	elif mycolor == PlayerColor[4]: #Purple
		if card.markers[ActionPurpleUsed] > 0:
			card.markers[ActionPurple] = 1
			card.markers[ActionPurpleUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionPurple] = 0
			card.markers[ActionPurpleUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[5]: #Grey
		if card.markers[ActionGreyUsed] > 0:
			card.markers[ActionGrey] = 1
			card.markers[ActionGreyUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionGrey] = 0
			card.markers[ActionGreyUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))

def toggleDeflect(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or not card.isFaceUp: return
	if card.markers[DeflectR] > 0:
		card.markers[DeflectR] = 0
		card.markers[DeflectU] = 1
		notify("'{}' uses deflect".format(card.Name))
	else:
		card.markers[DeflectR] = 1
		card.markers[DeflectU] = 0
		notify("'{}' readies deflect".format(card.Name))

def toggleGuard(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or not card.isFaceUp: return
	toggleToken(card, Guard)

def toggleInvisible(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or not card.isFaceUp: return
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
	if card.Type in typeIgnoreList or not card.isFaceUp: return
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
	if card.Type in typeIgnoreList or not card.isFaceUp: return
	if card.markers[ReadyII] > 0:
		card.markers[ReadyII] = 0
		card.markers[UsedII] = 1
		notify("'{}' spends the Ready Marker II on '{}'".format(me, card.Name))
	else:
		card.markers[ReadyII] = 1
		card.markers[UsedII] = 0
		notify("'{}' readies the Ready Marker II on '{}'".format(me, card.Name))

def toggleQuick(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or not card.isFaceUp: return
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
	if card.Type in typeIgnoreList or not card.isFaceUp: return
	if card.markers[VoltaricON] > 0:
		card.markers[VoltaricON] = 0
		card.markers[VoltaricOFF] = 1
		notify("'{}' disables Voltaric shield".format(card.Name))
	else:
		card.markers[VoltaricON] = 1
		card.markers[VoltaricOFF] = 0
		notify("'{}' enables Voltaric shield".format(card.Name))

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
	if card.Type in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	if "Vine Marker" in card.Name and card.controller == me:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")
		notify("{} Flips Vine Marker.".format(me))
	elif "Alt Zone" in card.Name and card.controller == me:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")
		notify("{} Flips Zone Marker.".format(me))
	elif card.isFaceUp == False:
		card.isFaceUp = True
		if card.Type != "Enchantment"  and "Conjuration" not in card.Type: #leaves the highlight around Enchantments and Conjurations
			card.highlight = None
		if card.Type == "Mage" or card.Type == "Creature": #places action marker on card
			toggleAction(card)
		if card.Type == "Mage": #once more to flip action to active side
			toggleAction(card)
			toggleQuick(card)
			if "Wizard" in card.Name:
					card.markers[VoltaricOFF] = 1
			if "Forcemaster" == card.Name:
					card.markers[DeflectR] = 1
			if "Beastmaster" == card.Name:
					card.markers[Pet] = 1
			if "Johktari Beastmaster" == card.Name:
					card.markers[WoundedPrey] = 1
			if "Priest" == card.Name:
					card.markers[HolyAvenger] = 1
			if "Druid" == card.Name:
					card.markers[Treebond] = 1
			if "Necromancer" == card.Name:
					card.markers[Eternal_Servant] = 1
			if "Warlock" == card.Name:
					card.markers[BloodReaper] = 1
		if "Anvil Throne Warlord Stats" == card.Name:
					card.markers[RuneofFortification] = 1
					card.markers[RuneofPower] = 1
					card.markers[RuneofPrecision] = 1
					card.markers[RuneofReforging] = 1
					card.markers[RuneofShielding] = 1
		if card.Type == "Creature":
			if "Invisible Stalker" == card.Name:
					card.markers[Invisible] = 1
			if "Thorg, Chief Bodyguard" == card.Name:
					card.markers[TauntT] = 1
			if "Sosruko, Ferret Companion" == card.Name:
					card.markers[Taunt] = 1
			if "Ichthellid" == card.Name:
					card.markers[EggToken] = 1
			if "Talos" == card.Name:
					toggleAction(card)
		if card.Type == "Conjuration":
			if "Ballista" == card.Name:
  				card.markers[LoadToken] = 1
			if "Akiro's Hammer" == card.Name:
  				card.markers[LoadToken] = 1
			if "Corrosive Orchid" == card.Name:
  				card.markers[MistToken] = 1
			if "Nightshade Lotus" == card.Name:
  				card.markers[MistToken] = 1
			if "Rolling Fog" == card.Name:
  				card.markers[DissipateToken] = 3
		if "Defense" in card.Stats:
			if "1x" in card.Stats:
				card.markers[Ready] = 1
			if "2x" in card.Stats:
				card.markers[Ready] = 1
				card.markers[ReadyII] = 1
		if "Forcefield" == card.Name:
			card.markers[FFToken] = 3
		if "[ReadyMarker]" in card.Text:
			card.markers[Ready] = 1
  	elif card.alternates is not None and "B" in card.alternates: #flip the initiative card
		nextPlayer = getNextPlayerNum()
		setGlobalVariable("PlayerWithIni", str(nextPlayer))
		for p in players:
			remoteCall(p, "changeIniColor", [card])
		#notify("{} turns '{}' face up.".format(me, card.Name))
	elif card.isFaceUp:
		notify("{} turns '{}' face down.".format(me, card.Name))
		card.isFaceUp = False
		card.peek()

def getNextPlayerNum():
	activePlayer = int(getGlobalVariable("PlayerWithIni"))
	nextPlayer = activePlayer + 1
	if nextPlayer > len(players):
		nextPlayer = 1
	return nextPlayer

def changeIniColor(card):
	global mycolor
	mute()
	if playerNum == int(getGlobalVariable("PlayerWithIni")):
		if mycolor == PlayerColor[0]:
			if card.controller == me:
				card.switchTo("")
			else:
				remoteCall(card.controller, "remoteSwitchPhase", [card, "", ""])
		elif mycolor == PlayerColor[1]:
			if card.controller == me:
				card.switchTo("B")
			else:
				remoteCall(card.controller, "remoteSwitchPhase", [card, "B", ""])
		elif mycolor == PlayerColor[2]:
			if card.controller == me:
				card.switchTo("C")
			else:
				remoteCall(card.controller, "remoteSwitchPhase", [card, "C", ""])
		elif mycolor == PlayerColor[3]:
			if card.controller == me:
				card.switchTo("D")
			else:
				remoteCall(card.controller, "remoteSwitchPhase", [card, "D", ""])
		elif mycolor == PlayerColor[4]:
			if card.controller == me:
				card.switchTo("E")
			else:
				remoteCall(card.controller, "remoteSwitchPhase", [card, "E", ""])
		elif mycolor == PlayerColor[5]:
			if card.controller == me:
				card.switchTo("F")
			else:
				remoteCall(card.controller, "remoteSwitchPhase", [card, "F", ""])

def discard(card, x=0, y=0):
	mute()
	if card.controller != me:
		whisper("{} does not control '{}' - discard cancelled".format(me, card))
		return
	card.isFaceUp = True
        detach(card)
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
	if card.type == "DiceRoll":
		genericAttack(0, x, y)
	
	if card.type =="Phase":
		nextPhase(table,0,0)

	if card.controller == me:
		if not card.isFaceUp:
			#is this a face-down enchantment? if so, prompt before revealing
			if "Mage" in card.Type:
				flipcard(card, x, y)
			else:
				castSpell(card, x, y)
		else:
			if card.Type == "Incantation" or card.Type == "Attack":
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("Did you wish to cast this spell?", choiceList, colorsList)
				if choice == 1:
					castSpell(card, x, y)
				else:
					return

############################################################################
######################		Utility Functions		########################
############################################################################

def addToken(card, tokenType):
	mute()
	if card.Type in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	card.markers[tokenType] += 1
	if card.isFaceUp:
		notify("{} added to '{}'".format(tokenType[0], card.Name))
	else:
		notify("{} added to face-down card.".format(tokenType[0]))

def subToken(card, tokenType):
	mute()
	if card.Type in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	if card.markers[tokenType] > 0:
		card.markers[tokenType] -= 1
		if card.isFaceUp:
			notify("{} removed from '{}'".format(tokenType[0], card.Name))
		else:
			notify("{} removed from face-down card.".format(tokenType[0]))

def toggleToken(card, tokenType):
	mute()
	if card.Type in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
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
        mute()
	global mycolor
	occupied = True
	mapDict = eval(getGlobalVariable('Map'))
        x,y = 0,0
	if mapDict:
                for i in range(len(mapDict.get('zoneArray'))):
                        for j in range(len(mapDict.get('zoneArray')[0])):
                                if mapDict.get('zoneArray')[i][j] and mapDict.get('zoneArray')[i][j].get('startLocation') == str(playerNum):
                                        zoneX,zoneY = mapDict.get('zoneArray')[i][j].get('x'),mapDict.get('zoneArray')[i][j].get('y')
                                        mapX,mapW = mapDict.get('x'),mapDict.get('X')
                                        zoneS = mapDict.get('zoneArray')[i][j].get('size')
                                        cardW,cardH = card.size.Width,card.size.Height
                                        if card.type == 'Mage':
                                                x = (zoneX if i < mapDict.get('I')/2 else mapX + mapW - cardW)
                                                y = (zoneY if j < mapDict.get('J')/2 else zoneY+zoneS-cardH)
                                        elif card.type == 'Magestats':
                                                x = (zoneX - cardW if i < mapDict.get('I')/2 else mapX + mapW)
                                                y = (zoneY if j < mapDict.get('J')/2 else zoneY+zoneS-cardH)
                                        else:
                                                x = (zoneX - cardW if i < mapDict.get('I')/2 else mapX + mapW)
                                                y = (zoneY + cardH if j < mapDict.get('J')/2 else zoneY+zoneS-2*cardH)
                                                xOffset = 0
                                                while True:
                                                        occupied = False
                                                        for c in table:
                                                                if c.controller == me:
                                                                        posx, posy = c.position
                                                                        debug("c.position {}".format(c.position))
                                                                        if posx == x+xOffset and posy == y:
                                                                                occupied = True
                                                                                break
                                                        if occupied:
                                                                xOffset += cardW*(-1 if i < mapDict.get('I')/2 else 1)
                                                        else: break
                                                x += xOffset
                                                
	card.moveToTable(x,y,True)
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

def showAltCard(card, x = 0, y = 0):
	mute()
	alt = card.alternates
	if 'B' in alt:
		if card.alternate == '':
			notify("{} flips {} to the alternate version of the card.".format(me, card))
			card.switchTo("B")
		else:
			notify("{} flips {} to the standard version of the card.".format(me, card))
			card.switchTo()

#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

#---------------------------------------------------------------------------
# Workflow routines
#---------------------------------------------------------------------------

def playSoundFX(sound):
	mute()

	#is the setting on?
	if not getSetting("AutoConfigSoundFX", True):
		return
	else:
		playSound(sound)

def initializeGame():
    mute()
    #### LOAD UPDATES
    v1, v2, v3, v4 = gameVersion.split('.')  ## split apart the game's version number
    v1 = int(v1) * 1000000
    v2 = int(v2) * 10000
    v3 = int(v3) * 100
    v4 = int(v4)
    currentVersion = v1 + v2 + v3 + v4  ## An integer interpretation of the version number, for comparisons later
    lastVersion = getSetting("lastVersion", convertToString(currentVersion - 1))  ## -1 is for players experiencing the system for the first time
    lastVersion = int(lastVersion)
    for log in sorted(changelog):  ## Sort the dictionary numerically
        if lastVersion < log:  ## Trigger a changelog for each update they haven't seen yet.
            stringVersion, date, text = changelog[log]
            updates = '\n-'.join(text)
            confirm("Documentation available in v.{} ({}):\n-{}".format(stringVersion, date, updates))
    setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def getStat(stats, stat): #searches stats string for stat and extract value
	statlist = stats.split(", ")
	for statitem in statlist:
		statval = statitem.split("=")
		if statval[0] == stat:
                        return (0 if statval[1]=='-' else int(statval[1]))
	return 0

def switchPhase(card, phase, phrase):
	global mycolor
	global playerNum
	global currentPhase
	mute()
	currentPhase = phase
	if debugMode:	#debuggin'
		card.switchTo(phase)
		notify("Phase changed to the {}".format(phrase))
		return True
	else:
		doneWithPhase = getGlobalVariable("DoneWithPhase")
		if str(playerNum) in doneWithPhase:
			return

		doneWithPhase += str(playerNum)
		if len(doneWithPhase) != len(players):
			setGlobalVariable("DoneWithPhase", doneWithPhase)
			if card.controller == me:
				card.highlight = mycolor
			else:
				remoteCall(card.controller, "remoteHighlight", [card, mycolor])
			notify("{} is done with the {}".format(me.name,card.Name))
			return False
		else:
			setGlobalVariable("DoneWithPhase", "")
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

def findDiscount(cspell,cdiscount): #test if spell satisfies requirements of discount card
	global discountsUsed

	#build test list from spell
	testlist = cspell.Type.split(",")
	testlist += cspell.Subtype.split(",")
	testlist += cspell.School.split(",")
	for i in range(len(testlist)):
		testlist[i] = testlist[i].strip().strip("]").strip("[")
	debug("casting discount testlist: {}".format(testlist))

	#discount already used?
	discountUsed = 0
	tuplist = [tup for tup in discountsUsed if tup[0] == cdiscount.Name]
	if len(tuplist) > 0:
		if tuplist[0][2] >= tuplist[0][1]:
			discountUsed += 1

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
		if discountUsed == 0:
			return discount
		else:
			return -1

def doDiscount(cdiscount):
	global discountsUsed
	lines = cdiscount.Text.split("[Casting Discount]")
	cells = lines[1].split(']')
	for i in range(len(cells)):
		cells[i] = cells[i].strip().strip("]").strip("[")

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

def castSpell(card, x = 0, y = 0):
	global infostr
	global Magebind
	castingCost = ""
	TraitStr = ""
	discountStr = ""

	if card.Cost != "" and card.Cost != None:
		if not "Enchantment" in card.Type:  # Attack, Creature, Conjuration, Equipment, and Incantation spells
			if "X" in card.Cost:  # e.g. Dispel
				castingCost = 0
			else:
				castingCost = int(card.Cost)

			infostr = "The printed casting cost of {} is {}".format(card.Name, castingCost)
			notifyStr = "{} turns '{}' face up, it has a printed casting cost of {}".format(me.name, card.Name, str(castingCost))

		else:  # Enchantment Spells
			#  Check to see if the player wants to reveal the Enchantment
			if getSetting("EnchantPromptReveal", False):
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("Would you like to reveal this hidden enchantment?", choiceList, colorsList)
				if choice == 0 or choice == 2:
					return

			#  castingCost = 2	# when we get attaching enchantments down
			revealCost = card.Cost.split("+")
			debug("debug: Casting Cost:{} and Reveal Cost:{}".format(revealCost[0], revealCost[1]))
			if "X" in card.Cost:  # e.g. Charm
				mageRevealCost = 0
			elif int(revealCost[1]) == 0:  #e.g. Brace Yourself
				flipcard(card, x, y)
				notify("{} revealed {} as it has a '0' reveal cost".format(me.name, card.Name))
				return
			else:
				mageRevealCost = int(revealCost[1])  # the second number (reveal cost)

			# if card has the Magebind trait, how much does it add to the reveal cost?
			if card.controller == me and "Magebind" in card.Traits:
				TraitValue, TraitStr = getTraitValue(card, Magebind)
				# Are we targeting a Mage with this Enchantment?
				castingCost = int(chooseMagebind(card, mageRevealCost, TraitValue))
			else:
				castingCost = mageRevealCost
				infostr = "The printed reveal cost of {} is {}".format(card.Name, mageRevealCost)
			notifyStr = "{} turns '{}' face up, it has a printed reveal cost of  {}".format(me.name, card.Name, str(mageRevealCost))

		# find any discounts from equipment(School, Type, Subtype, Targetbased?)
		discount = 0
		foundDiscounts = [ ]
		for c in table:
			if c.controller == me and c.isFaceUp and "[Casting Discount]" in c.Text and c != card and c.name != "Enchanter's Ring":
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
		infostr += "\nTotal mana amount to subtract from mana pool?"
		manacost = askInteger(infostr, castingCost - discount)

		# Do we have enough mana to pay for the spell?
		if manacost == None:
			# player closed the window and didn't cast the spell
			return
		if me.Mana < manacost:
			if not debugMode:
				notify("{} has insufficient mana in pool".format(me))
				# player is unable to pay for the spell
				return
			else:
				notify("{} has insufficient mana in pool".format(me))
				flipcard(card, x, y)
				return

		# Pay casting/reveal costs, register discounts, notify in chat window and flip the card face up
		for dc in foundDiscounts:
			doDiscount(dc)
		me.Mana -= manacost
		if not card.isFaceUp:
			flipcard(card, x, y)
			notify("{}".format(notifyStr))
		else:
			boundStr = "{} casts '{}' which is Spellbound, it has a printed casting cost of {}".format(me.name, card.Name, str(castingCost))
			if not discountStr == "":
				boundStr = boundStr + discountStr
			notify("{}".format(boundStr))
		if not TraitStr == "":
			notify("{}".format(TraitStr))
		notify("{} payed {} mana from pool for '{}'".format(me.name, manacost, card.Name))

def getTraitValue(card, TraitName):
	listofTraits = ""
	debug("{} has the {} trait".format(card.name, TraitName))
	listofTraits = card.Traits.split(", ")
	debug("{} ".format(listofTraits))
	if not len(listofTraits) > 1:
		strTraits = ''.join(listofTraits)
	else:
		for traits in listofTraits:
			if TraitName in traits:
				strTraits = ''.join(traits)
	STraitCost = strTraits.split("+")
	if STraitCost[1] == "X":
		infostr = "The spell {} has an Upkeep value of 'X' what is its value?".format(card.Name)
		TraitCost = askInteger(infostr, 3)
	else:
		TraitCost = int(STraitCost[1])
	TraitStr = "{} '{}' has the {}+{} trait".format(me.name, card.Name, STraitCost[0], TraitCost)
	return (TraitCost, TraitStr)

def chooseMagebind(card, mageRevealCost, TraitCosts):
	global infostr
	choiceList = ['Yes', 'No']
	colorsList = ['#0000FF', '#FF0000']
	choice = askChoice("Is the target of this Enchantment a Mage?", choiceList, colorsList)
	infostr = "The printed reveal cost of {} is {}".format(card.Name, mageRevealCost)
	if choice == 1:  # Enchantment is targeting a Mage
		mcastingCost = int(mageRevealCost) + int(TraitCosts)
		infostr += "\n+ {} to bind the spell to a Mage".format(TraitCosts)
	else:  # Enchatment is not targeting a Mage
		mcastingCost = int(mageRevealCost)
	return mcastingCost

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
				debug("Druid Water test: {}".format(card.Name))
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
			if "Warlock" in magename:
				magename = "Warlock"
			if "Warlord" in magename:
				magename = "Warlord"
			if "Priestess" in magename:
				magename = "Priestess"
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

############################################################################
############################	   Map Construction     ####################
############################################################################

def importArray(filename):
        """Takes a txt character array and outputs a dictionary of arrays (sets of columns). To get an entry from an array, use array[x][y]"""
        #Open the file
        directory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('maps')
        try: raw = open('{}\{}{}'.format(directory,filename,'.txt'),'r')
        except: return #Bad practice, I know. I'll try to find a better way later.
        #Create an empty array.
        #Because of the order in which data are read, we will need to transpose it.
        transposeArray = []
        #Fill up the transposed array, as a set of rows.
        scenarioDict = {}
        dictKey = None
        for line in raw:
                if line == '\n': pass #ignore blank lines
                elif line[0] != '#':
                        row = []
                        for char in range(len(line)):
                            if line[char] != '\n':
                                row.append(line[char])
                        transposeArray.append(row)
                else:
                        dictKey = line.replace('\n','').strip('#')
                        X0 = len(transposeArray[0])
                        X1 = len(transposeArray)
                        array = [[transposeArray[x1][x0] for x1 in range(X1)] for x0 in range(X0)]
                        transposeArray = []
                        scenarioDict[dictKey] = array
        return scenarioDict

def loadMapFile(group, x=0, y=0):
        mute()
        directory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('maps')
        fileList = [f.split('.')[0] for f in os.listdir(directory) if (os.path.isfile(os.path.join(directory,f)) and f.split('.')[1]=='txt')]
        choices = fileList+['Cancel']
        colors = ['#6600CC' for f in fileList] + ['#FF0000']
        choice = askChoice('Load which map?',choices,colors)
        if choice == 0 or choice == len(choices): return
        scenario = importArray(fileList[choice-1])
        notify('{} loads {}.'.format(me,fileList[choice-1]))
        
        mapArray = scenario.get('Map',False)
        objectsArray = scenario.get('Objects',False)
        creaturesArray= scenario.get('Creatures',False)

        for card in table:
                if (card.type == "Internal" or
                    card.name in ["Sslak, Orb Guardian","Usslak, Greater Orb Guardian"]): card.delete() #We need a way to distinguish between scenario guardians and those in spellbooks
	setNoGameBoard(table)

        #iterate over elements, top to bottom then left to right.
        I,J = len(mapArray),len(mapArray[0])
        X,Y = I*mapTileSize,J*mapTileSize
        x,y = (-X/2,-Y/2) #Do we want 0,0 to be the center, or the upper corner? Currently set as center.

        zoneArray = mapArray
        
        for i in range(I):
                for j in range(J): #Might as well add support for non-rectangular maps now. Though this won't help with the rows.
                        if mapArray:
                                tile = mapTileDict.get(mapArray[i][j],None)
                                SPT = (True if tile == "c3e970f7-1eeb-432b-ac3f-7dbcd4f45492" else False) #Spiked Pit Trap
                                zoneArray[i][j] = (1 if tile else 0)
                                if tile:
                                        tile = table.create(tile,x,y)
                                        tile.anchor = True
                                        if SPT: table.create("8731f61b-2af8-41f7-8474-bb9be0f32926",x+mapTileSize/2,y+mapTileSize/2) #Add trap marker
                                        #It doesn't look like this is the correct identifier for trap markers.
                        y += mapTileSize
                x += mapTileSize
                y = -Y/2
        x = -X/2

        mapDict = createMap(I,J,zoneArray,mapTileSize)
                        
        for i in range(I): #For some reason, I can't get the map tiles to be sent to the back successfully. So we'll do this in two parts.
                for j in range(J):
                        if objectsArray:
                                obj = mapObjectsDict.get(objectsArray[i][j],None)
                                if obj:
                                        duplicate = objectsArray[i][j].istitle()
                                        table.create(obj,
                                                     x+mapObjectOffset,
                                                     y+mapObjectOffset)
                                        if duplicate:
                                                table.create(obj,
                                                                   x+mapObjectOffset+mapMultipleObjectOffset,
                                                                   y+mapObjectOffset)
                        if creaturesArray:
                                if creaturesArray[i][j] in ['1','2','3','4','5','6']: mapDict.get('zoneArray')[i][j]['startLocation'] = creaturesArray[i][j]
                                cre = mapCreaturesDict.get(creaturesArray[i][j],None)
                                if cre:
                                        duplicate = creaturesArray[i][j].istitle()
                                        table.create(cre,
                                                     x+mapCreatureOffset,
                                                     y+mapCreatureOffset)
                                        if duplicate: table.create(cre,
                                                                   x+mapCreatureOffset+mapMultipleCreatureOffset,
                                                                   y+mapCreatureOffset)
                        y += mapTileSize
                x += mapTileSize
                y = -Y/2

        setGlobalVariable("Map",str(mapDict))
       
### Map Definitions ###

mapTileSize = 250
mapObjectOffset = 175
mapMultipleObjectOffset = -100
mapCreatureOffset = 0
mapMultipleCreatureOffset = 62

mapTileDict =  {
                "1" : "5fbc16dd-f861-42c2-ad0f-3f8aaf0ccb64", #Dropped Weapon
                "2" : "6136ff26-d2d9-44d2-b972-1e26214675b5", #Corrosive Mist
                "3" : "8972d2d1-348c-4c4b-8c9d-a1d235fe482e", #Altar of Oblivion
                "4" : "a21d1889-acf1-4121-b1d1-991f3f294f1d", #Secret Passage
                "5" : "a47fa32e-ac83-4ced-8f6a-23906ee38880", #Septagram
                "6" : "bf833552-8ee4-4c62-abd2-83da233da4ce", #Molten Rock
                "7" : "c3e970f7-1eeb-432b-ac3f-7dbcd4f45492", #Spiked Pit
                "8" : "cc063a84-2ba4-4f18-8a09-6e5a4e57ab5b", #Muddy Tile
                "9" : "dda1f46d-2e0a-4be8-b85a-2d25bbc40a12", #Boneyard
                "A" : "edca7d45-53e0-468d-83a5-7a446c81f070", #Samandriel's Circle
                "B" : "f8d70e09-2734-4de8-8351-66fa98ae0171", #Ethereal Mist
                "C" : "f8794ef9-e78f-412b-95d4-37dc055be158", #Debris
                "." : "4f1b033d-7923-4e0e-8c3d-b92ae19fbad1", #Generic Tile
                "D" : "0011a67e-df97-42f0-bdd2-1fe7f733b702", #Westlock 1
                "E" : "0191ddc0-ef8d-499a-b6a4-f9e0f01da219", #Westlock 2
                "F" : "023336ec-9969-4832-bbb7-b071b0b55906", #Westlock 3
                "G" : "035c27ba-d619-43dd-99f7-ecec7852913d", #Westlock 4
                "H" : "06a26b95-1821-411f-818c-359122845731", #Westlock 5
                "I" : "07cbfb65-3469-4aad-91c9-bcdd6bf4433c", #Westlock 6
                "J" : "0843b7ef-fdfb-411d-a1dd-d36e752d94d0", #Westlock 7
                "K" : "0908af74-c087-4624-ae23-4807cdce2727", #Westlock 8
                "L" : "0af23def-171a-4adb-bf05-0d958d824d5d", #Westlock 9
                "M" : "0b43f1c1-21c7-4083-a46f-e8a50f8035d7", #Westlock 10
                "N" : "0c14ca09-a83d-4185-afa0-bc38a31dbf82", #Westlock 11
                "O" : "0f14ca09-a83d-4185-afa0-bc38a31dbf82", #Westlock 12
                "P" : "24ae46c1-dd54-427b-bb4c-9e24aead34f5", #Salenia 1
                "Q" : "12bd0a8a-2eec-4cf3-b14e-6861de1d7a19", #Salenia 2
                "R" : "3ead8317-1867-4ccc-850d-dae7590137af", #Salenia 3
                "S" : "92e1afc0-d7de-434e-94ae-d7fb4fdbd744", #Salenia 4
                "T" : "17b4d74b-2bcd-476c-b3e7-2adb83c6c20f", #Salenia 5
                "U" : "8dd2393e-8fc8-4611-82de-d67aee5c2cbb", #Salenia 6
                "V" : "94908e50-bb5b-49fb-b3ba-94b467e9ea5a", #Salenia 7
                "W" : "e21d2461-8021-4b19-8eed-9bfd8e247b20", #Salenia 8
                "X" : "20313020-24ce-4149-9c30-775794d80a1e", #Salenia 9
                "Y" : "bcfe0daa-a4aa-4de1-868f-9132010f026c", #Salenia 10
                "Z" : "ec03ac8c-7ffb-4d36-8d8e-189fa83a776f", #Salenia 11
                "a" : "2d4a47ee-81e0-48f0-acb6-ec8e8d2a5826", #Salenia 12
                "b" : "43dc59fa-dd87-47ac-a4d6-574f7cec609c", #Apprentice Mode 1
                "c" : "62846feb-893c-40c5-8138-0777a24c8c73", #Apprentice Mode 2
                "d" : "f88b4ac6-b2da-48da-86a1-5213fe9e34be", #Apprentice Mode 3
                "e" : "3421bf20-a06f-4fc0-aac0-35a053e3c799", #Apprentice Mode 4
                "f" : "707e1095-18df-491a-afca-b32b0cfce67c", #Apprentice Mode 5
                "g" : "485fa227-2f6a-42b8-a112-0b97a9cf6317" #Apprentice Mode 6      	
                } 

mapObjectsDict = {"o" : "690a2c72-4801-47b5-84bd-b9e2f5811cb5",	# A V'Tar Orb
                  "O" : "690a2c72-4801-47b5-84bd-b9e2f5811cb5"}	# 2 V'Tar Orbs
        
mapCreaturesDict =     {"s" : "bf217fd3-18c0-4b61-a33a-117167533f3d",	# Orb Guardian
                        "S" : "bf217fd3-18c0-4b61-a33a-117167533f3d",	# 2 Orb Guardians
                        "u" : "54e67290-5e6a-4d8a-8bf0-bbb8fddf7ddd",	# Greater Orb Guardian
                        "U" : "54e67290-5e6a-4d8a-8bf0-bbb8fddf7ddd"}	# 2 Greater Orb Guardians
