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
                "passive": 'Every third attack makes the target BLEED',
                "abilities": {
                    'primary': {
                        'description': 'if an enemy attempts to strike you, parry their attack and hit them for [1.0 THEIR Damage]',
                        'cooldown': 5,
                        },
                    'secondary': {
                        'description': 'hit the enemy twice for [1.25 Damage] per hit, you drop 1 Speed',
                        'cooldown': 4,
                        }, 
                },
            },

            # high damage and resistances, regular hp
            # strikes slow but hard, gets very tanky with his abilities
            "knight": { 
                "base-stats": (30, 6, 3, 3), # (hp, damage, resistance, speed)
                "passive": 'reduce incoming damage by [0.10 Damage Received]',
                "abilities": {
                    'primary': {
                        'description': 'Strikes with your shield, dealing [1 Damage] and stunning the target',
                        'cooldown': 5,
                        },
                    'secondary': {
                        'description': 'Reduce damage taken by [0.25 Damage] and your Damage by [0.50 Damage] next 2 ROUNDS',
                        'cooldown': 3,
                        }, 
                },
            },
            
            # very low base stats, assassin playstyle, hits hard fast to burst down his foes
            # his abilities allow him to inflict heavy damage and to hide
            # low speed is benificial to let teammates hit target first
            # low base damage so players itemize heavily in damage instead of tankiness
            "ninja": { 
                "base-stats": (15, 2, 5, 1), # (hp, damage, resistance, speed)
                "passive": 'Killing a target makes you INVISIBLE for the next 2 ROUNDS, striking while HIDDEN deals [2.5 Damage] and reveals you',
                "abilities": {
                    'primary': {
                        'description': 'After [3] turns, Stab an enemy for [2.0 Damage] and cause them to BLEED',
                        'cooldown': 3, # cooldown starts on cast
                        },
                    'secondary': {
                        'description': 'After [2] turns, become INVISIBLE',
                        'cooldown': 6,
                        }, 
                },
            },

            # high base stats, punishes his team for getting low, has tools to stay healthy and do damage
            # or in extreme cases to drop damage for sustain
            "werewolf": { 
                "base-stats": (25, 10, 0, 2), # (hp, damage, resistance, speed)
                "passive": 'Every attack restores [0.25 damage] HP, getting below [0.25 MAX HP] makes you ENRAGED and stronger [+0.5 Damage]',
                "abilities": {
                    'primary': {
                        'description': 'Bite an enemy for [0.5 Damage] and heal for that amount',
                        'cooldown': 3,
                        },
                    'secondary': {
                        'description': 'Trade 1 HP for 1 Damage',
                        'cooldown': 1,
                        }, 
                },
            },

            # moderate stats, provides a lot of utility and tankiness but no damage, staying alive last as gaoler is a sure loss
            # but through his powerful secondary he can make enemies focus him first  
            "gaoler": { 
                "base-stats": (20, 3, 5, 8), # (hp, damage, resistance, speed)
                "passive": 'reduce your target\'s resistance by 1 every time you attack',
                "abilities": {
                    'primary': {
                        'description': 'reduce ALL enemies Speed by [3] and hit them for [1 Damage]',
                        'cooldown': 4,
                        },
                    'secondary': {
                        'description': "targets you've hit three times in a row can be CAGED, rendering them and GAOLER unable to act. This effect ends after [3] turns or if gaoler takes action",
                        'cooldown': 2,
                        }, 
                },
            },

            # Scarecrow's secondary is very powerful, the copy can survive and cast on it's own, if the first Scarecrow dies, the second
            # can still live, attack, and create other clones, there are no limits for clones but the very high cooldown
            "scarecrow": { 
                "base-stats": (10, 5, 0, 10), # (hp, damage, resistance, speed)
                "passive": 'Not acting for 2 ROUNDS makes you INVISIBLE',
                "abilities": {
                    'primary': {
                        'description': 'Slash for [2 Damage] and cause your target to BLEED',
                        'cooldown': 3, 
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
                "base-stats": (10, 1, 2, 5), # (hp, damage, resistance, speed)
                "passive": 'HP that enemies lose from your attacks is stored as SOULS, each soul adds [+1 Damage] and restore [0.5] HP',
                "abilities": {
                    'primary': {
                        'description': 'Deal [0.2 Damage] to a target, if you kill them gain [1.0 Enemy Max HP] as souls',
                        'cooldown': 5, 
                        },
                    'secondary': {
                        'description': 'Depleate all your souls to heal an ally 1 HP for every 1 SOUL, if more than [10] souls were used CLEANSE ENRAGED and STUNNED from target',
                        'cooldown': 1,
                        }, 
                },
            }, 


            # gets tankier the longer the game goes, and is very hard to take down because of his passive
            # war-thirster is underwhelming if not used aggressively
            "war-thirster": { 
                "base-stats": (30, 2, 4, 2), # (hp, damage, resistance, speed)
                "passive": 'when you die, you have a window of 3 ROUNDS to kill an enemy and get [0.5 Max HP] back',
                "abilities": {
                    'primary': {
                        'description': 'Lose [0.1 HP] And Cleave an enemy for [0.5 Damage + 0.5 Missing HP]',
                        'cooldown': 2, 
                        },
                    'secondary': {
                        'description': 'ENRAGED for [2] turns, and gain [1.0 of Missing HP] as Damage [for the duration]', # could be permanent increase
                        'cooldown': 4,
                        }, 
                },
            },
            
            # Low damage and Big HP pool. All about risk taking and playing on the edge to get devastating damage
            "sadist": { 
                "base-stats": (25, 5, 5, 7), # (hp, damage, resistance, speed)
                "passive": 'Receiving damage grants [+1 Damage] (Max +4 Damage/turn), [-1 Damage]/turn',
                "abilities": {
                    'primary': {
                        'description': 'Hit an enemy for [2.5 Damage] and take [0.25] of that damage',
                        'cooldown': 3, 
                        },
                    'secondary': {
                        'description': 'hit yourself [3] times, heal [1.0 Max HP] after [1] turn',
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




    


        

