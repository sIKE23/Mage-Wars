# -*- coding: utf-8 -*-
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
                  "Upkeep",
                  'Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic']
superlativeTraits = ["Regenerate",
                     "Aegis",
                     "Uproot",
                     "Dissipate"]

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
        if attacker and aTraitDict.get('Charge') and defender and getZoneContaining(attacker)==getZoneContaining(defender) and not specialCase and not hasAttackedThisTurn(attacker) and askChoice('Apply charge bonus to this attack?',['Yes','No'],["#01603e","#de2827"]) == 1: rememberCharge(attacker) #Let's try prompting for charge before opening menu, for a change.
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
        if defender and attacker and defender.Type in ['Creature','Conjuration','Conjuration-Wall','Mage']:
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
        atkTraits = attack.get('Traits',{})
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

getAttackList:
        computeAttack:
                getAdjustedDice
        getAttackTraitStr
        canDeclareAttack
"""

def getAttackList(card):
        """This returns an unmodified list of the card's attacks. It must be modified by <computeAttack> independently."""
        if not card or card.AttackBar == '': return [] #Return an empty list if passed a blank argument
        #Split up the attacks:
        attackKeyList0 = [attack.split(':\r\n') for attack in card.AttackBar.split(']\r\n')]
        isAttackSpell = (card.Type == 'Attack')
        attackList = []
        #Split 'or' clauses into multiple attacks. CURRENTLY ASSUMES that every attack has at most one OR clause. (!!!)
        attackKeyList1 = []
        for attack in attackKeyList0:
                name = (card.Name if isAttackSpell else attack[0])
                attributes = (attack[0] if isAttackSpell else attack[1]).split('] [')
                if isAttackSpell: attributes.append('Spell')
                options = []
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
                if isAttackSpell:
                        aDict['Range'] = [int(r) for r in card.Range.split('-')]
                        aDict['Cost'] = int(card.Cost) if card.Cost != 'X' else 0
                #Now we extract the attributes
                effectSwitch = False
                if "Heal" in attributes: continue
                for attribute in attributes: #Heal is too much bother for now. It will be easier to do in Q2 #aDict['EffectType'] = 'Heal'
                        attribute = attribute.strip('[]')
                        if attribute in ['Quick','Full'] : aDict['Action'] = attribute
                        elif 'Ranged' in attribute:
                                aDict['RangeType'] = attribute.split(':')[0]
                                if not isAttackSpell: aDict['Range'] = [int(r) for r in attribute.split(':')[1].split('-')]
                        elif 'Melee' in attribute:
                                aDict['RangeType'] = 'Melee'
                                aDict['Range'] = [0,0]
                        elif attribute in ['Damage Barrier','Passage Attack'] : aDict['RangeType'] = attribute
                        elif 'Cost' in attribute: aDict['Cost'] = (int(attribute.split('=')[1]) if attribute.split('=')[1] != 'X' else 0)
                        elif 'Dice' in attribute: aDict['Dice'] = (int(attribute.split('=')[1]) if attribute.split('=')[1] != 'X' else 0)
                        elif attribute in ['Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic'] : aDict['Type'] = attribute
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
                if card.Type == 'Mage':
                        if (c.Type in ['Equipment','Attack'] and card.controller == c.controller and (c.isFaceUp or c.Type=='Attack') and
                            (getAttachTarget(c) == card or (not canDeclareAttack(getAttachTarget(c)) if getAttachTarget(c) else True)) and
                            not c.markers[Disable]): attackList.extend(getAttackList(c))
                if c.Type == 'Enchantment' and getAttachTarget(c) == card and c.AttackBar: attackList.extend(getAttackList(c))
        
        if 'Familiar' or 'Spawnpoint' in card.Traits:
                for c in table:
                        if (c.Type == 'Attack' and card.controller == c.controller and getBindTarget(c)==card): attackList.extend(getAttackList(c))
        for a in attackList:
                if a.get('RangeType')!='Damage Barrier':
                        a['SourceID'] = card._id
                        a['OriginalAttack']['SourceID'] = card._id
        return attackList

