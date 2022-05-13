#######
#v3.0.0.0#
#######
# -*- coding: utf-8 -*-
import sys
sys.path.append(wd("lib"))
from math import factorial
from copy import deepcopy

'''
Attack
<card id="755727ff-55c8-417a-a376-958f1dbb8d99" name="Blinding Flash">
<property name="Nickname" value="Blinding Flash" />
<property name="Type" value="Attack" />
<property name="Subtype" value="Light" />
<property name="Cost" value="7" />
<property name="Action" value="Full" />
<property name="Range" value="0-0" />
<property name="cTargets" value="m0,M0))_Zone" />
<property name="Target" value="Zone" />
<property name="School" value="Holy" />
<property name="Level" value="2" />
<property name="Stats" value="" />
<property name="tAttacks" value="name=Blinding Flash;action type=Full;Cost=7;range type=Ranged;range=(0,0);Zone Attack=True;damage type=Light;dice=2;effects={10: ['Stun'], 4: ['Daze']};Ethereal=True;Unavoidable=True;+2 vs. Nonliving Creatures=True" />
<property name="AttackBar" value="[Ranged] [Zone Attack] [Light] [Dice=2] [d12] [4-9 = Daze; 10+ = Stun] [Ethereal] [Unavoidable] [+2 vs. Nonliving Creatures]" />
<property name="Traits" value="" />
<property name="Text" value="Attacks all objects in the zone except the caster." />
<property name="CardID" value="MW1A01" />
</card>

Conjuration
<card id="c202e960-7279-412a-b539-af007cc6d538" name="Rajan&apos;s Fury">
<property name="Nickname" value="Rajan&apos;s Fury" />
<property name="Type" value="Conjuration" />
<property name="Subtype" value="Totem" />
<property name="Cost" value="7" />
<property name="Action" value="Quick" />
<property name="Range" value="0-1" />
<property name="cTargets" value="m0,M1))_Zone" />
<property name="Target" value="Zone" />
<property name="School" value="Nature" />
<property name="Level" value="2" />
<property name="Stats" value="Armor=2, Life=7" />
<property name="StatArmor" value="2" />
<property name="StatLife" value="7" />
<property name="cAttacks" value="" />
<property name="AttackBar" value="" />
<property name="Traits" value="Zone Exclusive" />
<property name="Text" value="All animal creatures gain the Charge +1 trait." />
<property name="CardID" value="MW1J01" />
</card>

Creature
<card id="8963689f-6703-417d-aeda-64cbb9dab440" name="Asyran Cleric">
<property name="Nickname" value="Asyran Cleric" />
<property name="Type" value="Creature" />
<property name="Subtype" value="Cleric" />
<property name="Cost" value="5" />
<property name="Action" value="Full" />
<property name="Range" value="0-0" />
<property name="cTargets" value="m0,M0))_Zone" />
<property name="Target" value="Zone" />
<property name="School" value="Holy" />
<property name="Level" value="1" />
<property name="Stats" value="Armor=1, Life=6" />
<property name="StatArmor" value="1" />
<property name="StatLife" value="6" />
<property name="cAttacks" value="name=Staff;action type=Quick;range type=Melee;range=(0,0);dice=2||name=Healing Light;action type=Full;range type=Ranged;range=(0,1);Heal=True;dice=1;Heal target Living Creature the amount rolled.=True" />
<property name="AttackBar" value="Staff:&#xD;&#xA;[Quick] [Melee] [Dice=2]&#xD;&#xA;Healing Light:&#xD;&#xA;[Full] [Ranged:0-1] [Heal] [Dice=1] [Heal target Living Creature the amount rolled.]" />
<property name="Traits" value="" />
<property name="Text" value="" />
<property name="CardID" value="MW1C02" />
</card>

Enchantment
<card id="46b36e31-5dec-4a37-a39c-c2a5b6e0caee" name="Death Link">
<property name="Nickname" value="Death Link" />
<property name="Type" value="Enchantment" />
<property name="Subtype" value="Curse" />
<property name="Cost" value="2+6" />
<property name="Action" value="Quick" />
<property name="Range" value="0-2" />
<property name="cTargets" value="m0,M2))!SMage,tLiving,TCreature" />
<property name="Target" value="Non-Mage Living Creature" />
<property name="School" value="Dark" />
<property name="Level" value="2" />
<property name="Stats" value="" />
<property name="cAttacks" value="" />
<property name="AttackBar" value="" />
<property name="Traits" value="Magecast, Unique, Dark Mage Only" />
<property name="Text" value="Each Upkeep Phase, the controller of Death Link may heal up to 2 damage from his Mage and place it on this creature as direct damage, regardless of distance or LoS." />
<property name="CardID" value="MW1E08" />
</card>

Equipment
<card id="5d2f72e1-7aaf-4931-b0e0-f11cce928313" name="Lash of Hellfire">
<property name="Nickname" value="Lash of Hellfire" />
<property name="Type" value="Equipment" />
<property name="Subtype" value="" />
<property name="Cost" value="8" />
<property name="Action" value="Quick" />
<property name="Range" value="0-2" />
<property name="cTargets" value="m0,M2))SMage" />
<property name="Target" value="Mage" />
<property name="School" value="Dark+Fire" />
<property name="Level" value="1+1" />
<property name="Stats" value="Location=Weapon" />
<property name="StatEquipmentSlot" value="Weapon" />
<property name="tAttacks" value="name=Searing Thrash;action type=Quick;range type=Melee;range=(0,0);damage type=Flame;dice=4;effects={7: ['Burn'], 11: ['Burn', 'Burn']};Reach=True;Defrost=True" />
<property name="AttackBar" value="Searing Thrash:&#xD;&#xA;[Quick] [Melee] [Flame] [Dice=4] [d12] [7-10 = Burn; 11+ = 2 Burn] [Reach] [Defrost]" />
<property name="Traits" value="Warlock Only" />
<property name="Text" value="" />
<property name="CardID" value="MW1Q14" />
</card>

Incantation
<card id="2753eeea-2130-4399-ae88-f96ed1ccf776" name="Dispel">
<property name="Nickname" value="Dispel" />
<property name="Type" value="Incantation" />
<property name="Subtype" value="Metamagic" />
<property name="Cost" value="X" />
<property name="Action" value="Quick" />
<property name="Range" value="0-2" />
<property name="cTargets" value="m0,M2))TEnchantment" />
<property name="Target" value="Revealed Enchantment" />
<property name="School" value="Arcane" />
<property name="Level" value="1" />
<property name="Stats" value="" />
<property name="cAttacks" value="" />
<property name="AttackBar" value="" />
<property name="Traits" value="" />
<property name="Text" value="Destroy the target. X = total mana cost of target enchantment (casting plus reveal cost)." />
<property name="CardID" value="MW1I06" />
</card>
'''

