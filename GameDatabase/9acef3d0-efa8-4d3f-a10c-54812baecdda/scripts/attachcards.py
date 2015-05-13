###########################################################################
##########################    v1.12.0.0     #######################################
###########################################################################
############################
# Card Attachment and Alignment
############################

def menuDetachAction(card,x=0,y=0):
    """This detaches <card> and returns it to its home location"""
    mute()
    if isAttached(card):
        detach(card)
        moveCardToDefaultLocation(card,True)

def attachToTarget(card,x=0,y=0):
    """This command is used to explicitly attach one card to the card currently being targeted."""
    mute()
    if isAttachCardsEnabled() == "True":
        if card.controller == me:
            target = [cards for cards in table if cards.targetedBy==me]
            if len(target) == 0 or (len(target) == 1 and card in target):
                c,t = detach(card)
                if t:
                    notify("{} detaches {} from {}.".format(me,c,t))
            elif len(target) == 1:
                c,t = attach(card, target[0])
                if t:
                    notify("{} attaches {} to {}.".format(me,c,t))
            else:
                whisper("Incorrect targets, select up to 1 target.")
                return
    else:
        whisper("AttachCards must be enabled to use this feature")
    return

def attach(card,target):
    """Controller of <card> may attach it to <target>."""
    mute()
    unbind(card)
    if card.controller == me and canAttach(card,target):
        detachAll(card)
        consolidateAttachments(target)
        setGlobalDictEntry("attachDict",card._id,[target._id,len(getAttachments(target))+1])
        remoteCall(target.controller,'alignAttachments',[target])
        return card,target
    return card,None

def enchantmentAttachCost(card,target): #Target useful for when things like Harshforge Plate are integrated into this.
    discountStr = ''
    discount = 0
    foundDiscounts = []
    infostr = 'Enchantments cost 2 mana to cast.'
    notifyStr = "{} attaches a hidden enchantment on {}, with a base cost of 2 mana.".format(me, target.name)
    for c in table:
        if c.controller == me and c.isFaceUp and "[Casting Discount]" in c.Text and c != card:
            dc = findDiscount(card, c)
            debug("Discount Count Returned from test: {} from card: {}".format(dc, c.Name))
            if dc > 0:
                discountStr = "\nCost reduced by {} due to {}".format(dc, c.name)
                infostr = notifyStr + discountStr
                notifyStr = notifyStr + discountStr
                discount += dc
                foundDiscounts.append(c)
            elif dc < 0:
                discountStr = "\n{} already reached max uses this round.".format(c.name)
                infostr = notifyStr + discountStr
                notifyStr = notifyStr + discountStr
    choice = askChoice('Do you want to cast {} face-down on {}?'.format(card.name,target.name),['Yes, I am casting this as a spell','No, I want to attach it for other reasons'],["#171e78","#de2827"])
    if choice == 1:
        infostr += "\nTotal mana amount to subtract from mana pool?"
	manacost = askInteger(infostr, 2 - discount)
	if manacost == None: return # player closed the window and didn't cast the spell
        elif me.Mana < manacost:
                notify("{} has insufficient mana in pool".format(me))
                return
        for dc in foundDiscounts:
	    doDiscount(dc)
	me.Mana -= manacost 
        notify(notifyStr)
                
def detach(card):
    """Removes <card> from its target, then consolidates remaining cards on target."""
    mute()
    if isAttached(card) and card.controller == me:
        target = getGlobalDictEntry('attachDict',card._id)
        setGlobalDictEntry('attachDict',card._id,None)
        if target:
            target = Card(target[0])
            consolidateAttachments(target)
            if card.controller == me: alignAttachments(target)
            else: remoteCall(target.controller,'alignAttachments',[target])
        return card,target
    return card,None

def alignAttachments(card):
    """Orders <card> and its attachments"""
    mute()
    if card.controller == me:
        attachments = getAttachments(card)
        prevCards  = [card]
        count = 1
        x,y = card.position
        alignQueue = {}
        side = (-1 if table.isInverted(y) else 1)
        for c in attachments:
            Y = y-(count*side)*12
            #Please align your own cards first...
            if c.controller == me:
                c.moveToTable(x,Y)
                for p in reversed(prevCards):
                    if p.controller == me:
                        c.setIndex(p.getIndex)
                        break
            #...before assisting other players
            else:
                controller = c.controller
                if controller not in alignQueue: alignQueue[controller] = []
                alignQueue[controller].append({'cardId' : c._id, 'X' : x, 'Y' : Y, 'prevCardIds' : [i._id for i in prevCards]})
            count += 1
            prevCards.append(c)
        #Remotely trigger alignment in other players
        alignedPlayers = [me]
        for p in alignQueue:
            if p in getPlayers():
                alignedPlayers.append(p)
                rnd(1,10) #avoids desync issues
                remoteCall(p,'remoteAlign',[alignQueue[p],alignedPlayers])

