############################################################################
######################		Trait Computation	####################
############################################################################
"""
This section contains functions that figure out exactly which traits a card has.
"""

def getBasicTraits(card):
	"Returns basic traits intrinsic to the card"

	traits = card.Traits.split(", ")
	if "" in traits: traits.remove("")
	basicTraits = {'Creature' : ['Living','Corporeal'],
					'Conjuration' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity'],
					'Conjuration-Wall' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity']}.get(card.Type,[])

	if 'Living' in traits and 'Nonliving' in basicTraits: basicTraits.remove('Nonliving')
	elif 'Nonliving' in traits and 'Living' in basicTraits: basicTraits.remove('Living')
	if 'Incorporeal' in traits and 'Corporeal' in basicTraits: basicTraits.remove('Corporeal')

	traits.extend(basicTraits)
	return traits

def computeTraits(card):
		"""This is the centralized function that reads all traits possessed by a card. Do NOT compute traits anywhere else, ONLY compute them here.
		It returns a dictionary of traits. This function will end up being quite long and complex.It works together with traitParser. Standard format
		for traits is a dictionary."""
		traitDict = {}
		markers = card.markers
		name = card.name
		controller = card.controller
		subtype = card.subtype
		cardType = card.type
		school = card.school
		rawTraitsList = getBasicTraits(card)
		append = rawTraitsList.append
		extend = rawTraitsList.extend
		remove = rawTraitsList.remove

		#Search history for buffs
		extend(rememberBuffs(card))

		adraAbility = True
		adraEnemy = bool([c for c in table if c.name=="Adramelech Warlock" and c.controller != controller])
		for c in table: #scan cards in table for bonuses. We want to minimize iterations, so we'll scan only once.
				cName = c.name
				cController = c.controller
				cSubtype = c.subtype
				cType = c.type
				cBuffs = c.cBuffs
				if 'Mage' in cSubtype and cController == controller and 'Magestats' not in cType: 
					traitDict['MageID'] = c._id #Each card knows which mage controls it.
					mage = Card(traitDict['MageID'])
				#debug("c Name: {}".format(cName))
				#Search arena for passive buffs
				if cBuffs and c.isFaceUp:
					cBuffRange = cBuffs.split("))")[0]
					cBuffString = cBuffs.split("))")[1]
					if cBuffRange=="inf" or rangeMatcher(c,card,cBuffRange): extend(buffMatcher(c,card,cBuffString))

		if markers[Melee]: append('Melee +{}'.format(str(markers[Melee])))
		if markers[Ranged]: append('Ranged +{}'.format(str(markers[Ranged])))
		if markers[Armor]: append('Armor +{}'.format(str(markers[Armor])))
		if markers[Growth]: extend(['Life +{}'.format(str(3*markers[Growth])),'Melee +{}'.format(str(markers[Growth]))])
		if markers[Corrode]: append('Armor -{}'.format(str(markers[Corrode])))
		if markers[Guard]: 
			extend(['Counterstrike','Non-Flying'])
			if 'Flying' in listedTraits and 'Non-Flying' in rawTraitsList: remove('Flying')
		if markers[Sleep] or markers[Stun] or markers[Slam]: append('Incapacitated')
		if markers[Zombie] :
				extend(['Psychic Immunity','Slow','Nonliving','Bloodthirsty +0'])
				remove('Living')
				#Also should add undead,zombie subtypes, but no way to do that without the spellDictionary.
		if markers[Stuck] : extend(['Restrained','Unmovable'])
		if markers[Daze]: append('Defense -{}'.format(str(markers[Daze])))
		if markers[Light]: append('Light +{}'.format(str(markers[Light])))

		if markers[Pet] and 'Animal' in subtype: extend(['Melee +1','Armor +1','Life +3'])
		if markers[BloodReaper] and 'Demon' in subtype: append('Bloodthirsty +2')
		if markers[EternalServant] and 'Undead' in subtype and not "Legendary" in card.Traits: append('Piercing +1')
		if markers[Treebond] and 'Tree' in subtype: extend(['Innate Life +4','Armor +1','Lifebond +2'])
		if markers[Veteran] and 'Soldier' in subtype: extend(['Armor +1','Melee +1'])
		if markers[HolyAvenger] and 'Holy' in card.School and not 'Legendary' in card.Traits: append('Life +5')
		if markers[Wrath]: append('Melee +{}'.format(str(markers[Wrath])))
		if markers[Rage]: append('Melee +{}'.format(str(markers[Rage])))
		if markers[SirensCall] and 'Aquatic' in subtype and "Siren" in mage.name and 'Mage' not in subtype: extend(['Melee +2'])
		if markers[Grapple]: extend(['Melee -2'])
		if markers[EarthGlyphActive] and 'Magestats' not in card.Type: append('Armor +2')


		if 'Unstoppable' in rawTraitsList: extend(['Unmovable','Uncontainable'])
		if 'Incorporeal' in rawTraitsList: extend(['Nonliving','Burnproof','Uncontainable'])
		if 'Nonliving' in rawTraitsList: extend(['Poison Immunity','Finite Life'])
		if 'Rooted' in rawTraitsList: extend(['Unmovable','Non-Flying'])
		if 'Restrained' in rawTraitsList: extend(['Defense -2','Non-Flying'])
		if 'Incapacitated' in rawTraitsList and 'Flying' in listedTraits: remove('Flying')

		if (name == 'Gargoyle Sentry' and markers[Guard]): extend(['Armor +3','Tough -3'])
		elif (name == 'Dwarf Panzergarde' and markers[Guard]): extend(['Defense +3'])
		if (name == 'Dragonclaw Wolverine' and markers[Rage]):
				append('Armor +{}'.format(str(markers[Rage])))
				if markers[Rage] >= 3: append('Counterstrike')

		if 'Non-Flying' in rawTraitsList: rawTraitsList = [t for t in list(rawTraitsList) if t != 'Flying' and t != 'Non-Flying']

		for rawTrait in rawTraitsList:
				formTrait = traitParser(rawTrait)
				if formTrait[0] in additiveTraits: traitDict[formTrait[0]] = traitDict.get(formTrait[0],0) + (0 if formTrait[1] == '-' else int(formTrait[1]))
				elif formTrait[0] in superlativeTraits: traitDict[formTrait[0]] = max(traitDict.get(formTrait[0],0),int(formTrait[1]))
				elif formTrait[0] == 'Immunity':
						if not traitDict.get('Immunity'): traitDict['Immunity'] = [formTrait[1]]
						else: traitDict['Immunity'].append(formTrait[1])
				else: traitDict[formTrait[0]] = True
		traitDict['OwnerID'] = card._id #Tag the dictionary with its owner's ID in case we need to extract it later (extracting the owner is MUCH faster than extracting the dictionary)
		debug("traitDict: {}".format)
		return traitDict

def traitParser(traitStr):
		"""Reads a single trait and returns it in a standardized, parsed form. Should be used for everything that needs to read traits as information.
		Each trait is returned as a list with 1-2 values, with the first value being the identifier and the second being the value. The computeTraits
		function will take this list and output a dictionary, which will be the standard format for readable traits."""
		formattedTrait = [traitStr,True]
		if ' vs. ' in traitStr:
				vsList = traitStr.split(' vs. ')
				vsList.reverse()
				vsList[1] = int(vsList[1].replace('+',''))
				formattedTrait = ['VS',vsList]
		elif " +" in traitStr and traitStr.split(' +')[0] in additiveTraits:
				try: formattedTrait = [traitStr.split(' +')[0], int(traitStr.split(' +')[1])]
				except: formattedTrait = [traitStr.split(' +')[0], 0]
		elif " -" in traitStr and traitStr.split(' -')[0] in additiveTraits:
				try: formattedTrait = [traitStr.split(' ')[0], int(traitStr.split(' ')[1])]
				except: [traitStr.split(' ')[0], 0]
		elif " Immunity" in traitStr: formattedTrait = ["Immunity",traitStr.split(' ')[0]]
		for s in superlativeTraits:
				if s in traitStr: formattedTrait = traitStr.split(' ')
		return formattedTrait

"""
Trait and Attack Adjustments

The following functions evaluate the adjusted traits and attacks of a card, given the
state of the game and the cards attached to it.
"""

def getStatusDict(card): #Will later expand to make this more useful
		if card.Subtype == 'Mage': return {'Damage' : card.controller.Damage, 'Mana' : card.controller.Mana}
		else: return {'Damage' : card.markers[Damage], 'Mana' : card.markers[Mana]}

def computeArmor(aTraitDict,attack,dTraitDict):
		baseArmor = (getStat(Card(dTraitDict['OwnerID']).Stats,'Armor') if 'OwnerID' in dTraitDict else 0)
		return max(baseArmor+dTraitDict.get('Armor',0)-attack.get('Traits',{}).get('Piercing',0),0)

def getRemainingLife(cTraitDict):
		card = Card(cTraitDict.get('OwnerID'))
		damage =  card.markers[Damage] + card.markers[Tainted]*3 + (card.controller.damage if card.Subtype=="Mage" else 0)
		life = (card.controller.life if card.Subtype=="Mage" else (getStat(card.Stats,'Life') + cTraitDict.get('Life',0) + cTraitDict.get('Innate Life',0)))
		if life: return max(life - damage,0)