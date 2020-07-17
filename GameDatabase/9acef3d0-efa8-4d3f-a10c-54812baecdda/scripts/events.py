#######
#v3.0.0.0#
#######

def onTableLoaded():
	mute()
	#log in chat screen what version of the game definiton the player is using
	notify("{} is running v.{} of the Mage Wars module.".format(me, gameVersion))
	#if there's only one player, go into debug mode

def onGameStarted():
	mute()
	global debugMode
	#Set default map
	defineRectangularMap(4,3,250)

	#set the Game Host (this player will be the owner of the Initative and Phase Markers)
	setGlobalVariable("GameHostID",str((sorted([x._id for x in getPlayers()])[0])))

	#create a dictionary of attachments and bound spells and enable autoattachment
	setGlobalVariable("attachDict",str({}))
	setGlobalVariable("bindDict",str({}))
	setSetting("AutoAttach", True)

	#set global event lists for rounds and single actions
	setGlobalVariable("roundEventList",str([]))
	setGlobalVariable("turnEventList",str([]))

	#above to be replaced with consolidated game memory:
	setGlobalVariable("gameMemory",str([]))

	#Set the round to 0
	setGlobalVariable("RoundNumber", str(1))
	setGlobalVariable("timerIsRunning",str(False))

	#set the goal
	setGlobalVariable("Goal",str({}))

	# bring up window to point to documentation
	documentationReminder()
	#new Player Order
	setGlobalVariable("PlayersIDList",str([]))
	setGlobalVariable("MWPlayerDict",str({}))
	gameHost = Player(int(getGlobalVariable("GameHostID")))

	if me == gameHost:
		setRDALocation()
		if getSetting("AutoBoard", True):
			chooseGame()
		else:
			table.board = "Westlock - 4X3"
			setGlobalVariable("GameMode", "Arena")

	#if there's only one player, go into debug mode
	if len(getPlayers()) == 1:
		#debugMode = True
		setGlobalVariable("PlayerWithIni", str(me._id))
		setGlobalVariable("MWPlayerDict",str({1:{"PlayerNum": 1,"PlayerName":me.name}}))
		me.setGlobalVariable("MyColor",str(4)) #Purple for testing
		me.color = playerColorDict[eval(me.getGlobalVariable("MyColor"))]['Hex']
		setUpDiceAndPhaseCards()
		setGlobalVariable("GameSetup",str(0))
		publicChatMsg("There is only one player, so there is no need to roll for initative.")
		#publicChatMsg("Enabling debug mode. In debug mode, deck validation is turned off and you can advance to the next phase by yourself.")
		tutorialMessage("Introduction")
		tutorialMessage("Load Deck")
		setPhase(5)
	else:
		choosePlayerColor()
		if gameHost == me:
			remoteCall(me,"finishSetup",[])

#OnGameStarted Event Functions#
def chooseGame():
	mute()
	#buttonColorList = ["#de2827","#171e78","#01603e","#f7d917","#c680b4","#c0c0c0"];
	#choiceList = ["Mage Wars Arena","Wage Wars Arena: Domination","Mage Wars Arena: Co-Op Teams","Mage Wars Arena: Domination Co-Op Teams","Mage Wars Academy","Mage Wars Academy: Co-Op Teams"];
	buttonColorList = ["#de2827","#171e78", "#01603e"];
	choiceList = ["Mage Wars Arena","Mage Wars Arena: Domination", "Mage Wars Arena: Community Playtest Rules"];

	while (True):
		choice = askChoice("What would you like to Play?", choiceList, buttonColorList)
		if choice == 1:
			setGlobalVariable("GameMode", "Arena")
			setArenaBoard()
			break
		elif choice == 2:
			setGlobalVariable("GameMode", "Domination")
			loadMapFile()
			break
		elif choice == 3:
			setGlobalVariable("GameMode", "Playtest")
			setArenaBoard()
			break
	'''	elif choice == 3:
			setGlobalVariable("GameMode", "ArenaCoOpTeamPlay")
			setArenaBoard()
		elif choice == 4:
			setGlobalVariable("GameMode", "DominationCoOpTeamPlay")
			loadMapFile2()
		elif choice == 5:
			setGlobalVariable("GameMode", "Academy")
		elif choice == 6:
			setGlobalVariable("GameMode", "AcademyArenaCoOpTeamPlay")'''

