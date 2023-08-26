all_classes = [
    'Barbarian',
    'Bard',
    'Cleric',
    'Druid',
    'Fighter',
    'Paladin',
    'Ranger',
    'Rogue',
    'Sorcerer',
    'Wizard'
]


class CharacterSheet:
    
    def __init__(self, name, race, character_class, skill_proficiencies, #choose 2, options depending on class
                    STR=0, DEX=0, CON=0, INT=0, WIS=0, CHA=0
                    ):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.level = 1
        self.level_speed = 5
        self.XP = 0

        self.AC = 10

        self.ability_scores = {
            'STR', 0,
            'DEX', 0,
            'CON', 0,
            'INT', 0,
            'WIS', 0,
            'CHA', 0
        }
        self.ability_modifiers = {
            'STR', 0,
            'DEX', 0,
            'CON', 0,
            'INT', 0,
            'WIS', 0,
            'CHA', 0
        }
        self.ability_scores_race_bonus = {
            'STR', 0,
            'DEX', 0,
            'CON', 0,
            'INT', 0,
            'WIS', 0,
            'CHA', 0
        }
        if race == 'Elf':
            self.ability_scores_race_bonus['DEX'] = 2
            self.ability_scores_race_bonus['INT'] = 1
        elif race == 'Dwarf':
            self.ability_scores_race_bonus['CON'] = 2
            self.ability_scores_race_bonus['WIS'] = 1
        elif race == 'Halfling':
            self.ability_scores_race_bonus['DEX'] = 2
            self.ability_scores_race_bonus['CHA'] = 1
        elif race == 'Human':
            self.ability_scores_race_bonus['STR'] = 1
            self.ability_scores_race_bonus['DEX'] = 1
            self.ability_scores_race_bonus['CON'] = 1
            self.ability_scores_race_bonus['INT'] = 1
            self.ability_scores_race_bonus['WIS'] = 1
            self.ability_scores_race_bonus['CHA'] = 1
        elif race == 'Dragonborn':
            self.ability_scores_race_bonus['STR'] = 2
            self.ability_scores_race_bonus['CHA'] = 1
        elif race == 'Gnome':
            self.ability_scores_race_bonus['INT'] = 2
            self.ability_scores_race_bonus['CON'] = 1
        elif race == 'Half-Elf':
            self.ability_scores_race_bonus['CHA'] = 2
            self.ability_scores_race_bonus['DEX'] = 1
            self.ability_scores_race_bonus['STR'] = 1
        elif race == 'Half-Orc':
            self.ability_scores_race_bonus['STR'] = 2
            self.ability_scores_race_bonus['CON'] = 1
        elif race == 'Tiefling':
            self.ability_scores_race_bonus['CHA'] = 2
            self.ability_scores_race_bonus['INT'] = 1
        
        self.skills = {
            'acrobatics': 0,
            'animal_handling': 0,
            'arcana': 0,
            'athletics': 0,
            'deception': 0,
            'history': 0,
            'insight': 0,
            'intimidation': 0,
            'investigation': 0,
            'medicine': 0,
            'nature': 0,
            'perception': 0,
            'performance': 0,
            'persuasion': 0,
            'religion': 0,
            'sleight_of_hand': 0,
            'stealth': 0,
            'survival': 0
        }
        
        self.set_ability_score('STR', STR + self.ability_scores_race_bonus['STR'])
        self.set_ability_score('DEX', DEX + self.ability_scores_race_bonus['DEX'])
        self.set_ability_score('CON', CON + self.ability_scores_race_bonus['CON'])
        self.set_ability_score('INT', INT + self.ability_scores_race_bonus['INT'])
        self.set_ability_score('WIS', WIS + self.ability_scores_race_bonus['WIS'])
        self.set_ability_score('CHA', CHA + self.ability_scores_race_bonus['CHA'])
        
        self.proficiency_bonus = 0
        self.set_proficiency_bonus(self.compute_proficiency_bonus())
        self.set_skill_proficiencies(skill_proficiencies)

        self.hit_dice = self.compute_hit_dice()

        self.maxHP = int(self.hit_dice[1:]) + (1 if self.race == 'Dwarf' else 0)

        self.HP = self.maxHP

        self.spellcasting_ability_mod = self.compute_spellcasting_ability_mod()

        self.spell_attack_bonus = self.spellcasting_ability_mod + self.proficiency_bonus

        self.spell_save_DC = 8 + self.spellcasting_ability_mod + self.proficiency_bonus
        
        self.spell_slots = self.compute_spell_slots()[self.level - 1]
        self.available_spell_slots = self.spell_slots

        self.speed = self.compute_speed()

        self.sorcerer_points = 0
        self.spell_book = []

        self.inventory = []
        self.equipment = []
        self.class_features = []
        self.race_traits = []
        self.conditions = []

        self.saving_throw_proficiency = self.compute_saving_throw_proficiency()
    
        self.spellcasting_ability_mod = self.compute_spellcasting_ability_mod()

        if self.race == 'Barbarian':
            self.rage_num = self.compute_rage_num()[self.level - 1]
            self.rage_num_remaining = self.rage_num
            self.rage_damage = self.compute_rage_damage()[self.level - 1]

    def set_proficiency_bonus(self, new_bonus):
        delta = new_bonus - self.proficiency_bonus
        self.proficiency_bonus += delta
        self.spell_attack_bonus += delta
        self.spell_save_DC += delta
        for skill_name in self.skills.keys():
            if skill_name in self.skill_proficiencies:
                self.skills[skill_name] += delta

    def set_skill_proficiencies(self, new_skill_proficiencies):
        old_bonus = self.set_proficiency_bonus(0)
        self.skill_proficiencies = new_skill_proficiencies
        self.set_proficiency_bonus(old_bonus)

    def set_spellcasting_ability_mod(self, new):
        delta = new - self.spellcasting_ability_mod
        self.spell_attack_bonus += delta
        self.spell_save_DC += delta
    
    def set_ability_score(self, name, value):
        self.ability_scores[name] = value
        old_mod = self.ability_modifiers[name]
        self.ability_modifiers[name] = self.compute_modifier(value)
        delta = self.ability_scores[name] - old_mod

        if name == self.compute_spellcasting_ability_mod():
            self.set_spellcasting_ability_mod(self.spellcasting_ability_mod + delta)

        if name == 'STR':
            self.skills['athletics'] += delta
        elif name == 'DEX':
            self.skills['acrobatics'] += delta
            self.skills['sleight_of_hand'] += delta
            self.skills['stealth'] += delta

            self.AC += delta
        elif name == 'CON':
            pass
        elif name == 'INT':
            self.skills['arcana'] += delta
            self.skills['history'] += delta
            self.skills['investigation'] += delta
            self.skills['nature'] += delta
            self.skills['religion'] += delta
        elif name == 'WIS':
            self.skills['animal_handling'] += delta
            self.skills['insight'] += delta
            self.skills['medicine'] += delta
            self.skills['perception'] += delta
            self.skills['survival'] += delta
        elif name == 'CHA':
            self.skills['deception'] += delta
            self.skills['intimidation'] += delta
            self.skills['performance'] += delta
            self.skills['persuasion'] += delta

    def use_spell_slot(self, level, amount):
        self.available_spell_slots[level-1] -= amount

    def gain_spell_slot(self, level, amount):
        self.available_spell_slots[level-1] += amount
        
    def use_sorcery_points(self, level, amount):
        self.available_spell_slots[level-1] -= amount

    def gain_sorcery_points(self, level, amount):
        self.available_spell_slots[level-1] += amount

    def give_XP(self, amount):
        self.XP += amount

        self.XP_table = [
            0,  # Level 1
            300,  # Level 2
            900,  # Level 3
            2700,  # Level 4
            6500,  # Level 5
            14000,  # Level 6
            23000,  # Level 7
            34000,  # Level 8
            48000,  # Level 9
            64000,  # Level 10
            85000,  # Level 11
            100000,  # Level 12
            120000,  # Level 13
            140000,  # Level 14
            165000,  # Level 15
            195000,  # Level 16
            225000,  # Level 17
            265000,  # Level 18
            305000,  # Level 19
            355000  # Level 20
        ]
        self.XP_table = [int(xp / self.level_speed) for xp in self.XP_table]        

        if self.XP >= self.XP_table[self.level]:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.maxHP += int(self.hit_dice[1:])//2 + self.CONmod + (1 if self.race == 'Dwarf' else 0)

    def rest(self):
        self.HP = self.maxHP
        self.available_spell_slots = self.spell_slots
        self.rage_num_remaining = self.rage_num
    
    def add_equipment(self, name, description):
        self.equipment.append({'name': name, 'description': description})

    def modify_equipment(self, name, new_description):
        index = next(i for (i, item) in enumerate(self.equipment) if item["name"] == name)
        self.equipment[index]['description'] = new_description

    def remove_equipment(self, name):
        self.equipment.pop(next(i for (i, item) in enumerate(self.equipment) if item["name"] == name))
    
    def add_inventory(self, name, description):
        self.inventory.append({'name': name, 'description': description})

    def modify_inventory(self, name, new_description):
        index = next(i for (i, item) in enumerate(self.equipment) if item["name"] == name)
        self.inventory[index]['description'] = new_description
        
    def remove_inventory(self, name):
        self.inventory.pop(next(i for (i, item) in enumerate(self.equipment) if item["name"] == name))
                
    def compute_modifier(self, stat):
        return (stat - 10) // 2
    
    def compute_proficiency_bonus(self, level):
        return 2 + (level - 1) // 4

    def compute_hit_dice(self):
        if self.character_class in ['Barbarian']:
            return 'd12'
        elif self.character_class in ['Fighter', 'Paladin', 'Ranger']:
            return 'd10'
        elif self.character_class in ['Bard', 'Cleric', 'Druid', 'Rogue']:
            return 'd8'
        elif self.character_class in ['Sorcerer', 'Wizard']:
            return 'd6'
        else:
            return 'd8'
        
    def compute_spellcasting_ability_mod(self):
        if self.character_class in ['Bard', 'Sorcerer']:
            return 'CHA'
        elif self.character_class in ['Cleric', 'Druid', 'Ranger']:
            return 'WIS'
        elif self.character_class in ['Paladin']:
            return 'CHA'
        elif self.character_class in ['Wizard']:
            return 'INT'
        else:
            return 'STR'
        
    def compute_saving_throw_proficiency(self):
        if self.character_class in ['Barbarian']:
            return ['STR', 'CON']
        elif self.character_class in ['Bard']:
            return ['DEX', 'CHA']
        elif self.character_class in ['Cleric']:
            return ['WIS', 'CHA']
        elif self.character_class in ['Druid']:
            return ['INT', 'WIS']
        elif self.character_class in ['Fighter']:
            return ['STR', 'CON']
        elif self.character_class in ['Paladin']:
            return ['WIS', 'CHA']
        elif self.character_class in ['Ranger']:
            return ['STR', 'DEX']
        elif self.character_class in ['Rogue']:
            return ['DEX', 'INT']
        elif self.character_class in ['Sorcerer']:
            return ['CON', 'CHA']
        elif self.character_class in ['Wizard']:
            return ['INT', 'WIS']
        else:
            return ['STR, CON']

    def compute_spell_slots(self):

        if self.character_class in ['Barbarian', 'Fighter', 'Rogue']:
            return [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 1
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 2
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 3
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 4
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 6
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 7
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 10
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 11
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 12
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 13
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 14
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 16
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 17
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 18
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 19
            [0, 0, 0, 0, 0, 0, 0, 0, 0]   # Level 20
        ]
        elif self.character_class in ['Bard', 'Cleric', 'Druid', 'Sorcerer']:
            return [
            [2, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 1
            [3, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 2
            [4, 2, 0, 0, 0, 0, 0, 0, 0],  # Level 3
            [4, 3, 0, 0, 0, 0, 0, 0, 0],  # Level 4
            [4, 3, 2, 0, 0, 0, 0, 0, 0],  # Level 5
            [4, 3, 3, 0, 0, 0, 0, 0, 0],  # Level 6
            [4, 3, 3, 1, 0, 0, 0, 0, 0],  # Level 7
            [4, 3, 3, 2, 0, 0, 0, 0, 0],  # Level 8
            [4, 3, 3, 3, 1, 0, 0, 0, 0],  # Level 9
            [4, 3, 3, 3, 2, 0, 0, 0, 0],  # Level 10
            [4, 3, 3, 3, 2, 1, 0, 0, 0],  # Level 11
            [4, 3, 3, 3, 2, 1, 0, 0, 0],  # Level 12
            [4, 3, 3, 3, 2, 1, 1, 0, 0],  # Level 13
            [4, 3, 3, 3, 2, 1, 1, 0, 0],  # Level 14
            [4, 3, 3, 3, 2, 1, 1, 1, 0],  # Level 15
            [4, 3, 3, 3, 2, 1, 1, 1, 0],  # Level 16
            [4, 3, 3, 3, 2, 1, 1, 1, 1],  # Level 17
            [4, 3, 3, 3, 3, 1, 1, 1, 1],  # Level 18
            [4, 3, 3, 3, 3, 2, 1, 1, 1],  # Level 19
            [4, 3, 3, 3, 3, 2, 2, 1, 1]   # Level 20
        ]
        elif self.character_class in ['Paladin', 'Ranger']:
            return [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 1
                [2, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 2
                [3, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 3
                [3, 0, 0, 0, 0, 0, 0, 0, 0],  # Level 4
                [4, 2, 0, 0, 0, 0, 0, 0, 0],  # Level 5
                [4, 2, 0, 0, 0, 0, 0, 0, 0],  # Level 6
                [4, 3, 0, 0, 0, 0, 0, 0, 0],  # Level 7
                [4, 3, 0, 0, 0, 0, 0, 0, 0],  # Level 8
                [4, 3, 2, 0, 0, 0, 0, 0, 0],  # Level 9
                [4, 3, 2, 0, 0, 0, 0, 0, 0],  # Level 10
                [4, 3, 3, 0, 0, 0, 0, 0, 0],  # Level 11
                [4, 3, 3, 0, 0, 0, 0, 0, 0],  # Level 12
                [4, 3, 3, 1, 0, 0, 0, 0, 0],  # Level 13
                [4, 3, 3, 1, 0, 0, 0, 0, 0],  # Level 14
                [4, 3, 3, 2, 0, 0, 0, 0, 0],  # Level 15
                [4, 3, 3, 2, 0, 0, 0, 0, 0],  # Level 16
                [4, 3, 3, 3, 1, 0, 0, 0, 0],  # Level 17
                [4, 3, 3, 3, 1, 0, 0, 0, 0],  # Level 18
                [4, 3, 3, 3, 2, 0, 0, 0, 0],  # Level 19
                [4, 3, 3, 3, 2, 0, 0, 0, 0]   # Level 20
            ]
        elif self.character_class in ['Wizard']:
            return ['INT', 'WIS']
        else:
            return ['STR, CON']
    
    def activate_rage(self):
        self.rage_num_remaining -= 1
        self.conditions.append({'name': 'Rage', 
                                'description': 'Rage is active', 
                                'duration': {'days': 0, 'hours': 0, 'minutes': 1, 'seconds': 0}})

    def compute_rage_num(self):
        return [2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 100]
    
    def compute_rage_damage(self):
        return [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]

    def update_condition_timers(self, days, hours, minutes, seconds):
        for (i, condition) in enumerate(self.conditions):
            time = condition['duration']['seconds']
            time += condition['duration']['minutes'] * 60
            time += condition['duration']['hours'] * 60 * 60
            time += condition['duration']['days'] * 60 * 60 * 24

            time -= seconds
            time -= minutes * 60
            time -= hours * 60 * 60
            time -= days * 60 * 60 * 24

            if time > 0:
                condition['duration']['days'] = time // (60 * 60 * 24)
                time -= - self.condition['duration']['days'] * 60 * 60 * 24
                condition['duration']['hours'] = time // (60 * 60)
                time -= - self.condition['duration']['hours'] * 60 * 60
                condition['duration']['minutes'] = time // 60
                time -= - self.condition['duration']['minutes'] * 60
                condition['duration']['seconds'] = time
            elif time <= 0:
                self.conditions.pop(i)
            

    def strinigfy(self):
        nl = '\n'
        t = '\t'
        text = ''
        text += f'Name: {self.name} \t'
        text += f'Race: {self.race} \t'
        text += f'Class: {self.character_class} \t'
        text += f'Level: {str(self.level)} \n'

        text += f'STR: {str(self.ability_scores["STR"])} ({str(self.ability_modifiers["STR"]):+}), '
        text += f'DEX: {str(self.ability_scores["DEX"])} ({str(self.ability_modifiers["DEX"]):+}), '
        text += f'CON: {str(self.ability_scores["CON"])} ({str(self.ability_modifiers["CON"]):+}), '
        text += f'INT: {str(self.ability_scores["INT"])} ({str(self.ability_modifiers["INT"]):+}), '
        text += f'WIS: {str(self.ability_scores["WIS"])} ({str(self.ability_modifiers["WIS"]):+}), '
        text += f'CHA: {str(self.ability_scores["CHA"])} ({str(self.ability_modifiers["CHA"]):+}) \n'

        text += f'AC: {self.AC} \t'
        text += f'max HP: {self.maxHP} \t'
        text += f'current HP: {self.HP} \t'
        text += f'Speed: {str(self.speed)} \n'

        text += f'Saving throws: {", ".join(self.saving_throws)} \n'
        text += f'Proficency bonus: {str(self.proficiency_bonus)} \n'
        text += f'Skills: \n {nl.join([t + name + ": " + str(self.skills[name]) + ("(proficient)" if name in self.skill_proficiencies else "") for name in self.skills.keys()])}'
        
        text += f'Equipment: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.equipment])} \n'
        text += f'Inventory: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.inventory])} \n'
        
        text += f'Race traits: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.race_traits])} \n'
        text += f'Class features: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.features])} \n'

        text += '\n Spellcasting. \n'
        text += f'Spellcasting ability modifier: {str(self.spellcasting_ability_mod)} \t'
        text += f'Spell attack bonus: {str(self.spell_attack_bonus)} \t'
        text += f'Spell save DC: {str(self.spell_save_DC)} \n'
        text += f'Spell slots: {", ".join(["Level " + str(i) + ": " + str(self.available_spell_slots[i]) + "/" + str(val) for (i, val) in enumerate(self.spell_slots)])} \n'
        text += f'Spells: {", ".join([spell for spell in self.spells])} \n'