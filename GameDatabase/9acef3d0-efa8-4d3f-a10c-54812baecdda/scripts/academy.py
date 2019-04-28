#######
#v2.0.0.0#
#######

def nextPhaseAcademy():
	#Academy uses phases 2 - Reset, 4 - Upkeep, 8 - Actions Phase 
	mute()
	global roundTimes
	gameIsOver = getGlobalVariable("GameIsOver")
	if gameIsOver:	#don't advance phase once the game is done
		notify("Game is Over!")
		return
	if getGlobalVariable("GameSetup") != "True": # Player setup is not done yet.
		return
	card = None
	checkMageDeath(0)
	if currentPhase()[0] == "Reset Phase":
		init = [card for card in table if card.model == "8ad1880e-afee-49fe-a9ef-b0c17aefac3f"][0]
		if init.controller == me:
			flipcard(init)
		else:
			remoteCall(init.controller, "flipcard", [init])
		for p in players:
			remoteCall(p, "resetDiscounts",[])
			remoteCall(p, "resetCards", [])
			remoteCall(p, "resolveChanneling", [p])
		setPhase(4)
	elif currentPhase()[0] == "Upkeep Phase":
		tutorialMessage("Actions Phase")	
		for p in players:
			for card in table:
				traits = computeTraits(card)
				if card.markers[Burn] and card.controller.name == p.name: remoteCall(p, "resolveBurns", [card])
				if card.markers[Rot] and card.controller.name == p.name: remoteCall(p, "resolveRot", [card])
				if card.markers[Bleed] and card.controller.name == p.name: remoteCall(p, "resolveBleed", [card])
				if card.markers[Disable] and card.controller.name == p.name: remoteCall(p, "resolveDisable",[card])
				if 'Dissipate' in traits and card.controller.name == p.name: remoteCall(p, "resolveDissipate", [traits, card])
				if 'Madrigal' in traits and card.controller.name == p.name: remoteCall(p, "resolveMadrigal", [traits, card])
				if card.Name in ["Ghoul Rot", "Curse of Decay", "Arcane Corruption", "Force Crush"] and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveDotEnchantment", [card]) 
				if card.Name == "Curse Item" and card.controller.name != p.name and card.isFaceUp: 
					target = getAttachTarget(card)
					remoteCall(p, "resolveCurseItem", [target])
					if ("Regenerate" in traits or "Lifegain" in traits) and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveRegeneration", [traits, card])
			remoteCall(p, "resolveUpkeep", [])
		setPhase(8)
	elif currentPhase()[0] == "Actions Phase":
		remoteCall(me, "tutorialMessage", ["End"])
		nextTurn()
		setPhase(2)
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
				
