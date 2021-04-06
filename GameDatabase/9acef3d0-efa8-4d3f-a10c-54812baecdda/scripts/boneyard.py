#######
#v2.0.0.0#
#######

def getStat(stats, stat): #searches stats string for stat and extract value
	statlist = stats.split(", ")
	for statitem in statlist:
		statval = statitem.split("=")
		if statval[0] == stat:
						try: return int(statval[1])
						except: return 0
	return 0


##################################Upkeep######################################\


def resetMarkers():
	mute()
	for c in table:
		if c.targetedBy == me:
			c.target(False)
		if c.controller == me and c.isFaceUp and not "Alfiya" in c.Name: #don't waste time on facedown cards and only reset the markers on my cards.
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
			if "Packleader's Cowl" == c.Name: c.markers[Guard] = 1
			if "Lightning Raptor" == c.Name and c.markers[Charge]<5: c.markers[Charge] += 1
			#add a Guard Marker to Orb Guardians when they are in the same zone as an Orb
			if "Orb Guardian" in c.name:
					for o in table:
							isWithOrb = False
							if "V'Tar Orb" in o.name and (getZoneContaining(o) == getZoneContaining(c)): isWithOrb = True
							if isWithOrb: c.markers[Guard] = 1

	notify("{} resets all Action, Ability, Quickcast, and Ready Markers on the Mages cards by flipping them to their active side.\n".format(me.name))
	debug("card,stats,subtype {} {} {}".format(c.name,c.Stats,c.Subtype))

