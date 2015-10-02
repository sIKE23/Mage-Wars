


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
#	p.setActive()

def getStat(stats, stat): #searches stats string for stat and extract value
	statlist = stats.split(", ")
	for statitem in statlist:
		statval = statitem.split("=")
		if statval[0] == stat:
						try: return int(statval[1])
						except: return 0
	return 0
	
def cardX(card):
	x, y = card.position
	return x

def cardY(card):
	x, y = card.position
	return y

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
			if burnDamage > 0: notify("{} continues to Burn, {} damage was added!".format(card.Name, burnDamage))
			if burnRemoved > 0: notify("{} Burns were removed from {}.".format(burnsRemoved,card.Name))
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
				card.controller.Damage += bleedDamage
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
				processUpKeep(monolithUpKeepCost, card, HarshforgeMonolith, notifystr)
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
		if askChoice("Apply {} damage to {} from Stranglevine?".format(str(damage),card.Nickname),["Yes","No"],["#01603e","#de2827"])==1:
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
		card.alternate = myColor
	else:
		remoteCall(card.controller, "remoteSwitchPhase", [card, "myColor", ""])

def moveCardToDefaultLocation(card,returning=False):#Returning if you want it to go to the returning zone
		mute()
		mapDict = eval(getGlobalVariable('Map'))
		mwPlayerDict = eval(getGlobalVariable("MWPlayerDict"))
		#debug("\n" + str(mwPlayerDict))
		playerNum = mwPlayerDict[me._id]["PlayerNum"]
		x,y = 0,0
		if not card.isFaceUp: cardW,cardH = cardSizes[card.size]['backWidth'],cardSizes[card.size]['backHeight']
		else: cardW,cardH = cardSizes[card.size]['width'],cardSizes[card.size]['height']
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
			w,h = cardSizes[c.size][wKey],cardSizes[c.size][hKey]
			dx,dy = dVector
			return splay(x+dx*w,y+dy*h,dVector)
	return x,y

def debug(str):
	mute()
	global debugMode
	if debugMode:
		whisper("Debug Msg: {}".format(str))


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
	card.alternate = phase

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
				casterString = "{} will pay what {} can. You will pay the rest.\n\n".format(caster.Nickname,pronoun) if (caster.Subtype != "Mage" and caster.markers[Mana]) else ""
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

def rollDice2(dice):
	mute()
	
	mapDict = eval(getGlobalVariable('Map'))
	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me: c.delete()
	dieCardX, dieCardY = mapDict.get('DiceBoxLocation',(0,0))
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
	dieCard.anchor = (True)

	count = dice
	if count == 0:
		effectRoll = rollD12()
		attackRoll = [0,0,0,0,0,0]
	else:
		attackRoll, effectRoll = rollD6(count)

	damNormal = attackRoll[2] + 2* attackRoll[3]
	damPiercing = attackRoll[4] + 2* attackRoll[5]

	if getGlobalVariable("TableSetup") == "True": # if the table has been setup show the dice roll results on the table.
		for card in table:
			if card.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and card.controller == me:
				card.delete()
		dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
		dieCard.anchor = (True)

		dieCard.markers[attackDie[0]] = attackRoll[0]+attackRoll[1] # Blank Dice
		dieCard.markers[attackDie[2]] = attackRoll[2] # 1 Normal Damage
		dieCard.markers[attackDie[3]] = attackRoll[3] # 2 Normal Damage
		dieCard.markers[attackDie[4]] = attackRoll[4] # 1 Critical Damage
		dieCard.markers[attackDie[5]] = attackRoll[5] # 2 Critical Damage
		dieCard.markers[effectDie] = effectRoll

	playSoundFX('Dice')
	time.sleep(1)
	notify("{} rolled {} normal damage, {} critical damage, and {} on the effect die".format(me, damNormal, damPiercing, effectRoll))
	return (attackRoll, effectRoll)

def rollD6(dice):
	mute()
	notifyStr = ""
	diceBankD6 = eval(me.getGlobalVariable("DiceBankD6"))
	count = dice
	if (len(diceBankD6) < count): #diceBank running low - fetch more
		d6 = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code for effect roll: {}".format(d6[1]))
		if d6[1]==200: # Retrived random numbers from random.org
			diceBankD6 = d6[0].splitlines()
			notifyStr = "using Attack Dice rolled using the results from Random.org"
		else:
			while (len(diceBankD6) < 100):
				diceBankD6.append(rnd(0, 5))
				notifyStr = "using Attack Dice rolled using the results from the native randomizer"
	attackRoll = [0,0,0,0,0,0]
	for x in range(count):
		roll = int(diceBankD6.pop())
		attackRoll[roll] += 1
	effectRoll = rollD12()
	debug("Raw Attack Dice Roll results: {} {}".format(attackRoll, notifyStr))
	notify("{} rolls {} attack dice {}".format(me, count, notifyStr))

	me.setGlobalVariable("DiceBankD6", str(diceBankD6))
	return attackRoll, effectRoll

def rollD12():
	mute()
	diceBankD12 = eval(me.getGlobalVariable("DiceBankD12"))
	
	if (len(diceBankD12)) <= 1:
		d12 = webRead("http://www.random.org/integers/?num=100&min=0&max=11&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code for effect roll: {}".format(d12[1]))
		if d12[1] == 200:
			diceBankD12 = d12[0].splitlines()
			debug("Effect Die rolled using results from Random.org")
		else:
			while (len(diceBankD12) < 100):
				debug("Effect Die rolled using results from the native randomizer")
				diceBankD12.append(rnd(0, 11))

	effectRoll = int(diceBankD12.pop()) + 1
	me.setGlobalVariable("DiceBankD12", str(diceBankD12))
	return effectRoll