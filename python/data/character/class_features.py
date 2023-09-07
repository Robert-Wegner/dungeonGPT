barbarian_class_features = [
    {"name": "Rage", "level": 1, "description": "In battle, you fight with primal ferocity. On your turn, you can enter a rage as a bonus action. While raging, you gain the following benefits if you aren't wearing heavy armor: You have advantage on Strength checks and Strength saving throws. When you make a melee weapon attack using Strength, you gain a bonus to the damage roll that increases as you gain levels as a barbarian, as shown in the Rage Damage column of the Barbarian table. You have resistance to bludgeoning, piercing, and slashing damage. If you are able to cast spells, you can't cast them or concentrate on them while raging. Your rage lasts for 1 minute. It ends early if you are knocked unconscious or if your turn ends and you haven't attacked a hostile creature since your last turn or taken damage since then. You can also end your rage on your turn as a bonus action. Once you have raged the number of times shown for your barbarian level in the Rages column of the Barbarian table, you must finish a long rest before you can rage again."},
    {"name": "Unarmored Defense", "level": 1, "description": "While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a shield and still gain this benefit."},
    {"name": "Reckless Attack", "level": 2, "description": "Starting at 2nd level, you can throw aside all concern for defense to attack with fierce desperation. When you make your first attack on your turn, you can decide to attack recklessly. Doing so gives you advantage on melee weapon attack rolls using Strength during this turn, but attack rolls against you have advantage until your next turn."},
    {"name": "Danger Sense", "level": 2, "description": "At 2nd level, you gain an uncanny sense of when things nearby aren't as they should be, giving you an edge when you dodge away from danger. You have advantage on Dexterity saving throws against effects that you can see, such as traps and spells. To gain this benefit, you can't be blinded, deafened, or incapacitated."},
    {"name": "Frenzy", "level": 3, "description": "You can go into a frenzy when you rage. If you do so, for the duration of your rage you can make a single melee weapon attack as a bonus action on each of your turns after this one. When your rage ends, you suffer one level of exhaustion."},
    {"name": "Mindless Rage", "level": 6, "description": "Beginning at 6th level, you can't be charmed or frightened while raging. If you are charmed or frightened when you enter your rage, the effect is suspended for the duration of the rage."},
    {"name": "Intimidating Presence", "level": 10, "description": "Beginning at 10th level, you can use your action to frighten someone with your menacing presence. When you do so, choose one creature that you can see within 30 feet of you. If the creature can see or hear you, it must succeed on a Wisdom saving throw (DC equal to 8 + your proficiency bonus + your Charisma modifier) or be frightened of you until the end of your next turn. On subsequent turns, you can use your action to extend the duration of this effect on the frightened creature until the end of your next turn. This effect ends if the creature ends its turn out of line of sight or more than 60 feet away from you. If the creature succeeds on its saving throw, you can't use this feature on that creature again for 24 hours."},
    {"name": "Retaliation", "level": 14, "description": "Starting at 14th level, when you take damage from a creature that is within 5 feet of you, you can use your reaction to make a melee weapon attack against that creature."},
    {"name": "Extra Attack", "level": 5, "description": "Beginning at 5th level, you can attack twice, instead of once, whenever you take the Attack action on your turn."},
    {"name": "Fast Movement", "level": 5, "description": "Starting at 5th level, your speed increases by 10 feet while you aren't wearing heavy armor."},
    {"name": "Feral Instinct", "level": 7, "description": "By 7th level, your instincts are so honed that you have advantage on initiative rolls. Additionally, if you are surprised at the beginning of combat and aren't incapacitated, you can act normally on your first turn, but only if you enter your rage before doing anything else on that turn."},
    {"name": "Brutal Critical", "level": 9, "description": "Beginning at 9th level, you can roll one additional weapon damage die when determining the extra damage for a critical hit with a melee attack. This increases to two additional dice at 13th level and three additional dice at 17th level."},
    {"name": "Relentless Rage", "level": 11, "description": "Starting at 11th level, your rage can keep you fighting despite grievous wounds. If you drop to 0 hit points while you're raging and don't die outright, you can make a DC 10 Constitution saving throw. If you succeed, you drop to 1 hit point instead. Each time you use this feature after the first, the DC increases by 5. When you finish a short or long rest, the DC resets to 10."},
    {"name": "Persistent Rage", "level": 15, "description": "Beginning at 15th level, your rage is so fierce that it ends early only if you fall unconscious or if you choose to end it."},
    {"name": "Indomitable Might", "level": 18, "description": "Beginning at 18th level, if your total for a Strength check is less than your Strength score, you can use that score in place of the total."},
    {"name": "Primal Champion", "level": 20, "description": "At 20th level, you embody the power of the wilds. Your Strength and Constitution scores increase by 4. Your maximum for those scores is now 24."}
]


