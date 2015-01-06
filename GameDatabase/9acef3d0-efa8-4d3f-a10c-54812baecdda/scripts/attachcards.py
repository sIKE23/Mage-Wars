############################################################################
##########################    v2.12.0.0    ##################################
############################################################################
############################
# Card Attachment and Alignment
############################

"""
This module contains the bulk of the attachment code.
Features:
- The attachments of each card are preserved in the order in which they were attached to that card.
- Removing a card from the table detaches everything that was attached to it.
- Two methods of attaching a card; explicitly, using targeting and alt+q, and by simply dragging one
card over the other (if autoAttach is enabled), using the moveToCard method in actions.py
- Detaching a card is as easy as dragging it away from the card to which it was attached

Bugs/Missing Features:
- Mass selecting a stack of cards and dragging it causes the cards to unattach and semi-randomly attach
to each other
- If a card leaves the table, the attachments are automatically sent to the middle of the board. Not a
problem in itself, but perhaps a better location could be found...
- Right now, the criteria for what may be attached to what are pretty loose. It will be easy to add
restrictions, however.
"""


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
    if card.controller == me and canAttach(card,target):
        detachAll(card)
        consolidateAttachments(target)
        setGlobalDictEntry("attachDict",card._id,[target._id,len(getAttachments(target))+1])
        remoteCall(target.controller,'alignAttachments',[target])
        return card,target
    return card,None

def detach(card):
    """Removes <card> from its target, then consolidates remaining cards on target."""
    mute()
    if isAttached(card) and card.controller == me:
        target = getGlobalDictEntry('attachDict',card._id)
        setGlobalDictEntry('attachDict',card._id,None)
        if target:
            target = Card(target[0])
            consolidateAttachments(target)
            remoteCall(target.controller,'alignAttachments',[target])
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
            Y = y-(count*side)*8
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

def isAttached(card):
    """Determines whether <card> is attached to anything."""
    mute()
    if getGlobalDictEntry('attachDict',card._id):
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
    return [Card(key) for key in attachList]

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

def detachAll(card):
    """Removes all attachments from <card>"""
    mute()
    attachments = getAttachments(card)
    for c in attachments:
        remoteCall(c.controller,'detach',[c])

def canAttach(card,target):
    """Determines whether <card> may be attached to <target>"""
    if (isAttached(target)
        or getAttachments(card)
        or card==target
        or not target in table):
        return False
    if (card.Type in ['Enchantment','Equipment']
        or target.Type in ['Magestats']
        or card.Name in ['Tanglevine','Stranglevine','Quicksand']
        or set(['Spellbind','Familiar','Spawnpoint']) & set(target.Traits.split(', '))):
        return True
    return False

def isAttachCardsEnabled():
    """Checks whether the attachCards module is turned on."""
    return getSetting("attachCards", "True")
