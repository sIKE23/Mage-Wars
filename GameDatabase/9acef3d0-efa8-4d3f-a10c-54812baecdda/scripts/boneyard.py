



############################################################################
######################		Group Actions			########################
############################################################################

def optionsMenu(group,x=0,y=0):
	#Consolidates the many game toggle options into a single menu
	settingsList = [
		{True : "Auto Calculate Upkeep Effects Enabled", False: "Auto Calculate Upkeep Effects Disabled", "setting": "AutoResolveEffects"},
		{True : "Auto Attachments Enabled", False: "Auto Attachments Disabled", "setting": "AutoAttach"},
		{True : "Prompt for Game Selection and Board", False: "Standard Arena Gameboard Enabled", "setting": "AutoBoard"},
		{True : "Battle Calculator Enabled", False: "Battle Calculator Disabled", "setting": "BattleCalculator"},
		{True : "Sound Effects Enabled", False: "Sound Effects Disabled", "setting": "AutoConfigSoundFX"},
		{True : "Place the Roll Dice Area to the Side", False: "Place the Dice Roll Area to the Bottom", "setting": "RDALocation"},
		{True : "Tutorial Enabled", False: "Tutorial Disabled", "setting": "octgnTutorial"}
	]
	choices = [e[getSetting(e["setting"],True)] for e in settingsList] + ["Done"]
	colors = [{True:"#006600",False:"#800000"}[getSetting(e["setting"],True)] for e in settingsList] + ["#000000"]
	choice = askChoice("Click to toggle any game setting",choices,colors)
	if choice not in [0,len(choices)]:
		setSetting(settingsList[choice-1]["setting"],not getSetting(settingsList[choice-1]["setting"],True))
		optionsMenu(group)

#This function lets the player set a timer
def setTimer(group,x,y):
		timerIsRunning = eval(getGlobalVariable("timerIsRunning"))
		if timerIsRunning:
				whisper("You cannot start a new timer until the current one finishes!")
				return
		setGlobalVariable("timerIsRunning",str(True))
		timerDefault = getSetting('timerDefault',300)
		choices = ["30 seconds","60 seconds","180 seconds","{} seconds".format(str(timerDefault)),"Other"]
		colors = ["#006600" for c in choices][:-1] + ['#003366']
		choice = askChoice("Set timer for how long?",choices,colors)
		if choice == 0: return
		seconds = {1:30,2:60,3:180,4:timerDefault}.get(choice,0)
		if choice == 5:
				seconds = askInteger("Set timer for how many seconds?",timerDefault)
				setSetting('timerDefault',seconds)
		notify("{} sets a timer for {} minutes, {} seconds.".format(me,seconds/60,seconds%60))
		playSoundFX('Notification')
		time.sleep(0.2)
		playSoundFX('Notification')
		notifications = range(11) + [30] + [x*60 for x in range(seconds/60+1)][1:]
		endTime = time.time() + seconds
		notifications = [endTime - t for t in notifications if t < seconds]
		updateTimer(endTime,notifications)

#This function checks the timer, and then remotecalls itself if the timer has not finished
def updateTimer(endTime,notifications):
		mute()
		currentTime = time.time()
		if currentTime>notifications[-1]:
				timeLeft = int(endTime - notifications[-1])
				playSoundFX('Notification')
				if timeLeft > 60: notify("{} minutes left!".format(timeLeft/60))
				else: notify("{} seconds left!".format(timeLeft))
				notifications.remove(notifications[-1])
		if notifications: remoteCall(me,"updateTimer",[endTime,notifications])
		else:
				playSoundFX('Alarm')
				notify("Time's up!")
				setGlobalVariable("timerIsRunning",str(False))

def playerDone(group, x=0, y=0):
	notify("{} is done".format(me.name))

def genericAttack(group, x=0, y=0):
	target = [cards for cards in table if cards.targetedBy==me]
	defender = (target[0] if len(target) == 1 else None)
	dice = diceRollMenu(None,defender).get('Dice',-1)
	if dice >=0: rollDice(dice)

def flipCoin(group, x = 0, y = 0):
	mute()
	n = rnd(1, 2)
	if n == 1:
		notify("{} flips heads.".format(me))
	else:
		notify("{} flips tails.".format(me))

def createVineMarker(group, x=0, y=0):
	mute()
	table.create("ed8ec185-6cb2-424f-a46e-7fd7be2bc1e0", x, y)
	notify("{} creates a Green Vine Marker.".format(me))

def createCompassRose(group, x=0, y=0):
	table.create("7ff8ed79-159c-46e5-9e87-649b3269a931", 450, -40 )

def createAltBoardCard(group, x=0, y=0):
	table.create("af14ca09-a83d-4185-afa0-bc38a31dbf82", 450, -40 )

def resetDiscounts():
	#reset discounts used
	for tup in discountsUsed:
		discountsUsed.remove(tup)
		discountsUsed.append((tup[0],tup[1],0))

def advanceTurn():
	mute()
	nextPlayer = getNextPlayerNum()
	nextPlayerName = getGlobalVariable("P" + str(nextPlayer) + "Name")
	for p in players:
		if p.name == nextPlayerName:
			for p2 in players:
				remoteCall(p2, "setActiveP", [p])

#def setActiveP(p):
#	p.setActivePlayer()

def resetMarkers():
	mute()
	for c in table:
		if c.targetedBy == me:
			c.target(False)
		if c.controller == me and c.isFaceUp: #don't waste time on facedown cards and only reset the markers on my cards.
			mDict = {ActionRedUsed : ActionRed,
						ActionBlueUsed : ActionBlue,
						ActionGreenUsed : ActionGreen,
						ActionYellowUsed : ActionYellow,
						ActionPurpleUsed : ActionPurple,
						ActionGreyUsed : ActionGrey,
						QuickBack : Quick,
						Used : Ready,
						UsedII : ReadyII,
						VoltaricON : VoltaricOFF,
						DeflectU : DeflectR,
						Visible : Invisible}
			for key in mDict:
						if c.markers[key] == 1:
								c.markers[key] = 0
								c.markers[mDict[key]] = 1
		#add a Guard Marker to Orb Guardians when they are in the same zone as an Orb
		for c in table:
			if "Orb Guardian" in c.name:
				for o in table:
					isWithOrb = False
					if "V'Tar Orb" in o.name and (getZoneContaining(o) == getZoneContaining(c)):
						isWithOrb = True
						if isWithOrb:
							c.markers[Guard] = 1

	notify("{} resets all Action, Ability, Quickcast, and Ready Markers on the Mages cards by flipping them to their active side.".format(me.name))
	debug("card,stats,subtype {} {} {}".format(c.name,c.Stats,c.Subtype))

