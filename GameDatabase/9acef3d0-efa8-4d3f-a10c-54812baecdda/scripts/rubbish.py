# functions that I see are not used anywhere, at least that is what I think - delete when we are done

#WIP don't think we need this anymore
'''def diceRollMenu(attacker = None,defender = None,specialCase = None):
		mute()
		setEventList('Turn',[]) #Clear the turn event list. Will need to be changed when we implement sweeping/zone attacks properly
		aTraitDict = (computeTraits(attacker) if attacker else {})
		if aTraitDict.get("Incapacitated"):
				if specialCase!="Counterstrike": whisper("{} is incapacitated and cannot attack!".format(attacker.Nickname))
				return {}
		if attacker and (aTraitDict.get('Charge') or [1 for c in getAttachments(attacker) if (c.Name=="Lion Savagery" or c.Name=="Ballad of Courage") and c.isFaceUp and c.controller==attacker.controller]) and defender and getZoneContaining(attacker)==getZoneContaining(defender) and not specialCase and not hasAttackedThisTurn(attacker) and askChoice('Apply charge bonus to this attack?',['Yes','No'],["#01603e","#de2827"]) == 1: rememberCharge(attacker) #Let's try prompting for charge before opening menu, for a change.
		if not attacker: defender = None
		dTraitDict = (computeTraits(defender) if defender else {})
		attackList = getAttacks(attacker) if attacker else [{'Dice':i+1} for i in range(7)]
		choiceText = "Roll how many attack dice?"
		#Suppose there is an attacker with at least one attack:
		if aTraitDict:
				attackList = [computeAttack(attacker,attack,defender) for attack in attackList if attack.get('action type') != 'Damage Barrier']
				choiceText = "Use which attack?"
		if specialCase == 'Counterstrike':
				debug('Counterstrike found')
				for a in list(attackList):
						if a.get('Traits',{}).get('Counterstrike'): a['range type'] = 'Counterstrike'
						else: attackList.remove(a)
		choices = []
		for a in list(attackList):
				atkTraits = a.get('Traits',{})
				traits = getAttackTraitStr(atkTraits)
				expDam = str(round(expectedDamage(aTraitDict,a,dTraitDict),1)) if defender else ''
				killCh = str(round(chanceToKill(aTraitDict,a,dTraitDict)*100,1)) if defender else ''
				effectList = (['{} ({}%)'.format(e[1],
												str(round(getD12Probability(e[0],aTraitDict,a,dTraitDict)*100,1))) for e in a.get('d12',[])]
							  if a.get('d12') else '')
				choice = (("{} ({})".format(a.get('Name'),str(a.get('Dice',0))).center(68,' ') if a.get('Name') else str(a.get('Dice',0)).center(68,' '))+
						  ('\n{} Mana'.format(str(a.get('Cost',0))) if a.get('Cost') else '')+
						  ('\n'+', '.join(traits) if traits else '')+
						  ('\n'+', '.join(effectList) if effectList != '' else '')+
						  ('\nExpected damage: {} | Kill chance: {}%'.format(expDam,killCh) if (defender and a.get('EffectType','Attack')=='Attack') else ''))
				if specialCase == 'Counterstrike' and a.get('RangeType') != 'Counterstrike': continue
				if not attacker or isLegalAttack(aTraitDict,a,dTraitDict): choices.append(choice)
				else: attackList.remove(a)
		if defender and attacker and defender.Type in ['Creature','Conjuration','Conjuration-Wall']:
				choiceText = "Attacking {} with {}. Use which Attack?".format(defender.name,attacker.name)
		if specialCase == 'Counterstrike': choiceText = "{} can counterstrike! Use which attack?".format(attacker.name)
		colors = ([] if attacker else ['#E0B525']) + [getActionColor(attackList[i]) for i in range(len(choices))] + ['#666699','#000000']
		attackList = ([] if attacker else [{'Dice':0}]) + list(attackList)
		choices = ([] if attacker else ['Roll Effect Die']) + list(choices) + ['Other Dice Amount','Cancel Attack']
		if specialCase == 'Counterstrike' and not attackList: return {}
		count = (askChoice("No legal attacks detected!", ['Roll anyway','Cancel'], colors) if len(choices) == 2 else askChoice(choiceText, choices, colors))
		if count == 0 or count == len(choices): return {}
		elif count < len(choices)-1:
				return attackList[count-1]
		elif count == len(choices)-1:
				if attacker: return diceRollMenu()
				else: #Revert to standard input menu. Default value is the last one you entered.
						dice = min(askInteger("Roll how many Attack Dice?", getSetting('lastStandardDiceRollInput',8)),50) #max 50 dice rolled at once
						setSetting('lastStandardDiceRollInput',dice)
						return {'Dice' : dice}'''