bard_class_features = [
    {"name": "Bardic Inspiration", "level": 1, "description": "You can inspire others through stirring words or music. To do so, you use a bonus action on your turn to choose one creature other than yourself within 60 feet of you who can hear you. That creature gains one Bardic Inspiration die, a d6."},
    {"name": "Jack of All Trades", "level": 2, "description": "Starting at 2nd level, you can add half your proficiency bonus, rounded down, to any ability check you make that doesn't already include your proficiency bonus."},
    {"name": "Song of Rest", "level": 2, "description": "Beginning at 2nd level, you can use soothing music or oration to help revitalize your wounded allies during a short rest. If you or any friendly creatures who can hear your performance regain hit points at the end of the short rest by spending one or more Hit Dice, each of those creatures regains an extra 1d6 hit points."},
    {"name": "Expertise", "level": 3, "description": "At 3rd level, choose two of your skill proficiencies. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies."},
    {"name": "Font of Inspiration", "level": 5, "description": "Beginning when you reach 5th level, you regain all of your expended uses of Bardic Inspiration when you finish a short or long rest."},
    {"name": "Countercharm", "level": 6, "description": "At 6th level, you gain the ability to use musical notes or words of power to disrupt mind-influencing effects. As an action, you can start a performance that lasts until the end of your next turn. During that time, you and any friendly creatures within 30 feet of you have advantage on saving throws against being frightened or charmed. A creature must be able to hear you to gain this benefit. The performance ends early if you are incapacitated or silenced or if you voluntarily end it (no action required)."},
    {"name": "Magical Secrets", "level": 10, "description": "By 10th level, you have plundered magical knowledge from a wide spectrum of disciplines. Choose two spells from any class, including this one. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip."},
    {"name": "Superior Inspiration", "level": 20, "description": "At 20th level, when you roll initiative and have no uses of Bardic Inspiration left, you regain one use."},
    {"name": "College of Lore", "level": 3, "description": "Bards of the College of Lore know something about most things, collecting bits of knowledge from sources as diverse as scholarly tomes and peasant tales. Whether singing folk ballads in taverns or elaborate compositions in royal courts, these bards use their gifts to hold audiences spellbound. When the applause dies down, the audience members might find themselves questioning everything they held to be true, from their faith in the priesthood of the local temple to their loyalty to the king."},
    {"name": "Bonus Proficiencies", "level": 3, "description": "At 3rd level, you gain proficiency with three skills of your choice."},
    {"name": "Cutting Words", "level": 3, "description": "Also at 3rd level, you learn how to use your wit to distract, confuse, and otherwise sap the confidence and competence of others. When a creature that you can see within 60 feet of you makes an attack roll, an ability check, or a damage roll, you can use your reaction to expend one of your uses of Bardic Inspiration, rolling a Bardic Inspiration die and subtracting the number rolled from the creature's roll. You can choose to use this feature after the creature makes its roll, but before the GM determines whether the attack roll or ability check succeeds or fails, or before the creature deals its damage. The creature is immune if it can't hear you or if it's immune to being charmed."},
    {"name": "Additional Magical Secrets", "level": 6, "description": "At 6th level, you learn two spells of your choice from any class. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip. The chosen spells count as bard spells for you but don't count against the number of bard spells you know."},
    {"name": "Peerless Skill", "level": 14, "description": "Starting at 14th level, when you make an ability check, you can expend one use of Bardic Inspiration. Roll a Bardic Inspiration die and add the number rolled to your ability check. You can choose to do so after you roll the die for the ability check, but before the GM tells you whether you succeed or fail."}
]