def resolveBurns():
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	cardsWithBurn = [c for c in table if c.markers[Burn] and c.controller == me]
	if len(cardsWithBurn) > 0:
		notify("Resolving Burns for {}...".format(me))	#found at least one
		for card in cardsWithBurn:
			numMarkers = card.markers[Burn]
			burnDamage = 0
			burnsRemoved = 0
			for i in range(0, numMarkers):
				roll = rnd(0, 2)
				if roll == 0:
					card.markers[Burn] -= 1
					burnsRemoved += 1
				burnDamage += roll
			#apply damage
			if card.Subtype == "Mage":
				card.controller.Damage += burnDamage
			elif card.Type == "Creature" or "Conjuration" in card.Type and not card.Subtype == "Mage":
				card.markers[Damage] += burnDamage
			notify("{} damage added to {}. {} Burns removed.".format(burnDamage, card.Name, burnsRemoved))
		notify("Finished auto-resolving Burns for {}.".format(me))

def resolveRot():
	mute()

	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	cardsWithRot = [c for c in table if c.markers[Rot] and c.controller == me]
	if len(cardsWithRot) > 0:
		notify("Resolving Rot for {}...".format(me))	#found at least one
		for card in cardsWithRot:
			rotDamage = (card.markers[Rot])
			 #apply damage
			if card.Subtype == "Mage":
				card.controller.Damage += burnDamage
			elif card.Type == "Creature" or "Conjuration" in card.Type and not card.Subtype == "Mage":
				card.markers[Damage] += rotDamage
			notify("{} damage added to {}.".format(rotDamage, card.Name))
		notify("Finished auto-resolving Rot for {}.".format(me))

def resolveBleed():
	mute()

	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	cardsWithBleed = [c for c in table if c.markers[Bleed] and c.controller == me]
	if len(cardsWithBleed) > 0:
		notify("Resolving Bleed for {}...".format(me))	#found at least one
		for card in cardsWithBleed:
			bleedDamage = (card.markers[Bleed])
			 #apply damage
			if card.Subtype == "Mage":
				card.controller.Damage += burnDamage
			elif card.Type == "Creature" or "Conjuration" in card.Type and not card.Subtype == "Mage":
				card.markers[Damage] += bleedDamage
			notify("{} damage added to {}.".format(bleedDamage, card.Name))
		notify("Finished auto-resolving Bleed for {}.".format(me))

def resolveDissipate():
	mute()

#is the setting on?
	if not getSetting("AutoResolveDissipate", True):
		return

	cardsWithDissipate = [c for c in table if c.markers[DissipateToken] and c.controller == me]
	if len(cardsWithDissipate) > 0:
		notify("Resolving Dissipate for {}...".format(me))	#found at least one
		for card in cardsWithDissipate:
			notify("Removing 1 Dissipate Token from {}...".format(card.Name))
			card.markers[DissipateToken] -= 1 # Remove Token
			if card.markers[DissipateToken] == 0 and card.Name == "Rolling Fog": # Only discard Rolling Fog for now
				notify("{} discards {} as it no longer has any Dissipate Tokens".format(me, card.Name))
				card.moveTo(me.piles['Discard'])
			notify("Finished auto-resolving Dissipate for {}.".format(me))

	#use the logic for Dissipate for Disable Markers
	cardsWithDisable = [c for c in table if c.markers[Disable] and c.controller == me]
	if len(cardsWithDisable) > 0:
		notify("Resolving Disable Markers for {}...".format(me))	#found at least one
		for card in cardsWithDisable:
			notify("{} removes a Disable Marker from {}".format(me, c.name))	#found at least one
			card.markers[Disable] -= 1 # Remove Marker
			notify("Finished auto-resolving Disable Markers for {}.".format(me))

def resolveLoadTokens():
	mute()
	loadTokenCards = [card for card in table if card.Name in ["Ballista", "Akiro's Hammer"] and card.controller == me and card.isFaceUp ]
	for card in loadTokenCards:
		notify("Resolving Load Tokens for {}...".format(me))	#found at least one
		if card.markers[LoadToken] == 0:
			notify("Placing the First Load Token on {}...".format(card.Name)) #found no load token on card
			card.markers[LoadToken] = 1
		elif card.markers[LoadToken] == 1:
			notify("Placing the Second Load Token on {}...".format(card.Name)) #found one load token on card
			card.markers[LoadToken] = 2
		notify("Finished adding Load Tokens for {}.".format(me))

def resolveStormTokens():
	mute()
	stormTokenCards = [card for card in table if card.Name in ["Staff of Storms"] and card.controller == me and card.isFaceUp ]
	for card in stormTokenCards:
		if card.markers[StormToken] ==4:
			return
		notify("Resolving Storm Tokens for {}...".format(me))	#found at least one
		if card.markers[StormToken] == 0 or card.markers[StormToken] < 4:
			notify("Placing a Storm Token on the {}...".format(card.Name)) #Card needs a load token
			card.markers[StormToken] += 1
		notify("Finished adding Storm Tokens for {}.".format(me))

def resolveChanneling(p):
	mute()
	for c in table:
				if c.controller==me and c.isFaceUp:
						if c.Stats != None and c.Subtype != "Mage":
								if "Channeling=" in c.Stats: #let's add mana for spawnpoints etc.
										channel = getStat(c.Stats,"Channeling")
										channelBoost = len([k for k in table if k.isFaceUp and k.name == "Harmonize" and c == getAttachTarget(k)]) #Well, you can't really attach more than 1 harmonize anyway. But if there were another spell that boosted channeling, we could add it to this list.
										debug("Found Channeling stat {} in card {}".format(channel,c.name))
										for x in range(channel+channelBoost):
												addMana(c)
						if c.name == "Barracks": #has the channeling=X stat
								debug("Found Barracks")
								x = 0
								for c2 in table:
										if c2.isFaceUp and c2.Subtype != "" and c2.Subtype != None:
												#debug("owners {} {}".format(c.owner,c2.owner))
												if "Outpost" in c2.Subtype and c.owner == c2.owner:
														debug("Found Outpost")
														addMana(c)
														x += 1
										if x == 3: #max 3 outpost count.
												break
	if p == me:
		me.Mana += me.Channeling
		notify("{} channels {} mana.".format(me.name,me.Channeling))

