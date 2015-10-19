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

def formatCardObject(card): #Interprets the XML file for the card and correctly formats each field.
	#Format name without title
	#card.nickname = card.Name.split(", ")[0]

	#Format pronouns for card
	i = {"Male":1,"Female":2}.get(getGender(card),0)
	card.PSub = ["it","he","her"][i]				#Subject
	card.PObj = ["it","him","her"][i]				#Object
	card.PPos = ["its","his","her"][i]				#Possessive
	card.PRef = ["itself","himself","herself"][i]	#Reflexive

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

<property name="cBuffs" value="#X,@Self,tFlying,tLiving,TConjuration,[Fast;Psychic Immune;Armor+1,||#Y:^Friendly,Other,Cat,[mPiercing +1" />

prefixes:
	@ - self, other, or all. Assumes other if not specified
	[ - the type of buff granted to objects that qualify
	t - trait possessed
	! - NOT operator
	T - type of card
	S - subtype possessed
	^ - alignment (friendly vs enemy) possessed
	l - min level (can also use for minor flag)
	L - max level
	s - school possessed


"""

def statsParser(stringList):
	#Parses sets of "key=value" formatted strings and returns a dictionary
	output = {}
	for s in stringList:
		pair = s.split("=")
		try: output[pair[0]] = int(pair[1])
		except: output[pair[0]] = 0
	return output

def targetMatcher(targeter,target,cTargetString):
	"This function returns True if the target given satisfies the conditions in cTargetString (which should be given without range requirements)"
	candLists = cTargetString.split("||")
	for candidate in candLists:
		disqualified = False
		reqList = candidate.split(",")
		for req in reqList:
			disqualified = not targetReqParser(targeter,target,req)
		if not disqualified: return True
	return False

def targetReqParser(targeter,target,req):
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
	elif tag == "T": satisfies = (value == target.Type)
	elif tag == "S": satisfies = (value in target.Subtype) #In the future, will need to make a getAllSubtypes function to handle effects that can change subtypes, such as zombie tokens.
	elif tag == "s": satisfies = (value in target.School)
	elif tag == "_": satisfies = False #For now. Will change later.
	elif tag == "^": satisfies = ((value == "Friendly") == (target.controller == targeter.controller)) #A temporary placeholder until we get alignment working.
	if notFlag: satisfies = not satisfies
	return satisfies


def getAllTraits(card):
	return card.Traits.split(",")
	#	In the future, this function will calculate every single trait of the card (even those not listed in its xml, 
	#	much like computeTraits does now. For now, I will leave it as this placeholder.


###For now, let's store the targeting features here. Will need to move them in future.

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
"""

def storeEvent(argument):
	argument["Round Number"] = int(getGlobalVariable("RoundNumber"))
	memory = eval(getGlobalVariable("gameMemory"))
	memory.append(argument)
	setGlobalVariable("gameMemory",str(memory))

def timesHasOccurredThisRound(event): #Searches memory for instances of this event that have occurred this round. Only registers a match if all given keys match those from a remembered instance. Returns number of matches
	event["Round Number"] = int(getGlobalVariable("RoundNumber"))
	memory = eval(getGlobalVariable("gameMemory"))
	return len([1 for e in memory if len([k for k in event if e.get(k)==event[k]])==len(event)])

###############################
######     Targeting     ######
###############################

def listenForClick(argument):
	global passOnClick
	whisper(argument.get("Click Prompt","Left click to select target"))
	passOnClick = argument

def onCardClick(card,mousebutton,keysdown):
	global passOnClick
	if mousebutton == 0 and passOnClick:
		function,argument = passOnClick["Function"],passOnClick
		argument["Target ID"] = card._id
		function(argument)
		passOnClick = None

###########################################################################
##########################    v2.00.0.0     ###############################
###########################################################################

#Label spell functions associated with card actions with "CA", e.g. CA_Guard, CA_Attack, etc.
#On spells, label with before CA (bCA) and after CA (aCA) to indicated whether the effect should be  done before or after the card action.
#Here is the function for generating the spell list.
#spellList = [mergeDictionaries(spellDictionary[c.Name],{"Card ID":c._id) for c in table]

def passFunction(arg):
	pass

def actionMenu(card,x=0,y=0):
	"""This function brings up a menu of options for a given card. Called with *TAB*."""
	choiceList = getChoiceList(card) #getChoiceList returns a list of dictionary objects containing the choice text, color, function, and argument.
	choice = askChoice("What should {} do?".format(card.nickname),[c.get("text","") for c in choiceList],[c.get("color","") for c in choiceList])
	if choice == 0: return
	function,argument = choiceList[choice-1].get("function",passFunction),choiceList[choice-1].get("argument",{})
	argument["actor"] = card
	function(argument)

def getChoiceList(card):
	dictionary = spellDictionary[card.Name]
	choiceList = []
	#Get attacks - For now, attacks will not be integrated into this system
	#if canAttack(dictionary):
	#	for a in dictionary.get("Attacks",[]):
	#		if a.get("Action") not in ["Quick","Full","Passage Attack"]: continue
	#		c = {"Text":"Attack with {}\n{}".ljust(100,' ').format(a["Name"],"Passage Attack" if a["Action"]=="Passage Attack" else "{} dice {} attack".format(a["Dice"],a.get("Range Type","").lower())),
	#			 "Color":"#FF0000", #Red; later, might change so that color depends on type of attack
	#			 "Function":CA_Attack,
	#			 "Argument":a}
	#		choiceList.append(c)
	#Get special actions
	for a in dictionary.get("Special Actions",[]):
		c = {"text":	a["text"],
			 "color":	a.get("color","#303030"), #Grey by default
			 "function":a["function"],
			 "argument":a["argument"]}
		choiceList.append(c)
	#Get guard action
	if canGuard(card):
		c = {"text":	"{}\n{}".format("Guard".ljust(100,' '),dictionary.get('tCA_Guard',"Gain a guard token.")),#Need to add intercept text as well
			 "color":	"#303030", #Grey
			 "function":CA_Guard,
			 "argument":{}
			}
		choiceList.append(c) #Creatures have option to guard
	return choiceList

def canGuard(card):
	dictionary = spellDictionary[card.Name]
	if card.Type == "Creature": return True
	#if dictionary.get("Type")=="Creature": return True #For the purposes of testing, we'll just leave this simple for now.

#############################
######    Guarding     ######
#############################

##Convention for functions: first argument is card that has function, second is card calling the function.

def CA_Guard(arg):
	card = arg["actor"]
	#dictionary = spellDictionary[card.Name]
	#actor = Card(dictionary["Actor ID"])
	spellList = [(c,spellDictionary[c.Name]) for c in table if c.Name in spellDictionary]

	#First, resolve bCA effects
	[d["bCA_Guard"]["function"](c,card) for (c,d) in spellList if "bCA_Guard" in d]
	#[d["bCA_Guard"]["Function"](mergeDictionaries([d["bCA_Guard"]["Argument"],{"Source ID":d["Card ID"]},{"Actor ID":dictionary["Actor ID"]}])) for d in spellList if "bCA_Guard" in d]
	#Second, gain the guard marker
	card.markers[Guard] = 1
	notify("{} guards!".format(card.nickname))
	#Third, resolve aCA effects
	[d["aCA_Guard"]["function"](c,card) for (c,d) in spellList if "aCA_Guard" in d]
	#[d["aCA_Guard"]["Function"](mergeDictionaries([d["aCA_Guard"]["Argument"],{"Source ID":d["Card ID"]},{"Actor ID":dictionary["Actor ID"]}])) for d in spellList if "aCA_Guard" in d]

spellDictionary = {"Vine Snapper": {}}