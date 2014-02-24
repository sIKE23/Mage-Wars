############################################################################
##########################    v1.3.0.3    ##################################
############################################################################
import time
import re
############################################################################
##########################		Constants		############################
############################################################################

##########################		Markers			############################

ActionRed = ("Action", "4dd182d2-6e69-499c-b2ad-38701c0fb60d")
ActionRedUsed = ("Action Used", "2e069a99-1696-4cbe-b6c6-13e1dda29563")
ActionBlue = ("Action", "c980c190-448d-414f-9397-a5f17068ac58")
ActionBlueUsed = ("Action Used", "5926df42-919d-4c63-babb-5bfedd14f649")
ActionGreen = ("Action", "9cd83c4b-91b7-4386-9d9a-70719971f949")
ActionGreenUsed = ("Action Used", "5f20a2e2-cc59-4de7-ab90-cc7d1ced0eee")
ActionYellow = ("Action", "2ec4ddea-9596-45cc-a084-23caa32511be")
ActionYellowUsed = ("Action Used", "7c145c5d-54c3-4f5b-bf66-f4d52f240af6")
Mana = ("Mana", "00000000-0000-0000-0000-000000000002")
Damage = ("Damage", "00000000-0000-0000-0000-000000000004")
BloodReaper = ("BloodReaper","50d83b50-c8b1-47bc-a4a8-8bd6b9b621ce")
Burn = ("Burn", "f9eb0f3a-63de-49eb-832b-05912fc9ec64")
Cripple = ("Cripple", "82df2507-4fba-4c81-a1de-71e70b9a16f5")
Daze = ("Daze","3ef51126-e2c0-44b3-b781-0b3f8476cb20")
DeflectR = ("Deflect Ready", "684fcda0-e69d-426e-861c-5a92bc984f55")
DeflectU = ("Deflect Used", "2c5b85ea-93de-4a99-b64d-da6c48baa205")
Guard = ("Guard", "91ed27dc-294d-4732-ab71-37911f4011f2" )
HolyAvenger = ("Holy Avenger", "99381ac8-7d73-4d75-9787-60e6411d3613" )
Invisible = ("Invisible", "8d994fe9-2422-4a9d-963d-3ad10b2b823d")
Pet = ("Pet", "f4a2d3d3-4a95-4b9a-b899-81ea58293167")
Quick = ("Quick", "11370fe9-41a4-4f05-9249-29a179c0031b")
QuickBack = ("Quick back", "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd")
Ready = ("Ready", "aaea8e90-e9c5-4fbc-8de3-4bf651d784a7" )
Rot = ("Rot", "81360faf-87d6-42a8-a719-c49386bd2ab5" )
Slam = ("Slam", "f7379e4e-8120-4f1f-b734-51f1bd9fbab9" )
Sleep = ("Sleep", "ad0e8e3c-c1af-47b7-866d-427f8908dea4" )
Stun = ("Stun", "4bbac09e-a46c-42de-9272-422e8074533f" )
Taunt = ("Taunt(Sosroku)", "16f03c44-5656-4e9d-9629-90c4ff1765a7" )
TauntT = ("Taunt(Thorg)", "8b5e3fe0-7cb1-44cd-9e9c-dadadbf04ab7" )
Turn = ("Turn", "e0a54bea-6e30-409d-82cd-44a944e591dc")
Used = ("Used", "ab8708ac-9735-4803-ba4d-4932a787540d" )
Veteran = ("Veteran", "72ee460f-adc1-41ab-9231-765001f9e08e" )
Visible = ("Visible", "b9b205a2-a998-44f5-97dc-c7f315afbbe2")
VoltaricON = ("Voltaric ON", "a6e79926-db8d-4095-9aee-e3b46bf24a3f" )
VoltaricOFF = ("Voltaric OFF", "d91aabe0-d9cd-4b7e-b994-4e1c7a51c027")
Weak = ("Weak", "22ef0c9e-6c0b-4e24-a4fa-e9d83f24fcba" )
WoundedPrey = ("Wounded Prey", "42f6cee3-3de4-4c90-a77c-9fb2c432d78d" )
Growth = ("Growth", "c580e015-96ff-4b8c-8905-28688bcd70e8")
Corrode= ("Corrode", "c3de25bf-4845-4d2d-8a28-6c31ad12af46")
Ichthellid = ("Ichthellid Larva", "c8bff05e-e43a-4b23-b467-9c4596050f28")
Zombie = ("Zombie", "de101060-a4b4-4387-a7f8-aab82ecff2c8")
Treebond = ("Treebond", "ced2ce11-5e69-46a9-9fbb-887e96bdf805")
Eternal_Servant = ("Eternal Servant", "86a71cf6-35ce-4728-a2f8-6701b1e29aa4")

##########################		Dice-related			########################

Die = [ "DieBlank",
		"DieBlank",
		"Die1",
		"Die2",
		"Die1s",
		"Die2s"]
