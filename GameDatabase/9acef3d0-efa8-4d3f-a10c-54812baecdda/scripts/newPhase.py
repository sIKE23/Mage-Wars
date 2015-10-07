# removing gameTurn as python GlobalVariables
# removing roundTimes as python GlobalVariables

def nextPhaseArena():
	mute()
	myHexColor = playerColorDict[eval(me.getGlobalVariable("MyColor"))]['Hex']
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	playerNum = mwPlayerDict[me._id]["PlayerNum"]
	currentPhase = eval(getGlobalVariable("CurrentPhase"))
	phaseCard = Card(int(getGlobalVariable("PhaseCard"))) #the card ID for the Phase Card this game
	gameIsOver = getGlobalVariable("GameIsOver")

	if gameIsOver:	#don't advance phase once the game is done
		notify("Game is Over!")
		return
#	if getGlobalVariable("GameSetup") != "True": # Player setup is not done yet.
#		return

	if debugMode:	#
		phaseCard.alternate = str(currentPhase)
		notify("Phase changed to the {}".format(phaseCard.Nickname))
	else:

		doneWithPhase = getGlobalVariable("DoneWithPhase") 
		if not str(playerNum) in doneWithPhase: 
			doneWithPhase += str(playerNum) 
			setGlobalVariable("DoneWithPhase", doneWithPhase)

		if len(doneWithPhase) != len(getPlayers()):
			if phaseCard.controller == me:
				phaseCard.highlight = myHexColor 
			else:
				remoteCall(phaseCard.controller, "remoteHighlight", [phaseCard, myHexColor]) 
			notify("{} is done with the {}".format(me.name,phaseCard.Nickname)) 

		else: 
			setGlobalVariable("DoneWithPhase", "") 
			if currentPhase == 9: 
				currentPhase = 1 
			else:
				currentPhase += 1
			setGlobalVariable("CurrentPhase",str(currentPhase))
			checkMageDeath(0)

			if phaseCard.controller == me: 
				phaseCard.highlight = None 
				phaseCard.alternate = str(currentPhase) 
			else:
				remoteCall(phaseCard.controller, "remoteHighlight", [phaseCard, None]) 
				remoteCall(phaseCard.controller, "remoteSwitchPhase", [phaseCard,str(currentPhase)]) 

			notify("Phase changed to the {}".format(phaseCard.Nickname))

	#The Ready Stage
	if currentPhase == 1: #Initative Phase
		goal = eval(getGlobalVariable("Goal"))
		if goal.get("Type")=="Domination" and updateVtarScore() and checkDominationVictory(): return
		setEventList('Round',[])
		setEventList('Turn',[]) #Clear event list for new round
		gameTurn = int(getGlobalVariable("RoundNumber")) + 1
		setGlobalVariable("RoundNumber", str(gameTurn))
		roundTimes = eval(getGlobalVariable("RoundTimes"))
		rTime = time.time()
		roundTimes.append(rTime)
		setGlobalVariable("RoundTimes",str(roundTimes))
		notify("\n****** Round {} ******\nStart Time: {}\n".format(str(gameTurn),time.ctime(roundTimes[-1])))
		notify("It is {Player Initative is being passed to} Initiative Phase\n")#need to finish this....

		for p in players:
			remoteCall(p, "playerStats",[])

		init = [card for card in table if card.model == "8ad1880e-afee-49fe-a9ef-b0c17aefac3f"][0]
		if init.controller == me:
			flipcard(init)
		else:
			remoteCall(init.controller, "flipcard", [init])

	elif currentPhase == 2: #Reset Phase
		notify("Reseting all Action Markers, Quickcast Markers, and Ready Markers on all players cards by flipping them to their active side.")
		for p in players:
			remoteCall(p, "resetMarkers", [])
			remoteCall(p, "resetDiscounts",[])

	elif currentPhase == 3: #Channel Phase
		for p in players:
			remoteCall(p, "resolveChanneling", [p])

	elif currentPhase == 4: #Upkeep Phase
		tutorialMessage("Actions Menu")
		for p in players:
			remoteCall(p, "resolveBurns", [])
			remoteCall(p, "resolveRot", [])
			remoteCall(p, "resolveBleed", [])
			remoteCall(p, "resolveDissipate", [])
			remoteCall(p, "resolveLoadTokens", [])
			remoteCall(p, "resolveStormTokens", [])
			remoteCall(p, "resolveUpkeep", [])

	elif currentPhase == 5: #Planning Phase
		tutorialMessage("Cast Spell")

	elif currentPhase == 6: #Deployment Phase
		update()

	#The Action Stage
	elif currentPhase == 7: #Deployment Phase
		update()

	elif currentPhase == 8: #Creature Action Phases
			tutorialMessage("Actions Phase")

	elif currentPhase == 9:
		tutorialMessage("Bind Spell")
		remoteCall(me, "tutorialMessage", ["End"])

	else:
		notify("Error 23")

def changeIniMarker():
	mute()
	myColor = me.getGlobalVariable("MyColor")
	initativeCard = Card(int(getGlobalVariable("InitativeCard")))
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	initativeCard.alternate = myColor

def remoteHighlight(phaseCard, color):
	phaseCard.highlight = color

def remoteSwitchPhase(phaseCard,phase):
	phaseCard.alternate = phase
