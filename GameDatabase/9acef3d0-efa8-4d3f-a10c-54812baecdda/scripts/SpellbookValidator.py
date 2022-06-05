'''#######
#v2.2.0.0#
Created 30 April 2019

Changelog: (just for fun, nothing actually helpful here anymore)
	Sharkbait: 17 May 2022:
		What is it about May and me redoing this script? Anyway, refactored again and it's much betterTM now. It can still be improved, but this will do for the moment


	Sharkbait: 16 May 2020: 
		hahaha.... a year later. Anyways, I fixed the issue with multi school, level X cost spells with the druid.
		This doesn't address mage-only cards for level X yet, but I'm not sure it's super necessary right now.
	
	
	Sharkbait: 15 May 2019:
		Fixed a few errors. The Level X code was causing the level X logic to apply to all training a mage had, not just the 
		school that was trained up to Level X. It has been adjusted now to check for the whole school training first. Subtype
		training was causing an issue where the spellbookPointsToAdd could be overwritten, so I made it part of the if/elif branching scheme. 
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
	#deck object comes from OCTGN API
	mute()
	mageStatCard = findMageStatCard(deck)
	if mageStatCard == "Your deck is missing a Magestats card.":
		notify(mageStatCard)
	else:
		calculatedSpellbookPointTotal = createSpellbookAndCheck(deck, mageStatCard)
		notify("Spellbook of {} calculated to {} points".format(me,calculatedSpellbookPointTotal))
	return True

def findMageStatCard(deck):
	mute()
	for card in deck:
		if card.Type == 'Magestats':
			return card
	return "Your deck is missing a Magestats card."

def createSpellbookAndCheck(deck, mageStatCard):
	mute()
	cardDict = {}
	totalBookPointsCost = 0
	for card in deck: #run through deck adding levels and checking counts
		if not ("Mage" in card.Subtype or "Magestats" in card.Subtype or "Aura" in card.Subtype or "Talos" in card.Name):#None of these cards cost points to include
			debug(card.name)
			totalBookPointsCost += countCardPointCost(mageStatCard, card)
			debug(totalBookPointsCost)

			#This creates a Dict to count and check limits on all the non-Mage and non-Magestats cards.
			checkCounts(card, cardDict)
			
			checkForMageSchoolRestrictionViolation(mageStatCard, card)

	return totalBookPointsCost

def countCardPointCost(mageStatCard, card):
	cardPointsCost = 0
	totalCardLevel = getTotalCardLevel(card)
	if isNovice(card):
		debug('Novice')
		cardPointsCost += addPoints('trained', totalCardLevel)
	elif isCardCombo(mageStatCard, card):
		debug('Combo')
		cardPointsCost += addPoints('trained', totalCardLevel)
	elif isSubtypeInTraining(mageStatCard, card):
		debug('Subtype')
		cardPointsCost += addPoints('trained', totalCardLevel)
	elif compareToPartialTraining(mageStatCard, card):
		debug('Partial')
		cardPointsCost += partialTrainingPointsToAdd(mageStatCard, card)
	elif isOpposedCardType(mageStatCard, card):
		debug('Opposed Type Match')
		cardPointsCost += addPoints('opposed', totalCardLevel)
	elif (hasSchoolMatch(mageStatCard.MageSchoolFullTraining, card)) or (hasSchoolMatch(mageStatCard.MageSchoolOpposed, card)):
		debug('Full or OpposedMatch')
		cardPointsCost += addPointsBasedOnFullSchoolTraining(mageStatCard, card)
	else:
		debug('No Train or Opposed')
		cardPointsCost += addPoints('neutral', totalCardLevel)
	return cardPointsCost

def addPoints(training, level):
	if training == 'trained':
		multiplier = 1
		cardPointsCost = multiplier*level
	elif training == 'opposed':
		multiplier = 3
		cardPointsCost = multiplier*level
	else:
		multiplier = 2
		cardPointsCost = multiplier*level
	return cardPointsCost

def splitCardProperty(card, property):
	splitProperty = getattr(card, property)
	if '+' in splitProperty:
		cardProperty = splitProperty.split('+')
	else:
		cardProperty = splitProperty.split('/')
	return cardProperty

def isOpposedCardType(mageTypeOpposed, card):
	cardType = card.type.replace(' ','').split(',')
	if mageTypeOpposed in cardType:
		return	True
	else:
		return False

#Still some refactoring to do here
def addPointsBasedOnFullSchoolTraining(mageStatCard, card):
	cardPointsCost = 0
	cardSchoolList = splitCardProperty(card, 'school')
	training = mageStatCard.MageSchoolFullTraining
	opposed = mageStatCard.MageSchoolOpposed
	if '+' in card.School:
		cardLevelList = splitCardProperty(card, 'level')
		for school in cardSchoolList:
			if school in training:
				cardLevelIndex = cardSchoolList.index(school)
				cardPointsCost += addPoints('trained', int(cardLevelList[cardLevelIndex]))
			elif school in opposed:
				cardLevelIndex = cardSchoolList.index(school)
				cardPointsCost += addPoints('opposed', int(cardLevelList[cardLevelIndex]))
			else:
				cardLevelIndex = cardSchoolList.index(school)
				cardPointsCost += addPoints('neutral', int(cardLevelList[cardLevelIndex]))		
	else:
		cardLevel = getTotalCardLevel(card)
		opposedFound = []
		trainingFound = False
		for school in cardSchoolList:
			if school in training:
				trainingFound = True
				opposedFound.append(False)
			elif school in opposed:
				opposedFound.append(True)
			else:
				opposedFound.append(False)
		if trainingFound:
			cardPointsCost = addPoints('trained', cardLevel)
		elif all(opposedFound):
			cardPointsCost = addPoints('opposed', cardLevel)
		else:
			cardPointsCost = addPoints('neutral', cardLevel)
	return cardPointsCost

def compareToPartialTraining(mageStatCard, card):
	if mageStatCard.MageSchoolPartialTraining != '':
		mageSchoolPartialTraining = mageStatCard.MageSchoolPartialTraining.replace(' ','').split(',')
		if hasSchoolMatch(mageSchoolPartialTraining, card):
			return hasLevelMatch(mageSchoolPartialTraining, card)
		else:
			return False
	return False

def hasSchoolMatch(Training, card):
	cardSchool = splitCardProperty(card, 'school')
	for school in cardSchool:
		if school in Training:
			return True
	return False

def hasLevelMatch(Training, card):
	cardSchool = splitCardProperty(card, 'school')
	cardLevel = splitCardProperty(card, 'level')
	for school in cardSchool:
		if school in Training:
			mageSchoolLevelIndex = Training.index(school)+1
			cardLevelIndex = cardSchool.index(school)
			if int(Training[mageSchoolLevelIndex]) >= int(cardLevel[cardLevelIndex]):
				return True
	return False

#Still some refactoring to do here
def partialTrainingPointsToAdd(mageStatCard, card):
	mageSchoolPartialTraining = mageStatCard.MageSchoolPartialTraining.replace(' ','').split(',')
	if '+' in card.School:
		cardPointsCost = 0
		cardSchool = splitCardProperty(card, 'school')
		cardLevel = splitCardProperty(card, 'level')
		for school in cardSchool:
			if school in mageSchoolPartialTraining:
				mageSchoolLevelIndex = mageSchoolPartialTraining.index(school)+1
				cardLevelIndex = cardSchool.index(school)
				if int(mageSchoolPartialTraining[mageSchoolLevelIndex]) >= int(cardLevel[cardLevelIndex]):
					cardPointsCost += addPoints('trained', int(cardLevel[cardLevelIndex]))
				else:
					cardPointsCost += addPoints('neutral', int(cardLevel[cardLevelIndex]))	
			elif school in mageStatCard.MageSchoolFullTraining.replace(' ','').split(','):
				cardLevelIndex = cardSchool.index(school)
				cardPointsCost += addPoints('trained', int(cardLevel[cardLevelIndex]))
			else:
				cardLevelIndex = cardSchool.index(school)
				cardPointsCost += addPoints('neutral', int(cardLevel[cardLevelIndex]))
		return cardPointsCost		
	else:
		cardLevel = getTotalCardLevel(card)
		cardPointsCost = addPoints('trained', cardLevel)		
		return cardPointsCost

def isSubtypeInTraining(mageStatCard, card): 
	if mageStatCard.MageSubtypeTraining != '' and card.Subtype != '':
		cardSubtypeList = card.subtype.replace(' ','').split(',')
		if True in [cardSubtype in mageStatCard.MageSubtypeTraining for cardSubtype in cardSubtypeList]:
			return True
		else:
			return False
	else:
		return False

def isCardCombo(mageStatCard, card):
	if mageStatCard.MageComboTraining != '':
		comboFlag = True
		mageComboTraining = mageStatCard.MageComboTraining.Split(';')
		for element in mageComboTraining:
			testableAttributes = element.replace(' ','').split(',')
			if not testableAttributes[0] in getattr(card, testableAttributes[1]): 
				comboFlag = False
				return comboFlag
		return comboFlag
	return False


def isNovice(card):
    if "Novice" in card.Traits:
        return True
    else:
        return False

def getTotalCardLevel(card):
	if '/' in card.school:
		totalCardLevel = card.level.split('/')[0]
		totalCardLevel = int(totalCardLevel)
	elif '+' in card.school:
		cardLevel = card.level.split('+')
		totalCardLevel = 0
		for level in cardLevel:
			totalCardLevel += int(level)
	else:
		totalCardLevel = int(card.level)
	return totalCardLevel


def checkCounts(card, cardDict):
	mute()
	cardDict = addCardToCardDict(card, cardDict)
	level = getTotalCardLevel(card)
	if "Epic" in card.traits and cardDict[card.name]>1:
		notify("***ILLEGAL DECK***: multiple copies of Epic card {} found in spellbook".format(card.Name))
		return False
	elif level == 1 and cardDict[card.name]>6:
		notify("***ILLEGAL DECK***: there are too many copies of {} in {}'s Spellbook.".format(card.name, me))
		return False
	elif level > 1 and cardDict[card.name]>4:
		notify("***ILLEGAL DECK***: there are too many copies of {} in {}'s Spellbook.".format(card.name, me))
		return False

def addCardToCardDict(card, cardDict):
	mute()
	if card.name in cardDict:
		cardDict[card.name]+=1
	else:
		cardDict[card.name]=1
	return cardDict

def checkForMageSchoolRestrictionViolation(mageStatCard, card):
	if "Only" in card.traits:
		mageRestrictionName = mageStatCard.Nickname.replace(' ','').split('Stats')[0]
		if isCorrectMage(card, mageRestrictionName) or isCorrectSchool(mageStatCard, card):
			return False
		else:
			notify("***ILLEGAL DECK***: the card {} is not legal in a {} Spellbook.".format(card.Name,mageStatCard.Name.split(" Stats")[0]))
			return True
	return False

def isCorrectMage(card, name):
	legal = False
	if name+" Only" in card.traits:
		legal = True
	return legal

def isCorrectSchool(mageStatCard, card):
	legal = False
	if compareToPartialTraining(mageStatCard, card):
		legal = True
	elif (hasSchoolMatch(mageStatCard.MageSchoolFullTraining, card)):
		legal = True
	return legal
