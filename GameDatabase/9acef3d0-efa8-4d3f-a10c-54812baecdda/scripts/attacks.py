#######
#v2.0.0.0#
#######

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
				'Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic','Frost']
superlativeTraits = ["Regenerate",
					"Aegis",
					"Uproot",
					"Dissipate",
					"Ki",
					"Sai"
					"Nunchucks",
					"Melting"]

############################################################################
######################		Dice Roll Menu		####################
############################################################################
"""
The entire module is called through this function. All definitions of data should go through here.

---Code Structure---

diceRollMenu:
		getActionColor
		isLegalAttack

"""

def diceRollMenu(attacker = None,defender = None,specialCase = None):
		mute()
		setEventList('Turn',[]) #Clear the turn event list. Will need to be changed when we implement sweeping/zone attacks properly
		aTraitDict = (computeTraits(attacker) if attacker else {})
		if aTraitDict.get("Incapacitated"):
				if specialCase!="Counterstrike": whisper("{} is incapacitated and cannot attack!".format(attacker.name.split(',')[0]))
				return {}
		if attacker and (aTraitDict.get('Charge') or [1 for c in getAttachments(attacker) if (c.Name=="Lion Savagery" or c.Name=="Ballad of Courage") and c.isFaceUp and c.controller==attacker.controller]) and defender and getZoneContaining(attacker)==getZoneContaining(defender) and not specialCase and not hasAttackedThisTurn(attacker) and askChoice('Apply charge bonus to this attack?',['Yes','No'],["#01603e","#de2827"]) == 1: rememberCharge(attacker) #Let's try prompting for charge before opening menu, for a change.
		if not attacker: defender = None
		dTraitDict = (computeTraits(defender) if defender else {})
		attackList = getAttackList(attacker) if attacker else [{'Dice':i+1} for i in range(7)]
		choiceText = "Roll how many attack dice?"
		#Suppose there is an attacker with at least one attack:
		if aTraitDict:
				attackList = [computeAttack(aTraitDict,attack,dTraitDict) for attack in attackList if attack.get('RangeType') != 'Damage Barrier']
				choiceText = "Use which attack?"
		if specialCase == 'Counterstrike':
				for a in list(attackList):
						if a.get('Traits',{}).get('Counterstrike'): a['RangeType'] = 'Counterstrike'
						else: attackList.remove(a)
		choices = []
		for a in list(attackList):
				choice = formatAttackChoiceText(aTraitDict,a,dTraitDict)
				if specialCase == 'Counterstrike' and a.get('RangeType') != 'Counterstrike': continue
				if not attacker or isLegalAttack(aTraitDict,a,dTraitDict): choices.append(choice)
				else: attackList.remove(a)
		if specialCase == 'Counterstrike': 
				choiceText = "{} can counterstrike! Use which attack?".format(attacker.name)
		elif defender and attacker and defender.Type in ['Creature','Conjuration','Conjuration-Wall','Conjuration-Terrain']:
				choiceText = "Attacking {} with {}. Use which attack?".format(defender.name,attacker.name)
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

def formatAttackChoiceText(aTraitDict,attack,dTraitDict): # dict::trait -> dict::attack -> dict::trait -> str
	"Formats the text of input attack for display in the attack menu."
	# 1. Gather data
	trait_string = getAttackTraitStr(attack.get('Traits',{}))
	kill_chance = str(round(chanceToKill(aTraitDict,attack,dTraitDict)*100,1)) if dTraitDict else None
	effects = ['{} ({}%)'.format(e[1],str(round(getD12Probability(e[0],aTraitDict,attack,dTraitDict)*100,1))) for e in attack.get('d12',[])]
	# 2. Assemble components of attack string
	title = "{} ({})".format(attack.get("Name","Unnamed Attack"),str(attack.get('Dice',0))).center(68,' ')
	cost = '\n{} Mana'.format(str(attack.get('Cost',0))) if attack.get('Cost') else ""
	traits = ("\n" + ", ".join(trait_string)) if trait_string else ""
	effects = ("\n" + ", ".join(effects)) if effects else ""
	kill_chance = "\nKill chance: {}%".format(kill_chance) if (kill_chance and attack.get('EffectType','Attack')=='Attack') else ""
	# 3. Return formatted string
	return title+cost+traits+effects+kill_chance

def getActionColor(action):
		if action.get('EffectType','Attack') == 'Heal': return "#663300"        #Heal is always in orange
		#Assume is an attack
		if action.get('Traits',{}).get('Spell'): return "#9900FF"         #Spell attacks are purple
		if action.get('RangeType') == 'Ranged': return '#0f3706'     #Nonspell ranged attacks are green
		return '#CC0000'                                                        #Default to red

def isLegalAttack(aTraitDict,attack,dTraitDict):
		if not (aTraitDict.get('OwnerID') and dTraitDict.get('OwnerID')): return True
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkOS = Card(attack['OriginalSourceID'])
		atkTraits = attack.get('Traits',{})
		if defender.name == "V'Tar Orb Off": return True
		if not "Life" in defender.Stats: return False
		if attack["Name"] == "Arcane Zap" and ("Wizard" in attacker.Name or "Wizard - Playtest" in attacker.Name) and timesHasOccured("Arcane Zap",attacker.controller): return False
		# AOE attacks that don't affect attacker
		elif (attack["Name"] in
			["Blinding Flash", "Electrify", "Ring of Fire", "Quake Stomp", "Tornado"]
			and attacker == defender): return False
		if (defender.name == "Tanglevine" or defender.name  == "Stranglevine") and attack.get('RangeType') != "Melee": return False
		if attacker.controller.Mana + attacker.markers[Mana] < attack.get('Cost',0) - (sum([getCastDiscount(c,atkOS,defender)[0] for c in table]) if atkOS.Type == "Attack" else 0): return False
		if attack.get('Type','NoType') in dTraitDict.get('Immunity',[]): return False
		if 'Drain' in attack.get('Traits',{}) and 'Nonliving' in dTraitDict: return False
		aZone = getZoneContaining(attacker)
		if attack.get('Range'):
				if defender.Type == 'Conjuration-Wall':
						dZones = getZonesBordering(defender)
						inRange = False
						for z in dZones:
								distance = zoneGetDistance(aZone,z)
								if dTraitDict.get("Obscured") and distance > 1: return False #Obscured Check
								if ((0 if (attack.get('RangeType')=='Ranged' and dTraitDict.get('Flying')) else attack.get('Range')[0])
									<= distance
									<= attack.get('Range')[1]): inRange = True
						if not inRange: return False
				else:
						dZone = getZoneContaining(defender)
						distance = zoneGetDistance(aZone,dZone)
						if dTraitDict.get("Obscured") and distance > 1: return False #Obscured Check
						minRange = (0 if (attack.get('RangeType')=='Ranged' and ((dTraitDict.get('Flying') and not aTraitDict.get('Flying')) or (aTraitDict.get('Flying') and not dTraitDict.get('Flying')))) else attack.get('Range')[0])
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

getAttackList:
		computeAttack:
				getAdjustedDice
		getAttackTraitStr
		canDeclareAttack
"""

def getAttackList(card):
		"""This returns an unmodified list of the card's attacks. It must be modified by <computeAttack> independently."""
		if not card: return [] #Return an empty list if passed a blank argument
		if card.Name=="Dancing Scimitar" and timesHasUsedAbility(card) > 0: return []  #Dancing Scimitar's attack is only once per round.
		attackList = []
		if card.AttackBar != "":
				rawData = card.AttackBar
				#Split up the attacks:
				attackKeyList0 = [attack.split(':\r\n') for attack in card.AttackBar.split(']\r\n')]
				isAttackSpell = (card.Type == 'Attack')
				isDrainSpell = (card.Name in ["Drain Life", "Siphon Life"])
				#Trying to add healing
				isHealSpell = (card.Name in ["Heal"])
				#Split 'or' clauses into multiple attacks. CURRENTLY ASSUMES that every attack has at most one OR clause. (!!!)
				attackKeyList1 = []
				for attack in attackKeyList0:
						name = (card.Name if (isAttackSpell or isDrainSpell) else attack[0])
						attributes = (attack[0] if (isAttackSpell or isDrainSpell or isHealSpell) else attack[1]).split('] [')
						if (isAttackSpell or isDrainSpell or isHealSpell): attributes.append('Spell')
						if isDrainSpell: attributes.append('Drain')
						options = []
						tempAttributes = attributes
						for a in list(attributes):
								if ' OR ' in a:
										attributes.remove(a)
										options = a.split(' OR ')
						if options:
								for o in options:
										attackKeyList1.append([name,attributes+[o]])
						else:
								attackKeyList1.append([name,attributes])
				#Create attack dictionaries
				for attack in attackKeyList1:
						name = attack[0]
						attributes = attack[1]
						aDict = {'Name':name,
								'd12':[],
								'Traits': {},
								'EffectType': 'Attack',
								'SourceID': card._id,
								'OriginalSourceID': card._id
								#Later, when functionality is expanded to include non-attack effects, this will be modified
								}
						if (isAttackSpell or isDrainSpell):
								aDict['Range'] = [int(r) for r in card.Range.split('-')]
								aDict['Cost'] = int(card.Cost) if card.Cost != 'X' else 0
						#Now we extract the attributes
						effectSwitch = False
						if "Heal" in attributes: continue
						for attribute in attributes: #Heal is too much bother for now. It will be easier to do in Q2 #aDict['EffectType'] = 'Heal'
								attribute = attribute.strip('[]')
								if attribute in ['Quick','Full',"Trample"] : aDict['Action'] = attribute
								elif 'Ranged' in attribute:
										aDict['RangeType'] = attribute.split(':')[0]
										if not (isAttackSpell or isDrainSpell or isHealSpell): aDict['Range'] = [int(r) for r in attribute.split(':')[1].split('-')]
								elif 'Melee' in attribute:
										aDict['RangeType'] = 'Melee'
										aDict['Range'] = [0,0]
								elif attribute in ['Damage Barrier','Passage Attack'] : aDict['RangeType'] = attribute
								elif 'Cost' in attribute: aDict['Cost'] = (int(attribute.split('=')[1]) if attribute.split('=')[1] != 'X' else 0)
								elif 'Dice' in attribute:
										if attribute.split('=')[1] != 'X':
												aDict['Dice'] = int(attribute.split('=')[1])
										elif card.name == "Temple of Light" and card.controller == me:
												X = 0
												for c in table:
														if "Temple" in c.subtype and c.controller == me: X += 1
												X = min(me.mana,X) #Don't allow overspending
												askAmount = askInteger('Enter amount to pay for Temple of Lights attack (max: {})'.format(X),X)
												if askAmount == None or askAmount < 1: return [] #Allow player to cancel
												strength = min(askAmount,X) #Enforce maximum
												aDict['Dice'] = strength
												appendEventList('Round',['ToLX', strength])
												me.mana -= strength #Since maximum and mana supply are enforced,guaranteed to not be over limit
												notify("{} spends {} mana to power the Light Blast from the Temple of Light\n".format(me,str(strength)))
												toggleReady(card)
										else:
												aDict['Dice'] = 0

								elif attribute in ['Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic', 'Frost'] : aDict['Type'] = attribute
								elif attribute == 'd12' : effectSwitch = True
								elif effectSwitch:
										options = attribute.split('; ')
										aDict['d12'] = [o.split(' = ') for o in options]
										effectSwitch = False
								else:
										tPair = traitParser(attribute)
										if tPair[0] in additiveTraits: aDict['Traits'][tPair[0]] = aDict.get(tPair[0],0)+tPair[1]
										elif tPair[0] in superlativeTraits: aDict['Traits'][tPair[0]] = max(aDict.get(tPair[0],0),tPair[1])
										else: aDict['Traits'][tPair[0]] = tPair[1]
						aDict['OriginalAttack'] = deepcopy(aDict)
						if aDict.get('Dice')!=None: attackList.append(aDict) #For now, ignore abilities without a die roll. Maybe we can include them later...

		for c in table:
				if "Mage" in card.Subtype:
						if (c.Type in ['Equipment','Attack', 'Incantation'] and card.controller == c.controller and (c.isFaceUp or c.Type=='Attack' or c.Name in ["Drain Life", "Siphon Life", "Heal"]) and
							(getBindTarget(c) == card or (not canDeclareAttack(getBindTarget(c)) if getBindTarget(c) else True)) and
							not c.markers[Disable]): attackList.extend(getAttackList(c))
				if c.Type == 'Enchantment' and c.isFaceUp and getAttachTarget(c) == card and c.AttackBar: attackList.extend(getAttackList(c))

		if 'Familiar' in card.Traits or 'Spawnpoint' in card.Traits:
				for c in table:
						if (c.Type == 'Attack' and card.controller == c.controller and getBindTarget(c)==card): attackList.extend(getAttackList(c))
		for a in attackList:
				if a.get('RangeType')!='Damage Barrier':
						a['SourceID'] = card._id
						a['OriginalAttack']['SourceID'] = card._id
		return attackList

