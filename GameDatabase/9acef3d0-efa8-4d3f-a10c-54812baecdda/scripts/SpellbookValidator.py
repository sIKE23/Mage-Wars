'''#######
#v2.2.0.0#
Created 30 April 2019

Changelog:
	Sharkbait: 16 May 2020: 
		hahaha.... a year later. Anyways, I fixed the issue with multi school, level X cost spells with the druid.
		This doesn't address mage-only cards for level X yet, but I'm not sure it's super necessary right now.
	
	
	Sharkbait: 15 May 2019:
		Fixed a few errors. The Level X code was causing the level X logic to apply to all training a mage had, not just the 
		school that was trained up to Level X. It has been adjusted now to check for the whole school training first. Subtype
		training was causing an issue where the SBPadd could be overwritten, so I made it part of the if/elif branching scheme. 
		Subtyping was also doing the '/' costs wrong due to only checking for school. This has been fixed with comments near the 
		function explaining.**************WHEN YOU EDIT THIS NEXT, TAKE TIME TO ADD COMMENTS**************************
		
	Sharkbait: 10 May 2019:
		Finished up the first iteration of Level X training. I am pretty sure everything is at least functional for now except
		counting those mages as School mages. Currently, as long as the mage is at least a little trained in that school, the 
		validator will let it validate regardless of level.

	Sharkbait: 30 April 2019:
		Added Combo School-type, card counts, Mage Only
		
	Sharkbait: 30 April 2019:
		Completed all functionality except Combo School-Type, Level X, card counts, and redoing Mage and School only cards
#######'''

'''
validateDeck is the main function of this script. It takes in the deck object from the game when a player loads a deck. 

##########
mageStats
mageTraining
mageName
spellpointsTotal

The above group is taken from the mage stats card for use in determining the legality and cost of cards in a deck by calling the statCardParse function.
##########
spellbook

This variable is a dictionary that lists the training of the mage and the amount of spellpoints available during construction as listed on the mage stats card.
##########
schoolTrn
schoolOpp
mageSubtypeTrnList
mageSubtypeOppList
mageTypeTrnList
mageTypeOppList
comboSTList
levelXList

All of these variables were created to handle weird trainings that weren't strictly "trained in X school". An example is the Druid being trained in Level 1 of 
water spells. Each variable will be spelled out more in the function getUniqueTraining below.
###########
bookTotal
cardDict

These two are the outputs from the cardPointCount function. bookTotal used to be compared to the max allowed and a flag is raised if bookTotal exceeded 
spellbook["Spellpoints"] but it didn't give enough feedback as to what exactly was wrong so that part has been deleted. For now, bookTotal is announced in chat
to allow the players to decide whether to proceed or not until all the spellbook validators are confirmed to be correct. Additional functionality desired would be 
to have the option of listing out the cost calcs in chat so the players can figure out where their count may have gone wrong.
############
Possible redundant or currently unused variables that could use a cleaning pass:

spellpointsTotal - Not currently used. Could be used as a part of a comparison of allowable spellbook points, but I this is unnecessary
mageStats - I'm not seeing this used anywhere in this function, though I'll have to check the other scripts to see if it is. This is an artifact from old code
############

'''
def validateDeck(deck):
	mute()
	spellbook = {}
	mageStats, mageTraining, mageName, spellpointsTotal = statCardParse(deck)
	spellbook = spellbookDictProcessing (mageTraining, spellpointsTotal)
	schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList = getUniqueTraining(spellbook)
	bookTotal, cardDict=cardPointCount(deck, spellbook, schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList, mageName)
	notify("Spellbook of {} calculated to {} points".format(me,bookTotal))
	return True

def statCardParse(deck):
	mute()
	for c in deck:
		debug(c.name)
		if c.Type == "Magestats":
			mageStats = c.Stats.split(",")
			mageTraining = c.MageSchoolCost.replace(' ','')
			mageTraining = [mageTraining.split("=") for mageTraining in mageTraining.split(",")]
			mageTraining = [tuple(l) for l in mageTraining]
			mageName = c.name.split(" Stats")[0]
			spellpointsTotal = int(c.StatSpellBookPoints)
			break
	return [mageStats, mageTraining, mageName, spellpointsTotal]
	
def spellbookDictProcessing(mageTraining, spellpointsTotal):
	mute()
	spellbook = dict(mageTraining)
	spellbook = dict(zip(spellbook.keys(), [int(value) for value in spellbook.values()]))
	spellbook["Spellpoints"] = spellpointsTotal
	spellbook["booktotal"] = 0
	return spellbook
	
