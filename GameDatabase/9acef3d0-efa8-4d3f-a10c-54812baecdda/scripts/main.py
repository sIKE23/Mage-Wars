###########################################################################
##########################    v2.0.0.0     ###############################
###########################################################################
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
	card.nickname = "test"#card.Name.split(", ")[0]
	debug(card.nickname)

	#Format pronouns for card
	i = {"Male":1,"Female":2}.get(getGender(card),0)
	card.PSub = ["it","he","her"][i]				#Subject
	card.PObj = ["it","him","her"][i]				#Object
	card.PPos = ["its","his","her"][i]			#Possessive
	card.PRef = ["itself","himself","herself"][i]	#Reflexive
	"""
	#Format casting cost
	try: card.baseCost = int(card.Cost.split("+")[0])
	except: card.baseCost = 0

	#Format reveal cost
	try:
		reveal = card.Cost.split("+")[1]
		try: card.baseReveal = int(reveal)
		except: card.baseReveal = 0
	except: card.baseReveal = None

	#Format range.
	try: card.ranges = [int(n) for n in card.Range.split("-")]
	except: card.ranges = [0,0]

	#Format target
	try: card.targets = [s.split(",") for s in card.targeting.split("||")]
	except: card.targets = ["Zone"]

	#Format subtypes
	card.subtypes = card.Subtype.split(", ")
	#Format stats
	stats = statsParser(card.Stats.split(", ")) #Might be a more concise way to get this.
	card.baseArmor = stats.get("Armor")
	card.baseLife = stats.get("Life")
	card.baseChanneling = stats.get("Channeling")
	#Add card's built-in defense here
	#Work in progress, clearly.

	#Method Triggers:
	card.onDiscard = getOnDiscardFunction(card)
	"""
def getOnDiscardFunction(self): #Let's test this and see if it works...
	def discardFunction(caller):
		if self == caller: notify("{} is discarded!".format(self))
		else: notify("{} is a amused by {}'s destruction!".format(self,caller))
	return discardFunction

"""
Here is how to format the relevant new XML properties:
"Flying, Living Conjuration or Non-Mage Creature" === <property name="targeting" value="Flying,Living,Conjuration||!Mage,Creature" />

"""
def statsParser(stringList):
	#Parses sets of "key=value" formatted strings and returns a dictionary
	output = {}
	for s in stringList:
		pair = s.split("=")
		try: output[pair[0]] = int(pair[1])
		except: output[pair[0]] = 0
	return output