#WIP used by diceRollMenu that will be obsolete
'''def getActionColor(action):
		if action.get('EffectType','Attack') == 'Heal': return "#663300"        #Heal is always in orange
		#Assume is an attack
		if action.get('Traits',{}).get('Spell'): return "#9900FF"         #Spell attacks are purple
		if action.get('RangeType') == 'Ranged': return '#0f3706'     #Nonspell ranged attacks are green
		return '#CC0000'      '''                                                  #Default to red

#WIP used by diceRollMenu that will be obsolete
'''def isLegalAttack(aTraitDict,attack,dTraitDict):
		if not (aTraitDict.get('OwnerID') and dTraitDict.get('OwnerID')): return True
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})
		if attack["Name"] == "Arcane Zap" and "Wizard" in attacker.Name and timesHasOccured("Arcane Zap",attacker.controller): return False
		if (defender.name == "Tanglevine" or defender.name  == "Stranglevine") and attack.get('RangeType') != "Melee": return False
		if attacker.controller.Mana + attacker.markers[Mana] < attack.get('Cost',0): return False
		if attack.get('Type','NoType') in dTraitDict.get('Immunity',[]): return False
		aZone = getZoneContaining(attacker)
		if attack.get('Range'):
				if defender.Type == 'Conjuration-Wall':
						dZones = getZonesBordering(defender)
						inRange = False
						for z in dZones:
								distance = zoneGetDistance(aZone,z)
								if ((0 if (attack.get('RangeType')=='Ranged' and dTraitDict.get('Flying')) else attack.get('Range')[0])
									<= distance
									<= attack.get('Range')[1]): inRange = True
						if not inRange: return False
				else:
						dZone = getZoneContaining(defender)
						distance = zoneGetDistance(aZone,dZone)
						minRange = (0 if (attack.get('RangeType')=='Ranged' and dTraitDict.get('Flying')) else attack.get('Range')[0])
						if not (minRange <= distance <= attack.get('Range')[1]): return False
		if (dTraitDict.get('Flying') and
			not aTraitDict.get('Flying') and
			attack.get('RangeType') == 'Melee' and
			not atkTraits.get('Reach')): return False
		return True'''


'''Not called, delete'''
'''def computeD12(dTraitDict,d12Pair):#WIP
		defender = Card(dTraitDict.get('OwnerID'))
		effectText = d12Pair[1]
		effects = []
		if ' & ' in effectText: effects = effectText.split(' & ')
		elif '2 ' in effectText: effects = [effectText.strip('2 '),effectText.strip('2 ')]
		else: effects = [effectText]
		conditionTypes = {'Flame' : ['Burn'],
						  'Psychic' : ['Sleep'],
						  'Acid' : ['Corrode'],
						  'Poison' : ['Rot','Cripple','Tainted','Weak']}
		#First, make replacements for slamming unmovable creatures
		if dTraitDict.get('Unmovable'):
				for n,i in enumerate(effects):
						if i == 'Slam': effects[n] = 'Daze'
		#Then make removals
		for e in list(effects):
				illegalEffect = False

				for i in dTraitDict.get('Immunity',[]):
						if (e in conditionTypes.get(i,[])): illegalEffect = True
				if ((e=='Burn' and dTraitDict.get('Burnproof'))
					or (e in ['Snatch','Push'] and dTraitDict.get('Unmovable'))
					or (e == 'Bleed' and (dTraitDict.get('Nonliving') or 'Plant' in defender.Subtype))
					or (e in ['Bleed','Stuck','Stun','Daze','Cripple','Weak','Slam','Stagger'] and defender.Type != 'Creature')): illegalEffect = True #not sure about weak; can it affect conjurations?
				if illegalEffect: effects.remove(e)
		#Finally, replace corrode with damage if neccessary
		currentArmor = getStat(Card(dTraitDict['OwnerID']).Stats,'Armor') + dTraitDict.get("Armor",0)
		for n,i in enumerate(effects):
				if i == "Corrode":
						if currentArmor == 0: effects[n] = "Damage"
						else: currentArmor -= 1
		if not effects: return False
		if len(effects) == 1: return [d12Pair[0],effects[0]]
		if len(effects) == 2 and effects[0] == effects[1]: return [d12Pair[0],'2 '+effects[0]]
		else: return [d12Pair[0],'{} & {}'.format(effects[0],effects[1])]'''