def getUniqueTraining(spellbook):
	mageSubtypeTrnList = [] #store all subtypes training (Ex: Siren trained in Songs and Pirates)
	mageSubtypeOppList = []
	mageTypeTrnList = [] #store type training (Ex: Forcemaster opposed in creatures)
	mageTypeOppList = []
	comboSTList = [] #store School-Type training (Ex: Paladin trained in Holy Creatures)
	schoolTrn = []
	schoolOpp = []
	levelXList = []
	for key in spellbook:
		if key.startswith('S-'):	
			if spellbook[key]==1:
				mageSubtypeTrnList.append(key.split('-')[1])
			else:
				mageSubtypeOppList.append(key.split('-')[1])
		elif key.startswith('T-'):
			if spellbook[key]==1:			
				mageTypeTrnList.append(key.split('-')[1])
			else:
				mageTypeOppList.append(key.split('-')[1])
		#Future Idea: Could make this handle FM and monk's training in mind creatures
		elif key.startswith('C-'):
			school, type = key.split('-')[1:]
			comboSTList.append(school)
			comboSTList.append(type)
			if school not in schoolTrn:
				schoolTrn.append(school)
		elif key.startswith('L-'): 
			level, school = key.split('-')[1:3]
			levelXList += [school, level]
			if school not in schoolTrn:
				schoolTrn.append(school)
		else:
			if spellbook[key]==1:
				schoolTrn.append(key)
			elif spellbook[key]==3:
				schoolOpp.append(key)

	return [schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList]

#The ordering and functions can still be cleaned up, but overall it's functional. I've tested blightheart with the siren and it goes fine too.
def cardPointCount(deck, spellbook, schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList, mageName):
	mute()
	cardDict = {}
	for card in deck: #run through deck adding levels and checking counts
		SBPadd = 0
		if not ("Mage" in card.Subtype or "Magestats" in card.Subtype or "Aura" in card.Subtype):
			debug(card.name)
			
			#temporary way to make sure combo checks elements not letters. Also hijacked in the rewrite
			if '/' in card.school:
				cardSchoolList = card.school.replace(' ', '').split('/')
				rawCardLevel = card.level.split('/')[0]
				rawCardLevel = int(rawCardLevel)
			elif '+' in card.school:
				cardSchoolList = card.school.replace(' ', '').split('+')
				cardLevel = card.level.split('+')
				rawCardLevel = []
				for i in range(len(cardLevel)):
					rawCardLevel.append(int(cardLevel[i]))
				rawCardLevel = sum(rawCardLevel)
			else:
				cardSchoolList = [card.school, '']
				rawCardLevel = int(card.level)
				
			cardSubtypeList = card.subtype.replace(' ','').split(',') #Get card Subtype(s)
			cardTypeList = card.type.replace(' ','').split(',') #Get card Type
				
			#Check if the card is Novice. No matter the school, it only costs (card.level) points
			if "Novice" in card.Traits:
				SBPadd = int(card.level)
				spellbook['booktotal']+=SBPadd
				#notify(card.name)
				#notify(str(SBPadd))
				#notify("spellbook['booktotal']: " +str(spellbook['booktotal']))
				continue
				#checkForNovice(card) For more academy functionality later.. .maybe
				
			#Talos doesn't cost anything
			if "Talos" in card.Name:
				debug("Talos")
				continue
				
			#Check that both the mage is trained/opposed in subtypes and that the card has at least one of those subtypes
			if mageSubtypeTrnList != [] and True in [cardSubtype in mageSubtypeTrnList for cardSubtype in cardSubtypeList]:
				if '+' in card.school:
					SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp, 1)
				elif '/' in card.school:
					SBPadd = multiOrSchool(card, spellbook, True)
				else:
					SBPadd += int(card.level)
					
			#Check that the card has a combination of School and Type that matches the mage's training
			elif (comboSTList != []
				and True in [cardType in comboSTList for cardType in cardTypeList]
				and True in [comboCardSchool in comboSTList for comboCardSchool in cardSchoolList]):
					SBPadd = comboSTListProcess(card, comboSTList, spellbook, schoolTrn, mageTypeTrnList)
					
					
			#Check that both the mage is trained/opposed in a type of card and that the card is one of those types(Forcemaster, creatures = 3)
			elif  ((mageTypeTrnList != [] and True in [cardType in mageTypeTrnList for cardType in cardTypeList])
				or (mageTypeOppList != [] and True in [cardType in mageTypeOppList for cardType in cardTypeList])):
					#Theoretically this needs updated for the general case, but since this is the last
					#of Mage Wars 1.0, I can punt this to 2nd edition
					if 'Forcemaster' in mageName and 'Mind' in cardSchoolList:
						SBPadd = rawCardLevel
					elif 'Monk' in mageName and 'Mind' in cardSchoolList:
						SBPadd = rawCardLevel
					else:
						SBPmod = trainOrOpposed(card.type, mageTypeTrnList, mageTypeOppList)
						SBPadd = rawCardLevel*SBPmod					
					
			#Check for school training (regardless of level at first)
			elif ((True in [cardSchool in schoolTrn for cardSchool in cardSchoolList])
				or (True in [cardSchool in schoolOpp for cardSchool in cardSchoolList])):
					if (card.school in spellbook
						or (True in [cardSchool in schoolTrn for cardSchool in cardSchoolList])):
						if (True in [cardSchool in levelXList for cardSchool in cardSchoolList]):
							SBPadd = levelXListProcess(card, levelXList, spellbook, schoolTrn, schoolOpp)
						else:
							if "+" in card.school:
								SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
							elif "/" in card.school:
								SBPadd = multiOrSchool(card, spellbook)
							else:
								SBPmod = trainOrOpposed(card.school, schoolTrn, schoolOpp)
								SBPadd = SBPmod*int(card.level)
				
			#If nothing else triggers, it should cost 2/level
			if SBPadd == 0:
				if "+" in card.school:
					SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
				elif "/" in card.school:
					SBPadd = multiOrSchool(card, spellbook)
				else:
					SBPmod = 2 
					SBPadd = SBPmod*int(card.level)

			#This creates a Dict to count all the non-Mage and non-Magestats cards
			checkCounts(card, cardDict)
			
			if "Only" in card.traits:
				checkMageSchoolOnly(card, mageName, schoolTrn)
			
			#notify(card.name)
			#notify(str(SBPadd))	
			spellbook['booktotal']+=SBPadd	
			#notify("spellbook['booktotal']: " +str(spellbook['booktotal']))
	return (spellbook['booktotal'], cardDict)
		
	
