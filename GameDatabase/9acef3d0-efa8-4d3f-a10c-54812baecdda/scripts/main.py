#######
#v3.0.0.0#
#######

"""
The purpose of this module is to contain the bulk of the non-action code. I want to migrate the code not related to group/cardactions to this file.
"""

import time
import re
import sys
sys.path.append(wd("lib"))
import os
from math import factorial
from copy import deepcopy
from random import randint





def useUntargetedAbility(card, x=0, y=0):
	mute()
	debug(card.nickname)
	#debug(str(card.subtypes))

def testFormatting(card,x=0,y=0): #delete this function later
	formatCardObject(card)

def pSub(card):
	return {"M" : "he", "F" : "she"}.get(card.gender,"it")

def pObj(card):
	return {"M" : "him", "F" : "her"}.get(card.gender,"it")

def pPos(card):
	return {"M" : "his", "F" : "her"}.get(card.gender,"its")

def pRef(card):
	return {"M" : "himself", "F" : "herself"}.get(card.gender,"itself")

"""
Here is how to format the relevant new XML properties:

For targeting:
"Flying, Living Conjuration or Non-Mage Creature" === <property name="cTargets" value="m0,M2))tFlying,tLiving,TConjuration||!SMage,TCreature" />

note use of )) (range separator) and || (OR operator)

Range of spell given by
	m - minimum range
	M - maximum range
assumes infinite range (e.g. arena) if not specified

Can specify zone as a target via "_Zone"
Can specify facedown via "_Facedown" or any facing via "_Anyfacing"

For simple buffs:

<property name="cBuffs" value="m0,M1))@Self,tFlying,tLiving,TConjuration,[Fast;Psychic Immune;Armor+1,||#Y:^Friendly,Other,Cat,[mPiercing +1" />

prefixes:
	@ - self, target, or all. Assumes all if not specified.
	[ - the type of buff granted to objects that qualify
	t - trait possessed
	! - NOT operator
	T - type of card
	S - subtype possessed
	^ - alignment (friendly vs controlled vs enemy)
	l - min level (can also use for minor flag)
	L - max level
	s - school possessed

For infinite range buffs, use inf))


"""


def statsParser(stringList):
	#Parses sets of "key=value" formatted strings and returns a dictionary
	output = {}
	for s in stringList:
		pair = s.split("=")
		try: output[pair[0]] = int(pair[1])
		except: output[pair[0]] = 0
	return output

def rangeMatcher(source,target,cRangeString):
	debug("rangeMatcher\n")
	"Returns true if source and target are within range."
	distance = cardGetDistance(source,target)
	debug("distance: {}".format(distance))
	rangeSet = cRangeString.split(",")
	debug("rangeSet: {}".format(rangeSet))
	minimum = int(rangeSet[0][1:])
	debug("minimum: {}".format(minimum))
	maximum = int(rangeSet[1][1:])
	debug("maximum: {}".format(maximum))
	return (minimum <= distance <= maximum)

def targetMatcher(source,target,cTargetString):
	"This function returns True if the target given satisfies the conditions in cTargetString (which should be given without range requirements)"
	candLists = cTargetString.split("||")
	if "" in candLists: candLists.remove("")
	if candLists:
		debug("B")
		for candidate in candLists:
			disqualified = False
			reqList = candidate.split(",")
			for req in reqList:
				disqualified = not targetReqParser(source,target,req)
				if disqualified: break
			if not disqualified: return True
	return False

def buffMatcher(source,target,cBuffString):
	"This function returns a buff if the target given satisfies the conditions in cBuffString (which should be given without range requirements)"
	candLists = cBuffString.split("||")
	if "" in candLists: candLists.remove("")
	if candLists:
		for candidate in candLists:
			buff = []
			disqualified = False
			reqList = candidate.split(",")
			for req in reqList:
				#This isn't going to work for debuffs... might need to make a dBuff string?
				if req[0] == "[": buff.extend(req[1:-1].split(";"))
				else: disqualified = not targetReqParser(source,target,req)
				if disqualified: break
			if not disqualified: 
				return buff
	return []