def remoteAlign(alignData,alignedPlayers):
    mute()
    for d in alignData:
        card,X,Y,prevCards = Card(d['cardId']),d['X'],d['Y'],[Card(i) for i in d['prevCardIds']]
        card.moveToTable(X,Y)
        for c in reversed(prevCards):
            if c.controller in alignedPlayers:
                card.setIndex(c.getIndex)
                break

def detachAll(card):
    """Removes all attachments from <card> and places them in front of their owners"""
    mute()
    attachments = getAttachments(card)
    for c in attachments:
        if c.controller == me:
            detach(c)
            moveCardToDefaultLocation(c,True)
        else:
            remoteCall(c.controller,'detach',[c])
            remoteCall(c.controller,'moveCardToDefaultLocation',[c,True])
        rnd(0,0)

def unbindAll(card):
    """Like detachAll, but for bound spells"""
    mute()
    c = getBound(card)
    if c:
        if c.controller == me:
            unbind(c)
            moveCardToDefaultLocation(c,True)
        else:
            remoteCall(c.controller,'unbind',[c])
            remoteCall(c.controller,'moveCardToDefaultLocation',[c,True])
        rnd(0,0)

def isAttached(card):
    """Determines whether <card> is attached to anything."""
    mute()
    if getGlobalDictEntry('attachDict',card._id) and card in table:
        return True
    return False

def consolidateAttachments(card):
    return
    """Reorders attachments on target card to eliminate gaps between indices"""
    mute()
    aDict = eval(getGlobalVariable("attachDict"))
    attachments=getAttachments(card)
    count = 1
    for c in attachments:
        aDict[c._id] = [card,count]
        count +=1
    setGlobalVariable("attachDict",str(aDict))

def getAttachments(card):
    """Returns a list of cards that are attached to <card>, sorted by their attachment order"""
    mute()
    aDict = eval(getGlobalVariable("attachDict"))
    attachList = [key for key in aDict if aDict[key] and int(aDict[key][0]) == card._id]
    attachList.sort(key=lambda k: aDict[k][1])
    return [Card(key) for key in attachList if Card(key) in table]

def getAttachTarget(card):
    mute()
    result = getGlobalDictEntry('attachDict',card._id)
    if result and card in table: return Card(result[0])

def getGlobalDictEntry(dictionary,key):
    """Dictionary is input as a string. If the value is empty, returns False"""
    mute()
    gDict = eval(getGlobalVariable(dictionary))
    if key in gDict:
        return gDict[key]
    return None

def setGlobalDictEntry(dictionary,key,value):
    """Note that dictionary is input as a string"""
    mute()
    gDict = eval(getGlobalVariable(dictionary))
    gDict[key] = value
    setGlobalVariable(dictionary,str(gDict))