def resolveUpkeep():
	mute()
	#is the setting on?
	if not getSetting("AutoResolveUpkeep", True):
		return
	Upkeep = "Upkeep"
	MordoksObeliskInPlay = 0
	HarshforgeMonolithInPlay = 0
	ManaPrismInPlay = 0
	PsiOrbDisc = 0
	upKeepIgnoreList = ["Essence Drain","Mind Control","Stranglevine","Mordok's Obelisk","Harshforge Monolith","Psi-Orb", "Mana Prism"]
	for card in table:
		if card.Name == "Mordok's Obelisk" and card.isFaceUp:
			MordoksObeliskInPlay = 1
			MordoksObelisk = card
		if card.Name == "Harshforge Monolith" and card.isFaceUp:
			HarshforgeMonolithInPlay = 1
			HarshforgeMonolith = card
		if card.name == "Mana Prism" and card.isFaceUp and card.controller == me:
			ManaPrismInPlay = 1
			ManaPrism = card
		if card.Name == "Psi-Orb" and card.isFaceUp and card.controller == me: # if the player has Psi-Orb in play set Discount to 3
			PsiOrbDisc = 3
			if PsiOrbDisc == 3: notify("The PSI-Orb has {} Upkeep discounts avaialbe this Round.".format(PsiOrbDisc))

	for card in table:
		upKeepCost = 0
		obeliskUpKeepCost = 0
		monolithUpKeepCost = 0
		# Process Upkeep for Harshforge Monolith
		if card.Type == "Enchantment" and card.controller == me and HarshforgeMonolithInPlay == 1:
			monolithUpKeepCost = 1
			aZone = getZoneContaining(card)
			bZone = getZoneContaining(HarshforgeMonolith)
			distance = zoneGetDistance(aZone,bZone)
			if card.isFaceUp:
				notifystr = "Do you wish to pay the Upkeep +1 cost for your Face Up {} from Harshforge Monolith's effect?".format(card.Name)
			else:
				notifystr = "Do you wish to pay the Upkeep +1 cost for your Face Down {} from Harshforge Monolith's effect?".format(card.Name)
			if distance < 2:
				processUpKeep(monolithUpKeepCost, card.Name, HarshforgeMonolith, notifystr)
				if ManaPrismInPlay == 1:
					addToken(ManaPrism, Mana)
		# Process Upkeep for Mordok's Obelisk's
		if card.Type == "Creature" and card.controller == me and MordoksObeliskInPlay == 1 and card.isFaceUp:
			obeliskUpKeepCost = 1
			notifystr = "Do you wish to pay the Upkeep +1 cost for {} from Mordok's Obelisk's effect?".format(card.Name)
			processUpKeep(obeliskUpKeepCost, card, MordoksObelisk, notifystr)
			if ManaPrismInPlay == 1:
				addToken(ManaPrism, Mana)
		 # Process Upkeep for Cards with the Upkeep Card Trait
		if not card.Name in upKeepIgnoreList and "Upkeep" in card.Traits and card.controller == me and card.isFaceUp:
			upKeepCost = getTraitValue(card, "Upkeep")
			if PsiOrbDisc > 0 and "Mind" in card.school:
				PsiOrbDisc, notifystr, upKeepCost = processPsiOrb(card, PsiOrbDisc, upKeepCost)
			else:
				if isAttached(card) == True:
					attatchedTo = getAttachTarget(card)
					notifystr = "Do you wish to pay the Upkeep +{} cost for {} attached to {}?".format(upKeepCost, card.Name, attatchedTo.Name)
				else:
					notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(upKeepCost, card.Name)
		# Process Upkeep for Cards with the Upkeep Trait in the Card Text that is attached to Objects (Creatures)
		elif not card.Name in upKeepIgnoreList and "[Upkeep" in card.Text and card.controller == me and card.isFaceUp and isAttached(card) == True:
			attatchedTo = getAttachTarget(card)
			upKeepCost = getTextTraitValue(card, "Upkeep")
			if PsiOrbDisc > 0 and "Mind" in card.school:
				PsiOrbDisc, notifystr, upKeepCost = processPsiOrb(card, PsiOrbDisc, upKeepCost)
			else:
				notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(upKeepCost, card.Name, attatchedTo.Name)
		# Process Upkeep for Essence Drain
		elif card.Name == "Essence Drain" and card.controller != me and card.isFaceUp:
			upKeepCost = getTextTraitValue(card, "Upkeep")
			if PsiOrbDisc > 0 and "Mind" in card.school:
				PsiOrbDisc, notifystr, upKeepCost = processPsiOrb(card, PsiOrbDisc, upKeepCost)
			else:
				notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(upKeepCost, card.Name)
				processUpKeep(upKeepCost, card, Upkeep, notifystr)
				if ManaPrismInPlay == 1:
					addToken(ManaPrism, Mana)
				upKeepCost = 0
		# Process Upkeep for Mind Control
		elif card.Name == "Mind Control" and card.controller == me and card.isFaceUp and isAttached(card) == True:
			attatchedTo = getAttachTarget(card)
			upKeepCost = int(attatchedTo.level)
			if PsiOrbDisc > 0 and "Mind" in card.school:
				PsiOrbDisc, notifystr, upKeepCost = processPsiOrb(card, PsiOrbDisc, upKeepCost)
			else:
				notifystr = "Do you wish to pay the Upkeep +{} cost for the {} attached to {}?".format(upKeepCost, card.Name, attatchedTo.Name)
		# Process Upkeep for Stranglevine
		else:
			if card.Name == "Stranglevine" and card.controller == me and card.isFaceUp and isAttached(card) == True:
				attatchedTo = getAttachTarget(card)
				notify("{} has a Stranglevine attached to it adding a Crush token...".format(attatchedTo.name))
				card.markers[CrushToken] += 1
				upKeepCost = card.markers[CrushToken]
				notifystr = "Do you wish to pay the Upkeep +{} cost for {} attached to {}?".format(upKeepCost, card.Name, attatchedTo.Name)

		if upKeepCost >= 1:
			processUpKeep(upKeepCost, card, Upkeep, notifystr)

