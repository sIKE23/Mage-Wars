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