def canAttach(card,target):
    """Determines whether <card> may be attached to <target>"""
    tType = target.Type
    if (card==target
        or not target in table
        or not card in table
        or tType not in ['Conjuration','Creature','Conjuration-Wall','Equipment','Mage']
        or not target.isFaceUp
        or isAttached(target)
        or getAttachments(card)): return False
    cName = card.Name
    tName = target.Name
    cTargetBar = card.Target
    cType = card.Type
    attachments = getAttachments(target)
    cController = card.controller
    tController = target.controller
    for a in attachments:
        if (a.isFaceUp or a.controller == me) and a.Name == cName: return False
    traits = computeTraits(target)
    for s in card.Subtype.split(', '):
        if s in traits.get('Immunity',[]): return False
    if cName in ['Force Hold','Force Crush','Tanglevine','Stranglevine'] and traits.get('Uncontainable'): return False
    if cType == 'Enchantment':
        if ((cName == 'Harmonize' and 'Channeling' in target.Stats) or
            (cName == 'Barkskin' and tName == 'Druid') or
            (cName == 'Forcefield' and tName == 'Forcemaster') or
            (cTargetBar == 'Corporeal Creature' and tType in ['Creature','Mage'] and traits.get('Corporeal')) or
            (cTargetBar == 'Creature' and tType in ['Creature','Mage']) or
            (cTargetBar == 'Friendly Living Creature' and tType in ['Creature','Mage'] and traits.get('Living') and tController == cController) or
            (cTargetBar == 'Friendly, Soldier Creature' and tType in ['Creature','Mage'] and 'Soldier' in target.Subtype and tController == cController) or
            (cTargetBar == 'Incorporeal Creature' and tType in ['Creature','Mage'] and traits.get('Incorporeal')) or
            (cTargetBar == 'Living Creature' and tType in ['Creature','Mage'] and traits.get('Living')) or
            (cTargetBar == 'Living Non-Mage Creature' and tType == 'Creature' and traits.get('Living')) or #Ugh...
            (cTargetBar == 'Mage' and tType == 'Mage') or
            (cTargetBar == 'Non-Flying Creature' and tType in ['Creature','Mage'] and not traits.get('Flying')) or
            (cTargetBar == 'Nonliving Corporeal Conjuration' and 'Conjuration' in tType and traits.get('Corporeal')) or
            (cTargetBar == 'Non-Mage Corporeal Creature' and tType=='Creature' and traits.get('Corporeal')) or
            (cTargetBar == 'Non-Mage Creature' and tType=='Creature') or
            (cTargetBar == 'Non-Mage Living Creature' and tType=='Creature' and traits.get('Living')) or
            (cTargetBar == 'Non-Mage, Non-Epic Living Creature' and tType=='Creature' and traits.get('Living') and not traits.get('Epic')) or
            (cTargetBar == 'Zone or Object')): return True
    elif ((cType == 'Equipment' and tType == 'Mage') or
        (cName in ['Tanglevine','Stranglevine','Quicksand'] and tType in ['Creature','Mage'] and not traits.get('Flying'))): return True
    return False

def isAttachCardsEnabled():
    """Checks whether the attachCards module is turned on."""
    return getSetting("attachCards", "True")

############################################################################
##########################  Bound Spells  ##################################
############################################################################
"""We will make a distinction between attached cards and bound cards (for familiars,
spawnpoints, and spellbind objects"""

def bind(card,target):
    """Controller of <card> may attach it to <target>."""
    mute()
    detach(card)
    if card.controller == me:
        b = getBound(target)
        if b: unbind(b)
        detachAll(card)
        setGlobalDictEntry("bindDict",card._id,target._id)
        remoteCall(target.controller,'alignBound',[target])
        return card,target
    return card,None

def unbind(card):
    """Unbinds <card> from its target."""
    mute()
    if getBindTarget(card) and card.controller == me:
        target = getGlobalDictEntry('bindDict',card._id)
        setGlobalDictEntry('bindDict',card._id,None)
        return card,target
    return card,None

def getBound(card):
    """Returns the card bound to <card>"""
    mute()
    bDict = eval(getGlobalVariable("bindDict"))
    bound = map(lambda key: Card(key),[k for k in bDict if bDict[k]==card._id])
    if bound: return bound[0]

def getBindTarget(card):
    mute()
    result = getGlobalDictEntry('bindDict',card._id)
    if result and card in table: return Card(result)

def alignBound(card):
    mute()
    bound = getBound(card)
    if not bound: return
    x,y = card.position
    x -= 0
    y += 30
    z = card.getIndex
    if bound.controller == me: moveAndSetIndex(bound,x,y,z)
    else: remoteCall(bound.controller,'moveAndSetIndex',[bound,x,y,z])
    card.setIndex(z+1) #Assumes I control <card>. Not sure why I need this when alignAttachments works without, but it seems that moving a card brings it to the front.

def moveAndSetIndex(card,x,y,z):
    mute()
    card.moveToTable(x,y)
    card.setIndex(z)

def canBind(card,target):
    """Determines whether <card> may be attached to <target>"""
    if (card==target
        or not target in table
        or not card in table
        or isAttached(target)
        or getAttachments(card)
        or getBound(card)
        or getBound(target)
        or not target.isFaceUp): return False
    tName = target.Name