def computeAttack(aTraitDict,attack,dTraitDict):
		#debug("Compute Attack Function")
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		#debug("COMPUTE ATTACK\n")
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		KiDice = 0
		KiEffect = 0
		KiTrait = ""
		if "KiDice" in attack:
			#debug("KiDice: {}".format(str(attack["KiDice"])))
			KiDice = attack["KiDice"]
		if "KiEffect" in attack:
			KiEffect = attack["KiEffect"]
		if "KiTrait" in attack:
			KiTrait = attack["KiTrait"]

		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID')) if dTraitDict else None
		originalAttack = attack["OriginalAttack"]
		#debug("**** Right before deepcopy")
		attack = deepcopy(attack["OriginalAttack"])
		attack["OriginalAttack"] = originalAttack
		#debug("**** Right after deepcopy")
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		if KiDice !=0:
			attack["KiDice"] = KiDice	
		if "KiEffect" != 0:
			attack["KiEffect"] = KiEffect
		if "KiTrait" != "":
			if "Piercing" in KiTrait:
				temp = KiTrait.split('+')
				attack["Traits"][temp[0]]=int(temp[1])
				attack["KiTrait"] = KiTrait
			else:
				attack["Traits"][KiTrait] = True
				attack["KiTrait"] = KiTrait
		#debug("Attack Traits POST DEEPCOPY: {}\n".format(str(attack["Traits"])))	
		atkTraits = attack["Traits"]
		localADict = dict(aTraitDict)
		
		#Runesmithing
		atkOS = Card(attack['OriginalSourceID'])
		if atkOS.markers[RuneofPrecision] and atkOS.type == 'Equipment' and not atkTraits.get('Spell'): atkTraits['Piercing'] = atkTraits.get('Piercing',0) + 1
		#Holy Avenger
		if attacker.markers[HolyAvenger] and 'Holy' in attacker.School and not 'Legendary' in aTraitDict and not hasAttackedThisRound(attacker): #Holy avenger code
				eventList = getEventList('Round')
				for e in eventList:
						if e[0] == 'Attack' and e[1][0] == dTraitDict.get('OwnerID') and e[1][3] > 0:
								#This is to prevent gaining the HA benefit against conjurations or walls
								conjCheck = Card(e[1][0]).Type
								if "Conjuration" not in conjCheck:
									victim = Card(e[1][1]) if e[1][1] else None
								else: 
									victim = None
								if victim and victim.controller==attacker.controller and (victim.Type == 'Creature' or ('Conjuration' in victim.Type and 'Holy' in victim.School)) and victim != attacker:
										localADict['Melee'] = localADict.get('Melee',0) + 2
										localADict['Piercing'] = localADict.get('Piercing',0) + 1
										break
		#Kajarah
		if attack["Name"] == "Serrated Edge" and not hasAttackedThisRound(attacker): 
				debug("Serrated Edge Detected")
				eventList = getEventList('Round')
				for e in eventList:
						if e[0] == 'Attack' and Card(e[1][1]) == Card(dTraitDict.get('OwnerID')) and 'Animal' in Card(e[1][0]).Subtype and Card(e[1][0]).controller == attacker.controller and e[1][3] > 0:
								debug('dice added to attack')
								localADict['Ranged'] = localADict.get('Ranged',0) + 1
								break
		#BM Conditional Ranged +1
		if attacker.Name == "Johktari Beastmaster" and not atkTraits.get("Spell"): localADict['Ranged'] = localADict.get('Ranged',0) + 1
		#Ring of tides for Siren
		if attacker.name == 'Siren' and localADict.get("Tides") and ("Type" in attack.keys() and attack['Type']=="Hydro"): attack['Dice'] += 1
		#Wildfire Imp Melee buff for attacking a Burning Object
		if attacker.Name == "Wildfire Imp" and defender.markers[Burn]: localADict['Melee'] = localADict.get('Melee',0) + 2
		#Hydro Homies
		if ("Wall of Fire" in defender.name or "Fire Elemental" in defender.name) and attack.get('Type') == 'Hydro': attack['Traits']['Ethereal'] = True
		#Knight of the Red Helm attacking the Strongest (currently a token)
		if defender.markers[Strongest] and attacker.Name == "Knight of the Red Helm": localADict['Melee'] = localADict.get('Melee',0) + 2
		#Drokkar attacking Prey, currently works on anything with a grapple marker, not his specific prey
		if attacker.Name == "Drokkar" and attack["Name"] == "Tail Spike" and defender.markers[Grapple]: localADict['Melee'] = localADict.get('Melee',0) + 2
		#Lightning Raptor Counterstrike buff with 5 Charge tokens
		if attacker.Name == "Lightning Raptor" and attacker.markers[Charge] == 5: attack['Traits']['Counterstrike'] = True
		#Bloodfire Helmet Demon buff
		if attacker.Subtype == "Demon" and [1 for c in table if c.Name=="Bloodfire Helmet" and c.isFaceUp and c.controller == attacker.controller] and defender.markers[Burn]: localADict['Melee'] = localADict.get('Melee',0) + 1
		#Wounded prey
		if defender and defender.markers[WoundedPrey] and defender.Type == 'Creature' and defender.Subtype != 'Mage' and (attacker.controller != defender.controller or (attacker.controller == defender.controller and card.special == "Scenario")) and ("Mage" in attacker.Subtype or (attacker.Type == "Creature" and "Animal" in attacker.Subtype)) and defender.markers[Damage] and dTraitDict.get('Living'): localADict['Melee'] = localADict.get('Melee',0) + 1
		#()()()()This has an issue where the JBM's own creature attacks the JBM with the marker on her. It's a super corner case, but will need fixed sometime
		#Straywood Scout Token
		if defender and defender.markers[scoutToken] and not "Straywood Scout" in defender.name:
			localADict['Melee'] = localADict.get('Melee',0) + 1
			localADict['Ranged'] = localADict.get('Ranged',0) + 1
		if defender and defender.markers[AegisToken]: attack['Dice'] -= defender.markers[AegisToken]
		#if defender and defender.markers[WoundedPrey] and defender.Type == 'Creature' and attacker.controller != defender.controller and ("Mage" in attacker.Subtype or (attacker.Type == "Creature" and "Animal" in attacker.Subtype)) and defender.markers[Damage] and dTraitDict.get('Living'): localADict['Melee'] = localADict.get('Melee',0) + 1
		attack['Traits']['Piercing'] = atkTraits.get('Piercing',0) + localADict.get('Piercing',0)#Need to fix attack traitDict so it has same format as creature traitDict
		if localADict.get('Unavoidable'): attack['Traits']['Unavoidable'] = True
		if attack.get('RangeType') == 'Melee':
				if localADict.get('Vampiric'): attack['Traits']['Vampiric'] = True
				if attack.get('Action') == 'Quick' and localADict.get('Counterstrike'): attack['Traits']['Counterstrike'] = True
		for c in table:
				cName = c.name
				if (cName == "Critical Strike"
					and attacker == getAttachTarget(c)
					and not hasAttackedThisTurn(attacker)
					and attack.get('RangeType') in ["Melee","Counterstrike"]): #Making the big assumption that the attacker did not earlier make a ranged attack if this one is melee; I know it overlooks some cases, but it should hold up until Q2, I think.
						attack['Traits']['Piercing'] += 3
				elif (cName == "Badger Frenzy"
					and attacker == getAttachTarget(c)
					and attack.get('RangeType') in ["Melee","Counterstrike"]
					and attack.get("Action") == "Quick"):
						attack['Traits']['Doublestrike'] = True
				elif (cName == "Lion Savagery"
					and attacker == getAttachTarget(c)
					and attack.get('RangeType') in ["Melee","Counterstrike"]): #Making the big assumption that the attacker did not earlier make a ranged attack if this one is melee; I know it overlooks some cases, but it should hold up until Q2, I think.
						attack['Traits']['Piercing'] += 1
				elif (cName == 'Tooth & Nail' and #Global effects
					'Animal' in attacker.Subtype and
					attack.get('RangeType') in ['Melee','Counterstrike']): attack['Traits']['Piercing'] += 1
				elif c.controller == attacker.controller: #Friendly effects
						aType = attack.get('Type')
						if ( "Mage" in attacker.Subtype and
							((cName == 'Dawnbreaker Ring' and aType == 'Light') or
							(cName == 'Fireshaper Ring' and aType == 'Flame') or
							(cName == 'Lightning Ring' and aType == 'Lightning'))):
							localADict['Melee'] = localADict.get('Melee',0) + 1
							localADict['Ranged'] = localADict.get('Ranged',0) + 1
		#Force Armor
		if "Forcemaster" in defender.Name and atkTraits.get("Piercing"): 
			if atkTraits['Piercing'] >1:
				atkTraits['Piercing'] = atkTraits['Piercing'] - 2
			else:
				atkTraits['Piercing'] = 0
		attack['Dice'] = getAdjustedDice(localADict,attack,dTraitDict)
		#debug('attack[\'Dice\'] : {}'.format(str(attack['Dice'])))
		if dTraitDict.get('OwnerID'): attack['d12'] = [computeD12(dTraitDict,entry) for entry in attack.get('d12',[]) if computeD12(dTraitDict,entry)]
		return attack #If attack has zone attack trait, then it gains unavoidable