'''Not called, delete'''
'''def getAdjustedDice(aTraitDict,attack,dTraitDict):
		"""Decides how many dice should be rolled for attack based on the attacker (and the defender, if any)."""
		attackDice = attack.get('Dice',0)
		atkTraits = attack.get('Traits',{})
		attacker = (Card(aTraitDict['OwnerID']) if 'OwnerID' in aTraitDict else None)
		defender = (Card(dTraitDict['OwnerID']) if 'OwnerID' in dTraitDict else None)
		atkOS = Card(attack['source id'])
		if attacker and not "Autonomous" in atkOS.traits:
			if not hasAttackedThisTurn(attacker): #Once per attack sequence bonuses
				if (attack.get('RangeType') == 'Melee' or attack.get('RangeType') == 'Counterstrike') and not attack.get("Action") == "Trample": attackDice += aTraitDict.get('Melee',0) + (aTraitDict.get('Charge',0) if hasCharged(attacker) else 0)#Charge Bonus
				if attack.get('RangeType') == 'Ranged': attackDice += aTraitDict.get('Ranged',0)
			#No restriction on how many times may be applied
			if not atkTraits.get('Spell'):
				attackDice -= attacker.markers[Weak]
				attackDice -= attacker.markers[Stagger] * 2
				if (not "Aquatic" in atkOS.traits and "Shallow Sea" in aTraitDict):
					if not "Flying" in atkOS.traits:
						attackDice -=1 
					elif "Flying" in atkOS.traits and attack.get('RangeType') == "Melee" and not "Flying" in dTraitDict:
						attackDice -=1 
				if [True for c in getAttachments(attacker) if c.isFaceUp and c.Name == "Agony"]: attackDice -= 2
				if [True for c in getAttachments(attacker) if c.isFaceUp and c.Name == "Tangleroot"]: attackDice -= c.markers[DissipateToken]
				if [True for c in getAttachments(attacker) if c.isFaceUp and (c.Name == "Knight\'s Courage")] and defender.markers[Strongest]: 
						attackDice += 2 
						atkTraits['Piercing'] = atkTraits.get('Piercing',0) + 1
				if (attack["Name"] in ["Dragon-Tail Sweep", "Flying Side Kick"] or "Nunchucks" in aTraitDict) and attack.has_key("KiDice"):
					if attack["Name"] == 'Dragon-Tail Sweep':
						#debug("Attack Dice before: {}".format(attackDice))
						attackDice += 1
						#debug("Attack Dice after: {}".format(attackDice))
					elif attack["Name"] == "Flying Side Kick":
						attackDice += 2
					else:
						attackDice += 1
				if attacker.markers[FireGlyphActive]:
					attackDice +=2
				level = eval(attacker.Level)
				if Card(attack['source id']).name in listMageWeapons and "Mage" in attacker.Subtype and level >= 5: attackDice += 1
				if attacker.Name == "Lightning Raptor" and attacker.markers[Charge] > 1 : attackDice += attacker.markers[Charge]
				if [True for c in getAttachments(defender) if c.isFaceUp and c.Name == "Force Shield"] and attack.get('RangeType') == 'Melee': attackDice -= c.markers[DissipateToken]
		if defender:
				#Likely need to redo a lot of the exceptions based old stuff #WIP
				if 'Glancing' in dTraitDict and not attack.get("Traits",{}).get("Drain"): attackDice -= 3
				attackDice -= dTraitDict.get('Aegis',0)
				attackDice += (aTraitDict.get('Bloodthirsty',0) if ((defender.markers[Damage] or (defender.Subtype=="Mage" and defender.controller.Damage))
																	and (attacker and not hasAttackedThisTurn(attacker))
																	and defender.type == 'Creature'
																	and not dTraitDict.get('Nonliving')
																	and (attack.get("RangeType") == "Melee" or attack.get('RangeType') == 'Counterstrike')
																	and not attack.get("Action") == "Trample"
																	) else 0)
				attackDice += dTraitDict.get(attack.get('Type'),0) #Elemental weaknesses/resistances
				if [True for c in getAttachments(defender) if c.isFaceUp and c.name == "Marked for Death"]: #Marked for death
						eventList = getEventList('Round')
						if ((not [True for e in eventList if e[0] == 'Attack' and e[1][0] == attacker._id and e[1][1] == defender._id])
																	and attacker.type == 'Creature'
																	and (attacker and not hasAttackedThisRound(attacker))
																	and attack.get('RangeType') != 'Damage Barrier'):
								attackDice += 1
				vs = atkTraits.get('VS')
				if vs: #We'll assume each attack has only one vs+ trait
						if ((vs[0] == "Corporeal Conjurations" and 'Conjuration' in defender.Type and 'Corporeal' in dTraitDict) or
							(vs[0] == "Flying" and 'Flying' in dTraitDict) or
							(vs[0] == "Nonliving Creatures" and 'Creature'==defender.Type and 'Nonliving' in dTraitDict) or
							(vs[0] == "Nonliving and Dark creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or
							(vs[0] == "Nonliving or Dark Creatures" and 'Creature'==defender.Type and ('Nonliving' in dTraitDict or 'Dark' in defender.School)) or #Curse AW's inconsistent formatting...
							(vs[0] == "Nonliving" and 'Nonliving' in dTraitDict) or
							(vs[0] == "Incorporeal" and "Incorporeal" in dTraitDict) or
							(vs[0] == "Undead" and "Undead" in defender.Subtype)): attackDice += vs[1]
				if attacker and attack.get('Name') == 'Thundergun' and attacker.Name == "Grimson Deadeye, Sniper": #Deadeye's ability
						aZone = getZoneContaining(attacker)
						dZone = getZoneContaining(defender)
						distance = zoneGetDistance(aZone,dZone)
						attackDice -= max((distance-1),0)
		if attackDice <= 0: attackDice = 1
		if atkTraits.get('No Damage'): attackDice = 0
		return attackDice'''


