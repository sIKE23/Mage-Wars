from math import factorial
"""
Mage Wars Attacks Module

This module contains the functions relating to dice rolling and battle computations
"""

############################################################################
######################		Dice Rolling		####################
############################################################################

def getRollDice(dice):
        mute()
        global diceBank
	global diceBankD12
	global hasRolledIni
	global myIniRoll
	global dieCardX
	global dieCardY
	global dieCard2X
	global dieCard2Y
	table.create("d86b16a6-218a-4363-a408-599d3ef4a0b3", (dieCardX + -60), (dieCardY + -25))

	if not deckLoaded == True:
		notify("Please Load a Spellbook first.")
		choiceList = ['OK']
		colorsList = ['#FF0000']
		choice = askChoice("Please load a Spellbook first!", choiceList, colorsList)
		return

	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me:
			c.delete()
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
	dieCard2 = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCard2X, dieCard2Y) #dice field 2
	diceFrom = ""
        count = dice
        if (len(diceBank) < count): #diceBank running low - fetch more
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code for damage dice roll: {}".format(random_org[1]))
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
	debug("diceRoller result: {}".format(result))
	notify("{} rolls {} attack dice {}".format(me,count,diceFrom))

	damPiercing = result[4] + 2* result[5]
	damNormal = result[2] + 2* result[3]
	dieCard.markers[attackDie[0]] = result[0]+result[1] #blanks
	dieCard.markers[attackDie[2]] = result[2] #1
	dieCard.markers[attackDie[3]] = result[3] #2
	dieCard2.markers[attackDie[4]] = result[4] #1*
	dieCard2.markers[attackDie[5]] = result[5] #2*

	d12DiceCount = 1
	if (len(diceBankD12) < d12DiceCount): #diceBank running low - fetch more
		d12 = webRead("http://www.random.org/integers/?num=100&min=0&max=11&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code for effect roll: {}".format(d12[1]))
		if d12[1]==200: # OK code received:
			diceBankD12 = d12[0].splitlines()
			notify ("Using die from Random.org")
		else:
			notify ("Using die from the native randomizer")
			while (len(diceBankD12) < 100):
				diceBankD12.append(rnd(0, 11))

	effect = int(diceBankD12.pop()) + 1
	dieCard2.markers[DieD12] = effect

	if hasRolledIni:
		playSoundFX('Dice')
		time.sleep(1)
		notify("{} rolled {} normal damage, {} critical damage, and {} on the effect die".format(me,damNormal,damPiercing,effect))
                return (result,effect)                 
	else:
		hasRolledIni = True
		iniRoll(effect)
		return None,None

############################################################################
######################		    Menus		####################
############################################################################