def resolveBurns(card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	notify("Resolving Burns for {}...\n".format(card.controller, card))	#found at least one
	numMarkers = card.markers[Burn]
	Damage = 0
	burnsRemoved = 0
	zone = getZoneContaining(card)
	isInZone = getCardsInZone(zone)
	for i in range(0, numMarkers):
		roll = rnd(0, 2)
		if roll == 0: 
			card.markers[Burn] -= 1
			burnsRemoved += 1
		Damage += roll
	#apply damage
	addDamageAmount(card,Damage)
	if Damage > 0: notify("Adramelech laughs while {} continues to Burn, {} damage was added!\n".format(card, Damage))
	if burnsRemoved > 0: notify("{} Burns were removed from {}.\n".format(burnsRemoved,card))
	#notify("Finished auto-resolving Burns for {}.".format(card))

def resolveRot(card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	notify("Resolving Rot for {}...\n".format(card.controller, card))	#found at least one
	Damage = (card.markers[Rot])
	#apply damage
	addDamageAmount(card,Damage)
	notify("{} damage added to {}.\n".format(Damage, card.Name))
	#notify("Finished auto-resolving Rot for {}.".format(card))

def resolveBleed(card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	notify("Resolving Bleed for {}\'s {}...\n".format(card.controller, card))	#found at least one
	Damage = (card.markers[Bleed])
	#apply damage
	addDamageAmount(card,Damage)
	notify("{} damage added to {}\'s {}.\n".format(Damage, card.controller, card.Name))
	#notify("Finished auto-resolving Bleed for {}.".format(card))
	
	
	
	
def resolveTalos(card):
	countOutposts = 0
	for c in table: #ugh - this is done much better in the next release
		if "Outpost" in c.Subtype and c.controller == me and c.isFaceUp:
				countOutposts += 1
	if countOutposts >= 3:
			card.markers[DominationToken] += 1
			notify("Placing a Domination Token on to the {}...\n".format(card))


def resolveDissipate(traits, card):
	mute()
#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
		
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	if card.controller == me and 'Dissipate' in traits and card.isFaceUp:# and (card.markers[DissipateToken] or card.markers[FermataBlue1] or card.markers[FermataBlue2] or card.markers[FermataGreen1] or card.markers[FermataGreen2]):
			notify("Resolving Dissipate for {}...\n".format(card))	#found at least one
			card.markers[DissipateToken] -= 1 # Remove Token
			if card.name == "Wispwillow Amulet" and card.controller == me and card.isFaceUp:
					me.Mana += 1
					notify("{} gains 1 Mana by removing a Dissipate Token from a Wispwillow Amulet.\n".format(me.name))
			else:
					notify("Removing 1 Dissipate Token from {}, there are {} Dissipate tokens left.\n".format(card.Name,card.markers[DissipateToken]))
			if not card.markers[DissipateToken] and card.controller == me:
					cardLevel = getCardLevel(card)
					#Siren Songs with Fermata Markers, process these first so we can return the Fermata marker to the stats card to use on another song during this Upkeep
					if "Song" in card.Subtype and card.isFaceUp and Card(mageID).Name == "Siren" and (card.markers[FermataBlue1] or card.markers[FermataGreen1]):
									if askChoice("Do you want to extend the Song {} for a second more Round by paying {} mana?".format(card.Name,str(cardLevel)),["Yes","No"],["#171e78","#de2827"]) == 1:
											# has chosen to extend the Song a Second round but can't pay
											if me.Mana < cardLevel:
													notify("{} has insufficient mana in pool and the Song {} has Expired.\n".format(me,card.Name))
													card.moveTo(me.piles['Discard'])
													return
											# has chosen to extend the Song a Second round and now pays
											me.Mana -= cardLevel
											if card.markers[FermataBlue1] > 0:
													card.markers[FermataBlue1] = 0
													card.markers[FermataBlue2] = 1
											elif card.markers[FermataGreen1] > 0:
													card.markers[FermataGreen1] = 0
													card.markers[FermataGreen2] = 1
											notify("{} has decided to extend the Song {} and pays {} mana.\n".format(me,card.Name,cardLevel))
					elif "Song" in card.Subtype and card.isFaceUp and Card(mageID).Name == "Siren" and (card.markers[FermataBlue2] or card.markers[FermataGreen2]): # Song has a Fermata 2 Marker on it, Song will expire during this Upkeep
						notify("{} discards {} as the Song has expired. The Fermata Marker has been placed back on {} Stats card.\n".format(me,card.Name,me)) # for testing
						if card.markers[FermataBlue2]:
							Card(mageStatsID).markers[FermataBlue1] = 1
						elif card.markers[FermataGreen2]:
							Card(mageStatsID).markers[FermataGreen1] = 1
						card.moveTo(me.piles['Discard Pile'])
							#notify("{} discards {} as the Song has expired. The Fermata Marker has been placed back on {} Stats card.".format(me,card.Name,me))
					#Siren Songs without Fermata Markers
					elif "Song" in card.Subtype and card.isFaceUp and Card(mageID).Name == "Siren" and (Card(mageStatsID).markers[FermataBlue1] == 1 or Card(mageStatsID).markers[FermataGreen1] == 1):
							if askChoice("Do you want to extend the Song {} for one Round by paying {} mana?".format(card.Name,str(cardLevel)),["Yes","No"],["#171e78","#de2827"]) == 1:
									if me.Mana < cardLevel:
											notify("{} has insufficient mana in pool and the Song {} has Expired.\n".format(me,card.Name))
											card.moveTo(me.piles['Discard'])
											return
									me.Mana -= cardLevel
									if Card(mageStatsID).markers[FermataBlue1] == 1:
											card.markers[FermataBlue1] = 1
											Card(mageStatsID).markers[FermataBlue1] = 0
											notify("{} has decided to extend the Song {}, and moves the Blue Fermata Marker to this Song.\n".format(me,card.Name))
									elif Card(mageStatsID).markers[FermataGreen1] == 1:
											card.markers[FermataGreen1] = 1
											Card(mageStatsID).markers[FermataGreen1] = 0
											notify("{} has decided to extend the Song {}.\n".format(me,card.Name))
							else:
									card.moveTo(me.piles['Discard Pile'])
									notify("{} discards {} has decided not to extend the Song and it has expired. The Fermata Marker has been placed back on the {} Stats card.\n".format(me, card.Name,me))
					else:
						notify("{} discards {} as it no longer has any Dissipate Tokens\n".format(me, card.Name))
						card.moveTo(me.piles['Discard Pile'])
	#notify("Finished auto-resolving Dissipate for {}.".format(me))

	
def resolveDisable(card):
		notify("{} removes a Disable Marker from {}\n".format(me, card.name))	#found at least one
		card.markers[Disable] -= 1 # Remove Marker
		#notify("Finished auto-resolving Disable Markers for {}.".format(me))

def resolveLoadTokens(card):
	mute()
	#loadTokenCards = [card for card in table if card.Name in ["Ballista", "Akiro's Hammer"] and card.controller == me and card.isFaceUp]
	#for card in loadTokenCards:
	notify("Resolving Load Tokens for {}\'s {}...\n".format(card.controller, card))	#found at least one
	if card.markers[LoadToken] == 0:
		notify("Placing the First Load Token on {}\'s {}...\n".format(card.controller, card)) #found no load token on card
		card.markers[LoadToken] = 1
	elif card.markers[LoadToken] == 1:
		notify("Placing the Second Load Token on {}\'s {}...\n".format(card.controller, card)) #found one load token on card
		card.markers[LoadToken] = 2
	#notify("Finished adding Load Tokens for {}.".format(card))

def resolveStormTokens(card):
	mute()
	#stormTokenCards = [card for card in table if card.Name in ["Staff of Storms"] and card.controller == me and card.isFaceUp ]
	#for card in stormTokenCards:
	if card.markers[StormToken] ==4:
		return
	notify("Resolving Storm Tokens for {}...\n".format(card))	#found at least one
	if card.markers[StormToken] == 0 or card.markers[StormToken] < 4:
		notify("A Storm Token appears on {}\'s {}...\n".format(me, card)) #Card needs a load token
		card.markers[StormToken] += 1
	#notify("Finished adding Storm Tokens for {}.".format(me))

def resolveChanneling(p):
	mute()
	for c in table:
				if c.controller==me and c.isFaceUp:
						if c.Stats != None and not "Mage" in c.Subtype:
								if "Channeling=" in c.Stats: #let's add mana for spawnpoints etc.
										traits = computeTraits(c)
										channel = getStat(c.Stats,"Channeling")
										channelBoost = 0
										channelBoost = len([k for k in table if k.isFaceUp and "Harmonize" in  k.name and c == getAttachTarget(k)]) #Well, you can't really attach more than 1 harmonize anyway. But if there were another spell that boosted channeling, we could add it to this list.
										if 'Channeling' in traits:
											channelBoost = traits['Channeling']
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
						if c.name == "Echo of the Depths":
							songFind = False
							for c2 in table:
								if c2.isFaceUp and "Song" in c2.Subtype and c2.Subtype != None:
									songFind = True
							if songFind == True:
								addMana(c)
							
	if p == me:
		me.Mana += me.Channeling
		notify("{} channels {} mana.\n".format(me.name,me.Channeling))

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
	upKeepIgnoreList = ["Essence Drain","Minor Essence Drain","Mind Control","Stranglevine","Mordok's Obelisk","Harshforge Monolith","Psi-Orb", "Mana Prism"]
	
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
			if PsiOrbDisc == 3: notify("The PSI-Orb has {} Upkeep discounts available this Round.\n".format(PsiOrbDisc))


	for card in table:
		traits = computeTraits(card)
		#debug("Card: {}".format(card.name))
		#debug("Card Controller: {}".format(card.controller.name))
		#debug("Card Mage: {}".format(Card(traits['MageID']).name))
		upKeepCost = 0
		obeliskUpKeepCost = 0
		monolithUpKeepCost = 0
		upKeepFilter = "#ABFFFFFF" #Light Blue - R=126 G=198 B=222
		# Process Upkeep for Harshforge Monolith
		if card.Type == "Enchantment" and card.controller == me and HarshforgeMonolithInPlay == 1:
			monolithUpKeepCost = 1
			aZone = getZoneContaining(card)
			bZone = getZoneContaining(HarshforgeMonolith)
			if aZone == None:
					debug("Error: Harshforge Monolith: Card Name: {}, aZone: {}, bZone: {}".format(card,aZone,bZone))
					continue
			distance = zoneGetDistance(aZone,bZone)
			if card.isFaceUp:
				notifystr = "Do you wish to pay the Upkeep +1 cost for your Face Up {} from Harshforge Monolith's effect?".format(card.Name)
			else:
				notifystr = "Do you wish to pay the Upkeep +1 cost for your Face Down {} from Harshforge Monolith's effect?".format(card.Name)
			if distance < 2:
				card.filter = upKeepFilter
				processUpKeep(monolithUpKeepCost, card, HarshforgeMonolith, notifystr)
				if ManaPrismInPlay == 1:
					addToken(ManaPrism, Mana)
		# Process Upkeep for Mordok's Obelisk's
		if card.Type == "Creature" and 'Mage' not in card.subtype and card.controller == me and MordoksObeliskInPlay == 1 and card.isFaceUp:
			obeliskUpKeepCost = 1
			notifystr = "Do you wish to pay the Upkeep +1 cost for {} from Mordok's Obelisk's effect?".format(card.Name)
			card.filter = upKeepFilter
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
			target = getAttachTarget(card)
			upKeepCost = getTextTraitValue(card, "Upkeep")
			if PsiOrbDisc > 0 and "Mind" in card.school:
				PsiOrbDisc, notifystr, upKeepCost = processPsiOrb(card, PsiOrbDisc, upKeepCost)
			else:
				notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(upKeepCost, card.Name)
				card.filter = upKeepFilter
				processUpKeep(upKeepCost, card, target, notifystr)
				if ManaPrismInPlay == 1:
					addToken(ManaPrism, Mana)
				upKeepCost = 0
		#Process Upkeep for Minor Essence Drain
		elif card.Name == "Minor Essence Drain" and card.controller != me and card.isFaceUp:
			target = getAttachTarget(card)
			upKeepCost = 1
			if PsiOrbDisc > 0 and "Mind" in card.school:
				PsiOrbDisc, notifystr, upKeepCost = processPsiOrb(card, PsiOrbDisc, upKeepCost)
			else:
				notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(upKeepCost, card.Name)
				card.filter = upKeepFilter
				processUpKeep(upKeepCost, card, target, notifystr)
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
		# Process Monk Upkeep
		elif 'Monk' in Card(traits['MageID']).name and card.Type in ["Equipment", "Enchantment"] and card.isFaceUp and "Monk" not in card.Subtype and "Martial" not in card.Subtype and "Mind" not in card.School and card.controller == me:
			target = getAttachTarget(card)
			upKeepCost = 1
			notifystr = "Do you wish to pay the Upkeep +{} cost for {}?".format(upKeepCost, card.Name)
			card.filter = upKeepFilter
		# Process Upkeep for Stranglevine
		else:
			if card.Name == "Stranglevine" and card.controller == me and card.isFaceUp and isAttached(card) == True:
				attatchedTo = getAttachTarget(card)
				notify("{} has a Stranglevine attached to it adding a Crush token...\n".format(attatchedTo.name))
				card.markers[CrushToken] += 1
				upKeepCost = card.markers[CrushToken]
				notifystr = "Do you wish to pay the Upkeep +{} cost for {} attached to {}?".format(upKeepCost, card.Name, attatchedTo.Name)

		if upKeepCost > 0:
			card.filter = upKeepFilter
			processUpKeep(upKeepCost, card, Upkeep, notifystr)

def processPsiOrb(card, PsiOrbDisc, upKeepCost):
	mute()
	debug("Psi-Orb Discount: {} and Card Name: {} Card School: {}".format(str(PsiOrbDisc),card.name, card.school))
	PsiOrbDisc -= 1
	notify("{} uses the Psi-Orb to pay 1 less Upkeep for {}, there are {} remaining Upkeep discounts left for this Round.\n".format(me,card.name,PsiOrbDisc))
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
		notify("{} was unable to pay Upkeep cost for {} from {} effect and has placed {} in the discard pile.\n".format(me, card1, card2, card1))
		return
	else:
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 and card1.isFaceUp:
			me.Mana -= upKeepCost
			card1.filter = None
			target = getAttachTarget(card1)
			notify("{} pays the Upkeep cost of {} for {} on the {}\n".format(me, upKeepCost, card1, target))
			if card1.Name == "Stranglevine" and card1.controller == me and card1.isFaceUp and isAttached(card1) == True:
				attatchedTo = getAttachTarget(card1)
				damage = card1.markers[CrushToken]
				if not "Finite Life" in computeTraits(card1): card1.statlife = str(2*card1.markers[CrushToken]+6)
				remoteCall(attatchedTo.controller,"stranglevineReceiptPrompt",[attatchedTo,damage])
			else:
				if card1.Name == "Forcefield" and card1.controller == me and card1.isFaceUp and card1.markers[FFToken] < 3:
					card1.markers[FFToken] += 1
					card1.filter = None
					notify("{} adds a Forcefield token to {}, which has a total of {} Forcefield tokens now.\n".format(me.name,card1.name, card1.markers[FFToken]))
				#'''Playtesting'''
				elif card1.Name == "The Void" and card1.controller == me and card1.isFaceUp:
					target.markers[Ki] +=1
					notify("Giving the {} 1 additional Ki".format(target))
			return
		if choice == 1 and not card1.isFaceUp:
			me.Mana -= upKeepCost
			notify("{} pays the Upkeep cost of {} for the mage's Face Down Enchantment\n".format(me, upKeepCost, card1))
			card1.filter = None
			return
		else:
			card1.moveTo(me.piles['Discard Pile'])
			notify("{} has chosen not to pay the Upkeep cost for {} effect on {} and has placed {} in the discard pile.\n".format(me, card2, card1, card1))
			return

def resolveMelting(traits, card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
	if ("FrozenTundra" in traits and "Melting" in traits) and card.controller == me and card.isFaceUp:
		notify("{} is in the Frozen Tundra and will not melt\n".format(card.name))
		return
	meltAmount = traits.get("Melting")
	#apply damage
	addDamageAmount(card,meltAmount)
	notify("{}\'s {} melts adding {} damage.\n".format(card.controller, card.Name, meltAmount))
	#notify("Finished auto-resolving Bleed for {}.".format(card))

def resolveRegeneration(traits, card):
 	mute()
 	#for card in table:
			#traits = computeTraits(card)
	if ("Regenerate" in traits and "Finite Life" in traits) and card.controller == me and card.isFaceUp:
			notify("{} has the Finite Life Trait and can not Regenerate\n".format(card.name))
			return
	elif "Regenerate" in traits and card.controller == me and card.isFaceUp:
			regenAmount = traits.get("Regenerate")
			if "Mage" in card.Subtype and card.controller == me and me.damage != 0:
					if me.damage <= regenAmount:
							me.damage = 0
							notify("{}\'s {} regenerates and removes all damage.\n".format(card.controller, card.name))
					else:
							me.damage -= regenAmount
							notify("{}\'s {} regenerates and removes {} damage.\n".format(card.controller, card.name, regenAmount))
			elif "Mage" in card.Subtype and card.controller == me and me.damage != 0:
					notify("{} is at full health.\n".format(card.name))
			elif card.Type in ['Creature','Conjuration','Conjuration-Wall','Conjuration-Terrain']:
					damage = card.markers[Damage]
					if damage <= regenAmount and damage != 0:
							card.markers[Damage] = 0
							notify("{}\'s {} regenerates and removes all damage.\n".format(card.controller, card.name))
					elif damage == 0:
							notify("{}\'s {} is at full health.\n".format(card.controller, card.name))
					else:
							card.markers[Damage] -= regenAmount
							notify("{}\'s {} regenerates and removes {} damage.\n".format(card.controller, card.name,regenAmount))
	if ("Lifegain" in traits and not "Finite Life" in traits) and card.controller == me and card.isFaceUp:
			lifeGainAmount = traits.get("Lifegain")
			me.Life += lifeGainAmount
			notify("{} gains {} Life from the brilliant glow of the Sunfire Amulet.\n".format(card.name,lifeGainAmount))
	elif ("Lifegain" in traits and "Finite Life" in traits) and card.controller == me and card.isFaceUp:
			notify("{} has the Finite Life Trait and can not gain Life\n".format(card.name))
			return

def resolveDotEnchantment(card):
 	mute()
	target = getAttachTarget(card)
	damageAmount = 0
	if "Ghoul Rot" in card.Name and card.controller == me and card.isFaceUp:
			damageAmount = 2
	if "Force Crush" in card.Name and card.controller == me and card.isFaceUp:
			damageAmount = 2
	elif "Curse of Decay" in card.Name and card.controller == me and card.isFaceUp:
			damageAmount = 1
	elif "Arcane Corruption" in card.Name and card.controller == me and card.isFaceUp:
		attachments = 	getAttachments(target)
		for attach in attachments:
			if attach.Type == "Enchantment" and attach.controller.name == target.controller.name:
				damageAmount +=1
	for p in players:
		if p.name == target.controller.name:
			remoteCall(p, "addDamageAmount", [target, damageAmount])
			notify("{}\'s {} feels the effects of the {} and takes {} damage.\n".format(target.controller, target, card, damageAmount))
			
def resolveAreaDot(traits, card):
 	mute()
	damageAmount = 0
	type = {'Malacoda':'',
			'Plagued':'',
			'Idol':'',
			'Consecrated':''}
	if "Malacoda" in traits and card.controller == me and card.isFaceUp:
			damageAmount += 2
			type['Malacoda'] = 'Malacoda, '
	if "Plagued" in traits and card.controller == me and card.isFaceUp:
			damageAmount += 1
			type['Plagued'] = 'Plagued, '
	if "Pestilence" in traits and card.controller == me and card.isFaceUp:
			damageAmount += 1
			type['Idol']= 'Idol of Pestilence, '
	if "Consecrated Ground Damage" in traits and card.controller == me and card.isFaceUp:
			damageAmount += 1
			type['Consecrated'] = 'Consecrated Ground;'
	if type['Malacoda'] != '' and (type['Plagued'] == '' and type['Idol'] == '' and type['Consecrated'] == ''):
			type['Malacoda'] = 'Malacoda;'
	elif type['Plagued'] != '' and (type['Idol'] == '' and type['Consecrated'] == ''):
			type['Plagued'] = 'Plagued;'
	elif type['Idol'] != '' and type['Consecrated'] == '':
			type['Idol'] = 'Idol of Pestilence;'
	for p in players:
		if p.name == card.controller.name:
			remoteCall(p, "addDamageAmount", [card, damageAmount])
			notify("{}\'s {} feels the effect of the following: ".format(card.controller,card) + "\n{Malacoda}\n{Plagued}\n{Idol}\n{Consecrated}\n".format(**type)+ "and takes {} damage.\n".format(damageAmount))
			

def resolveCurseItem(card):			
	mute()
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	notifystr = "Do you wish to take 2 damage to keep your {}?".format(card.Name)
	choiceList = ['Yes', 'No']
	colorsList = ['#0000FF', '#FF0000']
	choice = askChoice("{}".format(notifystr), choiceList, colorsList)
	if choice == 1:
		for p in players:
			if p.name == card.controller.name:
				remoteCall(p, "addDamageAmount", [Card(mageID), 2])
		notify("{}\'s {} is cursed! {} takes 2 damage from holding onto it!\n".format(me, card, me))
		return
	else:
		card.moveTo(me.piles['Discard Pile'])
		notify("{}\'s {} is cursed! {} throws it away before taking any damage!\n".format(me, card, me))
		return
			
def stranglevineReceiptPrompt(card,damage):#I suppose this would really be better done as a generic damage receipt prompt but...Q2.
		mute()
		if askChoice("Apply {} damage to {} from Stranglevine?".format(str(damage),card.Name.split(",")[0]),["Yes","No"],["#01603e","#de2827"])==1:
				addDamageAmount(card,damage)
				strangleMessages=["Stranglevine tightens its hold on {}! ({} damage)\n",
								  "As Stranglevine grows, its hold on {} tightens! ({} damage)\n",
								  "{} is constricted by Stranglevine! ({} damage)\n",
								  "Stranglevine crushes {}! ({} damage)\n",
								  "Stranglevine writhes and constricts {}! ({} damage)\n"]
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

def placeControlMarker(attacker,defender):
	mute()
	#First, If orb is off, turn it on
	if defender.alternate == "":
		defender.alternate = "B"
		notify("{} flips V'Tar Orb On.\n".format(me))
	#Second, check to see if there is a control marker on the Orb already and if so remove it
	markerColor = playerColorDict[int(attacker.getGlobalVariable("MyColor"))]["ControlMarker"]
	if defender.markers[markerColor] == 1:
		notify("{} already has control of the V'tar Orb!\n".format(attacker.name))
		return
	elif sum([defender.markers[m] for m in listControlMarkers]) > 0:
		for m in listControlMarkers:
			defender.markers[m] = max(defender.markers[m]-1,0)
		notify("{} neutralizes the V'tar Orb!\n".format(attacker.name))
	else:
		defender.markers[markerColor] = 1
		notify("{} asserts control over the V'tar Orb!\nIndicating control using a {}.\n".format(attacker.name,markerColor[0]))

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def remoteHighlight(card, color):
	card.highlight = color

def remoteSwitchPhase(card, phase, phrase):
	card.alternate = phase

def remoteDeleteCard(card):
	card.delete()

def returnToHand(card): #Return card to your hand
	card.moveTo(me.hand)

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def castSpell(card,target=None):
		#Figure out who is casting the spell
		binder = getBindTarget(card)
		caster = getBindTarget(card)
		if not caster or not ("Familiar" in caster.Traits or "Spawnpoint" in caster.Traits):
				casters = [d for d in table if "Mage" in d.Subtype and d.isFaceUp and d.controller == me and not "Magestats" in d.Type]
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
		debug("Caster: " + caster.Name)
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
				discountList = filter(lambda d: d[1][0]>0, [(c,getCastDiscount(c,card,target)) for c in table])
				#filter(lambda d: d[1]>0, map(lambda c: (c,getCastDiscount(c,card,target)),table)) #Find all discounts. It would be better to pass a list, but this isn't a bottleneck, so we'll make do for now.
				#Reduce printed cost by sum of discounts
				if "Fang of the First Moon" in card.Name:
						castDiscount = 0
						for c in me.piles['Discard Pile']:
								if "Animal" in c.Subtype:
										castDiscount += 2
								if castDiscount > 0: discountList = [(card, (castDiscount,"Found {} discarded animal creatures in {}\'s discard pile".format(castDiscount,me)))]
				usedDiscounts = []
				discountAppend = usedDiscounts.append
				for c,d in discountList:
						if cost > 0: #Right now, all discounts are for 1 (except construction yard). If there is ever a 2-mana discount, we will need to adjust this to optimize discount use. Come to think of it, some discounts overlap, and we might want to optimize for those...well, we can cross that bridge when we reach it.
								discAmt = min(cost,d[0])
								cost -= discAmt
								discountAppend((c,discAmt,d[1])) #Keep track of which discounts we are applying, and how much of each was applied
						else: break #Stop if the cost of the spell reaches 0; we don't need any more discounts.
				#Magebane
				for attachment in getAttachments(caster):
					if attachment.Name == 'Magebane' and attachment.isFaceUp:
						if askChoice("The caster is cursed by Magebane. Would you like to take 1 damage to cast the spell?",["Yes","No"],["#171e78","#de2827"]) == 1:
							if "Mage" in caster.Subtype:
								caster.controller.Damage += 1
								notify("{} suffers damage from {}\n".format(caster,attachment))
							else:
								caster.markers[Damage] += 1
								notify("{} suffers damage from {}\n".format(caster,attachment))
						else:
							return
				
				#Ask the player how much mana they want to pay
				discountSourceNames = "\n".join(["{} -{}".format(d[2],str(d[1])) for d in usedDiscounts])
				#discountSourceNames = '\n'.join(map(lambda t: "{} (-{})".format(t[0].Name,str(t[1])),usedDiscounts))
				discountString = "The following discounts were applied: \n{}\n\n".format(discountSourceNames) if discountSourceNames else ""
				pronoun = {"Male":"he","Female":"she"}.get(getGender(caster),"it")
				casterString = "{} will pay what {} can. You will pay the rest.\n\n".format(caster.Name.split(",")[0],pronoun) if (caster.Type != "Mage" and caster.markers[Mana]) else ""
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
				if casterCost: notify("{} pays {} mana.\n".format(caster,str(casterCost)))
				cost -= casterCost
				if cost:
						if discountString =="":
							notify("{} pays {} mana.\n".format(me,str(cost)))
							me.Mana = max(me.Mana-cost,0)
						else:
							notify("{} pays {} mana with the following discount applied: {}.\n".format(me,str(cost),discountSourceNames))
							me.Mana = max(me.Mana-cost,0)
				for c,d,e in usedDiscounts: #track discount usage
						if c.Name=="Construction Yard": c.markers[Mana] -= d
						rememberAbilityUse(c)
				if card.Type == "Enchantment": notify("{} enchants {}!\n".format(caster,target.Name) if target else "{} casts an enchantment!".format(caster))
				elif card.Type == "Creature": notify("{} summons {}!\n".format(caster,card.Name))
				elif "Conjuration" in card.Type: notify("{} conjures {}!\n".format(caster,card.Name))
				else: notify("{} casts {}!\n".format(caster,card.Name))
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
						notify("{} pays {} mana.\n".format(me,str(cost)))
				for c,d in usedDiscounts: #track discount usage
						rememberAbilityUse(c)
				flipcard(card)
				notify("{} reveals {}!\n".format(me,card))
				if card.Name == "Healing Charm":
						roll = rollDice(4)[0]
						healAmount = roll[2] + 2*roll[3] + roll[4] + 2*roll[5]
						if target.Subtype == "Mage" and target.controller == me:
								me.Damage = 0 if me.Damage < healAmount else me.Damage - healAmount
						elif "Creature" in target.Type and target.Subtype != "Mage" and target.controller == me:
								target.markers[Damage] -= healAmount
						notify("Heal Charm heals {} points of damage on {}!\n".format(healAmount,target))
				return True

def getCastDiscount(card,spell,target=None): #Discount granted by <card> to <spell> given <target>. NOT for revealing enchantments.
		if card.controller != spell.controller or not card.isFaceUp or card==spell: return (0,"") #No discounts from other players' cards or facedown cards!
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
					 (cName == "Enchanter's Ring" and target and target.controller == card.controller and (target.type == "Creature" or target.Subtype == "Mage") and sType == "Enchantment") or
					 (cName == "Ring of Asyra" and ("Holy" in sSchool) and sType == "Incantation") or
					 (cName == "Ring of Beasts" and sType == "Creature" and ("Animal" in sSubtype)) or
					 (cName == "Ring of Curses" and sType != "Enchantment" and ("Curse" in sSubtype)) or
					 (cName == "Druid's Leaf Ring" and sType != "Enchantment" and ("Plant" in sSubtype)) or
					 (cName == "Force Ring" and sType != "Enchantment" and ("Force" in sSubtype)) or
					 (cName == "Ring of the Ocean\'s Depths" and sType != "Enchantment" and ("Hydro" in sSubtype or "Aquatic" in sSubtype)) or
					 (cName == "Ring of Command" and sType != "Enchantment" and ("Command" in sSubtype)) or
					 (cName == "Commander\'s Cape" and sType != "Enchantment" and ("Command" in sSubtype or ("Soldier" in sSubtype and "Creature" in sType))))):
						return (1,cName)
				#Discounts that apply no matter who casts the spell
				if ((cName == "General's Signet Ring" and ("Soldier" in sSubtype)) or
					(cName == "Eisenach's Forge Hammer" and (sType == "Equipment"))):
						return (1,cName)
				#Construction yard will be treated as a once-per-round discount.
				if (cName == "Construction Yard" and
					((not "Incorporeal" in spell.Traits and "War" in sSchool and "Conjuration" in sType) or ("Earth" in sSchool and sType=="Conjuration-Wall"))):
						return (card.markers[Mana],cName)
				#Discounts from Markers on Equipment
				if isBound(spell) == True and card.type == 'Equipment' and getBindTarget(spell) == card:
					 	boundCasterTraits = computeTraits(card)
						#Rune of Power
						if boundCasterTraits.get('Spellbind') == True and caster.markers[RuneofPower] == 1:
							return (1,"Rune of Power on {}".format(cName))
		if timesUsed <2: #Twice-per-round discounts
				if cName == "Death Ring" and (mageCast or spawnpointCast) and sType != "Enchantment" and ("Necro" in sSubtype or "Undead" in sSubtype):
						return (1,cName)
		return (0,"")
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
							  (cName == "Ring of Command" and ("Command" in sSubtype)) or
							  (cName == "Voice of the Sea" and ("Song" in sSubtype)) or
							  (cName == "Commander\'s Cape" and ("Command" in sSubtype))): return 1
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
		if "/" in target.level:
			tLevel = int(sum(map(lambda x: int(x), target.Level.split('/')[0])))
		else:
			tLevel = int(sum(map(lambda x: int(x), target.Level.split('+'))))
		if name == "Mind Control":
				cost = 2*tLevel
		elif name in ["Charm","Fumble"]:
				cost = tLevel-1
		elif name in ["Asyra's Touch","Badger Frenzy","Exile","Panther Stealth","Wolf Fury"] and tLevel == 1: #Level 1 Creatures Discount
				cost -= 1
		elif name in ["Sanctuary"] and tLevel <= 2: #Minor Creatures Discount
				cost -= 1
		if cost == None: return #If it doesn't fit an exception, the player will have to handle it.
		traits = computeTraits(card)
		if "Mage" in target.Subtype:
				cost += traits.get("Magebind",0)
		return cost

def computeCastCost(card,target=None): #Does NOT take discounts into consideration. Just computes base casting cost of the card. NOT reveal cost.
		cost = 2 if card.Type == 'Enchantment' else None
		try: cost = int(card.Cost)
		except: pass
		if target: #Compute exact cost based on target. For now, cards like dissolve will have to target the spell they want to destroy. Does not check for target legality.
				name = card.Name
				if "Vine Marker" in target.Name and card.Name == "Burst of Thorns": return int(card.Cost)
				tLevel = int(target.Level.split("/")[0]) if "/" in target.Level else int(sum(map(lambda x: int(x), target.Level.split('+'))))
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

def debug(str):
	mute()
	global debugMode
	if debugMode:
		whisper("Debug Msg: {}".format(str))

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
				cardSubtype = card.Subtype
				if cardType == 'Internal': return
				mapX,mapW = mapDict.get('x'),mapDict.get('X')
				if cardType in ['DiceRoll','Phase']:
					moveRDA(card)
					return
				for i in range(len(zoneArray)):
						for j in range(len(zoneArray[0])):
								zone = zoneArray[i][j]
								if zone and zone.get('startLocation') in [str(playerNum),"*"]:
										zoneX,zoneY,zoneS = zone.get('x'),zone.get('y'),zone.get('size')
										if cardSubtype == "Mage":
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