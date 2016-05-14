#######
#v2.0.0.0#
#######

def nextPhaseArena():
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
	if card.alternate == "":
		switchPhase(card,"Planning","Planning Phase")
	elif card.alternate == "Planning":
		switchPhase(card,"Deploy","Deployment Phase")
		tutorialMessage("Actions Menu")
	elif card.alternate == "Deploy":
		switchPhase(card,"Quick","First Quickcast Phase")
		tutorialMessage("Cast Spell")
	elif card.alternate == "Quick":
		switchPhase(card,"Actions","Actions Phase")
		tutorialMessage("Actions Phase")
	elif card.alternate == "Actions":
		switchPhase(card,"Quick2","Final Quickcast Phase")
		tutorialMessage("Bind Spell")
	elif card.alternate == "Quick2":
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
				remoteCall(p, "resolveChanneling", [p])
				remoteCall(p, "resolveRegeneration", [])
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

#def setActiveP(p):
#	p.setActive()

def switchPhase(card, phase, phrase):
	myHexColor = playerColorDict[eval(me.getGlobalVariable("MyColor"))]['Hex']
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	playerNum = mwPlayerDict[me._id]["PlayerNum"]
	global currentPhase
	mute()
	currentPhase = phase
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

def validateDeck(deck):
	mute()
	for c in deck:
			if c.Type == "Magestats":
					stats = c.Stats.split(",")
					schoolcosts = c.MageSchoolCost.replace(' ','').split(",")
					mageName = c.name.split(" Stats")[0]
					spellbook["spellpoints"] = int(StatSpellBookPoints)
			break
	#debug("Stats {}".format(stats))
	spellbook = {"Dark":2,"Holy":2,"Nature":2,"Mind":2,"Arcane":2,"War":2,"Earth":2,"Water":2,"Air":2,"Fire":2,"Creature":0}

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
		elif "Water" in costval[0] and c.name != "Druid":
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

		#Siren is trained in Water and all spells with Song or or Pirate subtypes.
		#By this point, Water has been correctly calculated, but the Song/Pirate spells are overcosted if they are not Water
		if "Water" not in card.School and "Siren" in c.name and ("Song" in card.Subtype or "Pirate" in card.Subtype):
			#subtract 1 per level per count as this card has been added x2 per non-trained school already
				if "+" in card.School:
					level = card.Level.split("+")
					for l in level:
						booktotal -= int(l)
				elif "/" in card.School:
					level = card.Level.split("/")
					booktotal -= int(level[0])
				elif card.School != "": # only one school
					booktotal -= int(card.Level)

		#Paladin is trained in Holy Level 3 Spells, War Level 2 Spells, and all Holy Creatures reguardless of their training
		#By this point, Level 3 and Lower Holy Spells and Level 2 and Lower War Spells have been correctly calculated, but spells higher then the specifed levels have been undercosted
		if "Holy" in card.School or "War" in card.School and "Paladin" in c.name:
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
					 if "Holy" == card.School and int(card.Level) > 3 and card.Type != "Creature" and "Paladin" in c.name:
						booktotal += int(card.Level)
					 elif "War" == card.School and int(card.Level) > 2 and "Paladin" in c.name:
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
			if "Paladin" in mageName:
				mageName = "Paladin"
			if "Siren" in mageName:
				mageName = "Siren"
			if mageName in card.Traits:	# mage restriction
				ok = True
			for s in [school for school in spellbook if spellbook[school] == 1]: # school restriction
				if s + " Mage" in card.Traits: # s will hold the school like Holy or Dark
					ok = True
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
	return True