attackDie = [ ("DieBlank","a1f061ec-efbe-444e-8e06-8d973600696c"),
		("DieBlank","a1f061ec-efbe-444e-8e06-8d973600696c"),
		("Die1","8cc1704a-6f2f-4dbf-a80c-8f79a5a8d165"),
		("Die2","b881f652-9384-43e1-9758-e68b04583b3b"),
		("Die1s","a3d3fff3-bb1c-4469-9a9d-f8dc1f341d39"),
		("Die2s","101976ea-ec22-4496-a762-6fbc0d1a41bb"),
		]
DieBlank = ("DieBlank","a1f061ec-efbe-444e-8e06-8d973600696c")
Die1 = ("Die1","8cc1704a-6f2f-4dbf-a80c-8f79a5a8d165")
Die2 = ("Die2","b881f652-9384-43e1-9758-e68b04583b3b")
Die1s = ("Die1s","a3d3fff3-bb1c-4469-9a9d-f8dc1f341d39")
Die2s = ("Die2s","101976ea-ec22-4496-a762-6fbc0d1a41bb")
Died12 = ("Died12","3cdf4231-065d-400e-9c74-d0ae669e852c")
diceBank = [1]

##########################		Other			############################

PlayerColor = 	["#de2827", 	# Red 		R=222 G=40  B=39
				"#171e78", 		# Blue		R=23  G=30  B=120
				"#01603e", 		# Green		R=1   G=96  B=62
				"#f7d917"] 		# Yellow 	R=247 G=217 B=23
mycolor = "#800080" # Purple
boardFlipped = False
showDebug = False
myIniRoll = 0
hasRolledIni = True

############################################################################
############################		Events		############################
############################################################################

def onGameStart():
	#reset color picking
	setGlobalVariable("ColorsChosen", "")
	
	#reset initiative automation
	setGlobalVariable("SetupDone", "")		
	setGlobalVariable("OppIniRoll", "0")
	setGlobalVariable("IniAllDone", "")

def onLoadDeck(player, groups):
	mute()
	if player == me:
		if validateDeck(groups[0]):
			playerSetup()
			if getGlobalVariable("SetupDone") == "": #we're the first done with setup
				setGlobalVariable("SetupDone", "x")
			else:	#other guy is done too
				for p in players:
					remoteCall(p, "SetupForIni", [])
				notify("Both players have set up. Please roll for initiative.")
		else:
			notify("Validation of {}'s deck FAILED. Please choose another deck.".format(me.name))
			for group in groups:
				for card in group:
					card.delete()

def SetupForIni():
	global hasRolledIni
	hasRolledIni = False

############################################################################
######################		Group Actions			########################
############################################################################

def playerDone(group, x=0, y=0):
	notify("{} is done".format(me.name))

def rollDice(group, x=0, y=0):
	mute()
	global diceBank
	global hasRolledIni
	global myIniRoll
	
	for c in table:
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd" and c.controller == me:
			c.delete()
	dieCard = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", -410, -80 )
	dieCard2 = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", -360, -80 )

	count = min(askInteger("Roll how many red dice?", 3),50) #max 50 dice rolled at once
	if count == None: return

	if (len(diceBank) < count): #diceBank running low - fetch more
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code: {}".format(random_org[1]))
		if random_org[1]==200: # OK code received:
			diceBank = random_org[0].splitlines()
		else:
			notify("www.random.org not responding (code:{}). Using built-in randomizer".format(random_org[1]))
			while (len(diceBank) < 20):
				diceBank.append(rnd(0,5))

	result = [0,0,0,0,0,0]
	for x in range(count):
		roll = int(diceBank.pop())
		result[roll] += 1
	debug("diceRoller result: {}".format(result))
	notify("{} rolls {} attack dice".format(me,count))

	damPiercing = result[4] + 2* result[5]
	damNormal = result[2] + 2* result[3]
	dieCard.markers[attackDie[0]] = result[0]+result[1] #blanks
	dieCard.markers[attackDie[2]] = result[2] #1
	dieCard.markers[attackDie[3]] = result[3] #2
	dieCard2.markers[attackDie[4]] = result[4] #1*
	dieCard2.markers[attackDie[5]] = result[5] #1*
	effect = rnd(1,12)
	dieCard2.markers[Died12] = effect
	
	if hasRolledIni:
		notify("{} rolled {} normal damage, {} critical damage and {} on effect die".format(me,damNormal,damPiercing,effect))
	else:
		hasRolledIni = True
		notify("{} rolled a {} for initiative".format(me, effect))
		oppRoll = eval(getGlobalVariable("OppIniRoll"))
		
		if oppRoll == 0:	#they haven't rolled yet
			setGlobalVariable("OppIniRoll", str(effect))
		elif oppRoll == effect:	#tie!
			notify("Tied initiative roll! Please roll again.")
			hasRolledIni = False
			setGlobalVariable("OppIniRoll", "0")
		elif effect > oppRoll:	#we won
			AskInitiative()
		else:	#they won
			remoteCall(players[1], "AskInitiative", [])

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def playerSetup():
	mute()

	# Players select their color
	global mycolor
	choiceList = ["Red", "Blue", "Green", "Yellow"]
	while (True):
		choice = askChoice("Pick a color:", choiceList, PlayerColor) - 1
		colorsChosen = getGlobalVariable("ColorsChosen")
		if colorsChosen == "":	#we're the first to pick
			setGlobalVariable("ColorsChosen", str(choice))
			mycolor = PlayerColor[choice]
			break
		elif str(choice) not in colorsChosen:	#not first to pick but no one else has taken this yet
			setGlobalVariable("ColorsChosen", colorsChosen + str(choice))
			mycolor = PlayerColor[choice]
			break
		else:	#someone else took our choice
			askChoice("Someone else took that color. Choose a different one.", ["OK"], ["#FF0000"])

	#set initial health and channeling values
	for c in me.hand:
		if c.Type == "Mage":
			stats = c.Stats.split(",")
			break
	for stat in stats:
		debug("stat {}".format(stat))
		statval = stat.split("=")
		if "Channeling" in statval[0]:
			me.Channeling = int(statval[1])
			me.Mana = 10+me.Channeling
			whisper("Channeling set to {} and Mana to {}".format(me.Channeling,me.Mana))
		elif "Life" in statval[0]:
			me.Life = int(statval[1])
			whisper("Life set to {}".format(me.Life))

