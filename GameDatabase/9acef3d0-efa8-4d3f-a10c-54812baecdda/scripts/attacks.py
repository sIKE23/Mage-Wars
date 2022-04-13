#######
#v3.0.0.0#
#######
# -*- coding: utf-8 -*-
import sys
sys.path.append(wd("lib"))
from math import factorial
from copy import deepcopy
"""
Mage Wars Attacks Module

This module contains the functions relating to dice rolling and battle computations
"""

############################################################################
######################		Definitions	####################
############################################################################

additiveTraits = ["Melee","Ranged",
				  "Armor","Life","Innate Life","Channeling","Defense",
				  "Tough",
				  "Charge",
				  "Bloodthirsty",
				  "Piercing",
				  "Mana Drain",
				  "Mana Transfer",
				  "Magebind",
				  "Lifebond",
				  "Lifegain",
				  "Upkeep",
				  'Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic']
superlativeTraits = ["Regenerate",
					 "Aegis",
					 "Uproot",
					 "Dissipate",
					 "Ki",
					 "Sai"
					 "Nunchucks",
					 "Melting"]

############################################################################
######################		Attack Choice Prompt		####################
############################################################################
"""
#WIP need to update this description
The entire module is called through this function. All definitions of data should go through here.

---Code Structure---

diceRollMenu:
		getActionColor
		isLegalAttack

"""
def isInRange(attacker, attack, defender):
	atkMinRange = attack['range'][0]
	atkMaxRange = attack['range'][1]
	attackType = attack['range type']
	distanceBetweenSrcTgt = cardGetDistance(attacker, defender)

	if attackType == 'Melee' and getZoneContaining(attacker)==getZoneContaining(defender):
		return True
	elif attackType == 'Ranged' and atkMinRange <= distanceBetweenSrcTgt and distanceBetweenSrcTgt <= atkMaxRange:
		return True
	else:
		return False

#Called by attackChoicePrompt in attacks.py
def createAttackOptionsList(modifiedAttacks, killChances, effectChances):
	options = []
	append = options.append

	for i,attack in enumerate(modifiedAttacks):
		name = attack["name"]
		dice = attack["dice"]
		#Todo: add traits and effects
		killChance = "{}%".format(str(killChances[i]))

		append("{} ({})".format(name,dice).center(68,' ') + "\nChance to Kill: {}".format(killChance).center(68,' '))

	colors = ["#CC0000" for i in options] #Red
	choiceText = "Use which attack?" if options else "No legal attacks available!"
	return choiceText, options, colors

#Called by targetMenu() in main.py
def attackChoicePrompt(attacker,defender,actionFilters=["Quick","Full"]):
	"""
	Prompts the attacking player to select an attack. Assumes that there exists an attacker and a defender.
	If you want to restrict the types of attack that can be chosen, you can set permissible action types in actionFilters
	If you set the action filter to "None", it will only pick up attacks without an action type. Called from main.py (targetMenu())
	"""
	mute()
	debug("attackChoicePrompt\n({},\n{},\n{})\n".format(attacker.name,defender.name,str(actionFilters)))

	#1: Populate the attack list.
	def filterPredicate(attack): #For clarity
		return attack.get("action type","None") in actionFilters or "Counterstrike" in actionFilters and attack.get("Counterstrike")# Need to add "action type" to attack spells, change cAttacks to tAttacks
	attackList = [attack for attack in getAttacks(attacker) if filterPredicate(attack)]

	#2: Filter attackList by range
	attackList = [attack for attack in attackList if isInRange(attacker, attack, defender)]
	
	#3: Get a modified list of attacks for populating the menu. #WIP
	modifiedAttacks = [computeAttack(attacker,attack,defender) for attack in attackList]

	#4: Compute the kill chances for the modified attacks
	killChances = [chanceToKill(attacker,attack,defender) for attack in modifiedAttacks]

	#5: Compute Effect chances for the modified attacks
	effectChances = [chanceForEffect(attacker, attack, defender) for attack in modifiedAttacks]

	#6: Generate the list of choices that will appear on the menu
	choiceText, options, colors = createAttackOptionsList(modifiedAttacks, killChances, effectChances)
	
	#7: Display the menu to the player and allow them to choose an option
	choice = askChoice(choiceText, options, colors)

	#8: Initiate the chosen attack. Note that the attack will be pulled from the UNMODIFIED attack list.
	#WIP This should return the attackList[index] to the targetMenu() function that called it and let that one initialize that attack sequence
	if choice > 0:
		index = choice - 1
		return(attackList[index])
		#initializeAttackSequence(attacker,attackList[index],defender)


#WIP don't think we need this anymore
def diceRollMenu(attacker = None,defender = None,specialCase = None):
		mute()
		setEventList('Turn',[]) #Clear the turn event list. Will need to be changed when we implement sweeping/zone attacks properly
		aTraitDict = (computeTraits(attacker) if attacker else {})
		if aTraitDict.get("Incapacitated"):
				if specialCase!="Counterstrike": whisper("{} is incapacitated and cannot attack!".format(attacker.Nickname))
				return {}
		if attacker and (aTraitDict.get('Charge') or [1 for c in getAttachments(attacker) if (c.Name=="Lion Savagery" or c.Name=="Ballad of Courage") and c.isFaceUp and c.controller==attacker.controller]) and defender and getZoneContaining(attacker)==getZoneContaining(defender) and not specialCase and not hasAttackedThisTurn(attacker) and askChoice('Apply charge bonus to this attack?',['Yes','No'],["#01603e","#de2827"]) == 1: rememberCharge(attacker) #Let's try prompting for charge before opening menu, for a change.
		if not attacker: defender = None
		dTraitDict = (computeTraits(defender) if defender else {})
		attackList = getAttacks(attacker) if attacker else [{'Dice':i+1} for i in range(7)]
		choiceText = "Roll how many attack dice?"
		#Suppose there is an attacker with at least one attack:
		if aTraitDict:
				attackList = [computeAttack(attacker,attack,defender) for attack in attackList if attack.get('action type') != 'Damage Barrier']
				choiceText = "Use which attack?"
		if specialCase == 'Counterstrike':
				debug('Counterstrike found')
				for a in list(attackList):
						if a.get('Traits',{}).get('Counterstrike'): a['range type'] = 'Counterstrike'
						else: attackList.remove(a)
		choices = []
		for a in list(attackList):
				atkTraits = a.get('Traits',{})
				traits = getAttackTraitStr(atkTraits)
				expDam = str(round(expectedDamage(aTraitDict,a,dTraitDict),1)) if defender else ''
				killCh = str(round(chanceToKill(aTraitDict,a,dTraitDict)*100,1)) if defender else ''
				effectList = (['{} ({}%)'.format(e[1],
												str(round(getD12Probability(e[0],aTraitDict,a,dTraitDict)*100,1))) for e in a.get('d12',[])]
							  if a.get('d12') else '')
				choice = (("{} ({})".format(a.get('Name'),str(a.get('Dice',0))).center(68,' ') if a.get('Name') else str(a.get('Dice',0)).center(68,' '))+
						  ('\n{} Mana'.format(str(a.get('Cost',0))) if a.get('Cost') else '')+
						  ('\n'+', '.join(traits) if traits else '')+
						  ('\n'+', '.join(effectList) if effectList != '' else '')+
						  ('\nExpected damage: {} | Kill chance: {}%'.format(expDam,killCh) if (defender and a.get('EffectType','Attack')=='Attack') else ''))
				if specialCase == 'Counterstrike' and a.get('RangeType') != 'Counterstrike': continue
				if not attacker or isLegalAttack(aTraitDict,a,dTraitDict): choices.append(choice)
				else: attackList.remove(a)
		if defender and attacker and defender.Type in ['Creature','Conjuration','Conjuration-Wall']:
				choiceText = "Attacking {} with {}. Use which Attack?".format(defender.name,attacker.name)
		if specialCase == 'Counterstrike': choiceText = "{} can counterstrike! Use which attack?".format(attacker.name)
		colors = ([] if attacker else ['#E0B525']) + [getActionColor(attackList[i]) for i in range(len(choices))] + ['#666699','#000000']
		attackList = ([] if attacker else [{'Dice':0}]) + list(attackList)
		choices = ([] if attacker else ['Roll Effect Die']) + list(choices) + ['Other Dice Amount','Cancel Attack']
		if specialCase == 'Counterstrike' and not attackList: return {}
		count = (askChoice("No legal attacks detected!", ['Roll anyway','Cancel'], colors) if len(choices) == 2 else askChoice(choiceText, choices, colors))
		if count == 0 or count == len(choices): return {}
		elif count < len(choices)-1:
				return attackList[count-1]
		elif count == len(choices)-1:
				if attacker: return diceRollMenu()
				else: #Revert to standard input menu. Default value is the last one you entered.
						dice = min(askInteger("Roll how many Attack Dice?", getSetting('lastStandardDiceRollInput',8)),50) #max 50 dice rolled at once
						setSetting('lastStandardDiceRollInput',dice)
						return {'Dice' : dice}

#WIP used by diceRollMenu that will be obsolete
def getActionColor(action):
		if action.get('EffectType','Attack') == 'Heal': return "#663300"        #Heal is always in orange
		#Assume is an attack
		if action.get('Traits',{}).get('Spell'): return "#9900FF"         #Spell attacks are purple
		if action.get('RangeType') == 'Ranged': return '#0f3706'     #Nonspell ranged attacks are green
		return '#CC0000'                                                        #Default to red

#WIP used by diceRollMenu that will be obsolete
def isLegalAttack(aTraitDict,attack,dTraitDict):
		if not (aTraitDict.get('OwnerID') and dTraitDict.get('OwnerID')): return True
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})
		if attack["Name"] == "Arcane Zap" and "Wizard" in attacker.Name and timesHasOccured("Arcane Zap",attacker.controller): return False
		if (defender.name == "Tanglevine" or defender.name  == "Stranglevine") and attack.get('RangeType') != "Melee": return False
		if attacker.controller.Mana + attacker.markers[Mana] < attack.get('Cost',0): return False
		if attack.get('Type','NoType') in dTraitDict.get('Immunity',[]): return False
		aZone = getZoneContaining(attacker)
		if attack.get('Range'):
				if defender.Type == 'Conjuration-Wall':
						dZones = getZonesBordering(defender)
						inRange = False
						for z in dZones:
								distance = zoneGetDistance(aZone,z)
								if ((0 if (attack.get('RangeType')=='Ranged' and dTraitDict.get('Flying')) else attack.get('Range')[0])
									<= distance
									<= attack.get('Range')[1]): inRange = True
						if not inRange: return False
				else:
						dZone = getZoneContaining(defender)
						distance = zoneGetDistance(aZone,dZone)
						minRange = (0 if (attack.get('RangeType')=='Ranged' and dTraitDict.get('Flying')) else attack.get('Range')[0])
						if not (minRange <= distance <= attack.get('Range')[1]): return False
		if (dTraitDict.get('Flying') and
			not aTraitDict.get('Flying') and
			attack.get('RangeType') == 'Melee' and
			not atkTraits.get('Reach')): return False
		return True

############################################################################
######################		Attack Data Retrieval	####################
############################################################################
"""
Functions that retrieve and compute the entries of attack dictionaries.

---Code Structure---

getAttacks:
		computeAttack:
				getAdjustedDice
		getAttackTraitStr
		canDeclareAttack
"""

"""
New format for attack dictionary:
attack = {
	"name" : 			str,
	"dice" : 			int,
	"source id" : 		int,	(the card that supplies the attack)
	"user id" :			int,	(the card that is using the attack)
	"target id" :		int,	(the card being targeted by the attack)
	"damage type" :		str,
	"action type" :		str, {"quick", "full", "counterstrike", "damage barrier", "none"}
	"range type" :		str, {"ranged", "melee"}
	"effects" :			dict[int:list[str]],		(example: {8:[burn],11:[burn,burn]})
	"cost" :			int
	"range" :			tuple(int,int)

	"counterstrike" :	bool,
	"piercing +X" :		int,
	"mana drain +X" :	int,
	"charge +X" :		int,
	"vampiric" :		bool,
	etc.

	"bAS_[step name]" : fun,
	"aAS_[step name]" : fun,
}

we can store these properties in the xml files with the following notation (no spaces between fields):

<property name="cAttacks" value="
	name=Snapping Bite;
	action type=quick;
	range type=melee;
	dice=4;
	counterstrike=True;
	piercing +X=4;
	effects={5:['Burn'],8:['Burn','Burn']}
	range=(1,2)
	||
	name=Triple Bite;
	action type=full;
	range type=melee;
	dice=3;
	triplestrike=True
	effects=5:Daze,8:Push+Daze
" />

"""



