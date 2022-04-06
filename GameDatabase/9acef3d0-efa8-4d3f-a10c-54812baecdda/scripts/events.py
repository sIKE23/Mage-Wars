#######
#v3.0.0.0#
#######

#This may get taken care of some day

def setAcademyBoard():
	mute()
	#For now, let's just define a region of the appropriate size. We also need an image (or do we?)
	table.board = gameBoardsDict[10]["boardName"]
	defineRectangularMap(1,1,900)


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

###############################

#def onMoveCards(player,cards,fromGroups,toGroups,oldIndices,indices,oldXs,oldYs,xs,ys,highlights,markers,faceup):
def onCardsMoved(args):
	#args = player,cards,fromGroups,toGroups,indexs,xs,ys,highlights,markers,faceups
	mute()
	setGlobalVariable("MoveCardArgs",str(args))
	#assign variables when appropriate to cut down on memory access operations
	cards = args.cards
	toGroups = args.toGroups
	fromGroups = args.fromGroups
	xs = args.xs
	ys = args.ys
	indices = args.indexs
	#loop over all cards
	for i, card in enumerate(cards):
	  	position = card.position
	  	if card.controller == me and fromGroups[i]==table:
			if not (getAttachTarget(card) in cards or getBindTarget(card) in cards): #Only check for detach if the attachtarget was not moved
				unbind(card)
				c,t = detach(card)
				if toGroups[i] == table: card.moveToTable(position[0],position[1])#ugly, but fixes a bug that was preventing all but the first detached enchantment from moving.
				actionType = None
				if t:
					actionType = ['detaches','from']
				hasAttached = False
				if len(cards) == 1 and toGroups[i] == table: #Only check for autoattach if this is the only card moved
					for a in table:
						if (cardX(a)-position[0])**2 + (cardY(a)-position[1])**2 < 400 and canBind(card,a):
							c,t = bind(card,a)
							if t:
								actionType = ['binds','to']
								hasAttached = True
								break
						elif getSetting('AutoAttach',True) and (cardX(a)-position[0])**2 + (cardY(a)-position[1])**2 < 400 and canAttach(card,a):
							if (card.Type == "Enchantment" or card.Name in ["Tanglevine","Stranglevine","Quicksand"]) and not card.isFaceUp and not castSpell(card,a): break
							c,t = attach(card,a)
							if t:
								actionType = ['attaches','to']
								hasAttached = True
								break
				if (not hasAttached) and (toGroups[i] == table): snapToZone(card)
				if actionType:
					notify("{} {} {} {} {}.".format(me,actionType[0],c,actionType[1],t))
				if toGroups[i] != table:
					unbind(card)
					detach(card)
					detachAll(card)
					unbindAll(card)
				if not ((indices[i] != position and xs[i]==str(int(position[0])) and ys[i]==str(int(position[1]))) or
					isAttached(card) or
	  				getBindTarget(card) or
	  				toGroups[i] != table):
	  				alignAttachments(card)
	  				alignBound(card)#Do not realign if it is  only the index that is changing. Prevents recursions.

def onScriptedCardsMoved(args):
	#assign variables to args before the loop to cut down on memory access operations
	cards = args.cards
	toGroups = args.toGroups
	indices = args.indexs
	xs = args.xs
	ys = args.ys
	#handle attached cards when attach target is moved/deleted by a function
	for i in range(len(cards)):
		card = cards[i]
		position = card.position
		if toGroups[i] != table:
			unbind(card)
			detach(card)
			detachAll(card)
			unbindAll(card)
		if not ((indices[i] != position and xs[i]==str(int(position[0])) and ys[i]==str(int(position[1]))) or
			isAttached(card) or
			getBindTarget(card) or
			toGroups[i] != table):
			alignAttachments(card)
			alignBound(card)


def onCardArrowTargeted(args):
	#args = player,fromCard,toCard,targeted,scripted
	mute()
	source,target = args.fromCard,args.toCard #Should probably make an attack declaration function. Eventually.
	if args.player == me == source.controller and args.targeted and not args.scripted and getSetting("DeclareAttackWithArrow",True): targetMenu(source,target)
# WIP - Tinkering required

def onCardDoubleClicked(args):
	#args = card, mouseButton, keysDown
	mute()
	if args.card.type == "DiceRoll":
		genericAttack(0)

	if args.card.type =="Phase":
		nextPhase(table)


def checkMageDeath(args):
	#args = player,counter,value,scripted
	mute()
	if getGlobalVariable("GameSetup") == "True" and me.Damage >= me.Life and askChoice('          Your Mage has fallen in the Arena! \n\nDo you wish to continue playing until the end of the current Phase?',['Yes','No'],["#01603e","#de2827"]) == 2:
			for card in table:
					if card.Subtype == "Mage" and card.controller == me:
							card.orientation = 1
							#playSoundFX('Winner')
							for p in players:
									remoteCall(p, "reportDeath",[me])
	#reportGame('MageDeath')

def reportDeath(deadmage):
	setGlobalVariable("GameIsOver", "True")
	setGlobalVariable("GameEndTime", str(time.ctime()))
	whisper("{} has fallen in the arena! At {} after {} Rounds.".format(deadmage, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")))
	choice = askChoice("{} has fallen in the arena! At {} after {} Rounds.".format(deadmage, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")), ['OK'], ['#de2827'])
	endingStats()
	if choice == 0 or 1:
		return

def reportVTarWin(winningmage,score):
	setGlobalVariable("GameIsOver", "True")
	setGlobalVariable("GameEndTime", str(time.ctime()))
	whisper("{} has won the Domination Match with a total of {} V'Tar! At {} after {} Rounds.".format(winningmage,score, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")))
	choice = askChoice("{} has won the Domination Match with a total of {} V'Tar!! At {} after {} Rounds.".format(winningmage, score, getGlobalVariable("GameEndTime"), getGlobalVariable("RoundNumber")), ['OK'], ['#de2827'])
	endingStats()
	if choice == 0 or 1:
		return

def concede(group=table, x = 0, y = 0):
	mute()
	if confirm("Are you sure you want to concede this game?"):
		setGlobalVariable("GameIsOver", "True")
		setGlobalVariable("GameEndTime", str(time.time()))
		for c in table:
			if c.Subtype == "Mage" and c.controller == me:
				c.orientation = 1
		# reportGame('Conceded')
		notify("{} has conceded the game".format(me))
		endingStats()
	else:
		notify("{} was about to concede the game, but thought better of it...".format(me))


def playerStats():
	mute()
	if getGlobalVariable("GameIsOver") == "True":
		notify("Player Stats at the end of the Match")
	notify("\nAt the Start of Round #{}, {}'s Mage has the following stats: Channeling: {}, Mana Pool {}, Life {}, and Damage {}.".format(getGlobalVariable("RoundNumber"),me.name,me.channeling,me.mana,me.life,me.damage))