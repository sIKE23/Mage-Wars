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

	#if there's only one player, go into debug mode - Currently does not go into debug mode so players can validate decks
	if len(getPlayers()) == 1:
		#debugMode = True
		setGlobalVariable("PlayerWithIni", str(me._id))
		setGlobalVariable("MWPlayerDict",str({1:{"PlayerNum": 1,"PlayerName":me.name}}))
		me.setGlobalVariable("MyColor",str(4)) #Purple for testing
		me.color = playerColorDict[eval(me.getGlobalVariable("MyColor"))]['Hex']
		setUpDiceAndPhaseCards()
		setGlobalVariable("GameSetup",str(0))
		#publicChatMsg("There is only one player, so there is no need to roll for initative.")
		#publicChatMsg("Enabling debug mode. In debug mode, deck validation is turned off and you can advance to the next phase by yourself.")
		tutorialMessage("Introduction")
		tutorialMessage("Load Deck")
		setPhase(5)
	else:
		choosePlayerColor()
		if gameHost == me:
			remoteCall(me,"finishSetup",[])

#Called by onGameStarted()
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

#Called by defineRectangularMap()
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

#Called by createMap()
def createZone(i,j,mapX,mapY,size):
	return  {'i' : i,
			 'j' : j,
			 'x' : mapX+i*size,
			 'y' : mapY+j*size,
			 'size' : size}

#Called by onGameStarted()
def setRDALocation():
	mute()
	if getSetting("RDALocation", True):
		notify("{} places the Roll Dice Area to the side of the Gameboard.".format(me))
	else:
		notify("{} places the Roll Dice Area to the Bottom of the Gameboard.".format(me))
		setGlobalVariable("DiceRollAreaPlacement", "Bottom")

#Called by onGameStarted()
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

#Called by chooseGame()
def setArenaBoard(): 
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

#Called by onGameStarted()
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

#Called by onGameStarted()
def finishSetup(): #Waits until all players have chosen a color, then finishes the setup process.
    mute()
    #first, check whether all the players have chosen a color. If not, use remoteCall to 'bounce' finishSetup() off of OCTGN so that it checks again later.
    if len(getPlayers()) > len(getGlobalVariable("ColorsChosen")):
        remoteCall(me,"finishSetup",[])
        return
    #if everybody has chosen a color, finish the process of setting up
    PlayerSetup()
    #the Gamehost now sets up the Phase and Roll Dice Area
    setUpDiceAndPhaseCards()
    setGlobalVariable("GameSetup", str(0))
    setGlobalVariable("MageRevealed", str(0))
    notify("Game setup is complete! Players should now load their Spellbooks.")
    nextTurn()
    setPhase(5)
    for p in players:
        remoteCall(p, "tutorialMessage", ["Introduction"])
        remoteCall(p, "tutorialMessage", ["Load Deck"])

#Called by finishSetup()
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

#Called by finishSetup()
def setUpDiceAndPhaseCards(): 
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
		for c in table:
			if c.type in ['DiceRoll','Phase']: moveRDA(c)
		setGlobalVariable("TableSetup", True)

#Called by setUpDiceAndPhaseCards()
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
            #publicChatMsg("Validation of {}'s spellbook FAILED. Please choose another spellbook.".format(me.name))
            for group in args.groups:
                for card in group:
                    if card.controller == me:
                        card.delete()



#Called by flipcard() when a mage is flipped for the first time
def mageSetup():
    mute()
    mageDict = eval(me.getGlobalVariable("MageDict"))
    if mageDict["MageStatsID"] == 00000 or mageDict["MageRevealed"] == "True": return #deck hasn't been loaded or the mage the mage card was flipped face down after mageSetup() has already run once
    mageID = int(mageDict["MageID"])
    mage = Card(mageID)
    mageStatsID = int(mageDict["MageStatsID"])
    magestats = Card(mageStatsID)
    #set initial health and channeling values
    me.Channeling = int(magestats.StatChanneling)
    me.Mana = me.Channeling + 10 + int(magestats.StatStartingMana)
    me.Life = int(magestats.StatLife)
    Card(mageID).Subtype = magestats.Subtype
    Card(mageID).Level = magestats.Level
    Card(mageID).Stats = magestats.Stats #havent decided if this is needed yet....proxygen??
    Card(mageID).AttackBar = magestats.AttackBar
    Card(mageID).Traits = magestats.Traits
    Card(mageID).cAttacks = magestats.cAttacks
    mage.alternate = "2"
    Card(mageID).Subtype = Card(mageID).alternateProperty("", "Subtype")
    Card(mageID).Level = Card(mageID).alternateProperty("", "Level")
    Card(mageID).Stats = Card(mageID).alternateProperty("", "Stats") #havent decided if this is needed yet....proxygen??
    Card(mageID).AttackBar = Card(mageID).alternateProperty("", "AttackBar")
    Card(mageID).Traits = Card(mageID).alternateProperty("", "Traits")
    Card(mageID).cAttacks = Card(mageID).alternateProperty("", "cAttacks")
    mage.alternate = ""
    mageDict["MageRevealed"] = "True"
    me.setGlobalVariable("MageDict",str(mageDict))
    # here is where issue #360 should be called from.....and replace the line below.
    notify("{} enters the Arena! - Channeling is set to {} and Mana is set to {} and Life set to {}\n".format(Card(mageID),me.Channeling,me.Mana,me.Life))
    mageRevealMessage(mage)
    setGlobalVariable("MageRevealed", str(int(getGlobalVariable("MageRevealed"))+1))
    if eval(getGlobalVariable("MageRevealed")) == len(getPlayers()): setGlobalVariable("MageRevealed","True")
    if getGlobalVariable("MageRevealed") == "True":
        rollForInitiative()

#Called by MageSetup()
def rollForInitiative():
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

#Called by rollForInitiative()
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