def parseAttack(string):
	debug("parseAttack\n")
	"Takes a raw attack string for a single attack (in the format used in the new xml fields) and returns a properly formatted dictionary object"
	#Requires that string contain exactly 1 properly formatted attack
	#Does not store the information of the original source of the attack
	mute()
	typeMatcher = { #contains types for all non-string fields
		# --- Basic fields
		"dice" : int,
		"effects" : dict,
		"range" : tuple,
		# --- Traits
		"Counterstrike" : bool,
		"Piercing +X" : int,
		"Mana Drain +X" : int,
		"Mana Transfer +X" : int,
		"Charge +X": int,
		"Vampiric": bool,
		"Defrost": bool,
		"Ethereal": bool,
	}

	output = {}
	fields = string.split(";")
	for field in fields:
		debug('field: {}'.format(field))
		pair = field.split("=")
		if typeMatcher.get(pair[0],str) in [tuple,dict]:
			output[pair[0]] = typeMatcher.get(pair[0],str)(eval(pair[1]))
		else:
			output[pair[0]] = typeMatcher.get(pair[0],str)(pair[1])
	return output

def getAttacks(card):
	"""
	Returns a list containing the attacks of the argument card.
	This includes ALL attacks belonging to that card, including damage barriers.
	Attacks associated with the card itself (that the card can declare) will be stored in cAttacks
	Attacks that the card provides to its attachtarget will be stored in tAttacks
	Additionally, all cards in play will be queried for attacks that they provide.
	"""

	#Requires that card be a card that may legally declare an attack
	debug("getAttacks({})\n".format(card.Name))
	output = []
	append = output.append
	#1: parse attacks given in the card's cAttacks field
	if card.cAttacks:
		rawAttackList = card.cAttacks.split("||")
		for string in rawAttackList:
			debug("string in cAttacks: {}\n".format(string))
			attack = parseAttack(string)
			attack["user id"] = card._id
			attack["source id"] = card._id
			append(attack)
			debug("attack: " + str(attack)+"\n")
	#2: parse attacks from attached cards or Attack(Type) cards
	attackSources = getAttachments(card) + ([c for c in table if (c.controller==card.controller and c.Type == "Equipment" and c.isFaceUp) or (c.controller==card.controller and c.Type == "Attack")] if "Mage" in card.Subtype else [])
	for a in attackSources:
		if a.tAttacks:
			rawAttackList = a.tAttacks.split("||")
			for string in rawAttackList:
				debug("string in tAttacks: {}\n".format(string))
				attack = parseAttack(string)
				attack["user id"] = card._id
				attack["source id"] = a._id
				append(attack)
				debug("attack: " + str(attack)+"\n")
	#3: parse attacks from other sources
	"""Notation: 'on parse function' = oPF_getAttacks, which is assumed to contain only a function"""
	[spellDictionary[c.Name]["oPF_getAttacks"](c,card,output) for c in table if "oPF_getAttacks" in spellDictionary.get(c.Name,{})]
	debug("getAttacks output: {}\n".format(str(output)))
	return output

def addDiceToAttack(attacker, attack, defender):
	'''
	Returns an int with the amount of Dice to add to an attack based various modifiers in the attack from both attacker and defender
	Dice Add traits:
	Melee +
	Ranged +
	Bloodthirsty
	Charge
	Damage Type +
	Dice + (Tar Trap/Roll X additional dice if...)
	'''

	debug("addDiceToAttack\n")
	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)
	rangeType = attack['range type']
	diceToAdd = 0

	if rangeType == 'Melee' or rangeType == 'Counterstrike':
		#Melee +
		if aTraitDict.get(rangeType,0)>0:
			diceToAdd += aTraitDict.get(rangeType,0)
		#Bloodthirsty
		diceToAdd += aTraitDict.get('Bloodthirsty',0) if ((defender.markers[Damage] or ("Mage" in defender.Subtype and defender.controller.Damage))	and (attacker and not hasAttackedThisTurn(attacker)) and defender.type == 'Creature' and not dTraitDict.get('Nonliving')) else 0
		#Charge
		diceToAdd += aTraitDict.get('Charge',0) if hasCharged(attacker) else 0
		#Damage Type +
		try: diceToAdd += dTraitDict[attack['damage type']] if dTraitDict[attack['damage type']]>0 else 0
		except: diceToAdd += 0
		#Dice +
		'''WIP, need to add the extra dice sources. (Adding them top the list below as I think about them). Might need a case for each since they are not uniform or add a 
		trait that we can add to the xml file
		Shallow Sea
		Tar Trap
		Marked For Death
		Straywood Scout marker'''

	elif rangeType == 'Ranged':
		#Ranged +
		diceToAdd += aTraitDict.get(rangeType,0)
		#Damage Type +
		try: diceToAdd += dTraitDict[attack['damage type']] if dTraitDict[attack['damage type']]>0 else 0
		except: diceToAdd += 0
		#Dice +
		'''WIP, need to add the extra dice sources. (Adding them top the list below as I think about them). Might need a case for each since they are not uniform or add a 
		trait that we can add to the xml file
		Tar Trap
		Marked For Death
		Straywood Scout marker'''
	return diceToAdd

def subDiceFromAttack(attacker, attack, defender):
	'''
	Returns an int with the amount of Dice to remove from an attack based various modifiers in the attack from both attacker and defender
	Dice Subtract traits:
	Melee -
	Ranged -
	Weak
	Stagger
	Damage Type -
	Dice - (Agony)
	'''

	debug("subDiceFromAttack\n")
	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)
	rangeType = attack['range type']
	diceToSubtract = 0

	#WIP need to add logic for spell attacks too, but just getting regular attacks up and running for now
	if rangeType == 'Melee' or rangeType == 'Counterstrike':#Non-Spell melee/counterstrikes
		#Melee -
		if aTraitDict.get(rangeType,0)<0:
			diceToSubtract += abs(aTraitDict.get(rangeType,0))
		#Weak
		diceToSubtract += attacker.markers[Weak]
		#Stagger
		diceToSubtract += attacker.markers[Stagger]*2
		#Damage Type -
		try: diceToSubtract += abs(dTraitDict[attack['damage type']]) if dTraitDict[attack['damage type']]<0 else 0
		except: diceToSubtract +=0
		#Dice -
		'''WIP, need to add the extra dice sources. (Adding them top the list below as I think about them). Might need a case for each since they are not uniform or add a 
		trait that we can add to the xml file
		Shallow Sea
		Aegis'''
		
	elif rangeType == 'Ranged':#Ranged non-Spell attacks
		#Weak
		diceToSubtract += attacker.markers[Weak]
		#Stagger
		diceToSubtract += attacker.markers[Stagger]*2
		#Damage Type -
		try: diceToSubtract += abs(dTraitDict[attack['damage type']]) if dTraitDict[attack['damage type']]<0 else 0
		except: diceToSubtract +=0
		#Dice -
		'''WIP, need to add the extra dice sources. (Adding them top the list below as I think about them). Might need a case for each since they are not uniform or add a 
		trait that we can add to the xml file
		Aegis'''
	return diceToSubtract


def computeAttack(attacker,attack,defender):#WIP
	debug("computeAttack\n")
	#Returns a new dictionary object containing the modified form of the attack, taking all bonuses into account. Does NOT modify the original attack.
	attack = deepcopy(attack)

	#1: compute all buffs on the attacker and defender
	diceToAdd = addDiceToAttack(attacker, attack, defender)
	diceToSubtract = subDiceFromAttack(attacker, attack, defender)
	
	#2: modify output based on buffs computed in #1
	attack['dice'] += diceToAdd
	attack['dice'] -= diceToSubtract

	#3: take special abilities (from the spelldictionary) into account
	#WIP

	#4: normalize dice to 1 if negative
	attack["dice"] = max(attack["dice"],1)
	return attack

def computeD12(dTraitDict,d12Pair):#WIP
		defender = Card(dTraitDict.get('OwnerID'))
		effectText = d12Pair[1]
		effects = []
		if ' & ' in effectText: effects = effectText.split(' & ')
		elif '2 ' in effectText: effects = [effectText.strip('2 '),effectText.strip('2 ')]
		else: effects = [effectText]
		conditionTypes = {'Flame' : ['Burn'],
						  'Psychic' : ['Sleep'],
						  'Acid' : ['Corrode'],
						  'Poison' : ['Rot','Cripple','Tainted','Weak']}
		#First, make replacements for slamming unmovable creatures
		if dTraitDict.get('Unmovable'):
				for n,i in enumerate(effects):
						if i == 'Slam': effects[n] = 'Daze'
		#Then make removals
		for e in list(effects):
				illegalEffect = False

				for i in dTraitDict.get('Immunity',[]):
						if (e in conditionTypes.get(i,[])): illegalEffect = True
				if ((e=='Burn' and dTraitDict.get('Burnproof'))
					or (e in ['Snatch','Push'] and dTraitDict.get('Unmovable'))
					or (e == 'Bleed' and (dTraitDict.get('Nonliving') or 'Plant' in defender.Subtype))
					or (e in ['Bleed','Stuck','Stun','Daze','Cripple','Weak','Slam','Stagger'] and defender.Type != 'Creature')): illegalEffect = True #not sure about weak; can it affect conjurations?
				if illegalEffect: effects.remove(e)
		#Finally, replace corrode with damage if neccessary
		currentArmor = getStat(Card(dTraitDict['OwnerID']).Stats,'Armor') + dTraitDict.get("Armor",0)
		for n,i in enumerate(effects):
				if i == "Corrode":
						if currentArmor == 0: effects[n] = "Damage"
						else: currentArmor -= 1
		if not effects: return False
		if len(effects) == 1: return [d12Pair[0],effects[0]]
		if len(effects) == 2 and effects[0] == effects[1]: return [d12Pair[0],'2 '+effects[0]]
		else: return [d12Pair[0],'{} & {}'.format(effects[0],effects[1])]