def computeAttack(aTraitDict,attack,dTraitDict): 
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID')) if dTraitDict else None
        originalAttack = attack["OriginalAttack"]
        attack = deepcopy(attack["OriginalAttack"])
        attack["OriginalAttack"] = originalAttack
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
                                victim = Card(e[1][1]) if e[1][1] else None
                                if victim and victim.controller==attacker.controller and (victim.Type in ['Creature','Mage'] or ('Conjuration' in victim.Type and 'Holy' in victim.School)):
                                        localADict['Melee'] = localADict.get('Melee',0) + 2
                                        localADict['Piercing'] = localADict.get('Piercing',0) + 1
                                        break
        #Wounded prey
        if defender and defender.markers[WoundedPrey] and defender.Type == 'Creature' and attacker.controller != defender.controller and attacker.type in ['Mage','Creature'] and defender.markers[Damage] and dTraitDict.get('Living'): localADict['Melee'] = localADict.get('Melee',0) + 1
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
                elif (cName == "Lion Savagery"
                      and attacker == getAttachTarget(c)
                      and attack.get('RangeType') in ["Melee","Counterstrike"]): #Making the big assumption that the attacker did not earlier make a ranged attack if this one is melee; I know it overlooks some cases, but it should hold up until Q2, I think.
                        attack['Traits']['Piercing'] += 1
                elif (cName == 'Tooth & Nail' and #Global effects
                    'Animal' in attacker.Subtype and
                    attack.get('RangeType') in ['Melee','Counterstrike']): attack['Traits']['Piercing'] += 1
                elif c.controller == attacker.controller: #Friendly effects
                        aType = attack.get('Type')
                        if (attacker.Type == "Mage" and
                            ((cName == 'Dawnbreaker Ring' and aType == 'Light') or
                             (cName == 'Fireshaper Ring' and aType == 'Flame') or
                             (cName == 'Lightning Ring' and aType == 'Lightning'))):
                            localADict['Melee'] = localADict.get('Melee',0) + 1
                            localADict['Ranged'] = localADict.get('Ranged',0) + 1
        attack['Dice'] = getAdjustedDice(localADict,attack,dTraitDict)
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
                    or (e in ['Bleed','Stuck','Stun','Daze','Cripple','Weak','Slam'] and defender.Type not in ['Creature','Mage'])): illegalEffect = True #not sure about weak; can it affect conjurations?
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
        if attacker:
                if not hasAttackedThisTurn(attacker): #Once per attack sequence bonuses
                        if attack.get('RangeType') == 'Melee': attackDice += aTraitDict.get('Melee',0) + (aTraitDict.get('Charge',0) if hasCharged(attacker) else 0)
                        if attack.get('RangeType') == 'Ranged': attackDice += aTraitDict.get('Ranged',0)
                #No restriction on how many times may be applied
                if not atkTraits.get('Spell'): attackDice -= attacker.markers[Weak]
        if defender:
                attackDice -= dTraitDict.get('Aegis',0)
                attackDice += (aTraitDict.get('Bloodthirsty',0) if ((defender.markers[Damage] or (defender.Type=="Mage" and defender.controller.Damage))
                                                                    and (attacker and not hasAttackedThisTurn(attacker))
                                                                    and not 'Plant' in defender.subtype
                                                                    and defender.type in ['Creature','Mage']
                                                                    and not dTraitDict.get('Nonliving')) else 0)
                attackDice += dTraitDict.get(attack.get('Type'),0) #Elemental weaknesses/resistances
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
        if (card.Type in ['Creature','Mage'] or
            ('Conjuration' in card.Type and card.AttackBar != '') or
            computeTraits(card).get('Autonomous') or
            [1 for attack in getAttackList(card) if attack.get('RangeType')=='Damage Barrier'] != []): #Probably want better method for dealing with damage barriers.
                return True

############################################################################
######################		Dice Rolling		####################
############################################################################

def rollDice(dice):
        mute()
        global diceBank
	global diceBankD12
        mapDict = eval(getGlobalVariable('Map'))
	if not deckLoaded == True:
		notify("Please Load a Spellbook first. (Ctrl+L)")
		choiceList = ['OK','Load Blank Spellbook (not recommended)']
		colorsList = ['#FF0000','#0000FF']
		choice = askChoice("Please load a Spellbook first!", choiceList, colorsList)
		if choice == 2:
                        global blankSpellbook
                        blankSpellbook = True
                        onLoadDeck(me,[me.hand,table])
		return

	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me:
			c.delete()
	dieCardX, dieCardY = mapDict.get('DiceBoxLocation',(0,0))
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
	dieCard.anchor = (True)
	rnd(0,0)
	diceFrom = ""
        count = dice
        if (len(diceBank) < count): #diceBank running low - fetch more
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
		#debug("Random.org response code for damage dice roll: {}".format(random_org[1]))
		if random_org[1]==200: # OK code received:
			diceBank = random_org[0].splitlines()
			diceFrom = "from Random.org"
		else:
