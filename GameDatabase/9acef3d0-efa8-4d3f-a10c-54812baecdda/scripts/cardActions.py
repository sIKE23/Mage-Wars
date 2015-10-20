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
	for a in dictionary.get("special actions",[]):
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

#############################
###    Utility Functions   ##
#############################

def removeDamage(card,amount):
	amount = min(card.markers[Damage],amount)
	card.markers[Damage] -= amount
	return amount

def buff(card,traits,duration):
	event = {
		"type": 	"buff",
		"card id":	card._id,
		"traits":	traits,
		"duration":	duration
	}
	storeEvent(event)

#############################
###     Codex Functions    ##
#############################

#CX stands for codex function

def CX_heal(card,amount):
	#TODO Check whether card is living
	#TODO: bCX functions
	amount = removeDamage(card,amount)
	#TODO: aCX functions
	return amount

def CX_reconstruct(card,amount):
	#TODO: bCX functions
	amount = removeDamage(card,amount)
	#TODO: aCX functions
	return amount

#############################
###  Spells (Alphabetical) ##
#############################

spellDictionary = {}

#############################################################################
# ----------------------------------- A ----------------------------------- #
#############################################################################


##############################
## Acolyte of the Bog Queen ##
##############################

def acolyteOfTheBogQueen_f1(arg):
	def clickFunction(arg2):
		if arg2.get("target") and arg2.get("actor"):
			target = arg2["target"]
			actor = arg2["actor"]
			if "Skeleton" in target.subtype and cardGetDistance(actor,target) <= 1:
				amount = str(CX_reconstruct(target,2))
				notify("Acolyte of the Bog Queen casts Repair Bones!")
				notify("{}'s bones reassemble themselves, reconstructing {} damage!".format(target.nickname,amount))
			else: whisper("Invalid target!")
	arg["function"] = clickFunction
	listenForClick(arg)

def acolyteOfTheBogQueen_f2(arg):
	def clickFunction(arg2):
		if arg2.get("target") and arg2.get("actor"):
			target = arg2["target"]
			actor = arg2["actor"]
			#TODO: Find out if target is a zombie here, don't rely on subtype.
			if "Zombie" in target.subtype and (target.type == "Creature") and cardGetDistance(actor,target) <= 1: 
				buff(target,["Melee +1"],"round")
				notify("Acolyte of the Bog Queen casts Vigor of the Grave!")
				notify("{} lets out an unearthly moan of fury! (Melee +1)".format(target.nickname))
			else: whisper("Invalid target!")
	arg["function"] = clickFunction
	listenForClick(arg)

spellDictionary["Acolyte of the Bog Queen"] = {
	"special actions" : [
		{
			"text" :	"Repair Bones:\nRepair a nearby skeleton object".ljust(100,' '),
			"color":	"#996600",
			"function":	acolyteOfTheBogQueen_f1,
			"argument": {},
		},{
			"text" :	"Vigor of the Grave:\nGive a nearby zombie Melee +1".ljust(100,' '),
			"color":	"#996600",
			"function":	acolyteOfTheBogQueen_f2,
			"argument":	{},
		}
	]
}