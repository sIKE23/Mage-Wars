###########################################################################
##########################    v1.12.5.0     #######################################
###########################################################################

############################################################################
############################	   Map Construction      ################################
############################################################################

def importArray(filename):
        """Takes a txt character array and outputs a dictionary of arrays (sets of columns). To get an entry from an array, use array[x][y]"""
        #Open the file
        directory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('maps')
        try: raw = open('{}\{}{}'.format(directory,filename,'.txt'),'r')
        except: return #Bad practice, I know. I'll try to find a better way later.
        #Create an empty array.
        #Because of the order in which data are read, we will need to transpose it.
        transposeArray = []
        #Fill up the transposed array, as a set of rows.
        scenarioDict = {}
        dictKey = None
        for line in raw:
                if line == '\n': pass #ignore blank lines
                elif line[0] != '#':
                        row = []
                        for char in range(len(line)):
                            if line[char] != '\n':
                                row.append(line[char])
                        transposeArray.append(row)
                else:
                        dictKey = line.replace('\n','').strip('#')
                        X0 = len(transposeArray[0])
                        X1 = len(transposeArray)
                        array = [[transposeArray[x1][x0] for x1 in range(X1)] for x0 in range(X0)]
                        transposeArray = []
                        scenarioDict[dictKey] = array
        return scenarioDict

def loadMapFile(group, x=0, y=0):
        mute()
        notify("This feature coming to your Mage Wars game here soon!")
        return
        directory = os.path.split(os.path.dirname(__file__))[0]+'\{}'.format('maps')
        fileList = [f.split('.')[0] for f in os.listdir(directory) if (os.path.isfile(os.path.join(directory,f)) and f.split('.')[1]=='txt')]
        choices = fileList+['Cancel']
        colors = ['#6600CC' for f in fileList] + ['#FF0000']
        choice = askChoice('Load which map?',choices,colors)
        if choice == 0 or choice == len(choices): return
        scenario = importArray(fileList[choice-1])
        notify('{} loads {}.'.format(me,fileList[choice-1]))

        mapArray = scenario.get('Map',False)
        objectsArray = scenario.get('Objects',False)
        creaturesArray= scenario.get('Creatures',False)

        for c in table:
                if c.type == "Internal": c.delete()# or
                   # card.name in ["Sslak, Orb Guardian","Usslak, Greater Orb Guardian"]): card.delete() #We need a way to distinguish between scenario guardians and those in spellbooks
	setNoGameBoard(table)

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
                                        if SPT: table.create("a4b3bb92-b597-441e-b2eb-d18ef6b8cc77",x+mapTileSize/2,y+mapTileSize/2) #Add trap marker
                        y += mapTileSize
                x += mapTileSize
                y = -Y/2
        x = -X/2

        mapDict = createMap(I,J,zoneArray,mapTileSize)

        for i in range(I): #For some reason, I can't get the map tiles to be sent to the back successfully. So we'll do this in two parts.
                for j in range(J):
                        if objectsArray:
                                obj = mapObjectsDict.get(objectsArray[i][j],None)
                                if obj:
                                        duplicate = objectsArray[i][j].istitle()
                                        table.create(obj,
                                                     x+mapObjectOffset,
                                                     y+mapObjectOffset)
                                        if duplicate:
                                                table.create(obj,
                                                                   x+mapObjectOffset+mapMultipleObjectOffset,
                                                                   y+mapObjectOffset)
                        if creaturesArray:
                                if creaturesArray[i][j] in ['1','2','3','4','5','6']: mapDict.get('zoneArray')[i][j]['startLocation'] = creaturesArray[i][j]
                                cre = mapCreaturesDict.get(creaturesArray[i][j],None)
                                if cre:
                                        duplicate = creaturesArray[i][j].istitle()
                                        table.create(cre,
                                                     x+mapCreatureOffset,
                                                     y+mapCreatureOffset)
                                        if duplicate: table.create(cre,
                                                                   x+mapCreatureOffset+mapMultipleCreatureOffset,
                                                                   y+mapCreatureOffset)
                        y += mapTileSize
                x += mapTileSize
                y = -Y/2

        setGlobalVariable("Map",str(mapDict))
        for c in table:
                remoteCall(c.controller,'moveCardToDefaultLocation',[c,True])

### Map Definitions ###

mapTileSize = 250
mapObjectOffset = 175
mapMultipleObjectOffset = -100
mapCreatureOffset = 0
mapMultipleCreatureOffset = 62


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
                "Orb" : "3d339a9d-8804-4afa-9bd5-1cabb1bebc9f",
                "Sslak" : "bf217fd3-18c0-4b61-a33a-117167533f3d", 
                "Usslak" : "54e67290-5e6a-4d8a-8bf0-bbb8fddf7ddd",
                "SecretPassage" : "a4b3bb92-b597-441e-b2eb-d18ef6b8cc77"}
