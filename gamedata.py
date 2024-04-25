import os
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 0, 255)
SCROLL = (236,212,156)

class SpriteSheet():
    def __init__(self, image):
        self.sheet = pygame.image.load(image).convert_alpha()

    def get_image(self, frame_x, frame_y, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill(colour)
        image.blit(self.sheet, (0, 0), ((frame_x * width), (frame_y * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image
    
    def get_image_list(self, width, height, rows, columns, remove_empty, scale, colour):
        image_list = []
        for r in range(rows):
            for c in range(columns):
                image = pygame.Surface((width, height)).convert_alpha()
                image.fill(colour)
                image.blit(self.sheet, (0, 0), ((c * width), (r * height), width, height))
                image = pygame.transform.scale(image, (width * scale, height * scale))
                image.set_colorkey(colour)
                image_list.append(image)
        image_list = image_list[:-remove_empty or None]
        return image_list




round_explosions_sprite_sheet = SpriteSheet(r"./Assets/Sprites/wills_pixel_explosions_sample/round_vortex/spritesheet/spritesheet.png")
round_explosions_sprite_list = round_explosions_sprite_sheet.get_image_list(100,100,9,10,9,6,BLACK)


ANIMATION_DICT = {
    "round_explosion" : round_explosions_sprite_list
}






icon_sprite_sheet = SpriteSheet(r"Assets/Sprites/Shikashi's Fantasy Icons Pack v2/BG 6.png")

icon_sprite_sheet_transparent = SpriteSheet(r"Assets/Sprites/Shikashi's Fantasy Icons Pack v2/#1 - Transparent Icons.png")

lyre_display = SpriteSheet(r"./Assets/CharImages/lyre_desc.png")
marcee_display = SpriteSheet(r"./Assets/CharImages/marcee_desc.png")
maurlo_display = SpriteSheet(r"./Assets/CharImages/maurlo_desc.png")
nailea_display = SpriteSheet(r"./Assets/CharImages/nailea_desc.png")
pynncone_display = SpriteSheet(r"./Assets/CharImages/pynncone_desc.png")
varick_display = SpriteSheet(r"./Assets/CharImages/varick_desc.png")
yayan_display = SpriteSheet(r"./Assets/CharImages/yayan_desc.png")

CHARDATA = (
    {"Lyre_image": lyre_display.get_image(0,0,407,836,0.38,SCROLL),
     "Lyre_summary":("A gullible changeling who is horrible at directions.",
                              "She indulges in an adventurer's lifestyle to outgrow her past.",
                              "An agile arcane rogue with a preference for bard magic.",
                              "Prefers to negotiate and manipulate rather than fight head on.",
                              ),
     "Lyre_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(5,0,32,32,1,BLACK),
         ("ability1","name"):"Dancing Lights",
         ("ability1","description"):"You reminisce on times past. Gain advantage against frightened effect.",
         ("ability2","icon"): icon_sprite_sheet.get_image(8,13,32,32,1,BLACK),
         ("ability2","name"):"Historian",
         ("ability2","description"):"You know a bit about everything. Status effects 50% less effective.",
         ("ability3","icon"): icon_sprite_sheet.get_image(5,16,32,32,1,BLACK),
         ("ability3","name"): "Mimir",
         ("ability3","description"):"Mimir knows the way. Know the next environment 2 turns ahead.",
         }},
    {"Marcee De la Mer_image": marcee_display.get_image(0,0,403,883,0.37,SCROLL),
     "Marcee De la Mer_summary":("Captain of the Ixen Kothar pirate crew. A flirty swashbuckling tiefling.",
                                 "One of the youngest to have sailed across Toril's equator.",
                                 "She never goes anywhere without at least 8 bladed weapons.",
                                 "Specializes in close combat and is not afraid to fight dirty."
                                 ),
     "Marcee De la Mer_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(3,1,32,32,1,BLACK),
         ("ability1","name"):"70 IQ",
         ("ability1","description"):"Words dont hurt if you dont understand them. Is immune to intimidation.",
         ("ability2","icon"): icon_sprite_sheet.get_image(8,11,32,32,1,BLACK),
         ("ability2","name"):"Captain's Command",
         ("ability2","description"):"Never far away from the crew. Cannons fire randomly each turn.",
         ("ability3","icon"): icon_sprite_sheet.get_image(6,0,32,32,1,BLACK),
         ("ability3","name"):"Lilon",
         ("ability3","description"):"For that extra cheerleader effect. Gain advantage on charisma.",
         }},
    {"Maurlo 'Maurlomallow' Liebermann_image": maurlo_display.get_image(0,0,407,836,0.4,SCROLL),
     "Maurlo 'Maurlomallow' Liebermann_summary":("An Inventive little rabbitfolk girl with a penchant for alchemy.",
                                                 "The shadow of a criminal syndicate looms over her as",
                                                 "she experiments on herself. Many utility options and effects.",
                                                 "She is never without her alchemical servants."
                                                 ),
     "Maurlo 'Maurlomallow' Liebermann_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(6,12,32,32,1,BLACK),
         ("ability1","name"):"Bag of Holding",
         ("ability1","description"):"Always carries something useful. Get 1 random consumable item per turn.",
         ("ability2","icon"): icon_sprite_sheet.get_image(10,15,32,32,1,BLACK),
         ("ability2","name"):"Substance Abuser",
         ("ability2","description"):"You've built a tolerance to toxins. Gain resistance against poison damage.",
         ("ability3","icon"): icon_sprite_sheet.get_image(14,3,32,32,1,BLACK),
         ("ability3","name"):"Trip-induced Third Eye",
         ("ability3","description"):"Adventure is a helluva drug. Can see invisible creatures and objects.",
         }},
    {"Nailea Arorangiurohanga_image": nailea_display.get_image(0,0,428,1070,0.33,SCROLL),
     "Nailea Arorangiurohanga_summary":("Born from a dream and destined to travel the stars.",
                                        "A Firbold druid with too many crimes against civilization to adequately",
                                        "quantify. Wields a dark sword inhabited by the highest of Quori.",
                                        "Fights unpredictably, capable of being very effective or not at all."),
     "Nailea Arorangiurohanga_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(4,0,32,32,1,BLACK),
         ("ability1","name"):"Backstory Trauma",
         ("ability1","description"):"Your nightmares feed your sword. Gain +4 damage every trauma trigger.",
         ("ability2","icon"): icon_sprite_sheet.get_image(7,10,32,32,1,BLACK),
         ("ability2","name"):"Cosmic Traveler",
         ("ability2","description"):"You are used to cosmic radiation. Gain resistance against radiant damage.",
         ("ability3","icon"): icon_sprite_sheet.get_image(10,19,32,32,1,BLACK),
         ("ability3","name"):"Neighlea",
         ("ability3","description"):"Why not? Chance to randomly turn into a horse per turn",
         }},
    {"Pynncone Amanita_image": pynncone_display.get_image(0,0,546,776,0.38,SCROLL),
     "Pynncone Amanita_summary":("An aspiring courier from Lustria Academy, with a druidic vow towards",
                                 "all things that rot and decay. A powerful mushroom-based caster.",
                                 "She travels to unravel the mysteries of her past crimes.",
                                 "Adept with powerful debuff effects and prefers smaller wildshapes."),
     "Pynncone Amanita_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(0,12,32,32,1,BLACK),
         ("ability1","name"):"Scholar of Rot",
         ("ability1","description"):"Studying mushrooms has its perks. Resistant to necrotic damage.",
         ("ability2","icon"): icon_sprite_sheet.get_image(9,13,32,32,1,BLACK),
         ("ability2","name"):"Courier at Heart",
         ("ability2","description"):"Receive letters of encouragement per turn. Letters provide +2 HP",
         ("ability3","icon"): icon_sprite_sheet.get_image(15,12,32,32,1,BLACK),
         ("ability3","name"):"Kai's Memory",
         ("ability3","description"):"Is this really a dream? Random chance that Kai takes damage for you.",
         }},
    {"Varick Ehre_image": varick_display.get_image(0,0,414,891,0.38,SCROLL),
     "Varick Ehre_summary":("Heir to the fallen Ehre noble family. Once a slave to the world itself.",
                            "A slippery shifter ranger capable of escaping any danger or shackle.",
                            "The younger brother to a family traitor, and older brother to a new adoptee.",
                            "Very mobile mid-to-close ranged brawler."),
     "Varick Ehre_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(0,3,32,32,1,BLACK),
         ("ability1","name"):"Sharp Teeth",
         ("ability1","description"):"Claws, fangs, and serrated blades. Yikes. Attacks induce bleeding effect.",
         ("ability2","icon"): icon_sprite_sheet.get_image(5,0,32,32,1,BLACK),
         ("ability2","name"):"Drunken Style",
         ("ability2","description"):"Random chance to drink bottle of alcohol. Alcohol gives +2 health.",
         ("ability3","icon"): icon_sprite_sheet.get_image(1,12,32,32,1,BLACK),
         ("ability3","name"):"Tiger Lily Bloom",
         ("ability3","description"):"Random chance that Andrealphus will grant bardic inspiration per turn.",
         }},
    {"Yayan_image": yayan_display.get_image(0,0,407,853,0.38,SCROLL),
     "Yayan_summary":("Devout follower of the god/goddess of luck and good fortune,",
                      "referred to as 'RNGesus'. A blacksmith at heart. Struggles with the",
                      "trauma of a fatherless upbringing. Adventuring to prove herself worthy.",
                      "Proficient in buffing effects and mid-range casting. Very well protected."),
     "Yayan_abilities":
        {("ability1","icon"): icon_sprite_sheet.get_image(13,13,32,32,1,BLACK),
         ("ability1","name"):"Fortune Favors the Bold",
         ("ability1","description"):"Gacha mid-battle! Per turn, gain 1 random food item from your gacha pot.",
         ("ability2","icon"): icon_sprite_sheet.get_image(4,4,32,32,1,BLACK),
         ("ability2","name"):"Heart of the Forge",
         ("ability2","description"):"You are used to working with red hot metal. Gain resistance to fire damage.",
         ("ability3","icon"): icon_sprite_sheet.get_image(2,3,32,32,1,BLACK),
         ("ability3","name"):"Spiritual Weapon",
         ("ability3","description"):"Your real friend. Random chance spiritual weapon will attack per turn.",
         }},
)