'''Not called, delete'''
'''def getAttackTraitStr(atkTraitDict): ##Takes an attack trait dictionary and returns a clean, easy to read list of traits
		attackList = []
		for key in atkTraitDict:
				text = key
				if key in additiveTraits: text += ' +{}'.format(str(atkTraitDict[key]))
				if key in superlativeTraits: text += ' {}'.format(str(atkTraitDict[key]))
				if key == 'VS': text = ('+' if atkTraitDict[key][1]>=0 else '') + str(atkTraitDict[key][1]) + ' vs. ' + atkTraitDict[key][0]
				if atkTraitDict[key]: attackList.append(text)
		return attackList'''


'''def rollDice(dice):
	mute()
	global attackDiceBank
	global effectDieBank
	mapDict = eval(getGlobalVariable('Map'))
	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me: c.delete()

	dieCardX, dieCardY = mapDict.get('DiceBoxLocation',(0,0))
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", dieCardX, dieCardY) #dice field 1
	dieCard.anchor = (True)
	rnd(0,0)
	diceFrom = ""
	count = dice
	if (len(attackDiceBank) < count): #attackDiceBank running low - fetch more
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
	#debug("Random.org response code for damage dice roll: {}".format(random_org[1]))
		if random_org[1]==200: # OK code received:
			attackDiceBank = random_org[0].splitlines()
			diceFrom = "from Random.org"
		else:
		#notify("www.random.org not responding (code:{}). Using built-in randomizer".format(random_org[1]))
			diceFrom = "from the native randomizer"
			while (len(attackDiceBank) < 20):
				attackDiceBank.append(rnd(0, 5))

	result = [0,0,0,0,0,0]
	for x in range(count):
		roll = int(attackDiceBank.pop())
		result[roll] += 1
	#debug("diceRoller result: {}".format(result))
	notify("{} rolls {} attack dice {}".format(me,count,diceFrom))

	damPiercing = result[4] + 2* result[5]
	damNormal = result[2] + 2* result[3]
	dieCard.markers[attackDie[0]] = result[0]+result[1] #blanks
	dieCard.markers[attackDie[2]] = result[2] #1
	dieCard.markers[attackDie[3]] = result[3] #2
	dieCard.markers[attackDie[4]] = result[4] #1*
	dieCard.markers[attackDie[5]] = result[5] #2*

	d12DiceCount = 1
	if (len(effectDieBank) < d12DiceCount): #diceBank running low - fetch more
		d12 = webRead("http://www.random.org/integers/?num=100&min=0&max=11&col=1&base=10&format=plain&rnd=new")
		#debug("Random.org response code for effect roll: {}".format(d12[1]))
		if d12[1]==200: # OK code received:
			effectDieBank = d12[0].splitlines()
			notify ("Using die from Random.org")
		else:
			notify ("Using die from the native randomizer")
			while (len(effectDieBank) < 100):
				effectDieBank.append(rnd(0, 11))

	effect = int(effectDieBank.pop()) + 1
	dieCard.markers[effectDie] = effect
	if getGlobalVariable("GameSetup") == "True":
		playSoundFX('Dice')
		time.sleep(1)
		notify("{} rolled {} normal damage, {} critical damage, and {} on the effect die".format(me,damNormal,damPiercing,effect))
		return (result,effect)'''


