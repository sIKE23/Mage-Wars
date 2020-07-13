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
				if (card.markers[EarthGlyphActive] or card.markers[FireGlyphInactive] or card.markers[AirGlyphInactive]) and 'Magestats' not in card.Type: remoteCall(p, "getRidofGlyphs", [card])
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
			remoteCall(p, "resolveUpkeep", [traits])
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

#def setActiveP(p):
#	p.setActive()


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
	
'''def validateDeck(deck):
	mute()
	spellbook = {"Dark":2,"Holy":2,"Nature":2,"Mind":2,"Arcane":2,"War":2,"Earth":2,"Water":2,"Air":2,"Fire":2,"Creature":0}

	for c in deck:
			if c.Type == "Magestats":
					stats = c.Stats.split(",")
					schoolcosts = c.MageSchoolCost.replace(' ','').split(",")
					mageName = c.name.split(" Stats")[0]
					spellbook["spellpoints"] = int(c.StatSpellBookPoints)
					break


	#get school costs
	for schoolcost in schoolcosts:
		#debug("schoolcost {}".format(schoolcost))
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
		elif "Water" in costval[0] and mageName != "Druid":
			spellbook["Water"] = int(costval[1])
		elif "Air" in costval[0]:
			spellbook["Air"] = int(costval[1])
		elif "Fire" in costval[0]:
			spellbook["Fire"] = int(costval[1])
	#debug("Spellbook {}".format(spellbook))

	# loop through all the spell cards in the spellbook then calculate the levels by school in the dictionary 'levels'
	# with a level a count per school. Spells/mages that are/have exceptions will typically be tracked in the booktotal value
	# once done the spell levels as caculated will be mutipled by their schoolcost mutipler and added to the booktotal value
	#which should not exceed the mages Spellbook Points
	levels = {}
	booktotal = 0
	epics = ["", "three"]
	cardCounts = { }
	for card in deck: #run through deck adding levels
		cardCost = 0
		if "Novice" in card.Traits: #Novice cards cost 1 spellpoint
			#debug("novice {}".format(card))
			booktotal += 1

		elif "Talos" in card.Name: #Talos costs nothing
			debug("Talos")
		elif "+" in card.School: #t this point process cards that belong in 2 schools and add their levels up
			#debug("and School {}".format(card))
			schools = card.School.split("+")
			level = card.Level.split("+")
			i = 0
			for s in schools:
				try:
					levels[s] += int(level[i])
				except:
					levels[s] = int(level[i])
				i += 1
		elif "/" in card.School: # at this point process cards that belong in 1 or more schools and figure out which school is the cheapest
			#debug("or School {}".format(card))
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
			except:				levels[s_low] = int(level[i])
		elif card.School != "": # at this point cards processed below should belong to only one school (and are not novice)
			#debug("Single School {}".format(card))
			try:
				levels[card.School] += int(card.Level)
			except:
				levels[card.School] = int(card.Level)

		if card.Type == "Creature" and mageName == "Forcemaster": #check for the forcemaster rule
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

		if "Water" in card.School and mageName == "Druid" and not "Nature" in card.School: #check for the druid rule
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
					schools = card.School.split("/")
					i = 0
					for s in schools:
						if s in levels:
							booktotal-=1
					#levels[card.School] -= 1
					#booktotal += 1
				elif card.School != "": # only one school
					levels[card.School] -= 1
					booktotal += 1
				debug("levels {}".format(levels))

		#Siren is trained in Water and all spells with Song or or Pirate subtypes.
		#By this point, Water has been correctly calculated, but the Song/Pirate spells are overcosted if they are not Water
		if "Siren" in mageName and (("Water" in card.School and "+" in card.School) or ("Water" not in card.School)) and ("Song" in card.Subtype or "Pirate" in card.Subtype):
			#subtract 1 per level per count as this card has been added x2 per non-trained school already
				if "+" in card.School:
					level = card.Level.split("+")
					schools = card.School.split("+")
					for s in schools:
						if not s == "Water":
							for l in level:
								booktotal -= int(l)
				elif "/" in card.School:
					level = card.Level.split("/")
					booktotal -= int(level[0])
				elif card.School != "": # only one school
					booktotal -= int(card.Level)

		#Paladin is trained in Holy Level 3 Spells, War Level 2 Spells, and all Holy Creatures reguardless of their training
		#By this point, Level 3 and Lower Holy Spells and Level 2 and Lower War Spells have been correctly calculated, but spells higher then the specifed levels have been undercosted
		if "Holy" in card.School or "War" in card.School and "Paladin" in mageName:
				if "+" in card.School:
						level = card.Level.split("+")
						school = card.School.split("+")
						for count in range(len(level)):
								if "Holy" == school[count] and int(level[count]) > 3 and card.Type != "Creature":# All Holy Creatures have already been caculated corretly with a 1x training cost
										booktotal += int(level[count])
								elif "War" == school[count] and int(level[count]) > 2  and card.Type != "Creature":# All War Creatures have already been caculated corretly with a 1x training cost
										booktotal += int(level[count])
								elif school[count] != "Holy" and school[count] != "War" and card.Type == "Creature":# Creatures not in the Holy or War School have already been caculated incorrectly with a 2x training cost
										booktotal -= int(level[count])
				elif "/" in card.School: # need to validate that this logic is correct
						level = card.Level.split("/")
						school = card.School.split("/")
						for count in range(len(level)):
								if "Holy" == school[count] and int(level[count]) > 3 and card.Type != "Creature":
										booktotal += int(level[count])
										break
								elif "War" == school[count] and int(level[count]) > 2  and card.Type != "Creature":
										booktotal += int(level[count])
										break
				else:
					 if "Holy" == card.School and int(card.Level) > 3 and card.Type != "Creature" and "Paladin" in mageName:
						booktotal += int(card.Level)
					 elif "War" == card.School and int(card.Level) > 2 and "Paladin" in mageName:
						booktotal += int(card.Level)

		#multiple Epic cards are not allowed in the spellbook.
		if "Epic" in card.Traits:
			if card.Name in epics:
				notify("*** ILLEGAL ***: multiple copies of Epic card {} found in spellbook".format(card.Name))
				return False
			epics.append(card.Name)

		if "Only" in card.Traits:	#check for school/mage restricted cards
			ok = False
			if "Beastmaster" in mageName:
				mageName = "Beastmaster"
			if "Wizard" in mageName:
				mageName = "Wizard"
			if "Warlock" in mageName:
				mageName = "Warlock"
			if "Warlord" in mageName:
				mageName = "Warlord"
			if "Priest" in mageName:
				mageName = "Priestess"
			if "Priestess" in mageName:
				mageName = "Priestess"
			if "Paladin" in mageName:
				mageName = "Paladin"
			if "Siren" in mageName:
				mageName = "Siren"
			if "Forcemaster" in mageName:
				mageName = "Forcemaster"
			if "Wizard" in mageName:
				mageName = "Wizard"
			if mageName in card.Traits:	# mage restriction
				ok = True
			if "Druid" in mageName and card.Name == "Ring of the Ocean\'s Depths":
				ok = True
			for s in [school for school in spellbook if spellbook[school] == 1]: # school restriction
				if s + " Mage" in card.Traits: # s will hold the school like Holy or Dark
					ok = True
				#if s == "Water" and mageName == "Druid":
					#ok = True
			if not ok:
				notify("*** ILLEGAL ***: the card {} is not legal in a {} Spellbook.".format(card.Name,mageName))
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
			if (l == 1 and cardCounts.get(card.Name) > 6 or (l >= 2 and cardCounts.get(card.Name) > 4)):
				notify("*** ILLEGAL ***: there are too many copies of {} in {}'s Spellbook.".format(card.Name, me))
				return False

	for level in levels:
		booktotal += spellbook[level]*levels[level]
	notify("Spellbook of {} calculated to {} points".format(me,booktotal))

	if (booktotal > spellbook["spellpoints"]):
		return False

	#all good!
	return True'''