cleric_class_features = [
    {
        'name': 'Channel Divinity: Turn Undead',
        'level': 2,
        'description': 'As an action, you present your holy symbol and speak a prayer censuring the undead. Each undead that can see or hear you within 30 feet of you must make a Wisdom saving throw...'
    },
    {
        'name': 'Destroy Undead',
        'level': 5,
        'description': 'Starting at 5th level, when an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed if its challenge rating is at or below a certain threshold, as shown in the Destroy Undead table...'
    },
    {
        'name': 'Divine Intervention',
        'level': 10,
        'description': 'Beginning at 10th level, you can call on your deity to intervene on your behalf when your need is great...',
    },
    {
        'name': 'Life Domain Spells',
        'level': 1,
        'description': 'Cleric Level Spells\n1st bless, cure wounds\n3rd lesser restoration, spiritual weapon\n5th beacon of hope, revivify\n7th death ward, guardian of faith\n9th mass cure wounds, raise dead'
    },
    {
        'name': 'Bonus Proficiency',
        'level': 1,
        'description': 'When you choose this domain at 1st level, you gain proficiency with heavy armor.'
    },
    {
        'name': 'Disciple of Life',
        'level': 1,
        'description': 'Also starting at 1st level, your healing spells are more effective. Whenever you use a spell of 1st level or higher to restore hit points to a creature, the creature regains additional hit points equal to 2 + the spell\'s level.'
    },
    {
        'name': 'Channel Divinity: Preserve Life',
        'level': 2,
        'description': 'Starting at 2nd level, you can use your Channel Divinity to heal the badly injured. As an action, you present your holy symbol and evoke healing energy...'
    },
    {
        'name': 'Blessed Healer',
        'level': 6,
        'description': 'Beginning at 6th level, the healing spells you cast on others heal you as well. When you cast a spell of 1st level or higher that restores hit points to a creature other than you, you regain hit points equal to 2 + the spell\'s level.'
    },
    {
        'name': 'Divine Strike',
        'level': 8,
        'description': 'At 8th level, you gain the ability to infuse your weapon strikes with divine energy. Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 radiant damage to the target. When you reach 14th level, the extra damage increases to 2d8.'
    },
    {
        'name': 'Supreme Healing',
        'level': 17,
        'description': 'Starting at 17th level, when you would normally roll one or more dice to restore hit points with a spell, you instead use the highest number possible for each die. For example, instead of restoring 2d6 hit points to a creature, you restore 12.'
    }
]

druid_class_features = [
    {
        'name': 'Wild Shape',
        'level': 2,
        'description': 'Assume the shape of a beast seen before. Can be used twice, recharged after rest. Restrictions based on druid level. While transformed, game statistics are replaced by beast statistics, but alignment, personality, and Intelligence, Wisdom, and Charisma scores remain.'
    },
    {
        'name': 'Circle of the Land - Bonus Cantrip',
        'level': 2,
        'description': 'Learn one additional druid cantrip.'
    },
    {
        'name': 'Circle of the Land - Natural Recovery',
        'level': 2,
        'description': 'Regain magical energy by meditating during a short rest. Choose expended spell slots to recover equal to half your druid level (rounded up).'
    },
    {
        'name': 'Circle of the Land - Circle Spells',
        'level': 3,
        'description': 'Gain access to circle spells connected to the land where you became a druid. Specific spells available at 3rd, 5th, 7th and 9th level.\nArctic Druid Level Circle Spells: 3rd - hold person, spike growth; 5th - sleet storm, slow; 7th - freedom of movement, ice storm; 9th - commune with nature, cone of cold.\nCoast Druid Level Circle Spells: 3rd - mirror image, misty step; 5th - water breathing, water walk; 7th - control water, freedom of movement; 9th - conjure elemental, scrying.\nDesert Druid Level Circle Spells: 3rd - blur, silence; 5th - create food and water, protection from energy; 7th - blight, hallucinatory terrain; 9th - insect plague, wall of stone.\nForest Druid Level Circle Spells: 3rd - barkskin, spider climb; 5th - call lightning, plant growth; 7th - divination, freedom of movement; 9th - commune with nature, tree stride.\nGrassland Druid Level Circle Spells: 3rd - invisibility, pass without trace; 5th - daylight, haste; 7th - divination, freedom of movement; 9th - dream, insect plague.\nMountain Druid Level Circle Spells: 3rd - spider climb, spike growth; 5th - lightning bolt, meld into stone; 7th - stone shape, stoneskin; 9th - passwall, wall of stone.\nSwamp Druid Level Circle Spells: 3rd - acid arrow, darkness; 5th - water walk, stinking cloud; 7th - freedom of movement, locate creature; 9th - insect plague, scrying.'
    },
    {
        'name': 'Timeless Body',
        'level': 18,
        'description': 'Age more slowly. For every 10 years that pass, your body ages only 1 year.'
    },
    {
        'name': 'Beast Spells',
        'level': 18,
        'description': 'Can cast druid spells in any shape assumed using Wild Shape.'
    },
    {
        'name': 'Archdruid',
        'level': 20,
        'description': 'Use Wild Shape an unlimited number of times. Ignore verbal and somatic components of druid spells.'
    },
    {
        'name': 'Circle of the Land - Land\'s Stride',
        'level': 6,
        'description': 'Moving through nonmagical difficult terrain costs no extra movement. Pass through nonmagical plants without being slowed or taking damage.'
    },
    {
        'name': 'Circle of the Land - Nature\'s Ward',
        'level': 10,
        'description': 'Can\'t be charmed or frightened by elementals or fey, and immune to poison and disease.'
    },
    {
        'name': 'Circle of the Land - Nature\'s Sanctuary',
        'level': 14,
        'description': 'Creatures of the natural world become hesitant to attack. When a beast or plant creature attacks you, it must make a Wisdom saving throw; on fail, it must choose a different target or the attack automatically misses.'
    }
]