def targetReqParser(source,target,req):
	"This parses a single requirement for targetMatcher to see if it is satisfied by card."
	notFlag = False
	tagPos = 0
	tag = req[0]
	if tag == "!":
		notFlag = True
		tag = req[1]
		tagPos = 1
	value = req[tagPos+1:]
	satisfies = False
	#Checks for each type of tag
	if tag == "t": satisfies = (value in getAllTraits(target))
	elif tag == "@": satisfies = (
		(value=="self" and source == target ) or 
		(value == "all") or 
		(value == "target" and getAttachTarget(source) == target)
	)
	elif tag == "T": satisfies = (value == target.Type)
	elif tag == "S": satisfies = (value in target.Subtype) #In the future, will need to make a getAllSubtypes function to handle effects that can change subtypes, such as zombie tokens.
	elif tag == "s": satisfies = (value in target.School)
	elif tag == "_": satisfies = False #For now. Will change later.
	elif tag == "^": satisfies = ((value in ["friendly","controlled"]) == (target.controller == source.controller)) #A temporary placeholder until we get alignment working.
	if notFlag: satisfies = not satisfies
	debug("targetReqParser: \n"+source.Name+" "+target.Name+" "+tag+" "+value+" "+str(satisfies)+"\n")
	return satisfies


def getAllTraits(card):
	return getBasicTraits(card)
	#	In the future, this function will calculate every single trait of the card (even those not listed in its xml, 
	#	much like computeTraits does now. For now, I will leave it as this placeholder.


###For now, let's store the targeting features here. Will need to move them in future.

######################################
######       Transactions       ######
######################################

def transaction(player,delta):
	"Handles mana transactions, changing the value of player's by delta as long as it does not drop below 0. Returns whether the transaction succeeded."
	if canTransact(player,delta):
		player.Mana += delta
		return True
	return False

def canTransact(player,delta):
	return (player.Mana-delta >= 0)

######################################
######   Turn Order Functions   ######
######################################

"Functions for handling turn order"

def establishTurnOrder():
	"The calling player chooses a turn order for all players"
	pass

def getTurnOrder():#WIP
	"""
	Retrieves the current turn order as a list of all player objects in order, with the current player first
	Use getTurnOrder()[0] to get the first player
	"""
	#debug("getTurnOrder()")
	return getPlayers() #TEMPORARY! Todo: implament turn order. For now, we will just use the id list

######################################
######     Memory Functions     ######
######################################

"""
These functions are for keeping track of what has happened so far this round.
Events are stored as dictionaries containing all relevant parameters. Example:
{"Round Number": 3,
 "Event Type" : "Attack",
 "Attacker": 65521,
 "Defender": 52234,
 "Damage Inflicted": 4,
 "Additional Strikes Remaining": 2}
 etc. I have not worked out whether or not OCTGN can handle storing dictionary objects (as opposed to dictionaries as strings),
 so that is something that is important to test.
 In contrast to the previous method of storing events, there will be only one list, and it will contain all the events that have occured in the entire game.

BUFF FORMAT

		"round": 		int(getGlobalVariable("RoundNumber"))	int
		"type": 		"buff",									str ("buff")
		"card id":		card._id,								int
		"traits":		traits,									list
		"duration":		duration								str ("round","game","turn")

"""

def storeEvent(arg):
	arg["round"] = int(getGlobalVariable("RoundNumber"))
	memory = eval(getGlobalVariable("gameMemory"))
	memory.append(arg)
	setGlobalVariable("gameMemory",str(memory))

def timesHasOccurred(event,keys): #Searches memory for instances of this event that have occurred. Only registers a match if all given keys match those from a remembered instance. Returns number of matches
	event["round"] = int(getGlobalVariable("RoundNumber"))
	memory = eval(getGlobalVariable("gameMemory"))
	#Check how many events this round match in the given keys
	return len([1 for e in memory if len([1 for k in keys if e.get(k)==event[k]])==len(keys)])

#This is from the 2.2.1.11 version. The above function doesn't work while the below is the one actually called throughout the scripts. Not sure why right now
def timesHasOccured(event,player=me):
		eventList = getEventList('Round')
		count = 0
		for e in eventList:
				if e[0] == 'Event' and e[1][0] == player._id and e[1][1]==event: count += 1
		return count


def getEvents(round):
	"Returns an ordered list of all events from the requested round"
	memory = eval(getGlobalVariable("gameMemory"))
	memory = [m for m in memory if m.get("round")==round]
	return memory

