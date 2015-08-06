###########################################################################
##########################    v1.12.5.0     #######################################
###########################################################################

############################################################################
############################	   Map Construction      ################################
############################################################################

def checkDominationVictory():
        goal = eval(getGlobalVariable("Goal")).get("Goal")
        victoriousPlayers = []
        for player in players:
                mage = [c for c in table if c.type=="Mage" and c.controller == player][0]
                vtar = mage.markers[VTar]
                if vtar >= goal: victoriousPlayers.append([player,vtar])
        soleWinner = None
        for player in victoriousPlayers:
                for other in list(victoriousPlayers):
                        if other[1] >= player[1] and other!=player: break
                        soleWinner = player
        if soleWinner:
                setGlobalVariable("GameIsOver", True)
                notify("{} wins with {} V'tar!".format(soleWinner[0],soleWinner[1]))
                [remoteCall(p,"reportVTarWin",[soleWinner[0],soleWinner[1]]) for p in players]
                return True

def updateVtarScore():
    if [1 for c in table if c.name=="Dampening Field" and c.isFaceUp]:
        notify("The dampening field suppresses all V'tar generation!")
        return True
    for player in players:
        mage = [c for c in table if c.type=="Mage" and c.controller == player][0]
        controlMarkerColor = playerColorDict[int(mage.controller.getGlobalVariable("MyColor"))]["ControlMarker"]
        vtarGain = len([1 for c in table if  ("V'Tar Orb" in c.name and c.markers[controlMarkerColor]) or (c.name == "Galaxxus" and c.controller == mage.controller)])
        if vtarGain:
            mage.markers[VTar] += vtarGain
            notify("{} gains {} V'tar!".format(mage.controller,str(vtarGain)))
    return True #This doesn't actually matter, except that we need it so that our if statement in nextPhase() evaluates to true.

def DominationTracker():
        mute()
        #need dynamic proxy card generation for this to work....
        card = table.create("a25a6dd5-04a8-490f-b5e6-834ffac8d018",-591,-5)
        card.Special1 = str(eval(getGlobalVariable("Map")).get("Map Name"))
        card.Special2 = str(eval(getGlobalVariable("Goal")).get("Goal"))

def readMap(filename):
        """Interprets a properly formatted .txt map file and returns a dictionary with the relevant scenario information."""
        #Open the file
        directory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('maps')
        try: raw = open('{}\{}{}'.format(directory,filename,'.txt'),'r')
        except: return
        #Create an empty array. Because of the order in which data are read, we will need to transpose it.
        transposeArray = []
        #Fill up the transposed array, as a set of rows.
        scenarioDict = {}
        dictKey = None
        for line in raw:
                if line == '\n': pass #ignore blank lines
                elif "@Scenario" in line:
                        raw = line.replace('\n','').strip('@')
                        split = raw.split("=")[1].strip("[]").split(",")
                        scenarioDict["Scenario"] = {"Type":split[0],"Goal":int(split[1])}
                elif "@" in line:
                        raw = line.replace('\n','').strip('@')
                        split = raw.split("=")
                        key = split[0]
                        locations = eval(split[1])
                        scenarioDict[key] = locations
                elif line[0] != '#':
                        row = []
                        for char in range(len(line.replace('\n',''))):
                            if line[char] != '\n':
                                row.append(line[char])
                        transposeArray.append(row)
                else:
                        dictKey = line.replace('\n','').strip('#')
                        X0 = len(transposeArray[0])
                        X1 = len(transposeArray)
                        array = [[transposeArray[x1][x0] for x1 in range(X1)] for x0 in range(X0)]
                        #transposeArray = []
                        scenarioDict[dictKey] = array
        return scenarioDict

