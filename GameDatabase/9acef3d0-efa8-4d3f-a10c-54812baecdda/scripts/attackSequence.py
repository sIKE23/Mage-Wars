############################################################################
######################      Seven Steps of an Attack    ####################
############################################################################

"""
notation:

bAS - before Attack Step
aAS - after Attack Step

"""

"""
Since each attack step may be carried out by a different player, each step of the
attack should lead into the next.
"""

"""
argument will contain the following keys:

"identifier":	Should be "attack", identifying this argument as an attack for the purposes of event memory handling.
"sourceID":
"attackerID":
"defenderID":
"attack": 		The attack object
"hit":			Boolean indicating whether the attack has successfully hit
"damage": 		Amount of damage inflicted by the attack
"conditions":	Conditions inflicted by the attack
"strike":		The number of the current strike (e.g. the second strike would be 2)

"""


def revealEnchantmentMenu(): #Returns true if at least 1 attachment was revealed
	"""
	Prompts the player to reveal an enchantment. 
	For now, it will simply look at all enchantments the player has. 
	Later I may add the ability to recommend enchantments.
	Returns boolean of whether enchantment was revealed.
	"""
	debug("revealEnchantmentMenu\n")
	def getLocation(enchantment):
		#Is it attached to a card?
		attachTarget = getAttachTarget(enchantment)
		if attachTarget: return attachTarget.Nickname
		#Otherwise, return the zone
		zone = getZoneContaining(enchantment)
		return "Zone {},{}".format(str(zone[i]+1),str(zone[j]+1))

	#Get a list of my enchantments and their targets
	myEnchantments = [(e,getLocation(e)) for e in table if e.Type == "Enchantment" and not e.isFaceUp and e.controller == me]

	#Present menu if face down enchantments exist
	options = ["{}\n{}\n{}".format(e[0].Nickname.center(68,' '),e[1],e[0].Text.split('\r\n')[0]) for e in myEnchantments] + ["I would not like to reveal an enchantment."]
	colors = ['#CC6600' for i in options] + ["#de2827"]
	if myEnchantments:
		choice = askChoice('Would you like to reveal an enchantment?',options,colors)
	else:
		choice = 0

	#Player chose not to reveal an enchantment
	if choice in [0,len(options)]: return False

	#Player selected an enchantment to reveal
	return revealEnchantment(myEnchantments[choice-1][0])


def revealEnchantmentsStep(nextPlayer,nextStep,argument,doneList=[]):
	"""
	Step where players have a chance to reveal enchantments. Each player in turn order may reveal an enchantment or pass
	doneList - players who are done revealing enchantments
	nextStep - string naming the function for the step to be executed after completing the reveal enchantments step
	nextPlayer - the player object for the player that will execute the next step
	argument - the argument to be passed to the function for the next step
	"""
	debug("revealEnchantmentsStep\n")
	turnOrder = getTurnOrder()
	debug("Me: {}\n".format(me))
	# If everybody is finished revealing enchantments, we need to proceed to the next step
	if len(doneList) == len(turnOrder):
		remoteCall(nextPlayer,nextStep,[argument])
		return

	#Otherwise, ask the current player if they want to reveal any enchantments.
	#If yes, perform this step again
	if revealEnchantmentMenu(): revealEnchantmentsStep(nextPlayer,nextStep,argument) #Reset the done list
	#If no, proceed to the next player in turn order
	else:
		# Add me to the done list
		doneList.append(me) 
		debug("No more Enchantment reveals from {}\n".format(me))
		# Find my place in the turnOrder list
		myTurnNo = 0
		while turnOrder[myTurnNo] != me:
			myTurnNo += 1

		# Find the next player to reveal enchantments
		nextRevealerNo = (myTurnNo + 1) % len(turnOrder)
		nextRevealer = turnOrder[nextRevealerNo]

		# Next player to reveal enchantments gets a chance to do so
		remoteCall(nextRevealer,"revealEnchantmentsStep",[nextPlayer,nextStep,argument,doneList])

def initializeAttackSequence(attacker,attack,defender): #Here is the defender's chance to ignore the attack if they have disabled their battle calculator
	mute()
	debug("initializeAttackSequence\n")
	#for now, let's package everything together beforehand
	argument = {
		"identifier":	"attack",
		"sourceID":		Card(attack['source id'])._id,
		"attackerID":	attacker._id,
		"defenderID":	defender._id,
		"attack": 		attack,
		"hit":			True,
		"damage": 		0,
		"effects":		[],
		"strike":		1,
	}
	debug("iAS argument: {}\n".format(argument))
	if getSetting("BattleCalculator",True): 
		remoteCall(
			getTurnOrder()[0],			# First player
			"revealEnchantmentsStep",	# Interim step
				[attacker.controller,	# Next player
				"declareAttackStep",	# Next Step
				argument]				# Argument
		)			

	else:
		if attacker.controller == me: genericAttack(table)
		else:
			remoteCall(attacker.controller,'whisper',['{} has disabled Battle Calculator, so generic dice menu will be used'])
			remoteCall(attacker.controller,'genericAttack',[table])