######################################
######     Recall Functions     ######
######################################

def rememberBuffs(card):
	"Returns a list of text-formatted traits granted via memorized buffs"
	memory = eval(getGlobalVariable("gameMemory"))
	roundNo = int(getGlobalVariable("RoundNumber"))
	cardID = card._id
	buffs = []
	extend = buffs.extend
	for m in memory:
		get = m.get
		if (get("type") == "buff"
			and get("card id") == cardID
			and ((get("duration") == "round" and get("round") == roundNo) or get("duration") == "game")
		): extend(get("traits",[]))
	return buffs

######################################
######        Targeting         ######
######################################

#Will probably need to move this.

def isValidAttackSource(card):
	return canDeclareAttack(card) #We'll just pass the buck for now.

def isValidAttackTarget(card):
	return ("Life" in card.stats)

def payForAttackSpell(player,attack):
	"Returns boolean for whether or not cost was paid"
	originalSource = Card(attack.get('OriginalSourceID'))
	if originalSource.Type == "Attack": return castSpell(originalSource)
	else:
		cost = attack.get('Cost')
		realCost = askInteger('Enter amount to pay for {}'.format(attack.get('Name')),cost)
		if realCost == None: return False
		else: return transaction(player,-realCost)

def targetMenu(source,target):
	"This will be a general function determining what happens when one card targets another, regardless of the method."
	#args = player,fromCard,toCard,targeted,scripted
	mute()
	debug("targetMenu")
	if not source and target: return

	if isValidAttackSource(source) and isValidAttackTarget(target) and getSetting('BattleCalculator',True):
		#WIP can get rid of these
		aTraitDict = computeTraits(source)
		dTraitDict = computeTraits(target)
		#-----------------------------


		attack = attackChoicePrompt(source,target)
		if attack:
			if attack.get("Cost") and not payForAttackSpell(me,attack): return
			if attack.get('source id')==source._id:
				remoteCall(target.controller,'initializeAttackSequence',[source,attack,target])
				source.arrow(target,False)
				return
			elif attack.get("Dice"): 
				notify("Attack cannot be parsed by Battle Calculator; rolling dice manually.")
				rollDice(attack.get("Dice"))
				source.arrow(target,False)
				return
	else:
		if source.Type == "Enchantment" and not source.isFaceUp and castSpell(source,target):
			attach(source,target)
			source.arrow(target,False)
		elif target.Type in typeIgnoreList or target.Name in typeIgnoreList or target.Type == "Magestats":
			mute()
			notify("{} is not a legal target".format(target.Name))
			source.arrow(target,False)
		elif source.Type !="Enchantment":
			castSpell(source,target) #Assume that player wants to cast card on target
			source.arrow(target,False)



#From the Boneyard - Will check to see if needed anymore

#---------------------------------------------------------------------------
# Workflow routines
#---------------------------------------------------------------------------

def playSoundFX(sound):
	mute()

	#is the setting on?
	if not getSetting("AutoConfigSoundFX", True):
		return
	else:
		playSound(sound)

def documentationReminder():
	mute()
	#### LOAD UPDATES
	v1, v2, v3, v4 = gameVersion.split('.')  ## split apart the game's version number
	v1 = int(v1) * 1000000
	v2 = int(v2) * 10000
	v3 = int(v3) * 100
	v4 = int(v4)
	currentVersion = v1 + v2 + v3 + v4  ## An integer interpretation of the version number, for comparisons later
	lastVersion = getSetting("lastVersion", convertToString(currentVersion - 1))  ## -1 is for players experiencing the system for the first time
	lastVersion = int(lastVersion)
	for log in sorted(changelog):  ## Sort the dictionary numerically
		if lastVersion < log:  ## Trigger a changelog for each update they haven't seen yet.
			stringVersion, date, text = changelog[log]
			updates = '\n-'.join(text)
			confirm("Documentation available in v.{} ({}):\n-{}".format(stringVersion, date, updates))
	setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------


def remoteHighlight(card, color):
	card.highlight = color

def remoteSwitchPhase(card, phase, phrase):
	card.alternate = phase

def remoteDeleteCard(card):
	card.delete()

