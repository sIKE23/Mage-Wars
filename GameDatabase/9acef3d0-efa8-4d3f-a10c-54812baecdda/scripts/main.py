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


def useUntargetedAbility(card, x=0, y=0):
	mute()
	debug(card.nickname)
	#debug(str(card.subtypes))

def testFormatting(card,x=0,y=0): #delete this function later
	formatCardObject(card)

def formatCardObject(card): #Interprets the XML file for the card and correctly formats each field.
	#Format name without title
	card.nickname = card.Name.split(", ")[0]

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