def processPsiOrb(card, PsiOrbDisc, upKeepCost):
	mute()
	debug("Psi-Orb Discount: {} and Card Name: {} Card School: {}".format(str(PsiOrbDisc),card.name, card.school))
	PsiOrbDisc -= 1
	notify("{} uses the Psi-Orb to pay 1 less Upkeep for {}, there are {} remaining Upkeep discounts left for this Round.".format(me,card.name,PsiOrbDisc))
	upKeepCost = upKeepCost - 1
	notifystr = "Do you wish to pay the Upkeep +{} cost for {} after the 1 Mana Discount from the Psi-Orb?".format(upKeepCost, card.Name)
	return PsiOrbDisc, notifystr, upKeepCost

def processUpKeep(upKeepCost, card1, card2, notifystr):
	mute()
	upKeepCost = upKeepCost
	card1 = card1
	card2 = card2
	notifystr = notifystr

	if me.Mana < upKeepCost:
		card1.moveTo(me.piles['Discard'])
		notify("{} was unable to pay Upkeep cost for {} from {} effect and has placed {} in the discard pile.".format(me, card1, card2, card1))
		return
	else:
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		#whisper("{} {}".format(me, notifystr))
		if choice == 1 and card1.isFaceUp:
			me.Mana -= upKeepCost
			notify("{} pays the Upkeep cost of {} for {}".format(me, upKeepCost, card1, card2))
			if card1.Name == "Stranglevine" and card1.controller == me and card1.isFaceUp and isAttached(card1) == True:
				attatchedTo = getAttachTarget(card1)
				damage = card1.markers[CrushToken]
				remoteCall(attatchedTo.controller,"stranglevineReceiptPrompt",[attatchedTo,damage])
			else:
				if card1.Name == "Forcefield" and card1.controller == me and card1.isFaceUp and card1.markers[FFToken] < 3:
					card1.markers[FFToken] += 1
					notify("{} adds a Forcefield token to {}, which has a total of {} Forcefield tokens now.".format(me.name,card1.name, card1.markers[FFToken]))
			return
		if choice == 1 and not card1.isFaceUp:
			me.Mana -= upKeepCost
			notify("{} pays the Upkeep cost of {} for the mage's Face Down Enchantment".format(me, upKeepCost, card1))
			return
		else:
			card1.moveTo(me.piles['Discard'])
			notify("{} has chosen not to pay the Upkeep cost for {} effect on {} and has placed {} in the discard pile.".format(me, card2, card1, card1))
			return

def stranglevineReceiptPrompt(card,damage):#I suppose this would really be better done as a generic damage receipt prompt but...Q2.
		mute()
		if askChoice("Apply {} damage to {} from Stranglevine?".format(str(damage),card.Name.split(",")[0]),["Yes","No"],["#01603e","#de2827"])==1:
				if card.Subtype == "Mage": card.controller.damage += damage
				else: card.markers[Damage] += damage
				strangleMessages=["Stranglevine tightens its hold on {}! ({} damage)",
								  "As Stranglevine grows, its hold on {} tightens! ({} damage)",
								  "{} is constricted by Stranglevine! ({} damage)",
								  "Stranglevine crushes {}! ({} damage)",
								  "Stranglevine writhes and constricts {}! ({} damage)"]
				message=rnd(0,len(strangleMessages)-1)
				notify(strangleMessages[message].format(card,str(damage)))
				traitsDict = computeTraits(card)
				if getRemainingLife(traitsDict) == 0: deathPrompt(traitsDict)

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

def toggleDebug(group, x=0, y=0):
	global debugMode
	debugMode = not debugMode
	if debugMode:
		notify("{} turns on debug".format(me))
	else:
		notify("{} turns off debug".format(me))

############################################################################
######################		Chat Actions			################################
############################################################################
def sayYes(group, x=0, y=0):
	notify("{} says Yes".format(me.name))

def sayNo(group, x=0, y=0):
	notify("{} says No".format(me.name))

def sayPass(group, x=0, y=0):
	notify("{} says Pass".format(me.name))

def sayThinking(group, x=0, y=0):
	notify("{} says I am thinking....".format(me.name))

def askThinking(group, x=0, y=0):
	notify("{} asks are you thinking?".format(me.name))

def askYourTurn(group, x=0, y=0):
	notify("{} asks is it your turn?".format(me.name))

def askMyTurn(group, x=0, y=0):
	notify("{} asks is it my turn?".format(me.name))

def askRevealEnchant(group, x=0, y=0):
	notify("{} asks do you wish to Reveal your Enchantment?".format(me.name))

############################################################################
######################		Card Actions			################################
############################################################################

##########################     Add/Subtract Tokens     ##############################

tokenList=['Armor',
		   'Banish',
		   'Bleed',
		   'Burn',
		   'Cripple',
		   'Corrode',
		   'Disable',
		   'Daze',
		   'Growth',
		   'Mana',
		   'Melee',
		   'Rage',
		   'Ranged',
		   'Rot',
		   'Slam',
		   'Stun',
		   'Stuck',
		   'Sleep',
		   'Tainted',
		   'Veteran',
		   'Weak',
		   'Wrath',
		   'Zombie'
		   ]

for token in tokenList:
		exec('def add'+token+'(card, x = 0, y = 0):\n\taddToken(card,'+token+')')
		exec('def sub'+token+'(card, x = 0, y = 0):\n\tsubToken(card,'+token+')')

def addControlMarker(card, x = 0, y = 0):
	mute()
	placeControlMarker(me,card)