def getAdjustedDice(aTraitDict,attack,dTraitDict):
		"""Decides how many dice should be rolled for attack based on the attacker (and the defender, if any)."""
		attackDice = attack.get('Dice',0)
		atkTraits = attack.get('Traits',{})
		attacker = (Card(aTraitDict['OwnerID']) if 'OwnerID' in aTraitDict else None)
		defender = (Card(dTraitDict['OwnerID']) if 'OwnerID' in dTraitDict else None)
		atkOS = Card(attack['source id'])
		if attacker and not "Autonomous" in atkOS.traits:
			if not hasAttackedThisTurn(attacker): #Once per attack sequence bonuses
				if (attack.get('RangeType') == 'Melee' or attack.get('RangeType') == 'Counterstrike') and not attack.get("Action") == "Trample": attackDice += aTraitDict.get('Melee',0) + (aTraitDict.get('Charge',0) if hasCharged(attacker) else 0)#Charge Bonus
				if attack.get('RangeType') == 'Ranged': attackDice += aTraitDict.get('Ranged',0)
			#No restriction on how many times may be applied
			if not atkTraits.get('Spell'):
				attackDice -= attacker.markers[Weak]
				attackDice -= attacker.markers[Stagger] * 2
				if (not "Aquatic" in atkOS.traits and "Shallow Sea" in aTraitDict):
					if not "Flying" in atkOS.traits:
						attackDice -=1 
					elif "Flying" in atkOS.traits and attack.get('RangeType') == "Melee" and not "Flying" in dTraitDict:
						attackDice -=1 
				if [True for c in getAttachments(attacker) if c.isFaceUp and c.Name == "Agony"]: attackDice -= 2
				if [True for c in getAttachments(attacker) if c.isFaceUp and c.Name == "Tangleroot"]: attackDice -= c.markers[DissipateToken]
				if [True for c in getAttachments(attacker) if c.isFaceUp and (c.Name == "Knight\'s Courage")] and defender.markers[Strongest]: 
						attackDice += 2 
						atkTraits['Piercing'] = atkTraits.get('Piercing',0) + 1
				if (attack["Name"] in ["Dragon-Tail Sweep", "Flying Side Kick"] or "Nunchucks" in aTraitDict) and attack.has_key("KiDice"):
					if attack["Name"] == 'Dragon-Tail Sweep':
						#debug("Attack Dice before: {}".format(attackDice))
						attackDice += 1
						#debug("Attack Dice after: {}".format(attackDice))
					elif attack["Name"] == "Flying Side Kick":
						attackDice += 2
					else:
						attackDice += 1
				if attacker.markers[FireGlyphActive]:
					attackDice +=2
				level = eval(attacker.Level)
				if Card(attack['source id']).name in listMageWeapons and "Mage" in attacker.Subtype and level >= 5: attackDice += 1
				if attacker.Name == "Lightning Raptor" and attacker.markers[Charge] > 1 : attackDice += attacker.markers[Charge]
				if [True for c in getAttachments(defender) if c.isFaceUp and c.Name == "Force Shield"] and attack.get('RangeType') == 'Melee': attackDice -= c.markers[DissipateToken]
		if defender:
				#Likely need to redo a lot of the exceptions based old stuff #WIP
				if 'Glancing' in dTraitDict and not attack.get("Traits",{}).get("Drain"): attackDice -= 3
				attackDice -= dTraitDict.get('Aegis',0)
				attackDice += (aTraitDict.get('Bloodthirsty',0) if ((defender.markers[Damage] or (defender.Subtype=="Mage" and defender.controller.Damage))
																	and (attacker and not hasAttackedThisTurn(attacker))
																	and defender.type == 'Creature'
																	and not dTraitDict.get('Nonliving')
																	and (attack.get("RangeType") == "Melee" or attack.get('RangeType') == 'Counterstrike')
																	and not attack.get("Action") == "Trample"
																	) else 0)
				attackDice += dTraitDict.get(attack.get('Type'),0) #Elemental weaknesses/resistances
				if [True for c in getAttachments(defender) if c.isFaceUp and c.name == "Marked for Death"]: #Marked for death
						eventList = getEventList('Round')
						if ((not [True for e in eventList if e[0] == 'Attack' and e[1][0] == attacker._id and e[1][1] == defender._id])
																	and attacker.type == 'Creature'
																	and (attacker and not hasAttackedThisRound(attacker))
																	and attack.get('RangeType') != 'Damage Barrier'):
								attackDice += 1
				vs = atkTraits.get('VS')
				if vs: #We'll assume each attack has only one vs+ trait
						if ((vs[0] == "Corporeal Conjurations" and 'Conjuration' in defender.Type and 'Corporeal' in dTraitDict) or
							(vs[0] == "Flying" and 'Flying' in dTraitDict) or
							(vs[0] == "Nonliving Creatures" and 'Creature'==defender.Type and 'Nonliving' in dTraitDict) or
							(vs[0] == "Nonliving and Dark creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or
							(vs[0] == "Nonliving or Dark Creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or #Curse AW's inconsistent formatting...
							(vs[0] == "Nonliving" and 'Nonliving' in dTraitDict) or
							(vs[0] == "Incorporeal" and "Incorporeal" in dTraitDict) or
							(vs[0] == "Undead" and "Undead" in defender.Subtype)): attackDice += vs[1]
				if attacker and attack.get('Name') == 'Thundergun' and attacker.Name == "Grimson Deadeye, Sniper": #Deadeye's ability
						aZone = getZoneContaining(attacker)
						dZone = getZoneContaining(defender)
						distance = zoneGetDistance(aZone,dZone)
						attackDice -= max((distance-1),0)
		if attackDice <= 0: attackDice = 1
		if atkTraits.get('No Damage'): attackDice = 0
		return attackDice

def getAttackTraitStr(atkTraitDict): ##Takes an attack trait dictionary and returns a clean, easy to read list of traits
		attackList = []
		for key in atkTraitDict:
				text = key
				if key in additiveTraits: text += ' +{}'.format(str(atkTraitDict[key]))
				if key in superlativeTraits: text += ' {}'.format(str(atkTraitDict[key]))
				if key == 'VS': text = ('+' if atkTraitDict[key][1]>=0 else '') + str(atkTraitDict[key][1]) + ' vs. ' + atkTraitDict[key][0]
				if atkTraitDict[key]: attackList.append(text)
		return attackList

def canDeclareAttack(card):#WIP called by isValidAttackSource from main.py
		if not card.isFaceUp: return False
		if (card.Type == 'Creature' or
			('Conjuration' in card.Type and card.AttackBar != '') or
			('Enchantment' in card.Type and card.AttackBar != '') or
			('Incantation' in card.Type and card.AttackBar != '') or
			(("Familiar" in card.Traits or "Spawnpoint" in card.Traits) and [True for c in [getBound(card)] if c and c.Type == "Attack"]) or
			computeTraits(card).get('Autonomous') or
			[1 for attack in getAttacks(card) if attack.get('RangeType')=='Damage Barrier'] != []): #Probably want better method for dealing with damage barriers.
				return True

############################################################################
######################		Dice Rolling		####################
############################################################################

'''def rollDice(dice):
	mute()
	global attackDiceBank
	global effectDieBank
	mapDict = eval(getGlobalVariable('Map'))
	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me: c.delete()

	dieCardX, dieCardY = mapDict.get('DiceBoxLocation',(0,0))
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
	dieCard.anchor = (True)
	rnd(0,0)
	diceFrom = ""
	count = dice
	if (len(attackDiceBank) < count): #attackDiceBank running low - fetch more
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
	#debug("Random.org response code for damage dice roll: {}".format(random_org[1]))
		if random_org[1]==200: # OK code received:
			attackDiceBank = random_org[0].splitlines()
			diceFrom = "from Random.org"
		else:
		#notify("www.random.org not responding (code:{}). Using built-in randomizer".format(random_org[1]))
			diceFrom = "from the native randomizer"
			while (len(attackDiceBank) < 20):
				attackDiceBank.append(rnd(0, 5))

	result = [0,0,0,0,0,0]
	for x in range(count):
		roll = int(attackDiceBank.pop())
		result[roll] += 1
	#debug("diceRoller result: {}".format(result))
	notify("{} rolls {} attack dice {}".format(me,count,diceFrom))

	damPiercing = result[4] + 2* result[5]
	damNormal = result[2] + 2* result[3]
	dieCard.markers[attackDie[0]] = result[0]+result[1] #blanks
	dieCard.markers[attackDie[2]] = result[2] #1
	dieCard.markers[attackDie[3]] = result[3] #2
	dieCard.markers[attackDie[4]] = result[4] #1*
	dieCard.markers[attackDie[5]] = result[5] #2*

	d12DiceCount = 1
	if (len(effectDieBank) < d12DiceCount): #diceBank running low - fetch more
		d12 = webRead("http://www.random.org/integers/?num=100&min=0&max=11&col=1&base=10&format=plain&rnd=new")
		#debug("Random.org response code for effect roll: {}".format(d12[1]))
		if d12[1]==200: # OK code received:
			effectDieBank = d12[0].splitlines()
			notify ("Using die from Random.org")
		else:
			notify ("Using die from the native randomizer")
			while (len(effectDieBank) < 100):
				effectDieBank.append(rnd(0, 11))

	effect = int(effectDieBank.pop()) + 1
	dieCard.markers[effectDie] = effect
	if getGlobalVariable("GameSetup") == "True":
		playSoundFX('Dice')
		time.sleep(1)
		notify("{} rolled {} normal damage, {} critical damage, and {} on the effect die".format(me,damNormal,damPiercing,effect))
		return (result,effect)'''

def rollDice(dice):
	mute()
	if dice == 0: attackRoll = [0,0,0,0,0,0]
	else: attackRoll = rollD6(dice)
	effectRoll = rollD12()
	displayRoll(attackRoll,effectRoll)
	return (attackRoll, effectRoll)

def displayRoll(attackRoll,effectRoll):
	mute()
	mapDict = eval(getGlobalVariable('Map'))
	for c in table:
			if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me: c.delete()
	dieCardX, dieCardY = mapDict.get('DiceBoxLocation',(0,0))
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field
	dieCard.anchor = (True)

	normalDamage = attackRoll[2] + 2* attackRoll[3] # calculate the results for Normal Damage
	criticalDamage = attackRoll[4] + 2* attackRoll[5] # calculate the results for Critical Damage

	#defines the markers that will be displayed in the RDA
	dieCard.markers[attackDie[0]] = attackRoll[0]+attackRoll[1] # Blank Dice
	dieCard.markers[attackDie[2]] = attackRoll[2] # display 1 Normal Damage
	dieCard.markers[attackDie[3]] = attackRoll[3] # display 2 Normal Damage
	dieCard.markers[attackDie[4]] = attackRoll[4] # display 1 Critical Damage
	dieCard.markers[attackDie[5]] = attackRoll[5] # display 2 Critical Damage
	dieCard.markers[effectDie] = effectRoll
	playSoundFX('Dice')
	time.sleep(1)
	notify("{} rolled {} Normal Damage, {} Critical Damage, and {} on the effect die\n".format(me, normalDamage, criticalDamage, effectRoll))

def rollD6(dice):
	mute()
	global attackDiceBank
	count = dice
	if (len(attackDiceBank) < count):
			attackDiceBank=list(rndArray(0,5,1000))
	attackRoll = [0,0,0,0,0,0]
	for x in range(count):
		roll = attackDiceBank.pop()
		attackRoll[roll] += 1
	#debug("Raw Attack Dice Roll results: {}".format(attackRoll))
	notify("{} rolls {} attack dice.\n".format(me,count))
	return attackRoll

def rollD12():
	mute()
	global effectDieBank
	if (len(effectDieBank)) <= 1:
			while (len(effectDieBank) < 50):
					effectDieBank.append(rnd(0,11))
	effectRoll = int(effectDieBank.pop()) + 1
	return effectRoll

def simpleRollDice(dice):
	"RollDice function which returns a plain number, rather than a list of values"
	values,effect = rollDice(dice)
	return values[2] + values[4] + 2 * (values[3] + values[5])
############################################################################
######################            Event Memory          ####################
############################################################################
"""
Events shall be formatted thus:

<A,cardID> attacks <B,cardID> with attack <C,attackDict> : [Attack,[A,B,C]]
<A,cardID> used defense <B,defenseDict> : [Defense, [A,B]]
<A,cardID> used charge: [Charge, [A]]
<A,cardID> uses ability number <B,int>: [Untargeted Ability, [A,B]]
"""


def getEventList(roundOrTurn):
		return (eval(getGlobalVariable("roundEventList")) if roundOrTurn =='Round' else eval(getGlobalVariable("turnEventList")))

def setEventList(roundOrTurn,eventList):
		if roundOrTurn =='Round': setGlobalVariable("roundEventList",str(eventList))
		else: setGlobalVariable("turnEventList",str(eventList))

def appendEventList(roundOrTurn,event):
		eventList = getEventList(roundOrTurn)
		eventList.append(event)
		setEventList(roundOrTurn,str(eventList))

def clearLocalTurnEventList(): #Clears the part of the turnList pertaining to the local player
		eventList = getEventList('Turn')
		for e in list(eventList):
				if (e[0] in ('Attack','Defense') and Card(e[1][0]).controller == me): eventList.remove(e)
		setEventList('Turn',eventList)

def hasAttackedThisTurn(card):
		eventList = getEventList('Turn')
		for e in eventList:
				if e[0] == 'Attack' and e[1][0] == card._id: return True

def hasAttackedThisRound(card):
		eventList = getEventList('Round')
		for e in eventList:
				if e[0] == 'Attack' and e[1][0] == card._id: return True

def timesHasUsedDefense(card,defenseDict):
		"""Counts how many times defense has been used this ROUND"""
		eventList = getEventList('Round')
		count = 0
		for e in eventList:
				if e[0] == 'Defense' and e[1][0] == card._id and e[1][1] == defenseDict: count += 1
		return count

def timesHasUsedAttack(card,attack):
		"""Counts how many times attack has been used this TURN"""
		eventList = getEventList('Turn')
		count = 0
		for e in eventList:
				if e[0] == 'Attack' and e[1][0] == card._id and e[1][2] == attack: count += 1
		return count

def timesHasUsedAbility(card,number=0):
		"""Counts how many times untargeted ability has been used this ROUND"""
		eventList = getEventList('Round')
		count = 0
		for e in eventList:
				if e[0] == 'Ability' and e[1][0] == card._id and e[1][1] == number: count += 1
		return count

def timesHasOccured(event,player=me):
		eventList = getEventList('Round')
		count = 0
		for e in eventList:
				if e[0] == 'Event' and e[1][0] == player._id: count += 1
		return count

def hasCharged(card):
		"""returns whether this card has charged this TURN"""
		eventList = getEventList('Turn')
		if ['Charge',[card._id]] in eventList: return True

def rememberDefenseUse(card,defense):
		appendEventList('Round',['Defense', [card._id,defense]])
		appendEventList('Turn',['Defense', [card._id,defense]])

def rememberAttackUse(attacker,defender,attack,damage=0):
		appendEventList('Round',['Attack', [attacker._id,defender._id,attack,damage]])
		appendEventList('Turn',['Attack', [attacker._id,defender._id,attack,damage]])

def rememberBattleMed(attacker,defender,Att = False,Def = False):
		appendEventList('Round',['Attack', [attacker._id,defender._id,Att,Def]])
		appendEventList('Turn',['Attack', [attacker._id,defender._id,Att,Def]])

def rememberCharge(attacker):
		appendEventList('Round',['Charge', [attacker._id]])
		appendEventList('Turn',['Charge', [attacker._id]])

def rememberAbilityUse(card,number=0): #We can call the targeted version 'rememberTargetAbility use', or some such. This one is for untargeted abilities
		appendEventList('Round',['Ability', [card._id,number]])
		appendEventList('Turn',['Ability', [card._id,number]])

def rememberPlayerEvent(event,player=me): #For misc. string events associated with a player. Useful for 'the first time per round...' effects.
		appendEventList('Round',['Event', [player._id,event]])
		appendEventList('Turn',['Event', [player._id,event]])


############################################################################
######################            Defenses              ####################
############################################################################
"""
Each defenseDict should have the following entries:
Source (id of the card that provides defense)
Minimum (e.g. 7+)
Uses (e.g. 1,2,inf)
Restrictions (e.g. melee only)
"""

def defenseParser(sourceID,rawDefenseStr):
		#For now, assume that the only restrictions are melee and ranged and that they are mutually exclusive
		defenseStr = str(rawDefenseStr).split('Defense')[1].strip('=') #Ugh...defenses are formatted inconsistendly in the XML files. But this should pick up both variants until we can standardize.
		defenseDict = {'Source' : sourceID}
		if 'No Melee' in rawDefenseStr:
				defenseDict['Restrictions'] = 'No Melee'
				defenseStr = (defenseStr.split('No Melee')[0]).strip(' ')
		elif 'No Ranged' in rawDefenseStr:
				defenseDict['Restrictions'] = 'No Ranged'
				defenseStr = (defenseStr.split('No Ranged')[0]).strip(' ')
		defTraitList = defenseStr.split(' ')
		for d in defTraitList:
				if '+' in d: defenseDict['Minimum'] = int(d.strip('+'))
				if 'x' in d: defenseDict['Uses'] = int(d.strip('x'))
				if d=='inf': defenseDict['Uses'] = 'inf'
		return defenseDict

def getDefenseList(aTraitDict,attack,dTraitDict):
		#For now, just find all defenses on the creature that have not been used completely.
		#Later, we'll be more selective, and will find defenses from other sources as well
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		statList = defender.Stats.split(', ')
		defenseList = []
		if not dTraitDict.get("Incapacitated"):
				for s in statList:
						if 'Defense' in s:
								#notify("Test: 5 s {}".format(s))
								dCandidate = defenseParser(defender._id,s)
								#notify("Test: 6 dCandidater {}".format(dCandidate))
								#Probably should actually separate so we first find the defenses, and iterate through them separately, but this will do for now.
								if dCandidate.get('Uses',0)=='inf' or timesHasUsedDefense(defender,dCandidate) < dCandidate.get('Uses',0):
										defenseList.append(dCandidate) #DO NOT modify the defense yet. We want to the history to see the original defense, not the modified one.
		for c in table:
				if (dTraitDict.get("Incapacitated") and not ("Autonomous" in c.Traits or c.Name in ["Force Orb","Force Sword"])): continue
				if c.Name=="Dancing Scimitar" and timesHasUsedAbility(c) > 0: continue #Dancing Scimitar's defense is only once per round.
				if c.isFaceUp and (getAttachTarget(c) == defender or (defender.Subtype == 'Mage' and c.type in ['Enchantment','Equipment'] and not getAttachTarget(c) and not c.Target == 'Zone' and (c.controller == defender.controller if c.type == "Equipment" else True)) and not c.markers[Disable]):
						rawText = c.text.split('\r\n[')
						traitsGranted = ([t.strip('[]') for t in rawText[1].split('] [') if (t.strip('[]')[0:8]=='Defense ' and t.strip('[]')[8]!='+')] if len(rawText) == 2 else [])
						if traitsGranted:
								for d in traitsGranted:
										dCandidate = defenseParser(c._id,d)
										#Runesmithing
										if c.markers[RuneofShielding]: dCandidate['Minimum'] = dCandidate['Minimum'] - 2
										if dCandidate.get('Uses',0)=='inf' or timesHasUsedDefense(defender,dCandidate) < dCandidate.get('Uses',0): defenseList.append(dCandidate)
		#Filter out unusable defenses
		for d in list(defenseList):
				if (d.get('Restrictions') == 'No Melee' and attack.get('RangeType') in ['Melee','Counterstrike'] or
					d.get('Restrictions') == 'No Ranged' and attack.get('RangeType') == 'Ranged' or
					(Card(d.get('Source')).name == 'Tarok, the Skyhunter' and
					 not (attacker.type == 'Creature' and
						  aTraitDict.get('Flying') and
						  attack.get('RangeType') in ['Melee','Counterstrike']))): defenseList.remove(d)
		#We should also search for enchantment pseudo-defenses, like block.
		return defenseList

def computeDefense(aTraitDict,attack,dTraitDict,defense):
		source = Card(defense.get("Source"))
		defender = Card(dTraitDict.get('OwnerID'))
		if "Autonomous" in source.Traits or source.Name in ["Force Orb","Force Sword"]: return dict(defense) #Autonomous equipment is not modified by anything
		modDefense = dict(defense)
		modDefense['Minimum'] = max(modDefense.get('Minimum',13)-dTraitDict.get('Defense',0),1)
		if (source.Name == "Dodge" and int(defender.level) <= 2): modDefense["Minimum"] = 1 #Note that dodge has 100% success rate for minors. This is super hacky, #WIP
		return modDefense

def defenseQuery(aTraitDict,attack,dTraitDict):
		"""Returns the defense if the attack was evaded and false if it was not"""
		#notify("Test: 1")
		defender = Card(dTraitDict.get('OwnerID'))
		#notify("Test: 2 defender {}".format(defender))
		atkTraits = attack.get('Traits',{})
		#notify("Test: 3a atkTraits {}".format(atkTraits))
		#notify("Test: 3b attack {}".format(attack))		
		#notify("Test: 3c dTraitDict {}".format(dTraitDict))
		defenseList = getDefenseList(aTraitDict,attack,dTraitDict)
		#notify("Test: 4 defenseList {}".format(defenseList))
		if atkTraits.get('Unavoidable') or not defenseList: return False
		modDefenseList = [computeDefense(aTraitDict,attack,dTraitDict,d) for d in defenseList]
		queryList = ['{}\nSuccess Rate {}% | Uses Remaining: {}'.format(Card(d.get('Source')).name.center(68,' '),
																	   str(round(((13-d.get('Minimum'))/12.0)*100,1)),
																	   ("Infinite" if d.get('Uses',0) == "inf" else
																		str(d.get('Uses',0) - timesHasUsedDefense(defender,d))))
					 for d in modDefenseList]
		colors = ["#996600" for d in queryList]
		queryList.append('I won\'t roll defense')
		colors.append("#000000")
		choice = askChoice('Would you like to use a defense?',queryList,colors)
		if choice == 0 or choice == len(queryList): return False
		defense = defenseList[choice-1]
		defSource = Card(defense.get('Source'))
		if defSource.Name == "Forcemaster": #Forcemaster's special defense
				if me.mana == 0:
						whisper("You cannot use that defense - you have no mana!")
						return False
				payManaChoice = askChoice("Pay 1 mana to use your innate defense?",["Yes","No"],["#01603e","#de2827"])
				if payManaChoice == 1:
						me.mana -= 1
						notify("{} pays 1 mana.".format(me))
				else: return False
		elif (defSource.Name == "Dodge" and int(defender.level) <= 2): #No need to roll dice if defender is minor for dodge
			rememberDefenseUse(defender,defense)
			notify("{} reflexively dodges the attack!\n".format(defender))
			return defense
		rememberDefenseUse(defender,defense)
		defense = computeDefense(aTraitDict,attack,dTraitDict,defense) #NOW we modify the defense
		notify("{} attempts to avoid the attack using {} {}!".format(defender.nickname,
																	pPos(defender),
																 	('innate defense' if defSource == defender else 'defense from {}'.format(defSource))))

		damageRoll,effectRoll = rollDice(0)
		if defense.get('Uses',0)>=1 and defSource.markers[Ready]: #Flip the defense marker
				defSource.markers[Ready]=0
				defSource.markers[Used]=1
		if defense.get('Uses',0)==2 and timesHasUsedDefense(defender,defense) >= 2 and defSource.markers[ReadyII]: #Flip the defenseII marker
				defSource.markers[ReadyII]=0
				defSource.markers[UsedII]=1
		if defSource.Name == "Forcemaster": #Flip forcemaster's deflect marker
				defSource.markers[DeflectR]=0
				defSource.markers[DeflectU]=1
		if defSource.Name == "Dancing Scimitar": #Note whether Dancing Scimitar has been used
				rememberAbilityUse(defSource) #Bookmark
		if effectRoll >= defense.get('Minimum',13):
			   notify("{} succeeds in {} defense attempt! Attack avoided!".format(defender.nickname,pPos(defender)))
			   return defense
		else:
			   notify("{} fails to defend {}...".format(defender.nickname,pRef(defender)))
			   return False

####################################
######### Old Functions area #######
####################################

"""
notation:

bAS - before Attack Step
aAS - after Attack Step

"""

"""
Since each attack step may be carried out by a different player, each step of the
attack should lead into the next.
"""

"""
argument will contain the following keys:

"identifier":	Should be "attack", identifying this argument as an attack for the purposes of event memory handling.
"sourceID":
"attackerID":
"defenderID":
"attack": 		The attack object
"hit":			Boolean indicating whether the attack has successfully hit
"damage": 		Amount of damage inflicted by the attack
"conditions":	Conditions inflicted by the attack
"strike":		The number of the current strike (e.g. the second strike would be 2)

"""


#old function, DELETE later when done referencing
'''def applyDamageAndEffects(aTraitDict,attack,dTraitDict,damage,rawEffect): #In general, need to adjust functions to accomodate partially or fully untargeted attacks.
		attacker = Card(aTraitDict.get('OwnerID',''))
		defender = Card(dTraitDict.get('OwnerID',''))
		atkTraits = attack.get('Traits',{})
		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		conditionsList = ['Bleed','Burn','Corrode','Cripple','Damage','Daze','Rot','Slam','Sleep','Stagger','Stuck','Stun','Tainted','Weak']
		effectsInflictDict = {'Damage' : "suffers 1 point of direct damage! (+1 Damage)",
							  'Bleed' : 'bleeds from its wounds! (+1 Bleed)',
							  'Burn' : 'is set ablaze! (+1 Burn)',
							  'Corrode' : 'corrodes! (+1 Corrode)',
							  'Cripple' : 'is crippled! (+1 Cripple)',
							  'Daze' : 'is dazed! (+1 Daze)',
							  'Rot' : 'rots! (+1 Rot)',
							  'Slam' : 'is slammed to the ground! (+1 Slam)',
							  'Sleep' : 'falls fast alseep! (+1 Sleep)',
							  'Stagger' : 'staggers about, not quite sure what is going on! (Minor Creatures can not Attack or Guard, Major Creatures -2 to All Attacks)',
							  'Stuck' : 'is stuck fast! (+1 Stuck)',
							  'Stun' : 'is stunned! (Stun)',
							  'Tainted' : "'s wounds fester! (+1 Tainted)",
							  'Weak' : 'is weakened! (+1 Weak)',
							  'Snatch' : 'is snatched toward {}! (Snatch)'.format(attacker),
							  'Push' : 'is pushed away from {}! (Push 1)'.format(attacker),
							  'Taunt' : 'wants to attack {}! (Taunt)'.format(attacker)}

		#Prep for Vampirism
		aDamage = getStatusDict(attacker).get('Damage',0)
		drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0)) if defender.Type == "Creature" else 0
		#if "Vine Marker" in defender.Name: drainableHealth = 0
		#else: drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0))

		if defender.Subtype == 'Mage': defender.controller.Damage += damage
		else: defender.markers[Damage] += damage
		notify("{} inflicts {} damage on {}{} average roll)".format(attacker,
																	str(damage),
																	defender,
																	('! (an above' if damage >= expectedDmg else '... (a below')))

		#Vine Markers are always destroyed from any amount of damage
		if "Vine Marker" in defender.name and damage >0:
			  notify("{} is smashed into the ground and destroyed.".format(defender))
			  defender.moveTo(me.piles['Discard'])
			  return #No sense going any further.

		#Bloodreaper health drain
		if attacker.markers[BloodReaper] and not timesHasOccured("Blood Reaper",attacker.controller) and defender.Type == "Creature" and dTraitDict.get("Living") and 'Demon' in attacker.Subtype and damage:
				mage = Card(aTraitDict.get('MageID'))
				healing = min(2,mage.controller.damage)
				if healing and not computeTraits(mage).get("Finite Life"):
						rememberPlayerEvent("Blood Reaper",attacker.controller)
						notify("{}'s health is restored by his Reaper's blood offering! (-{} Damage)".format(mage,str(healing)))
						remoteCall(mage.controller, "remotePlayerHeal", [healing])

		#Malakai's Fire
		if (attacker.Name=="Priest" and attack.get("Type")=="Light" and damage and "Conjuration" not in defender.Type and not timesHasOccured("Malakai's Fire",attacker.controller) and "Flame" not in dTraitDict.get("Immunity",[])):
				remoteCall(attacker.controller,"malakaisFirePrompt",[defender])

		#Mana Drain - Long term, will want a centralized function to adjust damage/mana of a card so we can take into account things like Mana Prism
		if defender.Type == 'Creature':
			dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if damage else 0)
			defender.controller.Mana -= dManaDrain
		else: dManaDrain = ""
		if dManaDrain: notify("{} drains {} mana from {}!".format(attacker,str(dManaDrain),defender.controller.nickname))
		#Vampirism
		if (atkTraits.get('Vampiric') and drainableHealth and
			(dTraitDict.get('Living') or not dTraitDict.get('Nonliving')) and defender.Type == 'Creature' > 0): #Long term, give all creatures Living trait by default, eliminate nonliving condition
				if attacker.controller == me: healingQuery(aTraitDict,
														   'Heal {} damage through vampirism?'.format(drainableHealth,defender.nickname),
														   drainableHealth,
														   "{} heals {} damage through vampirism!".format(attacker.nickname,'{}',defender.nickname))
				else: remoteCall(attacker.controller,'healingQuery',[aTraitDict,
																   'Heal {} damage through vampirism?'.format(drainableHealth,defender.nickname),
																   drainableHealth,
																   "{} heals {} damage through vampirism!".format(attacker.nickname,'{}',defender.nickname)])
		#Finally, apply conditions
		effects = ([rawEffect.split(' ')[1],rawEffect.split(' ')[1]] if '2' in rawEffect else rawEffect.split(' & ')) if rawEffect else []
		for e in effects:
				if e in conditionsList:
						if e=="Damage" and defender.Subtype == "Mage": defender.controller.damage += 1
						else: defender.markers[eval(e)]+=1
				notify('{} {}'.format(defender.nickname,effectsInflictDict.get(e,'is affected by {}!'.format(e))))'''

#Not currently called
'''
def damageReceiptMenu(aTraitDict,attack,dTraitDict,roll,effectRoll):
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})

		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		actualDmg,actualEffect = computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict)


		if defender.markers[VoltaricON] and actualDmg:#Voltaric Shield
				notify("The Voltaric Shield absorbs {} points of damage!".format(str(min(actualDmg,3))))
				actualDmg = max(actualDmg-3,0)
				defender.markers[VoltaricON] = 0
				defender.markers[VoltaricOFF] = 1
		if defender.type == "Creature" or defender.Subtype == "Mage": dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if actualDmg else 0) #Prep for mana drain
		else: dManaDrain = ""

		choice = askChoice('{}\'s attack will inflict {} damage {}on {}.{} Apply these results?'.format(attacker.nickame,
																										  actualDmg,
																										  ('and an effect ({}) '.format(actualEffect) if actualEffect else ''),
																										  defender.nickname,
																										  (' It will also drain {} mana from {}.'.format(
																												  str(dManaDrain),defender.controller.nickname) if dManaDrain else '')),
						   ['Yes',"Other Damage Amount",'No'],
						   ["#01603e","#FF6600","#de2827"])
		if choice == 1:
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg #for remembering damage. Pretty crude; We'll come up with a better alternative in Q2
		elif choice == 2:
				actualDmg = askInteger("Apply how much damage?",actualDmg)
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg
		else:
				notify('{} has elected not to apply auto-calculated battle results'.format(me))
				whisper('(Battle calculator not giving the right results? Report the bug to us so we can fix it!)')
'''


############################################################################
######################    Applying Damage and Effects   ####################
############################################################################
"""
Once an attack has been chosen, the code in this section determines what happens,
and prompts the recipient to accept the consequences.

---Code Structure---

damageReceiptMenu:
		applyDamageAndEffects
		revealAttachmentQuery
		computeRoll:
				computeEffect
healingQuery

"""
#Not being called currently. Delete
'''
def damageReceiptMenu(aTraitDict,attack,dTraitDict,roll,effectRoll):
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})
		#If it is healing, we heal and then end the attack, since it is not an attack.
		if False and attack.get('EffectType','Attack')=='Heal':
				healingAmt = min(sum([{0:0,1:0,2:1,3:2,4:1,5:2}.get(i,0)*roll[i] for i in range(len(roll))]),getStatusDict(defender).get('Damage',0))
				if healingAmt > 0: healingQuery(dTraitDict,
												'Heal {} for {} damage?'.format(defender.nickname,str(healingAmt)),
												healingAmt,
												"{} heals {} for {} damage!".format(attacker.nickname,defender.nickname,{}))
				else: notify("{} attempts to heal {} but fails.".format(attacker.nickname,defender.nickname))
				return 0 #Uh-oh...healing is treated as an attack for abilities that remember that. No worries; this will become irrelevant it Q2, and does not matter now.
		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		actualDmg,actualEffect = computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict)
		if defender.markers[VoltaricON] and actualDmg:#Voltaric Shield
				notify("The Voltaric Shield absorbs {} points of damage!".format(str(min(actualDmg,3))))
				actualDmg = max(actualDmg-3,0)
				defender.markers[VoltaricON] = 0
				defender.markers[VoltaricOFF] = 1
		if defender.type == "Creature" or defender.Subtype == "Mage": dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if actualDmg else 0) #Prep for mana drain
		else: dManaDrain = ""

		choice = askChoice('{}\'s attack will inflict {} damage {}on {}.{} Apply these results?'.format(attacker.nickame,
																										  actualDmg,
																										  ('and an effect ({}) '.format(actualEffect) if actualEffect else ''),
																										  defender.nickname,
																										  (' It will also drain {} mana from {}.'.format(
																												  str(dManaDrain),defender.controller.nickname) if dManaDrain else '')),
						   ['Yes',"Other Damage Amount",'No'],
						   ["#01603e","#FF6600","#de2827"])
		if choice == 1:
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg #for remembering damage. Pretty crude; We'll come up with a better alternative in Q2
		elif choice == 2:
				actualDmg = askInteger("Apply how much damage?",actualDmg)
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg
		else:
				notify('{} has elected not to apply auto-calculated battle results'.format(me))
				whisper('(Battle calculator not giving the right results? Report the bug to us so we can fix it!)')
'''


def remotePlayerHeal(amount):
		me.damage -= amount

def malakaisFirePrompt(heathen):
		mute()
		if me.mana >= 1 and askChoice("Smite the heathen with Malakai's Fire?",["Yes (1 mana)","No"],["#01603e","#de2827"])==1:
				me.mana -= 1
				notify("{} pays 1 mana to Smite the heathen {} with Malakai's Fire.".format(me,heathen))
				rememberPlayerEvent("Malakai's Fire")
				remoteCall(heathen.controller,"malakaisFireReceiptPrompt",[heathen])

def malakaisFireReceiptPrompt(heathen):
		mute()
		if askChoice("Malakai smites {}! Apply Burn condition?".format(heathen.Nickname),["Yes","No"],["#01603e","#de2827"])==1:
				heathen.markers[Burn]+=1
				bookOfMalakai=["...AND THE HEATHENS IN THEIR TREACHERY DOTH BURN LIKE CANDLES, SPAKE MALAKAI. AND LO, SO THEY DID BURN.\n- The book of Malakai, 16:3",
							   "...AND HE LIT A THOUSAND FIRES BENEATH THE FOUL. AND MALAKAI SAW THAT IT WAS JUST.\n- The book of Malakai, 19:25",
							   "...LET HE WHO JUDGETH WITH NO CAUSE BE JUDGED FIRST. AND THEN BURN HIM.\n-The book of Malakai, 4:22",
							   "...BEHOLD YE, FOR THIS IS THE FLAME OF RIGHTEOUSNESS. SEE THAT IT BURNETH EVERMORE IN YOUR HEART. AND ALSO IN THE HEARTS OF THE UNBELIEVERS, BUT IN A MORE LITERAL SENSE.\n-The book of Malakai, 5:18",
							   "...FOR I AM THE CANDLE IN THE DARK. THE FEAR IN THE EYES OF THE UNJUST. THE BANE OF THE IMPURE.\n-The book of Malakai, 8:9",
							   "...ALL WHO KNEEL BEFORE EVIL SHALL CLAIM THE FIRE OF WRATH AS THEIR REWARD. AS WILL THE EVIL THEMSELVES. REALLY, THOU SHOULDST NOT DISCRIMINATE IN ITS DISTRIBUTION.\n-The book of Malakai, 3:19",
							   "...AND MALAKAI GESTURED AT THE LADDINITES, AND LO! EACH BECAME A PILLAR OF FLAME, THEIR WICKEDNESS BURNING BRIGHTER THAN THE SUN.\n-The book of Malakai, 2:4",
							   "...AND MALAKAI DID SEE THAT THEY HAD VERILY REPENTED. AND PROCLAIMING THAT SOME CRIMES ARE FORGIVEN BUT THROUGH FLAME, HE SEARED THEIR WICKEDNESS FROM THEIR BONES.\n-The book of Malakai, 8:7",
							   "... AND I WILL STRIKE DOWN UPON THEE WITH GREAT VENGEANCE AND FURIOUS ANGER THOSE WHO ATTEMPT TO POISON AND DESTROY MY BROTHERS. AND YOU WILL KNOW MY NAME IS MALAKAI WHEN I LAY MY LIGHT UPON THEE \n-The book of Malakai, 25:17"]
				passage=rnd(0,len(bookOfMalakai)-1)
				notify(bookOfMalakai[passage])
				notify("{} is seared by the flames of righteousness! (+1 Burn)".format(heathen.Nickname))

def deathPrompt(cardTraitsDict,attack={},aTraitDict={}):
		card = Card(cardTraitsDict.get('OwnerID'))

		choice = askChoice("{} appears to be destoyed. Accept destruction?".format(card.nickname),
						   ["Yes","No"],
						   ["#01603e","#de2827"])
		if choice == 1:
				reusableAbilityTokens = [BloodReaper,
										 EternalServant,
										 HolyAvenger,
										 Pet]
				mage = Card(cardTraitsDict.get('MageID'))
				for t in reusableAbilityTokens:
						if card.markers[t]: mage.markers[t] = 1 #Return mage ability markers to their owner.
				if card.markers[WoundedPrey]:
						mages = [m for m in table if m.Name == "Johktari Beastmaster" and not m.markers[WoundedPrey]] #WARNING: This may identify the wrong JBM if there are more than 1 in the match. Unfortunately, markers cannot be associated with players, so it is difficult to correctly reassign the marker (not impossible, just not worth the effort)
						if mages:
								mage = mages[0]
								mage.markers[WoundedPrey] = 1
				deathMessage(cardTraitsDict,attack,aTraitDict)
				if ((attack.get('Traits',{}).get('Devour') and cardTraitsDict.get("Corporeal") and card.Type == 'Creature') or
					card.markers[Zombie]): obliterate(card)
				else: discard(card)
		else: notify("{} does not accept the destruction of {}.".format(me,card))

def computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict):
		defender = Card(dTraitDict["OwnerID"])
		armor = computeArmor(aTraitDict,attack,dTraitDict)
		atkTraits = attack.get('Traits',{})
		if dTraitDict.get('Incorporeal'): return (roll[2] + roll[4] + ((roll[3]+roll[5]) if atkTraits.get('Ethereal') else 0)),computeEffect(effectRoll,aTraitDict,attack,dTraitDict)
		normal = roll[2] + 2*roll[3]
		critical = roll[4] + 2*roll[5]
		if defender.Subtype == "Mage" and [1 for c in table if c.isFaceUp and c.Name == "Veteran's Belt" and c.controller == defender.controller]: #handle veteran's belt
				reduction = min(critical,2)
				critical -= reduction
				normal += reduction
		return (max((0 if (dTraitDict.get('Resilient') or atkTraits.get('Critical Damage')) else normal) - armor,0) +
				critical + (normal if atkTraits.get('Critical Damage') else 0),
				computeEffect(effectRoll,aTraitDict,attack,dTraitDict))

def computeEffect(effectRoll,aTraitDict,attack,dTraitDict):
		modRoll = effectRoll + dTraitDict.get('Tough',0) + dTraitDict.get(attack.get('Type'),0)
		defender = Card(dTraitDict['OwnerID'])
		attacker = Card(aTraitDict['OwnerID'])
		#Giant Wolf Spider's attack
		if attacker.Name == "Giant Wolf Spider" and attack.get("Name") == "Poison Fangs" and (dTraitDict.get("Restrained") or dTraitDict.get("Incapacitated")): modRoll += 4
		#Tidecaller's attack
		if (attacker.Name == "Shoalsdeep Tidecaller" and int(getGlobalVariable("PlayerWithIni")) == me._id) : modRoll += 4
		#Ki Effects
		if attack["Name"] in ["Projected Leg Sweep", "Dragon\'s Bite"] and attack.has_key("KiEffect"):
			modRoll += 6
		#Ring of Tides for a hydro attack from a Siren - Might be obsolete once cBuffs and stuff is implemented #WIP
		if attacker.Name == "Siren" and "Tides" in aTraitDict and ("Type" in attack.keys() and attack['Type']=="Hydro") and int(getGlobalVariable("PlayerWithIni")) == me._id : modRoll += 2
		#Elementalist's Air Glyph
		if attacker.markers[AirGlyphActive]:
			modRoll +=4
		if attacker.Name == "Temple of Light":
				eventList = getEventList("Round")
				for e in eventList:
						if "ToLX" in e[0]:
								modRoll += e[1]
		vs = attack.get('Traits',{}).get('VS')
		if vs: #We'll assume each attack has only one vs+ trait
						if ((vs[0] == "Corporeal Conjurations" and 'Conjuration' in defender.Type and 'Corporeal' in dTraitDict) or
							(vs[0] == "Flying" and 'Flying' in dTraitDict) or
							(vs[0] == "Nonliving Creatures" and 'Creature'==defender.Type and 'Nonliving' in dTraitDict) or
							(vs[0] == "Nonliving and Dark creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or
							(vs[0] == "Nonliving or Dark Creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or #Curse AW's inconsistent formatting...
							(vs[0] == "Nonliving" and 'Nonliving' in dTraitDict) or
							(vs[0] == "Incorporeal" and "Incorporeal" in dTraitDict) or
							(vs[0] == "Undead" and "Undead" in defender.Subtype)): modRoll += vs[1]
		debug('EffectRoll: {}, ModRoll: {}'.format(str(effectRoll),str(modRoll)))
		effects = attack.get('d12',[])
		if not effects or (dTraitDict.get('Incorporeal') and not attack.get('Traits',{}).get('Ethereal')): return None
		for effect in effects:
				rangeStr = effect[0]
				lowerBound, upperBound = 0,None
				if '-' in rangeStr: lowerBound,upperBound = int(rangeStr.split('-')[0]),int(rangeStr.split('-')[1])
				if '+' in rangeStr: lowerBound, upperBound = int(rangeStr.strip('+')),None
				if modRoll >= lowerBound and (modRoll <= upperBound if upperBound else True): return effect[1]
		return None

def healingQuery(traitDict,queryText,healingAmt,notifyText):
		card = (Card(traitDict.get('OwnerID')) if traitDict.get('OwnerID') else None)
		if not card or traitDict.get('Finite Life') or getRemainingLife(traitDict) == 0: return
		choice = askChoice(queryText,['Yes','No'],["#01603e","#de2827"])
		if choice == 1:
				healed = 0
				if card.Subtype == 'Mage':
						healed = min(card.controller.Damage,healingAmt)
						card.controller.Damage -= healed
				else:
						healed = min(card.markers[Damage],healingAmt)
						card.markers[Damage] -= healed
				notify(notifyText.format(str(healed)))



############################################################################
######################		Battle Predictions	####################
############################################################################

"""
Probability Distributions

The following functions return a dictionary of [normal,critical] damage pairs (as strings), correlated with the combinatorial frequency of each pair.
Due to the recursive nature of the computation, computing <dice> values in excess of 5 takes a noticeable amount of time.
However, this problem is solved by simply computing each dictionary before hand and then storing a list (or dictionary) of all
that are likely to be used. In other words, functions should not refer to comboDistr; we will simply run it to compute each dictionary.
"""

def comboDistr(dice):
	dieOutcomes = [[0,0],[1,0],[0,1],[2,0],[0,2]]
	distrDict = {'[0,0]': 1}
	for die in range(dice):
		outcomesList = [eval(key) for key in distrDict]
		outcomesList = list(set([str([d[0]+o[0],d[1]+o[1]]) for o in outcomesList for d in dieOutcomes]))
		outcomesList = [eval(L) for L in outcomesList]
		tempDict = {}
		for L in outcomesList:
			waysToGetL = 0
			for key in distrDict:
				k = eval(key)
				for o in dieOutcomes:
					if [k[0]+o[0],k[1]+o[1]] == L:
						waysToGetL += (2 if o == [0,0] else 1)*distrDict[key]
			tempDict[str(L)] = waysToGetL
		distrDict = tempDict
	return distrDict

def expectedDamage(aTraitDict,attack,dTraitDict):
		dice= attack.get('Dice',0)
		armor=computeArmor(aTraitDict,attack,dTraitDict)
		atkTraits = attack.get('Traits',{})
		if dice <= len(damageDict)-1 : distrDict = damageDict[dice]
		else: return
		if dTraitDict.get('Incorporeal'): return (float(dice) if atkTraits.get('Ethereal') else float(dice)/3)
		return sum([computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict)*distrDict[key] for key in distrDict])/float(6**dice)

def chanceToKill(attacker,attack,defender):
	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)
	dice = attack.get('Dice',0)
	armor = computeArmor(aTraitDict,attack,dTraitDict)
	defender = Card(dTraitDict['OwnerID'])
	life = getRemainingLife(dTraitDict)# if 'OwnerID' in dTraitDict else None))
	atkTraits = attack.get('Traits',{})
	if dice <= len(damageDict)-1 : distrDict = damageDict[dice]
	else: return
	if (dTraitDict.get('Incorporeal') and not atkTraits.get('Ethereal')): return (sum([nCr(dice,r)*(2**r)*(4**(dice-r)) for r in range(dice+1) if r >= life])/float(6**dice))
	return (sum([distrDict[key] for key in distrDict if computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict) >= life])/float(6**dice))

