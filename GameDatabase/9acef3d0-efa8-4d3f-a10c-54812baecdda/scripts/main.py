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

def formatCardObject(card): #Interprets the XML file for the card and correctly formats each field.
	#Format cost
	try: card.Cost = int(card.Cost)
	except:
		try: card.Cost = eval(card.CostFunction)
		except: card.Cost = 0

	#Format range.
	try: card.Range = [int(n) for n in card.Range.split("-")]
	except: card.Range = [0,0]

	#Format target
	try: card.TargetParameters = card.TargetParameters.split(", ")
	except: card.TargetParameters = ["Zone"]

	#Format subtypes
	card.Subtypes = card.Subtype.split(", ")

	#Format stats
	stats = keyValueStringParser(card.Stats.split(", ")) #Might be a more concise way to get this.
	#Work in progress, clearly.

def keyValueStringParser(stringList):
	#Parses sets of "key=value" formatted strings and returns a dictionary
	output = {}
	for s in stringList:
		pair = s.split("=")
		output[pair[0]] = pair[1]
	return output