def returnToHand(card): #Return card to your hand
	card.moveTo(me.piles["Spellbook"])

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def castSpell(card,target=None):
		#Figure out who is casting the spell
		binder = getBindTarget(card)
		caster = getBindTarget(card)
		if not caster or not ("Familiar" in caster.Traits or "Spawnpoint" in caster.Traits):
				casters = [d for d in table if "Mage" in d.Subtype and d.isFaceUp and d.controller == me and not "Magestats" in d.Type]
				if casters: caster = casters[0]
				else:
						whisper("And just who do you expect to cast that? You need to play a mage first.")
						return
		costStr = card.Cost
		if not target and card.Target not in ['Zone','Zone Border','Arena'] and card.Type in ["Incantation","Conjuration"]:
				targets = [c for c in table if c.targetedBy==me]
				if targets and len(targets) == 1: target = targets[0]
				else: whisper("No single target for {} detected. Cost calculation is more effective if you select a target.".format(card))
		if card.Type == "Enchantment" and not canAttach(card,target): return
		#Long term, invalid targets will result in spell cancellation. Won't enforce that for now, though.
		debug("Caster: " + caster.Name)
		if costStr:
				cardType = card.Type
				#First, determine the base cost
				cost = computeCastCost(card,target)
				if cost == None:
						costQuery = askInteger("Non-standard cost detected. Please enter base cost of this spell.\n(Close this menu to cancel)",0)
						if costQuery!=None: cost = costQuery
						else: return
				casterMana = caster.markers[Mana]
				ownerMana = me.Mana
				discountList = filter(lambda d: d[1][0]>0, [(c,getCastDiscount(c,card,target)) for c in table])
				#filter(lambda d: d[1]>0, map(lambda c: (c,getCastDiscount(c,card,target)),table)) #Find all discounts. It would be better to pass a list, but this isn't a bottleneck, so we'll make do for now.
				#Reduce printed cost by sum of discounts
				if "Fang of the First Moon" in card.Name:
						castDiscount = 0
						for c in me.piles['Discard Pile']:
								if "Animal" in c.Subtype:
										castDiscount += 2
								if castDiscount > 0: discountList = [(card, (castDiscount,"Found {} discarded animal creatures in {}\'s discard pile".format(castDiscount,me)))]
				usedDiscounts = []
				discountAppend = usedDiscounts.append
				for c,d in discountList:
						if cost > 0: #Right now, all discounts are for 1 (except construction yard). If there is ever a 2-mana discount, we will need to adjust this to optimize discount use. Come to think of it, some discounts overlap, and we might want to optimize for those...well, we can cross that bridge when we reach it.
								discAmt = min(cost,d[0])
								cost -= discAmt
								discountAppend((c,discAmt,d[1])) #Keep track of which discounts we are applying, and how much of each was applied
						else: break #Stop if the cost of the spell reaches 0; we don't need any more discounts.
				#Magebane
				for attachment in getAttachments(caster):
					if attachment.Name == 'Magebane' and attachment.isFaceUp:
						if askChoice("The caster is cursed by Magebane. Would you like to take 1 damage to cast the spell?",["Yes","No"],["#171e78","#de2827"]) == 1:
							if "Mage" in caster.Subtype:
								caster.controller.Damage += 1
								notify("{} suffers damage from {}\n".format(caster,attachment))
							else:
								caster.markers[Damage] += 1
								notify("{} suffers damage from {}\n".format(caster,attachment))
						else:
							return
				
				#Ask the player how much mana they want to pay
				discountSourceNames = "\n".join(["{} -{}".format(d[2],str(d[1])) for d in usedDiscounts])
				#discountSourceNames = '\n'.join(map(lambda t: "{} (-{})".format(t[0].Name,str(t[1])),usedDiscounts))
				discountString = "The following discounts were applied: \n{}\n\n".format(discountSourceNames) if discountSourceNames else ""
				pronoun = {"Male":"he","Female":"she"}.get(getGender(caster),"it")
				casterString = "{} will pay what {} can. You will pay the rest.\n\n".format(caster.Name.split(",")[0],pronoun) if (caster.Type != "Mage" and caster.markers[Mana]) else ""
				cost = askInteger("We think this spell costs {} mana.\n\n".format(str(cost))+
									 discountString+
									 casterString+
									 "How much mana would you like to pay?",cost)
				if cost == None: return
				if cost > casterMana + ownerMana:
						whisper('You do not have enough mana to cast {}!'.format(card.Name))
						return
				casterCost = min(casterMana,cost)
				caster.markers[Mana] -= casterCost #Hmmm... is casterMana mutable? Will need to experiment; not high priority
				if casterCost: notify("{} pays {} mana.\n".format(caster,str(casterCost)))
				cost -= casterCost
				if cost:
						if discountString =="":
							notify("{} pays {} mana.\n".format(me,str(cost)))
							me.Mana = max(me.Mana-cost,0)
						else:
							notify("{} pays {} mana with the following discount applied: {}.\n".format(me,str(cost),discountSourceNames))
							me.Mana = max(me.Mana-cost,0)
				for c,d,e in usedDiscounts: #track discount usage
						if c.Name=="Construction Yard": c.markers[Mana] -= d
						rememberAbilityUse(c)
				if card.Type == "Enchantment": notify("{} enchants {}!\n".format(caster,target.Name) if target else "{} casts an enchantment!".format(caster))
				elif card.Type == "Creature": notify("{} summons {}!\n".format(caster,card.Name))
				elif "Conjuration" in card.Type: notify("{} conjures {}!\n".format(caster,card.Name))
				else: notify("{} casts {}!\n".format(caster,card.Name))
				if card.Type != "Enchantment" and not card.isFaceUp: flipcard(card)
				
				if not binder or not "Spellbind" in binder.Traits:
						unbind(card) #If it is not bound, unbind it from its card
						if card.Type in ["Attack","Incantation"]: moveCardToDefaultLocation(card,True)
						else: card.sendToFront()
				return True

