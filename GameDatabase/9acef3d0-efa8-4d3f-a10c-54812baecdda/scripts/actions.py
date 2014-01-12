import time
	
ActionRed = ("Action", "4dd182d2-6e69-499c-b2ad-38701c0fb60d")
ActionRedUsed = ("Action Used", "2e069a99-1696-4cbe-b6c6-13e1dda29563")
ActionBlue = ("Action", "c980c190-448d-414f-9397-a5f17068ac58")
ActionBlueUsed = ("Action Used", "5926df42-919d-4c63-babb-5bfedd14f649")
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

showDebug = False
PlayerColor = ["#ff0000", # Red
				"#5882fa", # Blue
				"#facc2e", # Orange
				"#82fa58" ] # Green 
				
mycolor = "#82fa58" # Green
diceBank = [1]

def debug(str):
	if showDebug:
		whisper(str)
		
def toggleDebug(group, x=0, y=0):
	global showDebug
	showDebug = not showDebug
	if showDebug:
		notify("{} turns on debug".format(me))
	else:
		notify("{} turns off debug".format(me))
	
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
	
def nextPhase(group, x=-360, y=-125):
	global mycolor
	if mycolor == "#82fa58": # Playersetup is not done yet.
		return
	mute()
	card = None
	for c in table: #find phasecard
		if c.model == "6a71e6e9-83fa-4604-9ff7-23c14bf75d48":
			card = c
			break
	if card == None:
		card = table.create("6a71e6e9-83fa-4604-9ff7-23c14bf75d48", x, y )
		card.switchTo("Planning") #skips upkeep for first turn
		init = table.create("8ad1880e-afee-49fe-a9ef-b0c17aefac3f",-420,-125) #initiative token
		notify("Roll for initiative and flip token accordingly")
	elif card.alternate == "":
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
			notify("Performing ini, reset & channeling phases")
			init = moveCard("8ad1880e-afee-49fe-a9ef-b0c17aefac3f",-420,-125)
			flipcard(init)
			for p in players:
				p.Mana += p.Channeling
				notify("{} channels {}".format(p.name,p.Channeling))
			for c in table:
				if c.isFaceUp: #don't waste time on facedown cards
					if c.markers[ActionRedUsed] == 1:
						c.markers[ActionRedUsed] = 0
						c.markers[ActionRed] = 1
					if c.markers[ActionBlueUsed] == 1:
						c.markers[ActionBlueUsed] = 0
						c.markers[ActionBlue] = 1
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
					debug("card,stats,subtype {} {} {}".format(c.name,c.Stats,c.Subtype))
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
							whisper("Hamonize found and Mana added to channeling card")
						else:
							c2 = cardHere(cardX(c)+c.width()+1,cardY(c)+c.height()+1,"Channeling=")
							if c2 != None and c2.Type !="Mage":
								debug("Overlap found (bottom right) {}".format(c2.name))
								addMana(c2)
								whisper("Hamonize found and Mana added to channeling card")
							else:
								c2 = cardHere(cardX(c)-1,cardY(c)+c.height(),"Channeling=")
								if c2 != None and c2.Type !="Mage":
									debug("Overlap found (bottom left) {}".format(c2.name))
									addMana(c2)
									whisper("Hamonize found and Mana added to channeling card")
								else:
									c2 = cardHere(cardX(c)+c.width()+1,cardY(c),"Channeling=")
									if c2 != None and c2.Type !="Mage":
										debug("Overlap found (top right) {}".format(c2.name))
										addMana(c2)
										whisper("Hamonize found and Mana added to channeling card")
									else:
										whisper("Hamonize found but no Mana added")
			
		
def switchPhase(card, phase):
	global mycolor
	mute()
	if card.highlight == None: #other player not done yet
		card.highlight = mycolor
		notify("{} is done with {} phase".format(me.name,card.name))
		return False
	elif card.highlight != mycolor or showDebug:
		#debug("HL {}, mycolor {}".format(card.highlight,mycolor))
		card.highlight = None
		card.switchTo(phase)
		notify("Phase changed to {}".format(card.name))
		return True

def playerDone(group, x=0, y=0):
	notify("{} is done".format(me.name))

def rollDice(group, x=0, y=0):
	mute()
	dieCard = moveCard("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", -410, -35 )
	for c in table: #reuse existing diecard2 if possible
		if c.model == "a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd":
			if (-360,-35) == c.position:
				dieCard2 = c
				debug("found diecard 2")
				notfound = False
				break
			else:
				notfound= True
	if notfound:
		dieCard2 = table.create("a6ce63f9-a3fb-4ab2-8d9f-7d4b0108d7fd", -360, -35 )
		
	for tokenType in dieCard.markers:
		dieCard.markers[tokenType] = 0
	for tokenType in dieCard2.markers:
		dieCard2.markers[tokenType] = 0
	count = min(askInteger("Roll how many red dice?", 3),50) #max 50 dice rolled at once
	if count == None: return
	result = diceRoller(count)
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
	notify("{} rolled {} normal damage, {} critical damage and {} on effect die".format(me,damNormal,damPiercing,effect))