ITEMS_DATA = (

)


ATTACKS_DATA = (
    {
        "Number_of_attacks": 5,
        "Lyre_attacks": {
            "attack1_name": "Vicious Mockery",
            "attack1_description": """***CENSORED***""".splitlines(),
            "attack1_stats": {
                "damage": 2,
                "to_hit": 0,
                "range": "Melee, Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "Attack Disadvantage",
                "action_cost": 2
            },
            "attack2_name": "Snake Dagger",
            "attack2_description": """Old reliable.""".splitlines(),
            "attack2_stats": {
                "damage": 6,
                "to_hit": 2,
                "range": "Melee, Thrown",
                "requirements": "None",
                "extra_effects": "Poisoned",
                "action_cost": 2
            },
            "attack3_name": "Grapple",
            "attack3_description": """Get close and personal.""".splitlines(),
            "attack3_stats": {
                "damage": 0,
                "to_hit": 1,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Grappled",
                "action_cost": 2
            },
            "attack4_name": "Shortbow",
            "attack4_description": """Standard shortbow. It smells like the
old farm.""".splitlines(),
            "attack4_stats": {
                "damage": 9,
                "to_hit": 1,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 3
            }, 
            "attack5_name": "Renascitur's Sound Grenade",
            "attack5_description": """You remember Marcello's teachings...
and Meph's jealousy.""".splitlines(),
            "attack5_stats": {
                "damage": 13,
                "to_hit": 4,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "Deafened",
                "action_cost": 4
            } 
        }
    },

    {
        "Number_of_attacks": 7,
        "Marcee De la Mer_attacks": {
            "attack1_name": "Hand Scythe",
            "attack1_description": ["Lilon's old home."],
            "attack1_stats": {
                "damage": 8,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 2
            },
            "attack2_name": "Grapple",
            "attack2_description": ["Get close and personal."],
            "attack2_stats": {
                "damage": 0,
                "to_hit": 1,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Grappled",
                "action_cost": 2
            },
            "attack3_name": "Dagger",
            "attack3_description": ["The rogue classic."],
            "attack3_stats": {
                "damage": 4,
                "to_hit": 4,
                "range": "Melee, Thrown",
                "requirements": "None",
                "extra_effects": "Grappled",
                "action_cost": 2
            },
            "attack4_name": "Blunderbuss",
            "attack4_description": ["The real 1st mate."],
            "attack4_stats": {
                "damage": 10,
                "to_hit": 2,
                "range": "Thrown",
                "requirements": "Reloaded",
                "extra_effects": "Intimidated",
                "action_cost": 3
            },  
            "attack5_name": "Saber of Sezyryn",
            "attack5_description": ["Stolen from a fallen foe.","Forged with red dragon's blood."],
            "attack5_stats": {
                "damage": 10,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Burn",
                "action_cost": 4
            },
            "attack6_name": "Longsword of Revahndri",
            "attack6_description": ["Robbed from a shopkeep.", "Forged with gold dragon's blood."],
            "attack6_stats": {
                "damage": 8,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Protected",
                "action_cost": 4
            },  
            "attack7_name": "Lance of the Restless Sea",
            "attack7_description": ["Scavenged from stolen treasure.", "Holds an enslaved water primordial."],
            "attack7_stats": {
                "damage": 12,
                "to_hit": 1,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Proned",
                "action_cost": 4
            },  
        }
    },
    {
        "Number_of_attacks": 5,
        "Maurlo 'Maurlomallow' Liebermann_attacks": {
            "attack1_name": "Dagger",
            "attack1_description": ["About as large as a rabbit knife."],
            "attack1_stats": {
                "damage": 4,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 1
            },
            "attack2_name": "Thorn Whip",
            "attack2_description": ["For setting up point blank shots."],
            "attack2_stats": {
                "damage": 4,
                "to_hit": 1,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "Forced Melee",
                "action_cost": 2
            },
            "attack3_name": "Shocking Grasp",
            "attack3_description": ["A tazer set to 10,000 volts"],
            "attack3_stats": {
                "damage": 8,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Reaction Stun",
                "action_cost": 3
            },
            "attack4_name": "Light Crossbow",
            "attack4_description": ["Merely back up for when bullets", "run out."],
            "attack4_stats": {
                "damage": 9,
                "to_hit": 2,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 3
            },
            "attack5_name": "Arc Revolver",
            "attack5_description": ["From brother to sister."],
            "attack5_stats": {
                "damage": 12,
                "to_hit": 3,
                "range": "Thrown, Snipe",
                "requirements": "Reloaded",
                "extra_effects": "Intimidated",
                "action_cost": 4
            },
        }
    },
    {
        "Number_of_attacks": 4,
        "Nailea Arorangiurohanga_attacks": {
            "attack1_name": "Dagger",
            "attack1_description": ["It is covered in glitter."],
            "attack1_stats": {
                "damage": 4,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 1
            },
            "attack2_name": "Moon Sickle",
            "attack2_description": ["Smithed with a meteorite from", "Selune"],
            "attack2_stats": {
                "damage": 7,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 2
            },
            "attack3_name": "Infestation",
            "attack3_description": ["Desert locusts from your birthplace."],
            "attack3_stats": {
                "damage": 9,
                "to_hit": 2,
                "range": "Melee, Thrown",
                "requirements": "None",
                "extra_effects": "Poisoned",
                "action_cost": 3
            },
            "attack4_name": "Quori Sword",
            "attack4_description": ["It feeds off of your trauma."],
            "attack4_stats": {
                "damage": 11,
                "to_hit": 3,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Frightened",
                "action_cost": 4
            },
        }
    },
    {
        "Number_of_attacks": 3,
        "Pynncone Amanita_attacks": {
            "attack1_name": "Quarterstaff",
            "attack1_description": ["Its all damp and mossy,", "but sturdy enough."],
            "attack1_stats": {
                "damage": 6,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 2
            },
            "attack2_name": "Shortbow",
            "attack2_description": ["The wood is varnished to", "prevent rotting."],
            "attack2_stats": {
                "damage": 8,
                "to_hit": 3,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 3
            },
            "attack3_name": "Poison Spray",
            "attack3_description": ["A yellow cloud of fungal toxins"],
            "attack3_stats": {
                "damage": 13,
                "to_hit": 4,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Poisoned",
                "action_cost": 3
            },
        }
    },
    {
        "Number_of_attacks": 5,
        "Varick Ehre_attacks": {
            "attack1_name": "Claws",
            "attack1_description": ["For tearing through restraints."],
            "attack1_stats": {
                "damage": 5,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 2
            },
            "attack2_name": "Bite",
            "attack2_description": ["For gnawing through shackles."],
            "attack2_stats": {
                "damage": 7,
                "to_hit": 1,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 1
            },
            "attack3_name": "Shortsword",
            "attack3_description": ["The kind used by particularly", "violent individuals."],
            "attack3_stats": {
                "damage": 8,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 3
            },
            "attack4_name": "Longbow",
            "attack4_description": ["For hunting Owlbears"],
            "attack4_stats": {
                "damage": 9,
                "to_hit": 2,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 3
            },
            "attack5_name": "Whipsword of the Unknown",
            "attack5_description": ["There is a kind of grace", "and elegance to battle."],
            "attack5_stats": {
                "damage": 12,
                "to_hit": 3,
                "range": "Melee, Thrown",
                "requirements": "None",
                "extra_effects": "Grappled",
                "action_cost": 4
            },
        },
    },
    {
        "Number_of_attacks": 3,
        "Yayan_attacks": {
            "attack1_name": "Mace",
            "attack1_description": ["Forged it yourself.", "Quenched in holy water."],
            "attack1_stats": {
                "damage": 7,
                "to_hit": 2,
                "range": "Melee",
                "requirements": "None",
                "extra_effects": "Radiant",
                "action_cost": 2
            },
            "attack2_name": "Light Crossbow",
            "attack2_description": ["A normal bow is too inconvenient", "to draw back with heavy armor on."],
            "attack2_stats": {
                "damage": 9,
                "to_hit": 3,
                "range": "Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "None",
                "action_cost": 3
            },
            "attack3_name": "Sacred Flame",
            "attack3_description": ["Try not to burn down a forest", "this time around."],
            "attack3_stats": {
                "damage": 15,
                "to_hit": 2,
                "range": "Melee, Thrown, Snipe",
                "requirements": "None",
                "extra_effects": "Burn",
                "action_cost": 3
            },
        }
    },

)
    