#			notify("www.random.org not responding (code:{}). Using built-in randomizer".format(random_org[1]))
			diceFrom = "from the native randomizer"
			while (len(diceBank) < 20):
				diceBank.append(rnd(0, 5))

	result = [0,0,0,0,0,0]
	for x in range(count):
		roll = int(diceBank.pop())
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
	if (len(diceBankD12) < d12DiceCount): #diceBank running low - fetch more
		d12 = webRead("http://www.random.org/integers/?num=100&min=0&max=11&col=1&base=10&format=plain&rnd=new")
		#debug("Random.org response code for effect roll: {}".format(d12[1]))
		if d12[1]==200: # OK code received:
			diceBankD12 = d12[0].splitlines()
			notify ("Using die from Random.org")
		else:
			notify ("Using die from the native randomizer")
			while (len(diceBankD12) < 100):
				diceBankD12.append(rnd(0, 11))

	effect = int(diceBankD12.pop()) + 1
	dieCard.markers[DieD12] = effect
	initiativeDone = getGlobalVariable("InitiativeDone")
	if initiativeDone:
		playSoundFX('Dice')
		time.sleep(1)
		notify("{} rolled {} normal damage, {} critical damage, and {} on the effect die".format(me,damNormal,damPiercing,effect))
                return (result,effect)                 
	else:
		setGlobalVariable("InitiativeDone", "True")
		iniRoll(effect)
		return None,None

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
        appendEventList('Turn',['Attack', [attacker._id,attacker._id,attack,damage]])

def rememberCharge(attacker):
        appendEventList('Round',['Charge', [attacker._id]])
        appendEventList('Turn',['Charge', [attacker._id]])

def rememberAbilityUse(card,number=0): #We can call the targeted version 'rememberTargetAbility use', or some such. This one is for untargeted abilities
        appendEventList('Round',['Ability', [card._id,number]])
        appendEventList('Turn',['Ability', [card._id,number]])


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
                if (dTraitDict.get("Incapacitated") and not "Autonomous" in c.Traits): continue
                if c.isFaceUp and (getAttachTarget(c) == defender or (defender.Type == 'Mage' and c.type in ['Enchantment','Equipment'] and not getAttachTarget(c) and not c.Target == 'Zone') and not c.markers[Disable]):
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
                     not (attacker.type in ['Creature','Mage'] and
                          aTraitDict.get('Flying') and
                          attack.get('RangeType') in ['Melee','Counterstrike']))): defenseList.remove(d)
        #We should also search for enchantment pseudo-defenses, like block.
        return defenseList

def computeDefense(aTraitDict,attack,dTraitDict,defense):
        source = Card(defense.get("Source"))
        if "Autonomous" in source.Traits: return dict(defense) #Autonomous equipment is not modified by anything
        modDefense = dict(defense)
        modDefense['Minimum'] = max(modDefense.get('Minimum',13)-dTraitDict.get('Defense',0),1)
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
        rememberDefenseUse(defender,defense)
        defense = computeDefense(aTraitDict,attack,dTraitDict,defense) #NOW we modify the defense
        defSource = Card(defense.get('Source'))
        notify("{} attempts to avoid the attack using {}!".format(defender,
                                                                 ('its innate defense' if defSource == defender else 'its defense from {}'.format(defSource))))
        
        damageRoll,effectRoll = rollDice(0)
        if effectRoll >= defense.get('Minimum',13):
               notify("{} succeeds in its defense attempt! Attack avoided!".format(defender))
               return defense
        else:
               notify("{} fails to defend itself...".format(defender))
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
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        if getSetting("BattleCalculator",True):
                if attacker.controller == me: declareAttackStep(aTraitDict,attack,dTraitDict)
                else: remoteCall(attacker.controller,'declareAttackStep',[aTraitDict,attack,dTraitDict])
        else:
                if attacker.controller == me: genericAttack(table)
                else:
                        remoteCall(attacker.controller,'whisper',['{} has disabled Battle Calculator, so generic dice menu will be used'])
                        remoteCall(attacker.controller,'genericAttack',[table])

def interimStep(aTraitDict,attack,dTraitDict,prevStepName,nextStepFunction,refusedReveal = False,damageRoll = None,effectRoll = None): #The time between steps during which attachments may be revealed. After both players pass, play proceeds to the next step.
        mute()
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
        if (otherPlayer == me) or (not selfAttached and refusedReveal):
                aTraitDict = computeTraits(attacker)
                dTraitDict = computeTraits(defender)
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
        else: remoteCall(otherPlayer,'interimStep',[aTraitDict,attack,dTraitDict,prevStepName,nextStepFunction,(not selfAttached),damageRoll,effectRoll])