def setArenaBoard(): # should this be moved to arena.py?
	mute()
	boardButtonColorList = []
	boardList = []
	for num in gameBoardsDict:
		boardButtonColorList.append(gameBoardsDict[num]["buttonColor"])
		boardList.append(gameBoardsDict[num]["boardName"])
	while (True):
		choice = askChoice("Which Arena Game board would you like to to Use?", boardList, boardButtonColorList)
		if choice >= 1:
			notify('{} loads {}.'.format(me,boardList[choice-1]))
			break
	table.board = gameBoardsDict[choice]["boardName"]
	zoneDef = gameBoardsDict[choice]["zoneDef"]
	defineRectangularMap(zoneDef[0],zoneDef[1],zoneDef[2])
	return

def setAcademyBoard():
	mute()
	#For now, let's just define a region of the appropriate size. We also need an image (or do we?)
	table.board = gameBoardsDict[10]["boardName"]
	defineRectangularMap(1,1,900)

def defineRectangularMap(I,J,tilesize):
	mapDict = createMap(I,J,[[1 for j in range(J)] for i in range(I)],tilesize)
	#If the map is a single zone, then all start locations are the same.
	if len(mapDict['zoneArray'][0]) == 1 and len(mapDict['zoneArray']) == 1:
		mapDict.get('zoneArray')[0][0]['startLocation'] = '*'
	#Otherwise, place them on opposite corners of the board
	else:
		mapDict.get('zoneArray')[0][0]['startLocation'] = '1'
		mapDict.get('zoneArray')[-1][-1]['startLocation'] = '2'
	mapDict["RDA"] = (2,2)
	setGlobalVariable("Map", str(mapDict))
	debug("AAAAA "+str(mapDict))

def choosePlayerColor():
	mute()
	colorsList = []
	colorsListHex = []
	#debugMode = eval(me.getGlobalVariable("DebugMode"))
	for num in playerColorDict:
			colorsListHex.append(playerColorDict[num]["Hex"])
			colorsList.append(playerColorDict[num]["PlayerColor"])
	if not debugMode or len(getPlayers()) > 0:
		while (True):
			choice = askChoice("Pick a color:", colorsList, colorsListHex)
			colorsChosen = getGlobalVariable("ColorsChosen")
			if choice == 0:
				askChoice("Please choose a color!", ["OK"], ["#FF0000"])
			elif colorsChosen == "":	#we're the first to pick
				setGlobalVariable("ColorsChosen", str(choice))
				me.setGlobalVariable("MyColor", str(choice))
				break
			elif str(choice) not in colorsChosen:	#not first to pick but no one else has taken this yet
				setGlobalVariable("ColorsChosen", colorsChosen + str(choice))
				me.setGlobalVariable("MyColor", str(choice))
				break
			else:	#someone else took our choice
				askChoice("Someone else took that color. Choose a different one.", ["OK"], ["#FF0000"])
		notify("{} chooses {}!".format(me.name,playerColorDict[choice]["PlayerColor"]))

def finishSetup(): #Waits until all players have chosen a color, then finishes the setup process.
	mute()
	#first, check whether all the players have chosen a color. If not, use remoteCall to 'bounce' finishSetup() off of OCTGN so that it checks again later.
	if len(getPlayers()) > len(getGlobalVariable("ColorsChosen")):
		remoteCall(me,"finishSetup",[])
		return
	#if everybody has chosen a color, finish the process of setting up
	PlayerSetup()
	#the Gamehost now sets up the Initative, Phase, and Roll Dice Area
	setUpDiceAndPhaseCards()
	notify("Players will now roll for initiative.")
	rollForInitative()
	for p in players:
		remoteCall(p, "tutorialMessage", ["Introduction"])
		remoteCall(p, "tutorialMessage", ["Load Deck"])

