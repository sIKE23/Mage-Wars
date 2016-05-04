#######
#v2.0.0.0#
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
	"Returns true if source and target are within range."
	distance = cardGetDistance(source,target)
	rangeSet = cRangeString.split(",")
	minimum = int(rangeSet[0][1:])
	maximum = int(rangeSet[1][1:])
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
				if req[0] == "[": buff.extend(req[1:].split(";"))
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
	debug(source.Name+" "+target.Name+" "+tag+" "+value+" "+str(satisfies))
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

def getTurnOrder():
	"""
	Retrieves the current turn order as a list of all player objects in order, with the current player first
	Use getTurnOrder()[0] to get the first player
	"""
	debug("getTurnOrder()")
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
	if not source and target: return

	if isValidAttackSource(source) and isValidAttackTarget(target) and getSetting('BattleCalculator',True):
		aTraitDict = computeTraits(source)
		dTraitDict = computeTraits(target)
		attack = attackChoicePrompt(source,target)#diceRollMenu(source,target)
		if attack:
			if attack.get("Cost") and not payForAttackSpell(me,attack): return
			if attack.get('SourceID')==source._id:
				remoteCall(target.controller,'initializeAttackSequence',[aTraitDict,attack,dTraitDict])
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