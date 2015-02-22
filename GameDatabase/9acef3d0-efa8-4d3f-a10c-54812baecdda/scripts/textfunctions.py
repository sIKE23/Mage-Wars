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
                                codexDict[entry[0]] = entry[1]
                        entry = []
                else: entry.append(line.replace('\n','').strip(' '))
        while True:
                term = askString('What would you like to know more about?','Enter codex term here')
                if not (term): break
                if (codexDict.get(term) and askChoice("{}:\n{}".format(term,codexDict.get(term)),
                                                      ['Search for another term','Thanks, I\'m done'],
                                                      ['#666699','#000000']) != 1): break

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

def deathMessage(traitDict,attack={}):#For now, we'll hardcode this here. Long term, we should move phrases to a text file.
        card = Card(traitDict.get('OwnerID'))
        #Now we define sets of death phrases
        deathMessages = []
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