def placeControlMarker(attacker,defender):
	mute()
	#First, If orb is off, turn it on
	if defender.alternate == "":
		defender.switchTo('B')
		notify("{} flips V'Tar Orb On.".format(me))
	#Second, check to see if there is a control marker on the Orb already and if so remove it
	markerColor = playerColorDict[int(attacker.getGlobalVariable("MyColor"))]["ControlMarker"]
	if defender.markers[markerColor] == 1:
		notify("{} already has control of the V'tar Orb!".format(attacker.name))
		return
	elif sum([defender.markers[m] for m in listControlMarkers]) > 0:
		for m in listControlMarkers:
			defender.markers[m] = max(defender.markers[m]-1,0)
		notify("{} neutralizes the V'tar Orb!".format(attacker.name))
	else:
		defender.markers[markerColor] = 1
		notify("{} asserts control over the V'tar Orb!\nIndicating control using a {}.".format(attacker.name,markerColor[0]))

def addDamage(card, x = 0, y = 0):
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if "Mage" in card.Subtype and card.controller == me:
		me.Damage += 1
	else:
		addToken(card, Damage)

def addOther(card, x = 0, y = 0):
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	marker, qty = askMarker()
	if qty == 0:
		return
	card.markers[marker] += qty

def subDamage(card, x = 0, y = 0):
	if card.Subtype == "Mage" and card.controller == me:
			me.Damage -= 1
	else:
		subToken(card, Damage)

def clearTokens(card, x = 0, y = 0):
	mute()
	for tokenType in card.markers:
		card.markers[tokenType] = 0
	notify("{} removes all tokens from {}".format(me, card.Name))

##########################     Toggle Actions/Tokens     ##############################


def toggleAction(card, x=0, y=0):
	mute()
	myColor = int(me.getGlobalVariable("MyColor"))
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if myColor == "0":
		whisper("Please perform player setup to initialize player color")
	elif myColor == 1: # Red
		if card.markers[ActionRedUsed] > 0:
			card.markers[ActionRed] = 1
			card.markers[ActionRedUsed] = 0
			notify("{} readies Action Marker".format(card.Name))
		else:
			card.markers[ActionRed] = 0
			card.markers[ActionRedUsed] = 1
			notify("{} spends Action Marker".format(card.Name))
	elif myColor == 2: # Blue
		if card.markers[ActionBlueUsed] > 0:
			card.markers[ActionBlue] = 1
			card.markers[ActionBlueUsed] = 0
			notify("{} readies Action Marker".format(card.Name))
		else:
			card.markers[ActionBlue] = 0
			card.markers[ActionBlueUsed] = 1
			notify("{} spends Action Marker".format(card.Name))
	elif myColor == 3: #Green
		if card.markers[ActionGreenUsed] > 0:
			card.markers[ActionGreen] = 1
			card.markers[ActionGreenUsed] = 0
			notify("{} readies Action Marker".format(card.Name))
		else:
			card.markers[ActionGreen] = 0
			card.markers[ActionGreenUsed] = 1
			notify("{} spends Action Marker".format(card.Name))
	elif myColor == 4: #Yellow
		if card.markers[ActionYellowUsed] > 0:
			card.markers[ActionYellow] = 1
			card.markers[ActionYellowUsed] = 0
			notify("{} readies Action Marker".format(card.Name))
		else:
			card.markers[ActionYellow] = 0
			card.markers[ActionYellowUsed] = 1
			notify("{} spends Action Marker".format(card.Name))
	elif myColor == 5: #Purple
		if card.markers[ActionPurpleUsed] > 0:
			card.markers[ActionPurple] = 1
			card.markers[ActionPurpleUsed] = 0
			notify("{} readies Action Marker".format(card.Name))
		else:
			card.markers[ActionPurple] = 0
			card.markers[ActionPurpleUsed] = 1
			notify("{} spends Action Marker".format(card.Name))
	elif myColor == 6: #Grey
		if card.markers[ActionGreyUsed] > 0:
			card.markers[ActionGrey] = 1
			card.markers[ActionGreyUsed] = 0
			notify("{} readies Action Marker".format(card.Name))
		else:
			card.markers[ActionGrey] = 0
			card.markers[ActionGreyUsed] = 1
			notify("{} spends Action Marker".format(card.Name))