def revealEnchantment(card):
		if card.Type == "Enchantment" and not card.isFaceUp:
				cardType = card.Type
				target = getAttachTarget(card)
				if target and [True for c in getAttachments(target) if c.Name == card.Name and c.isFaceUp]:
						whisper("There is already a copy of {} attached to {}!".format(card.Name, target.Name))
						return
				if not target and card.Target not in ['Zone','Zone Border','Arena'] and not confirm("This enchantment is not attached to anything. Are you sure you want to reveal it?"): return
				#First, determine the base cost
				cost = computeRevealCost(card)
				if cost == None:
						costQuery = askInteger("Non-standard cost detected. Please enter the base cost of revealing this enchantment.",0)
						if costQuery!=None: cost = costQuery
						else: return
				ownerMana = me.Mana
				discountList = filter(lambda d: d[1]>0, map(lambda c: (c,getRevealDiscount(c,card)),table)) #Find all discounts. It would be better to pass a list, but this isn't a bottleneck, so we'll make do for now.
				#Reduce printed cost by sum of discounts
				usedDiscounts = []
				discountAppend = usedDiscounts.append
				for c,d in discountList:
						if cost > 0: #Right now, all discounts are for 1. If there is ever a 2-mana discount, we will need to adjust this to optimize discount use. Come to think of it, some discounts overlap, and we might want to optimize for those...well, we can cross that bridge when we reach it.
								cost = max(cost-d,0)
								discountAppend((c,d)) #Keep track of which discounts we are applying
						else: break #Stop if the cost of the spell reaches 0; we don't need any more discounts.
				#Ask the player how much mana they want to pay
				discountSourceNames = '\n'.join(map(lambda t: t[0].Name,usedDiscounts))
				discountString = "The following discounts were applied: \n{}\n\n".format(discountSourceNames) if discountSourceNames else ""
				cost = askInteger("We think this enchantment costs {} mana to reveal.\n\n".format(str(cost))+
									 discountString+
									 "How much mana would you like to pay?",cost)
				if cost == None: return
				#Do we have enough mana?
				if cost > ownerMana:
						whisper('You do not have enough mana to reveal {}!'.format(card.Name))
						return
				if cost:
						me.Mana = max(me.Mana-cost,0)
						notify("{} pays {} mana.\n".format(me,str(cost)))
				for c,d in usedDiscounts: #track discount usage
						rememberAbilityUse(c)
				flipcard(card)
				notify("{} reveals {}!\n".format(me,card))
				if card.Name == "Healing Charm":
						roll = rollDice(4)[0]
						healAmount = roll[2] + 2*roll[3] + roll[4] + 2*roll[5]
						if target.Subtype == "Mage" and target.controller == me:
								me.Damage = 0 if me.Damage < healAmount else me.Damage - healAmount
						elif "Creature" in target.Type and target.Subtype != "Mage" and target.controller == me:
								target.markers[Damage] -= healAmount
						notify("Heal Charm heals {} points of damage on {}!\n".format(healAmount,target))
				return True