def multiAndSchool(card, spellbook, schoolTrn, schoolOpp, sbpForce = 0):
	mute()
	schools = card.school.split('+')
	cardLevel = card.level.split('+')
	bookTotalAdd = 0
	index = 0
	for s in schools:
		if sbpForce == 0:
			SBPmod = trainOrOpposed(s, schoolTrn, schoolOpp)
			bookTotalAdd += SBPmod*int(cardLevel[index])
			index+=1
		else:
			bookTotalAdd += sbpForce*int(cardLevel[index])
			index+=1
	return bookTotalAdd

#Will take the lowest training in the school list. If the subtype flag is true, it will return as trained no matter what as of 15 May 2019.
#This is because there is no mage currently opposed to subtypes. If that changes, the code will need to adjust, I just don't have time today.
def multiOrSchool(card, spellbook, subtype = False):	
	mute()
	
	schools = card.school.split('/')
	cardLevel = int(card.level.split('/')[0])
	SBPmod = 2
	if subtype == False:
		for s in schools:
			if s in spellbook and spellbook[s]==1:
				SBPmod = 1
	else:
		SBPmod = 1
	return cardLevel*SBPmod

def comboTrain():
	mute()

def comboSTListProcess(card, comboSTList, spellbook, schoolTrn, mageTypeTrnList):
	SBPadd = 0
	while comboSTList != []:
		currentPair = comboSTList[0:2]
		comboSTList = comboSTList[2:]
		currentSchool = currentPair[0]
		currentType = currentPair[1]
		if '+' in card.school and (currentSchool in card.school and card.Type in currentType):
				tempAdd = multiAndSchool(card, spellbook, schoolTrn, [], 1)
				SBPadd+=tempAdd
		elif '/' in card.school and (currentSchool in card.school and card.Type in currentType):
			cardLevel = int(card.level.split('/')[0])				
			SBPadd += int(cardLevel)
		else:
			SBPadd+=int(card.level)
	return SBPadd
	