def PlayerSetup():
	mute()
	playersIDList = eval(getGlobalVariable("PlayersIDList"))
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))

	#creates a list of PlayerID's weeding out any Spectators who joined in the game lobby
	if eval(getGlobalVariable("PlayersIDList")) == []:
		for p in getPlayers():
			playersIDList.append(p._id)
			playersIDList.sort()
			setGlobalVariable("PlayersIDList",str(playersIDList))
	#creates a dictionary where { key is PlayerID : { PlayerNum, PlayerName }}
	playersIDList = eval(getGlobalVariable("PlayersIDList"))
	for i,j in enumerate(playersIDList, start=1):
		mwPlayerDict[j] = {"PlayerNum": (i),"PlayerName":Player(j).name}
		setGlobalVariable("MWPlayerDict",str(mwPlayerDict))

def setRDALocation():
	mute()
	if getSetting("RDALocation", True):
		notify("{} places the Roll Dice Area to the side of the Gameboard.".format(me))
	else:
		notify("{} places the Roll Dice Area to the Bottom of the Gameboard.".format(me))
		setGlobalVariable("DiceRollAreaPlacement", "Bottom")

def setUpDiceAndPhaseCards(): #some of this is for arena only, I think....
	mute()
	tableSetup = getGlobalVariable("TableSetup")
	myColor = me.getGlobalVariable("MyColor")
	gameHost = Player(int(getGlobalVariable("GameHostID")))
	if tableSetup == "False" and gameHost == me: #me.name == gameHost.name:
		RDA = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd",0,0) #Roll Dice Area
		RDA.anchor = (True)
		initativeCard = table.create("8ad1880e-afee-49fe-a9ef-b0c17aefac3f",0,0) #Initiative Marker
		initativeCard.anchor = (True)
		initativeCard.alternate = myColor
		setGlobalVariable("InitativeCard",str(initativeCard._id))
		#phaseCard = table.create("6a71e6e9-83fa-4604-9ff7-23c14bf75d48",0,0) #Phase Marker/Next Phase Button
		#phaseCard.anchor = (True)
		#phaseCard.alternate = "5" #Game starts at the Planning Phase
		#setGlobalVariable("PhaseCard",str(phaseCard._id))
		for c in table:
			if c.type in ['DiceRoll','Phase']: moveRDA(c)
		setGlobalVariable("TableSetup", True)

def rollForInitative():
	mute()
	effect = 0
	rollForPlayer = 0
	for p in getPlayers():
		notify("Automatically rolling initiative for {}...".format(p.name))
		effect = rnd(1,12)
		rollForPlayer += 1
		notify("{} rolled a {} for initiative".format(p.name, effect))
		myRollStr = (str(p._id) + ":" + str(effect) + ";")
		setGlobalVariable("OppIniRoll", getGlobalVariable("OppIniRoll") + myRollStr)
		update()

	#all initiatives rolled, see who had highest
	if getGlobalVariable("OppIniRoll").count(";") == len(getPlayers()):
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
				victoriousPlayerID = int(temp[0])
			elif int(temp[1]) == max:
				timesMaxRolled += 1

		# we got a tie in there somewhere. determine winner randomly from high rollers
		if timesMaxRolled > 1:
			notify("High roll tied! Randomly determining initiative...")
			highRollerPlayerNums = []
			for roll in rollStringList:
				if roll == "":
					continue
				temp = roll.split(":")
				if int(temp[1]) == max:
					highRollerPlayerNums.append(int(temp[0]))
			victoriousPlayerID = highRollerPlayerNums[rnd(0, len(highRollerPlayerNums) - 1)]
			debug(str(victoriousPlayerID))

		remoteCall(Player(victoriousPlayerID), "AskInitiative", [victoriousPlayerID])
	else:
		notify("Something unexpected happened and the automation for Initative has failed! Setting the game host as the player to choose Initative!")
		gameHost = Player(int(getGlobalVariable("GameHostID")))
		remoteCall(gameHost, "AskInitiative", [1])

