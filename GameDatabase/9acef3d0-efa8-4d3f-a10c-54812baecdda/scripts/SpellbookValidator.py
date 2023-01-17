#from APIMock import *


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
			debug(card.Name)
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
	elif (hasSchoolMatch(mageStatCard.MageSchoolFullTraining, card)) or (hasSchoolMatch(mageStatCard.MageSchoolOpposed, card)):
		debug('Full or OpposedMatch')
		cardPointsCost += addPointsBasedOnFullSchoolTraining(mageStatCard, card)
	elif isOpposedCardType(mageStatCard, card):
		debug('Opposed Type Match')
		cardPointsCost += addPoints('opposed', totalCardLevel)
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

def isOpposedCardType(mageStatCard, card):
	if mageStatCard.MageTypeOpposed != '':
		cardType = card.Type.replace(' ','')
		if True in [cardType in mageStatCard.MageTypeOpposed]:
			return True
		else:
			return False
	else:
		return False

'''def isOpposedCardType(mageTypeOpposed, card):
	cardType = card.Type.replace(' ','').split(',')
	if mageTypeOpposed in cardType:
		return	True
	else:
		return False'''

#Still some refactoring to do here
def addPointsBasedOnFullSchoolTraining(mageStatCard, card):
	cardPointsCost = 0
	cardSchoolList = splitCardProperty(card, 'School')
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
	cardSchool = splitCardProperty(card, 'School')
	for school in cardSchool:
		if school in Training:
			return True
	return False

def hasLevelMatch(Training, card):
	cardSchool = splitCardProperty(card, 'School')
	cardLevel = splitCardProperty(card, 'Level')
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
		cardSchool = splitCardProperty(card, 'School')
		cardLevel = splitCardProperty(card, 'Level')
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
		mageComboTraining = mageStatCard.MageComboTraining.split(';')
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
	if '/' in card.School:
		totalCardLevel = card.Level.split('/')[0]
		totalCardLevel = int(totalCardLevel)
	elif '+' in card.School:
		cardLevel = card.Level.split('+')
		totalCardLevel = 0
		for level in cardLevel:
			totalCardLevel += int(level)
	else:
		totalCardLevel = int(card.Level)
	return totalCardLevel


def checkCounts(card, cardDict):
	mute()
	cardDict = addCardToCardDict(card, cardDict)
	level = getTotalCardLevel(card)
	if "Epic" in card.Traits and cardDict[card.Name]>1:
		notify("***ILLEGAL DECK***: multiple copies of Epic card {} found in spellbook".format(card.Name))
		return False
	elif level == 1 and cardDict[card.Name]>6:
		notify("***ILLEGAL DECK***: there are too many copies of {} in {}'s Spellbook.".format(card.Name, me))
		return False
	elif level > 1 and cardDict[card.Name]>4:
		notify("***ILLEGAL DECK***: there are too many copies of {} in {}'s Spellbook.".format(card.Name, me))
		return False

def addCardToCardDict(card, cardDict):
	mute()
	if card.Name in cardDict:
		cardDict[card.Name]+=1
	else:
		cardDict[card.Name]=1
	return cardDict

def checkForMageSchoolRestrictionViolation(mageStatCard, card):
	if "Only" in card.Traits:
		mageRestrictionName = mageStatCard.Nickname.replace(' ','').split('Stats')[0]
		if isCorrectMage(card, mageRestrictionName) or isCorrectSchool(mageStatCard, card):
			return False
		else:
			notify("***ILLEGAL DECK***: the card {} is not legal in a {} Spellbook.".format(card.Name,mageStatCard.Name.split(" Stats")[0]))
			return True
	return False

def isCorrectMage(card, name):
	legal = False
	if name+" Only" in card.Traits:
		legal = True
	return legal

def isCorrectSchool(mageStatCard, card):
	legal = False
	if compareToPartialTraining(mageStatCard, card):
		legal = True
	elif (hasSchoolMatch(mageStatCard.MageSchoolFullTraining, card)):
		legal = True
	return legal