def createVineMarker(group, x=0, y=0):
	table.create("ed8ec185-6cb2-424f-a46e-7fd7be2bc1e0", 350, -35)

def createAltBoardCard(group, x=0, y=0):
	table.create("af14ca09-a83d-4185-afa0-bc38a31dbf82", 350, -35)

def invokeflipGameBoard(group, x=0, y=0):
	mute()
	for p in players:
		remoteCall(p, "flipGameBoard", [])

def flipGameBoard():
	mute()
	global boardFlipped
	if not boardFlipped:
		table.setBoardImage("background\\gameboard-alt-a.png")
	else:
		table.setBoardImage("background\\gameboard.png")
	boardFlipped = not boardFlipped

def AskInitiative():
	notify("{} is choosing whether or not to go first.".format(me))
	choiceList = ['Yes', 'No']
	colorsList = ['#FF0000', '#0000FF'] 
	choice = askChoice("You have won initiative! Would you like to go first?", choiceList, colorsList)
	if choice == 1:
		notify("{} has elected to go first!".format(me))
		CreateIniToken()
	else:
		notify("{} has elected NOT to go first! {} has first initiative.".format(me, players[1]))
		remoteCall(players[1], "CreateIniToken", [])

def CreateIniToken():
	mute()
	card = table.create("6a71e6e9-83fa-4604-9ff7-23c14bf75d48", -360, -150 )
	card.switchTo("Planning") #skips upkeep for first turn
	init = table.create("8ad1880e-afee-49fe-a9ef-b0c17aefac3f",-420,-150) #initiative token
	if mycolor == PlayerColor[0]:
		init.switchTo("")
	elif mycolor == PlayerColor[1]:
		init.switchTo("B")
	elif mycolor == PlayerColor[2]:
		init.switchTo("C")
	elif mycolor == PlayerColor[3]:
		init.switchTo("D")
	setGlobalVariable("IniAllDone", "x")
	notify("Setup is complete, let the battle begin!")
	
def nextPhase(group, x=-360, y=-150):
	global mycolor
	if getGlobalVariable("IniAllDone") == "": # Player setup is not done yet.
		return
	mute()
	card = None
	for c in table: #find phase card
		if c.model == "6a71e6e9-83fa-4604-9ff7-23c14bf75d48":
			card = c
			break
	if card.alternate == "":
		switchPhase(card,"Planning")
	elif card.alternate == "Planning":
		switchPhase(card,"Deploy")
	elif card.alternate == "Deploy":
		switchPhase(card,"Quick")
	elif card.alternate == "Quick":
		switchPhase(card,"Actions")
	elif card.alternate == "Actions":
		switchPhase(card,"Quick2")
	elif card.alternate == "Quick2":
		if switchPhase(card,"") == True: #Back to Upkeep
			notify("Ready Stage: Performing Initiative, Reset, and Channeling Phases")
			init = [card for card in table if card.model == "8ad1880e-afee-49fe-a9ef-b0c17aefac3f"][0]
			if init.controller == me:
				flipcard(init)
			else:
				remoteCall(init.controller, "flipcard", [init])
			for p in players:
				p.Mana += p.Channeling
				notify("{} channels {}".format(p.name,p.Channeling))
			for c in table:
				if c.isFaceUp: #don't waste time on facedown cards
					#reset markers
					if c.controller == me:
						resetMarkers(c)
					else:
						remoteCall(players[1], "resetMarkers", [c])
					#resolve channeling cards (harmonize, spawnpoints, familiars)
					if c.controller == me:
						resolveChanneling(c)
					else:
						remoteCall(players[1], "resolveChanneling", [c])

			#resolve burns
			cardsWithBurn = [c for c in table if c.markers[Burn] > 0]
			if len(cardsWithBurn) > 0:
				notify("Resolving Burns (if enabled)...")	#found at least one
				for c in cardsWithBurn:
					if c.controller == me:
						resolveBurns(c)
					else:
						remoteCall(players[1], "resolveBurns", [c])
				notify("Finished auto-resolving Burns.")