def AskInitiative(playerID):
	mute()
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	notify("{} has won the Initative Roll and is deciding who should go first.".format(me))
	players = getPlayers()
	choices = [p.name + (" (me)" if p==me else "") for p in players]
	colors = [(playerColorDict[int(p.getGlobalVariable("MyColor"))]["Hex"]) for p in players]
	#To simplify the process of determining initiative, we will have the initiative winner explicitly decide who goes first.
	while True:
		choice = askChoice("Who should go first?",choices,colors)
		if choice == 0: continue
		firstPlayer = players[choice - 1]
		playerID = firstPlayer._id
		notify("A decision has been reached! {} will go first.".format(firstPlayer))
		setGlobalVariable("PlayerWithIni", str(playerID))
		initativeCard = Card(int(getGlobalVariable("InitativeCard")))
		initativeCard.alternate = Player(playerID).getGlobalVariable("MyColor")
		break
	setGlobalVariable("GameSetup", str(0))
	notify("Game setup is complete! Players should now load their Spellbooks.")
	nextTurn()
	setPhase(5)

def moveRDA(card):
	"""Moves the dice roll area/initiative/phase marker to the appropriate area"""
	cardW,cardH = cardSizes[card.size]['width'],cardSizes[card.size]['height']
	cardType = card.type
	rdaChoice = getGlobalVariable("DiceRollAreaPlacement")
	mapDict = eval(getGlobalVariable("Map"))
	mapX,mapY = mapDict["x"],mapDict["y"]
	zoneS = mapDict["tileSize"]
	rdaI,rdaJ = mapDict["RDA"]
	mapHeight = mapDict["Y"]

	rowY = mapY + rdaJ*zoneS
	columnX = mapX + rdaI*zoneS

	x,y = 0,0

	if cardType == "DiceRoll":
		if rdaChoice == "Side":
			x = mapX - cardW - 10
			y = rowY - zoneS + 100
		else:
			x = columnX - zoneS
			y = mapY + mapHeight + 100
		mapDict['DiceBoxLocation'] = (x,y)
		setGlobalVariable("Map",str(mapDict))

	elif 'Player Token' in card.name:
		if rdaChoice == "Side":
			x = mapX - cardW - 10 - 100
			y = rowY - zoneS
		else:
			x = columnX - zoneS
			y = mapY + mapHeight + 10

	card.moveToTable(x,y,True)

def onDeckLoaded(args):
	#args = player,groups
	mute()
	global gameNum
	global debugMode
	if eval(getGlobalVariable("GameSetup")) == "False" and args.player == me:
		askChoice("Please Finish Setup before you try to load a deck.", ["OK"], ["#FF0000"])
		return
	if args.player == me:
		#if a deck was already loaded, reset the game
		if getGlobalVariable("DeckLoaded") == "True":
			notify ("{} has attempted to load a second Spellbook, the game will be reset".format(me))
			gameNum += 1
			resetGame()
		elif debugMode or validateDeck(args.groups[0]):
			setGlobalVariable("DeckLoaded", str(int(getGlobalVariable("DeckLoaded"))+1))
			if eval(getGlobalVariable("DeckLoaded")) == len(getPlayers()): setGlobalVariable("DeckLoaded","True")
			setGlobalVariable("GameSetup", str(int(getGlobalVariable("GameSetup"))+1))
			if eval(getGlobalVariable("GameSetup")) == len(getPlayers()): setGlobalVariable("GameSetup","True")
			mageDict = eval(me.getGlobalVariable("MageDict"))
			for card in me.piles["Spellbook"]:
				if card.Subtype == "Mage":
						mageDict["MageID"] = card._id
				elif card.Type == "Magestats":
						mageDict["MageStatsID"] = card._id
			me.setGlobalVariable("MageDict",str(mageDict))
			tutorialMessage("Play Card")
		else:
			#publicChatMsg and delete deck
			publicChatMsg("Validation of {}'s spellbook FAILED. Please choose another spellbook.".format(me.name))
			for group in args.groups:
				for card in group:
					if card.controller == me:
						card.delete()
	
