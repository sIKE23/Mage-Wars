#######
#v2.0.0.0#
#######

def nextPhaseAcademy():
	mute()
	global roundTimes
	global gameTurn
	gameIsOver = getGlobalVariable("GameIsOver")
	if gameIsOver:	#don't advance phase once the game is done
		notify("Game is Over!")
		return
	if getGlobalVariable("GameSetup") != "True": # Player setup is not done yet.
		return
	card = None
	checkMageDeath(0)
	for c in table: #find phase card
		if c.model == "6a71e6e9-83fa-4604-9ff7-23c14bf75d48":
			card = c
			break
	if not card:
				whisper("You must roll initiative first!")
				return
				
	if card.alternate == "Upkeep":
		switchPhase(card,"Actions","Actions Phase")
		tutorialMessage("Actions Phase")	
	
	elif card.alternate == "Actions":
		remoteCall(me, "tutorialMessage", ["End"])
		if switchPhase(card,"","Upkeep Phase") == True: # "New Round" begins time to perform the Intiative, Reset, Channeling and Upkeep Phases
		#Check for domination victory
			goal = eval(getGlobalVariable("Goal"))
			if goal.get("Type")=="Domination" and updateVtarScore() and checkDominationVictory(): return
			setEventList('Round',[])
			setEventList('Turn',[])#Clear event list for new round
			gameTurn = int(getGlobalVariable("RoundNumber")) + 1
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
				remoteCall(p, "resetDiscounts",[])
				remoteCall(p, "resetMarkers", [])
				remoteCall(p, "resetCards", [])
				remoteCall(p, "resolveChanneling", [p])
				for card in table:
					if not card.isFaceUp and card.Type == 'Enchantment' and card.controller.name == p.name: remoteCall(p, "revealAttachmentChannel", [card, 'Channeling'])
				for card in table:
					traits = computeTraits(card)
					if card.markers[Burn] and card.controller.name == p.name: remoteCall(p, "resolveBurns", [card])
					if card.markers[Rot] and card.controller.name == p.name: remoteCall(p, "resolveRot", [card])
					if card.markers[Bleed] and card.controller.name == p.name: remoteCall(p, "resolveBleed", [card])
					if 'Dissipate' in traits and card.controller.name == p.name: remoteCall(p, "resolveDissipate", [traits, card])
					if card.Name in ["Curse of Decay"] and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveDotEnchantment", [card]) 
					if "Regenerate" in traits and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveRegeneration", [traits, card])
				remoteCall(p, "resolveUpkeep", [])

	update() #attempt to resolve phase indicator sometimes not switching

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
				
def switchPhase(card, phase, phrase):
	myHexColor = playerColorDict[eval(me.getGlobalVariable("MyColor"))]['Hex']
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	playerNum = mwPlayerDict[me._id]["PlayerNum"]
	global currentPhaseMW
	mute()
	currentPhaseMW = phase
	if debugMode:	#debuggin'
		card.alternate = phase
		notify("Phase changed to the {}".format(phrase))
		return True
	else:
		doneWithPhase = getGlobalVariable("DoneWithPhase")
		if str(playerNum) in doneWithPhase:
			return

		doneWithPhase += str(playerNum)
		if len(doneWithPhase) != len(getPlayers()):
			setGlobalVariable("DoneWithPhase", doneWithPhase)
			if card.controller == me:
				card.highlight = myHexColor
			else:
				remoteCall(card.controller, "remoteHighlight", [card, myHexColor])
			notify("{} is done with the {}".format(me.name,card.Name))
			return False
		else:
			setGlobalVariable("DoneWithPhase", "")
			if card.controller == me:
				card.highlight = None
				card.alternate = phase
			else:
				remoteCall(card.controller, "remoteHighlight", [card, None])
				remoteCall(card.controller, "remoteSwitchPhase", [card, phase, phrase])
			notify("Phase changed to the {}".format(phrase))

			return True