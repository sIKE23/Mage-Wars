###########################################################################
##########################    v2.00.0.0     ###############################
###########################################################################

###############################
######     Targeting     ######
###############################

passOnClick = None

def listenForClick(arg):
	global passOnClick
	whisper(arg.get("Click Prompt","Left click to select target"))
	passOnClick = arg

def onCardClicked(args):
	#args = card, mouseButton, keysDown
	global passOnClick
	if passOnClick != None: #TODO - restrict to only left click
		function,argument = passOnClick["function"],passOnClick
		argument["target"] = args.card
		function(argument)
		passOnClick = None

#Label spell functions associated with card actions with "CA", e.g. CA_Guard, CA_Attack, etc.
#On spells, label with before CA (bCA) and after CA (aCA) to indicated whether the effect should be  done before or after the card action.
#Here is the function for generating the spell list.

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
	dictionary = spellDictionary.get(card.Name,{})
	choiceList = []
	append = choiceList.append
	#Creatures should have the option to attack
	if isValidAttackSource(card):
		c = {"text":	"{}\n{}".format("Declare Attack".ljust(100,' '),dictionary.get('tCA_Attack',"Declare an attack against a target object.")),#Need to add intercept text as well
			 "color":	"#FF0000", #Red
			 "function":CA_Attack,
			 "argument":{}
			}
		append(c)
	#Get special actions
	for a in dictionary.get("special actions",[]):
		c = {"text":	a["text"],
			 "color":	a.get("color","#303030"), #Grey by default
			 "function":a["function"],
			 "argument":a["argument"]}
		append(c)
	#Get guard action
	if canGuard(card):
		c = {"text":	"{}\n{}".format("Guard".ljust(100,' '),dictionary.get('tCA_Guard',"Gain a guard token.")),#Need to add intercept text as well
			 "color":	"#303030", #Grey
			 "function":CA_Guard,
			 "argument":{}
			}
		append(c) #Creatures have option to guard
	return choiceList

def CA_Attack(arg):
	actor = arg["actor"]
	def clickFunction(arg2):
		target = arg2["target"]
		if isValidAttackTarget(target): 
			actor.arrow(target,True)
			diceRollMenu(actor,target)
			#targetMenu(actor,target)
		else:
			whisper("That is not a valid attack target!")
	arg["function"] = clickFunction
	listenForClick(arg)


#############################
######    Guarding     ######
#############################

##Convention for functions: first argument is card that has function, second is card calling the function.
def canGuard(card):
	dictionary = spellDictionary.get(card.Name,{})
	if card.Type == "Creature": return True
	#if dictionary.get("Type")=="Creature": return True #For the purposes of testing, we'll just leave this simple for now.

def CA_Guard(arg):
	card = arg["actor"]
	#dictionary = spellDictionary[card.Name]
	#actor = Card(dictionary["Actor ID"])
	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]

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
###  Attack Step Functions ##
#############################
"""
AS_DeclareAttack(source,attack)

where source is the function's source and attack is a dictionary containing all the information about the attack.

attack = {
	sourceID	int
	attackerID	int
	defenderID	int
	args 		dict
	hit			bool
	damage 		int
	conditions	list(str)
}

Should have an event to indicate that a creature began an attack, and another to indicate that it finished its attack.

"""


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
			if not (target.isFaceUp and "Zombie" in target.subtype and target.type == "Creature"):
				whisper("Invalid target! Must target zombie creature.")
				return
			if cardGetDistance(actor,target) > 1:
				whisper("{} is too far away to invigorate. Target must be within 1 zone.".format(target.nickname))
				return
			buff(target,["Melee +1"],"round")
			notify("Acolyte of the Bog Queen casts Vigor of the Grave!")
			notify("{} lets out an unearthly moan of fury! (Melee +1)".format(target.nickname))

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

##########################
## Adramelech's Torment ##
##########################

def adramelechsTorment_f1(arg):
	def clickFunction(arg2):
		if arg2.get("target") and arg2.get("actor"):
			target = arg2["target"]
			actor = arg2["actor"]
			if not (target.isFaceUp and target.Type=="Creature"):
				whisper("Invalid target!")
				return
			if not [1 for c in table if c.controller == actor.controller and getAttachTarget(c) == target and c.isFaceUp and "Curse" in c.subtype]:
				whisper("{} must have a revealed curse to be ignited!".format(target.nickname))
				return
			if target.markers[Burn] > 0:
				whisper("{} is already burning!".format(target.nickname))
				return
			paid = transaction(actor.controller,-2)
			if paid: 
				target.markers[Burn] += 1
				notify("Adramelech's Torment sets {} aflame! (+1 Burn)".format(target.nickname))
			else:
				whisper("Insufficient mana!")

	arg["function"] = clickFunction
	listenForClick(arg)

spellDictionary["Adramelech's Torment"] = {
		"special actions" : [
		{
			"text" :	"Ignite Curse (2 mana):\nSet a cursed creature aflame.".ljust(100,' '),
			"color":	"#990000",
			"function":	adramelechsTorment_f1,
			"argument": {},
		}
	]
}

###################
## Asyran Cleric ##
###################

def asyranCleric_f1(arg):

	def clickFunction(arg2):
		if arg2.get("target") and arg2.get("actor"):
			target = arg2["target"]
			actor = arg2["actor"]
			#TODO: Fix check for living trait; getBasicTraits is not sufficient long term
			if not (target.isFaceUp and target.Type=="Creature" and "Living" in getBasicTraits(target)):
				whisper("Invalid target! Must target living creature.")
				return
			if cardGetDistance(actor,target) > 1:
				whisper("{} is too far away to heal. Target must be within 1 zone.".format(target.nickname))
				return
			notify("Asyran Cleric casts Healing Light!")
			amount = str(CX_heal(target,simpleRollDice(1)))
			notify("{} heals {} damage!".format(target.nickname,amount))

	arg["function"] = clickFunction
	listenForClick(arg)

spellDictionary["Asyran Cleric"] = {
	"special actions" : [
		{
			"text" :	"Healing Light:\nHeal a nearby living creature.".ljust(100,' '),
			"color":	"#FF9900",
			"function":	asyranCleric_f1,
			"argument": {},
		}
	]
}