def diceRoller(num):
	global diceBank
	mute()
	if (len(diceBank) < num): #diceBank running low - fetch more 
		random_org = webRead("http://www.random.org/integers/?num=200&min=0&max=5&col=1&base=10&format=plain&rnd=new")
		debug("Random.org response code: {}".format(random_org[1]))
		if random_org[1]==200: # ok code received:
			diceBank = random_org[0].splitlines()
		else:
			notify("www.random.org not responding (code:{}). Using built-in randomizer".format(random_org[1]))
			while (len(diceBank) < 20):
				diceBank.append(rnd(0,5))
	result = [0,0,0,0,0,0]
	for x in range(num): 
		roll = int(diceBank.pop())
		result[roll] += 1
	debug("diceRoller result: {}".format(result))
	return result
	
def createVineMarker(group, x=0, y=0):
	table.create("ed8ec185-6cb2-424f-a46e-7fd7be2bc1e0", 350, -35)

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))	

					
def playerSetup(group=None, x=0, y=0):
	global mycolor
	mute()
	notify("{} performs a setup".format(me.name))
	# Set color of players
	id = 0
	for p in players:
		playername = getGlobalVariable("Player"+str(id))
		if playername == "":
			setGlobalVariable("Player"+str(id), str(p.name))
			debug("player {} is {}".format(id,getGlobalVariable("Player"+str(id))))
			if p.name == me.name:
				mycolor = PlayerColor[id]
		else:
			if playername == me.name:
				mycolor = PlayerColor[id]
		id += 1
	
	# Reset counters by finding mage card and apply stats
	debug("Hand length: {}".format(len(me.hand)))
	if len(me.hand) == 0:
		notify("Please load a deck before activating setup")
		return
	for c in me.hand:
		if c.Type == "Mage":
			stats = c.Stats.split(",")
			break
	debug("Stats {}".format(stats))
	spellbook = {"Dark":2,"Holy":2,"Nature":2,"Mind":2,"Arcane":2,"War":2,"Earth":2,"Water":2,"Air":2,"Fire":2,"Creature":0}
	
	for stat in stats:
		debug("stat {}".format(stat))
		statval = stat.split("=")
		if statval[0] == "Channeling":
			me.Channeling = int(statval[1])
			me.Mana = 10+me.Channeling
			whisper("Channeling set to {} and Mana to {}".format(me.Channeling,me.Mana))
		elif statval[0] == "Life":
			me.Life = int(statval[1])
			whisper("Life set to {}".format(me.Life))
		elif statval[0] == "Spellbook":
			spellbook["spellpoints"] = int(statval[1])
		elif statval[0] == "Dark":
			spellbook["Dark"] = int(statval[1])
		elif statval[0] == "Holy":
			spellbook["Holy"] = int(statval[1])
		elif statval[0] == "Nature":
			spellbook["Nature"] = int(statval[1])	
		elif statval[0] == "Mind":
			spellbook["Mind"] = int(statval[1])
		elif statval[0] == "Arcane":
			spellbook["Arcane"] = int(statval[1])
		elif statval[0] == "War":
			spellbook["War"] = int(statval[1])
		elif statval[0] == "Earth":
			spellbook["Earth"] = int(statval[1])
		elif statval[0] == "Water" and c.name != "Druid":
			spellbook["Water"] = int(statval[1])
		elif statval[0] == "Air":
			spellbook["Air"] = int(statval[1])
		elif statval[0] == "Fire":
			spellbook["Fire"] = int(statval[1])
	debug("Spellbook {}".format(spellbook))
	#spellbook["Dark"] = sumLevel("Dark")
	levels = {}
	booktotal = 0
	for card in me.hand: #run through deck adding levels
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
					
	debug("levels {}".format(levels))
	for level in levels:
		debug("booktotal {}, level {}".format(booktotal,level))
		booktotal += spellbook[level]*levels[level]
	notify("Spellbook of {} calculated to {} points".format(me,booktotal))

#def sumLevel(School):
	
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
			if me.Mana < manacost:
				notify("{} has insufficient mana in pool".format(me))
				return
			me.Mana -= manacost
			notify("{} payed {} mana from pool for {}".format(me.name,manacost,card.name))
		
def defaultAction(card, x = 0, y = 0):
	mute()
	if not card.isFaceUp: #Face down card - flip
		flipcard(card, x, y)
	else:
		castSpell(card, x, y)
	#elif card.orientation & Rot90 == Rot90: #Rotated card - refresh
	#	kneel(card, x, y)
	#else:
	#	kneel(card, x, y)
		