def computeD12(dTraitDict,d12Pair):
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
		#debug("****getAdjustedDice")
		attackDice = attack.get('Dice',0)
		#debug("Attack Dice upon entry: {}".format(attackDice))
		atkTraits = attack.get('Traits',{})
		#debug("atkTraits : {}".format(atkTraits))
		attacker = (Card(aTraitDict['OwnerID']) if 'OwnerID' in aTraitDict else None)
		defender = (Card(dTraitDict['OwnerID']) if 'OwnerID' in dTraitDict else None)
		atkOS = Card(attack['OriginalSourceID'])

		if attacker and not "Autonomous" in atkOS.traits:
				if not hasAttackedThisTurn(attacker): #Once per attack sequence bonuses
						if (attack.get('RangeType') == 'Melee' or attack.get('RangeType') == 'Counterstrike') and not attack.get("Action") == "Trample": attackDice += aTraitDict.get('Melee',0) + (aTraitDict.get('Charge',0) if hasCharged(attacker) else 0)#Charge Bonus
						if attack.get('RangeType') == 'Ranged' and not (attack.get("Traits",{}).get("Zone Attack") or attack.get("Traits",{}).get("Drain")): attackDice += aTraitDict.get('Ranged',0)
				#No restriction on how many times may be applied
				if not atkTraits.get('Spell'):
						attackDice -= attacker.markers[Weak]
						attackDice -= attacker.markers[Stagger] * 2
						if attacker.markers[Freeze]:
							attackDice -=1
						if (not "Aquatic" in atkOS.traits and "Shallow Sea" in aTraitDict):
							if not "Flying" in atkOS.traits:
								attackDice -=1 
							elif "Flying" in atkOS.traits and attack.get('RangeType') == "Melee" and not "Flying" in dTraitDict:
								attackDice -=1 
						if [True for c in getAttachments(attacker) if c.isFaceUp and (c.Name == "Agony" or c.Name == "Shrink")]: attackDice -= 2
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
				if Card(attack['OriginalSourceID']).name in listMageWeapons and "Mage" in attacker.Subtype and level >= 5: attackDice += 1
				if attacker.Name == "Lightning Raptor" and attacker.markers[Charge] > 1 : attackDice += attacker.markers[Charge]
				if [True for c in getAttachments(defender) if c.isFaceUp and c.Name == "Force Shield"] and attack.get('RangeType') == 'Melee': attackDice -= c.markers[DissipateToken]
		if defender:
				if 'Glancing' in dTraitDict and not attack.get("Traits",{}).get("Drain"): attackDice -= 3
				#debug("dTraitDict: {}".format(dTraitDict))
				attackDice -= dTraitDict.get('Aegis',0)
				if dTraitDict.get('DampCloak') and attack.get('RangeType') == 'Ranged':
					attackDice -= 1
				attackDice += (aTraitDict.get('Bloodthirsty',0) if ((defender.markers[Damage] or ("Mage" in defender.Subtype and defender.controller.Damage))
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

def canDeclareAttack(card):
		if not card.isFaceUp: return False
		if (card.Type == 'Creature' or
			('Conjuration' in card.Type and card.AttackBar != '') or
			('Enchantment' in card.Type and card.AttackBar != '') or
			('Incantation' in card.Type and card.AttackBar != '') or
			(("Familiar" in card.Traits or "Spawnpoint" in card.Traits) and [True for c in [getBound(card)] if c and c.Type == "Attack"]) or
			computeTraits(card).get('Autonomous') or
			[1 for attack in getAttackList(card) if attack.get('RangeType')=='Damage Barrier'] != []): #Probably want better method for dealing with damage barriers.
				return True

############################################################################
######################		Dice Rolling		####################
############################################################################

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
			if c.model == "c752b2b7-3bc7-45db-90fc-9d27aa23f1a9" and c.controller == me: c.delete()
	dieCardX, dieCardY = mapDict.get('DiceBoxLocation',(0,0))
	dieCard = table.create("c752b2b7-3bc7-45db-90fc-9d27aa23f1a9", dieCardX, dieCardY) #dice field
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
								dCandidate = defenseParser(defender._id,s)
								#Probably should actually separate so we first find the defenses, and iterate through them separately, but this will do for now.
								if dCandidate.get('Uses',0)=='inf' or timesHasUsedDefense(defender,dCandidate) < dCandidate.get('Uses',0):
										defenseList.append(dCandidate) #DO NOT modify the defense yet. We want to the history to see the original defense, not the modified one.
		for c in table:
				if (dTraitDict.get("Incapacitated") and not ("Autonomous" in c.Traits or c.Name in ["Force Orb","Force Sword"])): continue
				if c.Name=="Dancing Scimitar" and timesHasUsedAbility(c) > 0: continue #Dancing Scimitar's defense is only once per round.
				if c.isFaceUp and (getAttachTarget(c) == defender or ("Mage" in defender.Subtype and c.type in ['Enchantment','Equipment'] and not getAttachTarget(c) and not c.Target == 'Zone' and (c.controller == defender.controller if c.type == "Equipment" else True)) and not c.markers[Disable]):
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
					not (attacker.Type == 'Creature' and
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
		if (source.Name == "Dodge" and int(defender.level) <= 2): modDefense["Minimum"] = 1 #Note that dodge has 100% success rate for minors
		return modDefense

def defenseQuery(aTraitDict,attack,dTraitDict):
		"""Returns the defense if the attack was evaded and false if it was not"""
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})
		defenseList = getDefenseList(aTraitDict,attack,dTraitDict)
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
		#debug("{}".format(defSource))
		#debug(str(defender.level))
		if defSource.Name == "Forcemaster": #Forcemaster's special defense
				if me.mana == 0:
						whisper("You cannot use that defense - you have no mana!")
						return False
				payManaChoice = askChoice("Pay 1 mana to use your innate defense?",["Yes","No"],["#01603e","#de2827"])
				if payManaChoice == 1:
						me.mana -= 1
						notify("{} pays 1 mana.\n".format(me))
				else: return False
		elif (defSource.Name == "Dodge" and int(defender.level) <= 2): #No need to roll dice if defender is minor for dodge
			rememberDefenseUse(defender,defense)
			notify("{} reflexively dodges the attack!\n".format(defender))
			return defense

		rememberDefenseUse(defender,defense)
		defense = computeDefense(aTraitDict,attack,dTraitDict,defense) #NOW we modify the defense
		notify("{} attempts to avoid the attack using {}!\n".format(defender,
																('its innate defense' if defSource == defender else 'its defense from {}'.format(defSource))))

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
				rememberAbilityUse(defSource)
		if (effectRoll >= defense.get('Minimum',13)):
			notify("{} succeeds in its defense attempt! Attack avoided!\n".format(defender))
			return defense
		else:
			notify("{} fails to defend itself...\n".format(defender))
			return False

############################################################################
######################      Seven Steps of an Attack    ####################
############################################################################
"""
Since each attack step may be carried out by a different player, each step of the
attack should lead into the next.
"""

def initializeAttackSequence(aTraitDict,attack,dTraitDict): #Here is the defender's chance to ignore the attack if they have disabled their battle calculator
	mute()
	#debug('Initializing Attack Sequence')
	attacker = Card(aTraitDict['OwnerID'])
	#debug('Attacker: {}'.format(attacker.name))
	defender = Card(dTraitDict['OwnerID'])
	#debug('Defender: {}'.format(defender.name))
	#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
	if getSetting("BattleCalculator",True):
		attack_traits = attack.get("Traits",{})
		#1. Check for interception on ranged single target attacks
		if attack.get("RangeType") == "Ranged" and not (attack_traits.get("Zone Attack") or attack_traits.get("Drain")):
			# Get list of valid interceptors
			guard_dicts = [computeTraits(c) for c in getCardsInZone(getZoneContaining(defender)) if c.markers[Guard] and c != defender and c.controller == defender.controller]
			interceptor_dicts = [d for d in guard_dicts if d.get("Intercept") and not ("Restrained" in d or "Incapacitated" in d) and isLegalAttack(aTraitDict,attack,d)]
			if interceptor_dicts:
				# Ask player which, if any, of the interceptors they would like to act
				menu_text = "{} is being targeted by {}'s {}. Would you like to intercept the attack?".format(defender.Name,attacker.Name,attack.get("Name"))
				to_text = lambda x: "Intercept with {}".format(Card(x["OwnerID"]).Name) if x else "Don't intercept"
				to_color = lambda x: "#009933" if x else "#ff0000"
				choice = listQuery(menu_text,interceptor_dicts,to_text,to_color)
				if choice:
					notify("{} leaps in front of {} to intercept the attack!\n".format(Card(choice["OwnerID"]),defender))
					dTraitDict = choice
					defender = Card(choice["OwnerID"])
			#choice_options = ["Intercept with {}".format(Card(d["OwnerID"]).Name) for d in interceptor_dicts] + ["Don't intercept"]
				#choice_colors = ["#009933" for d in interceptor_dicts] + ["#ff0000"]
				#choice = askChoice(choice_text,choice_options,choice_colors)
				#if 1 <= choice <= len(interceptor_dicts):
					# Switch target to selected interceptor
					#iTraitDict = interceptor_dicts[choice-1]
					#interceptor = Card(iTraitDict['OwnerID'])
					#notify("{} leaps in front of {} to intercept the attack!".format(interceptor,defender))
					#dTraitDict = iTraitDict
					#defender = interceptor
					#defender.markers[Guard] = 0 #We should eventually change this so that it auto-removes guard. However, we cannot do this here as it would get rid of guard bonuses such as the Gargoyle sentry. The token must be removed upon completion of the attack.

		#2. Handle Zone attacks
		if attack_traits.get("Zone Attack"):
			targetList = [computeTraits(c) for c in getCardsInZone(getZoneContaining(defender))]
			targetList = [t for t in targetList if isLegalAttack(aTraitDict,attack,t)]
			for target in targetList:
				remoteCall(attacker.controller,'declareAttackStep',[aTraitDict,attack,target])
		else: remoteCall(attacker.controller,'declareAttackStep',[aTraitDict,attack,dTraitDict])
		#if attacker.controller == me: declareAttackStep(aTraitDict,attack,dTraitDict)
		#else: remoteCall(attacker.controller,'declareAttackStep',[aTraitDict,attack,dTraitDict])
	else:
		remoteCall(attacker.controller,'whisper',['{} has disabled Battle Calculator, so generic dice menu will be used'])
		remoteCall(attacker.controller,'genericAttack',[table])

def interimStep(aTraitDict,attack,dTraitDict,prevStepName,nextStepFunction,refusedReveal = False,damageRoll = None,effectRoll = None): #The time between steps during which attachments may be revealed. After both players pass, play proceeds to the next step.
		mute()
		GhostForm = False
		DefensiveStance = False
		debug("INTERIM STEP \n")
		#debug("dTraitDict upon entrance: {}\n".format(str(dTraitDict)))
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		#First, check if the defender is dead. If it is, this attack needs to end now.
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		aController = attacker.controller
		dController = defender.controller
		playersList = [aController,dController]
		otherPlayer = me
		for p in playersList:
				if p != me: otherPlayer = p
		selfAttached = revealAttachmentQuery([attacker,defender],prevStepName)
		#if selfAttached:
		if dTraitDict.has_key("Ghost Form"):
			GhostForm = True
			aTraitDict = computeTraits(attacker)
			dTraitDict = computeTraits(defender)
			if GhostForm:
				dTraitDict["Incorporeal"] = True		
			#debug('recalcing dTraitDict: {}'.format(dTraitDict))
		#Intent: If Akiro's is revealed after the roll dice step, allow them to reroll what they choose. Without this, if not revealed before the roll Dice step starts, the card can still be revealed but won't trigger the option
		if selfAttached:
			for attachedCard in getAttachments(attacker):
				if attachedCard.isFaceUp and attachedCard.Name == "Akiro's Favor" and attachedCard.markers[Ready]:
						damageRoll,effectRoll = akirosFavor(attachedCard,damageRoll,effectRoll,1)
		if (otherPlayer == me) or (not selfAttached and refusedReveal):
				#aTraitDict = computeTraits(attacker)
				#dTraitDict = computeTraits(defender)
				#debug('recalcing dTraitDict: {}'.format(dTraitDict))
				if not dTraitDict.get('Flying') or not aTraitDict.get('Flying'): aTraitDict['Flying']=False
				attack = computeAttack(aTraitDict,attack,dTraitDict)
				nextPlayer = {'declareAttackStep': aController,
							'avoidAttackStep' : dController,
							'rollDiceStep' : aController,
							'damageAndEffectsStep' : dController,
							'additionalStrikesStep' : aController,
							'damageBarrierStep' : dController,
							'counterstrikeStep' : dController,
							'attackEndsStep' : aController}[nextStepFunction]
				remoteCall(nextPlayer,nextStepFunction,[aTraitDict,attack,dTraitDict]+([damageRoll,effectRoll] if (damageRoll != None and effectRoll != None) else []))
		else: 
				remoteCall(otherPlayer,'interimStep',[aTraitDict,attack,dTraitDict,prevStepName,nextStepFunction,(not selfAttached),damageRoll,effectRoll])

def declareAttackStep(aTraitDict,attack,dTraitDict): #Executed by attacker
		mute()
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		#debug("DECLARE ATTACK STEP\n")
		if not attack.get('KiTrait'):
			KiTrait = ''
			#debug("KiTrait: {}\n".format(KiTrait))
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		#1. Check whether any creatures in the zone are guarding and not restrained. If they are, and this is not one of them, cancel attack (if melee)
		if (not "Elusive" in aTraitDict) and attack.get("RangeType") == "Melee" and not defender.markers[Guard]:
			guard_dicts = [ computeTraits(c) for c in getCardsInZone(getZoneContaining(defender)) if c.markers[Guard] and c.controller != attacker.controller ]
			if [ True for d in guard_dicts if not ("Restrained" in d or "Incapacitated" in d or "Pest" in d) ] and not boolQuery("There appear to be guards in this zone. Continue with attack?","Yes, ignore the guards","No, cancel attack."): return

		atkOS = Card(attack['OriginalSourceID'])
		if atkOS.Name == "Dancing Scimitar": rememberAbilityUse(atkOS) #Make a note of Dancing Scimitar's use if used to attack.
		#Ki buffs
		#debug('Checking Ki Buffs here')
		if (attack["Name"] in ["Dragon-Tail Sweep", "Fist of Iron", "Flying Side Kick", "Projected Leg Sweep", "Projected Palm", "Dragon\'s Bite"] or attacker.name == 'Monk') and "Dancing Scimitar" not in Card(attack['OriginalSourceID']).name:
			KiDice, KiEffect, KiTrait = processKiBuff(attacker, defender, attack, aTraitDict, dTraitDict)
			attack["KiDice"] = KiDice
			attack["KiEffect"] = KiEffect
			if KiTrait != "":
				if "Piercing" in KiTrait:
					temp = KiTrait.split('+')
					attack["Traits"][temp[0]]=int(temp[1])
					attack["KiTrait"] = KiTrait
				elif "Ethereal" in KiTrait and attack['Traits'].has_key('Spell'):
					KiTrait = ''
				else:
					attack["Traits"][KiTrait] = True
					attack["KiTrait"] = KiTrait
			#debug('{} {} {}'.format(str(KiDice),str(KiEffect), str(attack["Dice"])))
		#debug("Finished with Ki Buffs")
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		#Check for helm of fear
		if "Mage" in defender.Subtype and [1 for c in table if c.Name=="Helm of Fear" and c.isFaceUp and c.controller == defender.controller] and (attack.get('RangeType') == 'Melee') and (attack.get('RangeType') != 'Counterstrike') and ((not aTraitDict.get("Nonliving")) or (not "Psychic" in aTraitDict.get("Immunity",[]))):
				notify("The Helm of Fear radiates a terrifying aura!\n")
				damageRoll,effectRoll = rollDice(0)
				if effectRoll >= 9:
						notify("{} cowers in fear under the malevolent gaze of the Warlock's Helm of Fear! It cannot attack Warlock this turn!\n".format(attacker.name.split(',')[0]))
						return
				else:
						notify("{} resists the urge to panic!\n".format(attacker.name.split(',')[0]))
		#Remember arcane zap
		if attack["Name"] == "Arcane Zap" and ("Wizard" in attacker.Name or "Wizard - Playtest" in attacker.Name): rememberPlayerEvent("Arcane Zap",attacker.controller)
		#If the defender is not flying, the attacker should lose the flying trait
		if attack.get('RangeType') == 'Counterstrike': notify("{} retaliates with {}!\n".format(attacker,attack.get('Name','a nameless attack')))
		elif attack.get('RangeType') == 'Damage Barrier': notify("{} is assaulted by the {} of {}!\n".format(defender,attack.get('Name','damage barrier'),attacker))
		else: notify("\n{} attacks {} with {}!\n".format(attacker,defender,attack.get('Name','a nameless attack')))
		#Check for daze
		if attacker.markers[Daze] and attack.get('RangeType') != 'Damage Barrier' and not "Autonomous" in atkOS.traits:
				debug("Daze 2\n")
				notify("{} is rolling the Effect Die to check the Dazed condition.\n".format(attacker))#gotta figure that gender thing of yours out.
				damageRoll,effectRoll = rollDice(0)
				if effectRoll < 7:
						for attachedCard in getAttachments(attacker):
								if attachedCard.isFaceUp and attachedCard.Name == "Akiro's Favor" and attachedCard.markers[Ready]:
										damageRoll,effectRoll = akirosFavor(attachedCard,damageRoll,effectRoll,2)
								if effectRoll < 7:
										notify("{} is so dazed that it completely misses!\n".format(attacker))
										rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
										interimStep(aTraitDict,attack,dTraitDict,'Declare Attack','additionalStrikesStep')
										return
						notify("{} is so dazed that it completely misses!\n".format(attacker))
						rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
						interimStep(aTraitDict,attack,dTraitDict,'Declare Attack','additionalStrikesStep')
						return
				else: notify("Though dazed, {} manages to avoid fumbling the attack.\n".format(attacker))
		#Monk Strike Through check
		'''if (attacker.markers[Ki] > 3 and
			attacker.name == 'Monk' and
			KiTrait != 'Critical Damage' and
			attack.get('RangeType') == 'Melee' and 
			"Dancing Scimitar" not in Card(attack['OriginalSourceID']).name and
			not timesHasOccured("GhostForm",attacker.controller)):
				notifystr = "Would you like to pay 4 Ki to make this attack do Critical Damage?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					attacker.markers[Ki]-=4
					notify("{} has chosen to pay 4 Ki to make {} deal Critical Damage with the Strike Through technique\n".format(me, attack["Name"]))
					KiTrait = "Critical Damage"
					attack["Traits"][KiTrait] = True
					attack["KiTrait"] = KiTrait
				elif choice == 2:
					notify("{} has chosen not to enhance {} with Ki Techniques\n".format(me, attack["Name"]))'''
						
		interimStep(aTraitDict,attack,dTraitDict,'Declare Attack','avoidAttackStep')

def avoidAttackStep(aTraitDict,attack,dTraitDict): #Executed by defender
		mute()
		#debug("AVOID ATTACK STEP\n")
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		#debug("Attack KiTrait: {}\n".format(str(attack["KiTrait"])))
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		# Cancel spell if jinxed
		if [1 for c in getAttachments(attacker) if c.Name == "Jinx" and c.isFaceUp] and attack.get("Traits",{}).get("Spell") and attack.get("Action") == "Quick":
				notify("Jinx!\n")
				return
		if not attack.get('RangeType') == 'Damage Barrier':
				#Check for forcefield
				if len([reduceFF(c) for c in getAttachments(defender) if c.isFaceUp and c.name == "Forcefield" and c.markers[FFToken]]):
						notify("The forcefield absorbs the attack!\n".format(attacker.name.split(',')[0]))
						rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
						interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
						return
				#Check for fumble
				if len([rememberAbilityUse(c) for c in getAttachments(attacker) if c.isFaceUp and c.name == "Fumble" and not timesHasUsedAbility(c)]) and not attack.get("Traits",{}).get("Spell") and not attack.get("Traits",{}).get("Zone Attack") and not aTraitDict.get("Unmovable"):
						notify("{} fumbles the attack!\n".format(attacker.name.split(',')[0]))
						rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
						interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
						return
				#Check for block
				if len([rememberAbilityUse(c) for c in getAttachments(defender) if c.isFaceUp and c.name in ["Block"] and not timesHasUsedAbility(c)]) and not attack.get("Traits",{}).get("Unavoidable"):
						notify("{}'s attack is blocked!\n".format(attacker.name.split(',')[0]))
						rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
						interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
						return
				#Check for Redirect
				if len([rememberAbilityUse(c) for c in getAttachments(defender) if c.isFaceUp and c.name in ["Redirect"] and not timesHasUsedAbility(c)]) and not attack.get("Traits",{}).get("Unavoidable"):
						notify("{}'s attack is redirected!\n".format(attacker.name.split(',')[0]))
						rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
						interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
						return
				#Check for Reverse Attack
				if len([rememberAbilityUse(c) for c in getAttachments(defender) if c.isFaceUp and c.name in ["Reverse Attack"] and not timesHasUsedAbility(c)]) and not attack.get("Traits",{}).get("Unavoidable"):
						notify("{}'s attack is magically reversed!\n".format(attacker.name.split(',')[0]))
						attack["OriginalAttack"]["original target dict"] = dTraitDict
						interimStep(aTraitDict,attack,aTraitDict,'Avoid Attack','rollDiceStep')
						return
				#Check for Symbiotic Orb
				symb_dicts = [computeTraits(c) for c in getCardsInZone(getZoneContaining(defender)) if c.name in ["Symbiotic Orb"] and c.markers[Ready] == 1 and c != defender and c.controller == defender.controller and attack.get("RangeType") == "Melee" and not attack.get("Traits",{}).get("Unavoidable")]
				if symb_dicts:
						buttonColorList = ["#de2827","#171e78","#01603e"]
						buttonList = ["Defend using 3 Mana","Defend using dissipate","Do not defend"]
						choice = askChoice("{} is being targeted by {}'s {}. Would you like to use your Symbiotic Orb to defend?".format(defender.Name,attacker.Name,attack.get("Name")),buttonList,buttonColorList)
						if choice == 1:
							if me.mana >=3:
								me.mana -= 3
								for c in getCardsInZone(getZoneContaining(defender)):
									if c.name in ["Symbiotic Orb"]:
										toggleReady(c) 
								notify("{} spends 3 mana and their Symbiotic Orb deflects the blow!\n".format(me))
								rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
								interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
								return
							else:
								notify("{} doesn't have enough mana to spend!\n".format(me))
								buttonList2 = ["Defend using dissipate","Do not defend"]
								buttonColorList2 = ["#171e78","#01603e"]
								choice = askChoice("{} is being targeted by {}'s {}. Would you like to use your Symbiotic Orb to defend?".format(defender.Name,attacker.Name,attack.get("Name")),buttonList2,buttonColorList2)
								if choice == 1:
									for c in getCardsInZone(getZoneContaining(defender)):
										if c.name in ["Symbiotic Orb"]:
											toggleReady(c) 
									notify("{} spends a local dissipate token and their Symbiotic Orb deflects the blow! (this has to be done manually)\n".format(me))
									rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
									interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
									return
								else:
									notify("{} chooses not to power the Symbiotic Orb for this attack\n".format(me))
						elif choice == 2:
							for c in getCardsInZone(getZoneContaining(defender)):
								if c.name in ["Symbiotic Orb"]:
									toggleReady(c) 
							notify("{} spends a local dissipate token and their Symbiotic Orb deflects the blow! (this has to be done manually)\n".format(me))
							rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
							interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
							return
						else:
							notify("{} chooses not to power the Symbiotic Orb for this attack\n".format(me))
				
				#Check for Block
				if len([rememberAbilityUse(c) for c in getAttachments(defender) if c.isFaceUp and c.name in ["Block"] and not timesHasUsedAbility(c)]) and not attack.get("Traits",{}).get("Unavoidable"):
						notify("{}'s attack is blocked!\n".format(attacker.name.split(',')[0]))
						
						interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
						return
				#Check for Nullify
				if len([rememberAbilityUse(c) for c in getAttachments(defender) if c.isFaceUp and c.name in ["Nullify"] and not timesHasUsedAbility(c)]) and attack.get("Traits",{}).get("Drain"):
						notify("{}'s Spell is Nullified!\n".format(attacker.name.split(',')[0]))
						rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
						interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
						return
				#Monk Defense Check
				'''if "Monk" in defender.name:
					#Pay 3 Ki to "Parry"
					if defender.markers[Ki] > 2 and not timesHasOccured("GhostForm",defender.controller):
						if attack.get("RangeType",{})=='Melee' and not attack.get("Traits",{}).get("Unavoidable") and not "Incapacitated" in dTraitDict:
							buttonColorList = ["#de2827","#171e78","#01603e","#f7d917"]
							buttonList = ["Parry","Ghost Form (Gain Incorporeal)", "Follow Up","No"]
							choice = askChoice("{} is being targeted by {}'s {}. Would you like to spend Ki to use an ability of your Monk?".format(defender.Name,attacker.Name,attack.get("Name")),buttonList,buttonColorList)
							if choice ==1:
								defender.markers[Ki] -= 3
								notify("{}'s attack is Parried!\n".format(attacker.name.split(',')[0]))
								rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
								interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
								return
							elif choice ==2:
								defender.markers[Ki] -= 4
								dTraitDict["Incorporeal"] = True
								dTraitDict["Ghost Form"] = True
								notify("{} spends 4 Ki and becomes Incorporeal\n".format(defender.name.split(',')[0]))
								rememberPlayerEvent("GhostForm",defender.controller)
							elif choice ==3:
								defender.markers[Ki] -= 2
								defender.markers[Guard] +=1
								notify("{} spends 2 Ki to Counterstrike!\n".format(defender.name.split(',')[0]))
						elif not attack.get("RangeType",{})=='Melee' or attack.get("Traits",{}).get("Unavoidable"):
							buttonColorList = ["#de2827","#171e78","#01603e"]
							buttonList = ["Ghost Form (Gain Incorporeal)", "No"]
							choice = askChoice("{} is being targeted by {}'s {}. Would you like to spend Ki to use an ability of your Monk?".format(defender.Name,attacker.Name,attack.get("Name")),buttonList,buttonColorList)
							if choice ==1:
								defender.markers[Ki] -= 4
								dTraitDict["Incorporeal"] = True
								dTraitDict["Ghost Form"] = True
								notify("{} spends 4 Ki and becomes Incorporeal\n".format(defender.name.split(',')[0]))
					#Pay 1 Ki to give counterstrike to attacks For Follow Up
					elif defender.markers[Ki] > 0 and not timesHasOccured("GhostForm",defender.controller):
						buttonColorList = ["#de2827","#171e78"]
						buttonList = ["Yes", "No"]
						choice = askChoice("{} is being targeted by {}'s {}. Would you like to spend 2 Ki for your Monk to use Follow Up?".format(defender.Name,attacker.Name,attack.get("Name")),buttonList,buttonColorList)
						if choice == 1:
							defender.markers[Ki] -= 2
							defender.markers[Guard] +=1
							notify("{} spends 2 Ki to Counterstrike!\n".format(defender.name.split(',')[0]))
					elif timesHasOccured("GhostForm",defender.controller):
						dTraitDict["Incorporeal"] = True
						dTraitDict["Ghost Form"] = True'''
		if attack.get('EffectType','Attack')=='Attack':
			if defenseQuery(aTraitDict,attack,dTraitDict)!=False: #Skip to additional strikes step if you avoided the attack
					#Spiked buckler code here, perhaps?
					rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
					interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
					return
		interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','rollDiceStep')

def reduceFF(card):
		card.markers[FFToken] = max(0, card.markers[FFToken]-1)
		return 1

def rollDiceStep(aTraitDict,attack,dTraitDict): #Executed by attacker
		mute()
		#debug("ROLL DICE STEP\n")
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		dice = attack.get('Dice',-1)
		if dice < 0:
				notify('Error: invalid attack format - no dice found\n')
				return
		damageRoll,effectRoll = rollDice(dice) #base roll
		# Gloves of Skill re-roll opportunity
		if "Mage" in attacker.Subtype and [1 for c in table if c.Name=="Gloves of Skill" and c.isFaceUp and c.controller == attacker.controller] and (attack.get('RangeType') == 'Ranged') and not timesHasOccured("Gloves of Skill",attacker.controller):
				cName = c
				damageRoll,effectRoll = akirosFavor(cName,damageRoll,effectRoll,3)
		# Akrio's Favor re-roll opportunity
		for attachedCard in getAttachments(attacker):
				if attachedCard.isFaceUp and attachedCard.Name == "Akiro's Favor" and attachedCard.markers[Ready]:
						damageRoll,effectRoll = akirosFavor(attachedCard,damageRoll,effectRoll,1)
		#Press the Attack reroll opportunity
		if [1 for c in table if c.Name=="Press the Attack" and c.isFaceUp and c.controller == attacker.controller and "Soldier" in attacker.subtype and getZoneContaining(c) == getZoneContaining(attacker)] and (attack.get('RangeType') == 'Melee'):
				cName = c
				minorCreature=False
				level = eval(attacker.Level)
				if level <3: minorCreature=True
				damageRoll,effectRoll = akirosFavor(cName,damageRoll,effectRoll,4, minorCreature)
		
		if "V'Tar Orb" in defender.name and attack.get('RangeType') == 'Melee': #If V'Tar Orb is attacked and "Hit", handle Control Markers and end attack sequence
				notify("{} scores a Hit on the V'Tar Orb!\n".format(attacker.name))
				remoteCall(defender.controller, "placeControlMarker", [attacker.controller, defender])
				buttonColorList = ["#de2827","#171e78","#01603e"]
				buttonList = ["Gain 2 Mana","Heal 2 damage","Gain 1 Mana and Heal 1 damage"]
				while (True):
						choice = askChoice("As the Orb Powered On by the touch of the {}, it released a small amount of residual energy, your Mage may choose how to use this energy as an immediate bonus!".format(attacker.name),buttonList,buttonColorList)
						if choice == 1:
								attacker.controller.mana += 2
								notify("{} Gains 2 Mana from a small amount of residual energy release by the V'Tar Orb when it was Powered On\n".format(attacker.controller.name))
								break
						elif choice == 2:
								if attacker.controller.damage > 1:
										attacker.controller.damage -= 2
										notify("{} Heals 2 Damage from a small amount of residual energy release by the V'Tar Orb when it was Powered On\n".format(attacker.controller.name))
								elif attacker.controller.damage == 1:
										attacker.controller.damage -= 1
										notify("{} Heals 1 Damage from a small amount of residual energy release by the V'Tar Orb when it was Powered On\n".format(attacker.controller.name))
								break
						elif choice == 3:
								attacker.controller.mana += 1
								if attacker.controller.damage >= 1:
										attacker.controller.damage -= 1
										notify("{} Heals 1 Damage and Gains 1 Mana when a small amount of residual energy was released by the V'Tar Orb when it was Powered On\n".format(attacker.controller.name))
								break
				return
		elif "V'Tar Orb" in defender.name and attack.get('RangeType') != 'Melee':
				return
		setGlobalVariable("avoidAttackTempStorage","Hit")
		interimStep(aTraitDict,attack,dTraitDict,'Roll Dice','damageAndEffectsStep',False,damageRoll,effectRoll)

def damageAndEffectsStep(aTraitDict,attack,dTraitDict,damageRoll,effectRoll): #Executed by defender
		mute()
		#debug("DAMAGE AND EFFECTS STEP\n")
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		damage = damageReceiptMenu(aTraitDict,attack,dTraitDict,damageRoll,effectRoll)
		#Handle Blur
		for attachedCard in getAttachments(defender):
				if attachedCard.isFaceUp and attachedCard.Name == "Blur" and damage:
						if defender.controller.mana == 0:
								detach(attachedCard)
								attachedCard.moveTo(me.piles['Discard'])
								alignAttachments(defender)
								notify("{} does not have enough mana to pay for Blur, it has been Destroyed!\n".format(defender.Name))
						payManaChoice = askChoice("Pay 1 mana to maintain Blur on your {}?".format(defender.Name),["Yes","No"],["#01603e","#de2827"])
						if payManaChoice == 1:
								defender.controller.mana -= 1
								notify("{} pays 1 mana for Blur.\n".format(me))
						else:
								detach(attachedCard)
								attachedCard.moveTo(me.piles['Discard Pile'])
								alignAttachments(defender)
								notify("{} did not pay to maintain Blur, it has been Destroyed.\n".format(me))
		for attachedCard in getAttachments(attacker):				
			if attachedCard.isFaceUp and "Fortified Resolve" in attachedCard.Name and damage > 0 and not timesHasOccured("FortRes",attacker.controller) and "Dancing Scimitar" not in Card(attack['OriginalSourceID']).name:
				attachedCard.markers[Charge] +=1
				rememberPlayerEvent("FortRes",attacker.controller)
				notify("Fortified Resolve charges up. It now has {} charges\n".format(attachedCard.markers[Charge]))
		#Living Armor Token Removal
		if "Living Armor" in dTraitDict and damage:
			for c in table:
				if "Living Armor" in c.Name:
					if c.markers[Armor] > 0:
						c.markers[Armor] -= 1
						notify("Living Armor loses 1 Armor token\n")
						
		#Battle Meditation
		if damage > 0 and "BattleMeditation" in aTraitDict and not timesHasOccured("BMAttack",attacker.controller):
			attacker.markers[Ki]+=1
			rememberPlayerEvent("BMAttack",attacker.controller)
			notify("{}\'s Battle Meditation generates 1 Ki from the attack!".format(attacker.name))
		if damage > 0 and "BattleMeditation" in dTraitDict and not timesHasOccured("BMDefense",defender.controller):
			defender.markers[Ki]+=1
			rememberPlayerEvent("BMDefense",defender.controller)
			notify("{}\'s Battle Meditation generates 1 Ki!".format(defender.name))
		rememberAttackUse(attacker,defender,attack['OriginalAttack'],damage) #Record that the attack was declared, using the original attack as an identifier
		interimStep(aTraitDict,attack,dTraitDict,'Damage and Effects','additionalStrikesStep')

def additionalStrikesStep(aTraitDict,attack,dTraitDict): #Executed by attacker
		mute()
		#debug("Additional Strikes Step")
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		dTraitDict = attack.get("original target dict",dTraitDict) #a messy solution to the issue of multiple attacks for reverse attack.
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		strikes = 1
		atkTraits = attack.get('Traits',{})
		if atkTraits.get('Doublestrike'): strikes = 2
		if atkTraits.get('Triplestrike'): strikes = 3
		if attacker.Name == 'Wall of Thorns':
				level = eval(defender.Level)
				strikes = (level - 1 if level > 1 else 1)
		if "Swarm" in aTraitDict:
				strikes = (int(attacker.StatLife)-attacker.markers[Damage]+1)
		if timesHasUsedAttack(attacker,attack['OriginalAttack']) < strikes: declareAttackStep(aTraitDict,attack,dTraitDict)
		else: interimStep(aTraitDict,attack,dTraitDict,'Additional Strikes','damageBarrierStep')

def damageBarrierStep(aTraitDict,attack,dTraitDict): #Executed by defender
		mute()
		debug("Damage Barrier Step")
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		debug(defender.name)
		deathFlag = False
		#Check for death here
		if getRemainingLife(dTraitDict) == 0:
				debug("Death Prompt")
				deathPrompt(dTraitDict,attack,aTraitDict)
				deathFlag = True
		#But damage barriers can still happen after death!
		if attack.get('RangeType') == 'Melee' and getGlobalVariable("avoidAttackTempStorage")=="Hit":
				attackList = getAttackList(defender)
				dBarrier = None
				for a in attackList:
						if a.get('RangeType') == 'Damage Barrier':
								dBarrier = a
								break
				if dBarrier:
						bTraitDict = computeTraits(Card(dBarrier.get('SourceID',defender._id)))
						debug(bTraitDict)
						debug(dBarrier)
						declareAttackStep(bTraitDict,dBarrier,aTraitDict)
		if deathFlag:
				setEventList('Turn',[]) #Clear the turn event list
				return
		interimStep(aTraitDict,attack,dTraitDict,'Damage Barrier','counterstrikeStep')

def counterstrikeStep(aTraitDict,attack,dTraitDict): #Executed by defender
		mute()
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		if attack.get('RangeType') == 'Melee':
				counterAttack = diceRollMenu(defender,attacker,'Counterstrike')
				if counterAttack:
						counterAttack['RangeType'] = 'Counterstrike'
						counterAttack["OriginalAttack"]["RangeType"] = 'Counterstrike'
						interimStep(dTraitDict,counterAttack,aTraitDict,'Counterstrike','declareAttackStep')
				defender.markers[Guard] = 0 
		interimStep(aTraitDict,attack,dTraitDict,'Counterstrike','attackEndsStep')

def attackEndsStep(aTraitDict,attack,dTraitDict): #Executed by attacker
		mute()
		#debug("Attack Ends Step")
		#debug("Attack Name: {} , Attack Dice: {}".format(str(attack["Name"]),str(attack["Dice"])))
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		if attacker.markers[AirGlyphActive] and not "Drake" in attacker.Name:
			attacker.markers[AirGlyphActive] -= 1
			attacker.markers[AirGlyphInactive] = 1
		if attacker.markers[FireGlyphActive] and not "Drake" in attacker.Name:
			attacker.markers[FireGlyphActive] -= 1
			attacker.markers[FireGlyphInactive] = 1 
		setEventList('Turn',[]) #Clear the turn event list

def akirosFavor(card,damageRoll,effectRoll,selection, minorCreature=False):
	mute()
	# the function will allow a player with Akiro's Favor revealed to re-roll the appropriate dice based on the choices avaialbale
	# 1 - prompt to re-roll both Dice, 2 - prompt to re-roll only the effect die, 3 - prompt to re-roll only the attack dice
	effectRoll = effectRoll
	damageRoll = damageRoll
	if "Akiro" in card.name:
			akirosFavor = card
	if selection == 1:
			choice = askChoice("You have Akiro's Favor! What would you like to re-roll?",["Re-roll Attack Dice","Re-roll Effect Die","Nothing!"],["#ff0000","#ebc815","#171e78"])
			if choice == 1:
					notify("With Akiro looking over his shoulder {} has decided to re-roll the Attack Dice!\n".format(me))
					damageRoll = rollD6(sum(damageRoll))
			elif choice == 2:
					notify("With Akiro looking over his shoulder {} has decided to re-roll the Effect Die!\n".format(me))
					effectRoll = rollD12()
			else: return (damageRoll,effectRoll)
	elif selection == 2:
			choice = askChoice("You have Akiro's Favor! Would you like to re-roll the Effect Die?",["Yes!","No!"],["#171e78","#de2827"])
			if choice == 1:
					notify("With Akiro looking over his shoulder {} has decided to reroll his Effect Die!\n".format(me))
					effectRoll = rollD12()
			else: return (damageRoll,effectRoll)
	elif selection == 3:
			choice = askChoice("Your gloves increase your skill! Would you like to re-roll the Attack Dice?",["Yes!","No!"],["#171e78","#de2827"])
			if choice == 1:
					notify("With the Gloves of Skill, {} has decided to reroll the Attack Dice!\n".format(me))
					damageRoll = rollD6(sum(damageRoll))
			else: return (damageRoll,effectRoll)
	elif selection == 4:
		if minorCreature==False:
			if me.mana >1:
					choice = askChoice("Your Formation increases the attack's effectiveness! Would you like to re-roll the Attack Dice?",["Yes!","No!"],["#171e78","#de2827"])
					if choice == 1:
							notify("The soldier's formation has allowed {} to reroll the Attack Dice!\n".format(me))
							damageRoll = rollD6(sum(damageRoll))
							me.mana -= 2
							notify("{} pays 2 mana to reroll the dice\n".format(me))
					else: return (damageRoll,effectRoll)
			else: return (damageRoll,effectRoll)
		else:
			if me.mana >0:
					choice = askChoice("Your Formation increases the attack's effectiveness! Would you like to re-roll the Attack Dice?",["Yes!","No!"],["#171e78","#de2827"])
					if choice == 1:
							notify("The soldier's formation has allowed {} to reroll the Attack Dice!\n".format(me))
							damageRoll = rollD6(sum(damageRoll))
							me.mana -= 1
							notify("{} pays 1 mana to reroll the dice\n".format(me))
					else: return (damageRoll,effectRoll)
			else: return (damageRoll,effectRoll)
	if "Akiro" in card.name:
			toggleReady(akirosFavor)
	displayRoll(damageRoll,effectRoll)
	return (damageRoll,effectRoll)


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

def damageReceiptMenu(aTraitDict,attack,dTraitDict,roll,effectRoll):
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		#debug("DAMAGE RECEIPT MENU\n")
		#debug("Attack Traits: {}\n".format(str(attack["Traits"])))
		atkTraits = attack.get('Traits',{})
		totalDice = roll[0]+roll[1]+roll[2]+roll[3]+roll[4]+roll[5]
		#If it is healing, we heal and then end the attack, since it is not an attack.
		if False and attack.get('EffectType','Attack')=='Heal':
				healingAmt = min(sum([{0:0,1:0,2:1,3:2,4:1,5:2}.get(i,0)*roll[i] for i in range(len(roll))]),getStatusDict(defender).get('Damage',0))
				if healingAmt > 0: healingQuery(dTraitDict,
												'Heal {} for {} damage?'.format(defender.name,str(healingAmt)),
												healingAmt,
												"{} heals {} for {} damage!".format(attacker.name,defender.name,{}))
				else: notify("{} attempts to heal {} but fails.\n".format(attacker.name,defender.name))
				return 0 #Uh-oh...healing is treated as an attack for abilities that remember that. No worries; this will become irrelevant it Q2, and does not matter now.
		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		actualDmg,actualEffect = computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict)
		if defender.markers[VoltaricON] and actualDmg:#Voltaric Shield
				notify("The Voltaric Shield absorbs {} points of damage!\n".format(str(min(actualDmg,3))))
				actualDmg = max(actualDmg-3,0)
				defender.markers[VoltaricON] = 0
				defender.markers[VoltaricOFF] = 1
		if defender.type == "Creature": dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if actualDmg else 0) #Prep for mana drain
		else: dManaDrain = ""
		if "Incorporeal" in dTraitDict:
			if "Ethereal" in attack.get("Traits"):
				nonBlanks = roll[2] + roll[3]+roll[4]+roll[5]
				onesRolled = None
			else:
				nonBlanks = None
				onesRolled = roll[2]+roll[4]
		else:
			nonBlanks = None
			onesRolled = None
		for attachedCard in getAttachments(defender):
			if attachedCard.isFaceUp and "Fortified Resolve" in attachedCard.Name:
					if attachedCard.markers[Charge]>0:
						FRChoice = askChoice("Spend a charge marker to reduce incoming damage by 2?",["Yes","No"],["#01603e","#de2827"])
						if FRChoice == 1:
							attachedCard.markers[Charge] -= 1
							actualDmg -= 2
							notify("{}\'s Fortified Resolve absorbs 2 damage\n".format(me))
		
		normalDamage = roll[2] + 2* roll[3] # calculate the results for Normal Damage
		criticalDamage = roll[4] + 2* roll[5] # calculate the results for Critical Damage
		choice = askChoice('{}\'s attack will inflict {} damage {}on {}.{} ({} normal damage and {} critical damage were rolled.){}{}\nApply these results?'.format(attacker.Name,
																										actualDmg,
																										('and an effect ({}) '.format(actualEffect) if actualEffect else ''),
																										defender.Name,
																										(' It will also drain {} mana from {}.'.format(
																												str(dManaDrain),defender.controller.name) if dManaDrain else ''),
																										normalDamage,
																										criticalDamage,
																										('({}/{} dice rolled damage.) '.format(str(nonBlanks),str(totalDice)) if nonBlanks else ''),
																										('({}/{} dice rolled ones.) '.format(str(onesRolled),str(totalDice)) if onesRolled else '')),
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
				notify('{} has elected not to apply auto-calculated battle results\n'.format(me))
				whisper('(Battle calculator not giving the right results? Report the bug to us so we can fix it!)')

def remotePlayerHeal(amount):
		me.damage -= amount

def applyDamageAndEffects(aTraitDict,attack,dTraitDict,damage,rawEffect): #In general, need to adjust functions to accomodate partially or fully untargeted attacks.
		attacker = Card(aTraitDict.get('OwnerID',''))
		defender = Card(dTraitDict.get('OwnerID',''))
		atkTraits = attack.get('Traits',{})
		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		conditionsList = ['Bleed','Burn','Corrode','Cripple','Damage','Daze','Freeze', 'Rot','Slam','Sleep','Stagger','Stuck','Stun','Tainted','Weak']
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
		drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0)) if defender.Type in ["Mage","Creature"] else 0
		drainLifeHealth = int(round(min(getRemainingLife(dTraitDict),damage,aDamage),0)) if defender.Type in ["Mage","Creature"] else 0

		#if "Vine Marker" in defender.Name: drainableHealth = 0
		#else: drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0))

		if "Mage" in defender.Subtype: defender.controller.Damage += damage
		else: defender.markers[Damage] += damage
		notify("{} inflicts {} damage on {}{} average roll)\n".format(attacker,
																	str(damage),
																	defender,
																	('! (an above' if damage >= expectedDmg else '... (a below')))

		#Vine Markers are always destroyed from any amount of damage
		if "Vine Marker" in defender.name and damage >0:
			notify("{} is smashed into the ground and destroyed.\n".format(defender))
			defender.moveTo(me.piles['Discard'])
			return #No sense going any further.

		#Bloodreaper health drain
		if attacker.markers[BloodReaper] and not timesHasOccured("Blood Reaper",attacker.controller) and defender.Type == 'Creature' and dTraitDict.get("Living") and 'Demon' in attacker.Subtype and damage:
				mage = Card(aTraitDict.get('OwnerID'))
				healing = min(2,mage.controller.damage)
				if healing and not computeTraits(mage).get("Finite Life"):
						rememberPlayerEvent("Blood Reaper",attacker.controller)
						notify("{}'s health is restored by his Reaper's blood offering! (-{} Damage)\n".format(mage,str(healing)))
						remoteCall(mage.controller, "remotePlayerHeal", [healing])

		#Demonic Link health drain
		if [1 for c in getAttachments(attacker) if c.Name=="Demonic Link" and c.isFaceUp and c.controller==attacker.controller] and not timesHasOccured("Demonic Link",attacker) and defender.Type == 'Creature' and dTraitDict.get("Living") and damage:
				mage = Card(aTraitDict.get('OwnerID'))
				healing = min(1,mage.controller.damage)
				if healing and not computeTraits(mage).get("Finite Life"):
						rememberPlayerEvent("Demonic Link", attacker.controller)
						notify("{}'s health is restored by the Demonic Link! (-{} Damage)\n".format(mage,str(healing)))
						remoteCall(mage.controller, "remotePlayerHeal", [healing])
						
		#Malakai's Fire
		if (attacker.Name=="Priest" and attack.get("Type")=="Light" and damage and "Conjuration" not in defender.Type and not timesHasOccured("Malakai's Fire",attacker.controller) and "Flame" not in dTraitDict.get("Immunity",[])):
				remoteCall(attacker.controller,"malakaisFirePrompt",[defender])

		#Mana Drain - Long term, will want a centralized function to adjust damage/mana of a card so we can take into account things like Mana Prism
		if defender.Type == 'Creature':
			dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if damage else 0)
			defender.controller.Mana -= dManaDrain
		else: dManaDrain = ""
		if dManaDrain: notify("{} drains {} mana from {}!\n".format(attacker,str(dManaDrain),defender.controller.name))
		#Vampirism
		if (atkTraits.get('Vampiric') and drainableHealth and
			(dTraitDict.get('Living') or not dTraitDict.get('Nonliving')) and defender.Type == 'Creature' > 0): #Long term, give all creatures Living trait by default, eliminate nonliving condition
				if attacker.controller == me: healingQuery(aTraitDict,
														'Heal {} damage through vampirism?'.format(drainableHealth,defender.name),
														drainableHealth,
														"{} heals {} damage through vampirism!".format(attacker.name,'{}',defender.name))
				else: remoteCall(attacker.controller,'healingQuery',[aTraitDict,
																'Heal {} damage through vampirism?'.format(drainableHealth,defender.name),
																drainableHealth,
																"{} heals {} damage through vampirism!".format(attacker.name,'{}',defender.name)])
		#Drain/Siphon Life
		if (atkTraits.get('Drain') and drainLifeHealth and
			(dTraitDict.get('Living') or not dTraitDict.get('Nonliving')) and defender.Type == 'Creature' > 0): #Long term, give all creatures Living trait by default, eliminate nonliving condition
				if attacker.controller == me: healingQuery(aTraitDict,
														'Drain {} life from the target?'.format(drainLifeHealth,defender.name),
														drainLifeHealth,
														"{} drains {} life from {}".format(attacker.name,'{}',defender.name))
				else: remoteCall(attacker.controller,'healingQuery',[aTraitDict,
																'Drain {} life from the target?'.format(drainLifeHealth,defender.name),
																drainLifeHealth,
																"{} drains {} life from {}".format(attacker.name,'{}',defender.name)])
		#Reconstruct - Devouring Jelly for now
		if (attacker.Name=="Devouring Jelly" and defender.Type == 'Creature' and dTraitDict.get('Corporeal') and damage and attacker.markers[Damage] > 0):
				cDamage = attacker.markers[Damage]
				reconstructAmount = 2
				if cDamage <= 2:
						attacker.markers[Damage] = 0
						notify("{} reconstructs {} Life and removes all damage.\n".format(attacker.Name,cDamage))
				else:
						attacker.markers[Damage] -= reconstructAmount
						notify("{} reconstructs 2 Life and removes {} damage.\n".format(attacker.Name,reconstructAmount))
		#Finally, apply conditions
		effects = ([rawEffect.split(' ')[1],rawEffect.split(' ')[1]] if '2' in rawEffect else rawEffect.split(' & ')) if rawEffect else []
		for e in effects:
				if e in conditionsList:
						if e == "Damage" and "Mage" in defender.Subtype: defender.controller.damage += 1
						else: defender.markers[eval(e)]+=1
				notify('{} {}\n'.format(defender.Name,effectsInflictDict.get(e,'is affected by {}!'.format(e))))