def diceRollMenu(attacker = None,defender = None):
        mute()
        aTraitDict = (computeTraits(attacker) if attacker else {})
        dTraitDict = (computeTraits(defender) if defender else {})
        attackList = getAttackList(attacker) if attacker else []
        choiceText,choices = "Roll how many red dice?",[str(i+1) for i in range(7)]
        #Suppose there is an attacker with at least one attack:
        if (attacker and attackList):
                choiceText = "Use which attack?"
                choices = []
                for attack in attackList:
                        modAttack = computeAttack(aTraitDict,attack,dTraitDict)
                        modDice = getAdjustedDice(aTraitDict,attack,dTraitDict)
                        traits = getAttackTraitStr(attack['Traits'])
                        expDam = str(round(expectedDamage(aTraitDict,attack,dTraitDict),1)) if defender else ''
                        killCh = str(round(chanceToKill(aTraitDict,attack,dTraitDict)*100,1)) if defender else ''
                        effectList = ['{} ({}%)'.format(effect[1], str(round(getD12Probability(effect[0],aTraitDict,attack,dTraitDict)*100,1))) for effect in modAttack['d12']] if modAttack['d12'] else ''
                        choice = ("{} ({})".format(modAttack['Name'],str(modDice)).center(68,' ')+
                                  ('\n'+', '.join(traits) if traits else '')+
                                  ('\n'+', '.join(effectList) if effectList != '' else '')+
                                  ('\nExpected damage: {} | Kill chance: {}%'.format(expDam,killCh) if defender else ''))
                        choices.append(choice)
                if defender and defender.Type in ['Creature','Conjuration','Mage']: choiceText = "Attacking {} with {}. Use which attack?".format(defender.name,attacker.name)
        #Then, suppose not (or suppose the indicated attacker has no attack list)
        elif defender and defender.Type in ['Creature','Conjuration','Mage']:
                choices = (['{}: Expected damage: {} | Kill chance: {}%'.format(str(i+1),
                        round(expectedDamage({},{'Dice':i+1},dTraitDict),1),
                        round(chanceToKill({},{'Dice':i+1},dTraitDict)*100,1)) for i in range(7)])  
        colors = ['#de2827' for i in range(len(choices))]
        choices.extend(['Other Dice Amount','Cancel Attack'])
        colors.extend(["#171e78","#c0c0c0"])
        count = askChoice(choiceText, choices, colors)
        if count == 0 or count == len(choices): return {}
        elif count < len(choices)-1:
                if (attacker and attackList): return attackList[count-1]#getAdjustedDice(aTraitDict,attackList[count-1],dTraitDict),attackList[count-1]['Traits']
                else: return {'Dice' : count}#count,[]
        elif count == len(choices)-1:
                if attacker: return diceRollMenu(None,defender)
                else: #Revert to standard input menu. Default value is the last one you entered.
                        dice = min(askInteger("Roll how many red dice?", getSetting('lastStandardDiceRollInput',8)),50)
                        setSetting('lastStandardDiceRollInput',dice)
                        return {'Dice' : dice}#dice,[] #max 50 dice rolled at once

def damageRecieptMenu(attacker,defender,damage,effect):
        choices = []

def revealAttachmentQuery(attacker,defender):
        recurText = ''
        while True:
                aList=[c for c in getAttachments(defender) if c.controller == me and not c.isFaceUp and c.Type == 'Enchantment']
                aList.extend([c for c in getAttachments(attacker) if c.controller == me and not c.isFaceUp and c.Type == 'Enchantment'])
                if not aList: return
                options = ['{}\n{}\n{}'.format(c.Name.center(68,' '),(('('+getAttachTarget(c).Name+')').center(68,' ')),c.Text.split('\n\t')[0]) for c in aList]
                colors = ['#CC6600' for i in options] #Orange
                options.append('I would not like to reveal an enchantment.')
                colors.append("#de2827")
                choice = askChoice('Would you like to reveal an enchantment?',options,colors)
                if choice == len(options): return
                castSpell(aList[choice-1])
                recurText = 'another '
                        
############################################################################
######################		Data Retrieval		####################
############################################################################

additiveTraits = ["Melee","Ranged",
                  "Armor","Life","Innate Life","Channeling",
                  "Tough",
                  "Charge",
                  "Bloodthirsty",
                  "Piercing",
                  "Mana Drain",
                  "Mana Transfer",
                  'Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic']
superlativeTraits = ["Regenerate",
                     "Aegis",
                     "Uproot"]