def getCastDiscount(card,spell,target=None): #Discount granted by <card> to <spell> given <target>. NOT for revealing enchantments.
		if card.controller != spell.controller or not card.isFaceUp or card==spell: return (0,"") #No discounts from other players' cards or facedown cards!
		caster = getBindTarget(spell)
		mageCast = not(caster and ("Familiar" in caster.Traits or "Spawnpoint" in caster.Traits))
		spawnpointCast = (caster and "Spawnpoint" in caster.Traits)
		cName = card.Name
		sSubtype = spell.Subtype
		sType = spell.Type
		sName = spell.Name
		sSchool = spell.School
		timesUsed = timesHasUsedAbility(card)
		if timesUsed < 1: #Once-per-round discounts
				#Discounts that only apply when your mage casts the spell
				if (mageCast and
					((cName == "Arcane Ring" and sType != "Enchantment" and (("Metamagic" in sSubtype) or ("Mana" in sSubtype))) or
					 (cName == "Enchanter's Ring" and target and target.controller == card.controller and (target.type == "Creature" or target.Subtype == "Mage") and sType == "Enchantment") or
					 (cName == "Ring of Asyra" and ("Holy" in sSchool) and sType == "Incantation") or
					 (cName == "Ring of Beasts" and sType == "Creature" and ("Animal" in sSubtype)) or
					 (cName == "Ring of Curses" and sType != "Enchantment" and ("Curse" in sSubtype)) or
					 (cName == "Druid's Leaf Ring" and sType != "Enchantment" and ("Plant" in sSubtype)) or
					 (cName == "Force Ring" and sType != "Enchantment" and ("Force" in sSubtype)) or
					 (cName == "Ring of the Ocean\'s Depths" and sType != "Enchantment" and ("Hydro" in sSubtype or "Aquatic" in sSubtype)) or
					 (cName == "Ring of Command" and sType != "Enchantment" and ("Command" in sSubtype)) or
					 (cName == "Commander\'s Cape" and sType != "Enchantment" and ("Command" in sSubtype or ("Soldier" in sSubtype and "Creature" in sType))))):
						return (1,cName)
				#Discounts that apply no matter who casts the spell
				if ((cName == "General's Signet Ring" and ("Soldier" in sSubtype)) or
					(cName == "Eisenach's Forge Hammer" and (sType == "Equipment"))):
						return (1,cName)
				#Construction yard will be treated as a once-per-round discount.
				if (cName == "Construction Yard" and
					((not "Incorporeal" in spell.Traits and "War" in sSchool and "Conjuration" in sType) or ("Earth" in sSchool and sType=="Conjuration-Wall"))):
						return (card.markers[Mana],cName)
				#Discounts from Markers on Equipment
				if isBound(spell) == True and card.type == 'Equipment' and getBindTarget(spell) == card:
					boundCasterTraits = computeTraits(card)
					#Rune of Power
					if boundCasterTraits.get('Spellbind') == True and caster.markers[RuneofPower] == 1:
						return (1,"Rune of Power on {}".format(cName))
		if timesUsed <2: #Twice-per-round discounts
				if cName == "Death Ring" and (mageCast or spawnpointCast) and sType != "Enchantment" and ("Necro" in sSubtype or "Undead" in sSubtype):
						return (1,cName)
		return (0,"")
		#Returns discount as integer (0, if no discount)

