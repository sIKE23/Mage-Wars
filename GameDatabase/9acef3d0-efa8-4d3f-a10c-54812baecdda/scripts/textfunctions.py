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
        criteria in [DamageType,Trait,Subtype,Type,Name,AttackTrait]
        """
        card = Card(traitDict.get('OwnerID'))
        atkTraits = attack.get('Traits',{})
        textDirectory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('scripts\scriptText')
        rawData = list(open('{}\{}{}'.format(textDirectory,'DeathMessages','.txt'),'r'))
        deathMessages = []
        for line in rawData:
                splitLine = line.replace('\n','').split('@')
                criteriaList = splitLine[1].split(',')
                violation = False
                for c in criteriaList:
                        C=c.split('=')
                        if ((C[0] == 'DamageType' and C[1]!=attack.get('Type')) or
                            (C[0] == 'Trait' and not traitDict.get(C[1])) or
                            (C[0] == 'Subtype' and not C[1] in card.Subtype) or
                            (C[0] == 'Type' and not C[1] in card.Type) or
                            (C[0] == 'Name' and C[1] != card.Name) or
                            (C[0] == 'AttackTrait' and not atkTraits.get(C[1])) or
                            (C[0] == 'DamageType!' and C[1]==attack.get('Type')) or
                            (C[0] == 'Trait!' and traitDict.get(C[1])) or
                            (C[0] == 'Subtype!' and C[1] in card.Subtype) or
                            (C[0] == 'Type!' and C[1] in card.Type) or
                            (C[0] == 'Name!' and C[1] == card.Name) or
                            (C[0] == 'AttackTrait!' and atkTraits.get(C[1]))):
                                violation = True
                                break
                if not violation: deathMessages.append(splitLine[0])
        if not deathMessages: return
        deathMessage = deathMessages[rnd(0,len(deathMessages)-1)].format(card)
        notify(deathMessage)
