from random import random

"""
    A player has a set of champions he could recruit or buy and then control them through dangerous dungeons.
    Strategy and thinking ahead is necessary to stay alive and come up ahead from all the terrible fights ahead...
"""

# resistance formula should support negative numbers

# could cause unforseen bugs: # potential BUG #
# ctrl - f or ctrl - d to find them

# docstrings... spam them fuckers

# channeling, attacking, spell-casting are the actions champions could take in a certain round

def randomify(variable, rng_range, modifier=1) -> int:
    """ formula: variable + int(random() * rng_range) + modifier """
    return variable + int(random() * rng_range) + modifier




class Menu:
    pass


class Player:
    """
        This class represents the player, it holds player specific data like:
            - name
            - owned champions
            - inventory
            - dungeons progress
    """
    def __init__(self, name):
        self.name = name # name of the player
        self.owned_champions = [] # champions you bought/recruted
        self.lineUp = [] # 4 champion the player chose to take to the next fight
        self.inventory = {} # unused items
        self.dungeons_progress = {} # dungeons you finished and those you didn't, stores dungeon object
        self.gold = 1000 # reward from getting missions done, needed to buy champions and items

    def save_progress(self):
        """ After major events or when the user wants to quit, save progress """
        pass



class Battle:
    def __init__(self, entities):
        self.onGoing = True
        self.round = 1
        self.entities = entities # array of all entities (champions + enemies) in battle
        self.championTurnOrder = [] # array of entities' initiative
        self.turnToken = 0 # turn token is the index of the player who can take action


    def set_champions_order(self) -> list:
        """
        Turn is decided on SPEED, but there's an RNG element too:
            - INITIATIVE = SPEED + randomNumber(1,6)
        Champions and Monsters act based on their initiative, higher initiative means you get to act sooner.
        This function decides champions acting order.
        """
        
        for champion in self.champions:
            champion.initiative = randomify(champion.speed, 6)

        self.championTurnOrder = sorted(self.champions, key=lambda x: x.initiative)
        return self.championTurnOrder



class Shop:
    """
        Handles player interaction with the shop, buying and selling items
        Saves item stats and passives like with the Champion class
    """
    def __init__(self):
        pass