#old function, DELETE later when done referencing
'''def applyDamageAndEffects(aTraitDict,attack,dTraitDict,damage,rawEffect): #In general, need to adjust functions to accomodate partially or fully untargeted attacks.
		attacker = Card(aTraitDict.get('OwnerID',''))
		defender = Card(dTraitDict.get('OwnerID',''))
		atkTraits = attack.get('Traits',{})
		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		conditionsList = ['Bleed','Burn','Corrode','Cripple','Damage','Daze','Rot','Slam','Sleep','Stagger','Stuck','Stun','Tainted','Weak']
		effectsInflictDict = {'Damage' : "suffers 1 point of direct damage! (+1 Damage)",
							  'Bleed' : 'bleeds from its wounds! (+1 Bleed)',
							  'Burn' : 'is set ablaze! (+1 Burn)',
							  'Corrode' : 'corrodes! (+1 Corrode)',
							  'Cripple' : 'is crippled! (+1 Cripple)',
							  'Daze' : 'is dazed! (+1 Daze)',
							  'Rot' : 'rots! (+1 Rot)',
							  'Slam' : 'is slammed to the ground! (+1 Slam)',
							  'Sleep' : 'falls fast alseep! (+1 Sleep)',
							  'Stagger' : 'staggers about, not quite sure what is going on! (Minor Creatures can not Attack or Guard, Major Creatures -2 to All Attacks)',
							  'Stuck' : 'is stuck fast! (+1 Stuck)',
							  'Stun' : 'is stunned! (Stun)',
							  'Tainted' : "'s wounds fester! (+1 Tainted)",
							  'Weak' : 'is weakened! (+1 Weak)',
							  'Snatch' : 'is snatched toward {}! (Snatch)'.format(attacker),
							  'Push' : 'is pushed away from {}! (Push 1)'.format(attacker),
							  'Taunt' : 'wants to attack {}! (Taunt)'.format(attacker)}

		#Prep for Vampirism
		aDamage = getStatusDict(attacker).get('Damage',0)
		drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0)) if defender.Type == "Creature" else 0
		#if "Vine Marker" in defender.Name: drainableHealth = 0
		#else: drainableHealth = int(round(min(getRemainingLife(dTraitDict)/float(2),damage/float(2),aDamage),0))

		if defender.Subtype == 'Mage': defender.controller.Damage += damage
		else: defender.markers[Damage] += damage
		notify("{} inflicts {} damage on {}{} average roll)".format(attacker,
																	str(damage),
																	defender,
																	('! (an above' if damage >= expectedDmg else '... (a below')))

		#Vine Markers are always destroyed from any amount of damage
		if "Vine Marker" in defender.name and damage >0:
			  notify("{} is smashed into the ground and destroyed.".format(defender))
			  defender.moveTo(me.piles['Discard'])
			  return #No sense going any further.

		#Bloodreaper health drain
		if attacker.markers[BloodReaper] and not timesHasOccured("Blood Reaper",attacker.controller) and defender.Type == "Creature" and dTraitDict.get("Living") and 'Demon' in attacker.Subtype and damage:
				mage = Card(aTraitDict.get('MageID'))
				healing = min(2,mage.controller.damage)
				if healing and not computeTraits(mage).get("Finite Life"):
						rememberPlayerEvent("Blood Reaper",attacker.controller)
						notify("{}'s health is restored by his Reaper's blood offering! (-{} Damage)".format(mage,str(healing)))
						remoteCall(mage.controller, "remotePlayerHeal", [healing])

		#Malakai's Fire
		if (attacker.Name=="Priest" and attack.get("Type")=="Light" and damage and "Conjuration" not in defender.Type and not timesHasOccured("Malakai's Fire",attacker.controller) and "Flame" not in dTraitDict.get("Immunity",[])):
				remoteCall(attacker.controller,"malakaisFirePrompt",[defender])

		#Mana Drain - Long term, will want a centralized function to adjust damage/mana of a card so we can take into account things like Mana Prism
		if defender.Type == 'Creature':
			dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if damage else 0)
			defender.controller.Mana -= dManaDrain
		else: dManaDrain = ""
		if dManaDrain: notify("{} drains {} mana from {}!".format(attacker,str(dManaDrain),defender.controller.nickname))
		#Vampirism
		if (atkTraits.get('Vampiric') and drainableHealth and
			(dTraitDict.get('Living') or not dTraitDict.get('Nonliving')) and defender.Type == 'Creature' > 0): #Long term, give all creatures Living trait by default, eliminate nonliving condition
				if attacker.controller == me: healingQuery(aTraitDict,
														   'Heal {} damage through vampirism?'.format(drainableHealth,defender.nickname),
														   drainableHealth,
														   "{} heals {} damage through vampirism!".format(attacker.nickname,'{}',defender.nickname))
				else: remoteCall(attacker.controller,'healingQuery',[aTraitDict,
																   'Heal {} damage through vampirism?'.format(drainableHealth,defender.nickname),
																   drainableHealth,
																   "{} heals {} damage through vampirism!".format(attacker.nickname,'{}',defender.nickname)])
		#Finally, apply conditions
		effects = ([rawEffect.split(' ')[1],rawEffect.split(' ')[1]] if '2' in rawEffect else rawEffect.split(' & ')) if rawEffect else []
		for e in effects:
				if e in conditionsList:
						if e=="Damage" and defender.Subtype == "Mage": defender.controller.damage += 1
						else: defender.markers[eval(e)]+=1
				notify('{} {}'.format(defender.nickname,effectsInflictDict.get(e,'is affected by {}!'.format(e))))'''