fighter_class_features = [
  {
    "name": "Fighting Style",
    "level": 1,
    "description": "Choose a fighting style as your specialty. You can't choose the same style more than once.\n\nArchery: You gain a +2 bonus to attack rolls you make with ranged weapons.\n\nDefense: While you are wearing armor, you gain a +1 bonus to AC.\n\nDueling: When you are wielding a melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.\n\nGreat Weapon Fighting: When you roll a 1 or 2 on a damage die for an attack you make with a two-handed melee weapon, you can reroll the die and must use the new roll, even if the new roll is a 1 or a 2.\n\nProtection: When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield.\n\nTwo-Weapon Fighting: When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack."
  },
  {
    "name": "Second Wind",
    "level": 1,
    "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again."
  },
  {
    "name": "Action Surge",
    "level": 2,
    "description": "Starting at 2nd level, you can push yourself beyond your normal limits for a moment. On your turn, you can take one additional action on top of your regular action and a possible bonus action. Once you use this feature, you must finish a short or long rest before you can use it again. Starting at 17th level, you can use it twice before a rest, but only once on the same turn."
  },
  {
    "name": "Martial Archetype",
    "level": 3,
    "description": "Choose an archetype at 3rd level that provides features at various levels."
  },
  {
    "name": "Extra Attack",
    "level": 5,
    "description": "Beginning at 5th level, you can attack twice, instead of once, whenever you take the Attack action on your turn. The number of attacks increases to three when you reach 11th level in this class and to four when you reach 20th level in this class."
  },
  {
    "name": "Indomitable",
    "level": 9,
    "description": "Beginning at 9th level, you can reroll a saving throw that you fail. If you do so, you must use the new roll, and you can't use this feature again until you finish a long rest. You can use this feature twice between long rests starting at 13th level and three times between long rests starting at 17th level."
  },
  {
    "name": "Champion - Improved Critical",
    "level": 3,
    "description": "At 3rd level, as a Champion, your weapon attacks score a critical hit on a roll of 19 or 20."
  },
  {
    "name": "Champion - Remarkable Athlete",
    "level": 7,
    "description": "Starting at 7th level as a Champion, you can add half your proficiency bonus (rounded up) to any Strength, Dexterity, or Constitution checks you make that don't already use your proficiency bonus. In addition, when you make a running long jump, the distance you can cover increases by a number of feet equal to your Strength modifier."
  },
  {
    "name": "Champion - Additional Fighting Style",
    "level": 10,
    "description": "At 10th level as a Champion, you can choose a second option from the Fighting Style class feature."
  },
  {
    "name": "Champion - Superior Critical",
    "level": 15,
    "description": "Starting at 15th level, your weapon attacks score a critical hit on a roll of 18–20."
  },
  {
    "name": "Champion - Survivor",
    "level": 18,
    "description": "At 18th level as a Champion, you attain the pinnacle of resilience in battle. At the start of each of your turns, you regain hit points equal to 5 + your Constitution modifier if you have no more than half of your hit points left. You don't gain this benefit if you have 0 hit points."
  }
]