class CardObject:
    def __init__(self, id, name, nickname, type, subtype, cost, actionType, range, target, school, level, traits, text):
        self.id = id                    #int
        self.name = name                #str
        self.nickname = nickname        #str
        self.type = type                #might just not need this and can declare in the child class as a class variable
        self.subtype = subtype          #str
        self.cost = cost                #int
        self.actionType = actionType    #str
        self.range = range              #list of ints
        self.target = target            #str
        self.school = school            #list of ints
        self.level = level              #list of ints
        self.traits = traits            #list of str
        self.text = text                #str


class AttackCardObject(CardObject):
    type = 'Attack'

    def __init__(self, rangeType, zoneAtt, casterFlag, damageType, dice, effects, bonus):
        self.rangeType = rangeType          #str
        self.zoneAtt = zoneAtt              #bool
        self.casterFlag = casterFlag        #bool, true if attack will affect caster
        self.damageType = damageType        #str
        self.dice = dice                    #int
        self.effects = effects              #list of strs
        self.bonus = bonus                  #dict

class ConjurationCardObject(CardObject):
    type = 'Conjuration'

    def __init__(self, armor, life, attackName, dice, effects):
        self.armor = armor
        self.life = life
        self.attackName = attackName                        #list of str
        self.dice = dice                                    #Might want to make attacks an object on their own, still tbd while I work this out
        self.effects = effects                              #Might want to make attacks an object on their own, still tbd while I work this out

class CreatureCardObject(CardObject):
    type = 'Creature'

    def __init__(self, armor, life, attackName, attackActionType, attackRange, attackRangeType, damageType, dice, effects, bonus):
        self.armor = armor                                  #int
        self.life = life                                    #int
        self.attackName = attackName                        #list of str
        self.attackActionType = attackActionType            #list of str
        self.attackRange = attackRange                      #list of str
        self.attackRangeType = attackRangeType              #list str
        self.damageType = damageType                        #list str
        self.dice = dice                                    #list int
        self.effects = effects                              #list of strs
        self.bonus = bonus                                  #list of dict


class EnchantmentCardObject(CardObject):
    type = 'Enchantment'

    def __init__(self, revealCost, bonus):
        self.revealCost = revealCost
        self.bonus = bonus

class EquipmentCardObject(CardObject):
    type = 'Equipment'

    def __init__(self, attackName, attackActionType, attackRange, attackRangeType, damageType, dice, effects, bonus):
        self.attackName = attackName                        #list of str
        self.attackActionType = attackActionType            #list of str
        self.attackRange = attackRange                      #list of str
        self.attackRangeType = attackRangeType              #list str
        self.damageType = damageType                        #list str
        self.dice = dice                                    #list int
        self.effects = effects                              #list of strs
        self.bonus = bonus                                  #list of dict - buffs/debuffs provided by card

class IncantationCardObject(CardObject):
    type = 'Incantation'

 