def malakaisFirePrompt(heathen):
		mute()
		if me.mana >= 1 and askChoice("Smite the heathen with Malakai's Fire?",["Yes (1 mana)","No"],["#01603e","#de2827"])==1:
				me.mana -= 1
				notify("{} pays 1 mana to Smite the heathen {} with Malakai's Fire.\n".format(me,heathen))
				rememberPlayerEvent("Malakai's Fire")
				remoteCall(heathen.controller,"malakaisFireReceiptPrompt",[heathen])

def malakaisFireReceiptPrompt(heathen):
		mute()
		if askChoice("Malakai smites {}! Apply Burn condition?".format(heathen.Name.split(",")[0]),["Yes","No"],["#01603e","#de2827"])==1:
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
				notify("{} is seared by the flames of righteousness! (+1 Burn)\n".format(heathen.Name.split(",")[0]))

def deathPrompt(cardTraitsDict,attack={},aTraitDict={}):
		mute()
		card = ""
		card = Card(cardTraitsDict.get('OwnerID'))
		if "Mage" in card.Subtype: return

		choice = askChoice("{} appears to be destoyed. Accept destruction?".format(card.name),
						["Yes","No"],
						["#01603e","#de2827"])
		if choice == 1:
				returnMarkers(card, cardTraitsDict)
				deathMessage(cardTraitsDict,attack,aTraitDict)
				if ((attack.get('Traits',{}).get('Devour') and cardTraitsDict.get("Corporeal") and card.Type == 'Creature') or
					card.markers[Zombie]): obliterate(card)
				else: discard(card)
		else: notify("{} does not accept the destruction of {}.\n".format(me,card))