paladin_class_features = [
    {
        "name": "Divine Sense",
        "level": 1,
        "description": "As an action, detect celestial, fiend, or undead beings within 60 feet. Also detect consecrated or desecrated places or objects within the same radius. Can use this feature a number of times equal to 1 + Charisma modifier. Regain all uses after a long rest."
    },
    {
        "name": "Lay on Hands",
        "level": 1,
        "description": "Pool of healing power that replenishes after a long rest. Restore hit points equal to paladin level × 5 as an action. Can also cure diseases or neutralize poisons by expending 5 hit points from the pool. No effect on undead and constructs."
    },
    {
        "name": "Fighting Style",
        "level": 2,
        "description": "Choose one of the following options: Defense (+1 bonus to AC while wearing armor), Dueling (+2 bonus to damage rolls when wielding a melee weapon in one hand and no other weapons), Great Weapon Fighting (reroll 1s or 2s on damage dice for melee weapons wielded with two hands), Protection (impose disadvantage on attacks against targets other than you within 5 feet when wielding a shield)."
    },
    {
        "name": "Spellcasting",
        "level": 2,
        "description": "Learn to cast spells like a cleric. Prepare a number of spells equal to Charisma modifier + half paladin level. Cast spells using spell slots, which are regained after a long rest. Use Charisma for spellcasting ability, saving throw DC, and spell attack modifier. Can use a holy symbol as a spellcasting focus."
    },
    {
        "name": "Divine Smite",
        "level": 2,
        "description": "When hitting a creature with a melee weapon attack, expend a spell slot to deal additional radiant damage. Extra damage is 2d8 for 1st-level spell slot, +1d8 for each higher level. Damage increases by 1d8 against undead or fiends."
    },
    {
        "name": "Divine Health",
        "level": 3,
        "description": "Immune to disease."
    },
    {
        "name": "Sacred Oath",
        "level": 3,
        "description": "Swear an oath at 3rd level, granting features at 3rd, 7th, 15th, and 20th level. Each oath provides oath spells and the Channel Divinity feature. Oath spells always prepared and don't count against the number of spells prepared each day."
    },
    {
        "name": "Extra Attack",
        "level": 5,
        "description": "Attack twice instead of once when taking the Attack action."
    },
    {
        "name": "Aura of Protection",
        "level": 6,
        "description": "Friendly creatures within 10 feet gain a bonus to saving throws equal to Charisma modifier (minimum +1). Aura range increases to 30 feet at 18th level."
    },
    {
        "name": "Aura of Courage",
        "level": 10,
        "description": "You and friendly creatures within 10 feet can't be frightened. Aura range increases to 30 feet at 18th level."
    },
    {
        "name": "Improved Divine Smite",
        "level": 11,
        "description": "All melee weapon strikes deal an additional 1d8 radiant damage. Add this damage to Divine Smite's extra damage when used together."
    },
    {
        "name": "Cleansing Touch",
        "level": 14,
        "description": "Use action to end one spell on yourself or a willing creature. Can use a number of times equal to Charisma modifier. Regain uses after a long rest."
    },
    {
        "name": "Aura of Devotion",
        "level": 7,
        "description": "You and friendly creatures within 10 feet can't be charmed. Aura range increases to 30 feet at 18th level."
    },
    {
        "name": "Purity of Spirit",
        "level": 15,
        "description": "Always under the effects of protection from evil and good spell."
    },
    {
        "name": "Holy Nimbus",
        "level": 20,
        "description": '''Emanate an aura of sunlight as an action. For 1 minute, bright light shines from you in a 30-foot radius, and dim light shines 30 feet beyond that.
                        Whenever an enemy creature starts its turn in the bright light, the creature takes 10 radiant damage.
                        In addition, for the duration, you have advantage on saving throws against spells cast by fiends or undead.
                        Once you use this feature, you can't use it again until you finish a long rest.'''
    },
    {
        "name": "Breaking your Oath",
        "level": 3,
        "description": "A paladin, who strives to uphold high standards of conduct, may still make mistakes or stray from their oath. In such cases, they seek absolution from a cleric or another paladin of the same order. This absolution can involve acts of penitence, confession, and forgiveness. However, if a paladin intentionally breaks their oath without showing remorse, they may be forced to abandon the paladin class."
    },
    {
        'name': 'Sacred Weapon', 
        'level': 8, 
        'description': "Imbue a weapon with positive energy, adding Charisma modifier to attack rolls, emitting bright light, and making it magical for 1 minute."
    },
    {
        'name': 'Turn the Unholy', 
        'level': 8, 
        'description': "Use holy symbol and prayer to censure fiends and undead within 30 feet. They must make a Wisdom saving throw or be turned for 1 minute or until taking damage. Turned creatures must move away, can't approach within 30 feet, can't take reactions, and can only use Dash or try to escape."
    }
]

