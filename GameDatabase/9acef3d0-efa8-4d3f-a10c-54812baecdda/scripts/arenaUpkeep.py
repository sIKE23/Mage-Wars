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
										#channelBoost = len([k for k in table if k.isFaceUp and k.name == "Harmonize" and c == getAttachTarget(k)]) #Well, you can't really attach more than 1 harmonize anyway. But if there were another spell that boosted channeling, we could add it to this list.
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

def resolveLivingArmor(traits, card):
	gamemode = getGlobalVariable("GameMode")
	mage = Card(traits['MageID']) 
	if gamemode == "Playtest" and card.isFaceUp:
		if card.markers[Armor] < 3:
			notifystr = "Would you like to pay 1 mana to add 2 Armor Tokens due to Living Armor?"
			choiceList = ['Yes', 'No']
			colorsList = ['#0000FF', '#FF0000']
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if me.Mana == 0:
				notify("{} cannot afford to add more armor to Living Armor".format(me))
			elif choice == 1 :
				me.Mana -= 1
				if card.markers[Armor] < 2:
					card.markers[Armor]+=2
					notify("{} has chosen to pay 1 mana to add 2 Armor Tokens to Living Armor".format(me))
				elif card.markers[Armor] < 3:
					card.markers[Armor]+=1
					notify("{} has chosen to pay 1 mana to add Armor Tokens to Living Armor, but only adds 1 due to reaching the max of 3".format(me))
			elif choice == 2:
				notify("{} has chosen not to pay for Armor Tokens".format(me))
				return
		else:
			notify("Living Armor has 3 tokens already and will not generate more")
			
	else:
		if card.markers[Armor] < 2 and card.isFaceUp:
			card.markers[Armor]+=2
			notify("Living Armor generates 2 Armor Tokens")
		elif card.markers[Armor] < 3 and card.isFaceUp:
			card.markers[Armor]+=1
			notify("Living Armor generates 1 Armor Token")
		else:
			notify("Living Armor has 3 tokens already and will not generate more")
	return
	
def getRidofGlyphs(card):
	card.markers[FireGlyphInactive] = 0
	card.markers[AirGlyphInactive] = 0
	card.markers[EarthGlyphActive] -= 1
	
	
def resolveKiGen(traits, card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
		
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	mage = Card(mageID)
	if card.name == 'Ring of Ki':
		notifystr = "Would you like to pay 1 mana to gain 2 Ki?"
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 :
			me.Mana -= 1
			mage.markers[Ki]+=2
			notify("{} has chosen to pay 1 mana to gain 2 Ki".format(me))
		elif choice == 2:
			notify("{} has chosen not to pay for Ki".format(me))
	if card.controller == me and 'Ki' in traits and card.isFaceUp:
		notify("Generating Ki for {}...\n".format(card))	#found at least one
		card.markers[Ki] += 1 
	return
	
def resolveUpkeepGlyphs(traits, card):
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageStats = Card(mageStatsID)
	mage = Card(traits["MageID"])
	if card.markers[EarthGlyphActive]:
		notifystr = "Would you like to pay 2 mana to give 2 Armor to a friendly creature?"
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 :
			me.Mana -= 2
			mageStats.markers[EarthGlyphActive] = 0
			mageStats.markers[EarthGlyphInactive] = 1
			mage.markers[EarthGlyphActive] +=1
			notify("{} has chosen to pay 2 mana to give a friendly creature 2 Armor.\n(You'll have to manually move the Glyph token from your mage to target for now)\n".format(me))
	if card.markers[WaterGlyphActive]:
		notifystr = "Would you like to pay 2 mana to heal a friendly creature by 2?"
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		choice = askChoice("{}".format(notifystr), choiceList, colorsList)
		if choice == 1 :
			me.Mana -= 2
			mageStats.markers[WaterGlyphActive] = 0
			mageStats.markers[WaterGlyphInactive] = 1
			notify("{} has chosen to pay 2 mana to heal a friendly creature by 2.\n(You'll have to manually heal the target for now)\n".format(me))			
	return
	
def resolveKiUpkeep(traits, card):
	mute()
	#is the setting on?
	if not getSetting("AutoResolveEffects", True):
		return
		
	mageDict = eval(me.getGlobalVariable("MageDict"))
	mageStatsID = int(mageDict["MageStatsID"])
	mageID = int(mageDict["MageID"])
	mage = Card(mageID)
	if card.name == 'Five Point Death Strike':
		target = getAttachTarget(card)
		notifystr = "Would you like to pay 1 Ki to keep the Five Point Death Strike attached to {}?".format(target.name)
		choiceList = ['Yes', 'No']
		colorsList = ['#0000FF', '#FF0000']
		if mage.markers[Ki]<1:
			notify("{} cannot afford to keep powering the Death Strike".format(me))
			card.moveTo(me.piles['Discard Pile'])
		else:
			choice = askChoice("{}".format(notifystr), choiceList, colorsList)
			if choice == 1 :
				mage.markers[Ki]-=1
				notify("{} has chosen to pay 1 Ki to prolong the Death Strike!".format(me))
			elif choice == 2:
				notify("{} has chosen not to continue powering the Death Strike".format(me))
				card.moveTo(me.piles['Discard Pile'])
	return
	
def resolveMadrigal(traits, card):
	if ("Madrigal" in traits and "Finite Life" in traits) and card.controller == me and card.isFaceUp:
			notify("{} has the Finite Life Trait and can not heal".format(card.name))
			return
	if "Mage" in card.Subtype and card.controller == me and me.Damage > 1:
			damageAmount = 2
			subDamageAmount(card, 2)
	elif "Mage" in card.Subtype and card.controller == me:
			damageAmount = me.Damage
			me.Damage = 0
	elif "Mage" not in card.Subtype and card.markers[Damage]<2:
			damageAmount = card.markers[Damage]
			card.markers[Damage] = 0
	else:
			damageAmount = 2
			subDamageAmount(card, 2)
	if damageAmount > 0:
		notify("{}'s Healing Madrigal heals {} damage from {} ".format(me,damageAmount, card.name))
	else:
		notify("{}'s {} is already at full health".format(me, card.name))