#OnDeckLoaded Event Functions#
def mageSetup():
	#set initial health and channeling values
	for c in me.piles["Spellbook"]:
		if c.Subtype == "Mage":
			stats = c.Stats.split(",")
			#me.Mage = c.name - when #1278 happens and game Counters support strings....
			break
	for stat in stats:
		debug("stat {}".format(stat))
		statval = stat.split("=")
		if "Channeling" in statval[0]:
			me.Channeling = int(statval[1])
			me.Mana = 10+me.Channeling
			#if debugMode: me.Mana = 100
			whisper("Channeling set to {} and Mana to {}".format(me.Channeling,me.Mana))
		elif "Life" in statval[0]:
			me.Life = int(statval[1])
			whisper("Life set to {}".format(me.Life))

	setGlobalVariable("GameSetup", str(int(getGlobalVariable("GameSetup"))+1))
	if eval(getGlobalVariable("GameSetup")) == len(getPlayers()): setGlobalVariable("GameSetup","True")


###############################
######     Targeting     ######
###############################

passOnClick = None

def listenForClick(arg):
	global passOnClick
	whisper(arg.get("Click Prompt","Left click to select target"))
	passOnClick = arg

def onCardClicked(args):
	#args = card, mouseButton, keysDown
	global passOnClick
	if passOnClick != None: #TODO - restrict to only left click
		function,argument = passOnClick["function"],passOnClick
		argument["target"] = args.card
		function(argument)
		passOnClick = None

###############################

#def onMoveCards(player,cards,fromGroups,toGroups,oldIndices,indices,oldXs,oldYs,xs,ys,highlights,markers,faceup):
def onCardsMoved(args):
	#args = player,cards,fromGroups,toGroups,indexs,xs,ys,highlights,markers,faceups
	mute()
	setGlobalVariable("MoveCardArgs",str(args))
	#assign variables when appropriate to cut down on memory access operations
	cards = args.cards
	toGroups = args.toGroups
	fromGroups = args.fromGroups
	xs = args.xs
	ys = args.ys
	indices = args.indexs
	#loop over all cards
	for i, card in enumerate(cards):
	  	position = card.position
	  	if card.controller == me and fromGroups[i]==table:
			if not (getAttachTarget(card) in cards or getBindTarget(card) in cards): #Only check for detach if the attachtarget was not moved
				unbind(card)
				c,t = detach(card)
				if toGroups[i] == table: card.moveToTable(position[0],position[1])#ugly, but fixes a bug that was preventing all but the first detached enchantment from moving.
				actionType = None
				if t:
					actionType = ['detaches','from']
				hasAttached = False
				if len(cards) == 1 and toGroups[i] == table: #Only check for autoattach if this is the only card moved
					for a in table:
						if (cardX(a)-position[0])**2 + (cardY(a)-position[1])**2 < 400 and canBind(card,a):
							c,t = bind(card,a)
							if t:
								actionType = ['binds','to']
								hasAttached = True
								break
						elif getSetting('AutoAttach',True) and (cardX(a)-position[0])**2 + (cardY(a)-position[1])**2 < 400 and canAttach(card,a):
							if (card.Type == "Enchantment" or card.Name in ["Tanglevine","Stranglevine","Quicksand"]) and not card.isFaceUp and not castSpell(card,a): break
							c,t = attach(card,a)
							if t:
								actionType = ['attaches','to']
								hasAttached = True
								break
				if (not hasAttached) and (toGroups[i] == table): snapToZone(card)
				if actionType:
					notify("{} {} {} {} {}.".format(me,actionType[0],c,actionType[1],t))
				if toGroups[i] != table:
					unbind(card)
					detach(card)
					detachAll(card)
					unbindAll(card)
				if not ((indices[i] != position and xs[i]==str(int(position[0])) and ys[i]==str(int(position[1]))) or
					isAttached(card) or
	  				getBindTarget(card) or
	  				toGroups[i] != table):
	  				alignAttachments(card)
	  				alignBound(card)#Do not realign if it is  only the index that is changing. Prevents recursions.