# champions have base stats (resistance, damage, hp, speed) and items (right hand, left hand, armor, boots) and passives
# future attributes: range, accuracy, movement, abilities, 
class Champion:
    def __init__(self, champion_class, baseStats, passive='', abilities={}):
        # generic stats
        self.champion_class = champion_class
        self.Base_hp, self.Base_damage, self.Base_resistance, self.Base_speed = baseStats # keep track of Base stats, don't change these
        self.hp, self.damage, self.resistance, self.speed = baseStats # battle buffs go here, they reset to base stats when the battle is over
        self.items = {
            'right-hand': '',
            'left-hand': '',
            'armor': '',
            'boots': '',
        }
        self.passive = passive
        self.abilities = abilities

        self.initiative = 0 
        
        # unusual stats
        self.critChance = 0
        self.critDamage = 1.25
        self.souls = 0
        self.shield = 0
        self.parry = False 

        # status
        self.bleeding = False # lose some HP (1) at round start
        self.stunned = False # unable to act
        self.enraged = False # attack your allies at round start
        self.invisible = False # untargetable, breaks when you take action
        self.roundsChanneling = 0 # how many rounds spent channeling

        # advanced stats
        self.roundsSinceLastKill = 100 # potential BUG #
        self.zombieState = False # a champion is officially dead when zombieState is False and HP is 0

    def attack(self, target, attack):
        pass

    def takeDamage(self, attacker, attack):
        pass

    @classmethod
    def create_champion(cls, champion_class):
        """
            Our factory function, deals with creating champions based on data it stores, mainly their base stats, passives and abilities
        """
        champion_classes = { 
            # high damage and low hp and resistances, strong on extended trades because of crits and bleeds
            # can extend trades by dodging crutial enemy abilities
            "samurai": { 
                "base-stats": (20, 10, 2, 7), # (hp, damage, resistance, speed)
                "passive": 'After ability usage, strike twice (second hit deals 0.25 damage)',
                "abilities": {
                    'primary': {
                        'description': 'if an enemy attempts to strike you, parry their attack and hit them for [1.0 THEIR Damage]',
                        'cooldown': 3,
                        },
                    'secondary': {
                        'description': 'Next 3 round you get [0.20 CRIT CHANCE] and your attacks cause enemies to BLEED',
                        'cooldown': 5,
                        }, 
                },
            },

            # high damage and resistances, regular hp
            # strikes slow but hard, gets very tanky with his abilities
            "knight": { 
                "base-stats": (30, 6, 8, 5), # (hp, damage, resistance, speed)
                "passive": 'reduce incoming damage by 0.10',
                "abilities": {
                    'primary': {
                        'description': 'Strikes with your shield, dealing [0.5 Damage] and stunning the target',
                        'cooldown': 3,
                        },
                    'secondary': {
                        'description': 'Reduce damage taken by [0.25 Damage] and your Damage by [0.50 Damage] next 2 ROUNDS',
                        'cooldown': 2,
                        }, 
                },
            },
            
            # very low base stats, assassin playstyle, hits hard fast to burst down his foes
            # his abilities allow him to inflict heavy damage and to hide
            "ninja": { 
                "base-stats": (10, 3, 8, 10), # (hp, damage, resistance, speed)
                "passive": 'Killing a target makes you INVISIBLE for the next 2 ROUNDS, your first strike after being HIDDEN deals [2.5 Damage]',
                "abilities": {
                    'primary': {
                        'description': 'Stab an enemy for [2.0 Damage] and cause them to BLEED',
                        'cooldown': 5,
                        },
                    'secondary': {
                        'description': 'become INVISIBLE, your next attack gets an additional bonus [0.25 Damage]',
                        'cooldown': 8,
                        }, 
                },
            },

            # high base stats, punishes his team for getting low, has tools to stay healthy and do damage
            # or in extreme cases to drop damage for sustain
            "werewolf": { 
                "base-stats": (25, 10, 0, 2), # (hp, damage, resistance, speed)
                "passive": 'Every attack restores [3 HP], getting below [10 HP] makes you ENRAGED and stronger [+5 Damage]',
                "abilities": {
                    'primary': {
                        'description': 'Bite an enemy for [1.3 Damage] and heal for half that amount',
                        'cooldown': 3,
                        },
                    'secondary': {
                        'description': 'STUN yourself for 2 rounds, heal [10 HP]',
                        'cooldown': 5,
                        }, 
                },
            },

            # moderate stats, provides a lot of utility and tankiness but no damage, staying alive last as gaoler is a sure loss
            # but through his powerful secondary he can make enemies focus him first  
            "gaoler": { 
                "base-stats": (20, 3, 5, 4), # (hp, damage, resistance, speed)
                "passive": 'reduce your target\'s resistance by 2 every time you attack',
                "abilities": {
                    'primary': {
                        'description': 'reduce ALL enemies speed by [3] and hit them for [0.5 Damage]',
                        'cooldown': 4,
                        },
                    'secondary': {
                        'description': "targets you've hit three times in a row can be CAGED, rendering them and gaoler unable to act, this effect ends if gaoler is dead or take action",
                        'cooldown': 2,
                        }, 
                },
            },

            # Scarecrow's secondary is very powerful, the copy can survive and cast on it's own, if the first Scarecrow dies, the second
            # can still live, attack, and create other clones, there are no limits for clones but the very high cooldown
            "scarecrow": { 
                "base-stats": (10, 8, 0, 10), # (hp, damage, resistance, speed)
                "passive": 'Not acting for 2 ROUNDS makes you INVISIBLE',
                "abilities": {
                    'primary': {
                        'description': 'Slash for [1.5 Damage] and cause your target to BLEED',
                        'cooldown': 2, 
                        },
                    'secondary': {
                        'description': 'summon an exact copy of me',
                        'cooldown': 10, # starts on cooldown
                        }, 
                },
            },

            # Healer can act both as a damage dealer and as a support healer (duh), her healing is bound to damage she deals though, and past
            # 10 SOULS she would either get a fat heal off, or let a teammate down for the huge damage boost
            "healer": { 
                "base-stats": (10, 6, 5, 5), # (hp, damage, resistance, speed)
                "passive": 'HP that enemies lose from your attacks is stored as SOULS, each soul adds [+1 Damage]',
                "abilities": {
                    'primary': {
                        'description': 'Deal [1.5 Damage] to a target, if you kill them gain their HP as souls',
                        'cooldown': 4, 
                        },
                    'secondary': {
                        'description': 'Depleate all your souls to heal an ally 1 HP for every 1 SOUL and remove ENRAGED and STUNNED debuffs',
                        'cooldown': 2,
                        }, 
                },
            }, 


            # gets tankier the longer the game goes, and is very hard to take down because of his passive
            # war-thirster is underwhelming if not used aggressively
            "war-thirster": { 
                "base-stats": (20, 2, 4, 2), # (hp, damage, resistance, speed)
                "passive": 'when you die, you have a window of 3 ROUNDS to kill an enemy and get [0.5 Max HP] back',
                "abilities": {
                    'primary': {
                        'description': 'Cleave an enemy for [1.0 Damage + 0.5 Missing HP]',
                        'cooldown': 6, 
                        },
                    'secondary': {
                        'description': 'ENRAGE, and gain [1.0 of Missing HP] as Damage',
                        'cooldown': 8,
                        }, 
                },
            },
            
            "berserk": { 
                "base-stats": (25, 8, 5, 7), # (hp, damage, resistance, speed)
                "passive": 'Your Damage is increased by [0.50 Max HP], your attacks heal for [0.50 Damage + 0.30 Missing HP]',
                "abilities": {
                    'primary': {
                        'description': 'hit an enemy and yourself for [0.80 Damage]',
                        'cooldown': 3, 
                        },
                    'secondary': {
                        'description': 'Stab yourself for [0.50 Damage], not stabbing yourself for 5 rounds makes you ENRAGED',
                        'cooldown': 0,
                        }, 
                },
            },


        }

        return cls(
            champion_class,
            champion_classes[champion_class]["base-stats"],
            passive = champion_classes[champion_class]['passive'],
            abilities = champion_classes[champion_class]['abilities'],
        )




    


        