ranger_class_features = [
  {
    "name": "Favored Enemy",
    "level": 1,
    "description": "Choose a type of favored enemy: aberrations, beasts, celestials, constructs, dragons, elementals, fey, fiends, giants, monstrosities, oozes, plants, or undead. Alternatively, choose two races of humanoid as favored enemies. Gain advantage on Wisdom (Survival) checks to track favored enemies and on Intelligence checks to recall information about them. Learn one language spoken by favored enemies."
  },
  {
    "name": "Natural Explorer",
    "level": 1,
    "description": "Choose one type of favored terrain: arctic, coast, desert, forest, grassland, mountain, or swamp. Gain double proficiency bonus on Intelligence or Wisdom checks related to favored terrain. While traveling for an hour or more in favored terrain, gain various benefits."
  },
  {
    "name": "Fighting Style",
    "level": 2,
    "description": "Choose one of the following options: Archery, Defense, Dueling, or Two-Weapon Fighting. Gain specific bonus according to chosen style."
  },
  {
    "name": "Primeval Awareness",
    "level": 3,
    "description": "Use action and expend ranger spell slot to sense presence of certain creature types within a range. Doesn't reveal location or number of creatures."
  },
  {
    "name": "Extra Attack",
    "level": 5,
    "description": "When taking Attack action, make two attacks instead of one."
  },
  {
    "name": "Hunter's Prey",
    "level": 3,
    "description": "Choose one of the following features: Colossus Slayer, Giant Killer, or Horde Breaker. Colossus Slayer: When the character hits a creature with a weapon attack, they deal an additional 1d8 damage if the creature is below its maximum hit points. This extra damage can only be dealt once per turn. Giant Killer: When a Large or larger creature within 5 feet of the character hits or misses them with an attack, the character can use their reaction to immediately attack that creature, provided they can see it. Horde Breaker: Once on each of the character's turns when they make a weapon attack, they can make another attack with the same weapon against a different creature that is within 5 feet of the original target and within range of their weapon.",
  },
  {
    "name": "Land's Stride",
    "level": 8,
    "description": "Move through nonmagical difficult terrain without extra movement. Pass through nonmagical plants without being slowed or damaged. Gain advantage on saving throws against certain magically created or manipulated plants."
  },
  {
    "name": "Defensive Tactics",
    "level": 7,
    "description": "Choose one of the following features: Escape the Horde, Multiattack Defense, or Steel Will. Escape the Horde: Opportunity attacks against you are made with disadvantage. Multiattack Defense: When a creature hits you with an attack, you gain a +4 bonus to AC against all subsequent attacks made by that creature for the rest of the turn. Steel Will: You have advantage on saving throws against being frightened.",
  },
  {
    "name": "Multiattack",
    "level": 11,
    "description": "Choose one of the following features: Volley or Whirlwind Attack.  Volley allows a player to make a ranged attack against multiple creatures within a 10-foot range of a visible point, using ammunition and making individual attack rolls for each target. Whirlwind attack permits a player to make a melee attack against multiple creatures within 5 feet of them, also requiring separate attack rolls for each target.",
  },
  {
    "name": "Hide in Plain Sight",
    "level": 10,
    "description": "Spend 1 minute creating camouflage to hide. Gain bonus to Stealth checks as long as remaining still. Must camouflage again after moving or taking action/reaction."
  },
  {
    "name": "Superior Hunter's Defense",
    "level": 15,
    "description": "Choose one of the following features: Evasion, Stand Against the Tide, or Uncanny Dodge. Evasion allows you to avoid damage when making a successful Dexterity saving throw against an effect. Stand Against the Tide lets you redirect a missed melee attack towards another creature. Uncanny Dodge allows you to halve the damage of an attack if you can see the attacker and use your reaction."
  },
  {
    "name": "Vanish",
    "level": 14,
    "description": "Use Hide action as a bonus action. Can't be tracked by nonmagical means."
  },
  {
    "name": "Feral Senses",
    "level": 18,
    "description": "Attack creatures you can't see without disadvantage. Aware of location of invisible creatures within 30 feet of you."
  },
  {
    "name": "Foe Slayer",
    "level": 20,
    "description": "Once per turn, add Wisdom modifier to attack roll or damage roll against favored enemies."
  }
]

