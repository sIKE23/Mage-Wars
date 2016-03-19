###########################################################################
##########################    v1.14.0.0     #######################################
###########################################################################

############################################################################
##########################      Codex		   #######################################
############################################################################
import sys
sys.path.append(wd("lib"))
import os

def readScriptTextFile(filename):
	"Takes a .txt file from the scriptText directory and returns a list of each line in that file."
	textDirectory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('scripts\scriptText')
	rawList = list(open('{}\{}{}'.format(textDirectory,filename,'.txt'),'r'))
	for n,text in enumerate(rawList): #We need to strip \n from the lines
		rawList[n] = text.replace("\n","").replace("^","\n") #Use ^ to indicate a newline in the txt files
	return rawList

def searchCodex(group, x=0, y=0):
		rawCodex = readScriptTextFile("Codex")
		codexDict = {}
		entry = []
		for line in rawCodex:
				if line and line[0] == '#':
						if len(entry) >= 2:
								entry[1] = ' \n'.join(entry[1:])
								keys = entry[0].split(',')
								for k in keys: codexDict[k] = entry[1]
						entry = []
				else: entry.append(line.replace('\n','').strip(' '))
		while True:
				term = askString('What would you like to know more about?','Enter codex term here')
				#Parse numbers into X
				numReplaced = False
				if not (term): break
				for c in str(term):
						if isNumber(c): term = term.replace(c,'') if numReplaced else term.replace(c,'X')
				if (codexDict.get(term) and askChoice("{}:\n{}".format(term,codexDict.get(term)),
													  ['Search for another term','Thanks, I\'m done'],
													  ['#666699','#000000']) != 1): break

def getRulingsAndClarifications(card, x=0, y=0):
		if not (card.isFaceUp or card.controller == me):
				whisper('You do not have permission to view that card')
				return
		name = card.name
		rawList = readScriptTextFile("RulingsAndClarifications")
		entry = []
		for line in rawList:
				if line and line[0] == '#':
						if len(entry) >= 2:
								entry[1] = ' \n'.join(entry[1:])
								if entry[0].replace('\n','') == name:
										askChoice("{}:\n{}".format(name,entry[1]),['Done'],['#000000'])
										return
								entry = []
				else: entry.append(line.replace('\n','').strip(' '))
		askChoice("This spell does not appear to have any rulings or clarifications. Let us know if there is a clarfication or ruling that you would like to see added!"
				  ,['Done']
				  ,['#000000'])