def levelXListProcess(card, levelXList, spellbook, schoolTrn, schoolOpp):
	SBPadd = 0
	#This should just compare the level of the spell to the level of the training in the proper school and return SBPadd based on that
	while levelXList != [] and SBPadd == 0:
		LevelX_schools = []
		LevelX_levels = []
		for item in levelXList:
			if len(item)>1:
				LevelX_schools.append(item)
			else:
				LevelX_levels.append(item)
		LevelX_index = 0
		card_school_index = 0
		#If the card in question has a + cost and the mage has training in the card's school...
		if '+' in card.school:		
			cardLevel = card.level.split('+')
			cardSchools = card.school.split('+')
			
			#for each school in cardSchools...
			for current_card_school in cardSchools:
				#Check if the current school being checked is on the Level X list
				if current_card_school in levelXList:
					#if it is, find out what index it has so you can correlate to its level
					LevelX_index = LevelX_schools.index(current_card_school)
					if  int(cardLevel[card_school_index])<=int(LevelX_levels[LevelX_index]):
						#If the level of training is equal or higher than the card's level in that school, SBP mod is 1
						SBPmod = 1
						SBPadd = SBPadd+SBPmod*int(cardLevel[card_school_index])
					else:
						#otherwise it's 2
						SBPmod = 2
						SBPadd = SBPadd+SBPmod*int(cardLevel[card_school_index])
				else:
				#If the current school being checked isn't on the Level X list, then process as normal
					SBPmod = trainOrOpposed(current_card_school, schoolTrn, schoolOpp)
					SBPadd=SBPadd+SBPmod*int(cardLevel[card_school_index])
				card_school_index += 1
		elif '/' in card.school:#		and currentTrnSchool in card.school:
			cardSchools=card.school.split('/')
			cardLevel = int(card.level.split('/')[0])
			#check each school for training first since that will be the lowest cost
			for current_card_school in cardSchools:
				if (current_card_school in spellbook and spellbook[current_card_school]==1):
					SBPadd = multiOrSchool(card, spellbook)
			
				#Might not need this part
			if SBPadd == 0:
				#But for now I'm leaving it in
				for current_card_school in cardSchools:
					if (current_card_school in levelXList):
						#If the current card school is in levelXList compare the level to level x training
						LevelX_index = LevelX_schools.index(current_card_school)
						if int(cardLevel) <= int(LevelX_levels[LevelX_index]):
							SBPmod = 1
							SBPadd = SBPadd+SBPmod*int(cardLevel)
						else:
							SBPmod = 2
							SBPadd = SBPadd+SBPmod*int(cardLevel)
		else:
			LevelX_index = LevelX_schools.index(card.school)
			if  int(card.level)<=int(LevelX_levels[LevelX_index]):	
				SBPadd+=int(card.level)	
			else:
				SBPadd += 2*int(card.level)
	return SBPadd
	
#There's potential to use this more than current, but I'm tired and haven't been able to come up with it fully yet
def trainOrOpposed(cardAttribute, mageTraining, mageOpposed):
	mute()
	if cardAttribute in mageTraining:
		SBPmod=1
	elif cardAttribute in mageOpposed:
		SBPmod=3
	else:
		SBPmod=2
	return SBPmod

def checkCounts(card, cardDict):
	mute()
	if card.name in cardDict:
		cardDict[card.name]+=1
	else:
		cardDict[card.name]=1
	level = getCardLevel(card)
	if "Epic" in card.traits and cardDict[card.name]>1:
		notify("***ILLEGAL DECK***: multiple copies of Epic card {} found in spellbook".format(card.Name))
		return False
	elif level == 1 and cardDict[card.name]>6:
		notify("***ILLEGAL DECK***: there are too many copies of {} in {}'s Spellbook.".format(card.name, me))
		return False
	elif level > 1 and cardDict[card.name]>4:
		notify("***ILLEGAL DECK***: there are too many copies of {} in {}'s Spellbook.".format(card.name, me))
		return False
	
def getCardLevel(card):
	mute()
	l=0
	if "+" in card.Level:
		level = card.Level.split("+")
		for s in level:
			l += int(s)
	elif "/" in card.Level:
		level = card.Level.split("/")
		l = int(level[0])
	else:
		l = int(card.Level)	
	return l
	
#Check for Mage Class Only cards (Warlock Only, etc) and School only (Holy Mage Only)
def checkMageSchoolOnly(card, mageName, schoolTrn):
	mute()
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
	if "Druid" in mageName:
		mageName = "Druid"
		
	schoolList = ["Holy", "Dark", "Mind", "Arcane", "Nature", "War", "Fire", "Water", "Air", "Earth"]
	
	if mageName+" Only" in card.traits:
		ok = True
		
	for s in schoolList:
		if [mageTrn in schoolList for mageTrn in schoolTrn]:
			ok = True

	if not ok:
		notify("***ILLEGAL DECK***: the card {} is not legal in a {} Spellbook.".format(card.Name,mageName))
		return False

#trainOrOpposed
def mageTypeTrnProcessing(card, mageTypeTrnList, mageTypeOppList):
	return

def	checkForNovice(card):
	mute()
	
#Old code below in case it's needed later
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