rogue_class_features = [{
    "name": "Expertise",
    "level": 1,
    "description": "At 1st level, choose two of your skill proficiencies, or one of your skill proficiencies and your proficiency with thieves' tools. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies. At 6th level, you can choose two more of your proficiencies (in skills or with thieves' tools) to gain this benefit."
    },
    {
    "name": "Sneak Attack",
    "level": 1,
    "description": "Beginning at 1st level, you know how to strike subtly and exploit a foe's distraction. Once per turn, you can deal an extra 1d6 damage to one creature you hit with an attack if you have advantage on the attack roll. The attack must use a finesse or a ranged weapon. You don't need advantage on the attack roll if another enemy of the target is within 5 feet of it, that enemy isn't incapacitated, and you don't have disadvantage on the attack roll. The amount of the extra damage increases as you gain levels in this class, as shown in the Sneak Attack column of the Rogue table."
    },
    {
    "name": "Thieves' Cant",
    "level": 1,
    "description": "During your rogue training you learned thieves' cant, a secret mix of dialect, jargon, and code that allows you to hide messages in seemingly normal conversation. Only another creature that knows thieves' cant understands such messages. It takes four times longer to convey such a message than it does to speak the same idea plainly. In addition, you understand a set of secret signs and symbols used to convey short, simple messages, such as whether an area is dangerous or the territory of a thieves' guild, whether loot is nearby, or whether the people in an area are easy marks or will provide a safe house for thieves on the run."
    },
    {
    "name": "Cunning Action",
    "level": 2,
    "description": "Starting at 2nd level, your quick thinking and agility allow you to move and act quickly. You can take a bonus action on each of your turns in combat. This action can be used only to take the Dash, Disengage, or Hide action."
    },
    {
    "name": "Uncanny Dodge",
    "level": 5,
    "description": "Starting at 5th level, when an attacker that you can see hits you with an attack, you can use your reaction to halve the attack's damage against you."
    },
    {
    "name": "Evasion",
    "level": 7,
    "description": "Beginning at 7th level, you can nimbly dodge out of the way of certain area effects, such as a red dragon's fiery breath or an ice storm spell. When you are subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw, and only half damage if you fail."
    },
    {
    "name": "Reliable Talent",
    "level": 11,
    "description": "By 11th level, you have refined your chosen skills until they approach perfection. Whenever you make an ability check that lets you add your proficiency bonus, you can treat a d20 roll of 9 or lower as a 10."
    },
    {
    "name": "Blindsense",
    "level": 14,
    "description": "Starting at 14th level, if you are able to hear, you are aware of the location of any hidden or invisible creature within 10 feet of you."
    },
    {
    "name": "Slippery Mind",
    "level": 15,
    "description": "By 15th level, you have acquired greater mental strength. You gain proficiency in Wisdom saving throws."
    },
    {
    "name": "Elusive",
    "level": 18,
    "description": "Beginning at 18th level, you are so evasive that attackers rarely gain the upper hand against you. No attack roll has advantage against you while you aren't incapacitated."
    },
    {
    "name": "Stroke of Luck",
    "level": 20,
    "description": "At 20th level, you have an uncanny knack for succeeding when you need to. If your attack misses a target within range, you can turn the miss into a hit. Alternatively, if you fail an ability check, you can treat the d20 roll as a 20. Once you use this feature, you can't use it again until you finish a short or long rest."
    },
    {
    "name": "Fast Hands",
    "level": 3,
    "description": "Starting at 3rd level, you can use the bonus action granted by your Cunning Action to make a Dexterity (Sleight of Hand) check, use your thieves' tools to disarm a trap or open a lock, or take the Use an Object action."
    },
    {
    "name": "Second-Story Work",
    "level": 3,
    "description": "When you choose this archetype at 3rd level, you gain the ability to climb faster than normal; climbing no longer costs you extra movement. In addition, when you make a running jump, the distance you cover increases by a number of feet equal to your Dexterity modifier."
    },
    {
    "name": "Supreme Sneak",
    "level": 9,
    "description": "Starting at 9th level, you have advantage on a Dexterity (Stealth) check if you move no more than half your speed on the same turn."
    },
    {
    "name": "Use Magic Device",
    "level": 13,
    "description": "By 13th level, you have learned enough about the workings of magic that you can improvise the use of items even when they are not intended for you. You ignore all class, race, and level requirements on the use of magic items."
    },
    {
    "name": "Thief's Reflexes",
    "level": 17,
    "description": "When you reach 17th level, you have become adept at laying ambushes and quickly escaping danger. You can take two turns during the first round of any combat. You take your first turn at your normal initiative and your second turn at your initiative minus 10. You can't use this feature when you are surprised."
    }
]

sorcerer_class_features = [
    { 
        "name": "Sorcery Points",
        "level": 2,
        "description": "Start with 2 sorcery points, gain more as you reach higher levels. Regain all spent points after a long rest."
    },
    { 
        "name": "Flexible Casting",
        "level": 2,
        "description": "Use sorcery points to gain additional spell slots or sacrifice spell slots to gain additional sorcery points."
    },
    { 
        "name": "Creating Spell Slots",
        "level": 2,
        "description": "Transform unexpended sorcery points into one spell slot as a bonus action. Cannot create spell slots higher than 5th level."
    },
    { 
        "name": "Converting Spell Slot to Sorcery Points",
        "level": 2,
        "description": "Expend one spell slot to gain a number of sorcery points equal to the slot’s level."
    },
    { 
        "name": "Metamagic",
        "level": 3,
        "description": "Gain the ability to twist your spells to suit your needs with two Metamagic options of your choice. Gain additional ones at 10th and 17th level."
    },
    { 
        "name": "Metamagic - Careful Spell",
        "level": 3,
        "description": "Spend 1 sorcery point to protect creatures from a spell's full force."
    },
    { 
        "name": "Metamagic - Distant Spell",
        "level": 3,
        "description": "Spend 1 sorcery point to double the range of a spell."
    },
    { 
        "name": "Metamagic - Empowered Spell",
        "level": 3,
        "description": "Spend 1 sorcery point to reroll damage for a spell, must use the new rolls."
    },
    { 
        "name": "Metamagic - Extended Spell",
        "level": 3,
        "description": "Spend 1 sorcery point to double the duration of a spell."
    },
    { 
        "name": "Metamagic - Heightened Spell",
        "level": 3,
        "description": "Spend 3 sorcery points to give a target of the spell disadvantage on its first saving throw against it."
    },
    { 
        "name": "Metamagic - Quickened Spell",
        "level": 3,
        "description": "Spend 2 sorcery points to change the casting time of a spell to 1 bonus action."
    },
    { 
        "name": "Metamagic - Subtle Spell",
        "level": 3,
        "description": "Spend 1 sorcery point to cast a spell without any somatic or verbal components."
    },
    { 
        "name": "Metamagic - Twinned Spell",
        "level": 3,
        "description": "Spend sorcery points equal to a spell's level to target a second creature with the same spell."
    },
    { 
        "name": "Sorcerous Restoration",
        "level": 20,
        "description": "Regain 4 expended sorcery points whenever you finish a short rest."
    },
    { 
        "name": "Dragon Ancestor",
        "level": 1,
        "description": "Choose one type of dragon as your ancestor. The damage type associated with the dragon is used by features you gain later."
    },
    { 
        "name": "Draconic Ancestry",
        "level": 1,
        "description": "Ability to speak, read, and write Draconic. Interacting with dragons doubles your proficiency bonus if it applies."
    },
    { 
        "name": "Draconic Resilience",
        "level": 1,
        "description": "Your hit point maximum increases by 1, with an additional 1 increase per level. Your skin gains dragon-like scales providing extra armor."
    },
    { 
        "name": "Elemental Affinity",
        "level": 6,
        "description": "Add Charisma modifier to damage roll of spell related to your draconic ancestry. Spend 1 sorcery point to gain resistance to that damage type for 1 hour."
    },
    { 
        "name": "Dragon Wings",
        "level": 14,
        "description": "Gain the ability to sprout wings and fly at your current speed. Wings can be created as a bonus action and lasts till dismissed. Wings can't be manifested while wearing restrictive armor/clothes."
    },
    { 
        "name": "Draconic Presence",
        "level": 18,
        "description": "Channel the dread presence of your dragon ancestor and exude an aura of awe or fear. Extends to 60 feet. Expend 5 sorcery points to use this power."
    }
]