#Familiars
    if ((tName == 'Goblin Builder' and 'Conjuration' in card.Type and card.Name not in['Tanglevine','Stranglevine','Quicksand'])
        or (tName == 'Thoughtspore' and card.Type in ['Attack','Incantation'] and sum([int(i) for i in card.level.split('+')])<=2)
        #or sectarus, but I haven't got around to it yet.
        or (tName == 'Wizard\'s Tower' and card.Type == 'Attack' and 'Epic' not in card.Traits and card.Action == 'Quick')
        or (tName == 'Sersiryx, Imp Familiar' and ((card.Type == 'Attack' and 'Fire' in card.School) or (card.Type == 'Enchantment' and 'Curse' in card.Subtype)) and sum([int(i) for i in card.level.split('+')])<=2)
        or (tName == 'Fellella, Pixie Familiar' and card.Type == 'Enchantment')
        or (tName == 'Huginn, Raven Familiar' and card.Type == 'Incantation' and sum([int(i) for i in card.level.split('+')])<=2)
        or (tName == 'Gurmash, Orc Sergeant' and 'Command' in card.Subtype)
#Spawnpoints
        or (tName == 'Barracks' and card.Type == 'Creature' and 'Soldier' in card.Subtype and target.markers[Mana] >= 2)
        or (tName == 'Battle Forge' and card.Type == 'Equipment')
        or (tName == 'Gate to Voltari' and card.Type == 'Creature' and 'Arcane' in card.School and not ("Incorporeal" in card.Traits) and target.markers[Mana] >= 3)
        or (tName == 'Lair' and card.Type == 'Creature' and 'Animal' in card.Subtype)
        or (tName == 'Pentagram' and card.Type == 'Creature' and 'Dark' in card.School and not ('Nonliving' in card.Traits or 'Incorporeal' in card.Traits) and target.markers[Mana] >= 2)
        or (tName == 'Temple of Asyra' and card.Type == 'Creature' and 'Holy' in card.School and target.markers[Mana] >= 2)
        or (tName == 'Graveyard' and card.Type == 'Creature' and 'Dark' in card.School and ('Nonliving' in card.Traits or 'Incorporeal' in card.Traits))
        or (tName == 'Seedling Pod' and card.Type in ['Creature','Conjuration','Conjuration-Wall'] and 'Plant' in card.Subtype and target.markers[Mana] >= 3)
        or (tName == 'Samara Tree' and card.name == 'Seedling Pod')
        or (tName == 'Vine Tree' and card.Type in ['Creature','Conjuration','Conjuration-Wall'] and 'Vine' in card.Subtype)
        or (tName == 'Libro Mortuos' and card.Type == 'Creature' and 'Undead' in card.Subtype)
#Spellbind (only)
        or (tName == 'Helm of Command' and card.Type == 'Incantation' and 'Epic' not in card.Traits and 'Command' in card.Subtype)
        or (tName == 'Elemental Wand' and card.Type == 'Attack' and 'Epic' not in card.Traits)
        or (tName == 'Mage Wand' and card.Type == 'Incantation' and 'Epic' not in card.Traits)):
        return True
    return False

############################################################################
##########################    Zones       ##################################
############################################################################

def createMap(I,J,zoneArray,tileSize):
    mapDict = {'I' : I,
               'J' : J,
               'tileSize' : tileSize,
               'x' : -tileSize*I/2,
               'y' : -tileSize*J/2,
               'X' : tileSize*I,
               'Y' : tileSize*J}
    array = list(zoneArray)
    zoneList = []
    for i in range(len(zoneArray)):
        for j in range(len(zoneArray[0])):
            z = (createZone(i,j,mapDict['x'],mapDict['y'],mapDict['tileSize']) if zoneArray[i][j] else {})
            array[i][j] = z 
            if z: zoneList.append(z)
    mapDict['zoneArray'] = array
    mapDict['zoneList'] = zoneList
    return mapDict

def createZone(i,j,mapX,mapY,size):
    return  {'i' : i,
             'j' : j,
             'x' : mapX+i*size,
             'y' : mapY+j*size,
             'size' : size}

def zoneContains(zone,card): #returns whether an object is inside the zone
    x,y = card.position
    X,Y = card.width(),card.height()
    if getAttachTarget(card):
        return zoneContains(zone,getAttachTarget(card))
    else:
        if ((zone.get('x') < x < zone.get('x') + zone.get('size') - X) and
            (zone.get('y') < y < zone.get('y') + zone.get('size') - Y)): return True
    return False

def zoneBorders(zone,card): #returns whether an object overlaps the zone border
    x,y = card.position
    X,Y = card.width(),card.height()
    if (zoneContains(zone,card) or
        (x > zone.get('x') + zone.get('size')) or (x < zone.get('x') - X) or
        (y > zone.get('y') + zone.get('size')) or (y < zone.get('y') - Y)): return False
    return True

