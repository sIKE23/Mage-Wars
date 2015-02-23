############################################################################
######################		Codex		    ########################
############################################################################
import sys
sys.path.append(wd("lib"))
import os

def searchCodex(group, x=0, y=0):
        textDirectory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('scripts\scriptText')
        rawCodex = list(open('{}\{}{}'.format(textDirectory,'Codex','.txt'),'r'))
        codexDict = {}
        entry = []
        for line in rawCodex:
                if line[0] == '#':
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

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getEnchantRecommendationList(step):
        """Returns a list of names of recommended enchantments to reveal"""
        textDirectory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('scripts\scriptText')
        rawData = list(open('{}\{}{}'.format(textDirectory,'EnchantmentTiming','.txt'),'r'))
        recommendationList = []
        for line in rawData:
                if line[0] == '#':
                        if len(recommendationList) >= 2 and recommendationList[0] == step: return recommendationList[1:]
                        recommendationList = []
                else: recommendationList.append(line.replace('\n','').strip(' '))
        return []

def deathMessage(traitDict,attack={}):
        """
        Format: <death message>@criterion1=value1,criterion2=value2
        Example:
        {} dies...@Type=Creature,Subtype=Guy,Trait=Living
        where
        criteria in [DamageType,Trait,Subtype,Type,Name]
        """
        card = Card(traitDict.get('OwnerID'))
        textDirectory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('scripts\scriptText')
        rawData = list(open('{}\{}{}'.format(textDirectory,'DeathMessages','.txt'),'r'))
        deathMessages = []
        for line in rawData:
                splitLine = line.replace('\n','').split('@')
                criteriaList = splitLine[1].split(',')
                violation = False
                for c in criteriaList:
                        C=c.split('=')
                        if not ((C[0] == 'DamageType' and C[1]==attack.get('Type')) or
                                (C[0] == 'Trait' and traitDict.get(C[1])) or
                                (C[0] == 'Subtype' and C[1] in card.Subtype) or
                                (C[0] == 'Type' and C[1] in card.Type) or
                                (C[0] == 'Name' and C[1] == card.Name)):
                                violation = True
                                break
                if not violation: deathMessages.append(splitLine[0])
        if not deathMessages: return
        deathMessage = deathMessages[rnd(0,len(deathMessages)-1)].format(card)
        notify(deathMessage)
        """
        if 'Undead' in card.Subtype:
                deathMessages = ["{} seems almost relieved as the peace of death greets it once more.",
                                 "The unholy magic binding {} together unravels, and it collapses to the floor!",
                                 "The room dims briefly as dark powers flee from {}'s corpse!"]
        elif 'Plant' in card.Subtype:
                deathMessages = ["{} wilts and shrivels away!",
                                 "{} collapses, its damage too extensive to regrow!"]
        elif 'Demon' in card.Subtype:
                deathMessages = ["{} exhales a cloud of sulfur and brimstone as it collapses!",
                                 "{} sneers mockingly at you as the life leaves its body!",
                                 "{} screams in exhilaration, its soul joyfully returning to the infernian depths whence it came!"]
        elif 'Soldier' in card.Subtype and not 'Goblin' in card.Subtype:
                deathMessages = ["{} salutes its commander with its dying breath!"
                                 "{} dies as it lived - with honor!",
                                 "{} screams a fearsome battle cry before succumbing to its injuries!"]
        elif 'Canine' in card.Subtype:
                deathMessages = ["{} whimpers and collapses!",
                                 "{} seems to have finally mastered 'Play Dead'...",
                                 "{} dies with a snarl upon its lips!"]
        elif 'Angel' in card.Subtype:
                deathMessages = ["{} falls, a beatific smile upon its lips.",
                                 "The radiant glow fades from {} as its eyes close forever.",
                                 "You hear the faint sound of a heavenly choir as {} passes from this world."]
        elif traitDict.get('Incorporeal'):
                deathMessages = ["{} dissipates into nothingness!"
                                 "{} fades away like mist!"]
        elif card.Type == 'Creature':
                deathMessages = ["{} has perished in battle!",
                                 "{} falls in combat!"]
        elif card.Type == 'Conjuration':
                deathMessages = ["{} crumbles to the ground!",
                                 "{} is demolished!"]

        deathMessage = deathMessages[rnd(0,len(deathMessages)-1)].format(card)
        notify(deathMessage)
        """
