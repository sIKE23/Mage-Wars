# removing gameTurn as python GlobalVariables
# removing roundTimes as python GlobalVariables

def nextPhase(group,x=0,y=0):
	mute()
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	playerNum = mwPlayerDict[me._id]["PlayerNum"]
	gameMode = getGlobalVariable("GameMode")


	if debugMode:	#
		if gameMode == "Arena" or "Domination" or "Playtest": nextPhaseArena()
		elif gameMode == "Academy": nextPhaseAcademy()
		return True
	else:
		doneWithPhase = getGlobalVariable("DoneWithPhase")
		if str(playerNum) in doneWithPhase:
			return

		doneWithPhase += str(playerNum)
		if len(doneWithPhase) != len(getPlayers()):
			setGlobalVariable("DoneWithPhase", doneWithPhase)
			if currentPhase()[1]<5:
				remoteHighlight(phaseCard, myHexColor)
				notify("{} is ready to move on with the {}\n".format(me.name,currentPhase()[0]))
			else:
				remoteHighlight(phaseCard, myHexColor)
				notify("{} is done with the {}\n".format(me.name,currentPhase()[0]))

			return False
		else:
			setGlobalVariable("DoneWithPhase", "")
			if gameMode == "Arena" or "Domination" or "Playtest": nextPhaseArena()
			elif gameMode == "Academy": nextPhaseAcademy()
			#nextPhaseArena()
			return True

def nextPhaseArena():
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
	if currentPhase()[0] == "Initiative Phase":
		init = [card for card in table if card.model == "8ad1880e-afee-49fe-a9ef-b0c17aefac3f"][0]
		if init.controller == me and len(getPlayers())>1:
			flipcard(init)
		else:
			remoteCall(init.controller, "flipcard", [init])
		#setPhase(2) #Combining the Initiative, Reset, and channeling phases in order to cut down on the amount of passing needed
	#elif currentPhase()[0] == "Reset Phase":
		setEventList('Round',[])#This helps track defenses, arcane zap, etc
		setEventList('Turn',[])#This helps track defenses, arcane zap, etc
		for p in players:
			remoteCall(p, "resetDiscounts",[])
			remoteCall(p, "resetMarkers", [])
		#setPhase(3)
	#elif currentPhase()[0] == "Channeling Phase":	
		for p in players:
			remoteCall(p, "resolveChanneling", [p])
		setPhase(4)
	elif currentPhase()[0] == "Upkeep Phase":
		for p in players:
			for card in table:
				traits = computeTraits(card)
				#redo the below for removing glyphs
				if (card.markers[EarthGlyphActive] or card.markers[FireGlyphInactive] or card.markers[AirGlyphInactive]) and 'Magestats' not in card.Type and "Drake" not in card.Name: remoteCall(p, "getRidofGlyphs", [card])
				if (card.markers[EarthGlyphActive] or card.markers[WaterGlyphActive]) and ('Magestats' in card.Type or "Drake" in card.Name) and card.controller.name == p.name: remoteCall(p, "resolveUpkeepGlyphs", [traits, card])
				if 'UpKip' in traits and card.controller.name == p.name: remoteCall(p, "resolveKiUpkeep", [traits, card])
				if card.Name == 'Ring of Ki' and card.controller.name == p.name: remoteCall(p, "resolveKiGen", [traits, card])
				if "Ki" in traits and not "Magestats" in card.type and card.controller.name == p.name: remoteCall(p, "resolveKiGen", [traits, card])
				if (card.Name == "Living Armor" or card.Name == "Living Armor - Playtest") and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveLivingArmor", [traits, card])
				if "Melting" in traits and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveMelting",[traits, card])
				if (card.markers[Burn] or "Hellscape" in traits) and card.controller.name == p.name: remoteCall(p, "resolveBurns", [card])
				if card.markers[Rot] and card.controller.name == p.name: remoteCall(p, "resolveRot", [card])
				if card.markers[Bleed] and card.controller.name == p.name: remoteCall(p, "resolveBleed", [card])
				if card.markers[Disable] and card.controller.name == p.name: remoteCall(p, "resolveDisable",[card])
				if 'Dissipate' in traits and card.controller.name == p.name: remoteCall(p, "resolveDissipate", [traits, card])
				if 'Madrigal' in traits and card.controller.name == p.name: remoteCall(p, "resolveMadrigal", [traits, card])
				if 'AquaticTerrain' in traits and card.controller.name == p.name: remoteCall(p, "resolveSirenHeal",[traits, card])
				if ('Malacoda' in traits or 'Pestilence' in traits or 'Plagued' in traits or "Consecrated Ground Damage" in traits or "PoisonGasCloud" in traits) and card.controller.name == p.name: remoteCall(p, "resolveAreaDot", [traits, card])
				if card.Name in ["Ballista", "Akiro's Hammer"] and card.controller.name == p.name and card.isFaceUp and card.markers[LoadToken] < 2: remoteCall(p, "resolveLoadTokens", [card])
				if card.Name in ["Ghoul Rot", "Curse of Decay", "Arcane Corruption", "Force Crush", "Reclamation"] and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveDotEnchantment", [card]) 
				if card.Name == "Curse Item" and card.controller.name != p.name and card.isFaceUp: 
					target = getAttachTarget(card)
					remoteCall(p, "resolveCurseItem", [target])
				if card.Name == "Altar of Domination" and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveTalos", [card])
				if card.Name in ["Staff of Storms"] and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveStormTokens", [card])
				if ("Regenerate" in traits or "Lifegain" in traits) and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveRegeneration", [traits, card])
			remoteCall(p, "resolveUpkeep", [])
		setPhase(5)
	elif currentPhase()[0] == "Planning Phase":
		setPhase(6)
	elif currentPhase()[0] == "Deployment Phase":
		setPhase(7)
	elif currentPhase()[0] == "First QC Phase":
		setPhase(8)
	elif currentPhase()[0] == "Actions Phase":
		setPhase(9)
	elif currentPhase()[0] == "Final QC Phase":
		nextTurn()
		setPhase(1)
	update() #attempt to resolve phase indicator sometimes not switching

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

def resetDiscounts():
	#reset discounts used
	for tup in discountsUsed:
		discountsUsed.remove(tup)
		discountsUsed.append((tup[0],tup[1],0))

def resetMarkers():
	mute()
	for c in table:
		if c.targetedBy == me:
			c.target(False)
		if c.controller == me and c.isFaceUp and not "Alfiya" in c.Name: #don't waste time on facedown cards and only reset the markers on my cards.
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
			if "Packleader's Cowl" == c.Name: c.markers[Guard] = 1
			if "Lightning Raptor" == c.Name and c.markers[Charge]<5: c.markers[Charge] += 1
			#add a Guard Marker to Orb Guardians when they are in the same zone as an Orb
			if "Orb Guardian" in c.name:
					for o in table:
							isWithOrb = False
							if "V'Tar Orb" in o.name and (getZoneContaining(o) == getZoneContaining(c)): isWithOrb = True
							if isWithOrb: c.markers[Guard] = 1

	notify("{} resets all Action, Ability, Quickcast, and Ready Markers on the Mages cards by flipping them to their active side.\n".format(me.name))
	debug("card,stats,subtype {} {} {}".format(c.name,c.Stats,c.Subtype))