def declareAttackStep(argument): #Executed by attacker #WIP lots of other logic to add in here I think from 2020 function
	mute()
	debug("declareAttackStep\n")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	atkOS 		= 	Card(argument["sourceID"])
	attack 		= 	argument["attack"]

	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]
	debug("spellList: {}".format(spellList))

	#1: resolve bAS effects - Monk using Ki? #WIP
	[d["bAS_DeclareAttack"]["function"](c,argument) for (c,d) in spellList if "bAS_DeclareAttack" in d]

	#2: check for daze
	if attacker.markers[Daze] and attack.get('RangeType') != 'Damage Barrier' and not "Autonomous" in atkOS.traits:
		notify("{} is rolling the Effect Die to check the Dazed condition.\n".format(attacker.nickname))#gotta figure that gender thing of yours out.
		damageRoll,effectRoll = rollDice(0)
		if effectRoll < 7:
			notify("{} is so dazed that {} completely misses!\n".format(attacker.nickname,pSub(attacker)))
			#remember attack use
			additionalStrikesStep(argument)
			return
		else: notify("Though dazed, {} manages to avoid fumbling the attack.\n".format(attacker.nickname))

	#3: give appropriate notification
	if attack.get('RangeType') == 'Counterstrike': notify("{} retaliates with {}!\n".format(attacker.nickname,attack.get('Name','a nameless attack')))
	elif attack.get('RangeType') == 'Damage Barrier': notify("{} is assaulted by the {} of {}!\n".format(defender.nickname,attack.get('Name','damage barrier'),attacker))
	else: notify("{} attacks {} with {}!\n".format(attacker.nickname,defender.nickname,attack.get('name','a nameless attack')))

	#4: resolve aAS effects
	[d["aAS_DeclareAttack"]["function"](c,card) for (c,d) in spellList if "aAS_DeclareAttack" in d]

	#5: end attack if cancelled
	if argument.get("cancel"): return

	#6: Next step
	remoteCall(
		getTurnOrder()[0],			# First player
		"revealEnchantmentsStep",	# Interim step
			[defender.controller,	# Next player
			"avoidAttackStep",		# Next Step
			argument]				# Argument
	)		

def avoidAttackStep(argument): #Executed by defender
	mute()
	debug("avoidAttackStep\n")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	atkOS 		= 	Card(argument["sourceID"])
	attack 		= 	argument["attack"]

	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]

	#1: resolve bAS effects
	[d["bAS_AvoidAttack"]["function"](c,argument) for (c,d) in spellList if "bAS_AvoidAttack" in d]

	#2: Roll defenses #WIP
	pass #defenseQuery(argument) #DefenseQuery will set the argument[hit] to false

	#3: resolve aAS effects
	[d["aAS_AvoidAttack"]["function"](c,argument) for (c,d) in spellList if "aAS_AvoidAttack" in d]

	#4: end attack if cancelled
	if argument.get("cancel"): return

	#5: go to the next step. If !hit, skip to additional strikes step
	if argument["hit"]:
		remoteCall(
			getTurnOrder()[0],			# First player
			"revealEnchantmentsStep",	# Interim step
				[attacker.controller,	# Next player
				"rollDiceStep",			# Next Step
				argument]				# Argument
	)
	else:
		remoteCall(
			getTurnOrder()[0],			# First player
			"revealEnchantmentsStep",	# Interim step
				[attacker.controller,	# Next player
				"additionalStrikesStep",# Next Step
				argument]				# Argument
	)

def rollDiceStep(argument): #Executed by attacker
	mute()
	debug("rollDiceStep\n")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	atkOS 		= 	Card(argument["sourceID"])
	attack 		= 	argument["attack"]

	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]
	debug("spellList: {}\n".format(spellList))

	#1: resolve bAS effects
	[d["bAS_RollDice"]["function"](c,argument) for (c,d) in spellList if "bAS_RollDice" in d]

	debug("attack: {}".format(attack))
	#2: roll dice
	dice = attack.get('dice',-1)
	if dice < 0:
		notify('Error: invalid attack format - no dice found')
		return
	damageRoll,effectRoll = rollDice(dice)

	argument["roll"] = (damageRoll,effectRoll)

	#3: resolve aAS effects
	[d["aAS_RollDice"]["function"](c,argument) for (c,d) in spellList if "aAS_RollDice" in d]

	#4: end attack if cancelled
	if argument.get("cancel"): return

	#5: Go to next step
	remoteCall(
		getTurnOrder()[0],			# First player
		"revealEnchantmentsStep",	# Interim step
			[defender.controller,	# Next player
			"damageAndEffectsStep",	# Next Step
			argument]				# Argument
	)

