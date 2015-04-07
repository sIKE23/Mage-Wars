"""
This file contains functions for generating data to be used in other functions.
The functions in this file are NOT used by the module, and should not be included
in its definition.
"""

additiveTraits = ["Melee","Ranged",
                  "Armor","Life","Innate Life","Channeling","Defense",
                  "Tough",
                  "Charge",
                  "Bloodthirsty",
                  "Piercing",
                  "Mana Drain",
                  "Mana Transfer",
                  "Magebind",
                  "Lifebond",
                  "Upkeep",
                  'Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic']
superlativeTraits = ["Regenerate",
                     "Aegis",
                     "Uproot",
                     "Dissipate"]

damageTypes = ['Flame','Acid','Lightning','Light','Wind','Hydro','Poison','Psychic']

def cardParser(filePath):
    """
    - Formats the contents of an xml file as spell dictionary entries.
    - Put r (no quotes) before filepath to prevent backslash errors.
    - Can use SHIFT+RCLICK on file, then select 'copy file as path' to make obtaining the filepath easy.
    """
    #First, we create a list of cards in the set.
    rawFile = list(open(filePath,'r'))
    rawCardList = []
    append = rawCardList.append
    startReadCard = False
    tempCard = []
    tAppend = tempCard.append
    for line in rawFile:
        line = line.replace("&apos;","\\'").replace("&amp;","&")
        replace = line.replace
        strip = line.strip
        if "<card id=" in line:
            startReadCard = True
            line = replace('\n','')
            line = line.strip()
            line = line.replace("\" name","\"SPLITHERE!!!name")
            line = line.strip('<>')
            line = line.replace(" /","")
            line = line.split('SPLITHERE!!!')
            tAppend(line)
        elif "</card>" in line:
            startReadCard = False
            append(list(tempCard))
            tempCard = []
            tAppend = tempCard.append
        elif "<property name=" in line and startReadCard:
            line = replace('\n','')
            line = line.strip()
            line = line.replace("\" value","\"SPLITHERE!!!value")
            line = line.strip('<>')
            line = line.replace(" /","")
            line = line.split('SPLITHERE!!!')
            tAppend(line)
    #Now we have a list of cards. Let's reformat them as a copy-pastable dictionary:
    processedCardList = []
    append = processedCardList.append
    for c in rawCardList:
        name = ""
        pCard = []
        app = pCard.append
        specialSubtypes = []
        cSubtypes = []
        cType = None
        cAction = None
        for l in c:
            pType = l[0].split("=")[1].strip("\"")
            pValue = l[1].split("value=")[1].strip("\"") if 'property name' in l[0] else l[1].split("name=")[1].strip("\"")
            if "card id" in l[0]: #It is the first line.
                name = pValue
                app("'Name' : '{}'".format(name))
                app("'GUID' : '{}'".format(pType))
            elif "property name" in l[0]:
                if pType == "Type": #Mages and Walls will be treated as subtypes
                    if pValue == "Conjuration-Wall":
                        app("'Type' : 'Conjuration'")
                        cType = "Conjuration"
                        specialSubtypes.append("Wall")
                    elif pValue == "Mage": #Does not take level 4 apprentice mages into account. We can just do those manually, though.
                        app("'Type' : 'Creature'")
                        app("'Level' : 6")
                        cType = "Creature"
                        specialSubtypes.append("Mage")
                    else:
                        cType = pValue
                        app("'Type' : '{}'".format(pValue))
                elif pType == "Subtype":
                    cSubtypes = pValue.split(', ') + specialSubtypes
                    if cSubtypes and cSubtypes != ['']:
                        app("'Subtypes' : {}".format(str(cSubtypes))) #Note the plural
                elif pType == "Cost":
                    if cType == "Enchantment":
                        app("'Cast Cost' : 2")
                        reveal  = pValue.split('+')[1]
                        try: app("'Reveal Cost' : {}".format(str(int(reveal))))
                        except: app("'Reveal Cost' : 0") 
                    else:    
                        try: app("'Cast Cost' : {}".format(str(int(pValue)))) 
                        except: app("'Cast Cost' : 0")
                elif pType == "Action":
                    cAction = pValue
                    app("'Action' : '{}'".format(pValue))
                elif pType == "Range":
                    app("'Minimum Range' : {}".format(pValue.split('-')[0]))
                    app("'Maximum Range' : {}".format(pValue.split('-')[1]))
                elif pType == "Target": #Note: does NOT use final target format, just distinguishes between basic target types. Use onComputeLegality functions to take care of special restrictions.
                    tList = []
                    if "Creature" in pValue or "Object" in pValue or pValue == "Mage": tList.append("Creature")
                    if "Conjuration" in pValue or "Object" in pValue: tList.append("Conjuration")
                    if "Enchantment" in pValue or "Object" in pValue: tList.append("Enchantment")
                    if "Equipment" in pValue or "Object" in pValue: tList.append("Equipment")
                    if "Zone" == pValue or "Zone Border"==pValue: tList.append(pValue)
                    app("'Targets' : {}".format(str(tList)))
                elif pType == "School": #Want to give school as dictionaries, with levels indexed by school
                    if "+" in pValue: app("'Schools' : {}".format(str(pValue.split("+"))))
                    elif "/" in pValue: app("'Schools' : {}".format(str(pValue.split("/"))))
                    else: app("'Schools' : {}".format(str([pValue])))
                elif pType == "Level":
                    if "+" in pValue:
                        levels = pValue.split("+")
                        level = sum(map(lambda x: int(x),levels))
                        app("'Level' : {}".format(str(level)))
                    elif "/" in pValue:
                        level = pValue.split("/")[0] #Let's assume we will will never have AND and OR on the same card.
                        app("'Level' : {}".format(str(level)))
                    else:
                        app("'Level' : {}".format(pValue))
                elif pType == "Stats" and pValue:
                    args = pValue.split(', ')
                    for a in args:
                        pair = a.split('=')
                        p0,p1 = pair[0],pair[1]
                        if p0 in ["Armor","Life","Channeling"]:
                            try: int(p1)
                            except: p1 = '0' #Non-integer values default to 0
                            app("'{}' : {}".format(p0,p1))
                        if p0 == "Defense":
                            defenseStr = p1
                            defDict = {}
                            if 'No Melee' in defenseStr: defDict['Restrictions'] = 'Melee'
                            elif 'No Ranged' in defenseStr: defDict['Restrictions'] = 'Ranged'
                            defTraitList = defenseStr.split(' ')
                            for d in defTraitList:
                                if '+' in d: defDict['Minimum'] = int(d.strip('+'))
                                if 'x' in d: defDict['Uses'] = int(d.strip('x'))
                            app("'Defenses' : [{"+
                                "\n\t'Minimum Roll' : {}".format(defDict['Minimum'])+
                                ("\n\t'Maximum Uses' : {}".format(defDict['Uses']) if defDict.get('Uses') else '')+
                                ("\n\t'Weakness' : '{}'".format(defDict['Restrictions']) if defDict.get('Restrictions') else '')+
                                "\n\t}]")
                elif pType == "AttackBar" and pValue:
                    attackKeyList = [attack.split(':&#xD;&#xA;') for attack in pValue.split(']&#xD;&#xA;')]
                    for a in attackKeyList:
                        if len(a)==1:
                            a.append(name)
                            a.reverse()
                        a[1] = [t.strip('[]') for t in a[1].split('] [')]
                        d12 = False
                        for n,t in enumerate(list(a[1])):
                            if ' +' in t:
                                tSplit = t.split(' +')
                                try: a[1][n] = "'{} +X': {}".format(tSplit[0],str(int(tSplit[1])))
                                except: a[1][n] = "'{} +X': {}".format(tSplit[0],"0")
                            elif ' -' in t:
                                tSplit = t.split(' -')
                                try: a[1][n] = "'{} -X': -{}".format(tSplit[0],str(int(tSplit[1])))
                                except: a[1][n] = "'{} -X': -{}".format(tSplit[0],"0")
                            elif "Dice" in t:
                                tSplit = t.split('=')
                                try: a[1][n] = "'Dice': {}".format(str(int(tSplit[1])))
                                except: a[1][n] = "'Dice': 0"
                            elif "d12"==t:
                                d12 = True
                                a[1][n]==None
                            elif d12:
                                tSplit = a[1][n].split("; ")
                                for i,s in enumerate(tSplit):
                                    sSplit = s.split(" = ")
                                    sSplit[1] = [sSplit[1].split('2 ')[1],sSplit[1].split('2 ')[1]] if '2' in sSplit[1] else sSplit[1].split(' & ')
                                    tSplit[i] = "{}: {}".format(sSplit[0].split('+')[0].split('-')[0],sSplit[1])
                                a[1][n] = "'d12': {"+', '.join(tSplit)+"}"
                                d12 = False
                            elif t in damageTypes: a[1][n] = "'Damage Type': '{}'".format(t)
                            elif t in ["Quick","Full"]: a[1][n] = "'Action': '{}'".format(t)
                            elif t=="Melee":
                                a[1][n] = "'Range Type': 'Melee'"
                                a[1].append("'Minimum Range': 0")
                                a[1].append("'Maximum Range': 0")
                            elif "Ranged:" in t:
                                a[1][n] = "'Range Type': 'Ranged'"
                                tSplit = t.split(":")[1].split("-")
                                a[1].append("'Minimum Range': {}".format(tSplit[0]))
                                a[1].append("'Maximum Range': {}".format(tSplit[1]))
                            elif t in ["Passage Attack","Damage Barrier"]: a[1][n] = "'Range Type': '{}'".format(t)
                            elif "." in t and not "vs" in t: a[1][n] = "'Text': '{}'".format(t)
                            else: a[1][n] = "'{}': True".format(t)
                        a[1] = [e for e in a[1] if e!="d12"]
                    if attackKeyList:
                        attackList = ["'Name': '" + a[0] + "',\n\t" + ",\n\t".join(a[1]) for a in attackKeyList]
                        app("'Attacks' : [{\n\t"+
                                "\n\t},{\n\t".join(attackList)+"\n\t}]")
                elif pType == "Traits":
                    if not pValue: continue
                    tList = pValue.split(", ")
                    dList = []
                    for t in tList:
                        done = False
                        for a in additiveTraits:
                            if a in t and not "Immunity" in t:
                                try: t,v = (t.split(" +")[0],int(t.split(" +")[1])) if " +" in t else (t.split(" -")[0],int(t.split(" -")[1])+1)
                                except ValueError: (t.split(" +")[0],0) if " +" in t else (t.split(" -")[0],0)
                                t = t + " +X"
                                dList.append([t,v])
                                done = True
                        if not done:
                            for s in superlativeTraits:
                                if s in t:
                                    try: t,v = s + " X",t.replace(s+" ","")
                                    except ValueError: t,v = s + " X",0
                                    dList.append([t,v])
                                    done = True
                        if not done: dList.append([t,True])
                    app("'Traits' : {\n\t"+
                                    ",\n\t".join(["'"+t[0]+"': "+str(t[1]) for t in dList])+
                                    "\n\t}")
                elif pType == "Text": app("'Text' : \"{}\"".format(pValue.replace("&#xD;&#xA;","\n").replace("&amp;","&")))
                #Card IDs are useless in-game.
                            
                    
        if cType in ["Enchantment","Creature","Conjuration","Equipment","Attack","Incantation"]: append((name,pCard))
    #Finally, print the results so we can copypaste them.
    for n,c in processedCardList:
        pass
        print "spellDictionary['"+n+"'] = {"
        print ",\n".join(c)
        print "}\n\n"
