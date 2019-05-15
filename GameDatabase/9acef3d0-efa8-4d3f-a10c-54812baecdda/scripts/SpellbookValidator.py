'''#######
#v2.2.0.0#
Created 30 April 2019

Changelog:
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
		elif key.startswith('C-'):
			school, type = key.split('-')[1:]
			comboSTList.append(school)
			comboSTList.append(type)
			if school not in schoolTrn:
				schoolTrn.append(school)
		elif key.startswith('L-'): #- will need to pick out the level at some point
			level, school = key.split('-')[1:3]
			levelXList += [(school, level)]
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
		if not ("Mage" in card.Subtype or "Magestats" in card.Subtype):
			#notify(card.name)
			
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
				continue
				#notify(str(SBPadd))
				#checkForNovice(card) For more academy functionality later.. .maybe
				
			#Talos doesn't cost anything
			if "Talos" in card.Name:
				debug("Talos")
				continue
				
			#Check that both the mage is trained/opposed in subtypes and that the card has at least one of those subtypes
			if mageSubtypeTrnList != [] and True in [cardSubtype in mageSubtypeTrnList for cardSubtype in cardSubtypeList]:
				if '+' in card.school:
					SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp, 1)
					#notify(str(SBPadd))
				elif '/' in card.school:
					SBPadd = multiOrSchool(card, spellbook, True)
					#notify(str(SBPadd))
				else:
					SBPadd += int(card.level)
					#notify("SBPadd: "+str(SBPadd))
					
			#Check that the card has a combination of School and Type that matches the mage's training
			elif (comboSTList != []
				and True in [cardType in comboSTList for cardType in cardTypeList]
				and True in [comboCardSchool in comboSTList for comboCardSchool in cardSchoolList]):
					SBPadd = comboSTListProcess(card, comboSTList, spellbook, schoolTrn, mageTypeTrnList)
					#spellbook['booktotal']+=SBPadd
					#notify(card.name)
					#notify("comboSTList add: "+ str(SBPadd))
					
					
			#Check that both the mage is trained/opposed in a type of card and that the card is one of those types(Forcemaster, creatures = 3)
			elif  ((mageTypeTrnList != [] and True in [cardType in mageTypeTrnList for cardType in cardTypeList])
				or (mageTypeOppList != [] and True in [cardType in mageTypeOppList for cardType in cardTypeList])):
					if mageName == 'Forcemaster' and 'Mind' in cardSchoolList:
						SBPadd = rawCardLevel
					else:
						SBPmod = trainOrOpposed(card.type, mageTypeTrnList, mageTypeOppList)
						SBPadd = rawCardLevel*SBPmod					
					
			#Check for school training (regardless of level at first)
			elif ((True in [cardSchool in schoolTrn for cardSchool in cardSchoolList])
				or (True in [cardSchool in schoolOpp for cardSchool in cardSchoolList])):
					#notify("159: " +card.name)
					if card.school in spellbook:
						#notify("Not Processing levelXList")
						if "+" in card.school:
							SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
						elif "/" in card.school:
							SBPadd = multiOrSchool(card, spellbook)
						else:
							SBPmod = trainOrOpposed(card.school, schoolTrn, schoolOpp)
							SBPadd = SBPmod*int(card.level)
					elif (levelXList != [] and False not in [cardSchool not in schoolOpp for cardSchool in cardSchoolList]):
						#notify("Processing levelXList")
						SBPadd = levelXListProcess(card, levelXList, spellbook, schoolTrn, schoolOpp)
						
					#else:

				
			#If nothing else triggers, it should cost 2/level
			if SBPadd == 0:
				if "+" in card.school:
					SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
				elif "/" in card.school:
					SBPadd = multiOrSchool(card, spellbook)
				else:
					SBPmod = trainOrOpposed(card.school, schoolTrn, schoolOpp)
					SBPadd = SBPmod*int(card.level)

			#This creates a Dict to count all the non-Mage and non-Magestats cards
			checkCounts(card, cardDict)
			
			if "Only" in card.traits:
				checkMageSchoolOnly(card, mageName, schoolTrn)
				#checkSchoolOnly(card, ) This is going to be a pain in the ass for the "Level X" trained mages
				
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
		#SBPadd = 0
		currentTrainedSchoolLevel = levelXList[0:1]
		levelXList = levelXList[1:]
		currentTrnSchool = currentTrainedSchoolLevel[0][0]
		#notify("currentTrnSchool: " + currentTrnSchool)
		currentTrnLevel = int(currentTrainedSchoolLevel[0][1])
		#notify("currentTrnLevel: " + str(currentTrnLevel))
		index = 0
		
		
		
		
		
		
		#If the card in question has a + cost and the mage has training in the card's school...
		if '+' in card.school:# and currentTrnSchool in card.school:		
			cardLevel = card.level.split('+')
			#If the card's level is below threshold, treat normally
			if  int(cardLevel[index])<=currentTrnLevel:	
				tempAdd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
				SBPadd+=tempAdd
				#notify("285 SBPadd: "+str(SBPadd))
				index+=1
			#If the card's level is above, delete the "training" from the list and run the And School processing
			#int(cardLevel[index])=>currentTrnLevel:
			else:
				newSchoolTrn = schoolTrn.remove(currentTrnSchool)
				tempAdd = multiAndSchool(card, spellbook, newSchoolTrn, schoolOpp)
				SBPadd+=tempAdd
				#notify("293 SBPadd: "+str(SBPadd))
				index+=1
		elif '/' in card.school and currentTrnSchool in card.school:
			cardLevel = int(card.level.split('/')[0])				
			SBPadd += int(cardLevel)
			#notify("298 SBPadd: "+str(SBPadd))
		else:
			if  int(card.level)<=currentTrnLevel:	
				SBPadd+=int(card.level)	
				#notify("302 SBPadd: "+str(SBPadd))
			else:
				SBPadd += 2*int(card.level)
				#notify("305 SBPadd: "+str(SBPadd))
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