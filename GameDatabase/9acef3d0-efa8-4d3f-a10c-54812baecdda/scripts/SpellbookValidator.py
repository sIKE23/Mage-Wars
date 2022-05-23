'''#######
#v2.2.0.0#
Created 30 April 2019

Changelog:
	Sharkbait: 17 May 2022:
		What is it about May and me redoing this script? Anyway, refactored again and it's much betterTM now.


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
	#rewrite to be a dictionary that gets passed?
	mageSchoolFullTraining, mageSchoolOpposed, mageSchoolPartialTraining, mageSubtypeTraining, mageComboTraining, mageTypeOpposed, mageName = parseMageStatCard(deck)
	bookTotal = createSpellbookAndCheck(deck, mageSchoolFullTraining, mageSchoolOpposed, mageSchoolPartialTraining, mageSubtypeTraining, mageComboTraining, mageTypeOpposed, mageName)
	notify("Spellbook of {} calculated to {} points".format(me,bookTotal))
	return True

def parseMageStatCard(deck):
    mute()
    for c in deck:
        debug(c.name)
        if c.Type == "Magestats":
            mageSchoolFullTraining = c.MageSchoolFullTraining.replace(' ','').split(',')
            mageSchoolOpposed = c.MageSchoolOpposed.replace(' ','').split(',')
            mageSchoolPartialTraining = c.MageSchoolPartialTraining.replace(' ','').split(',')
            mageSubtypeTraining = c.MageSubtypeTraining.replace(' ','').split(',')
            mageComboTraining = c.MageComboTraining.replace(' ','').split(';')#might need to rework this a bit on the set.xml property line. School = Holy, Type = Creature?
            mageTypeOpposed = c.MageTypeOpposed.replace(' ','').split(',')
            mageName = c.name.split(" Stats")[0]
            break
    return [mageSchoolFullTraining, mageSchoolOpposed, mageSchoolPartialTraining, mageSubtypeTraining, mageComboTraining, mageTypeOpposed, mageName]
	
def createSpellbookAndCheck(deck, mageSchoolFullTraining, mageSchoolOpposed, mageSchoolPartialTraining, mageSubtypeTraining, mageComboTraining, mageTypeOpposed, mageName):
	mute()
	cardDict = {}
	totalBookPointsCost = 0
	for card in deck: #run through deck adding levels and checking counts
		if not ("Mage" in card.Subtype or "Magestats" in card.Subtype or "Aura" in card.Subtype or "Talos" in card.Name):#None of these cards cost points to include
			debug(card.name)
			totalBookPointsCost += countSpellbookPointTotal(card, mageSchoolFullTraining, mageSchoolOpposed, mageSchoolPartialTraining, mageSubtypeTraining, mageComboTraining, mageTypeOpposed)
			debug(totalBookPointsCost)
			
			#This creates a Dict to count and check limits on all the non-Mage and non-Magestats cards.
			checkCounts(card, cardDict)

			if "Only" in card.traits:
				checkMageSchoolOnly(card, mageName, [mageSchoolFullTraining,mageSchoolPartialTraining])
	return totalBookPointsCost

def countSpellbookPointTotal(card, mageSchoolFullTraining, mageSchoolOpposed, mageSchoolPartialTraining, mageSubtypeTraining, mageComboTraining, mageTypeOpposed):
	spellbookPointTotal = 0
	rawCardLevel = getRawCardLevel(card)
	if isNovice(card):
		debug('Novice')
		multiplier = 1
		spellbookPointTotal += rawCardLevel*multiplier
		debug(spellbookPointTotal)
	elif mageComboTraining != [''] and compareCardToCombo(mageComboTraining, card):
		debug('Combo')
		multiplier = 1
		spellbookPointTotal += rawCardLevel*multiplier
	elif mageSubtypeTraining != [''] and compareSubtypeToTraining(mageSubtypeTraining, card):
		debug('Subtype')
		multiplier = 1
		spellbookPointTotal += rawCardLevel*multiplier
		debug(spellbookPointTotal)
	elif mageSchoolPartialTraining != [''] and compareToPartialTraining(mageSchoolPartialTraining, card):
		debug('Partial')
		spellbookPointTotal += partialTrainingPointsToAdd(mageSchoolPartialTraining, card)
		debug(spellbookPointTotal)
	elif mageSchoolFullTraining !=[''] and hasSchoolMatch(mageSchoolFullTraining, card):
		debug('FullMatch')
		spellbookPointTotal += fullSchoolTrainingPointsToAdd(mageSchoolFullTraining, mageSchoolOpposed, card)
		debug(spellbookPointTotal)
	elif mageTypeOpposed !=[''] and isOpposedCardType(mageTypeOpposed, card):
		debug('Opposed Type Match')
		multiplier = 3
		spellbookPointTotal += rawCardLevel*multiplier
		debug(spellbookPointTotal)
	elif mageSchoolOpposed !=[''] and isOpposedCardSchool(mageSchoolOpposed,card):
		debug('School Opposed Match')
		multiplier = 3
		spellbookPointTotal += rawCardLevel*multiplier
		debug(spellbookPointTotal)
	else:
		debug('No Train or Opposed')
		multiplier = 2
		spellbookPointTotal += rawCardLevel*multiplier
		debug(spellbookPointTotal)
	return spellbookPointTotal

def splitCardSchool(card):
	if '+' in card.School:
		cardSchool = card.school.split('+')
	else:
		cardSchool = card.school.split('/')
	return cardSchool

def splitCardLevel(card):
	if '+' in card.Level:
		cardLevel = card.level.split('+')
	else:
		cardLevel = card.level.split('/')
	return cardLevel

def isOpposedCardSchool(mageSchoolOpposed,card):
	cardSchool = splitCardSchool(card)
	opposedFound = []
	for school in cardSchool:
		if school in mageSchoolOpposed:
			opposedFound.append(True)
		else:
			opposedFound.append(False)
	if True in opposedFound:
		return True
	else:
		return False

def isOpposedCardType(mageTypeOpposed, card):
	cardType = card.type.replace(' ','').split(',')
	if mageTypeOpposed in cardType:
		return	True
	else:
		return False

def fullSchoolTrainingPointsToAdd(Training, opposed, card):
	if '+' in card.School:
		spellbookPointsToAdd = 0
		cardSchool = splitCardSchool(card)
		cardLevel = splitCardLevel(card)
		for school in cardSchool:
			if school in Training:
				cardLevelIndex = cardSchool.index(school)
				multiplier = 1
				spellbookPointsToAdd += int(cardLevel[cardLevelIndex])*multiplier
			elif school in opposed:
				cardLevelIndex = cardSchool.index(school)
				multiplier = 3
				spellbookPointsToAdd += int(cardLevel[cardLevelIndex])*multiplier
			else:
				cardLevelIndex = cardSchool.index(school)
				multiplier = 2
				spellbookPointsToAdd += int(cardLevel[cardLevelIndex])*multiplier
		return spellbookPointsToAdd		
	else:
		cardLevel = getRawCardLevel(card)
		multiplier = 1
		spellbookPointsToAdd = cardLevel*multiplier			
		return spellbookPointsToAdd

def compareToPartialTraining(mageSchoolPartialTraining, card):
	if hasSchoolMatch(mageSchoolPartialTraining, card):
		return hasLevelMatch(mageSchoolPartialTraining, card)
	else:
		return False

def hasSchoolMatch(Training, card):
	cardSchool = splitCardSchool(card)
	for school in cardSchool:
		if school in Training:
			return True
	return False

def hasLevelMatch(mageSchoolPartialTraining, card):
	cardSchool = splitCardSchool(card)
	cardLevel = splitCardLevel(card)
	for school in cardSchool:
		if school in mageSchoolPartialTraining:
			mageSchoolLevelIndex = mageSchoolPartialTraining.index(school)+1
			cardLevelIndex = cardSchool.index(school)
			if int(mageSchoolPartialTraining[mageSchoolLevelIndex]) >= int(cardLevel[cardLevelIndex]):
				return True
	return False


def partialTrainingPointsToAdd(mageSchoolPartialTraining, card):
	if '+' in card.School:
		spellbookPointsToAdd = 0
		cardSchool = splitCardSchool(card)
		cardLevel = splitCardLevel(card)
		for school in cardSchool:
			if school in mageSchoolPartialTraining:
				mageSchoolLevelIndex = mageSchoolPartialTraining.index(school)+1
				cardLevelIndex = cardSchool.index(school)
				if int(mageSchoolPartialTraining[mageSchoolLevelIndex]) >= int(cardLevel[cardLevelIndex]):
					multiplier = 1
					spellbookPointsToAdd += int(cardLevel[cardLevelIndex])*multiplier
				else:
					multiplier = 2
					spellbookPointsToAdd += int(cardLevel[cardLevelIndex])*multiplier	
			else:
				cardLevelIndex = cardSchool.index(school)
				multiplier = 2
				spellbookPointsToAdd += int(cardLevel[cardLevelIndex])*multiplier
		return spellbookPointsToAdd		
	else:
		cardLevel = getRawCardLevel(card)
		multiplier = 1
		spellbookPointsToAdd = cardLevel*multiplier			
		return spellbookPointsToAdd

def compareSubtypeToTraining(mageSubtypeTraining, card):
	cardSubtypeList = card.subtype.replace(' ','').split(',') 	#Get card Subtype(s)
	if True in [cardSubtype in mageSubtypeTraining for cardSubtype in cardSubtypeList]:
		return True
	else:
		return False

def compareCardToCombo(mageComboTraining, card):
	comboFlag = True
	for element in mageComboTraining:
		testableAttributes = element.replace(' ','').split(',')
		if not testableAttributes[0] in getattr(card, testableAttributes[1]): 
			comboFlag = False
			return comboFlag
	return comboFlag


def isNovice(card):
    if "Novice" in card.Traits:
        return True
    else:
        return False

def getRawCardLevel(card):
	if '/' in card.school:
		rawCardLevel = card.level.split('/')[0]
		rawCardLevel = int(rawCardLevel)
	elif '+' in card.school:
		cardLevel = card.level.split('+')
		rawCardLevel = 0
		for level in cardLevel:
			rawCardLevel += int(level)
	else:
		rawCardLevel = int(card.level)
	return rawCardLevel


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
		
	if [mageTrn in schoolList for mageTrn in schoolTrn]:
		ok = True

	if not ok:
		notify("***ILLEGAL DECK***: the card {} is not legal in a {} Spellbook.".format(card.Name,mageName))
		return False
