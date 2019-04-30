'''#######
#v2.2.0.0#
Created 30 April 2019

Changelog:
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
			schoolTrn.append(school)#************ This will need to be done when you to the LevelX stuff too (for X Mage only stuff)
		#elif key.startswith('L-'): - will need to pick out the level at some point
		else:
			if spellbook[key]==1:
				schoolTrn.append(key)
			else:
				schoolOpp.append(key)

	return [schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList]

	
	
#The ordering and functions can still be cleaned up, but overall it's functional. I've tested blightheart with the siren and it goes fine too.
def cardPointCount(deck, spellbook, schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList, mageName):
	mute()
	cardDict = {}
	for card in deck: #run through deck adding levels and checking counts
		#notify(card.name)
		#temporary way to make sure combo checks elements not letters
		if '/' in card.school:
			cardSchool = card.school.replace(' ', '').split('/')
		elif '+' in card.school:
			cardSchool = card.school.replace(' ', '').split('+')
		else:
			cardSchool = [card.school, '']
		#This creates a Dict to count all the non-Mage and non-Magestats cards
		if not ("Mage" in card.subtype or "Magestats" in card.subtype):
			checkCounts(card, cardDict)
			if "Only" in card.traits:
				checkMageSchoolOnly(card, mageName, schoolTrn)
				#checkSchoolOnly(card, ) This is going to be a pain in the ass
		cardSubtypeList = card.subtype.replace(' ','').split(',') #Get card Subtype(s)
		cardTypeList = card.type.replace(' ','').split(',') #Get card Type
		#This ignores the mage and the stats cards since they don't count for SBP 
		if "Mage" in card.Subtype or "Magestats" in card.Subtype:
			debug("Mage, Magestats")
		#Check if the card is Novice. No matter the school, it only costs (card.level) points
		elif "Novice" in card.Traits:
			SBPadd = int(card.level)
			spellbook['booktotal']+=SBPadd
			#notify(str(SBPadd))
			#checkForNovice(card) For more academy functionality later.. .maybe
		#Talos doesn't cost anything
		elif "Talos" in card.Name:
			debug("Talos")
		#Check that both the mage is trained/opposed in subtypes and that the card has at least one of those subtypes
		elif mageSubtypeTrnList != [] and True in [cardSubtype in mageSubtypeTrnList for cardSubtype in cardSubtypeList]:
			if '+' in card.school:
				SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp, 1)
				spellbook['booktotal']+=SBPadd
				#notify(str(SBPadd))
			elif '/' in card.school:
				SBPadd = multiOrSchool(card, spellbook)
				#notify(str(SBPadd))
			else:
				spellbook['booktotal']+=int(card.level)
				#notify(card.level)
		#Check that the card has a combination of School and Type that matches the mage's training
		elif (comboSTList != []
			and True in [cardType in comboSTList for cardType in cardTypeList]
			and True in [comboCardSchool in comboSTList for comboCardSchool in cardSchool]):
				SBPadd = comboSTListProcess(card, comboSTList, spellbook, schoolTrn, mageTypeTrnList)
				spellbook['booktotal']+=SBPadd
				#notify(str(SBPadd))
		#Check for an AND school
		elif "+" in card.school:
			SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
			spellbook['booktotal']+=SBPadd
			#notify(str(SBPadd))
		#Check for an OR school
		elif "/" in card.school:
			SBPadd = multiOrSchool(card, spellbook)
			spellbook['booktotal']+=SBPadd
			#notify(str(SBPadd))
		#Check if the School of the card is either trained or opposed and add accordingly
		elif card.school in spellbook:
			SBPmod = trainOrOpposed(card.school, schoolTrn, schoolOpp)
			spellbook['booktotal']+=SBPmod*int(card.level)
			#notify(str(SBPmod*int(card.level)))
		#Check that both the mage is trained/opposed in a type of card and that the card is one of those types
		elif mageTypeTrnList != [] and True in [cardType in mageTypeTrnList for cardType in cardTypeList] and "Mage" not in cardSubtypeList:
			spellbook['booktotal']+=int(card.level)
		elif mageTypeOppList != [] and True in [cardType in mageTypeOppList for cardType in cardTypeList] and "Mage" not in cardSubtypeList:
			spellbook['booktotal']+=3*int(card.level)
		#If nothing else triggers, it should cost 2/level
		else:
			spellbook['booktotal']+=2*int(card.level)
			#notify(str(2*int(card.level)))
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



def multiOrSchool(card, spellbook):	
	mute()
	schools = card.school.split('/')
	cardLevel = int(card.level.split('/')[0])
	SBPmod = 2
	for s in schools:
		if s in spellbook and spellbook[s]==1:
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
	
	
#There's potential to use this more than current, but I'm tired and haven't been able to come up with it fully yet
def trainOrOpposed(cardSchool, schoolTrn, schoolOpp):
	mute()
	if cardSchool in schoolTrn:
		SBPmod=1
	elif cardSchool in schoolOpp:
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



def	checkForNovice(card):
	mute()