def loadMapFile(group, x=0, y=0):
        mute()
        directory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('maps')
        fileList = [f.split('.')[0] for f in os.listdir(directory) if (os.path.isfile(os.path.join(directory,f)) and f.split('.')[1]=='txt')]
        choices = fileList+['Cancel']
        colors = ['#6600CC' for f in fileList] + ['#FF0000']
        choice = askChoice('Load which map?',choices,colors)
        if choice == 0 or choice == len(choices): return
        choiceName = choices[choice-1]
        scenario = readMap(fileList[choice-1])
        notify('{} loads {}.'.format(me,fileList[choice-1]))

        if scenario.get("Scenario"): setGlobalVariable("Goal",str(scenario["Scenario"]))

        mapArray = scenario.get('Map',False)
        mapTileSize = 250 #replace 250 with a stored tilesize from scenario if we later decide to allow the design of maps with non-standard tilesizes.
        mapObjects = [(k,scenario.get(k,[])) for k in mapObjectsDict]
        startZones = scenario.get("startZoneDict",{}) #should probably include a default placement dictionary.
        jRDA,iRDA = scenario.get("RDA",(2,2))

        for c in table:
                if (c.type == "Internal" or "Scenario" in c.special) and c.controller == me:
                        c.delete() # delete Scenario creatures and other game markers
                elif (c.type == "Internal" or "Scenario" in c.special)  and c.controller != me:
                        remoteCall(c.controller,'remoteDeleteCard', [c])

        #iterate over elements, top to bottom then left to right.
        I,J = len(mapArray),len(mapArray[0])
        X,Y = I*mapTileSize,J*mapTileSize
        x,y = (-X/2,-Y/2) #Do we want 0,0 to be the center, or the upper corner? Currently set as center.

        zoneArray = mapArray

        for i in range(I):
                for j in range(J): #Might as well add support for non-rectangular maps now. Though this won't help with the rows.
                        if mapArray:
                                tile = mapTileDict.get(mapArray[i][j],None)
                                SPT = (True if tile == "c3e970f7-1eeb-432b-ac3f-7dbcd4f45492" else False) #Spiked Pit Trap
                                zoneArray[i][j] = (1 if tile else 0)
                                if tile:
                                        tile = table.create(tile,x,y)
                                        tile.anchor = True
                                        if SPT: table.create("fc31f61b-2af8-41f7-8474-bb9be0f32926",x+mapTileSize/2 - 28,y+mapTileSize/2 - 40) #Add trap marker
                        y += mapTileSize
                x += mapTileSize
                y = -Y/2
        x = -X/2

        mapDict = createMap(I,J,zoneArray,mapTileSize)

        mapDict["Map Name"] = choiceName
        mapDict["RDA"] = iRDA,jRDA
        
        for z in startZones:
                playerNumber = z["Player"]
                zx,zy = eval(z["Zone"])
                mapDict['zoneArray'][zy-1][zx-1]['startLocation'] = str(playerNumber)

        setGlobalVariable("Map",str(mapDict))

        for c in table:
                if c.type in ['DiceRoll','Phase']: moveRDA(c)

        for obj,locations in mapObjects:
                for L in locations:
                        j,i = L
                        mapPlace(obj,(i-1,j-1))

        setNoGameBoard(table)
        for p in players:
        	remoteCall(p,"DominationMatchStart",[]) 
        
def DominationMatchStart():
        mute()
        mapText = ""
        map = str(eval(getGlobalVariable("Map")).get("Map Name"))
        goal = str(eval(getGlobalVariable("Goal")).get("Goal"))
        mapText = getMapText(map)
        choiceList = ['OK']
        colorList = ['#de2827']
        whisper("{}!\n\nYou will need {} V'Tar to secure the V'Torrak and Dominate the arena! Good Luck!".format(mapText,goal))
        choice = askChoice("{}!\n\nYou will need {} V'Tar to secure the V'Torrak and Dominate the arena! Good Luck!".format(mapText,goal), choiceList, colorList)
        if choice == 0 or choice == 1:
                return

def mapPlace(key,coords):
        mapDict = eval(getGlobalVariable("Map"))
        mapTileSize = mapDict['tileSize']
        i,j = coords
        x,y = i*mapTileSize+mapDict["x"],j*mapTileSize+mapDict["y"]
        GUID = mapObjectsDict[key]["GUID"]
        offset = mapObjectsDict[key]["Offset"]
        dVector = mapObjectsDict[key]["Splay Vector"]
        x += offset
        y += offset

        x,y = splay(x,y,dVector)
        card = table.create(GUID,x,y)

        if card.type == "Creature":
                card.special = "Scenario"
                if "Orb Guardian" in card.name:
                        toggleGuard(card)
        elif card.type == "Conjuration":
                card.special = "Scenario"

### Map Definitions ###

mapTileDict = {
        "1" : "5fbc16dd-f861-42c2-ad0f-3f8aaf0ccb64", #V'Torrak
        "2" : "6136ff26-d2d9-44d2-b972-1e26214675b5", #Corrosive Pool
        "3" : "8972d2d1-348c-4c4b-8c9d-a1d235fe482e", #Altar of Oblivion
        "4" : "a47fa32e-ac83-4ced-8f6a-23906ee38880", #Septagram
        "5" : "bf833552-8ee4-4c62-abd2-83da233da4ce", #Molten Rock
        "6" : "c3e970f7-1eeb-432b-ac3f-7dbcd4f45492", #Spiked Pit
        "7" : "edca7d45-53e0-468d-83a5-7a446c81f070", #Samandriel's Circle
        "8" : "f8d70e09-2734-4de8-8351-66fa98ae0171", #Ethereal Mist
        "." : "4f1b033d-7923-4e0e-8c3d-b92ae19fbad1"} #Generic Tile

mapObjectsDict = {
        "Orb" : {"GUID":"fd339a9d-8804-4afa-9bd5-1cabb1bebc9f", "Offset":175, "Splay Vector": (-1,0)},
        "Sslak" : {"GUID":"865954e9-4c67-4858-b3e0-484c66e19db9", "Offset":5, "Splay Vector": (1,0)},
        "Usslak" : {"GUID":"5688957a-e243-4999-8301-b869be3f6fdb", "Offset":5, "Splay Vector": (1,0)},
        "SecretPassage" : {"GUID":"fb43bb92-b597-441e-b2eb-d18ef6b8cc77", "Offset":175, "Splay Vector": (-1,0)}
        }