def revealAttachmentQuery(cardList,step): #Returns true if at least 1 attachment was revealed
		recommendList = getEnchantRecommendationList(step)
		recurText = 'an'
		while True:
				aList = []
				for card in cardList:
						aList.extend([c for c in getAttachments(card) if (c.controller == me and
																		not c.isFaceUp and
																		c.Name in recommendList)])
				if not aList: return (False if recurText == 'an' else True)
				options = ['{}\n{}\n{}'.format(c.Name.center(68,' '),(('('+getAttachTarget(c).Name+')').center(68,' ')),c.Text.split('\r\n')[0]) for c in aList]
				colors = ['#CC6600' for i in options] #Orange
				options.append('I would not like to reveal an enchantment.')
				colors.append("#de2827")
				choice = askChoice('Would you like to reveal {} enchantment?'.format(recurText),options,colors)
				if choice == len(options): return (False if recurText == 'an' else True)
				revealEnchantment(aList[choice-1])
				recurText = 'another'

def computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict):
		defender = Card(dTraitDict["OwnerID"])
		armor = computeArmor(aTraitDict,attack,dTraitDict)
		atkTraits = attack.get('Traits',{})
		gameMode = getGlobalVariable("GameMode")
		#Attempt to implement different effects for Ethereal based on community playtest project
		if gameMode == "Playtest":
				if dTraitDict.get('Incorporeal'): return (roll[2] + roll[4] + (((roll[3]+roll[5])) if atkTraits.get('Ethereal') else 0)),computeEffect(effectRoll,aTraitDict,attack,dTraitDict)
		else:
				if dTraitDict.get('Incorporeal'): return (roll[2] + roll[4] + ((2*(roll[3]+roll[5])) if atkTraits.get('Ethereal') else 0)),computeEffect(effectRoll,aTraitDict,attack,dTraitDict)
		if dTraitDict.get('Incorporeal'): return (roll[2] + roll[4] + ((2*(roll[3]+roll[5])) if atkTraits.get('Ethereal') else 0)),computeEffect(effectRoll,aTraitDict,attack,dTraitDict)
		normal = roll[2] + 2*roll[3]
		critical = roll[4] + 2*roll[5]

		normalD = 0 if (dTraitDict.get('Resilient') or atkTraits.get('Critical Damage')) else normal
		criticalD = critical + (normal if atkTraits.get('Critical Damage') else 0)

		if "Mage" in defender.Subtype and [1 for c in table if c.isFaceUp and c.Name == "Veteran's Belt" and c.controller == defender.controller]: #handle veteran's belt
				reduction = min(criticalD,2)
				criticalD -= reduction
				normalD += reduction

		return ( max( normalD - armor, 0 ) + criticalD, computeEffect(effectRoll,aTraitDict,attack,dTraitDict))

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
		#Ring of Tides for a hydro attack from a Siren
		if attacker.Name == "Siren" and "Tides" in aTraitDict and ("Type" in attack.keys() and attack['Type']=="Hydro") and int(getGlobalVariable("PlayerWithIni")) == me._id : modRoll += 2
		if attacker.markers[AirGlyphActive]:
			modRoll +=4
		if attacker.Name == "Temple of Light":
				eventList = getEventList("Round")
				for e in reversed(eventList):
						if "ToLX" in e[0]:
								modRoll += e[1]
								break

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
		#debug('EffectRoll: {}, ModRoll: {}'.format(str(effectRoll),str(modRoll)))
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
				if "Mage" in card.Subtype:
						healed = min(card.controller.Damage,healingAmt)
						card.controller.Damage -= healed
				else:
						healed = min(card.markers[Damage],healingAmt)
						card.markers[Damage] -= healed
				notify(notifyText.format(str(healed)))