wizard_class_features = [
    {
        "name": "Arcane Recovery",
        "level": 1,
        "description": "Regain spent magical energy via spellbook study. Once daily after a short rest, you can recover spell slots totaling half your wizard level (round up), but not including slots of 6th level or higher."
    },
    {
        "name": "Spell Mastery",
        "level": 18,
        "description": "Master a 1st-level and a 2nd-level spell from your spellbook for at-will casting. With 8 hours of study, swap chosen spells for others of same level."
    },
    {
        "name": "Signature Spells",
        "level": 20,
        "description": "Master two 3rd-level spells from your spellbook for simplified casting. These spells, once chosen, are always prepared and can be cast once without expending a spell slot. Refresh this ability with a short or long rest."
    },
    {
        "name": 'Evocation Savant', 
        "level": 2, 
        "description": 'At 2nd level, copying an evocation spell into your spellbook requires half the gold and time.'
    },
    {
        "name": 'Sculpt Spells', 
        "level": 2, 
        "description": 'At 2nd level, create safe zones within your evocation spells. Affected creatures of your choice = 1 + spell\'s level, who automatically succeed on their saves, taking no damage if they normally take half on success.'
    },
    {
        "name": 'Potent Cantrip', 
        "level": 6, 
        "description": 'From 6th level, damaging cantrips affect even dodgy creatures, inflicting half damage on successful save, with no added cantrip effects.'
    },
    {
        "name": 'Empowered Evocation', 
        "level": 10, 
        "description": 'From 10th level, add your Intelligence modifier to one damage roll of any wizard evocation spell you cast.'
    },
    {
        "name": 'Overchannel', 
        "level": 14, 
        "description": 'From 14th level, maximize damage of your 1st-5th level damaging wizard spell. No effect on first use, but subsequent uses pre-long rest inflict 2d12 necrotic damage per spell level, increasing by 1d12 each use, bypassing resistance and immunity.'
    },
    {
        "name:": 'Spellbook',
        "level": 1,
        "description": '''As you gain levels, you add spells to your spellbook that reflect your arcane research and intellectual discoveries about the universe. This can come from various sources like scrolls found in your adventures or old books in libraries.
            To copy a spell into your spellbook, it must satisfy two conditions: it must be a wizard spell of at least 1st level and it must be a level you can prepare. You must reproduce the basic form of the spell, decode the original wizard's notation, practice the spell, then write it in your spellbook. This takes 2 hours and costs 50 gp per spell level. The fee covers materials for mastering the spell and recording it. After spending this time and money, the spell is now prepared like your other spells.
            You can copy a spell from your own spellbook into another book for backup, which is faster and easier since you know your notation and the spell. This costs 1 hour and 10 gp per spell level. If your spellbook is lost, you follow the same process to transfer your prepared spells into a new book. For additional spells, you must find new ones. Many wizards keep backup spellbooks as precaution.
            Your spellbook can have various forms, depending on your preferences.'''
    }
]