def declareAttackStep(aTraitDict,attack,dTraitDict): #Executed by attacker
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        #If the defender is not flying, the attacker should lose the flying trait
        if attack.get('RangeType') == 'Counterstrike': notify("{} retaliates with {}!".format(attacker,attack.get('Name','a nameless attack')))
        elif attack.get('RangeType') == 'Damage Barrier': notify("{} is assaulted by the {} of {}!".format(defender,attack.get('Name','damage barrier'),attacker))
        else: notify("{} attacks {} with {}!".format(attacker,defender,attack.get('Name','a nameless attack')))
        #Check for daze
        if attacker.markers[Daze] and not attack.get('RangeType') == 'Damage Barrier':
                damageRoll,effectRoll = rollDice(0)
                if effectRoll < 7:
                        notify("{} is so dazed that it completely misses!".format(attacker))
                        interimStep(aTraitDict,attack,dTraitDict,'Declare Attack','additionalStrikesStep')
                        return
                else: notify("Though dazed, {} manages to avoid fumbling the attack.".format(attacker))
        interimStep(aTraitDict,attack,dTraitDict,'Declare Attack','avoidAttackStep')

def avoidAttackStep(aTraitDict,attack,dTraitDict): #Executed by defender
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        if attack.get('EffectType','Attack')=='Attack':
               if defenseQuery(aTraitDict,attack,dTraitDict)!=False: #Skip to additional strikes step if you avoided the attack
                       #Spiked buckler code here, perhaps?
                       rememberAttackUse(attacker,defender,attack['OriginalAttack'],0)
                       interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','additionalStrikesStep')
                       return
        interimStep(aTraitDict,attack,dTraitDict,'Avoid Attack','rollDiceStep')

def rollDiceStep(aTraitDict,attack,dTraitDict): #Executed by attacker
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        dice = attack.get('Dice',-1)
        if dice < 0:
                notify('Error: invalid attack format - no dice found')
                return
        damageRoll,effectRoll = rollDice(dice)
        interimStep(aTraitDict,attack,dTraitDict,'Roll Dice','damageAndEffectsStep',False,damageRoll,effectRoll)

def damageAndEffectsStep(aTraitDict,attack,dTraitDict,damageRoll,effectRoll): #Executed by defender
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        damage = damageReceiptMenu(aTraitDict,attack,dTraitDict,damageRoll,effectRoll)
        rememberAttackUse(attacker,defender,attack['OriginalAttack'],damage) #Record that the attack was declared, using the original attack as an identifier
        interimStep(aTraitDict,attack,dTraitDict,'Damage and Effects','additionalStrikesStep')

def additionalStrikesStep(aTraitDict,attack,dTraitDict): #Executed by attacker
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        strikes = 1
        atkTraits = attack.get('Traits',{})
        if atkTraits.get('Doublestrike'): strikes = 2
        if atkTraits.get('Triplestrike'): strikes = 3
        if attacker.Name == 'Wall of Thorns':
                level = (6 if defender.type == 'Mage' else int(defender.Level)) #Mages really should have level in their xml. But we don't need to worry about this; the spellDictionary will render this moot.
                strikes = (level - 1 if level > 1 else 1)
        if timesHasUsedAttack(attacker,attack['OriginalAttack']) < strikes: declareAttackStep(aTraitDict,attack,dTraitDict)
        else: interimStep(aTraitDict,attack,dTraitDict,'Additional Strikes','damageBarrierStep')

def damageBarrierStep(aTraitDict,attack,dTraitDict): #Executed by defender
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        deathFlag = False
        #Check for death here
        if getRemainingLife(dTraitDict) == 0:
                deathPrompt(dTraitDict,attack,aTraitDict)
                deathFlag = True
        #But damage barriers can still happen after death!
        if attack.get('RangeType') == 'Melee': #Need to add: and attack *was 'successful'*
                attackList = getAttackList(defender)
                dBarrier = None
                for a in attackList:
                        if a.get('RangeType') == 'Damage Barrier':
                                dBarrier = a
                                break
                if dBarrier:
                        bTraitDict = computeTraits(Card(dBarrier.get('SourceID',defender._id)))
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
                        interimStep(dTraitDict,counterAttack,aTraitDict,'Counterstrike','declareAttackStep')
        defender.markers[Guard] = 0
        interimStep(aTraitDict,attack,dTraitDict,'Counterstrike','attackEndsStep')