def onScriptedCardsMoved(args):
	#assign variables to args before the loop to cut down on memory access operations
	cards = args.cards
	toGroups = args.toGroups
	indices = args.indexs
	xs = args.xs
	ys = args.ys
	#handle attached cards when attach target is moved/deleted by a function
	for i in range(len(cards)):
		card = cards[i]
		position = card.position
		if toGroups[i] != table:
			unbind(card)
			detach(card)
			detachAll(card)
			unbindAll(card)
		if not ((indices[i] != position and xs[i]==str(int(position[0])) and ys[i]==str(int(position[1]))) or
			isAttached(card) or
			getBindTarget(card) or
			toGroups[i] != table):
			alignAttachments(card)
			alignBound(card)


def onCardArrowTargeted(args):
	#args = player,fromCard,toCard,targeted,scripted
	mute()
	source,target = args.fromCard,args.toCard #Should probably make an attack declaration function. Eventually.
	if args.player == me == source.controller and args.targeted and not args.scripted and getSetting("DeclareAttackWithArrow",True): targetMenu(source,target)
# WIP - Tinkering required

def onCardDoubleClicked(args):
	#args = card, mouseButton, keysDown
	mute()
	if args.card.type == "DiceRoll":
		genericAttack(0)

	if args.card.type =="Phase":
		nextPhase(table)


def checkMageDeath(args):
	#args = player,counter,value,scripted
	mute()
	if getGlobalVariable("GameSetup") == "True" and me.Damage >= me.Life and askChoice('          Your Mage has fallen in the Arena! \n\nDo you wish to continue playing until the end of the current Phase?',['Yes','No'],["#01603e","#de2827"]) == 2:
			for card in table:
					if card.Subtype == "Mage" and card.controller == me:
							card.orientation = 1
							#playSoundFX('Winner')
							for p in players:
									remoteCall(p, "reportDeath",[me])
	#reportGame('MageDeath')

def reportDeath(deadmage):
	setGlobalVariable("GameIsOver", "True")
	setGlobalVariable("GameEndTime", str(time.ctime()))
	whisper("{} has fallen in the arena! At {} after {} Rounds.".format(deadmage, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")))
	choice = askChoice("{} has fallen in the arena! At {} after {} Rounds.".format(deadmage, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")), ['OK'], ['#de2827'])
	endingStats()
	if choice == 0 or 1:
		return

def reportVTarWin(winningmage,score):
	setGlobalVariable("GameIsOver", "True")
	setGlobalVariable("GameEndTime", str(time.ctime()))
	whisper("{} has won the Domination Match with a total of {} V'Tar! At {} after {} Rounds.".format(winningmage,score, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")))
	choice = askChoice("{} has won the Domination Match with a total of {} V'Tar!! At {} after {} Rounds.".format(winningmage, score, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")), ['OK'], ['#de2827'])
	endingStats()
	if choice == 0 or 1:
		return

def concede(group=table, x = 0, y = 0):
	mute()
	if confirm("Are you sure you want to concede this game?"):
		setGlobalVariable("GameIsOver", "True")
		setGlobalVariable("GameEndTime", str(time.time()))
		for c in table:
			if c.Subtype == "Mage" and c.controller == me:
				c.orientation = 1
		# reportGame('Conceded')
		notify("{} has conceded the game".format(me))
		endingStats()
	else:
		notify("{} was about to concede the game, but thought better of it...".format(me))


def playerStats():
	mute()
	if getGlobalVariable("GameIsOver") == "True":
		notify("Player Stats at the end of the Match")
	notify("\nAt the Start of Round #{}, {}'s Mage has the following stats: Channeling: {}, Mana Pool {}, Life {}, and Damage {}.".format(getGlobalVariable("RoundNumber"),me.name,me.channeling,me.mana,me.life,me.damage))