def getAttackList(card):
        if not card or card.AttackBar == '': return {} #Return an empty list if passed a blank argument
        rawData = card.AttackBar
        #First, split up the attacks:
        attackKeyList = [attack.split(':\r\n') for attack in rawData.split(']\r\n')]
        isAttackSpell = (len(attackKeyList[0]) == 1)
        attackList = []
        for attack in attackKeyList:
                name = (card.name if isAttackSpell else attack[0])
                aDict = {'Name':name,
                         'Action':None,
                         'Range':[None,None],
                         'Dice':0,
                         'Type':None,
                         'd12':[],
                         'Traits': {}
                         }
                attributes = (attack[0] if isAttackSpell else attack[1]).split('] [')
                #Now we extract the attributes
                effectSwitch = False
                hasDiceValue = False
                for attribute in attributes:
                        attribute = attribute.strip('[]')
                        if attribute in ['Quick','Full'] : aDict['Action'] = attribute
                        elif 'Ranged' in attribute: aDict['Range'] = attribute.split(':')
                        elif attribute == 'Melee' : aDict['Range'] = ['Melee','0-0']
                        elif 'Dice' in attribute:
                                aDict['Dice'] = int(attribute[-1])
                                hasDiceValue = True
                        elif attribute in ['Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic'] : aDict['Type'] = attribute
                        elif attribute =='d12' : effectSwitch = True
                        elif effectSwitch:
                                options = attribute.split('; ')
                                aDict['d12'] = [o.split(' = ') for o in options]
                                effectSwitch = False
                        else:
                                tPair = traitParser(attribute)
                                if tPair[0] in additiveTraits: aDict['Traits'][tPair[0]] = aDict.get(tPair[0],0)+tPair[1]
                                elif tPair[0] in superlativeTraits: aDict['Traits'][tPair[0]] = max(aDict.get(tPair[0],0),tPair[1])
                                else: aDict['Traits'][tPair[0]] = tPair[1]
                if hasDiceValue: attackList.append(aDict)
        if card.Type == 'Mage': #find all attacks granted by equipment. Assume all controlled equipment is equipped to mage.
                for c in table:
                        if (c.Type == 'Equipment' and card.controller == c.controller): attackList.extend(getAttackList(c))
        return attackList

def traitParser(traitStr):
        """Reads a single trait and returns it in a standardized, parsed form. Should be used for everything that needs to read traits as information.
        Each trait is returned as a list with 1-2 values, with the first value being the identifier and the second being the value. The computeTraits
        function will take this list and output a dictionary, which will be the standard format for readable traits."""
        formattedTrait = [traitStr,True]
        if " +" in traitStr and traitStr.split(' +')[0] in additiveTraits: formattedTrait = [traitStr.split(' +')[0], int(traitStr.split(' +')[1])]
        elif " -" in traitStr and traitStr.split(' -')[0] in additiveTraits: formattedTrait = [traitStr.split(' ')[0], int(traitStr.split(' ')[1])]
        elif " Immunity" in traitStr: formattedTrait = ["Immunity",traitStr.split(' ')[0]]
        for s in superlativeTraits:
                if s in traitStr: formattedTrait = traitStr.split(' ')
        return formattedTrait

def computeTraits(card):
        """This is the centralized function that reads all traits possessed by a card. Do NOT compute traits anywhere else, ONLY compute them here.
        It returns a dictionary of traits. This function will end up being quite long and complex.It works together with traitParser. Standard format
        for traits is a dictionary."""
        traitDict = {}
        rawTraitsList = card.Traits.split(', ')
        for c in getAttachments(card): #Get bonuses from attached enchantments
                if c.type == 'Enchantment':
                        rawText = c.text.split('\n\t[')
                        traitsGranted = ([t.strip('[]') for t in rawText[1].split('] [')] if len(rawText) == 2 else [])
                        rawTraitsList.extend(traitsGranted)       
        if card.Type == 'Mage':
                for c in table:
                        if c.Type == 'Equipment' and c.controller == card.controller:
                                rawText = c.text.split('\n\t[')
                                traitsGranted = ([t.strip('[]') for t in rawText[1].split('] [')] if len(rawText) == 2 else [])
                                rawTraitsList.extend(traitsGranted)                    
        rawTraitsList.append('Melee +{}'.format(str(card.markers[Melee])))
        rawTraitsList.append('Ranged +{}'.format(str(card.markers[Ranged])))
        rawTraitsList.append('Armor +{}'.format(str(card.markers[Armor])))
        rawTraitsList.extend(['Life +{}'.format(str(3*card.markers[Growth])),'Melee +{}'.format(str(card.markers[Growth]))])
        rawTraitsList.append('Armor -{}'.format(str(card.markers[Corrode])))
        if card.markers[Pet] and 'Animal' in card.Subtype: rawTraitsList.extend(['Melee +1','Armor +1','Life +3'])
        if card.markers[BloodReaper] and 'Demon' in card.Subtype: rawTraitsList.append('Bloodthirsty +2')
        if card.markers[Eternal_Servant] and 'Undead' in card.Subtype: rawTraitsList.append('Piercing +1')
        if card.markers[Treebond] and 'Tree' in card.Subtype: rawTraitsList.extend(['Innate Life +4','Armor +1','Lifebond +2'])
        if card.markers[Veteran] and 'Soldier' in card.Subtype: rawTraitsList.extend(['Armor +1','Melee +1'])
        for rawTrait in rawTraitsList:
                formTrait = traitParser(rawTrait)
                if formTrait[0] in additiveTraits: traitDict[formTrait[0]] = traitDict.get(formTrait[0],0) + (0 if formTrait[1] == '-' else int(formTrait[1]))
                elif formTrait[0] in superlativeTraits: traitDict[formTrait[0]] = max(traitDict.get(formTrait[0],0),int(formTrait[1]))
                else: traitDict[formTrait[0]] = True
        debug(card.name+' traits = '+str(traitDict))
        traitDict['OwnerID'] = card._id #Tag the dictionary with its owner's ID in case we need to extract it later (extracting the owner is MUCH faster than extracting the dictionary)
        return traitDict