def getRevealDiscount(card,spell): #Discount granted by <card> to <spell>. ONLY used for revealing enchantments (don't call for casting spells!)
		if card.controller != spell.controller or not card.isFaceUp or card==spell: return 0 #No discounts from other players' cards or facedown cards, or from itself!
		target = getAttachTarget(spell)
		cName = card.Name
		sSubtype = spell.Subtype
		sType = spell.Type
		sName = spell.Name
		sSchool = spell.School
		timesUsed = timesHasUsedAbility(card)
		if timesUsed < 1 and ((cName == "Arcane Ring" and (("Metamagic" in sSubtype) or ("Mana" in sSubtype))) or
							  (cName == "Ring of Asyra" and ("Holy" in sSchool)) or
							  (cName == "Ring of Curses" and ("Curse" in sSubtype)) or
							  (cName == "Druid's Leaf Ring" and ("Plant" in sSubtype)) or
							  (cName == "Force Ring" and ("Force" in sSubtype)) or
							  (cName == "Ring of Command" and ("Command" in sSubtype)) or
							  (cName == "Voice of the Sea" and ("Song" in sSubtype)) or
							  (cName == "Commander\'s Cape" and ("Command" in sSubtype))): return 1
		if timesUsed <2 and cName == "Death Ring" and ("Necro" in sSubtype or "Undead" in sSubtype): return 1
		return 0
		#Returns discount as integer (0, if no discount)

def computeRevealCost(card): #For enchantment reveals
		target = getAttachTarget(card) #To what is it attached?
		cost = None
		try: cost = int(card.Cost.split('+')[1])
		except: pass
		if not target: return cost
		#Exceptions
		name = card.Name
		if "/" in target.level:
			tLevel = int(sum(map(lambda x: int(x), target.Level.split('/')[0])))
		else:
			tLevel = int(sum(map(lambda x: int(x), target.Level.split('+'))))
		if name == "Mind Control":
				cost = 2*tLevel
		elif name in ["Charm","Fumble"]:
				cost = tLevel-1
		elif name in ["Asyra's Touch","Badger Frenzy","Exile","Panther Stealth","Wolf Fury"] and tLevel == 1: #Level 1 Creatures Discount
				cost -= 1
		elif name in ["Sanctuary"] and tLevel <= 2: #Minor Creatures Discount
				cost -= 1
		if cost == None: return #If it doesn't fit an exception, the player will have to handle it.
		traits = computeTraits(card)
		if "Mage" in target.Subtype:
				cost += traits.get("Magebind",0)
		return cost

def computeCastCost(card,target=None): #Does NOT take discounts into consideration. Just computes base casting cost of the card. NOT reveal cost.
		cost = 2 if card.Type == 'Enchantment' else None
		try: cost = int(card.Cost)
		except: pass
		if target: #Compute exact cost based on target. For now, cards like dissolve will have to target the spell they want to destroy. Does not check for target legality.
				name = card.Name
				if "Vine Marker" in target.Name and card.Name == "Burst of Thorns": return int(card.Cost)
				tLevel = (int(target.Level.split("/")[0]) if "/" in target.Level else int(sum(map(lambda x: int(x), target.Level.split('+')))))
				if name in ["Dissolve", "Conquer"]:
						cost = int(target.Cost)
				elif name in ["Dispel","Steal Enchantment"]:
						revealCost = computeRevealCost(target)
						if revealCost!=None: cost = 2 + revealCost
				elif name in ["Steal Equipment"]:
						cost = 2*int(target.Cost)
				elif name in ["Rouse the Beast","Disarm"]:
						cost = tLevel
				elif name in ["Quicksand"]:
						cost = 2*tLevel
				elif name == "Explode":
						cost = 6+int(target.Cost)
				elif name == "Shift Enchantment":
						if not card.isFaceUp: cost = 1
						else: cost = tLevel
				elif name == "Sleep":
						cost = {1:4,2:5,3:6}.get(tLevel,2*tLevel)
				elif name == "Defend":
						cost = {1:1,2:1,3:2,4:2}.get(tLevel,3)
				#For now, we won't consider things like harshforge plate. We could, but it is not necessary at the moment. We will add that when we implement the 3 stages of casting a spell. (Q2)
		return cost


def isDead(card):
	"returns boolean indicating whether this card is dead."
	pass

def getStat(stats, stat): #searches stats string for stat and extract value
	statlist = stats.split(", ")
	for statitem in statlist:
		statval = statitem.split("=")
		if statval[0] == stat:
						try: return int(statval[1])
						except: return 0
	return 0

def cardX(card):
	x, y = card.position
	return x

def cardY(card):
	x, y = card.position
	return y

	