def attackEndsStep(aTraitDict,attack,dTraitDict): #Executed by attacker
        mute()
        attacker = Card(aTraitDict.get('OwnerID'))
        defender = Card(dTraitDict.get('OwnerID'))
        setEventList('Turn',[]) #Clear the turn event list

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
        atkTraits = attack.get('Traits',{})
        #If it is healing, we heal and then end the attack, since it is not an attack.
        if False and attack.get('EffectType','Attack')=='Heal':
                healingAmt = min(sum([{0:0,1:0,2:1,3:2,4:1,5:2}.get(i,0)*roll[i] for i in range(len(roll))]),getStatusDict(defender).get('Damage',0))
                if healingAmt > 0: healingQuery(dTraitDict,
                                                'Heal {} for {} damage?'.format(defender.name,str(healingAmt)),
                                                healingAmt,
                                                "{} heals {} for {} damage!".format(attacker.name,defender.name,'{}'))
                else: notify("{} attempts to heal {} but fails.".format(attacker.name,defender.name))
                return 0 #Uh-oh...healing is treated as an attack for abilities that remember that. No worries; this will become irrelevant it Q2, and does not matter now.
        
        expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
        actualDmg,actualEffect = computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict)
        if defender.markers[VoltaricON] and actualDmg:#Voltaric Shield
                notify("The Voltaric Shield absorbs {} points of damage!".format(str(min(actualDmg,3))))
                actualDmg = max(actualDmg-3,0)
                defender.markers[VoltaricON] = 0
                defender.markers[VoltaricOFF] = 1
        dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if actualDmg else 0) #Prep for mana drain
        choice = askChoice('{}\'s attack will inflict {} damage {}on {}.{} Apply these results?'.format(attacker.Name,
                                                                                                          actualDmg,
                                                                                                          ('and an effect ({}) '.format(actualEffect) if actualEffect else ''),
                                                                                                          defender.Name,
                                                                                                          (' It will also drain {} mana from {}.'.format(
                                                                                                                  str(dManaDrain),defender.controller.name) if dManaDrain else '')),
                           ['Yes','No'],
                           ["#01603e","#de2827"])
        if choice == 1:
                applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
                return actualDmg #for remembering damage. Pretty crude; We'll come up with a better alternative in Q2
        else:
                notify('{} has elected not to apply auto-calculated battle results'.format(me))
                whisper('(Battle calculator not giving the right results? Report the bug to us so we can fix it!)')

def applyDamageAndEffects(aTraitDict,attack,dTraitDict,damage,rawEffect): #In general, need to adjust functions to accomodate partially or fully untargeted attacks.
        attacker = Card(aTraitDict.get('OwnerID',''))
        defender = Card(dTraitDict.get('OwnerID',''))
        atkTraits = attack.get('Traits',{})
        expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
        conditionsList = ['Bleed','Burn','Corrode','Cripple','Damage','Daze','Rot','Slam','Sleep','Stuck','Stun','Tainted','Weak']
        effectsInflictDict = {'Damage' : "suffers 1 point of direct damage! (+1 Damage)",
                              'Bleed' : 'bleeds from its wounds! (+1 Bleed)',
                              'Burn' : 'is set ablaze! (+1 Burn)',
                              'Corrode' : 'corrodes! (+1 Corrode)',
                              'Cripple' : 'is crippled! (+1 Cripple)',
                              'Daze' : 'is dazed! (+1 Daze)',
                              'Rot' : 'rots! (+1 Rot)',
                              'Slam' : 'is slammed to the ground! (+1 Slam)',
                              'Sleep' : 'falls fast alseep! (+1 Sleep)',
                              'Stuck' : 'is stuck fast! (+1 Stuck)',
                              'Stun' : 'is stunned! (Stun)',
                              'Tainted' : "'s wounds fester! (+1 Tainted)",
                              'Weak' : 'is weakened! (+1 Weak)',
                              'Snatch' : 'is snatched toward {}! (Snatch)'.format(attacker),
                              'Push' : 'is pushed away from {}! (Push 1)'.format(attacker),
                              'Taunt' : 'wants to attack {}! (Taunt)'.format(attacker)}

        #Prep for Vampirism
        aDamage = getStatusDict(attacker).get('Damage',0)
        drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0))

        if defender.Type == 'Mage': defender.controller.Damage += damage
        else: defender.markers[Damage] += damage
        notify("{} inflicts {} damage on {}{} average roll)".format(attacker,
                                                                    str(damage),
                                                                    defender,
                                                                    ('! (an above' if damage >= expectedDmg else '... (a below')))
        #Mana Drain - Long term, will want a centralized function to adjust damage/mana of a card so we can take into account things like Mana Prism
        dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if damage else 0)
        defender.controller.Mana -= dManaDrain
        if dManaDrain: notify("{} drains {} mana from {}!".format(attacker,str(dManaDrain),defender.controller.name))
        #Vampirism
        if (atkTraits.get('Vampiric') and drainableHealth and
            (dTraitDict.get('Living') or not dTraitDict.get('Nonliving')) and defender.Type in ['Creature','Mage'] > 0): #Long term, give all creatures Living trait by default, eliminate nonliving condition
                if attacker.controller == me: healingQuery(aTraitDict,
                                                           'Drain {} health from {}?'.format(drainableHealth,defender.name),
                                                           drainableHealth,
                                                           "{} drains {} health from {}!".format(attacker.name,'{}',defender.name))
                else: remoteCall(attacker.controller,'healingQuery',[aTraitDict,
                                                                   'Drain {} health from {}?'.format(drainableHealth,defender.name),
                                                                   drainableHealth,
                                                                   "{} drains {} health from {}!".format(attacker.name,'{}',defender.name)])
        #Finally, apply conditions
        effects = ([rawEffect.split(' ')[1],rawEffect.split(' ')[1]] if '2' in rawEffect else rawEffect.split(' & ')) if rawEffect else []
        for e in effects:
                if e in conditionsList:
                        if e=="Damage" and defender.Type == "Mage": defender.controller.damage += 1
                        else: defender.markers[eval(e)]+=1
                notify('{} {}'.format(defender.Name,effectsInflictDict.get(e,'is affected by {}!'.format(e))))

