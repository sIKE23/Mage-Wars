#######
#v2.0.0.0#
#######

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
		if init.controller == me:
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
				if card.markers[Burn] and card.controller.name == p.name: remoteCall(p, "resolveBurns", [card])
				if card.markers[Rot] and card.controller.name == p.name: remoteCall(p, "resolveRot", [card])
				if card.markers[Bleed] and card.controller.name == p.name: remoteCall(p, "resolveBleed", [card])
				if card.markers[Disable] and card.controller.name == p.name: remoteCall(p, "resolveDisable",[card])
				if 'Dissipate' in traits and card.controller.name == p.name: remoteCall(p, "resolveDissipate", [traits, card])
				if 'Madrigal' in traits and card.controller.name == p.name: remoteCall(p, "resolveMadrigal", [traits, card])
				if ('Malacoda' in traits or 'Pestilence' in traits or 'Plagued' in traits or "Consecrated Ground Damage" in traits) and card.controller.name == p.name: remoteCall(p, "resolveAreaDot", [traits, card])
				if card.Name in ["Ballista", "Akiro's Hammer"] and card.controller.name == p.name and card.isFaceUp and card.markers[LoadToken] < 2: remoteCall(p, "resolveLoadTokens", [card])
				if card.Name in ["Ghoul Rot", "Curse of Decay", "Arcane Corruption", "Force Crush"] and card.controller.name == p.name and card.isFaceUp: remoteCall(p, "resolveDotEnchantment", [card]) 
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

def resolveLivingArmor(traits, card):
	gamemode = getGlobalVariable("GameMode")
	mage = Card(traits['MageID']) 
	if gamemode == "Playtest" and card.isFaceUp:
		if card.markers[Armor] < 3:
			notifystr = "Would you like to pay 1 mana to add 2 Armor Tokens due to Living Armor?"
			choiceList = ['Yes', 'No']
			colorsList = ['#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if me.Mana == 0:
				notify("{} cannot afford to add more armor to Living Armor".format(me))
			elif choice == 1 :
				me.Mana -= 1
				if card.markers[Armor] < 2:
					card.markers[Armor]+=2
					notify("{} has chosen to pay 1 mana to add 2 Armor Tokens to Living Armor".format(me))
				elif card.markers[Armor] < 3:
					card.markers[Armor]+=1
					notify("{} has chosen to pay 1 mana to add Armor Tokens to Living Armor, but only adds 1 due to reaching the max of 3".format(me))
			elif choice == 2:
				notify("{} has chosen not to pay for Armor Tokens".format(me))
				return
		else:
			notify("Living Armor has 3 tokens already and will not generate more")
			
	else:
		if card.markers[Armor] < 2 and card.isFaceUp:
			card.markers[Armor]+=2
			notify("Living Armor generates 2 Armor Tokens")
		elif card.markers[Armor] < 3 and card.isFaceUp:
			card.markers[Armor]+=1
			notify("Living Armor generates 1 Armor Token")
		else:
			notify("Living Armor has 3 tokens already and will not generate more")
	return
	
def getRidofGlyphs(card):
	card.markers[FireGlyphInactive] = 0
	card.markers[AirGlyphInactive] = 0
	card.markers[EarthGlyphActive] -= 1
	
	
def resolveKiGen(traits, card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
		
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	mage = Card(mageID)
	if card.name == 'Ring of Ki':
		notifystr = "Would you like to pay 1 mana to gain 2 Ki?"
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 :
			me.Mana -= 1
			mage.markers[Ki]+=2
			notify("{} has chosen to pay 1 mana to gain 2 Ki".format(me))
		elif choice == 2:
			notify("{} has chosen not to pay for Ki".format(me))
	if card.controller == me and 'Ki' in traits and card.isFaceUp:
		notify("Generating Ki for {}...\n".format(card))	#found at least one
		card.markers[Ki] += 1 
	return
	
def resolveUpkeepGlyphs(traits, card):
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageStats = Card(mageStatsID)
	mage = Card(traits["MageID"])
	if card.markers[EarthGlyphActive]:
		notifystr = "Would you like to pay 2 mana to give 2 Armor to a friendly creature?"
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 :
			me.Mana -= 2
			mageStats.markers[EarthGlyphActive] = 0
			mageStats.markers[EarthGlyphInactive] = 1
			mage.markers[EarthGlyphActive] +=1
			notify("{} has chosen to pay 2 mana to give a friendly creature 2 Armor.\n(You'll have to manually move the Glyph token from your mage to target for now)\n".format(me))
	if card.markers[WaterGlyphActive]:
		notifystr = "Would you like to pay 2 mana to heal a friendly creature by 2?"
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 :
			me.Mana -= 2
			mageStats.markers[WaterGlyphActive] = 0
			mageStats.markers[WaterGlyphInactive] = 1
			notify("{} has chosen to pay 2 mana to heal a friendly creature by 2.\n(You'll have to manually heal the target for now)\n".format(me))			
	return
	
def resolveKiUpkeep(traits, card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
		
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	mage = Card(mageID)
	if card.name == 'Five Point Death Strike':
		target = getAttachTarget(card)
		notifystr = "Would you like to pay 1 Ki to keep the Five Point Death Strike attached to {}?".format(target.name)
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		if mage.markers[Ki]<1:
			notify("{} cannot afford to keep powering the Death Strike".format(me))
			card.moveTo(me.piles['Discard Pile'])
		else:
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if choice == 1 :
				mage.markers[Ki]-=1
				notify("{} has chosen to pay 1 Ki to prolong the Death Strike!".format(me))
			elif choice == 2:
				notify("{} has chosen not to continue powering the Death Strike".format(me))
				card.moveTo(me.piles['Discard Pile'])
	return
	
def resolveMadrigal(traits, card):
	if ("Madrigal" in traits and "Finite Life" in traits) and card.controller == me and card.isFaceUp:
			notify("{} has the Finite Life Trait and can not heal".format(card.name))
			return
	if "Mage" in card.Subtype and card.controller == me and me.Damage > 1:
			damageAmount = 2
			subDamageAmount(card, 2)
	elif "Mage" in card.Subtype and card.controller == me:
			damageAmount = me.Damage
			me.Damage = 0
	elif "Mage" not in card.Subtype and card.markers[Damage]<2:
			damageAmount = card.markers[Damage]
			card.markers[Damage] = 0
	else:
			damageAmount = 2
			subDamageAmount(card, 2)
	if damageAmount > 0:
		notify("{}'s Healing Madrigal heals {} damage from {} ".format(me,damageAmount, card.name))
	else:
		notify("{}'s {} is already at full health".format(me, card.name))
		
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


def changeIniColor(card):
	mute()
	myColor = me.getGlobalVariable("MyColor")
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	if mwPlayerDict[me._id]["PlayerNum"] == int(getGlobalVariable("PlayerWithIni")):
		card.alternate = myColor
	else:
		remoteCall(card.controller, "remoteSwitchPhase", [card, "myColor", ""])

def getNextPlayerNum():
	debug(getGlobalVariable("PlayerWithIni"))
	activePlayer = int(getGlobalVariable("PlayerWithIni"))
	nextPlayer = activePlayer + 1
	if nextPlayer > len(getPlayers()):
		nextPlayer = 1
	return nextPlayer
	