#Not currently called
'''
def damageReceiptMenu(aTraitDict,attack,dTraitDict,roll,effectRoll):
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})

		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		actualDmg,actualEffect = computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict)


		if defender.markers[VoltaricON] and actualDmg:#Voltaric Shield
				notify("The Voltaric Shield absorbs {} points of damage!".format(str(min(actualDmg,3))))
				actualDmg = max(actualDmg-3,0)
				defender.markers[VoltaricON] = 0
				defender.markers[VoltaricOFF] = 1
		if defender.type == "Creature" or defender.Subtype == "Mage": dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if actualDmg else 0) #Prep for mana drain
		else: dManaDrain = ""

		choice = askChoice('{}\'s attack will inflict {} damage {}on {}.{} Apply these results?'.format(attacker.nickame,
																										  actualDmg,
																										  ('and an effect ({}) '.format(actualEffect) if actualEffect else ''),
																										  defender.nickname,
																										  (' It will also drain {} mana from {}.'.format(
																												  str(dManaDrain),defender.controller.nickname) if dManaDrain else '')),
						   ['Yes',"Other Damage Amount",'No'],
						   ["#01603e","#FF6600","#de2827"])
		if choice == 1:
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg #for remembering damage. Pretty crude; We'll come up with a better alternative in Q2
		elif choice == 2:
				actualDmg = askInteger("Apply how much damage?",actualDmg)
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg
		else:
				notify('{} has elected not to apply auto-calculated battle results'.format(me))
				whisper('(Battle calculator not giving the right results? Report the bug to us so we can fix it!)')
'''