def deathPrompt(cardTraitsDict,attack={},aTraitDict={}):
        card = Card(cardTraitsDict.get('OwnerID'))
        choice = askChoice("{} appears to be destoyed. Accept destruction?".format(card.name),
                           ["Yes","No"],
                           ["#01603e","#de2827"])
        if choice == 1:
                deathMessage(cardTraitsDict,attack,aTraitDict)
                if ((attack.get('Traits',{}).get('Devour') and cardTraitsDict.get("Corporeal") and card.Type in ['Creature','Mage']) or
                    card.markers[Zombie]): obliterate(card)
                else: discard(card)
        else: notify("{} does not accept the destruction of {}.".format(me,card))

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
        armor = computeArmor(aTraitDict,attack,dTraitDict)
        atkTraits = attack.get('Traits',{})
        if dTraitDict.get('Incorporeal'): return (roll[2] + roll[4] + ((2*(roll[3]+roll[5])) if atkTraits.get('Ethereal') else 0)),computeEffect(effectRoll,aTraitDict,attack,dTraitDict)
        normal = roll[2] + 2*roll[3]
        critical = roll[4] + 2*roll[5]
        return (max((0 if (dTraitDict.get('Resilient') or atkTraits.get('Critical Damage')) else normal) - armor,0) +
                critical + (normal if atkTraits.get('Critical Damage') else 0),
                computeEffect(effectRoll,aTraitDict,attack,dTraitDict))