def isNumber(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def getEnchantRecommendationList(step):
		"""Returns a list of names of recommended enchantments to reveal"""
		rawData = readScriptTextFile("EnchantmentTiming")
		recommendationList = []
		for line in rawData:
				if line and line[0] == '#':
						if len(recommendationList) >= 2 and recommendationList[0] == step: return recommendationList[1:]
						recommendationList = []
				else: recommendationList.append(line.replace('\n','').strip(' '))
		return []

def deathMessage(traitDict,attack={},aTraitDict={}):
		"""
		Format: <death message>@criterion1=value1,criterion2=value2
		Example:
		{} dies...@Type=Creature,Subtype=Guy,Trait=Living
		"""
		card = Card(traitDict.get('OwnerID'))
		attacker = Card(aTraitDict.get('OwnerID')) if aTraitDict else None
		mage = Card(traitDict.get('MageID')) if traitDict.get('MageID') else None
		attackerMage = Card(aTraitDict.get('MageID')) if aTraitDict.get('MageID') else None
		atkTraits = attack.get('Traits',{})
		rawData = readScriptTextFile("DeathMessages")
		gender = getGender(card)
		attackerGender = getGender(attacker) if attacker else None
		deathMessages = []
		for line in rawData:
				splitLine = line.replace('\n','').split('@')
				if len(splitLine)!=2: continue
				criteriaList = splitLine[1].split(',')
				violation = False
				for c in criteriaList:
						C=c.split('=')
						if not ((C[0] == 'DamageType' and (attack and C[1]==attack.get('Type'))) or
								(C[0] == 'Range' and (attack and C[1]==attack.get('RangeType'))) or
								(C[0] == 'Trait' and traitDict.get(C[1])) or
								(C[0] == 'Subtype' and C[1] in card.Subtype) or
								(C[0] == 'Type' and C[1] in card.Type) or
								(C[0] == 'Name' and C[1] == card.Name) or
								(C[0] == 'Mage' and (mage and C[1] in mage.Name)) or
								(C[0] == 'AttackerMage' and (attackerMage and C[1] in attackerMage.Name)) or
								(C[0] == 'AttackTrait' and (attack and atkTraits.get(C[1]))) or
								(C[0] == 'AttackerType' and (attacker and C[1] in attacker.Type)) or
								(C[0] == 'AttackerName' and (attacker and C[1]==attacker.Name)) or
								(C[0] == 'AttackerSubtype' and (not attacker or not C[1] in attacker.Subtype)) or
								(C[0] == 'AttackerTrait' and (attacker and aTraitDict.get(C[1]))) or
								(C[0] == 'DamageType!' and (attack and C[1]!=attack.get('Type'))) or
								(C[0] == 'Range!' and (attack and C[1]!=attack.get('RangeType'))) or
								(C[0] == 'Trait!' and not traitDict.get(C[1])) or
								(C[0] == 'Subtype!' and C[1] not in card.Subtype) or
								(C[0] == 'Type!' and C[1] not in card.Type) or
								(C[0] == 'Name!' and C[1] != card.Name) or
								(C[0] == 'Mage!' and (mage and C[1] not in mage.Name)) or
								(C[0] == 'AttackerMage!' and (attackerMage and C[1] not in attackerMage.Name)) or
								(C[0] == 'AttackTrait!' and (attack and not atkTraits.get(C[1]))) or
								(C[0] == 'AttackerType!' and (attacker and not C[1] in attacker.Type)) or
								(C[0] == 'AttackerName!' and (attacker and C[1]!=attacker.Name)) or
								(C[0] == 'AttackerSubtype!' and (attacker and not C[1] in attacker.Subtype)) or
								(C[0] == 'AttackerTrait!' and (attacker and not aTraitDict.get(C[1])))):
								violation = True
								break
				if not violation: deathMessages.append(splitLine[0])
		if not deathMessages: return
		deathMessage = deathMessages[rnd(0,len(deathMessages)-1)]
		if attacker: deathMessage = deathMessage.replace('<A>',attacker.name.split(',')[0])
		deathMessage = deathMessage.replace('<D>',card.name.split(',')[0])
		if mage: deathMessage = deathMessage.replace('<AM>',mage.name)
		if attackerMage: deathMessage = deathMessage.replace('<DM>',attackerMage.name)
		#Pronouns
		subjectDict = {'Male' : 'he', 'Female' : 'she'}
		objectDict = {'Male' : 'him', 'Female' : 'her'}
		possessiveDict = {'Male' : 'his', 'Female' : 'her'}
		if attacker:
				deathMessage = deathMessage.replace('<as>',subjectDict.get(attackerGender,'it'))
				deathMessage = deathMessage.replace('<ao>',objectDict.get(attackerGender,'it'))
				deathMessage = deathMessage.replace('<ap>',possessiveDict.get(attackerGender,'its'))
		deathMessage = deathMessage.replace('<ds>',subjectDict.get(gender,'it'))
		deathMessage = deathMessage.replace('<do>',objectDict.get(gender,'it'))
		deathMessage = deathMessage.replace('<dp>',possessiveDict.get(gender,'its'))
		notify(deathMessage)

def getGender(card):
		genders = readScriptTextFile("Genders")
		name = card.Name
		gender = None
		for l in genders:
				line = l.replace('\n','')
				if line in ['Male','Female']:
						gender = line
				elif line == name: return gender

def getMapText(map):
		rawMapText = readScriptTextFile("MapText")
		newMapText = []
		entry = []
		for l in rawMapText:
				line = l.replace('\n','')
				if map in line:
						newMapText = line.split(':')
						return str(newMapText[1])
				elif line == map: return str(map)

def getNewFeaturesList(table, x=0, y=0):
		rawFeatures = readScriptTextFile("NewFeatures")
		featuresList = []
		entry = []
		for l in rawFeatures:
				line = l.replace('\n','')
				if line and line[0] == '#':
						if len(entry) >= 2:
								name = entry[0]
								text = ' \n'.join(entry[1:])
								featuresList.append([name,text])
						entry = []
				else: entry.append(line.strip(' '))
		choices = [f[0] for f in featuresList] + ["Thanks, that's enough for now"]
		colors = ['#666699' for f in featuresList] + ['#000000']
		while True:
				f = askChoice("Which new feature interests you?",choices,colors)
				if f in [0,len(choices)]: return
				elif askChoice(featuresList[f-1][1],['Tell me about something else','Thanks, I\'m done'],['#666699','#000000'])!=1: return

def tutorialMessage(tag):
	global tutorialTagsRead
	if not getSetting("octgnTutorial", True) or tag in tutorialTagsRead: return
	tutorialTagsRead.append(tag)
	rawData = readScriptTextFile("Tutorial")
	messageDict = {}
	key = ""
	entry = {}
	for l in rawData:
		if l == "": continue
		elif l[0] == "#":
			if key:
				messageDict[key] = entry
				entry = {}
		elif l[0] == "@": key = l[1:]
		else: entry[{">":"boxText","*":"whisperText"}[l[0]]] = l[1:]
	choices = ["\nContinue\n","Disable tutorial"]
	colors = ["#006600","#990000"]
	boxText = messageDict[tag].get("boxText")
	whisperText = messageDict[tag].get("whisperText")
	if boxText:
		choice = askChoice(boxText,choices,colors)
		if choice == 2: setSetting("octgnTutorial",False)
	if whisperText: whisper(whisperText)