############################################################################
######################		Trait Computation	####################
############################################################################
"""
This section contains functions that figure out exactly which traits a card has.
"""

def computeTraits(card):
		"""This is the centralized function that reads all traits possessed by a card. Do NOT compute traits anywhere else, ONLY compute them here.
		It returns a dictionary of traits. This function will end up being quite long and complex.It works together with traitParser. Standard format
		for traits is a dictionary."""
		debug("computeTraits being called")
		traitDict = {}
		markers = card.markers
		name = card.name
		controller = card.controller
		subtype = card.subtype
		cardType = card.type
		school = card.school
		rawTraitsList = ({'Creature' : ['Living','Corporeal'],
						'Conjuration' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity'],
						'Conjuration-Wall' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity'],
						'Conjuration-Terrain' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity']}.get(cardType,[])) #Get innate traits depending on card type
		append = rawTraitsList.append
		extend = rawTraitsList.extend
		remove = rawTraitsList.remove
		listedTraits = card.Traits.split(', ')
		if 'Living' in listedTraits and 'Nonliving' in rawTraitsList: remove('Nonliving')
		elif 'Nonliving' in listedTraits and 'Living' in rawTraitsList: remove('Living')
		if 'Incorporeal' in listedTraits and 'Corporeal' in rawTraitsList: remove('Corporeal')
		if (name == 'Shoalsdeep Tidecaller' and int(getGlobalVariable("PlayerWithIni")) == me._id): append('Melee +2')
		extend(listedTraits)
		adraAbility = True
		adraEnemy = bool([c for c in table if c.name=="Adramelech Warlock" and c.controller != controller])
		for c in table: #scan cards in table for bonuses. We want to minimize iterations, so we'll scan only once.
				cName = c.name
				cController = c.controller
				cSubtype = c.subtype
				cType = c.type
				cMarkers = c.markers
				if 'Mage' in cSubtype and cController == controller and 'Magestats' not in cType: 
					traitDict['MageID'] = c._id #Each card knows which mage controls it.
					mage = Card(traitDict['MageID'])
				if c.isFaceUp: #only look at face-up cards
						if getAttachTarget(c) == card: #Get traits from attachments to this card:
								if cType in ['Enchantment','Conjuration']:
										rawText = c.text.split('\r\n[')
										traitsGranted = ([t.strip('[]') for t in rawText[1].split('] [')] if len(rawText) == 2 else [])
										extend(traitsGranted)
								if adraEnemy and "Curse" in cSubtype and cController != controller:
										adra = bool([k for k in table if k.name=="Adramelech Warlock" and k.controller == cController])
										if adra and adraAbility:
												append('Flame +1')
												adraAbility = False
												#debug('Triggered')
								if cName == "Sentinel of V'tar":
										for o in table:
												isWithOrb = False
												if ("V'Tar Orb" in c.name and
													getZoneContaining(c) == getZoneContaining(card)): isWithOrb = True
												if isWithOrb:
														extend(['Unmovable','Anchored'])
														if markers[Guard]: extend(['Armor +2','Melee +1'])
								if cName == "Maim Wings": rawTraitsList = [t for t in list(rawTraitsList) if t != 'Flying']
								if cName == 'Shrink': append('Pest')
								if cName == 'Glancing Blow': append('Glancing')
								if cName == 'Blessed Focus':
									cCreature = getAttachTarget(c)
									if cCreature.markers[Damage]==0: extend(['Melee +1','Piercing +1'])

						# Get traits from cards in this zone
						if getZoneContaining(c) == getZoneContaining(card): #get traits from cards in this zone.
								#Note - we need to optimize the speed here, so we'll use if branching even though we are hardcoding specific cases.
								if (name == 'Skeelax, Taunting Imp'
										and c.markers[Burn]): append('Regenerate 2') #and phase = upkeep, but I don't think this matters for now.
								elif (name in ['Sslak, Orb Guardian','Usslak, Orb Guardian'] and "V'Tar Orb" in c.name):
										extend(['Unmovable','Anchored'])
								elif cType == 'Incantation': pass
								elif cType == 'Enchantment':
										if (cName == 'Fortified Position' and
												cardType == 'Creature' and
												cController == controller and
												'Corporeal' in rawTraitsList): append('Armor +2')
										if (cName == 'Resolute Aura' and
												cardType == 'Creature' and
												cController == controller): extend(['Tough -2'])
										if (cName == 'Resolute Aura' and
												cardType == 'Creature' and
												cController == controller and
												name != "Paladin"): append('Armor +2')
										if (cName == 'Vengeful Aura' and
												cardType == 'Creature' and
												cController == controller): append('Melee +1')
										if (cName == 'Vengeful Aura' and
												cardType == 'Creature' and
												cController == controller): extend(['Piercing +2'])
										if (cName == 'Sacred Ground' and
												cController == controller and
												cardType == 'Creature' and
												'Living' in rawTraitsList): append('Aegis 1')
										if (cName == 'Healing Madrigal' and
												c.isFaceUp and
												cController == controller and
												cardType == 'Creature' and
												'Living' in rawTraitsList): append('Madrigal')
										if (cName == 'Plagued' and
												c.isFaceUp and
												cardType == 'Creature' and
												not 'Poison Immunity' in rawTraitsList and
												'Living' in rawTraitsList): append('Plagued')
										if (cName == 'Standard Bearer' and
												cController == controller and
												getAttachTarget(c) != card and
												cardType == 'Creature'): extend(['Melee +1','Armor +1'])
										if (cName == 'Press the Attack' and
												cController == controller and
												"Soldier" in subtype and
												cardType == 'Creature'): extend(['Melee +1'])
										if (cName == 'Dig In' and
												cController == controller and
												"Soldier" in subtype and
												cardType == 'Creature'): extend(['Armor +1'])
										if (cName == 'Fire at Will' and
												cController == controller and
												"Soldier" in subtype and
												cardType == 'Creature'): extend(['Piercing +2'])
								elif cType == 'Conjuration' or cType == 'Conjuration-Terrain':
										if (cName == 'Consecrated Ground' and
												cardType == 'Creature' and
												cController == controller and
												subtype != 'Mage' and
												'Holy' in school and
												'Living' in rawTraitsList): append('Regenerate 1')
										if (cName == 'Consecrated Ground' and
												cardType == 'Creature' and
												cController != controller and
												subtype != 'Mage' and
												'Holy' not in school): append('Consecrated Ground Damage')
										if (cName == 'Mohktari, Great Tree of Life' and
												cController == controller and
												cardType == 'Creature' and
												'Living' in rawTraitsList): append('Regenerate 2')
										if (cName == 'Raincloud' and
												('Conjuration' in cardType or cardType == 'Creature') and
												'Living' in rawTraitsList): extend(['Regenerate 1','Flame -2','Acid -2'])
										if (cName == 'Shallow Sea' and
												cardType == 'Creature' and
												"Aquatic" in subtype): append('Melee +1')
										if (cName == 'Shallow Sea' and
												cardType == 'Creature' and
												"Aquatic" not in subtype): append('Shallow Sea')
										if (cName == 'Frozen Tundra' and
												'Frost' not in subtype): append('Frost +1')
										if (cName == 'Hellscape' and
												name != "Hellscape" and
												"Flame Immunity" not in rawTraitsList): append('Hellscape')
										if (cName == 'Hellscape' and
												"Flame Immunity" not in rawTraitsList): append('Flame +1')
										if (cName == 'Poison Gas Cloud' and
												cardType == 'Creature' and
												"Nonliving" not in rawTraitsList and
												"Poison Immunity" not in rawTraitsList): append('PoisonGasCloud')
										if (cName == 'Frozen Tundra'): append('FrozenTundra')
										if (cName == 'Steep Hill' and
												cardType == 'Creature'): append("Ranged +1-if-Non-Flying")
										if (cName == 'Swamp' and cardType == 'Creature' and
												(not 'Aquatic' in subtype) and
												("Non-Flying" in rawTraitsList or not 'Flying' in rawTraitsList)): extend(['Slow-if-Non-Flying','Unmovable-if-Non-Flying','Non-Elusive'])
										if cName == 'Ethereal Mist': append('Obscured')
										if ((cName == 'Corrosive Pool'  or
												cName == 'Molten Rock') and
												cardType == 'Creature' and
												'Corporeal' in rawTraitsList and
												("Non-Flying" in rawTraitsList or not 'Flying' in rawTraitsList)): append('Hindered-if-Non-Flying')
										if cName == 'Samandriel&apos;s Circle':
												if cardType == 'Creature' and 'Living' in rawTraitsList: append('Regenerate 1')
												elif cardType == 'Creature' and 'Nonliving' in rawTraitsList: append('Hindered')
										if (cName == 'Septagram' and
												(not "Mage" in subtype)): append('Warded')
								elif cType == 'Creature':
										if (cName == 'Highland Unicorn' and
												cController == controller and
												cardType == 'Creature' and
												'Living' in rawTraitsList): append('Regenerate 1')
										if (name == 'Guard Dog' and
												cController == controller and
												'Conjuration' in cardType and
												not getAttachTarget(c)): append('Vigilant')
										if (cName == 'Makunda' and
												cController == controller and
												c != card and
												cardType == 'Creature' and
												'Cat' in subtype): append('Piercing +1') #Long term, need to indicate that it is only melee attacks. For now, should not matter since no cats have ranged attacks.
										if (cName == 'Redclaw, Alpha Male' and
												c != card and
												cardType == 'Creature' and
												'Canine' in subtype): extend(['Armor +1','Melee +1'])
										if (cName == 'Sardonyx, Blight of the Living' and
												cardType == 'Creature' and
												'Living' in rawTraitsList): append('Finite Life')
										if (cName == 'Malacoda' and
												cardType == 'Creature' and
												not 'Poison Immunity' in rawTraitsList and
												'Living' in rawTraitsList): append('Malacoda')
										if (cName == 'Steelclaw Cub' and
												name == 'Steelclaw Matriarch' and
												cController == controller): append('Melee +1')
								if ('Mage' in cSubtype and cController == controller): #Effects when creature is in same zone as controlling mage
										if name == 'Goran, Werewolf Pet': append('Bloodthirsty +1')
										if markers[Pet] and 'Animal' in subtype: append('Melee +1')
								if ('Siren' in name and 'Conjuration-Terrain' in cType and cSubtype == 'Aquatic'): 
									append('Channeling +1')
									append('AquaticTerrain')
								if (name == 'Naiya' and 'Conjuration-Terrain' in cType and cSubtype == 'Aquatic'): 
									append('Regenerate 1')
									append('Channeling +1')
						if 'Mage' in subtype and not 'Magestats' in cardType:
								if cType == 'Equipment' and cName == 'Ring of Tides' and (cController == controller) and not c.markers[Disable] and int(getGlobalVariable("PlayerWithIni")) == me._id: append ('Tides')#This will need changed some day to just add attack dice, but this is a quick fix for the moment
								if cType == 'Equipment' and cName == 'Force Armor' and (cController == controller) and not c.markers[Disable]: append('Force Armor')
								if cType == 'Equipment' and cName == 'Dampening Cloak' and (cController == controller) and not c.markers[Disable]: append('DampCloak')
								if cType == 'Equipment' and cName == 'Living Armor' and cController == controller: 
									append('Armor +{}'.format(str(cMarkers[Armor])))
									append('Living Armor')
								if cType == 'Equipment' and (cController == controller or getAttachTarget(c) == card) and not c.markers[Disable]:
										rawText = c.text.split('\r\n[')
										traitsGranted = ([t.strip('[]') for t in rawText[1].split('] [')] if len(rawText) == 2 else [])
										extend(traitsGranted)
										#Runesmithing
										if c.markers[RuneofFortification] and 'Armor +' in ', '.join(rawText): append('Armor +1')
								if cName in ['Mana Crystal','Mana Flower']: append('Channeling +1')
								if cName == 'Animal Kinship':
										canine = reptile = bear = ape = cat = False
										for a in table:
												aSubtype = a.subtype
												if (a.controller == controller and
														'Animal' in aSubtype and
														cardType == 'Creature'):
														if 'Canine' in aSubtype: canine = True
														if 'Reptile' in aSubtype: reptile = True
														if 'Bear' in aSubtype: bear = True
														if 'Ape' in aSubtype: ape = True
														if 'Cat' in aSubtype: cat = True
										if canine: append('Melee +1')
										if reptile: append('Armor +1')
										if bear: append('Tough -2')
										if ape: append('Climbing')
										if cat: append('Elusive')
						#Global effects
						#Conjurations
						if (cName == 'Idol of Pestilence' and card.isFaceUp and cardType == 'Creature' and not 'Poison Immunity' in rawTraitsList and 'Living' in rawTraitsList): append('Pestilence')
						if (cName == 'Wreck of the Viridian Lace' and 'Pirate' in subtype and int(getGlobalVariable("PlayerWithIni")) == me._id): extend(['Melee +1', 'Ranged +1'])
						if (cName == 'Armory' and cController == controller and 'Soldier' in subtype): extend(['Armor +1','Piercing +1'])
						if (cName == 'Rajan\'s Fury' and 'Animal' in subtype): append('Charge +1')
						if (cName == 'Gate to Hell' and cController == controller and 'Demon' in subtype): append('Melee +1')
						if (cName == 'Deathlock' and cardType in ['Creature','Conjuration','Conjuration-Wall','Conjuration-Terrain']): append('Finite Life')
						if (cName == 'Etherian Lifetree' and 'Living' in rawTraitsList and c != card): append('Innate Life +2')
						if (cName == 'Rolling Fog'): append('Obscured')
						if (cName == 'Gravikor' and card.isFaceUp and cardType == 'Creature' and 'Flying' in rawTraitsList and cardGetDistance(c,card)<=2): 
							append('Non-Flying')
							remove('Flying')
						#>>Altar of Skulls<<
						#Incantations
						if (cName == 'Akiro\'s Battle Cry' and cController == controller and 'Soldier' in subtype): extend(['Charge +2,Fast'])
						if (cName == 'Call of the Wild' and cController == controller and 'Animal' in subtype): append('Melee +1')
						if (cName == 'Zombie Frenzy' and ('Zombie' in subtype or markers[Zombie])):
								rawTraitsList = [t for t in rawTraitsList if t not in ['Lumbering','Pest','Slow']]
								extend(['Fast','Bloodthirsty +1'])
		
		if markers[Melee]: append('Melee +{}'.format(str(markers[Melee])))
		if markers[Ranged]: append('Ranged +{}'.format(str(markers[Ranged])))
		if markers[Armor]: append('Armor +{}'.format(str(markers[Armor])))
		if markers[Growth]: extend(['Life +{}'.format(str(3*markers[Growth])),'Melee +{}'.format(str(markers[Growth]))])
		if markers[Corrode]: append('Armor -{}'.format(str(markers[Corrode])))
		if markers[Guard]:
				extend(['Counterstrike','Non-Flying'])
				if 'Flying' in listedTraits and 'Non-Flying' in rawTraitsList: remove('Flying')
		if markers[Sleep] or markers[Stun] or markers[Slam]: append('Incapacitated')
		if markers[Zombie]:
				extend(['Psychic Immunity','Slow','Nonliving','Bloodthirsty +0'])
				remove('Living')
				#Also should add undead,zombie subtypes, but no way to do that without the spellDictionary.
		if markers[Stuck] : extend(['Restrained','Unmovable'])
		if markers[Daze]: append('Defense -{}'.format(str(markers[Daze])))
		if markers[Light]: append('Light +{}'.format(str(markers[Light])))
		if markers[Obscured]: append('Obscured')
		if markers[Pet] and 'Animal' in subtype: extend(['Melee +1','Armor +1','Life +3'])
		if markers[BloodReaper] and 'Demon' in subtype: append('Bloodthirsty +2')
		if markers[EternalServant] and 'Undead' in subtype and not "Legendary" in card.Traits: append('Piercing +1')
		if markers[Treebond] and 'Tree' in subtype: extend(['Innate Life +4','Armor +1','Lifebond +2'])
		if markers[Veteran]: extend(['Armor +1','Melee +1'])
		if markers[HolyAvenger] and 'Holy' in card.School and not 'Legendary' in card.Traits: append('Life +5')
		if markers[Wrath]: append('Melee +{}'.format(str(markers[Wrath])))
		if markers[Rage]: append('Melee +{}'.format(str(markers[Rage])))
		if markers[SirensCall] and 'Aquatic' in subtype and "Siren" in mage.name and 'Mage' not in subtype: extend(['Melee +2'])
		if markers[Grapple]: extend(['Melee -2'])
		if markers[EarthGlyphActive] and 'Magestats' not in card.Type: append('Armor +2')
		if markers[ToughToken]: extend(['Tough -2'])
		if markers[DefenseToken]: extend(['Defense +1'])

				#Harshforge monolith

		if 'Unstoppable' in rawTraitsList: extend(['Unmovable','Uncontainable'])
		if 'Incorporeal' in rawTraitsList: extend(['Nonliving','Burnproof','Uncontainable'])
		if 'Nonliving' in rawTraitsList: extend(['Poison Immunity','Finite Life'])
		if 'Rooted' in rawTraitsList: extend(['Unmovable','Non-Flying'])
		if 'Restrained' in rawTraitsList: extend(['Defense -2','Non-Flying'])
		if 'Incapacitated' in rawTraitsList and 'Flying' in listedTraits: remove('Flying')#append('Non-Flying')
		if (name == 'Gargoyle Sentry' and markers[Guard]): extend(['Armor +3','Tough -3'])
		if (name == 'Dwarf Panzergarde' and markers[Guard]): extend(['Defense +3'])
		if (name == 'Dragonclaw Wolverine' and markers[Rage]):
				append('Armor +{}'.format(str(markers[Rage])))
				if markers[Rage] >= 3: append('Counterstrike')

		if not "Flying" in rawTraitsList: append("Non-Flying") #Unfortunate, but needed for next step

		for condtrait in ["Slow","Unmovable","Ranged +1"]:
				for cond in ["Non-Flying"]:
						if '{}-if-{}'.format(condtrait,cond) in rawTraitsList and cond in rawTraitsList:
								append(condtrait)

		for nulltrait in ["Flying,Elusive"]:
				if 'Non-{}'.format(nulltrait) in rawTraitsList:
						rawTraitsList = [t for t in list(rawTraitsList) if t != nulltrait and t != 'Non-{}'.format(nulltrait)]

		for rawTrait in rawTraitsList:
				formTrait = traitParser(rawTrait)
				if formTrait[0] in additiveTraits: traitDict[formTrait[0]] = traitDict.get(formTrait[0],0) + (0 if formTrait[1] == '-' else int(formTrait[1]))
				elif formTrait[0] in superlativeTraits: traitDict[formTrait[0]] = max(traitDict.get(formTrait[0],0),int(formTrait[1]))
				elif formTrait[0] == 'Immunity':
						if not traitDict.get('Immunity'): traitDict['Immunity'] = [formTrait[1]]
						else: traitDict['Immunity'].append(formTrait[1])
				else: traitDict[formTrait[0]] = True
		traitDict['OwnerID'] = card._id #Tag the dictionary with its owner's ID in case we need to extract it later (extracting the owner is MUCH faster than extracting the dictionary)
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

def processKiBuff(attacker, defender, attack, aTraitDict, dTraitDict):
	KiDice = False
	KiEffect = False
	KiTrait = ""
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	mage = Card(mageID)
	if timesHasOccured("GhostForm",attacker.controller):#And non-spell attack?
		KiTrait = "Ethereal"
	else:
		if mage.markers[Ki] >0 and ('Nunchucks' in aTraitDict or "Sai" in aTraitDict) and attack["RangeType"]=='Melee':
			if 'Nunchucks' in aTraitDict:
				notifystr = "Would you like to pay 1 Ki to give this attack 1 additional die with Nunchucks?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=1
					notify("{} has chosen to pay 1 Ki for their nunchucks to give {} one additional die\n".format(me, attack["Name"]))
					KiDice = True
			if mage.markers[Ki] >0 and "Sai" in aTraitDict:
				notifystr = "Would you like to pay 1 Ki to give this attack + 2 Piercing?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=1
					notify("{} has chosen to pay 1 Ki for their Sai to give {} Piercing +2\n".format(me, attack["Name"]))
					KiTrait = "Piercing+2"
		if mage.markers[Ki] > 0 and attack["Name"] == "Dragon\'s Bite":
				notifystr = "Would you like to pay 1 Ki to give this attack +6 to the Effect Roll?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=1
					notify("{} has chosen to pay 1 Ki to give {} +6 to the Effect Roll\n".format(me, attack["Name"]))
					KiEffect = True
				elif choice == 2:
					notify("{} has chosen not enhance {} with Ki\n".format(me, attack["Name"]))
		elif mage.markers[Ki] > 1 and attack["Name"] in ["Dragon-Tail Sweep", "Flying Side Kick", "Projected Leg Sweep", "Projected Palm"]:
			if attack["Name"] == "Dragon-Tail Sweep":
				notifystr = "Would you like to pay 2 Ki to give this attack 1 additional die?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=2
					notify("{} has chosen to pay 2 Ki to give {} one additional die\n".format(me, attack["Name"]))
					KiDice = True
				elif choice == 2:
					notify("{} has chosen not enhance {} with Ki\n".format(me, attack["Name"]))
			elif attack["Name"] == "Flying Side Kick":
				notifystr = "Would you like to pay 2 Ki to give this attack 2 additional dice?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=2
					notify("{} has chosen to pay 2 Ki to give {} two additional die\n".format(me, attack["Name"]))
					KiDice = True
				elif choice == 2:
					notify("{} has chosen not enhance {} with Ki\n".format(me, attack["Name"]))
			elif attack["Name"] == "Projected Leg Sweep":
				notifystr = "Would you like to pay 2 Ki to give this attack +6 to the Effect Roll?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=2
					notify("{} has chosen to pay 1 Ki to give {} +6 to the Effect Roll\n".format(me, attack["Name"]))
					KiEffect = True
				elif choice == 2:
					notify("{} has chosen not enhance {} with Ki\n".format(me, attack["Name"]))
			elif attack["Name"] == 'Projected Palm':
				notifystr = "Would you like to pay 2 Ki to give this attack Unavoidable?"
				choiceList = ['Yes', 'No']
				colorsList = ['#0000FF', '#FF0000']
				choice = askChoice("{}".format(notifystr), choiceList, colorsList)
				if choice == 1 :
					mage.markers[Ki]-=2
					notify("{} has chosen to pay 2 Ki to give {} Unavoidable.\n".format(me, attack["Name"]))
					KiTrait = "Unavoidable"
				elif choice == 2:
					notify("{} has chosen not enhance {} with Ki\n".format(me, attack["Name"]))
		elif mage.markers[Ki] > 2 and attack["Name"] == "Fist of Iron":
			notifystr = "Would you like to pay 3 Ki to make this attack do Critical Damage?"
			choiceList = ['Yes', 'No']
			colorsList = ['#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if choice == 1 :
				mage.markers[Ki]-=3
				notify("{} has chosen to pay 3 Ki to make {} deal Critical Damage\n".format(me, attack["Name"]))
				KiTrait = "Critical Damage"
			elif choice == 2:
				notify("{} has chosen not enhance {} with Ki\n".format(me, attack["Name"]))
		'''if mage.markers[Ki] > 2 and mage.name == 'Monk' and not timesHasOccured("GhostForm",attacker.controller):
			notifystr = "Would you like to pay 4 Ki to use Ghost Form?"
			choiceList = ['Yes', 'No']
			colorsList = ['#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if choice == 1:
				defender.markers[Ki] -= 4
				aTraitDict["Incorporeal"] = True
				aTraitDict["Ghost Form"] = True
				KiTrait = "Ethereal"
				notify("{} spends 4 Ki and becomes Incorporeal\n".format(attacker.name.split(',')[0]))
				rememberPlayerEvent("GhostForm",attacker.controller)
			elif choice == 2:
				notify("{} has chosen not to use Ghost Form\n".format(me, attack["Name"]))	'''
	return KiDice, KiEffect, KiTrait
	
def buffWithGlyphs(mageStats, attacker, drake = None):
	if me.Mana > 6:
		if timesHasOccured("AirGlyphDeactivate",attacker.controller) and timesHasOccured("FireGlyphDeactivate",attacker.controller):
			notifystr = "You have already deactivated both this round"
			choiceList = ['OK']
			colorsList = ['#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			choice = 4
		elif timesHasOccured("FireGlyphDeactivate",attacker.controller):
			notifystr = "Would you like to deactivate your Air Glyph?"
			choiceList = ['Yes', 'No']
			colorsList = ['#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if choice == 2:
				choice = 4
		elif timesHasOccured("AirGlyphDeactivate",attacker.controller):
			notifystr = "Would you like to deactivate your Fire Glyph?"
			choiceList = ['Yes', 'No']
			colorsList = ['#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if choice == 1:
				choice = 2
			else:
				choice = 4
		else:
			notifystr = "Which buff would you like to apply?"
			choiceList = ['Air (+4 effect)', 'Fire (+2 dice)', 'both' ,'None']
			colorsList = ['#0000FF','#0000FF','#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1:
			me.Mana -=3
			if drake and drake.markers[AirGlyphActive]>0 and drake != attacker:
				drake.markers[AirGlyphActive] = 0
				drake.markers[AirGlyphInactive] = 1
			else:
				mageStats.markers[AirGlyphActive] = 0
				mageStats.markers[AirGlyphInactive] = 1
			attacker.markers[AirGlyphActive] +=1
			rememberPlayerEvent("AirGlyphDeactivate",attacker.controller)
			notify("{} has chosen to pay 3 mana and deactivate the Air Glyph to give this attack +4 to the effect roll\n".format(me))
		elif choice == 2:
			me.Mana -=3
			if drake and drake.markers[FireGlyphActive]>0 and drake != attacker:
				drake.markers[FireGlyphActive] = 0
				drake.markers[FireGlyphInactive] = 1
			else:
				mageStats.markers[FireGlyphActive] = 0
				mageStats.markers[FireGlyphInactive] = 1
			attacker.markers[FireGlyphActive] +=1
			rememberPlayerEvent("FireGlyphDeactivate",attacker.controller)
			notify("{} has chosen to pay 3 mana and deactivate the Fire Glyph to give this attack +2 dice\n".format(me))
		elif choice ==3:
			me.Mana -=6
			if drake and drake.markers[AirGlyphActive]>0 and drake != attacker:
				drake.markers[AirGlyphActive] = 0
				drake.markers[AirGlyphInactive] = 1
			else:
				mageStats.markers[AirGlyphActive] = 0
				mageStats.markers[AirGlyphInactive] = 1
			attacker.markers[AirGlyphActive] +=1
			if drake and drake.markers[FireGlyphActive]>0 and drake != attacker:
				drake.markers[FireGlyphActive] = 0
				drake.markers[FireGlyphInactive] = 1
			else:
				mageStats.markers[FireGlyphActive] = 0
				mageStats.markers[FireGlyphInactive] = 1
			attacker.markers[FireGlyphActive] +=1
			rememberPlayerEvent("FireGlyphDeactivate",attacker.controller)
			rememberPlayerEvent("AirGlyphDeactivate",attacker.controller)
			notify("{} has chosen to pay 6 mana and deactivate both Air and Fire Glyphs to give this attack +2 dice and +4 to the effect roll\n".format(me))
	elif me.Mana > 2:
		notifystr = "Which buff would you like to apply?"
		choiceList = ['Air (+4 effect)', 'Fire (+3 dice)','None']
		colorsList = ['#0000FF','#0000FF','#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1:
			me.Mana -=3
			if drake and drake.markers[AirGlyphActive]>0 and drake != attacker:
				drake.markers[AirGlyphActive] = 0
				drake.markers[AirGlyphInactive] = 1
			else:
				mageStats.markers[AirGlyphActive] = 0
				mageStats.markers[AirGlyphInactive] = 1
			attacker.markers[AirGlyphActive] +=1
			rememberPlayerEvent("AirGlyphDeactivate",attacker.controller)
			notify("{} has chosen to pay 3 mana and deactivate the Air Glyph to give this attack +4 to the effect roll\n".format(me))
		elif choice == 2:
			me.Mana -=3
			if drake and drake.markers[FireGlyphActive]>0 and drake != attacker:
				drake.markers[FireGlyphActive] = 0
				drake.markers[FireGlyphInactive] = 1
			else:
				mageStats.markers[FireGlyphActive] = 0
				mageStats.markers[FireGlyphInactive] = 1
			attacker.markers[FireGlyphActive] +=1
			rememberPlayerEvent("FireGlyphDeactivate",attacker.controller)
			notify("{} has chosen to pay 3 mana and deactivate the Fire Glyph to give this attack +2 dice\n".format(me))
	else:
		notify("You don't have enough Mana to pay for the buffs")
	
	return

def getStatusDict(card): #Will later expand to make this more useful
		if "Mage" in card.Subtype: return {'Damage' : card.controller.Damage, 'Mana' : card.controller.Mana}
		else: return {'Damage' : card.markers[Damage], 'Mana' : card.markers[Mana]}

def computeArmor(aTraitDict,attack,dTraitDict):
		baseArmor = (getStat(Card(dTraitDict['OwnerID']).Stats,'Armor') if 'OwnerID' in dTraitDict else 0)
		return max(baseArmor+dTraitDict.get('Armor',0)-attack.get('Traits',{}).get('Piercing',0),0)

def getRemainingLife(cTraitDict):
		card = Card(cTraitDict.get('OwnerID'))
		damage =  card.markers[Damage] + card.markers[Tainted]*3 + (card.controller.damage if "Mage" in card.Subtype else 0)
		life = (card.controller.life if "Mage" in card.Subtype else (getStat(card.Stats,'Life') + cTraitDict.get('Life',0) + cTraitDict.get('Innate Life',0)))
		if life: return max(life - damage,0)

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

def chanceToKill(aTraitDict,attack,dTraitDict):
	dice = attack.get('Dice',0)
	#armor = computeArmor(aTraitDict,attack,dTraitDict)
	defender = Card(dTraitDict['OwnerID'])
	life = getRemainingLife(dTraitDict)# if 'OwnerID' in dTraitDict else None))
	atkTraits = attack.get('Traits',{})
	if dice <= len(damageDict)-1 : distrDict = damageDict[dice]
	else: return 0
	if (dTraitDict.get('Incorporeal') and not atkTraits.get('Ethereal')): return (sum([nCr(dice,r)*(2**r)*(4**(dice-r)) for r in range(dice+1) if r >= life])/float(6**dice))
	return (sum([distrDict[key] for key in distrDict if computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict) >= life])/float(6**dice))

def computeDamageDistribution(aTraitDict,attack,dTraitDict): # dict: traitdict -> dict: attackdict -> dict: traitdict -> Option<dict<nat:float>>
	"""Returns a dictionary where each key is a nat associated with the probability of inflicting that amount of damage"""
	dice = attack.get('Dice',0)
	output = {}
	#1. For incorporeal opponents, a simple combinatorial calculation will suffice
	if (dTraitDict.get('Incorporeal') and not atkTraits.get('Ethereal')):
		for n in range(dice+1):
			output[n] = nCr(dice,n)*(2**n)*(4**(dice-n))/float(6**dice)
		return output

	#2. Otherwise, retrieve the distrdict; if there is none, return a NoneType
	distrDict = damageDict.get(dice)
	if not distrDict: return
	#23. Iterate over the numbers between 0 and 2*dice. For each number, compute the probability of that number occurring
	for n in range(dice*2+1):
		#4. Compute list of damages matching n
		matches = [distrDict[key] for key in distrDict if computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict) == n]
		output[n] = sum(matches)/float(6**dice)
	return output

def computeAggregateDamage(normal,critical,aTraitDict,attack,dTraitDict):
		defender = Card(dTraitDict["OwnerID"])
		atkTraits = attack.get('Traits',{})

		normalD = 0 if (dTraitDict.get('Resilient') or atkTraits.get('Critical Damage')) else normal
		criticalD = critical + (normal if atkTraits.get('Critical Damage') else 0)

		if "Mage" in defender.Subtype and [1 for c in table if c.isFaceUp and c.Name == "Veteran's Belt" and c.controller == defender.controller]: #handle veteran's belt in damage prediction
				reduction = min(criticalD,2)
				criticalD -= reduction
				normalD += reduction

		armor = computeArmor(aTraitDict,attack,dTraitDict)

		return (max( normalD - armor , 0 ) + criticalD)

def nCr(n,r):
	return factorial(n) / factorial(r) / factorial(n-r)

def getD12Probability(rangeStr,aTraitDict,attack,dTraitDict):# needs to be changed to take Tough/elemental into account
		d12Bonus = dTraitDict.get('Tough',0) + dTraitDict.get(attack.get('Type'),0)
		defender = Card(dTraitDict['OwnerID'])
		attacker = Card(aTraitDict['OwnerID'])
		#Giant Wolf Spider's attack
		if attacker.Name == "Giant Wolf Spider" and attack.get("Name") == "Poison Fangs" and dTraitDict.get("Restrained"): d12Bonus += 4
		if (attacker.Name == "Shoalsdeep Tidecaller" and int(getGlobalVariable("PlayerWithIni")) == me._id): d12Bonus += 4
		if attacker.Name == "Siren" and "Tides" in aTraitDict and ("Type" in attack.keys() and attack['Type']=="Hydro") and int(getGlobalVariable("PlayerWithIni")) == me._id : d12Bonus += 2
		if attacker.Name == "Temple of Light":
				eventList = getEventList("Round")
				for e in reversed(eventList):
						if "ToLX" in e[0]:
								d12Bonus += e[1]
								break

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