def computeEffect(effectRoll,aTraitDict,attack,dTraitDict):
        modRoll = effectRoll + dTraitDict.get('Tough',0) + dTraitDict.get(attack.get('Type'),0)
        defender = Card(dTraitDict['OwnerID'])
        attacker = Card(aTraitDict['OwnerID'])
        #Giant Wolf Spider's attack
        if attacker.Name == "Giant Wolf Spider" and attack.get("Name") == "Poison Fangs" and (dTraitDict.get("Restrained") or dTraitDict.get("Incapacitated")): modRoll += 4
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
                if card.Type == 'Mage':
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
        traitDict = {}
        markers = card.markers
        name = card.name
        controller = card.controller
        subtype = card.subtype
        cardType = card.type
        rawTraitsList = ({'Mage' : ['Living','Corporeal'],
                          'Creature' : ['Living','Corporeal'],
                          'Conjuration' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity'],
                          'Conjuration-Wall' : ['Nonliving','Corporeal','Unmovable','Psychic Immunity']}.get(cardType,[])) #Get innate traits depending on card type
        append = rawTraitsList.append
        extend = rawTraitsList.extend
        remove = rawTraitsList.remove
        listedTraits = card.Traits.split(', ')
        if 'Living' in listedTraits and 'Nonliving' in rawTraitsList: remove('Nonliving')
        elif 'Nonliving' in listedTraits and 'Living' in rawTraitsList: remove('Living')
        if 'Incorporeal' in listedTraits and 'Corporeal' in rawTraitsList: remove('Corporeal')
        extend(listedTraits)
        adraAbility = True
        adraEnemy = bool([c for c in table if c.name=="Adramelech Warlock" and c.controller != controller])
        for c in table: #scan cards in table for bonuses. We want to minimize iterations, so we'll scan only once.
                cName = c.name
                cController = c.controller
                cSubtype = c.subtype
                cType = c.type
                if cType == 'Mage' and cController == controller: traitDict['MageID'] = c._id #Each card knows which mage controls it.
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
                                                debug('Triggered')
                                if cName == "Sentinel of V'tar":
                                        for o in table:
                                                isWithOrb = False
                                                if (o.name == "V'tar Orb" and
                                                    getZoneContaining(c) == getZoneContaining(card)): isWithOrb = True
                                                if isWithOrb:
                                                        extend(['Unmovable','Anchored'])
                                                        if markers[Guard]: extend(['Armor +2','Melee +1'])
                                elif cName == "Maim Wings": rawTraitsList = [t for t in list(rawTraitsList) if t != 'Flying']
                                
                                        
                        # Get traits from cards in this zone
                        if getZoneContaining(c) == getZoneContaining(card): #get traits from cards in this zone.
                                #Note - we need to optimize the speed here, so we'll use if branching even though we are hardcoding specific cases.
                                if (name == 'Skeelax, Taunting Imp'
                                    and c.markers[Burn]): append('Regenerate 2') #and phase = upkeep, but I don't think this matters for now.
                                elif (name in ['Sslak, Orb Guardian','Usslak, Orb Guardian'] and
                                    cName == "V'tar Orb"): extend(['Unmovable','Anchored'])
                                if cType == 'Enchantment':
                                        if (cName == 'Fortified Position' and
                                            cardType in ['Creature','Mage'] and
                                            'Corporeal' in rawTraitsList): append('Armor +2')
                                        elif (cName == 'Sacred Ground' and
                                            cController == controller and
                                            cardType in ['Creature','Mage'] and
                                            'Living' in rawTraitsList): append('Aegis 1')
                                        elif (cName == 'Astral Anchor' and
                                            cardType in ['Creature','Mage']): append('Anchored')
                                        elif (cName == 'Standard Bearer' and
                                            cController == controller and
                                            getAttachTarget(c) != card and
                                            cardType in ['Creature','Mage']): extend(['Melee +1','Armor +1'])
                                elif cType == 'Conjuration':
                                        if (name == 'Guard Dog'
                                            and cController == controller
                                            and not getAttachTarget(c)): append('Vigilant')
                                        if (cName == 'Mohktari, Great Tree of Life' and
                                            cController == controller and
                                            cardType in ['Creature','Mage'] and
                                            'Living' in rawTraitsList): append('Regenerate 2')
                                        elif (cName == 'Raincloud' and
                                              cController == controller and
                                              cardType in ['Creature','Mage','Conjuration']): extend(['Regenerate 1','Flame -2','Acid -2'])
                                elif cType == 'Creature':
                                        if (cName == 'Highland Unicorn' and
                                              cController == controller and
                                              cardType in ['Creature','Mage'] and
                                              'Living' in rawTraitsList): append('Regenerate 1')
                                        elif (cName == 'Makunda' and
                                              cController == controller and
                                              c != card and
                                              cardType in ['Creature','Mage'] and
                                              'Cat' in subtype): append('Piercing +1') #Long term, need to indicate that it is only melee attacks. For now, should not matter since no cats have ranged attacks.
                                        #Mort?
                                        elif (cName == 'Redclaw, Alpha Male' and
                                              c != card and
                                              cardType in ['Creature','Mage'] and
                                              'Canine' in subtype): extend(['Armor +1','Melee +1'])
                                        elif (cName == 'Sardonyx, Blight of the Living' and
                                              cardType in ['Creature','Mage'] and
                                              'Living' in rawTraitsList): append('Finite Life')
                                        #Victorian Gryffin, but I don't feel like adding it right now
                                elif cType == 'Incantation': pass
                                elif (cType == 'Mage' and cController == controller): #Effects when creature is in same zone as controlling mage
                                        if name == 'Goran, Werewolf Pet': append('Bloodthirsty +1')
                                        if markers[Pet] and 'Animal' in subtype: append('Melee +1')
                        if cardType == 'Mage':
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
                                                    'Animal' in aSubtype
                                                    and cardType in ['Creature','Mage']):
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
                        elif (cName == 'Armory' and cController == controller and 'Soldier' in subtype): extend(['Armor +1','Piercing +1'])
                        elif (cName == 'Rajan\'s Fury' and 'Animal' in subtype): append('Charge +1')
                        elif (cName == 'Gate to Hell' and cController == controller and 'Demon' in subtype): append('Melee +1')
                        elif (cName == 'Mordok\'s Obelisk' and cardType == 'Creature'): append('Upkeep +1')
                        elif (cName == 'Deathlock' and cardType in ['Creature','Mage','Conjuration','Conjuration-Wall']): append('Finite Life')
                        elif (cName == 'Etherian Lifetree' and 'Living' in rawTraitsList and c != card): append('Innate Life +2')
                        elif (cName == 'Rolling Fog'): append('Obscured')
                        elif (cName == 'Harshforge Monolith' and cardType == 'Enchantment' and cardGetDistance(c,card)<=1): append('Upkeep +1')
                        elif (cName == 'Gravikor' and cardType == 'Creature' and cardGetDistance(c,card)<=2): append('Non-Flying')
                        #>>Altar of Skulls<<
                        #Incantations
                        elif (cName == 'Akiro\'s Battle Cry' and cController == controller and 'Soldier' in subtype): extend(['Charge +2,Fast'])
                        elif (cName == 'Call of the Wild' and cController == controller and 'Animal' in subtype): append('Melee +1')
                        elif (cName == 'Zombie Frenzy' and ('Zombie' in subtype or markers[Zombie])):
                                rawTraitsList = [t for t in rawTraitsList if t not in ['Lumbering','Pest','Slow']]
                                extend(['Fast','Bloodthirsty +1'])
        
        if markers[Melee]: append('Melee +{}'.format(str(markers[Melee])))
        if markers[Ranged]: append('Ranged +{}'.format(str(markers[Ranged])))
        if markers[Armor]: append('Armor +{}'.format(str(markers[Armor])))
        if markers[Growth]: extend(['Life +{}'.format(str(3*markers[Growth])),'Melee +{}'.format(str(markers[Growth]))])
        if markers[Corrode]: append('Armor -{}'.format(str(markers[Corrode])))
        if markers[Guard]: extend(['Counterstrike','Non-Flying'])
        if markers[Sleep] or markers[Stun]: append('Incapacitated')
        if markers[Zombie] :
                extend(['Psychic Immunity','Slow','Nonliving','Bloodthirsty +0'])
                remove('Living')
                #Also should add undead,zombie subtypes, but no way to do that without the spellDictionary.
        if markers[Stuck] : extend(['Restrained','Unmovable'])
        if markers[Daze]: append('Defense -{}'.format(str(markers[Daze])))
        
        if markers[Pet] and 'Animal' in subtype: extend(['Melee +1','Armor +1','Life +3'])
        if markers[BloodReaper] and 'Demon' in subtype: append('Bloodthirsty +2')
        if markers[EternalServant] and 'Undead' in subtype: append('Piercing +1')
        if markers[Treebond] and 'Tree' in subtype: extend(['Innate Life +4','Armor +1','Lifebond +2'])
        if markers[Veteran] and 'Soldier' in subtype: extend(['Armor +1','Melee +1'])
        if markers[HolyAvenger] and 'Holy' in card.School and not 'Legendary' in card.Traits: append('Life +5')

                #Harshforge monolith

        if 'Unstoppable' in rawTraitsList: extend(['Unmovable','Uncontainable'])
        if 'Incorporeal' in rawTraitsList: extend(['Nonliving','Burnproof','Uncontainable'])
        if 'Nonliving' in rawTraitsList: extend(['Poison Immunity','Finite Life'])
        if 'Rooted' in rawTraitsList: extend(['Unmovable','Non-Flying'])
        if 'Restrained' in rawTraitsList: append('Defense -2')

        if (name == 'Gargoyle Sentry' and markers[Guard]): extend(['Armor +3','Tough -3'])
        elif (name == 'Dwarf Panzergarde' and markers[Guard]): extend(['Defense +3'])
        #Dragonclaw wolverine, but we need rage markers for its ability.

        if 'Non-Flying' in rawTraitsList: rawTraitsList = [t for t in list(rawTraitsList) if t != 'Flying']

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