def toggleDeflect(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[DeflectR] > 0:
		card.markers[DeflectR] = 0
		card.markers[DeflectU] = 1
		notify("{} uses deflect".format(card.Name))
	else:
		card.markers[DeflectR] = 1
		card.markers[DeflectU] = 0
		notify("{} readies deflect".format(card.Name))

def toggleGatetoHell(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[GateClosed] > 0:
		card.markers[GateClosed] = 0
		card.markers[GateOpened] = 1
		notify("The Gate to Hell has been Opened!")
	else:
		card.markers[GateClosed] = 1
		card.markers[GateOpened] = 0
		notify("The Gate to Hell has been Closed!")

def toggleGuard(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	toggleToken(card, Guard)

def toggleInvisible(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[Invisible] > 0:
		card.markers[Invisible] = 0
		card.markers[Visible] = 1
		notify("{} becomes visible".format(card.Name))
	else:
		card.markers[Invisible] = 1
		card.markers[Visible] = 0
		notify("{} becomes invisible".format(card.Name))

def toggleReady(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[Ready] > 0:
		card.markers[Ready] = 0
		card.markers[Used] = 1
		notify("{} spends the Ready Marker on {}".format(me, card.Name))
	else:
		card.markers[Ready] = 1
		card.markers[Used] = 0
		notify("{} readies the Ready Marker on {}".format(me, card.Name))

def toggleReadyII(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[ReadyII] > 0:
		card.markers[ReadyII] = 0
		card.markers[UsedII] = 1
		notify("{} spends the Ready Marker II on {}".format(me, card.Name))
	else:
		card.markers[ReadyII] = 1
		card.markers[UsedII] = 0
		notify("{} readies the Ready Marker II on {}".format(me, card.Name))

def toggleQuick(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[Quick] > 0:
		card.markers[Quick] = 0
		card.markers[QuickBack] = 1
		notify("{} spends Quickcast action".format(card.Name))
	else:
		card.markers[Quick] = 1
		card.markers[QuickBack] = 0
		notify("{} readies Quickcast Marker".format(card.Name))

def toggleVoltaric(card, x=0, y=0):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList or not card.isFaceUp: return
	if card.markers[VoltaricON] > 0:
		card.markers[VoltaricON] = 0
		card.markers[VoltaricOFF] = 1
		notify("{} disables Voltaric shield".format(card.Name))
	else:
		choice = askChoice('Do you want to enable your Voltaric Shield by paying 2 mana?'['Yes','No'],["#171e78","#de2827"])
		if choice == 1:
			if me.Mana < 2:
				notify("{} has insufficient mana in pool".format(me))
				return
			me.Mana -= 2
			card.markers[VoltaricON] = 1
			card.markers[VoltaricOFF] = 0
			notify("{}  spends two mana to enable his Voltaric shield".format(me))
		else: notify("{} chose not to enable his Voltaric shield".format(me))

############################################################################
######################		Other  Actions		################################
############################################################################


def rotateCard(card, x = 0, y = 0):
	# Rot90, Rot180, etc. are just aliases for the numbers 0-3
	mute()
	if card.controller == me:
		card.orientation = (card.orientation + 1) % 4
		if card.isFaceUp:
			notify("{} Rotates {}".format(me, card.Name))
		else:
			notify("{} Rotates a card".format(me))

def flipcard(card, x = 0, y = 0):
	mute()
	tutorialMessage("Advance Phase")
	cardalt = card.alternates
	cZone = getZoneContaining(card)
	# markers that are cards in game that have two sides
	if "Vine Marker" in card.Name and card.controller == me:
		if card.alternate == '':
			card.switchTo('B')
			notify("{} flips the Vine Marker to use its Black side.".format(me))
		else:
			card.switchTo('')
			notify("{} flips the Vine Marker to use its Green side.".format(me))
		return
	elif "Alt Zone" in card.Name and card.controller == me:
		if card.alternate == "B":
			card.switchTo('')
		else:
			card.switchTo('B')
		notify("{} flips Zone Marker.".format(me))
		return
	elif "V'Tar Orb" in card.Name and card.controller == me:
		if card.alternate == "B":
			card.switchTo('')
			notify("{} flips V'Tar Orb Off".format(me))
		else:
			card.switchTo('B')
			notify("{} flips V'Tar Orb On.".format(me))
		return
	elif "Player Token" in card.Name:
		nextPlayer = getNextPlayerNum()
		debug(nextPlayer)
		setGlobalVariable("PlayerWithIni", str(nextPlayer))
		for p in players:
			remoteCall(p, "changeIniColor", [card])

	# do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList: return
	# normal card flipping processing starts here
	if card.isFaceUp == False:
		card.isFaceUp = True
		if card.Type != "Enchantment"  and "Conjuration" not in card.Type: #leaves the highlight around Enchantments and Conjurations
			card.highlight = None
		if card.Type == "Creature": #places action marker on card
			toggleAction(card)
		if card.Subtype == "Mage": #once more to flip action to active side
			toggleAction(card)
			toggleQuick(card)
			if "Wizard" in card.Name:
					card.markers[VoltaricOFF] = 1
			if "Forcemaster" == card.Name:
					card.markers[DeflectR] = 1
			if "Beastmaster" == card.Name:
					card.markers[Pet] = 1
			if "Johktari Beastmaster" == card.Name:
					card.markers[WoundedPrey] = 1
			if "Priest" == card.Name:
					card.markers[HolyAvenger] = 1
			if "Druid" == card.Name:
					card.markers[Treebond] = 1
			if "Necromancer" == card.Name:
					card.markers[EternalServant] = 1
			if "Warlock" == card.Name:
					card.markers[BloodReaper] = 1
		if "Anvil Throne Warlord Stats" == card.Name:
					card.markers[RuneofFortification] = 1
					card.markers[RuneofPower] = 1
					card.markers[RuneofPrecision] = 1
					card.markers[RuneofReforging] = 1
					card.markers[RuneofShielding] = 1
		if card.Name in typeChannelingList and card.controller == me and card.isFaceUp == True:
			notify("{} increases the Channeling stat by 1 as a result of {} being revealed".format(me, card))
			me.Channeling += 1
		if "Harmonize" == card.Name and card.controller == me and isAttached(card) and card.isFaceUp == True:
			magecard = getAttachTarget(card)
			if magecard.Subtype == "Mage":
				notify("{} increases the Channeling stat by 1 as a result of {} being revealed".format(me, card))
				me.Channeling += 1
		if card.Type == "Creature":
			if "Invisible Stalker" == card.Name:
					card.markers[Invisible] = 1
			if "Thorg, Chief Bodyguard" == card.Name:
					card.markers[TauntT] = 1
			if "Sosruko, Ferret Companion" == card.Name:
					card.markers[Taunt] = 1
			if "Skeelax, Taunting Imp" == card.Name:
					card.markers[TauntS] = 1
			if "Ichthellid" == card.Name:
					card.markers[EggToken] = 1
			if "Talos" == card.Name:
					toggleAction(card)
			if "Orb Guardian" in card.name and card.special == "Scenario" and [1 for c in getCardsInZone(myZone) if "V'Tar Orb" in c.name]:
					card.markers[Guard] = 1
		if card.Type == "Conjuration":
			if "Ballista" == card.Name:
				card.markers[LoadToken] = 1
			if "Akiro's Hammer" == card.Name:
				card.markers[LoadToken] = 1
			if "Corrosive Orchid" == card.Name:
				card.markers[MistToken] = 1
			if "Nightshade Lotus" == card.Name:
				card.markers[MistToken] = 1
			if "Rolling Fog" == card.Name:
				card.markers[DissipateToken] = 3
			if "Gate to Hell" == card.Name:
				card.markers[GateClosed] = 1
		if "Defense" in card.Stats and not card.Name=="Forcemaster":
			if "1x" in card.Stats:
				card.markers[Ready] = 1
			if "2x" in card.Stats:
				card.markers[Ready] = 1
				card.markers[ReadyII] = 1
		if "Forcefield" == card.Name:
			card.markers[FFToken] = 3
		if "[ReadyMarker]" in card.Text:
			card.markers[Ready] = 1
	elif card.isFaceUp and not "B" in cardalt:
		notify("{} turns {} face down.".format(me, card.Name))
		card.isFaceUp = False
		card.peek()
	elif card.isFaceUp and "B" or "C" in cardalt:
		if card.alternate == '':
			notify("{} flips {} to the alternate version of the card.".format(me, card))
			card.switchTo('B')
		elif card.alternate == 'B' and 'C' in cardalt:
			notify("{} flips {} to the alternate version of the card.".format(me, card))
			card.switchTo('C')
		else:
			notify("{} flips {} to the standard version of the card.".format(me, card))
			card.switchTo()

def getNextPlayerNum():
	debug(getGlobalVariable("PlayerWithIni"))
	activePlayer = int(getGlobalVariable("PlayerWithIni"))
	nextPlayer = activePlayer + 1
	if nextPlayer > len(getPlayers()):
		nextPlayer = 1
	return nextPlayer

def changeIniColor(card):
	mute()
	myColor = me.getGlobalVariable("MyColor")
	mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
	if mwPlayerDict[me._id]["PlayerNum"] == int(getGlobalVariable("PlayerWithIni")):
		card.switchTo(myColor)
	else:
		remoteCall(card.controller, "remoteSwitchPhase", [card, "myColor", ""])

def discard(card, x=0, y=0):
	mute()
	#[formatCardObject(c) for c in table if c.Type == "Creature"]
	#[c.onDiscard(card) for c in table if c.Type == "Creature"] #Testing the new discard method
	if card.controller != me:
		whisper("{} does not control {} - discard cancelled".format(me, card))
		return
	if card.Name in typeChannelingList and card.controller == me and card.isFaceUp == True:
			notify("{} decreases the Channeling stat by 1 because {} is being discarded".format(me, card))
			me.Channeling -= 1
	elif "Harmonize" == card.Name and card.controller == me:
		discardedCard = getAttachTarget(card)
		if card.Subtype == "Mage":
			notify("{} decreases the Channeling stat by 1 as a result of {} being discarded".format(me, card))
			me.Channeling -= 1
	elif card.special == "Scenario":
		obliterate(card)
		return
	card.isFaceUp = True
	detach(card)
	card.moveTo(me.piles['Discard'])
	notify("{} discards {}".format(me, card))

def obliterate(card, x=0, y=0):
	mute()
	if card.controller != me:
		whisper("{} does not control {} - card obliteration cancelled".format(me, card))
		return
	if card.Name in typeChannelingList and card.controller == me and card.isFaceUp == True:
			notify("{} decreases the Channeling stat by 1 because {} has been obliterated".format(me, card))
			me.Channeling -= 1
	elif "Harmonize" == card.Name and card.controller == me:
		discardedCard = getAttachTarget(card)
		if card.Subtype == "Mage":
			notify("{} decreases the Channeling stat by 1 because {} has been obliterated".format(me, card))
			me.Channeling -= 1
	else:
			notify("{} obliterates {}".format(me, card))
	card.isFaceUp = True
	detach(card)
	card.moveTo(me.piles['Obliterate Pile'])


def defaultAction(card,x=0,y=0):
	mute()
	if card.controller == me:
		if not card.isFaceUp:
			#is this a face-down enchantment? if so, prompt before revealing
			payForAttack = not (getSetting('BattleCalculator',True) and card.Type=='Attack')
			if card.Subtype == "Mage" or not payForAttack or card.Type == "Magestats": #Attack spells will now be paid for through the battlecalculator
				flipcard(card, x, y)

				if not getSetting('attackChangeNotified',False) and not payForAttack:
					whisper('Note: Mana for {} will be paid when you declare an attack using the Battle Calculator, or if you double-click on {} again.'.format(card,card))
					setSetting('attackChangeNotified',True)
			elif card.Type == "Enchantment": revealEnchantment(card)
			else: castSpell(card)

		else:
			if card.Type == "Incantation" or card.Type == "Attack": castSpell(card) #They can cancel in the castSpell prompt; no need to add another menu

############################################################################
######################		Utility Functions		########################
############################################################################

def addToken(card, tokenType):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	card.markers[tokenType] += 1
	if card.isFaceUp:
		notify("{} added to {}".format(tokenType[0], card.Name))
	else:
		notify("{} added to face-down card.".format(tokenType[0]))

def subToken(card, tokenType):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	if card.markers[tokenType] > 0:
		card.markers[tokenType] -= 1
		if card.isFaceUp:
			notify("{} removed from {}".format(tokenType[0], card.Name))
		else:
			notify("{} removed from face-down card.".format(tokenType[0]))

def toggleToken(card, tokenType):
	mute()
	if card.Type in typeIgnoreList or card.Name in typeIgnoreList: return  # do not place markers/tokens on table objects like Initative, Phase, and Vine Markers
	if card.markers[tokenType] > 0:
		card.markers[tokenType] = 0
		if card.isFaceUp:
			notify("{} removes a {} from {}".format(me, tokenType[0], card.Name))
		else:
			notify("{} removed from face-down card.".format(tokenType[0]))
	else:
		card.markers[tokenType] = 1
		if card.isFaceUp:
			notify("{} adds a {} token to {}".format(me, tokenType[0], card.Name))
		else:
			notify("{} added to face-down card.".format(tokenType[0]))

def playCardFaceDown(card, x=0, y=0):
	mute()
	tutorialMessage("Reveal Card")
	myHexColor = playerColorDict[eval(me.getGlobalVariable("MyColor"))]['Hex']
	card.isFaceUp = False
	moveCardToDefaultLocation(card)
	card.peek()
	card.highlight = myHexColor
	notify("{} prepares a Spell from their Spellbook by placing a card face down on the table.".format(me))

def moveCardToDefaultLocation(card,returning=False):#Returning if you want it to go to the returning zone
		mute()
		mapDict = eval(getGlobalVariable('Map'))
		mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
		#debug("\n" + str(mwPlayerDict))
		playerNum = mwPlayerDict[me._id]["PlayerNum"]
		x,y = 0,0
		if not card.isFaceUp: cardW,cardH = cardSizes[card.size()]['backWidth'],cardSizes[card.size()]['backHeight']
		else: cardW,cardH = cardSizes[card.size()]['width'],cardSizes[card.size()]['height']
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
			w,h = cardSizes[c.size()][wKey],cardSizes[c.size()][hKey]
			dx,dy = dVector
			return splay(x+dx*w,y+dy*h,dVector)
	return x,y

def debug(str):
	mute()
	global debugMode
	if debugMode:
		whisper("Debug Msg: {}".format(str))

def createCard(group,x=0,y=0):
		mute()
		global debugMode
		cardName = askString("Create which card?","Enter card name here")
		guid,quantity = askCard({'Name':cardName},title="Select card version and quantity")
		if guid and quantity:
				cards = ([table.create(guid,0,0,1,True)] if quantity == 1 else table.create(guid,0,0,quantity,True))
				for card in cards:
						card.moveTo(me.hand)
						if not debugMode:
							notify("*** ILLEGAL *** - Spellbook is no longer valid")
						notify("A card was created and was placed into {}'s spellbook.".format(me))


#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

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
	card.switchTo(phase)

def remoteDeleteCard(c):
	c.delete()

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def castSpell(card,target=None):
		#Figure out who is casting the spell
		binder = getBindTarget(card)
		caster = getBindTarget(card)
		if not caster or not ("Familiar" in caster.Traits or "Spawnpoint" in caster.Traits):
				casters = [d for d in table if d.Subtype == "Mage" and d.isFaceUp and d.controller == me]
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
				discountList = filter(lambda d: d[1]>0, map(lambda c: (c,getCastDiscount(c,card,target)),table)) #Find all discounts. It would be better to pass a list, but this isn't a bottleneck, so we'll make do for now.
				#Reduce printed cost by sum of discounts
				usedDiscounts = []
				discountAppend = usedDiscounts.append
				for c,d in discountList:
						if cost > 0: #Right now, all discounts are for 1 (except construction yard). If there is ever a 2-mana discount, we will need to adjust this to optimize discount use. Come to think of it, some discounts overlap, and we might want to optimize for those...well, we can cross that bridge when we reach it.
								discAmt = min(cost,d)
								cost -= discAmt
								discountAppend((c,discAmt)) #Keep track of which discounts we are applying, and how much of each was applied
						else: break #Stop if the cost of the spell reaches 0; we don't need any more discounts.
				#Ask the player how much mana they want to pay
				discountSourceNames = '\n'.join(map(lambda t: "{} (-{})".format(t[0].Name,str(t[1])),usedDiscounts))
				discountString = "The following discounts were applied: \n{}\n\n".format(discountSourceNames) if discountSourceNames else ""
				pronoun = {"Male":"he","Female":"she"}.get(getGender(caster),"it")
				casterString = "{} will pay what {} can. You will pay the rest.\n\n".format(caster.Name.split(",")[0],pronoun) if (caster.Subtype != "Mage" and caster.markers[Mana]) else ""
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
				if casterCost: notify("{} pays {} mana.".format(caster,str(casterCost)))
				cost -= casterCost
				if cost:
						if discountString =="":
							notify("{} pays {} mana.".format(me,str(cost)))
							me.Mana = max(me.Mana-cost,0)
						else:
							notify("{} pays {} mana with the following discount applied: {}.".format(me,str(cost),discountSourceNames))
							me.Mana = max(me.Mana-cost,0)
				for c,d in usedDiscounts: #track discount usage
						if c.Name=="Construction Yard": c.markers[Mana] -= d
						rememberAbilityUse(c)
				if card.Type == "Enchantment": notify("{} enchants {}!".format(caster,target.Name) if target else "{} casts an enchantment!".format(caster))
				elif card.Type == "Creature": notify("{} summons {}!".format(caster,card.Name))
				elif "Conjuration" in card.Type: notify("{} conjures {}!".format(caster,card.Name))
				else: notify("{} casts {}!".format(caster,card.Name))
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
						notify("{} pays {} mana.".format(me,str(cost)))
				for c,d in usedDiscounts: #track discount usage
						rememberAbilityUse(c)
				notify("{} reveals {}!".format(me,card.Name))
				flipcard(card)
				return True

def getCastDiscount(card,spell,target=None): #Discount granted by <card> to <spell> given <target>. NOT for revealing enchantments.
		if card.controller != spell.controller or not card.isFaceUp or card==spell: return 0 #No discounts from other players' cards or facedown cards!
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
					 (cName == "Enchanter's Ring" and target and target.controller == card.controller and target.type == "Creature" and sType == "Enchantment") or
					 (cName == "Ring of Asyra" and ("Holy" in sSchool) and sType == "Incantation") or
					 (cName == "Ring of Beasts" and sType == "Creature" and ("Animal" in sSubtype)) or
					 (cName == "Ring of Curses" and sType != "Enchantment" and ("Curse" in sSubtype)) or
					 (cName == "Druid's Leaf Ring" and sType != "Enchantment" and ("Plant" in sSubtype)) or
					 (cName == "Force Ring" and sType != "Enchantment" and ("Force" in sSubtype)) or
					 (cName == "Ring of Command" and sType != "Enchantment" and ("Command" in sSubtype)))):
						return 1
				#Discounts that apply no matter who casts the spell
				if ((cName == "General's Signet Ring" and ("Soldier" in sSubtype)) or
					(cName == "Eisenach's Forge Hammer" and (sType == "Equipment"))):
						return 1
				#Construction yard will be treated as a once-per-round discount.
				if (cName == "Construction Yard" and
					((not "Incorporeal" in spell.Traits and "War" in sSchool and "Conjuration" in sType) or ("Earth" in sSchool and sType=="Conjuration-Wall"))):
						return card.markers[Mana]
		if timesUsed <2: #Twice-per-round discounts
				if cName == "Death Ring" and (mageCast or spawnpointCast) and sType != "Enchantment" and ("Necro" in sSubtype or "Undead" in sSubtype):
						return 1
		return 0
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
							  (cName == "Ring of Command" and ("Command" in sSubtype))): return 1
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
		tLevel = int(sum(map(lambda x: int(x), target.Level.split('+'))))
		if name == "Mind Control":
				cost = 2*tLevel
		elif name in ["Charm","Fumble"]:
				cost = tLevel-1
		if cost == None: return #If it doesn't fit an exception, the player will have to handle it.
		traits = computeTraits(card)
		if target.Subtype=="Mage":
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
