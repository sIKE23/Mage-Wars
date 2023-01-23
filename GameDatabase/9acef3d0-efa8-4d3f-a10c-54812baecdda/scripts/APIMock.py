from bs4 import BeautifulSoup

def openAndParseFileForKey(filepath, findAllKey):
    xmlFile = open(filepath, 'r')
    parsedXmlFile = BeautifulSoup(xmlFile, 'xml')
    allCardsFromFile = parsedXmlFile.find_all(findAllKey)
    return allCardsFromFile

class Card:
    def __init__(self, name):
        self.Name = name
        allCardProperties = openAndParseFileForKey('definition.xml', 'property')
        for i in range(len(allCardProperties)):
            prop = str(allCardProperties[i].attrs['name'])
            setattr(self, prop, '')

def assignCorrectPropertiesToCard(cardData):
    cardProperties = cardData.find_all('property')
    card = Card(str(cardData['name']))
    for property in cardProperties:
        setattr(card, str(property.attrs['name']), str(property.attrs['value']))
    return card

def addMageAndStatsCard(mageName):
    allMageCards = openAndParseFileForKey("Sets/d9d7e352-5bae-4dd2-8354-8132d9603fdd/set.xml", 'card')
    mage = ''
    mageStats = ''
    for i in range(len(allMageCards)):
        if allMageCards[i]['name'] == mageName:
            mage = assignCorrectPropertiesToCard(allMageCards[i])
        elif allMageCards[i]['name'] == mageName + " Stats":
            mageStats = assignCorrectPropertiesToCard(allMageCards[i])
    return mage, mageStats

def createDeckFromXMLFile(mageName):
    deck = []
    deck.extend(addMageAndStatsCard(mageName))
    cardsInDeck = openAndParseFileForKey("testset.xml", 'card')
    for i in range(len(cardsInDeck)):
        currentCard = assignCorrectPropertiesToCard(cardsInDeck[i])
        deck.append(currentCard)
    return deck


def mute():
    return

def debug(arg):
    return

def notify(arg):
	return

me = "Sharkbait"