def getStatusDict(card): #Will later expand to make this more useful
        if card.Type == 'Mage': return {'Damage' : card.controller.Damage, 'Mana' : card.controller.Mana}
        else: return {'Damage' : card.markers[Damage], 'Mana' : card.markers[Mana]}

def computeArmor(aTraitDict,attack,dTraitDict):
        baseArmor = (getStat(Card(dTraitDict['OwnerID']).Stats,'Armor') if 'OwnerID' in dTraitDict else 0)
        return max(baseArmor+dTraitDict.get('Armor',0)-attack.get('Traits',{}).get('Piercing',0),0)

def getRemainingLife(cTraitDict):
        card = Card(cTraitDict.get('OwnerID'))
        life = getStat(card.Stats,'Life') + cTraitDict.get('Life',0) + cTraitDict.get('Innate Life',0) #Preventing life gain is handled when traits are computed, not here
        if life: return max(life - card.markers[Damage] - (card.markers[Tainted]*3),0)

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
        armor = computeArmor(aTraitDict,attack,dTraitDict)
        defender = Card(dTraitDict['OwnerID'])
        life = getRemainingLife(dTraitDict)# if 'OwnerID' in dTraitDict else None))
        atkTraits = attack.get('Traits',{})
        if dice <= len(damageDict)-1 : distrDict = damageDict[dice]
        else: return
        if (dTraitDict.get('Incorporeal') and not atkTraits.get('Ethereal')): return (sum([nCr(dice,r)*(2**r)*(4**(dice-r)) for r in range(dice+1) if r >= life])/float(6**dice))
        return (sum([distrDict[key] for key in distrDict if computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict) >= life])/float(6**dice))

def computeAggregateDamage(normal,critical,aTraitDict,attack,dTraitDict):
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