SPELLS_DATA = (
    {
        "Number_of_spells": 7,
        "Lyre_spells": {
            "spell1_name": "Mage Hand",
            "spell1_description": ["As an arcane rogue, this hand", "is invisible.","Useful for stealing opponent's items."],
            "spell1_stats": {
                "damage": "None",
                "save_dc": 11,
                "dc_type": "Passive Perception",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save,", "steal 1 random item from opponent", "inventory."],
                "action_cost": 3,
                "magic_cost": 5
            },
            "spell2_name": "Tasha's Hideous Laughter",
            "spell2_description": ["A spell constructed by the wizard", "Tasha. Sends its targets into", "a hysterical fit of laughter."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": 13,
                "dc_type": "Wisdom",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, each attck", "and spell attack from the opponent", "deals 3 less damage next turn."],
                "action_cost": 3,
                "magic_cost": 8
            },
            "spell3_name": "Mirror Image",
            "spell3_description": ["Cast up to 3 illusory clones of", "yourself that mimic your every move."],
            "spell3_stats": {
                "damage": "None",
                "save_dc": 12,
                "dc_type": "Wisdom",
                "range": "Melee, Thrown",
                "spell_effect": ["If opponent attacks while this spell", "is active, on a failed save, damage", "of their strongest attack is negated."],
                "action_cost": 4,
                "magic_cost": 12
            },
            "spell4_name": "Suggestion",
            "spell4_description": ["By giving a reasonable enough", "request, you may compel your", "opponent to do anything."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": 12,
                "dc_type": "Charisma",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, choose 1 attack,", "spell, roleplay option, or", "movement zone to disable."],
                "action_cost": 4,
                "magic_cost": 15
            },
            "spell5_name": "Cloud of Daggers",
            "spell5_description": ["Your grief manifests itself as", " sharp blades floating through the", "wind like dandelion seeds."],
            "spell5_stats": {
                "damage": 20,
                "save_dc": 12,
                "dc_type": "Dexterity",
                "range": "Melee",
                "spell_effect": ["On a failed save, opponent takes", "full damage and receives the", "[ Bleeding ] condition. Else,", "opponent only takes half damage."],
                "action_cost": 5,
                "magic_cost": 20
            },
            "spell6_name": "Bestow Curse",
            "spell6_description": ["Words have power, especially words", "of malice. Your strongest", "spell."],
            "spell6_stats": {
                "damage": "None",
                "save_dc": "14",
                "dc_type": "Wisdom",
                "range": "Melee",
                "spell_effect": ["On a failed save, opponent has", "disadvantage against all spell", "saves for 3 turns."],
                "action_cost": 8,
                "magic_cost": 30
            },
            "spell7_name": "Rest",
            "spell7_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell7_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
     },
    {
        "Number_of_spells": 6,
        "Marcee De la Mer_spells": {
            "spell1_name": "Booming Blade",
            "spell1_description": ["Imbue your battle spirit into", "your weapon and make it cry","in battle like rolling thunder."],
            "spell1_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["All weapon attacks next turn", "deal additional +4 thunder damage"],
                "action_cost": 3,
                "magic_cost": 5
            },
            "spell2_name": "Suggestion",
            "spell2_description": ["Half of it is magic,", "the other half is raw seduction.", "Befitting a charming sailor."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": 13,
                "dc_type": "Wisdom",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, choose 1 attack,", "spell, roleplay option, or", "movement zone to disable."],
                "action_cost": 4,
                "magic_cost": 15
            },
            "spell3_name": "Wall of Water",
            "spell3_description": ["Your lance holds the pressure of", "the ocean depths. In every sense,", "You command the seas."],
            "spell3_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["For the next 3 turns,", "incoming ranged weapon attack", "damage is halved and fire", "damage is ignored."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell4_name": "Revahndri's Waltz",
            "spell4_description": ["Your longsword is enchanted with", "a protection spell that activates", "when you use it."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["AC is increased by 4 during", "the next turn."],
                "action_cost": 5,
                "magic_cost": 18
            },
            "spell5_name": "Sezyryn's Sun",
            "spell5_description": ["Your rapier has absorbed the", "essence of the sun. This spell", "conjures an inferno."],
            "spell5_stats": {
                "damage": 30,
                "save_dc": 14,
                "dc_type": "Dexterity",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, opponent takes", "full damage and receives the", "[ Burn ] condition. Else,", "opponent only takes half damage."],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell6_name": "Rest",
            "spell6_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell6_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
    },
    {
        "Number_of_spells": 7,
        "Maurlo 'Maurlomallow' Liebermann_spells": {
            "spell1_name": "Catapult",
            "spell1_description": ["Deploy your magical mini cannon to", "blast anything small and heavy","enough at your opponent."],
            "spell1_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Dexterity",
                "range": "Thrown, Snipe",
                "spell_effect": ["On a failed save, opponent", "takes damage. Else, take no damage."],
                "action_cost": 4,
                "magic_cost": 10
            },
            "spell2_name": "Cure Wounds",
            "spell2_description": ["Nothing a shot of enchanted", "morphine to pick you back up."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Gain +25 additional health points."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell3_name": "Heat Metal",
            "spell3_description": ["You have a lot of magic tools,", "including a turbocharged induction", "magnet."],
            "spell3_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Constitution",
                "range": "None",
                "spell_effect": ["On a failed save, opponent takes", "damage and you may bestow either a", "-3 AC debuff or to disable one", " metal weapon, both for 2 turns."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell4_name": "Invisibility",
            "spell4_description": ["A sheen of light drapes you", "as you disappear from sight."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Until the end of the next turn,", "attacks made on you have", "disadvantage."],
                "action_cost": 5,
                "magic_cost": 20
            },
            "spell5_name": "Vortex Warp",
            "spell5_description": ["You may punch a hole through", "space and make a portal to", "somewhere else."],
            "spell5_stats": {
                "damage": "None",
                "save_dc": 14,
                "dc_type": "Charisma",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, opponent is moved", "to a range zone of your choice.", "They are stuck there until", "the end of next turn."],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell6_name": "Dispel Magic",
            "spell6_description": ["One of your many artifacts", "is a small metal pyramid that", "disables magic in a range."],
            "spell6_stats": {
                "damage": "None",
                "save_dc": 15,
                "dc_type": "Charisma",
                "range": "Melee, Thrown, Snipe",
                "spell_effect": ["On a failed save, choose any", "active spell debuff casted with,", "magic cost equal to 15 or", "lower to dispell"],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell7_name": "Rest",
            "spell7_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell7_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
    },
    {
        "Number_of_spells": 10,
        "Nailea Arorangiurohanga_spells": {
            "spell1_name": "Catapult",
            "spell1_description": ["Deploy your magical mini cannon to", "blast anything small and heavy","enough at your opponent."],
            "spell1_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Dexterity",
                "range": "Thrown, Snipe",
                "spell_effect": ["On a failed save, opponent", "takes damage. Else, take no damage."],
                "action_cost": 4,
                "magic_cost": 10
            },
            "spell2_name": "Cure Wounds",
            "spell2_description": ["Nothing a shot of enchanted", "morphine to pick you back up."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Gain +25 additional health points."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell3_name": "Heat Metal",
            "spell3_description": ["You have a lot of magic tools,", "including a turbocharged induction", "magnet."],
            "spell3_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Constitution",
                "range": "None",
                "spell_effect": ["On a failed save, opponent takes", "damage and you may bestow either a", "-3 AC debuff or to disable one", " metal weapon, both for 2 turns."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell4_name": "Invisibility",
            "spell4_description": ["A sheen of light drapes you", "as you disappear from sight."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Until the end of the next turn,", "attacks made on you have", "disadvantage."],
                "action_cost": 5,
                "magic_cost": 20
            },
            "spell5_name": "Vortex Warp",
            "spell5_description": ["You may punch a hole through", "space and make a portal to", "somewhere else."],
            "spell5_stats": {
                "damage": "None",
                "save_dc": 14,
                "dc_type": "Charisma",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, opponent is moved", "to a range zone of your choice.", "They are stuck there until", "the end of next turn."],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell6_name": "Dispel Magic",
            "spell6_description": ["One of your many artifacts", "is a small metal pyramid that", "disables magic in a range."],
            "spell6_stats": {
                "damage": "None",
                "save_dc": 15,
                "dc_type": "Charisma",
                "range": "Melee, Thrown, Snipe",
                "spell_effect": ["On a failed save, choose any", "active spell debuff casted with,", "magic cost equal to 15 or", "lower to dispell"],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell7_name": "Rest",
            "spell7_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell7_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell8_name": "Rest",
            "spell8_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell8_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell9_name": "Rest",
            "spell9_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell9_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell10_name": "Rest",
            "spell10_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell10_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
    },
    {
        "Number_of_spells": 10,
        "Pynncone Amanita_spells": {
            "spell1_name": "Catapult",
            "spell1_description": ["Deploy your magical mini cannon to", "blast anything small and heavy","enough at your opponent."],
            "spell1_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Dexterity",
                "range": "Thrown, Snipe",
                "spell_effect": ["On a failed save, opponent", "takes damage. Else, take no damage."],
                "action_cost": 4,
                "magic_cost": 10
            },
            "spell2_name": "Cure Wounds",
            "spell2_description": ["Nothing a shot of enchanted", "morphine to pick you back up."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Gain +25 additional health points."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell3_name": "Heat Metal",
            "spell3_description": ["You have a lot of magic tools,", "including a turbocharged induction", "magnet."],
            "spell3_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Constitution",
                "range": "None",
                "spell_effect": ["On a failed save, opponent takes", "damage and you may bestow either a", "-3 AC debuff or to disable one", " metal weapon, both for 2 turns."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell4_name": "Invisibility",
            "spell4_description": ["A sheen of light drapes you", "as you disappear from sight."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Until the end of the next turn,", "attacks made on you have", "disadvantage."],
                "action_cost": 5,
                "magic_cost": 20
            },
            "spell5_name": "Vortex Warp",
            "spell5_description": ["You may punch a hole through", "space and make a portal to", "somewhere else."],
            "spell5_stats": {
                "damage": "None",
                "save_dc": 14,
                "dc_type": "Charisma",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, opponent is moved", "to a range zone of your choice.", "They are stuck there until", "the end of next turn."],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell6_name": "Dispel Magic",
            "spell6_description": ["One of your many artifacts", "is a small metal pyramid that", "disables magic in a range."],
            "spell6_stats": {
                "damage": "None",
                "save_dc": 15,
                "dc_type": "Charisma",
                "range": "Melee, Thrown, Snipe",
                "spell_effect": ["On a failed save, choose any", "active spell debuff casted with,", "magic cost equal to 15 or", "lower to dispell"],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell7_name": "Rest",
            "spell7_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell7_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell8_name": "Rest",
            "spell8_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell8_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell9_name": "Rest",
            "spell9_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell9_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell10_name": "Rest",
            "spell10_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell10_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
    },
    {
        "Number_of_spells": 7,
        "Varick Ehre_spells": {
            "spell1_name": "Catapult",
            "spell1_description": ["Deploy your magical mini cannon to", "blast anything small and heavy","enough at your opponent."],
            "spell1_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Dexterity",
                "range": "Thrown, Snipe",
                "spell_effect": ["On a failed save, opponent", "takes damage. Else, take no damage."],
                "action_cost": 4,
                "magic_cost": 10
            },
            "spell2_name": "Cure Wounds",
            "spell2_description": ["Nothing a shot of enchanted", "morphine to pick you back up."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Gain +25 additional health points."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell3_name": "Heat Metal",
            "spell3_description": ["You have a lot of magic tools,", "including a turbocharged induction", "magnet."],
            "spell3_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Constitution",
                "range": "None",
                "spell_effect": ["On a failed save, opponent takes", "damage and you may bestow either a", "-3 AC debuff or to disable one", " metal weapon, both for 2 turns."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell4_name": "Invisibility",
            "spell4_description": ["A sheen of light drapes you", "as you disappear from sight."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Until the end of the next turn,", "attacks made on you have", "disadvantage."],
                "action_cost": 5,
                "magic_cost": 20
            },
            "spell5_name": "Vortex Warp",
            "spell5_description": ["You may punch a hole through", "space and make a portal to", "somewhere else."],
            "spell5_stats": {
                "damage": "None",
                "save_dc": 14,
                "dc_type": "Charisma",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, opponent is moved", "to a range zone of your choice.", "They are stuck there until", "the end of next turn."],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell6_name": "Dispel Magic",
            "spell6_description": ["One of your many artifacts", "is a small metal pyramid that", "disables magic in a range."],
            "spell6_stats": {
                "damage": "None",
                "save_dc": 15,
                "dc_type": "Charisma",
                "range": "Melee, Thrown, Snipe",
                "spell_effect": ["On a failed save, choose any", "active spell debuff casted with,", "magic cost equal to 15 or", "lower to dispell"],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell7_name": "Rest",
            "spell7_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell7_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell8_name": "Rest",
            "spell8_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell8_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell9_name": "Rest",
            "spell9_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell9_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell10_name": "Rest",
            "spell10_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell10_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
    },
    {
        "Number_of_spells": 10,
        "Yayan_spells": {
            "spell1_name": "Catapult",
            "spell1_description": ["Deploy your magical mini cannon to", "blast anything small and heavy","enough at your opponent."],
            "spell1_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Dexterity",
                "range": "Thrown, Snipe",
                "spell_effect": ["On a failed save, opponent", "takes damage. Else, take no damage."],
                "action_cost": 4,
                "magic_cost": 10
            },
            "spell2_name": "Cure Wounds",
            "spell2_description": ["Nothing a shot of enchanted", "morphine to pick you back up."],
            "spell2_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Gain +25 additional health points."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell3_name": "Heat Metal",
            "spell3_description": ["You have a lot of magic tools,", "including a turbocharged induction", "magnet."],
            "spell3_stats": {
                "damage": 15,
                "save_dc": "13",
                "dc_type": "Constitution",
                "range": "None",
                "spell_effect": ["On a failed save, opponent takes", "damage and you may bestow either a", "-3 AC debuff or to disable one", " metal weapon, both for 2 turns."],
                "action_cost": 5,
                "magic_cost": 15
            },
            "spell4_name": "Invisibility",
            "spell4_description": ["A sheen of light drapes you", "as you disappear from sight."],
            "spell4_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Until the end of the next turn,", "attacks made on you have", "disadvantage."],
                "action_cost": 5,
                "magic_cost": 20
            },
            "spell5_name": "Vortex Warp",
            "spell5_description": ["You may punch a hole through", "space and make a portal to", "somewhere else."],
            "spell5_stats": {
                "damage": "None",
                "save_dc": 14,
                "dc_type": "Charisma",
                "range": "Melee, Thrown",
                "spell_effect": ["On a failed save, opponent is moved", "to a range zone of your choice.", "They are stuck there until", "the end of next turn."],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell6_name": "Dispel Magic",
            "spell6_description": ["One of your many artifacts", "is a small metal pyramid that", "disables magic in a range."],
            "spell6_stats": {
                "damage": "None",
                "save_dc": 15,
                "dc_type": "Charisma",
                "range": "Melee, Thrown, Snipe",
                "spell_effect": ["On a failed save, choose any", "active spell debuff casted with,", "magic cost equal to 15 or", "lower to dispell"],
                "action_cost": 4,
                "magic_cost": 20
            },
            "spell7_name": "Rest",
            "spell7_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell7_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell8_name": "Rest",
            "spell8_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell8_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell9_name": "Rest",
            "spell9_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell9_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            },
            "spell10_name": "Rest",
            "spell10_description": ["It may not be a long", "rest, but it should be", "long enough"],
            "spell10_stats": {
                "damage": "None",
                "save_dc": "None",
                "dc_type": "None",
                "range": "None",
                "spell_effect": ["Skip a turn to regain magic", "Gain 25 magic points next turn."],
                "action_cost": 10,
                "magic_cost": -25
            }
        }
    },
)

ROLEPLAY_DATA = (
    {
        "Number_of_roleplays": 2,
        "Lyre_roleplays":{
            "roleplay1_name": "Bargain",
            "roleplay1_description": ["Your specialty."],
            "roleplay1_stats": {
                "save_dc": "Charisma",
                "dc_type": "10",
                "range": "Melee, Thrown",
                "roleplay_effect": """On a failed save, you successfully strike
a deal with your opponent to disable one of
their attacks. In exchange, you must disable
one of your attacks of an equal action cost.""".splitlines(),
                "action_cost": 2
            },
            "roleplay2_name": "Feign Cease Fire",
            "roleplay2_description": ["You lie as easily as your breathe."],
            "roleplay2_stats": {
                "save_dc": "Wisdom",
                "dc_type": "10",
                "range": "Melee, Thrown",
                "roleplay_effect": """On a failed save, you successfully fool
your opponent into thinking you are yielding.
Your attack immediately after this will be
made with advantage. Each succesful rp will
decrease the dc by -4.""".splitlines(),
                "action_cost": 3
            },
        }
    },
    {
        "Number_of_roleplays": 3,
        "Marcee De la Mer_roleplays":{
            "roleplay1_name": "Flirt",
            "roleplay1_description": ["Your specialty."],
            "roleplay1_stats": {
                "save_dc": "Charisma",
                "dc_type": "10",
                "range": "Melee, Thrown",
                "roleplay_effect": """On a failed save, you fluster
the enemy and they may break concentration
on a spell.""".splitlines(),
                "action_cost": 1
            },
            "roleplay2_name": "Intimidate",
            "roleplay2_description": ["Your big dick energy unsettles lesser people."],
            "roleplay2_stats": {
                "save_dc": "Charisma",
                "dc_type": "10",
                "range": "Melee, Thrown",
                "roleplay_effect": """On a failed save, you successfully unnerve
your opponent. Their next attacks will
deal -3 less damage each.""".splitlines(),
                "action_cost": 2
            },
            "roleplay3_name": "Prank Call",
            "roleplay3_description": ["All hail the magic conch shell."],
            "roleplay3_stats": {
                "save_dc": "Wisdom",
                "dc_type": "10",
                "range": "Snipe",
                "roleplay_effect": """On a failed save, you trick
your opponent into answering your prank
call. Their total action points are reduced
by 2 the next turn.""".splitlines(),
                "action_cost": 2
            },
        }
    },
    {},
    {},
    {},
    {},
    {},
)

ALL_ITEMS =(
    {
        "item_name": None,
        "item_icon": None,
        "item_description": None,
        "item_effect": None,
        "item_action_cost": None
    },
    {
        "item_name": "Potion of Minor Healing",
        "item_icon": icon_sprite_sheet_transparent.get_image(0,9,32,32,2.5,BLACK),
        "item_description": """Its kind of spicy.""".splitlines(),
        "item_effect": """Heals 10 hp.""".splitlines(),
        "item_action_cost": 1
    },
    {
        "item_name": "Potion of Minor Magic",
        "item_icon": icon_sprite_sheet_transparent.get_image(1,9,32,32,2.5,BLACK),
        "item_description": """It glows in the dark.""".splitlines(),
        "item_effect": """Restores 10 mp.""".splitlines(),
        "item_action_cost": 1        
    },
    {
        "item_name": "Cocaine",
        "item_icon": icon_sprite_sheet_transparent.get_image(10,15,32,32,2.5,BLACK),
        "item_description": """Blitzkrieg tactics.""".splitlines(),
        "item_effect": """Gives +3 action points.""".splitlines(),
        "item_action_cost": 0
    },
    {
        "item_name": "Telescope",
        "item_icon": icon_sprite_sheet_transparent.get_image(7,10,32,32,2.5,BLACK),
        "item_description": """200/200 vision""".splitlines(),
        "item_effect": """Attacks made in snipe zone have
a +3 bonus to hit for a turn.""".splitlines(),
        "item_action_cost": 0
    }
)

START_ITEMS = {
    "Lyre_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
    "Marcee De la Mer_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
    "Maurlo 'Maurlomallow' Liebermann_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
    "Nailea Arorangiurohanga_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
    "Pynncone Amanita_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
    "Varick Ehre_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
    "Yayan_items": [ALL_ITEMS[1], ALL_ITEMS[2], ALL_ITEMS[3], ALL_ITEMS[4],
                   ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0], ALL_ITEMS[0],
                   ALL_ITEMS[0]],
}

CHARSHEET_DATA = {
        "Lyre_sheet":{
            "name": "Lyre",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(5,0,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(8,13,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(5,16,32,32,2.5,BLACK),
        },
        "Marcee De la Mer_sheet":{
            "name": "Marcee De la Mer",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(3,1,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(8,11,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(6,0,32,32,2.5,BLACK),
        },
        "Maurlo 'Maurlomallow' Liebermann_sheet":{
            "name": "Maurlo 'Maurlomallow' Liebermann",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(6,12,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(10,15,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(14,3,32,32,2.5,BLACK),
        },
        "Nailea Arorangiurohanga_sheet":{
            "name": "Nailea Arorangiurohanga",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(4,0,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(7,10,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(10,19,32,32,2.5,BLACK),
        },
        "Pynncone Amanita_sheet":{
            "name": "Pynncone Amanita",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(0,12,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(9,13,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(15,12,32,32,2.5,BLACK),
        },
        "Varick Ehre_sheet":{
            "name": "Varick Ehre",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(0,3,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(5,0,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(1,12,32,32,2.5,BLACK),
        },
        "Yayan_sheet":{
            "name": "Yayan",
            "AC": 10,
            "max_hp": 100,
            "max_mp": 100,
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
            "skill1": icon_sprite_sheet.get_image(13,13,32,32,2.5,BLACK),
            "skill2": icon_sprite_sheet.get_image(4,4,32,32,2.5,BLACK),
            "skill3": icon_sprite_sheet.get_image(2,3,32,32,2.5,BLACK),
        },
    }