def kneel(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify("{} exhausts '{}'".format(me, card.Name))
    else:
        notify("{} readies '{}'".format(me, card.Name))

def inspectCard(card, x = 0, y = 0):
    whisper("{}".format(card))
    for k in card.properties:
        if len(card.properties[k]) > 0:
            whisper("{}: {}".format(k, card.properties[k]))
                                
def flipcard(card, x = 0, y = 0):
	mute()
	if card.isFaceUp == False:
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
	elif card.alternates is not None and "B" in card.alternates:
		if card.alternate == "B":
			card.switchTo("")
		else:
			card.switchTo("B")		
		#notify("{} turns '{}' face up.".format(me, card.Name))
	elif card.isFaceUp:
		card.isFaceUp = False
		notify("{} turns '{}' face down.".format(me, card.Name))        
	
def addMana(card, x = 0, y = 0):
	addToken(card, Mana)
	
def addDamage(card, x = 0, y = 0):
    addToken(card, Damage)
	
def addBurn(card, x = 0, y = 0):
	addToken(card, Burn)
    
def addCripple(card, x = 0, y = 0):
    addToken(card, Cripple)

def addDaze(card, x=0, y=0):
	addToken(card, Daze)

def addOther(card, x = 0, y = 0):
	marker, qty = askMarker()
	if qty == 0: return
	card.markers[marker] += qty
	
def addToken(card, tokenType):
	mute()
	card.markers[tokenType] += 1
	notify("{} added to '{}'".format(tokenType[0], card.Name))
	
def addStun(card, x=0, y=0):
	addToken(card, Stun)
	
def addWeak(card, x=0, y=0):
	addToken(card, Weak)
	
def subMana(card, x = 0, y = 0):
    subToken(card, Mana)

def subDamage(card, x = 0, y = 0):
    subToken(card, Damage)
	
def subBurn(card, x = 0, y = 0):
    subToken(card, Burn)
	
def subCripple(card, x = 0, y = 0):
    subToken(card, Cripple)
	
def subDaze(card, x = 0, y = 0):
    subToken(card, Daze)

def subToken(card, tokenType):
    mute()
    card.markers[tokenType] -= 1
    notify("{} removes a {} from '{}'".format(me, tokenType[0], card.Name))

def subStun(card, x = 0, y = 0):
    subToken(card, Stun)
	
def subWeak(card, x = 0, y = 0):
    subToken(card, Weak)
	
def clearTokens(card, x = 0, y = 0):
	mute()
	for tokenType in card.markers:
		card.markers[tokenType] = 0
	notify("{} removes all tokens from '{}'".format(me, card.Name))
	
def toggleAction(card, x=0, y=0):
	global mycolor
	mute()
	#PlayerColor = ["#FF0000", # Red
	#			"#5882FA", # Blue
	#			"#FACC2E", # Orange
	#			"#82FA58" ] # Green 
	if mycolor == "#82fa58":
		whisper("Please perform player setup to initialize player color")
	elif mycolor == "#ff0000": # Red
		if card.markers[ActionRedUsed] > 0:
			card.markers[ActionRed] = 1
			card.markers[ActionRedUsed] = 0
		else:
			card.markers[ActionRed] = 0
			card.markers[ActionRedUsed] = 1
	elif mycolor == "#5882fa": # Red
		if card.markers[ActionBlueUsed] > 0:
			card.markers[ActionBlue] = 1
			card.markers[ActionBlueUsed] = 0
		else:
			card.markers[ActionBlue] = 0
			card.markers[ActionBlueUsed] = 1
	
def toggleBloodReaper(card, x=0, y=0):
	toggleToken(card, BloodReaper)

def toggleDeflect(card, x=0, y=0):
	mute()
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
	
def toggleQuick(card, x=0, y=0):
	mute()
	if card.markers[Quick] > 0:
		card.markers[Quick] = 0
		card.markers[QuickBack] = 1
		notify("'{}' spends Quick Cast action".format(card.Name))
	else:
		card.markers[Quick] = 1
		card.markers[QuickBack] = 0
		notify("'{}' readies Quick Cast action".format(card.Name))
	
def toggleTaunt(card, x=0, y=0):
	toggleToken(card, Taunt)
	
def toggleToken(card, tokenType):
	mute()
	if card.markers[tokenType] > 0:
		card.markers[tokenType] = 0
		notify("{} removes a {} from '{}'".format(me, tokenType[0], card.Name))
	else:
		card.markers[tokenType] = 1
		notify("{} adds a {} to '{}'".format(me, tokenType[0], card.Name))

def toggleVoltaric(card, x=0, y=0):
	mute()
	if card.markers[VoltaricON] > 0:
		card.markers[VoltaricON] = 0
		card.markers[VoltaricOFF] = 1
		notify("'{}' disables Voltaric shield".format(card.Name))
	else:
		card.markers[VoltaricON] = 1
		card.markers[VoltaricOFF] = 0
		notify("'{}' enables Voltaric shield".format(card.Name))
		
def discard(card, x=0, y=0):
	mute()
	if card.controller != me:
		whisper("{} does not control '{}' - discard cancelled".format(me, card))
		return
	card.isFaceUp = True

	card.moveTo(me.piles['Discard'])
	notify("{} discards '{}'".format(me, card))

def playCardFaceDown(card, x=-360, y=70):
	global mycolor
	offset=0
	occupied = True
	if mycolor != "#ff0000":
		y = 140
	while occupied:
		occupied = False
		for c in table:
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
	