#######
#v2.2.0.0#
#######


def validateDeck(deck):
	mute()
	spellbook = {}
	mageStats, mageTraining, mageName, spellpointsTotal = statCardParse(deck)
	spellbook = spellbookDictProcessing (mageTraining, spellpointsTotal)
	schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList = getUniqueTraining(spellbook)
	bookTotal=cardPointCount(deck, spellbook, schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList)
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
			comboSTList = []
		#elif key.startswith('L-'): - will need to pick out the level at some point
		else:
			if spellbook[key]==1:
				schoolTrn.append(key)
			else:
				schoolOpp.append(key)

	return [schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList]
	
def	checkForNovice(card):
	mute()
#The ordering and functions can still be cleaned up, but overall it's functional. I've tested blightheart with the siren and it goes fine too.
def cardPointCount(deck, spellbook, schoolTrn, schoolOpp, mageSubtypeTrnList, mageSubtypeOppList, mageTypeTrnList, mageTypeOppList, comboSTList, levelXList):
	mute()
	for card in deck: #run through deck adding levels
		cardCost = 0
		cardSchool = card.school
		cardSubtypeList = card.subtype.replace(' ','').split(',') #Get card Subtype(s)
		cardTypeList = card.type.replace(' ','').split(',') #Get card Type
		if "Mage" in card.Subtype or "Magestats" in card.Subtype:
			debug("Mage, Magestats")
		elif "Novice" in card.Traits:
			SBPadd = int(card.level)
			spellbook['booktotal']+=SBPadd
			#checkForNovice(card) For more academy functionality later.. .maybe
		#Talos doesn't cost anything
		elif "Talos" in card.Name:
			debug("Talos")
		#Check that both the mage is trained/opposed in subtypes and that the card has at least one of those subtypes
		elif mageSubtypeTrnList != [] and True in [cardSubtype in mageSubtypeTrnList for cardSubtype in cardSubtypeList]:
			if '+' in card.school:
				SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp, 1)
				spellbook['booktotal']+=SBPadd
			elif '/' in card.school:
				SBPadd = multiOrSchool(card, spellbook)
			else:
				spellbook['booktotal']+=int(card.level)
		elif "+" in card.school:
			SBPadd = multiAndSchool(card, spellbook, schoolTrn, schoolOpp)
			spellbook['booktotal']+=SBPadd
		elif "/" in card.school:
			SBPadd = multiOrSchool(card, spellbook)
			spellbook['booktotal']+=SBPadd
		#Check if the School of the card is either trained or opposed and add accordingly
		elif cardSchool in spellbook:
			SBPmod = trainOrOpposed(cardSchool, schoolTrn, schoolOpp)
			spellbook['booktotal']+=SBPmod*int(card.level)
		#Check that both the mage is trained/opposed in a type of card and that the card is one of those types
		elif mageTypeTrnList != [] and True in [cardType in mageTypeTrnList for cardType in cardTypeList] and "Mage" not in cardSubtypeList:
			spellbook['booktotal']+=int(card.level)
		elif mageTypeOppList != [] and True in [cardType in mageTypeOppList for cardType in cardTypeList] and "Mage" not in cardSubtypeList:
			spellbook['booktotal']+=3*int(card.level)
		#If nothing else triggers, it should cost 2/level
		else:
			spellbook['booktotal']+=2*int(card.level)
	return spellbook['booktotal']
		
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

def spellbookDictProcessing(mageTraining, spellpointsTotal):
	mute()
	spellbook = dict(mageTraining)
	spellbook = dict(zip(spellbook.keys(), [int(value) for value in spellbook.values()]))
	spellbook["Spellpoints"] = spellpointsTotal
	spellbook["booktotal"] = 0
	return spellbook