def getTraitValue(card, TraitName):
	listofTraits = ""
	debug("{} has the {} trait".format(card.name, TraitName))
	listofTraits = card.Traits.split(", ")
	debug("List of Traits: {} ".format(listofTraits))
	if not len(listofTraits) > 1:
		strTraits = ''.join(listofTraits)
	else:
		for traits in listofTraits:
			if TraitName in traits:
				strTraits = ''.join(traits)
	STraitCost = strTraits.split("+")
	if STraitCost[1].strip('[]') == "X":
		infostr = "The spell {} has an Upkeep value of 'X' what is the value of X?".format(card.Name)
		TraitCost = askInteger(infostr, 3)
	else:
		TraitCost = int(STraitCost[1].strip('[]'))
	return (TraitCost)

def getTextTraitValue(card, TraitName):
	listofTraits = ""
	debug("{} has the {} trait in its card text.".format(card.name, TraitName))
	cardText = card.Text.split("\r\n")
	strofTraits = cardText[1]
	debug("{}".format(strofTraits))
	if "] [" in strofTraits:
			listofTraits = strofTraits.split("] [")
			for traits in listofTraits:
					if TraitName in traits:
							strTrait = ''.join(traits)
	else:
			strTrait = strofTraits
	STraitCost = strTrait.split("+")
	if STraitCost[1].strip('[]') == "X":
		TraitCost = 0
	else:
		TraitCost = int(STraitCost[1].strip('[]'))
	return (TraitCost)


def moveCardToDefaultLocation(card,returning=False):#Returning if you want it to go to the returning zone
		mute()
		mapDict = eval(getGlobalVariable('Map'))
		mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
		#debug("\n" + str(mwPlayerDict))
		playerNum = mwPlayerDict[me._id]["PlayerNum"]
		x,y = 0,0
		if not card.isFaceUp: cardW,cardH = cardSizes[card.size]['backWidth'],cardSizes[card.size]['backHeight']
		else: cardW,cardH = cardSizes[card.size]['width'],cardSizes[card.size]['height']
		if mapDict:
				iRDA,jRDA = mapDict.get("RDA",(2,2))
				zoneArray = mapDict.get('zoneArray')
				cardType = card.type
				if cardType == 'Internal': return
				mapX,mapW = mapDict.get('x'),mapDict.get('X')
				if cardType in ['DiceRoll','Phase']:
					moveRDA(card)
					return
				for i in range(len(zoneArray)):
						for j in range(len(zoneArray[0])):
								zone = zoneArray[i][j]
								if zone and zone.get('startLocation') == str(playerNum):
										zoneX,zoneY,zoneS = zone.get('x'),zone.get('y'),zone.get('size')
										if card.Subtype == 'Mage':
												x = (zoneX if i < mapDict.get('I')/2 else zoneX + zoneS - cardW)
												y = (zoneY if j < mapDict.get('J')/2 else zoneY + zoneS - cardH)
										elif cardType == 'Magestats':
												x = (zoneX - cardW if i < mapDict.get('I')/2 else mapX + mapW)
												y = (zoneY if j < mapDict.get('J')/2 else zoneY+zoneS-cardH)
										else:
												x = (zoneX - cardW if i < mapDict.get('I')/2 else mapX + mapW)
												y = (zoneY+cardH+cardH*int(returning) if j < mapDict.get('J')/2 else zoneY+zoneS-2*cardH-cardH*int(returning))
												dVector = ((-1,0) if i<mapDict.get('I')/2 else (1,0))
												x,y = splay(x,y,dVector)
		card.moveToTable(x,y,True)

def splay(x,y,dVector = (1,0)):
	"""Returns coordinates x,y unless there is already a card at those coordinates,
	in which case it searches for the next open position in the direction defined by dVector.
	Now using recursion!"""
	for c in table:
		if c.controller == me and (x,y) == c.position:
			wKey,hKey = {True: ("width","height"), False: ("backWidth","backHeight")}[c.isFaceUp]
			w,h = cardSizes[c.size][wKey],cardSizes[c.size][hKey]
			dx,dy = dVector
			return splay(x+dx*w,y+dy*h,dVector)
	return x,y

def debug(str):
	mute()
	global debugMode
	if debugMode:
		whisper("Debug Msg: {}".format(str))
# End of Boneyard gathering