def damageAndEffectsStep(argument): #Executed by defender
	mute()
	debug("damageAndEffectsStep\n")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	atkOS 		= 	Card(argument["sourceID"])
	attack 		= 	argument["attack"]

	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)
	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]

	#1: resolve bAS effects #Example: Fortified resolve, brace yourself
	[d["bAS_DamageAndEffects"]["function"](c,argument) for (c,d) in spellList if "bAS_RollDice" in d]

	#2: apply damage and effects
	applyAttackResultsPrompt(argument) 

	#3: resolve aAS effects
	[d["aAS_DamageAndEffects"]["function"](c,argument) for (c,d) in spellList if "aAS_RollDice" in d]

	#4: end attack if cancelled
	if argument.get("cancel"): return

	#5: Go to next step
	remoteCall(
		getTurnOrder()[0],			# First player
		"revealEnchantmentsStep",	# Interim step
			[attacker.controller,	# Next player
			"additionalStrikesStep",# Next Step
			argument]				# Argument
	)

	remoteCall(attacker.controller,'additionalStrikesStep',[argument])

def applyAttackResultsPrompt(argument):
	mute()
	debug("applyAttackResultsPrompt\n")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	attack 		= 	argument["attack"]
	damageRoll	=	argument["roll"][0]
	effectRoll  = 	argument["roll"][1]
	defPlayer	=	defender.controller
	attPlayer	=	attacker.controller
	
	
	debug("damageRoll: {}\neffectRoll: {}\n".format(damageRoll,effectRoll))
	#1: Get damage and effects
	damage,effects = getAttackResults(argument)
	#debug("damage after return: {}\n".format(damage))
	
	#2: Generate informational statement
	#WIP: Create damage statement method in textFunctions and move the below to it
	statement = "{}'s attack ({}) will result in the following:".format(attacker.nickname,attack["name"])
	results = []
	append = results.append

	if damage: 
		append(" {} damage inflicted upon {}".format(str(damage),defender.nickname))
	else:
		append(" 0 damage against {}".format(defender.nickname))
	if effects: append("Effects: {}".format(" and ".join(effects)))
	if damage and attack.get("Mana Drain +X"): append("{} mana drained from {}".format(attack["Mana Drain +X"],defPlayer.Name))
	if damage and attack.get("Mana Transfer +X"): append("{} mana transferred from {} to {}".format(attack["Mana Transfer +X"],defPlayer.Name,attPlayer.name))

	append("\nConfirm these results")
	statement += "\n".join(results)

	#3: Prompt player to accept damage
	choice = askChoice(statement,["Accept","Reject (cancels attack)"],["#0f3706","#CC0000"])

	#4: If player did not accept, flag the attack as cancelled and return
	if not choice == 1:
		argument["cancel"] = True
		return

	#5: Apply damage and effects
	argument["damage"] = damage
	argument["effects"] = effects
	applyDamageAndEffects(argument)

def getAttackResults(argument): #WIP this needs cleaned up heavily
	mute()
	debug("getAttackResults\n")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	attack 		= 	argument["attack"]
	damageRoll	=	argument["roll"][0]
	effectRoll  = 	argument["roll"][1]

	
	#make a computeDamageToApply function
    #Needs to take resilient, incorporeal,vet belt, etc into account
	#Make a compute total armor function
	armor = getStat(defender.Stats,'Armor') #WIP temporary 
	debug("armor: {}\n".format(armor))

	normalDamage = damageRoll[2]+2*damageRoll[3]
	criticalDamage = damageRoll[4]+2*damageRoll[5]
	
	damage = (max(normalDamage-armor,0)) + criticalDamage
	effects = None
	debug("damage: {}\n".format(damage))

	return damage,effects



def applyDamageAndEffects(argument):
	mute()
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	attack 		= 	argument["attack"]
	damage		=	argument["damage"]
	effects		=	argument["effects"]

	#1: Compute actual damage
	#WIP this is unfinished 
	debug("damage before application: {}\n".format(damage))
	
	#real 1: 
	notify("{} inflicts {} damage on {}\n".format(attacker.name,
																	str(damage),
																	defender.name))
	remoteCall(defender.controller,"addDamageFromAttack",[defender,damage])
	