def chanceForEffect(attacker, attack, defender):
	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)
	effects = attack.get('effects')
	conditionTypes = {	'Flame' : ['Burn'],
						'Psychic' : ['Sleep'],
						'Acid' : ['Corrode'],
						'Poison' : ['Rot','Cripple','Tainted','Weak']}
	#WIP
	return

def computeAggregateDamage(normal,critical,aTraitDict,attack,dTraitDict):
		defender = Card(dTraitDict["OwnerID"])
		if defender.Subtype == "Mage" and [1 for c in table if c.isFaceUp and c.Name == "Veteran's Belt" and c.controller == defender.controller]: #handle veteran's belt in damage prediction
				reduction = min(critical,2)
				critical -= reduction
				normal += reduction
		armor = computeArmor(aTraitDict,attack,dTraitDict)
		atkTraits = attack.get('Traits',{})
		return (max((0 if (dTraitDict.get('Resilient') or atkTraits.get('Critical Damage')) else normal) - armor,0) +
				critical + (normal if atkTraits.get('Critical Damage') else 0))

def nCr(n,r):
	return factorial(n) / factorial(r) / factorial(n-r)

def getD12Probability(rangeStr,aTraitDict,attack,dTraitDict):# needs to be changed to take Tough/elemental into account
		d12Bonus = dTraitDict.get('Tough',0) + dTraitDict.get(attack.get('Type'),0)
		defender = Card(dTraitDict['OwnerID'])
		attacker = Card(aTraitDict['OwnerID'])
		#Giant Wolf Spider's attack
		if attacker.Name == "Giant Wolf Spider" and attack.get("Name") == "Poison Fangs" and dTraitDict.get("Restrained"): d12Bonus += 4
		if attacker.Name == "Temple of Light":
						  eventList = getEventList("Round")
						  for e in eventList:
							  if "ToLX" in e[0]:
								d12Bonus += e[1]
		vs = attack.get('Traits',{}).get('VS')
		if vs: #We'll assume each attack has only one vs+ trait
						if ((vs[0] == "Corporeal Conjurations" and 'Conjuration' in defender.Type and 'Corporeal' in dTraitDict) or
							(vs[0] == "Flying" and 'Flying' in dTraitDict) or
							(vs[0] == "Nonliving Creatures" and 'Creature'==defender.Type and 'Nonliving' in dTraitDict) or
							(vs[0] == "Nonliving and Dark creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or
							(vs[0] == "Nonliving or Dark Creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or #Curse AW's inconsistent formatting...
							(vs[0] == "Nonliving" and 'Nonliving' in dTraitDict) or
							(vs[0] == "Incorporeal" and "Incorporeal" in dTraitDict) or
							(vs[0] == "Undead" and "Undead" in defender.Subtype)): d12Bonus += vs[1]
		lowerBound, upperBound = 0,None
		if '-' in rangeStr: lowerBound,upperBound = int(rangeStr.split('-')[0]),int(rangeStr.split('-')[1])
		if '+' in rangeStr: lowerBound, upperBound = int(rangeStr.strip('+')),None
		lowerBound,upperBound = max(lowerBound - d12Bonus,0),(max(upperBound - d12Bonus,0) if upperBound else None)
		successIncidence = 0 if (upperBound == 0 or lowerBound > 12) else ((upperBound if (upperBound and upperBound<12) else 12) - lowerBound + 1)
		return min(successIncidence/float(12),float(1))

"""
Pre-Generated Data

Pre-generated damage frequency dictionaries should be stored below. Don't put anything else there; just data. This can be easily expanded
as needed by using comboDistr() and copypasting, though I can't imagine anybody needs more than a 10 dice calculation (what would you really
need to know besides *You're dead, ha ha ha*?)
"""
damageDict = {
	0 : {'[0,0]': 1},
	1 : {'[0, 1]': 1, '[2, 0]': 1, '[0, 2]': 1, '[0, 0]': 2, '[1, 0]': 1},
	2 : {'[1, 2]': 2, '[0, 4]': 1, '[0, 2]': 5, '[3, 0]': 2, '[2, 2]': 2, '[0, 3]': 2, '[1, 1]': 2, '[2, 0]': 5, '[2, 1]': 2, '[0, 1]': 4, '[4, 0]': 1, '[1, 0]': 4, '[0, 0]': 4},
	3 : {'[4, 2]': 3, '[6, 0]': 1, '[0, 0]': 8, '[4, 1]': 3, '[2, 3]': 6, '[1, 3]': 6, '[0, 3]': 13, '[5, 0]': 3, '[1, 1]': 12, '[0, 5]': 3, '[2, 1]': 15, '[4, 0]': 9, '[3, 2]': 6, '[3, 0]': 13, '[0, 1]': 12, '[3, 1]': 6, '[1, 2]': 15, '[0, 4]': 9, '[0, 2]': 18, '[2, 2]': 18, '[0, 6]': 1, '[2, 0]': 18, '[1, 0]': 12, '[2, 4]': 3, '[1, 4]': 3},
	4 : {'[4, 2]': 42, '[3, 3]': 24, '[6, 2]': 4, '[5, 0]': 28, '[8, 0]': 1, '[6, 0]': 14, '[5, 2]': 12, '[4, 3]': 12, '[0, 0]': 16, '[4, 1]': 36, '[2, 3]': 64, '[0, 8]': 1, '[1, 3]': 52, '[0, 3]': 56, '[0, 7]': 4, '[1, 1]': 48, '[0, 5]': 28, '[2, 1]': 72, '[1, 5]': 12, '[2, 5]': 12, '[4, 4]': 6, '[3, 1]': 52, '[7, 0]': 4, '[3, 2]': 64, '[3, 0]': 56, '[6, 1]': 4, '[0, 1]': 32, '[4, 0]': 49, '[1, 2]': 72, '[0, 4]': 49, '[0, 2]': 56, '[2, 2]': 102, '[5, 1]': 12, '[2, 6]': 4, '[2, 0]': 56, '[1, 0]': 32, '[2, 4]': 42, '[3, 4]': 12, '[1, 4]': 36, '[1, 6]': 4, '[0, 6]': 14},
	5 : {'[4, 2]': 335, '[3, 3]': 280, '[6, 2]': 80, '[5, 0]': 161, '[6, 4]': 10, '[8, 0]': 20, '[0, 9]': 5, '[6, 0]': 105, '[5, 3]': 60, '[8, 2]': 5, '[5, 2]': 170, '[4, 3]': 190, '[5, 1]': 140, '[10, 0]': 1, '[4, 1]': 245, '[2, 3]': 410, '[0, 8]': 20, '[1, 3]': 280, '[5, 4]': 30, '[1, 7]': 20, '[0, 7]': 50, '[1, 1]': 160, '[0, 5]': 161, '[2, 1]': 280, '[1, 5]': 140, '[2, 5]': 170, '[0, 0]': 32, '[3, 5]': 60, '[3, 1]': 280, '[4, 6]': 10, '[2, 7]': 20, '[8, 1]': 5, '[3, 2]': 410, '[2, 8]': 5, '[3, 0]': 200, '[1, 8]': 5, '[4, 4]': 120, '[6, 1]': 70, '[0, 10]': 1, '[6, 3]': 20, '[7, 0]': 50, '[7, 2]': 20, '[3, 4]': 190, '[0, 1]': 80, '[4, 0]': 210, '[1, 2]': 280, '[0, 4]': 210, '[0, 2]': 160, '[2, 2]': 460, '[0, 6]': 105, '[2, 6]': 80, '[0, 3]': 200, '[2, 0]': 160, '[1, 0]': 80, '[2, 4]': 335, '[4, 5]': 30, '[7, 1]': 20, '[1, 4]': 245, '[1, 6]': 70, '[9, 0]': 5, '[3, 6]': 20},
	6 : {'[4, 2]': 1995, '[3, 3]': 1940, '[6, 2]': 840, '[0, 11]': 6, '[6, 4]': 270, '[8, 0]': 195, '[0, 9]': 80, '[6, 0]': 581, '[5, 3]': 900, '[8, 4]': 15, '[8, 2]': 135, '[9, 0]': 80, '[5, 1]': 966, '[11, 0]': 6, '[10, 2]': 6, '[4, 8]': 15, '[4, 3]': 1650, '[2, 10]': 6, '[5, 6]': 60, '[0, 3]': 640, '[1, 9]': 30, '[9, 2]': 30, '[10, 0]': 27, '[4, 1]': 1260, '[2, 3]': 2040, '[6, 5]': 60, '[2, 9]': 30, '[7, 1]': 300, '[1, 3]': 1200, '[5, 4]': 600, '[1, 7]': 300, '[0, 7]': 366, '[1, 1]': 480, '[5, 2]': 1386, '[2, 1]': 960, '[5, 0]': 732, '[2, 5]': 1386, '[12, 0]': 1, '[0, 0]': 64, '[3, 5]': 900, '[9, 1]': 30, '[3, 1]': 1200, '[3, 7]': 120, '[6, 6]': 20, '[2, 7]': 360, '[10, 1]': 6, '[8, 1]': 120, '[3, 2]': 2040, '[2, 8]': 135, '[3, 0]': 640, '[1, 8]': 120, '[4, 4]': 1290, '[7, 3]': 120, '[0, 12]': 1, '[6, 1]': 630, '[0, 10]': 27, '[6, 3]': 440, '[7, 0]': 366, '[7, 2]': 360, '[3, 4]': 1650, '[7, 4]': 60, '[0, 1]': 192, '[0, 8]': 195, '[8, 3]': 30, '[3, 8]': 30, '[1, 2]': 960, '[0, 4]': 780, '[0, 2]': 432, '[2, 2]': 1800, '[0, 6]': 581, '[4, 6]': 270, '[2, 6]': 840, '[1, 5]': 966, '[2, 0]': 432, '[1, 0]': 192, '[2, 4]': 1995, '[4, 5]': 600, '[1, 10]': 6, '[1, 4]': 1260, '[1, 6]': 630, '[0, 5]': 732, '[4, 0]': 780, '[3, 6]': 440, '[4, 7]': 60, '[5, 5]': 180},
	7 : {'[4, 2]': 9870, '[3, 3]': 10360, '[0, 8]': 1337, '[6, 0]': 2674, '[8, 4]': 525, '[2, 10]': 210, '[0, 0]': 128, '[2, 3]': 8680, '[8, 0]': 1337, '[1, 3]': 4480, '[0, 7]': 2045, '[5, 2]': 8505, '[6, 8]': 35, '[9, 1]': 560, '[7, 5]': 420, '[0, 9]': 721, '[4, 3]': 10535, '[2, 8]': 1785, '[3, 5]': 7742, '[6, 1]': 4067, '[5, 8]': 105, '[8, 5]': 105, '[10, 3]': 42, '[0, 1]': 448, '[3, 1]': 4480, '[1, 2]': 3024, '[10, 4]': 21, '[5, 1]': 5124, '[2, 0]': 1120, '[9, 0]': 721, '[0, 14]': 1, '[6, 2]': 6272, '[1, 11]': 42, '[0, 13]': 7, '[8, 2]': 1785, '[4, 8]': 525, '[3, 0]': 1904, '[5, 4]': 6426, '[0, 5]': 2884, '[9, 3]': 210, '[1, 5]': 5124, '[12, 2]': 7, '[2, 5]': 8505, '[4, 0]': 2632, '[4, 1]': 5460, '[0, 12]': 35, '[6, 3]': 4900, '[7, 2]': 3612, '[1, 12]': 7, '[8, 3]': 875, '[3, 8]': 875, '[5, 3]': 7742, '[2, 2]': 6384, '[0, 6]': 2674, '[9, 2]': 665, '[1, 4]': 5460, '[3, 6]': 4900, '[2, 11]': 42, '[0, 11]': 119, '[6, 4]': 3710, '[7, 1]': 2562, '[11, 2]': 42, '[13, 0]': 7, '[10, 0]': 329, '[0, 3]': 1904, '[1, 7]': 2562, '[2, 9]': 665, '[4, 9]': 105, '[2, 12]': 7, '[12, 0]': 35, '[2, 7]': 3612, '[3, 7]': 2240, '[8, 1]': 1365, '[6, 5]': 1610, '[7, 3]': 2240, '[0, 10]': 329, '[1, 10]': 189, '[14, 0]': 1, '[8, 6]': 35, '[0, 4]': 2632, '[5, 5]': 3360, '[4, 6]': 3710, '[3, 9]': 210, '[2, 4]': 9870, '[1, 6]': 4067, '[3, 10]': 42, '[9, 4]': 105, '[4, 7]': 1470, '[1, 9]': 560, '[7, 0]': 2045, '[11, 0]': 119, '[10, 2]': 210, '[3, 2]': 8680, '[5, 7]': 420, '[4, 5]': 6426, '[5, 0]': 2884, '[1, 1]': 1344, '[2, 1]': 3024, '[4, 4]': 9870, '[6, 6]': 700, '[1, 8]': 1365, '[11, 1]': 42, '[4, 10]': 21, '[7, 6]': 140, '[5, 6]': 1610, '[10, 1]': 189, '[0, 2]': 1120, '[2, 6]': 6272, '[12, 1]': 7, '[1, 0]': 448, '[3, 4]': 10535, '[6, 7]': 140, '[7, 4]': 1470},
	8 : {'[4, 2]': 42896, '[3, 3]': 47040, '[0, 8]': 7393, '[6, 0]': 10864, '[7, 5]': 9520, '[5, 9]': 840, '[1, 13]': 56, '[0, 0]': 256, '[12, 4]': 28, '[2, 3]': 33152, '[8, 0]': 7393, '[1, 3]': 15232, '[3, 11]': 336, '[0, 7]': 9648, '[5, 2]': 43568, '[6, 8]': 1540, '[9, 1]': 5768, '[13, 1]': 56, '[6, 10]': 56, '[8, 4]': 8890, '[0, 15]': 8, '[0, 9]': 4824, '[4, 3]': 55440, '[2, 8]': 16156, '[3, 5]': 50008, '[6, 1]': 21392, '[8, 7]': 280, '[5, 8]': 3640, '[8, 5]': 3640, '[10, 3]': 1568, '[0, 1]': 1024, '[3, 1]': 15232, '[1, 2]': 8960, '[10, 4]': 924, '[5, 1]': 23072, '[2, 0]': 2816, '[6, 9]': 280, '[9, 0]': 4824, '[0, 14]': 44, '[6, 2]': 37660, '[2, 10]': 3388, '[2, 12]': 308, '[0, 13]': 168, '[8, 2]': 16156, '[4, 8]': 8890, '[5, 10]': 168, '[3, 0]': 5376, '[2, 4]': 42896, '[5, 4]': 49504, '[0, 5]': 10304, '[9, 3]': 4760, '[1, 5]': 23072, '[12, 2]': 308, '[2, 5]': 43568, '[10, 0]': 2716, '[4, 0]': 8288, '[4, 1]': 21056, '[10, 5]': 168, '[0, 12]': 518, '[6, 3]': 38416, '[7, 2]': 26608, '[1, 12]': 280, '[8, 3]': 12040, '[3, 8]': 12040, '[5, 3]': 50008, '[10, 6]': 56, '[2, 2]': 21056, '[0, 6]': 10864, '[9, 2]': 8008, '[1, 4]': 21056, '[8, 6]': 1540, '[3, 6]': 38416, '[2, 11]': 1120, '[0, 11]': 1288, '[6, 4]': 34888, '[7, 1]': 16360, '[11, 2]': 1120, '[14, 1]': 8, '[2, 14]': 8, '[13, 0]': 168, '[8, 8]': 70, '[0, 3]': 5376, '[1, 7]': 16360, '[15, 0]': 8, '[4, 9]': 3080, '[1, 11]': 952, '[12, 0]': 518, '[2, 7]': 26608, '[9, 5]': 840, '[3, 7]': 23296, '[7, 0]': 9648, '[6, 5]': 21616, '[7, 3]': 23296, '[0, 10]': 2716, '[2, 13]': 56, '[11, 3]': 336, '[7, 8]': 280, '[14, 0]': 44, '[4, 12]': 28, '[7, 7]': 1120, '[0, 4]': 8288, '[3, 12]': 56, '[5, 5]': 35056, '[4, 6]': 34888, '[3, 9]': 4760, '[16, 0]': 1, '[12, 3]': 56, '[11, 4]': 168, '[1, 6]': 21392, '[3, 10]': 1568, '[9, 4]': 3080, '[4, 7]': 18928, '[1, 9]': 5768, '[2, 9]': 8008, '[13, 2]': 56, '[11, 0]': 1288, '[10, 2]': 3388, '[3, 2]': 33152, '[4, 11]': 168, '[8, 1]': 10696, '[4, 5]': 49504, '[5, 0]': 10304, '[1, 1]': 3584, '[2, 1]': 8960, '[5, 7]': 9520, '[4, 4]': 60550, '[6, 6]': 12040, '[0, 16]': 1, '[1, 8]': 10696, '[11, 1]': 952, '[4, 10]': 924, '[7, 6]': 4480, '[5, 6]': 21616, '[1, 10]': 2632, '[14, 2]': 8, '[10, 1]': 2632, '[0, 2]': 2816, '[2, 6]': 37660, '[12, 1]': 280, '[1, 0]': 1024, '[3, 4]': 55440, '[1, 14]': 8, '[6, 7]': 4480, '[9, 6]': 280, '[7, 4]': 18928},
	9 : {'[4, 2]': 169344, '[3, 3]': 190848, '[0, 8]': 35298, '[6, 0]': 40320, '[7, 5]': 117936, '[5, 9]': 22680, '[2, 10]': 36288, '[7, 8]': 11340, '[5, 12]': 252, '[0, 0]': 512, '[9, 8]': 630, '[12, 4]': 1512, '[2, 3]': 116928, '[4, 14]': 36, '[8, 0]': 35298, '[1, 3]': 48384, '[3, 11]': 9072, '[0, 7]': 40464, '[5, 2]': 196560, '[6, 8]': 32130, '[9, 1]': 43416, '[13, 1]': 1512, '[6, 10]': 3024, '[8, 4]': 99792, '[0, 15]': 228, '[0, 9]': 26689, '[4, 3]': 255024, '[2, 8]': 114669, '[3, 5]': 269136, '[1, 2]': 25344, '[6, 1]': 97776, '[1, 14]': 396, '[8, 5]': 59346, '[14, 4]': 36, '[10, 3]': 25956, '[0, 1]': 2304, '[3, 1]': 48384, '[13, 4]': 252, '[10, 4]': 18774, '[18, 0]': 1, '[5, 1]': 92736, '[2, 0]': 6912, '[6, 9]': 10500, '[9, 0]': 26689, '[0, 14]': 774, '[17, 0]': 9, '[6, 2]': 194040, '[1, 13]': 1512, '[2, 12]': 5922, '[0, 13]': 2142, '[8, 2]': 114669, '[4, 8]': 99792, '[5, 10]': 7308, '[11, 6]': 504, '[4, 1]': 74592, '[2, 4]': 169344, '[5, 4]': 308574, '[3, 13]': 504, '[0, 5]': 34272, '[9, 3]': 58632, '[13, 0]': 2142, '[1, 5]': 92736, '[15, 2]': 72, '[12, 2]': 5922, '[2, 5]': 196560, '[8, 8]': 3780, '[15, 1]': 72, '[4, 0]': 24768, '[6, 12]': 84, '[3, 2]': 116928, '[3, 0]': 14592, '[10, 5]': 7308, '[0, 12]': 5040, '[6, 3]': 241332, '[7, 2]': 160452, '[2, 11]': 15876, '[8, 3]': 112644, '[5, 11]': 1512, '[3, 8]': 112644, '[13, 3]': 504, '[5, 3]': 269136, '[10, 6]': 3024, '[2, 2]': 65664, '[12, 5]': 252, '[0, 6]': 40320, '[9, 2]': 69372, '[1, 4]': 74592, '[6, 11]': 504, '[3, 6]': 241332, '[16, 2]': 9, '[1, 12]': 4662, '[0, 11]': 10116, '[6, 4]': 255906, '[7, 1]': 86832, '[11, 2]': 15876, '[5, 6]': 201096, '[14, 1]': 396, '[2, 14]': 432, '[4, 13]': 252, '[10, 0]': 17649, '[7, 6]': 71064, '[0, 3]': 14592, '[11, 5]': 1512, '[1, 7]': 86832, '[15, 0]': 228, '[4, 9]': 46746, '[1, 11]': 11592, '[7, 7]': 30240, '[12, 0]': 5040, '[2, 7]': 160452, '[16, 1]': 9, '[9, 5]': 22680, '[3, 7]': 177984, '[7, 0]': 40464, '[6, 5]': 201096, '[7, 3]': 177984, '[0, 10]': 17649, '[2, 13]': 1764, '[11, 3]': 9072, '[8, 9]': 630, '[14, 0]': 774, '[10, 7]': 504, '[4, 12]': 1512, '[8, 6]': 32130, '[0, 4]': 24768, '[3, 12]': 2604, '[5, 5]': 269136, '[4, 6]': 255906, '[3, 9]': 58632, '[9, 7]': 2520, '[16, 0]': 54, '[12, 3]': 2604, '[11, 4]': 5796, '[0, 18]': 1, '[1, 6]': 97776, '[10, 8]': 126, '[3, 10]': 25956, '[9, 4]': 46746, '[4, 7]': 172152, '[1, 9]': 43416, '[0, 17]': 9, '[2, 9]': 69372, '[13, 2]': 1764, '[11, 0]': 10116, '[10, 2]': 36288, '[14, 3]': 72, '[4, 11]': 5796, '[1, 15]': 72, '[8, 1]': 66537, '[2, 15]': 72, '[8, 10]': 126, '[3, 4]': 255024, '[2, 16]': 9, '[5, 0]': 34272, '[1, 1]': 9216, '[12, 6]': 84, '[2, 1]': 25344, '[7, 9]': 2520, '[5, 7]': 117936, '[4, 4]': 317772, '[6, 6]': 137088, '[0, 16]': 54, '[1, 8]': 66537, '[11, 1]': 11592, '[7, 10]': 504, '[4, 10]': 18774, '[8, 7]': 11340, '[1, 16]': 9, '[1, 10]': 24444, '[14, 2]': 432, '[10, 1]': 24444, '[0, 2]': 6912, '[3, 14]': 72, '[2, 6]': 194040, '[12, 1]': 4662, '[1, 0]': 2304, '[4, 5]': 308574, '[5, 8]': 59346, '[6, 7]': 71064, '[9, 6]': 10500, '[7, 4]': 172152},
	10 : {'[4, 2]': 620640, '[3, 3]': 712320, '[0, 8]': 151380, '[6, 0]': 139680, '[7, 5]': 1056240, '[10, 3]': 283920, '[5, 9]': 328020, '[0, 11]': 64570, '[14, 5]': 360, '[1, 13]': 21420, '[7, 8]': 215460, '[5, 12]': 13440, '[8, 11]': 1260, '[11, 7]': 5040, '[0, 0]': 1024, '[9, 8]': 29400, '[12, 4]': 36120, '[2, 3]': 387840, '[5, 8]': 650160, '[4, 14]': 2340, '[18, 1]': 10, '[1, 3]': 145920, '[15, 4]': 360, '[3, 11]': 130200, '[0, 7]': 155520, '[5, 2]': 806400, '[6, 8]': 431550, '[9, 1]': 266890, '[13, 1]': 21420, '[0, 20]': 1, '[6, 10]': 74760, '[8, 4]': 854955, '[2, 18]': 10, '[0, 15]': 3372, '[0, 9]': 129140, '[4, 3]': 1061760, '[2, 8]': 685665, '[3, 5]': 1273440, '[1, 2]': 69120, '[6, 1]': 403200, '[5, 14]': 360, '[1, 14]': 7740, '[8, 5]': 650160, '[14, 4]': 2340, '[7, 12]': 840, '[0, 1]': 5120, '[5, 13]': 2520, '[3, 1]': 145920, '[13, 4]': 10080, '[10, 4]': 246330, '[18, 0]': 65, '[5, 1]': 342720, '[2, 0]': 16640, '[12, 7]': 840, '[6, 9]': 193620, '[9, 0]': 129140, '[0, 14]': 8730, '[17, 0]': 300, '[6, 2]': 892080, '[2, 10]': 298710, '[9, 10]': 1260, '[2, 12]': 73710, '[0, 13]': 19440, '[3, 10]': 283920, '[8, 2]': 685665, '[4, 8]': 854955, '[5, 10]': 141372, '[11, 6]': 21840, '[18, 2]': 10, '[4, 15]': 360, '[2, 14]': 9720, '[4, 1]': 247680, '[2, 4]': 620640, '[5, 4]': 1655640, '[3, 13]': 15960, '[0, 5]': 107904, '[9, 3]': 520680, '[4, 13]': 10080, '[1, 5]': 342720, '[15, 2]': 2640, '[12, 2]': 73710, '[2, 5]': 806400, '[7, 9]': 79800, '[15, 1]': 2280, '[4, 0]': 71040, '[3, 16]': 90, '[6, 12]': 5460, '[16, 3]': 90, '[3, 2]': 387840, '[8, 0]': 151380, '[11, 4]': 102060, '[3, 0]': 38400, '[10, 5]': 141372, '[14, 6]': 120, '[0, 12]': 37845, '[19, 0]': 10, '[6, 3]': 1298640, '[7, 2]': 838800, '[2, 11]': 159120, '[8, 3]': 825810, '[9, 9]': 6300, '[3, 8]': 825810, '[4, 10]': 246330, '[5, 3]': 1273440, '[10, 6]': 74760, '[2, 2]': 195840, '[12, 5]': 13440, '[0, 6]': 139680, '[9, 2]': 483970, '[10, 10]': 252, '[15, 3]': 720, '[1, 4]': 247680, '[6, 11]': 21840, '[3, 6]': 1298640, '[16, 2]': 585, '[1, 12]': 50400, '[15, 0]': 3372, '[6, 4]': 1573530, '[7, 1]': 404640, '[12, 8]': 210, '[11, 2]': 159120, '[5, 6]': 1477140, '[14, 1]': 7740, '[1, 17]': 90, '[13, 0]': 19440, '[8, 8]': 94500, '[8, 12]': 210, '[7, 6]': 770400, '[3, 15]': 720, '[0, 3]': 38400, '[5, 11]': 47880, '[1, 7]': 404640, '[0, 19]': 10, '[4, 9]': 493440, '[1, 11]': 101160, '[7, 7]': 438480, '[12, 0]': 37845, '[2, 7]': 838800, '[6, 14]': 120, '[16, 1]': 540, '[9, 5]': 328020, '[3, 7]': 1113720, '[10, 9]': 1260, '[7, 0]': 155520, '[10, 0]': 97285, '[11, 5]': 47880, '[6, 5]': 1477140, '[7, 3]': 1113720, '[0, 10]': 97285, '[2, 13]': 28980, '[7, 11]': 5040, '[11, 3]': 130200, '[8, 9]': 29400, '[14, 0]': 8730, '[10, 7]': 25200, '[4, 12]': 36120, '[8, 6]': 431550, '[0, 4]': 71040, '[3, 12]': 50820, '[5, 5]': 1693692, '[4, 6]': 1573530, '[3, 9]': 520680, '[16, 0]': 1110, '[12, 3]': 50820, '[6, 13]': 840, '[0, 18]': 65, '[1, 6]': 403200, '[10, 8]': 8190, '[1, 18]': 10, '[9, 4]': 493440, '[4, 7]': 1247220, '[1, 9]': 266890, '[0, 17]': 300, '[10, 1]': 176490, '[2, 9]': 483970, '[4, 11]': 102060, '[11, 0]': 64570, '[10, 2]': 298710, '[14, 3]': 4080, '[13, 2]': 28980, '[16, 4]': 45, '[1, 15]': 2280, '[8, 1]': 352980, '[4, 16]': 45, '[13, 6]': 840, '[8, 10]': 8190, '[3, 4]': 1061760, '[2, 16]': 585, '[5, 0]': 107904, '[1, 1]': 23040, '[12, 6]': 5460, '[2, 1]': 69120, '[9, 7]': 79800, '[17, 2]': 90, '[5, 7]': 1056240, '[4, 4]': 1484280, '[20, 0]': 1, '[17, 1]': 90, '[6, 6]': 1188180, '[0, 16]': 1110, '[1, 8]': 352980, '[11, 1]': 101160, '[13, 5]': 2520, '[13, 3]': 15960, '[8, 7]': 215460, '[11, 8]': 1260, '[1, 16]': 540, '[1, 10]': 176490, '[14, 2]': 9720, '[7, 10]': 25200, '[0, 2]': 16640, '[3, 14]': 4080, '[2, 6]': 892080, '[12, 1]': 50400, '[1, 0]': 5120, '[4, 5]': 1655640, '[2, 17]': 90, '[6, 7]': 770400, '[2, 15]': 2640, '[9, 6]': 193620, '[7, 4]': 1247220}
	}