def zoneClosest(zoneList,card): #finds closest zone from a list. If border is enabled, returns
    x,y = card.position
    X,Y = card.width(),card.height()
    x += X/2
    y += Y/2
    zone = zoneList[0]
    for z in zoneList:
        zX, zY = z.get('x')+z.get('size')/2,z.get('y')+z.get('size')/2
        zoneX, zoneY = zone.get('x')+zone.get('size')/2,zone.get('y')+zone.get('size')/2
        if abs(zX-x)+abs(zY-y) < abs(zoneX-x)+abs(zoneY-y): zone = z
    return zone

def zoneGetContain(zone,card): # Finds the closest straight-line place to move the object so it is contained.
    x,y = card.position
    X,Y = card.width(),card.height()
    coordinates = [x,y]
    if (x <= zone.get('x')): coordinates[0] = zone.get('x') + 1
    if (x + X >= zone.get('x')+zone.get('size')): coordinates[0] = zone.get('x') + zone.get('size') - X - 1
    if (y <= zone.get('y')): coordinates[1] = zone.get('y') + 1
    if (y + Y >= zone.get('y')+zone.get('size')): coordinates[1] = zone.get('y') + zone.get('size') - Y - 1
    return (coordinates[0],coordinates[1])

def zoneGetBorder(zone,card): #like getContain, but for borders. Snaps to the nearest border.
    x,y = card.position
    X,Y = card.width(),card.height()
    borders = [[(zone['x']),(zone['y'] + zone['size']/2)],
               [(zone['x'] + zone['size']/2),(zone['y'])],
               [(zone['x'] + zone['size']),(zone['y'] + zone['size']/2)],
               [(zone['x'] + zone['size']/2),(zone['y'] + zone['size'])]]
    c = [x+X/2,y+Y/2]
    border = borders[0]
    for b in list(borders):
        if (abs(b[0]-c[0]) + abs(b[1]-c[1])) < (abs(border[0]-c[0]) + abs(border[1]-c[1])): border = b
    return (border[0]-X/2,border[1]-Y/2)

def cardGetDistance(card1,card2):
    zone1 = getZoneContaining(card1)
    zone2 = getZoneContaining(card2)
    return zoneGetDistance(zone1,zone2)

def zoneGetDistance(zone1,zone2):
    return abs(zone1['i']-zone2['i']) + abs(zone1['j']-zone2['j'])

def getZoneContaining(card): #returns the zone occupied by the card. If attached, will return zone occupied by attachee.
    if not getGlobalVariable("Map"): return
    if getAttachTarget(card): return getZoneContaining(getAttachTarget(card))
    mapDict = eval(getGlobalVariable("Map"))
    x,X,y,Y = mapDict.get('x'),mapDict.get('X'),mapDict.get('y'),mapDict.get('Y')
    tileSize = mapDict.get('tileSize')
    zoneArray = mapDict.get('zoneArray')
    cx,cy = card.position
    cX,cY = (card.width(),card.height())
    if not (x<cx+cX/2<x+X and y<cy+cY/2<y+Y): return None
    i,j = int(float(cx+cX/2-x)/tileSize),int(float(cy+cY/2-y)/tileSize)
    if zoneArray[i][j]: return zoneArray[i][j]

def getZonesBordering(card): #returns list of zones bordered by card
    if not getGlobalVariable("Map"): return
    mapDict = eval(getGlobalVariable("Map"))
    zoneList = []
    for z in list(mapDict.get('zoneList',[])):
        if zoneBorders(z,card): zoneList.append(z)
    return zoneList

def getCardsInZone(zone): #returns a list of cards in the zone
    cardList = []
    for c in table:
        if getZoneContaining(c) == zone: cardList.append(c)
    return cardList

def snapToZone(card):
    zoneList = getZonesBordering(card)
    if zoneList:
            zone = zoneClosest(zoneList,card)
            if card.Target == 'Zone' or card.Type == 'Mage' or not card.isFaceUp: #snap to zone
                    snapX,snapY = zoneGetContain(zone,card)
                    card.moveToTable(snapX,snapY)
            elif card.type == 'Conjuration-Wall': #snap to zone border
                    snapX,snapY = zoneGetBorder(zone,card)
                    card.moveToTable(snapX,snapY)