def resetMarkers(c):
	mute()
	if c.markers[ActionRedUsed] == 1:
		c.markers[ActionRedUsed] = 0
		c.markers[ActionRed] = 1
	if c.markers[ActionBlueUsed] == 1:
		c.markers[ActionBlueUsed] = 0
		c.markers[ActionBlue] = 1
	if c.markers[ActionGreenUsed] == 1:
		c.markers[ActionGreenUsed] = 0
		c.markers[ActionGreen] = 1
	if c.markers[ActionYellowUsed] == 1:
		c.markers[ActionYellowUsed] = 0
		c.markers[ActionYellow] = 1
	if c.markers[QuickBack] == 1:
		c.markers[QuickBack] = 0
		c.markers[Quick] = 1
	if c.markers[Used] == 1:
		c.markers[Used] = 0
		c.markers[Ready] = 1
	if c.markers[VoltaricON] == 1:
		c.markers[VoltaricON] = 0
		c.markers[VoltaricOFF] = 1
	if c.markers[DeflectU] == 1:
		c.markers[DeflectU] = 0
		c.markers[DeflectR] = 1
	if c.markers[Visible] == 1:
		c.markers[Visible] = 0
		c.markers[Invisible] = 1
	debug("card,stats,subtype {} {} {}".format(c.name,c.Stats,c.Subtype))

def resolveBurns(card):
	#is the setting on?
	if not getSetting("AutoResolveBurns", True):
		return
	
	#roll em
	mute()
	numMarkers = card.markers[Burn]
	burnDamage = 0
	burnsRemoved = 0
	for i in range(0, numMarkers):
		roll = rnd(0, 2)
		if roll == 0:
			card.markers[Burn] -= 1
			burnsRemoved += 1
		elif roll == 1:
			burnDamage += 1
		elif roll == 2:
			burnDamage += 2
	#apply damage
	if card.Type == "Mage":
		card.controller.Damage += burnDamage
	elif card.Type == "Creature":
		card.markers[Damage] += burnDamage
	notify("{} damage added to {}. {} Burns removed.".format(burnDamage, card.Name, burnsRemoved))

def resolveChanneling(c):
	mute()
	if c.Stats != None and c.Type != "Mage":
		if "Channeling=" in c.Stats: #let's add mana for spawnpoints etc.
			channel = getStat(c.Stats,"Channeling")
			debug("Found Channeling stat {} in card {}".format(channel,c.name))
			for x in range(channel):
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
	if c.name == "Harmonize":
		c2 = cardHere(cardX(c)-1,cardY(c)-1,"Channeling=")
		if c2 != None and c2.Type != "Mage":
			debug("Overlap found (top left) {}".format(c2.name))
			addMana(c2)
			whisper("Harmonize found and Mana added to channeling card")
		else:
			c2 = cardHere(cardX(c)+c.width()+1,cardY(c)+c.height()+1,"Channeling=")
			if c2 != None and c2.Type !="Mage":
				debug("Overlap found (bottom right) {}".format(c2.name))
				addMana(c2)
				whisper("Harmonize found and Mana added to channeling card")
			else:
				c2 = cardHere(cardX(c)-1,cardY(c)+c.height(),"Channeling=")
				if c2 != None and c2.Type !="Mage":
					debug("Overlap found (bottom left) {}".format(c2.name))
					addMana(c2)
					whisper("Harmonize found and Mana added to channeling card")
				else:
					c2 = cardHere(cardX(c)+c.width()+1,cardY(c),"Channeling=")
					if c2 != None and c2.Type !="Mage":
						debug("Overlap found (top right) {}".format(c2.name))
						addMana(c2)
						whisper("Harmonize found and Mana added to channeling card")
					else:
						whisper("Harmonize found but no Mana added")


def toggleDebug(group, x=0, y=0):
	global showDebug
	showDebug = not showDebug
	if showDebug:
		notify("{} turns on debug".format(me))
	else:
		notify("{} turns off debug".format(me))

def toggleResolveBurns(group, x=0, y=0):
	autoResolveBurns = getSetting("AutoResolveBurns", True)
	setSetting("AutoResolveBurns", not autoResolveBurns)
	if autoResolveBurns:
		whisper("You have disabled automatic resolution of Burn tokens on your cards.")
	else:
		whisper("You have enabled automatic resolution of Burn tokens on your cards.")

############################################################################
######################		Card Actions			########################
############################################################################

##########################     Add Tokens     ##############################

def addDamage(card, x = 0, y = 0):
    addToken(card, Damage)

def addBurn(card, x = 0, y = 0):
	addToken(card, Burn)

def addCripple(card, x = 0, y = 0):
    addToken(card, Cripple)

def addCorrode(card, x = 0, y = 0):
    addToken(card, Corrode)

def addDaze(card, x=0, y=0):
	addToken(card, Daze)

def addMana(card, x = 0, y = 0):
	addToken(card, Mana)

def addStun(card, x=0, y=0):
	addToken(card, Stun)