def additionalStrikesStep(argument):#aTraitDict,attack,dTraitDict): #Executed by attacker
	mute()
	debug("additionalStrikesStep")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	atkOS 		= 	Card(argument["sourceID"])
	attack 		= 	argument["attack"]
	atkTraits 	= 	attack.get('Traits',{})

	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]

	#1: store use of the attack in memory
	storeEvent(deepcopy(argument))

	#2: resolve bAS effects
	[d["bAS_AdditionalStrikes"]["function"](c,argument) for (c,d) in spellList if "bAS_AdditionalStrikes" in d]

	#3: resolve strikes

	strikes = 1
	if atkTraits.get('Doublestrike'): strikes = 2
	elif atkTraits.get('Triplestrike'): strikes = 3
	elif attacker.Name == 'Wall of Thorns':
		level = int(defender.Level)
		strikes = (level - 1 if level > 1 else 1)

	#4: resolve aAS effects
	[d["aAS_AdditionalStrikes"]["function"](c,argument) for (c,d) in spellList if "aAS_AdditionalStrikes" in d]

	#5: end attack if cancelled
	if argument.get("cancel"): return

	#6: if there are strikes remaining and defender is not dead, resolve them.

	if argument["strike"] < strikes and not isDead(defender):
		#Adjust argument and reset parameters
		argument["strike"] += 1
		argument["hit"] = True
		argument["damage"] = 0
		argument["conditions"] = []

		#Go back to declareAttackStep and begin a new strike 
		remoteCall(
			getTurnOrder()[0],			# First player
			"revealEnchantmentsStep",	# Interim step
				[attacker.controller,	# Next player
				"declareAttackStep",	# Next Step
				argument]				# Argument
	)

	#7: if not, go to the next step
	else:
		remoteCall(
			getTurnOrder()[0],			# First player
			"revealEnchantmentsStep",	# Interim step
				[defender.controller,	# Next player
				"damageBarrierStep",	# Next Step
				argument]				# Argument
		)

def damageBarrierStep(argument): #Executed by defender
	mute()
	debug("damageBarrierStep")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	attack 		= 	argument["attack"]

	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)

	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]

	#1: resolve bAS effects
	[d["bAS_DamageBarrier"]["function"](c,argument) for (c,d) in spellList if "bAS_RollDice" in d]

	#2: resolve damage barrier
	if attack.get("range type") == "Melee" and argument["hit"]:
		attackList = getAttacks(defender)
		dBarrier = None
		for a in attackList:
			if a.get('action type') == 'Damage Barrier':
				dBarrier = a
				break
		if dBarrier:
			# create a new dbarrier attack and resolve it. Depends on how I implement attack sources.
			pass

	#3: resolve aAS effects
	[d["aAS_DamageBarrier"]["function"](c,argument) for (c,d) in spellList if "aAS_DamageBarrier" in d]

	#4: end attack if cancelled or if defender is now dead
	if argument.get("cancel") or isDead(defender): return

	#5: Go to next step
	remoteCall(
	getTurnOrder()[0],			# First player
	"revealEnchantmentsStep",	# Interim step
		[defender.controller,	# Next player
		"counterstrikeStep",	# Next Step
		argument]				# Argument
	)

def counterstrikeStep(argument): #Executed by defender
	mute()
	debug("counterstrikeStep")
	attacker 	= 	Card(argument["attackerID"])
	defender 	= 	Card(argument["defenderID"])
	attack 		= 	argument["attack"]

	aTraitDict = computeTraits(attacker)
	dTraitDict = computeTraits(defender)

	spellList = [(c,spellDictionary.get(card.Name,{})) for c in table if c.Name in spellDictionary]

	if attack.get('RangeType') == 'Melee':
		counterAttack = diceRollMenu(defender,attacker,'Counterstrike')
		if counterAttack:
			counterAttack['RangeType'] = 'Counterstrike'
			interimStep(dTraitDict,counterAttack,aTraitDict,'Counterstrike','declareAttackStep')
		defender.markers[Guard] = 0

	#?: Go to next step
	remoteCall(
	getTurnOrder()[0],			# First player
	"revealEnchantmentsStep",	# Interim step
		[attacker.controller,	# Next player
		"attackEndsStep",		# Next Step
		argument]				# Argument
	)

def attackEndsStep(argument): #Executed by attacker
		mute()
		debug("attackEndsStep")
		setEventList('Turn',[]) #Clear the turn event list