#Not being called currently. Delete
'''
def damageReceiptMenu(aTraitDict,attack,dTraitDict,roll,effectRoll):
		attacker = Card(aTraitDict.get('OwnerID'))
		defender = Card(dTraitDict.get('OwnerID'))
		atkTraits = attack.get('Traits',{})
		#If it is healing, we heal and then end the attack, since it is not an attack.
		if False and attack.get('EffectType','Attack')=='Heal':
				healingAmt = min(sum([{0:0,1:0,2:1,3:2,4:1,5:2}.get(i,0)*roll[i] for i in range(len(roll))]),getStatusDict(defender).get('Damage',0))
				if healingAmt > 0: healingQuery(dTraitDict,
												'Heal {} for {} damage?'.format(defender.nickname,str(healingAmt)),
												healingAmt,
												"{} heals {} for {} damage!".format(attacker.nickname,defender.nickname,{}))
				else: notify("{} attempts to heal {} but fails.".format(attacker.nickname,defender.nickname))
				return 0 #Uh-oh...healing is treated as an attack for abilities that remember that. No worries; this will become irrelevant it Q2, and does not matter now.
		expectedDmg = expectedDamage(aTraitDict,attack,dTraitDict)
		actualDmg,actualEffect = computeRoll(roll,effectRoll,aTraitDict,attack,dTraitDict)
		if defender.markers[VoltaricON] and actualDmg:#Voltaric Shield
				notify("The Voltaric Shield absorbs {} points of damage!".format(str(min(actualDmg,3))))
				actualDmg = max(actualDmg-3,0)
				defender.markers[VoltaricON] = 0
				defender.markers[VoltaricOFF] = 1
		if defender.type == "Creature" or defender.Subtype == "Mage": dManaDrain = (min(atkTraits.get('Mana Drain',0)+atkTraits.get('Mana Transfer',0),defender.controller.Mana) if actualDmg else 0) #Prep for mana drain
		else: dManaDrain = ""

		choice = askChoice('{}\'s attack will inflict {} damage {}on {}.{} Apply these results?'.format(attacker.nickame,
																										  actualDmg,
																										  ('and an effect ({}) '.format(actualEffect) if actualEffect else ''),
																										  defender.nickname,
																										  (' It will also drain {} mana from {}.'.format(
																												  str(dManaDrain),defender.controller.nickname) if dManaDrain else '')),
						   ['Yes',"Other Damage Amount",'No'],
						   ["#01603e","#FF6600","#de2827"])
		if choice == 1:
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg #for remembering damage. Pretty crude; We'll come up with a better alternative in Q2
		elif choice == 2:
				actualDmg = askInteger("Apply how much damage?",actualDmg)
				applyDamageAndEffects(aTraitDict,attack,dTraitDict,actualDmg,actualEffect)
				return actualDmg
		else:
				notify('{} has elected not to apply auto-calculated battle results'.format(me))
				whisper('(Battle calculator not giving the right results? Report the bug to us so we can fix it!)')
'''


# I am guessing that Cosworth used another game as a jumping point and these fuctions were from that game 


Die = [ "DieBlank",
		"DieBlank",
		"Die1",
		"Die2",
		"Die1s",
		"Die2s"]

DieBlank = ("No Damage","a1f061ec-efbe-444e-8e06-8d973600696c")
Die1 = ("1 Normal Damage","8cc1704a-6f2f-4dbf-a80c-8f79a5a8d165")
Die2 = ("2 Normal Damageface","b881f652-9384-43e1-9758-e68b04583b3b")
Die1s = ("1 Critical Damage","a3d3fff3-bb1c-4469-9a9d-f8dc1f341d39")
Die2s = ("2 Critical Damage","101976ea-ec22-4496-a762-6fbc0d1a41bb")


def inspectCard(card, x = 0, y = 0):
	whisper("{}".format(card))
	for k in card.properties:
		if len(card.properties[k]) > 0:
			whisper("{}: {}".format(k, card.properties[k]))
			

def returnToHand(card): #Return card to your hand
	card.moveTo(me.hand)
	



#Check see if a card at x1,y1 overlaps a card at x2,y2
#Both have size w, h
def overlaps(x1, y1, x2, y2, w, h):
	#Four checks, one for each corner
	if x1 >= x2 and x1 <= x2 + w and y1 >= y2 and y1 <= y2 + h: return True
	if x1 + w >= x2 and x1 <= x2 and y1 >= y2 and y1 <= y2 + h: return True
	if x1 >= x2 and x1 <= x2 + w and y1 + h >= y2 and y1 <= y2: return True
	if x1 + w >= x2 and x1 <= x2 and y1 + h >= y2 and y1 <= y2: return True
	return False


def cardHere(x, y, stat=""):
	for c in table:
		if c.controller == me:
			cx, cy = c.position
			#if overlaps(x, y, cx, cy, c.width(), c.height()):
			if x >= cx and x <= cx+c.width() and y >= cy and y <= cy+c.height() and stat in c.Stats:
				return c
	return None


def cardX(card):
	x, y = card.position
	return x

def cardY(card):
	x, y = card.position
	return y


def findCard(group, model):
	for c in group:
		if c.model == model:
			return c
	return None