def addSlam(card, x=0, y=0):
	addToken(card, Slam)

def addWeak(card, x=0, y=0):
	addToken(card, Weak)

def addOther(card, x = 0, y = 0):
	marker, qty = askMarker()
	if qty == 0: return
	card.markers[marker] += qty

##########################     Toggle Actions/Tokens     ##############################

def toggleAction(card, x=0, y=0):
	global mycolor
	mute()
	if mycolor == "#800080":
		whisper("Please perform player setup to initialize player color")
	elif mycolor == PlayerColor[0]: # Red
		if card.markers[ActionRedUsed] > 0:
			card.markers[ActionRed] = 1
			card.markers[ActionRedUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionRed] = 0
			card.markers[ActionRedUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[1]: # Blue
		if card.markers[ActionBlueUsed] > 0:
			card.markers[ActionBlue] = 1
			card.markers[ActionBlueUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionBlue] = 0
			card.markers[ActionBlueUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[2]: #Green
		if card.markers[ActionGreenUsed] > 0:
			card.markers[ActionGreen] = 1
			card.markers[ActionGreenUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionGreen] = 0
			card.markers[ActionGreenUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))
	elif mycolor == PlayerColor[3]: #Yellow
		if card.markers[ActionYellowUsed] > 0:
			card.markers[ActionYellow] = 1
			card.markers[ActionYellowUsed] = 0
			notify("'{}' readies Action Marker".format(card.Name))
		else:
			card.markers[ActionYellow] = 0
			card.markers[ActionYellowUsed] = 1
			notify("'{}' spends Action Marker".format(card.Name))

def toggleBloodReaper(card, x=0, y=0):
	toggleToken(card, BloodReaper)

def toggleDeflect(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[DeflectR] > 0:
		card.markers[DeflectR] = 0
		card.markers[DeflectU] = 1
		notify("'{}' uses deflect".format(card.Name))
	else:
		card.markers[DeflectR] = 1
		card.markers[DeflectU] = 0
		notify("'{}' readies deflect".format(card.Name))

def toggleGuard(card, x=0, y=0):
	toggleToken(card, Guard)

def toggleInvisible(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[Invisible] > 0:
		card.markers[Invisible] = 0
		card.markers[Visible] = 1
		notify("'{}' becomes visible".format(card.Name))
	else:
		card.markers[Invisible] = 1
		card.markers[Visible] = 0
		notify("'{}' becomes invisible".format(card.Name))

def toggleReady(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[Ready] > 0:
		card.markers[Ready] = 0
		card.markers[Used] = 1
		notify("'{}' becomes used".format(card.Name))
	else:
		card.markers[Ready] = 1
		card.markers[Used] = 0
		notify("'{}' becomes ready".format(card.Name))

def togglePet(card, x=0, y=0):
	toggleToken(card, Pet)

def toggleTaunt(card, x=0, y=0):
	toggleToken(card, Taunt)

def toggleTauntT(card, x=0, y=0):
	toggleToken(card, TauntT)

def toggleQuick(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[Quick] > 0:
		card.markers[Quick] = 0
		card.markers[QuickBack] = 1
		notify("'{}' spends Quick Cast action".format(card.Name))
	else:
		card.markers[Quick] = 1
		card.markers[QuickBack] = 0
		notify("'{}' readies Quick Cast action".format(card.Name))

def toggleVoltaric(card, x=0, y=0):
	mute()
	if not card.isFaceUp:
		return
	if card.markers[VoltaricON] > 0:
		card.markers[VoltaricON] = 0
		card.markers[VoltaricOFF] = 1
		notify("'{}' disables Voltaric shield".format(card.Name))
	else:
		card.markers[VoltaricON] = 1
		card.markers[VoltaricOFF] = 0
		notify("'{}' enables Voltaric shield".format(card.Name))

######################     Remove Tokens     ###########################

def subDamage(card, x = 0, y = 0):
    subToken(card, Damage)

def subBurn(card, x = 0, y = 0):
    subToken(card, Burn)

def subCripple(card, x = 0, y = 0):
    subToken(card, Cripple)

def subCorrode(card, x = 0, y = 0):
    subToken(card, Corrode)

def subDaze(card, x = 0, y = 0):
    subToken(card, Daze)

def subMana(card, x = 0, y = 0):
    subToken(card, Mana)

def subStun(card, x = 0, y = 0):
    subToken(card, Stun)

def subSlam(card, x = 0, y = 0):
	subToken(card, Slam)

def subWeak(card, x = 0, y = 0):
    subToken(card, Weak)

def clearTokens(card, x = 0, y = 0):
	mute()
	for tokenType in card.markers:
		card.markers[tokenType] = 0
	notify("{} removes all tokens from '{}'".format(me, card.Name))




############################################################################
######################		Other  Actions		################################
############################################################################

def rotateCard(card, x = 0, y = 0):
	# Rot90, Rot180, etc. are just aliases for the numbers 0-3
	mute()
	if card.controller == me:
		card.orientation = (card.orientation + 1) % 4
		if card.isFaceUp:
			notify("{} Rotates '{}'".format(me, card.Name))
		else:
			notify("{} Rotates a card".format(me))

def flipcard(card, x = 0, y = 0):
	mute()
	if "Vine" in card.name and card.controller == me:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")
		notify("{} Flips Vine Marker.".format(me))
	elif "Alt Zone" in card.name and card.controller == me:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")
		notify("{} Flips Zone Marker.".format(me))
	elif card.isFaceUp == False:
		card.isFaceUp = True
		notify("{} turns '{}' face up.".format(me, card.Name))
		card.highlight = None
		if card.Type == "Mage" or card.Type == "Creature": #places action marker on card
			toggleAction(card)
		if card.Type == "Mage": #once more to flip action to active side
			toggleAction(card)
			toggleQuick(card)
			if "Wizard" in card.name:
					card.markers[VoltaricOFF] = 1
			if "Forcemaster" == card.name:
					card.markers[DeflectR] = 1
			if "Beastmaster" == card.name:
					card.markers[Pet] = 1
			if "Beastmaster (Johktari)" == card.name:
					card.markers[WoundedPrey] = 1
			if "Priest" == card.name:
					card.markers[HolyAvenger] = 1
			if "Druid" == card.name:
					card.markers[Treebond] = 1
		if card.Type == "Creature":	
			if "Invisible Stalker" == card.name:
					card.markers[Invisible] = 1
			if "Thorg, Chief Bodyguard" == card.name:
					card.markers[TauntT] = 1
			if "Sosruko, Ferret Companion" == card.name:
					card.markers[Taunt] = 1
	elif card.alternates is not None and "B" in card.alternates: #flip the initiative card
		colorsChosen = getGlobalVariable("ColorsChosen")
		if "0" in colorsChosen and "1" in colorsChosen: #red and blue
			if card.alternate == "B":
				card.switchTo("")
			else:
				card.switchTo("B")
		elif "0" in colorsChosen and "2" in colorsChosen: #red and green
			if card.alternate == "C":
				card.switchTo("")
			else:
				card.switchTo("C")
		elif "0" in colorsChosen and "3" in colorsChosen: #red and yellow
			if card.alternate == "D":
				card.switchTo("")
			else:
				card.switchTo("D")
		elif "1" in colorsChosen and "2" in colorsChosen: #blue and green
			if card.alternate == "C":
				card.switchTo("B")
			else:
				card.switchTo("C")
		elif "1" in colorsChosen and "3" in colorsChosen: #blue and yellow
			if card.alternate == "D":
				card.switchTo("B")
			else:
				card.switchTo("D")
		elif "2" in colorsChosen and "3" in colorsChosen: #green and yellow
			if card.alternate == "D":
				card.switchTo("C")
			else:
				card.switchTo("D")
		#notify("{} turns '{}' face up.".format(me, card.Name))
	elif card.isFaceUp:
		notify("{} turns '{}' face down.".format(me, card.Name))
		card.isFaceUp = False

def discard(card, x=0, y=0):
	mute()
	if card.controller != me:
		whisper("{} does not control '{}' - discard cancelled".format(me, card))
		return
	card.isFaceUp = True

	card.moveTo(me.piles['Discard'])
	notify("{} discards '{}'".format(me, card))

def defaultAction(card, x = 0, y = 0):
	mute()
	if card.controller == me:
		if not card.isFaceUp:
			#is this a face-down enchantment? if so, prompt before revealing
			if card.Type == "Enchantment":
				if getSetting("EnchantPromptReveal", True):
					choiceList = ['Yes', 'Yes, and don\'t ask me again', 'No']
					colorsList = ['#0000FF', '#0040FF', '#FF0000'] 
					choice = askChoice("Would you like to reveal this hidden enchantment?", choiceList, colorsList)
					if choice == 0 or choice == 3:
						return
					elif choice == 2:
						setSetting("EnchantPromptReveal", False)
			
			flipcard(card, x, y)
		else:
			castSpell(card, x, y)


############################################################################
######################		Utility Functions		########################
############################################################################

def addToken(card, tokenType):
	mute()
	card.markers[tokenType] += 1
	if card.isFaceUp:
		notify("{} added to '{}'".format(tokenType[0], card.Name))
	else:
		notify("{} added to face-down card.".format(tokenType[0]))

def subToken(card, tokenType):
	mute()
	card.markers[tokenType] -= 1
	if card.isFaceUp:
		notify("{} removed from '{}'".format(tokenType[0], card.Name))
	else:
		notify("{} removed from face-down card.".format(tokenType[0]))

def toggleToken(card, tokenType):
	mute()
	if card.markers[tokenType] > 0:
		card.markers[tokenType] = 0
		if card.isFaceUp:
			notify("{} removes a {} from '{}'".format(me, tokenType[0], card.Name))
		else:
			notify("{} removed from face-down card.".format(tokenType[0]))
	else:
		card.markers[tokenType] = 1
		if card.isFaceUp:
			notify("{} adds a {} to '{}'".format(me, tokenType[0], card.Name))
		else:
			notify("{} added to face-down card.".format(tokenType[0]))

def playCardFaceDown(card, x=-360, y=0):
	global mycolor
	offset=0
	occupied = True
	if mycolor == PlayerColor[0]:
		y = -10
	elif mycolor == PlayerColor[1]:
		y = 40
	elif mycolor == PlayerColor[2]:
		y = 90
	elif mycolor == PlayerColor[3]:
		y = 140
	while occupied:
		occupied = False
		for c in table:
			if c.controller == me:
				posx, posy = c.position
				debug("c.position {}".format(c.position))
				if posx == x+offset and posy == y:
					occupied = True
					break
		if occupied:
			offset -= 30
	card.moveToTable(x+offset, y, True)
	mute()
	card.peek()
	card.highlight = mycolor

def debug(str):
	global showDebug
	if showDebug:
		whisper(str)

def moveCard(model, x, y):
	for c in table:
		if c.model == model:
			c.moveToTable(x, y)
			return c
	return table.create(model, x, y)

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


#------------------------------------------------------------
# Global variable manipulations function
#------------------------------------------------------------

#---------------------------------------------------------------------------
# Workflow routines
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def getStat(stats, stat): #searches stats string for stat and extract value
	statlist = stats.split(",")
	for statitem in statlist:
		statval = statitem.split("=")
		if statval[0] == stat:
			try:
				return int(statval[1])
			except:
				return 0
	return 0

def switchPhase(card, phase):
	global mycolor
	mute()
	if card.highlight == None: #other player not done yet
		if card.controller == me:
			card.highlight = mycolor
		else:
			remoteCall(card.controller, "remoteHighlight", [card, mycolor])
		notify("{} is done with {} phase".format(me.name,card.name))
		return False
	elif card.highlight != mycolor or showDebug:
		if card.controller == me:
			card.highlight = None
			card.switchTo(phase)
		else:
			remoteCall(card.controller, "remoteHighlight", [card, None])
			remoteCall(card.controller, "remoteSwitchPhase", [card, phase])
		notify("Phase changed to {}".format(phase))
		return True

def remoteHighlight(card, color):
	card.highlight = color

def remoteSwitchPhase(card, phase):
	card.switchTo(phase)

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def castingDiscount(cspell,cdiscount): #test if spell satisfies requirements of discount card
	#build test list from spell
	testlist = cspell.Type.split(",")
	testlist += cspell.Subtype.split(",")
	testlist += cspell.School.split(",")
	debug("casting discount testlist: {}".format(testlist))

	lines = cdiscount.Text.split("[Casting Discount]")
	debug("lines: {}".format(lines))
	if len(lines)>1: #line found - now proces it
		cells = lines[1].split("][")
		debug("cells: {}".format(cells))
		try:
			discount = int(cells[0].strip("["))
		except ValueError:
			debug("no discount value found")
			return 0
		reqstr = cells[1].strip("]") #discount requirements should be here
		reqs = reqstr.split(",")
		for req in reqs:
			debug("testing req {}".format(req.split("/")))
			found = False
			for r in req.split("/"):
				if r in testlist:
					found = True
			if not found:
				return 0
	return discount

def castSpell(card, x = 0, y = 0):
	if card.Cost != "" and card.Cost != None:
		notify("Printed casting cost of {} is {}".format(card,card.Cost))
		try:
			castingcost = int(card.Cost)
		except ValueError:
			if "+" in card.Cost: #a x+y cost as in enchantments. We want the reveal cost
				try:
					castingcosts = card.Cost.split("+")
					castingcost = int(castingcosts[1]) #reveal cost is the second one
				except ValueError:
					castingcost = 0
			elif "X" in card.Cost: #e.g. Dispel
				castingcost = 0
				#target code
			else:
				castingcost = 0

		if castingcost > 0:
			#TODO Who is casting the spell?
			infostr = "Printed casting cost is {}".format(castingcost)
			# find any discounts from equipment(School, Type, Subtype, Targetbased?)
			discount = 0
			for c in table:
				if c.controller == me and c.isFaceUp and "[Casting Discount]" in c.Text and c != card:
					discount += castingDiscount(card,c)
					if discount > 0:
						infostr += "\nCost reduced by {} due to {}".format(discount,c.name)
			infostr += "\nTotal mana amount to subtract from mana pool?"
			manacost = askInteger(infostr,castingcost-discount)
			if manacost == None:
				return
			if me.Mana < manacost:
				notify("{} has insufficient mana in pool".format(me))
				return
			me.Mana -= manacost
			notify("{} payed {} mana from pool for {}".format(me.name,manacost,card.name))

def inspectCard(card, x = 0, y = 0):
    whisper("{}".format(card))
    for k in card.properties:
        if len(card.properties[k]) > 0:
            whisper("{}: {}".format(k, card.properties[k]))

def validateDeck(deck):
	for c in deck:
		if c.Type == "Mage":
			stats = c.Stats.split(",")
			schoolcosts = c.MageSchoolCost.split(",")
			break

	debug("Stats {}".format(stats))
	spellbook = {"Dark":2,"Holy":2,"Nature":2,"Mind":2,"Arcane":2,"War":2,"Earth":2,"Water":2,"Air":2,"Fire":2,"Creature":0}

	#get spellbook point limit
	for stat in stats:
		debug("stat {}".format(stat))
		statval = stat.split("=")
		if "Spellbook" in statval[0]:
			spellbook["spellpoints"] = int(statval[1])
			break

	#get school costs
	for schoolcost in schoolcosts:
		debug("schoolcost {}".format(schoolcost))
		costval = schoolcost.split("=")
		if "Spellbook" in costval[0]:
			spellbook["spellpoints"] = int(costval[1])
		elif "Dark" in costval[0]:
			spellbook["Dark"] = int(costval[1])
		elif "Holy" in costval[0]:
			spellbook["Holy"] = int(costval[1])
		elif "Nature" in costval[0]:
			spellbook["Nature"] = int(costval[1])
		elif "Mind" in costval[0]:
			spellbook["Mind"] = int(costval[1])
		elif "Arcane" in costval[0]:
			spellbook["Arcane"] = int(costval[1])
		elif "War" in costval[0]:
			spellbook["War"] = int(costval[1])
		elif "Earth" in costval[0]:
			spellbook["Earth"] = int(costval[1])
		elif "Water" in costval[0] and c.name != "Druid":
			spellbook["Water"] = int(costval[1])
		elif "Air" in costval[0]:
			spellbook["Air"] = int(costval[1])
		elif "Fire" in costval[0]:
			spellbook["Fire"] = int(costval[1])
	debug("Spellbook {}".format(spellbook))
	#spellbook["Dark"] = sumLevel("Dark")
	levels = {}
	booktotal = 0
	epics = ["", "three"]
	for card in deck: #run through deck adding levels
		if "Novice" in card.Traits: #Novice cards cost 1 spellpoint
			debug("novice {}".format(card))
			booktotal += 1
		elif "+" in card.School: #and clause
			debug("and {}".format(card))
			schools = card.School.split("+")
			level = card.Level.split("+")
			i = 0
			for s in schools:
				try:
					levels[s] += int(level[i])
				except:
					levels[s] = int(level[i])
				i += 1
		elif "/" in card.School: #or clause
			debug("or {}".format(card))
			schools = card.School.split("/")
			level = card.Level.split("/")
			i = -1
			s_low = schools[0]
			for s in schools:
				i += 1
				if spellbook[s] < 2: #if trained in one of the schools use that one
					s_low = s
					break
			try:
				levels[s_low] += int(level[i])
			except:
				levels[s_low] = int(level[i])
		elif card.School != "": # only one school
			debug("single {}".format(card))
			try:
				levels[card.School] += int(card.Level)
			except:
				levels[card.School] = int(card.Level)

		if card.Type == "Creature" and c.name == "Forcemaster": #check for the forcemaster rule
			debug("FM creature test")
			if "Mind" not in card.School:
				if "+" in card.School:
					level = card.Level.split("+")
					for l in level:
						booktotal += int(l)
				elif "/" in card.School:
					level = card.Level.split("/")
					booktotal += int(level[0])
				elif card.School != "": # only one school
					booktotal += int(card.Level)

		if "Water" in card.School and c.name == "Druid": #check for the druid rule
			if "1" in card.Level:
				debug("Druid Water test: {}".format(card.name))
				if "+" in card.School:
					schools = card.School.split("+")
					level = card.Level.split("+")
					i = 0
					for s in schools:
						if s == "Water" and 1 == int(level[i]): #if water level 1 is here only pay 1 spell book point for it.
							levels[s] -= 1
							booktotal += 1
						i += 1
				elif "/" in card.School: #this rule will calculate wrong if water is present as level 1 but wizard is trained in another element of the same spell too
					level = card.Level.split("/")
					levels[card.School] -= 1
					booktotal += 1
				elif card.School != "": # only one school
					levels[card.School] -= 1
					booktotal += 1
				debug("levels {}".format(levels))

		if "Epic" in card.Traits:	#check for multiple epic cards
			if card.Name in epics:
				notify("*** ILLEGAL ***: multiple copies of Epic card {} found in spellbook".format(card.Name))
				return False
			epics.append(card.Name)

		if "Only" in card.Traits:	#check for school/mage restricted cards
			ok = False

			magename = c.Name
			if "Beastmaster" in magename:
				magename = "Beastmaster"
			if "Wizard" in magename:
				magename = "Wizard"
			if magename in card.Traits:	#mage restriction
				ok = True

			for s in [school for school in spellbook if spellbook[school] == 1]:
				if s + " Mage" in card.Traits:
					ok = True

			if not ok:
				notify("*** ILLEGAL ***: the card {} is not legal in a {} deck.".format(card.Name, c.Name))
				return False

	debug("levels {}".format(levels))
	for level in levels:
		debug("booktotal {}, level {}".format(booktotal,level))
		booktotal += spellbook[level]*levels[level]
	notify("Spellbook of {} calculated to {} points".format(me,booktotal))

	if (booktotal > spellbook["spellpoints"]):
		return False

	#all good!
	return True