"""
Trait and Attack Adjustments

The following functions evaluate the adjusted traits and attacks of a card, given the
state of the game and the cards attached to it.
"""
def getAdjustedDice(aTraitDict,attack,dTraitDict):
        """Decides how many dice should be rolled for attack based on the attacker (and the defender, if any)."""
        attackDice = attack['Dice']
        defender = (Card(dTraitDict['OwnerID']) if 'OwnerID' in dTraitDict else None)
        if attack.get('Range',[None,None])[0] == 'Melee': attackDice += aTraitDict.get('Melee',0)
        if attack.get('Range',[None,None])[0] == 'Ranged': attackDice += aTraitDict.get('Ranged',0)
        if defender:
                attackDice -= dTraitDict.get('Aegis',0)
                attackDice += (aTraitDict.get('Bloodthirsty',0) if (defender.markers[Damage]
                                                                    and not 'Plant' in defender.subtype
                                                                    and defender.type == 'Creature'
                                                                    and not dTraitDict.get('Nonliving',False)) else 0)
                attackDice += dTraitDict.get(attack.get('Type',None),0) #Elemental weaknesses/resistances
                #Charge, but not sure how best to implement yet. Probably just add a prompt menu. Actually, we could do this for a lot of
                #traits that are hard to autodetect.
        if attackDice == 0: attackDice = 1
        if attack.get('Traits',{}).get('No Damage',False): attackDice = 0
        return attackDice

def computeArmor(aTraitDict,attack,dTraitDict):
        baseArmor = (getStat(Card(dTraitDict['OwnerID']).Stats,'Armor') if 'OwnerID' in dTraitDict else 0)
        return max(baseArmor+dTraitDict.get('Armor',0)-attack.get('Traits',{}).get('Piercing',0),0)

def computeAttack(aTraitDict,attackDict,dTraitDict):
        attack = attackDict
        atkTraits = attack.get('Traits',{})
        attack['Traits']['Piercing'] = atkTraits.get('Piercing',0) + aTraitDict.get('Piercing',0)#Need to fix attack traitDict so it has same format as creature traitDict
        return attackDict

def getAttackTraitStr(atkTraitDict): ##Takes an attack trait dictionary and returns a clean, easy to read list of traits
        attackList = []
        for key in atkTraitDict:
                text = key
                if key in additiveTraits: text += ' +{}'.format(str(atkTraitDict[key]))
                if key in superlativeTraits: text += ' {}'.format(str(atkTraitDict[key]))
                if atkTraitDict[key]: attackList.append(text)
        return attackList

def getRemainingLife(card):
        if not card: return 0
        life = getStat(card.Stats,'Life')
        if life: return max(life - card.markers[Damage] - (card.markers[Taint]*3),0)

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


"""
Calculations

The following functions are used to provide useful data to players; specifically, the expected damage inflicted and the chance to kill a
target.
"""

def computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict):
        armor = computeArmor(aTraitDict,attack,dTraitDict)
        atkTraits = attack.get('Traits',{})
        if dTraitDict.get('Incorporeal',False): return roll[2] + roll[4] + (2*(roll[3]+roll[5]) if atkTraits.get('Ethereal',False) else 0)
        normal = roll[2] + 2*roll[3]
        critical = roll[4] + 2*roll[5]
        return (max((0 if (dTraitDict.get('Resilient',False) or atkTraits.get('Critical Damage',False)) else normal) - armor,0) +
                critical + (normal if atkTraits.get('Critical Damage',False) else 0),
                computeEffect(effectRoll,aTraitDict,attack,dTraitDict))

def computeEffect(effectRoll,aTraitDict,attack,dTraitDict):
        modRoll = effectRoll + dTraitDict.get('Tough',0) + dTraitDict.get(attack.get('Type',None),0)
        debug('EffectRoll: {}, ModRoll: {}'.format(str(effectRoll),str(modRoll)))
        effects = attack.get('d12',[])
        if not effects: return None
        for effect in effects:
                rangeStr = effect[0]
                lowerBound, upperBound = 0,None
                if '-' in rangeStr: lowerBound,upperBound = int(rangeStr.split('-')[0]),int(rangeStr.split('-')[1])
                if '+' in rangeStr: lowerBound, upperBound = int(rangeStr.strip('+')),None
                if modRoll >= lowerBound and (modRoll <= upperBound if upperBound else True): return effect[1]
        return None
                

def computeAggregateDamage(normal,critical,aTraitDict,attack,dTraitDict):
        armor = computeArmor(aTraitDict,attack,dTraitDict)
        atkTraits = attack.get('Traits',{})
        return (max((0 if (dTraitDict.get('Resilient',False) or atkTraits.get('Critical Damage',False)) else normal) - armor,0) +
                critical + (normal if atkTraits.get('Critical Damage',False) else 0))
    
def expectedDamage(aTraitDict,attack,dTraitDict):
        dice= getAdjustedDice(aTraitDict,attack,dTraitDict)
        armor=computeArmor(aTraitDict,attack,dTraitDict)
        atkTraits = attack.get('Traits',{})
        if dice <= len(damageDict)-1 : distrDict = damageDict[dice]
        else: return
        if dTraitDict.get('Incorporeal',False): return (float(dice) if atkTraits.get('Ethereal',False) else float(dice)/3)
        return sum([computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict)*distrDict[key] for key in distrDict])/float(6**dice)

def chanceToKill(aTraitDict,attack,dTraitDict):
        dice = getAdjustedDice(aTraitDict,attack,dTraitDict)
        armor = computeArmor(aTraitDict,attack,dTraitDict)
        defender = Card(dTraitDict['OwnerID'])
        life = getRemainingLife(defender)# if 'OwnerID' in dTraitDict else None))
        atkTraits = attack.get('Traits',{})
        if dice <= len(damageDict)-1 : distrDict = damageDict[dice]
        else: return
        if dTraitDict.get('Incorporeal',False): return sum([nCr(dice,r)*(2**r)*(4**(dice-r)) for r in range(dice+1) if r >= life])/float(6**dice)
        return sum([distrDict[key] for key in distrDict if computeAggregateDamage(eval(key)[0],eval(key)[1],aTraitDict,attack,dTraitDict) >= life])/float(6**dice)

def nCr(n,r):
    return factorial(n) / factorial(r) / factorial(n-r)

def getD12Probability(rangeStr,aTraitDict,attack,dTraitDict):# needs to be changed to take Tough/elemental into account
        d12Bonus = dTraitDict.get('Tough',0) + dTraitDict.get(attack.get('Type',None),0)
        lowerBound, upperBound = 0,None
        if '-' in rangeStr: lowerBound,upperBound = int(rangeStr.split('-')[0]),int(rangeStr.split('-')[1])
        if '+' in rangeStr: lowerBound, upperBound = int(rangeStr.strip('+')),None
        debug(str(lowerBound)+','+str(upperBound))
        lowerBound,upperBound = max(lowerBound - d12Bonus,0),(max(upperBound - d12Bonus,0) if upperBound else None)
        successIncidence = 0 if (upperBound == 0 or lowerBound > 12) else ((upperBound if upperBound else 12) - lowerBound + 1)
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
