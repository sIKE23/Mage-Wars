'''
PSeudo example just to get something on here:
func my_first_test() {
  input = "ab";
  expected = "ba";
  actual = MyProgram.reverse(input);
  expect(actual).to equal(expected);
}

['Equals', 
'GetHashCode',
'GetType',
'MemberwiseClone',
'ReferenceEquals', 
'ToString', 
'__class__', 
'__cmp__', 
'__delattr__', 
'__dict__', 
'__doc__', 
'__format__', 
'__getattr__', 
'__getattribute__', 
'__hash__', 
'__init__', 
'__module__', 
'__new__', 
'__reduce__', 
'__reduce_ex__', 
'__repr__', 
'__setattr__', 
'__sizeof__', 
'__str__', 
'__subclasshook__', 
'__weakref__', 
'_id', 
'_markers', 
'_props', 
'alternate', 
'alternateProperty', 
'alternates', 
'anchor', 
'arrow', 
'controller', 
'delete', 
'filter', 
'group', 
'hasProperty', 
'height', 
'highlight', 
'index', 
'isFaceUp', 
'isInverted', 
'markers', 
'model', 
'moveTo', 
'moveToBottom', 
'moveToTable', 
'name', 
'offset', 
'orientation', 
'owner',
'peek', 
'peekers', 
'position', 
'properties', 
'resetProperties', 
'select', 
'sendToBack', 
'sendToFront', 
'set', 
'setId', 
'size', 
'target', 
'targetedBy', 
'width']

<property name="Type" type="String" hidden="False" ignoreText="False"/>
		<property name="Subtype" type="String" hidden="False" ignoreText="False"/>
		<property name="Cost" type="String" hidden="False" ignoreText="False"/>
		<property name="Action" type="String" hidden="False" ignoreText="False"/>
		<property name="Range" type="String" hidden="False" ignoreText="False"/>
		<property name="Target" type="String" hidden="False" ignoreText="False"/>
		<property name="School" type="String" hidden="False" ignoreText="False"/>
		<property name="Level" type="String" hidden="False" ignoreText="False"/>
		<property name="Stats" type="String" hidden="False" ignoreText="False"/>
		<property name="StatArmor" type="String" hidden="True" ignoreText="False"/>
		<property name="StatChanneling" type="String" hidden="True" ignoreText="False"/>
		<property name="StatDefense" type="String" hidden="True" ignoreText="False"/>
		<property name="StatEquipmentSlot" type="String" hidden="True" ignoreText="False"/>
		<property name="StatLife" type="String" hidden="True" ignoreText="False"/>
		<property name="StatSpellBookPoints" type="String" hidden="True" ignoreText="False"/>
		<property name="StatStartingMana" type="String" hidden="True" ignoreText="False"/>
		<property name="AttackBar" type="String" hidden="False" ignoreText="False"/>
		<property name="Traits" type="String" hidden="False" ignoreText="False"/>
		<property name="Text" type="String" hidden="False" ignoreText="False"/>
		<property name="CardID" type="String" hidden="False" ignoreText="False"/>
		<property name="MageTraining" type="String" hidden="False" ignoreText="False"/>
		<property name="MageSchoolCost" type="String" hidden="False" ignoreText="False"/>
		<property name="MageAbilities" type="String" hidden="False" ignoreText="False"/>
		<property name="Special" type="String" hidden="True" ignoreText="False"/>
		<property name="Special1" type="String" hidden="True" ignoreText="False"/>
		<property name="Special2" type="String" hidden="True" ignoreText="False"/>
		<property name="Special3" type="String" hidden="True" ignoreText="False"/>
		<!--Convenient name and pronoun Properties-->
		<property name="Nickname" type="String" hidden="True" ignoreText="False"/>
		<property name="PSub" type="String" hidden="True" ignoreText="False"/>
		<property name="PObj" type="String" hidden="True" ignoreText="False"/>
		<property name="PPos" type="String" hidden="True" ignoreText="False"/>
		<property name="PRef" type="String" hidden="True" ignoreText="False"/>
		<!--translations of properties into code versions-->
		<property name="cTargets" type="String" hidden="True" ignoreText="False" />
		<property name="cBuffs" type="String" hidden="True" ignoreText="False" />
		<property name="cAttacks" type="String" hidden="True" ignoreText="False" />
		<property name="tAttacks" type="String" hidden="True" ignoreText="False" />
'''
class Beastmaster :
    Name="Beastmaster"
    Type="Creature",
    Subtype="Mage",
    Level="6",
    Stats="Spellbook=120, Life=36, Armor=0, Channeling=9",
    cAttacks="name=Basic Melee Attack;action type=Quick;range type=Melee;range=(0,0);dice=3",
    cBuffs="m0,M0))@self,[Melee +1]",
    StatArmor='0',
    StatChanneling='9',
    StatLife='36',


class Hellion :
    Name="Flaming Hellion",
    Type="Creature",
    Subtype="Demon",
    Level="3",
    Cost='13',
    School='Dark',
    Stats="Armor=2, Life=9",
    cAttacks="name=Flameblast;action type=Full;range type=Ranged;range=(1,1);damage type=Flame;dice=3;effects={10: ['Burn', 'Burn'], 5: ['Burn']};Defrost=True||name=Hell Trident;action type=Quick;range type=Melee;range=(0,0);damage type=Flame;dice=4;effects={7: ['Burn'], 11: ['Burn', 'Burn']};Defrost=True",
    Traits="Flame Immunity",
    StatArmor='2',
    StatLife='9',





def testAttackSequence(source, target):
    '''
    
    Objects: Source, Target
    '''
    print (source.Name)

source = Beastmaster
target = Hellion
testAttackSequence(source)