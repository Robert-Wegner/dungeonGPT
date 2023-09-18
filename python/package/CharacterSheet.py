import os
import sys
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from data.character.feats import feats as FEATS
from data.character.race_traits import elf_race_traits as ELF_RACE_TRAITS
from data.character.race_traits import dwarf_race_traits as DWARF_RACE_TRAITS
from data.character.race_traits import halfling_race_traits as HALFLING_RACE_TRAITS
from data.character.race_traits import human_race_traits as HUMAN_RACE_TRAITS
from data.character.race_traits import dragonborn_race_traits as DRAGONBORN_RACE_TRAITS
from data.character.race_traits import gnome_race_traits as GNOME_RACE_TRAITS
from data.character.race_traits import halfelf_race_traits as HALFELF_RACE_TRAITS
from data.character.race_traits import halforc_race_traits as HALFORC_RACE_TRAITS
from data.character.race_traits import tiefling_race_traits as TIEFLING_RACE_TRAITS
from data.character.class_features import cleric_class_features as CLERIC_CLASS_FEATURES
from data.character.class_features import barbarian_class_features as BARBARIAN_CLASS_FEATURES
from data.character.class_features import bard_class_features as BARD_CLASS_FEATURES
from data.character.class_features import druid_class_features as DRUID_CLASS_FEATURES
from data.character.class_features import fighter_class_features as FIGHTER_CLASS_FEATURES
from data.character.class_features import paladin_class_features as PALADIN_CLASS_FEATURES
from data.character.class_features import ranger_class_features as RANGER_CLASS_FEATURES
from data.character.class_features import rogue_class_features as ROGUE_CLASS_FEATURES
from data.character.class_features import sorcerer_class_features as SORCERER_CLASS_FEATURES
from data.character.class_features import wizard_class_features as WIZARD_CLASS_FEATURES
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

def get_file_path(file_path):
    file_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    new_path = os.path.join(file_dir, file_path)
    return os.path.abspath(os.path.realpath(new_path))

with open(get_file_path("data/spells.p"), "rb") as f:
    spell_dictionary = pickle.load(f)


class CharacterSheet:
 
    def __init__(self, name, race, character_class, first_skill_proficiency, second_skill_proficiency, #choose 2, options depending on class
                    STR, DEX, CON, INT, WIS, CHA):
 
        self.log = []
        self.logging = False
 
        self.name = name
        self.race = race
        self.character_class = character_class
        print("------------CHARCLASS: ", self.character_class)
        self.level = 1
        self.level_speed = 5
        self.level_up_state = "none" #none, normal or special
        self.level_up_message = ''
 
        self.XP = 0
        self.XP_table = self.compute_XP_table()
        self.AC = 10
 
        self.ability_scores = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'INT': 0,
            'WIS': 0,
            'CHA': 0
        }
        self.ability_modifiers = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'INT': 0,
            'WIS': 0,
            'CHA': 0
        }
        self.ability_scores_race_bonus = {
            'STR': 0,
            'DEX': 0,
            'CON': 0,
            'INT': 0,
            'WIS': 0,
            'CHA': 0
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
            'Acrobatics': 0,
            'Animal Handling': 0,
            'Arcana': 0,
            'Athletics': 0,
            'Deception': 0,
            'History': 0,
            'Insight': 0,
            'Intimidation': 0,
            'Investigation': 0,
            'Medicine': 0,
            'Nature': 0,
            'Perception': 0,
            'Performance': 0,
            'Persuasion': 0,
            'Religion': 0,
            'Sleight of Hand': 0,
            'Stealth': 0,
            'Survival': 0
        }
 
        self.proficiency_bonus = 0
 
        self.spellcasting_ability = self.compute_spellcasting_ability()
        self.spellcasting_ability_mod = 0
        self.spell_attack_bonus = 0
        self.spell_save_DC = 8 
 
 
        self.set_ability_score('STR', STR + self.ability_scores_race_bonus['STR'])
        self.set_ability_score('DEX', DEX + self.ability_scores_race_bonus['DEX'])
        self.set_ability_score('CON', CON + self.ability_scores_race_bonus['CON'])
        self.set_ability_score('INT', INT + self.ability_scores_race_bonus['INT'])
        self.set_ability_score('WIS', WIS + self.ability_scores_race_bonus['WIS'])
        self.set_ability_score('CHA', CHA + self.ability_scores_race_bonus['CHA'])
 
        self.proficiency_bonus = 0
        self.skill_proficiencies = []
        self.set_proficiency_bonus(self.compute_proficiency_bonus())
        self.set_skill_proficiencies([first_skill_proficiency, second_skill_proficiency])
 
 
        self.hit_dice = self.compute_hit_dice()
 
        self.max_HP = int(self.hit_dice[1:]) + (1 if self.race == 'Dwarf' else 0)
 
        self.HP = self.max_HP
 
 
        self.max_spell_slots = self.compute_max_spell_slots()
        self.spell_slots = self.max_spell_slots
 
        self.max_sorcery_points = self.compute_max_sorcery_points()
        self.sorcery_points = self.max_sorcery_points
 
        self.race_traits = self.compute_race_traits()
        self.class_features = self.compute_class_features()

        self.features = [feature for feature in self.class_features if feature['level'] == 1]

        self.inventory = []
        self.equipment = []
        self.conditions = []
        self.spells = []
        self.saving_throw_proficiencies = self.compute_saving_throw_proficiencies()

        self.max_rages = self.compute_max_rages()
        self.rages = self.max_rages
        self.rage_damage = self.compute_rage_damage()

        self.max_wild_shape_num = self.compute_wild_shape_num()
        self.wild_shape_num = self.max_wild_shape_num

        self.logging = True

        self.log.append(f'The character has been created!\n{self.print()}\n')

        self.errors = []

    def clear_log(self):
        self.log = []
 
    def print_log(self):
        return '\n'.join(self.log)
 
    def set_spell_attack_bonus(self, new_bonus):
        if self.logging and self.spell_attack_bonus != new_bonus:
            self.log.append(f'Spell attack bonus: {self.spell_attack_bonus} -> {new_bonus}')
 
        self.spell_attack_bonus = new_bonus
 
    def set_spell_save_DC(self, new_DC):
        if self.logging and self.spell_save_DC != new_DC:
            self.log.append(f'Spell save DC: {self.spell_save_DC} -> {new_DC}')
 
        self.spell_save_DC = new_DC
 
    def set_proficiency_bonus(self, new_bonus):
        if self.logging and self.proficiency_bonus != new_bonus:
            self.log.append(f'Proficiency Bonus: {self.proficiency_bonus} -> {new_bonus}')
 
        delta = new_bonus - self.proficiency_bonus
        self.proficiency_bonus += delta
        self.set_spell_attack_bonus(self.spell_attack_bonus + delta)
        self.set_spell_save_DC(self.spell_save_DC + delta)
        for skill_name in self.skill_proficiencies:
            self.set_skill_bonus(skill_name, self.skills[skill_name] + delta)
 
    def set_skill_bonus(self, skill_name, new_bonus):
        skill_name = skill_name.capitalize()
        if self.logging and self.skills[skill_name] != new_bonus:
                self.log.append(f'{skill_name}: {self.skills[skill_name]} -> {new_bonus}')
 
        self.skills[skill_name] = new_bonus
 
    def set_skill_proficiencies(self, new_skill_proficiencies):
        new_skill_proficiencies = [entry.capitalize() for entry in new_skill_proficiencies]
 
        if self.logging and self.skill_proficiencies != new_skill_proficiencies:
            self.log.append(f'Skill proficiencies: {", ".join(self.skill_proficiencies)} -> {", ".join(new_skill_proficiencies)}')
        old_logging = self.logging
        self.logging = False
        old_bonus = self.proficiency_bonus
        self.set_proficiency_bonus(0)
        self.skill_proficiencies = new_skill_proficiencies
        if old_logging:
            self.logging = True
        self.set_proficiency_bonus(old_bonus)
 
    def add_skill_proficiency(self, skill_name):
        if skill_name not in self.skill_proficiencies:
            self.set_skill_proficiencies(self.skill_proficiencies.copy().append(skill_name))

    def remove_skill_proficiency(self, skill_name):
        if skill_name in self.skill_proficiencies:
            self.set_skill_proficiencies(self.skill_proficiencies.copy().remove(skill_name))
 
    def set_spellcasting_ability_mod(self, new):
        if self.logging and self.spellcasting_ability_mod != new:
            self.log.append(f'Spellcasting ability modifier: {self.spellcasting_ability_mod} -> {new}')
        delta = new - self.spellcasting_ability_mod
        self.spellcasting_ability_mod += delta
        self.set_spell_attack_bonus(self.spell_attack_bonus + delta)
        self.set_spell_save_DC(self.spell_save_DC + delta)
 
    def set_AC(self, new_AC):
        if self.logging and self.AC != new_AC:
            self.log.append(f'AC: {self.AC} -> {new_AC}')
        self.AC = new_AC
 
    def set_max_HP(self, new_max_HP):
        if self.logging and self.max_HP != new_max_HP:
            self.log.append(f'max HP: {self.max_HP} -> {new_max_HP}')
        self.max_HP = new_max_HP
 
    def set_HP(self, new_HP):
        if self.logging and self.HP != new_HP:
            self.log.append(f'HP: {self.HP} -> {new_HP}')
        self.HP = new_HP
 
    def set_ability_score(self, name, value):
        if self.logging and self.ability_scores[name] != value:
            self.log.append(f'{name}: {self.ability_scores[name]} -> {value}')
 
        delta_score = value - self.ability_scores[name]
        self.ability_scores[name] += delta_score
        old_mod = self.ability_modifiers[name]
        self.ability_modifiers[name] = self.compute_modifier(self.ability_scores[name])
 
        if self.logging and self.ability_modifiers[name] != old_mod:
            self.log.append(f'{name}mod: {old_mod} -> {self.ability_modifiers[name]}')
 
        delta_mod = self.ability_modifiers[name] - old_mod
 
        if name == self.spellcasting_ability:
            self.set_spellcasting_ability_mod(self.spellcasting_ability_mod + delta_mod)
 
        if name == 'STR':
            self.set_skill_bonus('Athletics', self.skills['Athletics'] + delta_mod)
        elif name == 'DEX':
            self.set_skill_bonus('Acrobatics', self.skills['Acrobatics'] + delta_mod)
            self.set_skill_bonus('Sleight of Hand', self.skills['Sleight of Hand'] + delta_mod)
            self.set_skill_bonus('Stealth', self.skills['Stealth'] + delta_mod)
 
            self.set_AC(self.AC + delta_mod)
        elif name == 'CON':
            pass
        elif name == 'INT':
            self.set_skill_bonus('Arcana', self.skills['Arcana'] + delta_mod)
            self.set_skill_bonus('History', self.skills['History'] + delta_mod)
            self.set_skill_bonus('Investigation', self.skills['Investigation'] + delta_mod)
            self.set_skill_bonus('Nature', self.skills['Nature'] + delta_mod)
            self.set_skill_bonus('Religion', self.skills['Religion'] + delta_mod)
        elif name == 'WIS':
            self.set_skill_bonus('Animal Handling', self.skills['Animal Handling'] + delta_mod)
            self.set_skill_bonus('Insight', self.skills['Insight'] + delta_mod)
            self.set_skill_bonus('Medicine', self.skills['Medicine'] + delta_mod)
            self.set_skill_bonus('Perception', self.skills['Perception'] + delta_mod)
            self.set_skill_bonus('Survival', self.skills['Survival'] + delta_mod)
        elif name == 'CHA':
            self.set_skill_bonus('Deception', self.skills['Deception'] + delta_mod)
            self.set_skill_bonus('Intimidation', self.skills['Intimidation'] + delta_mod)
            self.set_skill_bonus('Performance', self.skills['Performance'] + delta_mod)
            self.set_skill_bonus('Persuasion', self.skills['Persuasion'] + delta_mod)
 
    def use_spell_slots(self, level, amount):
        if self.logging and amount > 0:
            self.log.append(f'Available level {level} spell slots: {self.spell_slots[level-1]} -> {self.spell_slots[level-1] - amount}')
        self.spell_slots[level-1] -= amount
    def gain_spell_slots(self, level, amount):
        if self.logging and amount > 0:
            self.log.append(f'Available level {level} spell slots: {self.spell_slots[level-1]} -> {self.spell_slots[level-1] + amount}')
        self.spell_slots[level-1] += amount
    def set_spell_slots(self, new_spell_slots):
        for (i, slots) in enumerate(self.spell_slots):
            self.gain_spell_slots(i+1, new_spell_slots[i] - slots)
 
    def gain_max_spell_slots(self, level, amount):
        if self.logging and amount > 0:
            self.log.append(f'Level {level} spell slots: {self.max_spell_slots[level-1]} -> {self.max_spell_slots[level-1] + amount}')
        self.max_spell_slots[level-1] += amount
    def set_max_spell_slots(self, new_max_spell_slots):
        for (i, slots) in enumerate(self.max_spell_slots):
            self.gain_max_spell_slots(i+1, new_max_spell_slots[i] - slots)
 
    def set_max_sorcery_points(self, amount):
        if self.logging and self.max_sorcery_points != amount:
            self.log.append(f'Sorcery points: {self.max_sorcery_points} -> {amount}')
        self.max_sorcery_points = amount
    def set_sorcery_points(self, amount):
        if self.logging and self.sorcery_points != amount:
            self.log.append(f'Sorcery points: {self.sorcery_points} -> {amount}')
        self.sorcery_points = amount
    def use_sorcery_points(self, amount):
        self.set_sorcery_points(self.sorcery_points - amount)
    def gain_sorcery_points(self, amount):
        self.set_sorcery_points(self.sorcery_points + amount)
 
 
    def create_spell_slot_from_sorcery_points(self, level):
        if self.logging:
            self.log.append(f'Converting sorcery points to spell slot of level {level}')
 
        if self.level == 1:
            self.use_sorcery_points(2)
        elif self.level == 2:
            self.use_sorcery_points(3)
        elif self.level == 3:
            self.use_sorcery_points(5)
        elif self.level == 4:
            self.use_sorcery_points(6)
        elif self.level == 5:
            self.use_sorcery_points(7)
 
        self.gain_max_spell_slots(level, 1)
 
    def create_sorcery_points_from_spell_slot(self, level):
        if self.logging:
            self.log.append(f'Converting spell slot of level {level} to sorcery points')
 
        if self.level == 1:
            self.gain_sorcery_points(1)
        elif self.level == 2:
            self.gain_sorcery_points(2)
        elif self.level == 3:
            self.gain_sorcery_points(3)
        elif self.level == 4:
            self.gain_sorcery_points(4)
        elif self.level == 5:
            self.gain_sorcery_points(5)
 
        self.use_max_spell_slots(level, 1)
 
    def activate_rage(self):
        self.set_rages(self.rages, self.rages - 1)
        self.add_condition('Rage', 'Rage is active', 0, 0, 0, 0)
 
    def set_max_rages(self, amount):
        if self.logging and self.max_rages != amount:
            self.log.append(f'Max rages: {self.max_rages} -> {amount}')
        self.max_rages = amount

    def set_rages(self, amount):
        if self.logging and self.rages != amount:
            self.log.append(f'Rages: {self.rages} -> {amount}')
        self.rages = amount
 
    def set_rage_damage(self, new_damage):
        if self.logging and self.rage_damage != new_damage:
            self.log.append(f'Rage damage: {self.rage_damage} -> {new_damage}')
        self.rage_damage = new_damage
 
    def add_condition(self, name, description, duration_days, duration_hours, duration_minutes, duration_seconds):
        duration = {'days': duration_days,
                    'hours': duration_hours,
                    'minutes': duration_minutes,
                    'seconds': duration_seconds}
        if self.logging:
            self.log.append(f'Added condition: {name} with duration {self.duration_to_string(duration)}')
        self.conditions.append({'name': name, 
                                'description': description, 
                                'duration': duration})
 
    def remove_condition(self, name):
        if self.logging:
            self.log.append(f'Removed condition: {name}')
        for (i, condition) in enumerate(self.conditions):
            if condition['name'] == name:
                self.conditions.pop(i)
 
    def add_inventory_item(self, name, description):
        if self.logging:
            self.log.append(f'Added inventory item: {name}')
        self.inventory.push({'name': name,
                             'description': description})
 
    def remove_inventory_item(self, name):
        if self.logging:
            self.log.append(f'Removed inventory item: {name}')
        for (i, item) in enumerate(self.inventory):
            if item['name'] == name:
                self.inventory.pop(i)
 
    def modify_inventory_item(self, name, description):
        if self.logging:
            self.log.append(f'Modified inventory item: {name}')
        for (i, item) in enumerate(self.inventory):
            if item['name'] == name:
                item['description'] = description
 
    def add_equipment_item(self, name, description):
        if self.logging:
            self.log.append(f'Added equipment item: {name}')
        self.equipment.append({'name': name,
                             'description': description})
 
    def remove_equipment_item(self, name):
        if self.logging:
            self.log.append(f'Removed equipment item: {name}')
        for (i, item) in enumerate(self.equipment):
            if item['name'] == name:
                self.equipment.pop(i)
 
    def modify_equipment_item(self, name, description):
        if self.logging:
            self.log.append(f'Modified equipment item: {name}')
        for (i, item) in enumerate(self.equipment):
            if item['name'] == name:
                item['description'] = description
 
    def activate_wild_shape(self, beast_name):
        self.set_wild_shape_num(self.wild_shape_num - 1)
        self.add_condition('Wild Shape', f'Transformed into a {beast_name}', 0, self.level // 2, 0, 0)

    def deactivate_wild_shape(self):
        self.remove_condition('Wild Shape')

    def set_max_wild_shape_num(self, amount):
        if self.logging and self.max_wild_shape_num != amount:
            self.log.append(f'Max Wild shapes: {self.max_wild_shape_num} -> {amount}')
        self.max_wild_shape_num = amount

    def set_wild_shape_num(self, amount):
        if self.logging and self.wild_shape_num != amount:
            self.log.append(f'Wild Shapes: {self.wild_shape_num} -> {amount}')
        self.wild_shape_num = amount
 
    def add_spell(self, spell_name, spell_level, spell_description):
        if self.logging and not any(spell['name'] == spell_name for spell in self.spells):
            self.log.append(f'Added spell: {spell_name}')
        self.spells.append({'name': spell_name,
                            'level': spell_level,
                            'description': spell_description})
        
    def remove_spell(self, spell_name):
        if self.logging and any(spell['name'] == spell_name for spell in self.spells):
            self.log.append(f'Removed spell: {spell_name}')
        self.spells = [spell for spell in self.spells if spell['name'] != spell_name]

    def award_XP(self, amount):
        if self.logging and amount > 0:
            self.log.append(f'XP: {self.XP} -> {self.XP + amount}')
        self.XP += amount
 
        self.XP_table = [int(xp / self.level_speed) for xp in self.XP_table]        
 
        if self.XP >= self.XP_table[self.level]:
            self.prepare_level_up()
 
    def prepare_level_up(self):
        if self.level < 20:
            if self.logging:
                self.log.append('Level up is ready')
            self.level_up_message = 'You can level up!'
            special_levels = self.compute_special_levels()
            if self.level+1 in special_levels:
                self.level_up_message += 'You can either increase two ability scores by 1 or choose a feat.'
                self.level_up_state = "special"
            else:
                self.level_up_state = "normal"

    def level_up(self):
        if self.level < 20:
            if self.logging:
                self.log.append(f'Level: {self.level} -> {self.level+1}')
            self.level += 1
            self.set_max_HP(self.max_HP + int(self.hit_dice[1:])//2 + self.ability_modifiers['CON'] + (1 if self.race == 'Dwarf' else 0))
            self.set_proficiency_bonus(self.compute_proficiency_bonus())
            self.set_max_spell_slots(self.compute_max_spell_slots())
            self.set_max_sorcery_points(self.compute_max_sorcery_points())
            self.set_rage_damage(self.compute_rage_damage())
            self.set_max_rages(self.compute_max_rages())
            for feature in self.class_features:
                if feature['level'] == self.level:
                    self.add_feature(feature['name'], feature['description'])
 
            new_spells = self.compute_spells(self.level)
            for spell in new_spells:
                if spell['name'] not in self.spells:
                    self.add_spell(spell['name'], spell['level'], spell['description'])
        
        self.level_up_state = "none"

    def level_up_with_ability_score_improvement(self, first_ability_name, second_ability_name):
        self.set_ability_score(first_ability_name, self.ability_scores[first_ability_name] + 1)
        self.set_ability_score(second_ability_name, self.ability_scores[second_ability_name] + 1)
        self.level_up()
 
    def level_up_with_feat(self, feat_name):
        self.add_feat(feat_name)
        self.level_up()
 
    def add_feat(self, feat_name):
        for feat in self.compute_feats():
            if feat['name'] == feat_name:
                self.add_feature(feat['name'], feat['description'])
 
    def add_feature(self, feature_name, description):
        if self.logging:
            self.log.append(f'Adding feature: {feature_name}')
        self.features.append({'name': feature_name, 'description': description})
 
    def remove_feature(self, feature_name):
        if self.logging:
            self.log.append(f'Removing feature: {feature_name}')
        for (i, feature) in enumerate(self.features):
            if feature['name'] == feature_name:
                self.features.pop(i)
 
    def rest(self):
        self.set_HP(self.max_HP)
        self.set_spell_slots(self.max_spell_slots)
        self.set_rages(self.max_rages)
        self.set_sorcery_points(self.max_sorcery_points)
        self.set_wild_shape_num(self.max_wild_shape_num)
 
 
    def print(self, feature_descriptions=True, item_descriptions=True, spell_descriptions=False):
        nl = '\n'
        t = '      '
        text = ''
        text += f'Name: {self.name}{t}'
        text += f'Race: {self.race}{t}'
        text += f'Class: {self.character_class}{t}'
        text += f'Level: {self.level}{t}'
        text += f'XP: {self.XP}/{self.XP_table[self.level+1]} \n'
 
        text += self.level_up_message + '\n' if self.level_up_state else ''
        if self.level_up_state != "none":
            text += 'You can level up! '
        if self.level_up_state == "special":
            text += 'You can either increase two ability scores by 1 or choose a feat. \n'

        text += f'STR: {self.ability_scores["STR"]} ({self.ability_modifiers["STR"]:+}), '
        text += f'DEX: {self.ability_scores["DEX"]} ({self.ability_modifiers["DEX"]:+}), '
        text += f'CON: {self.ability_scores["CON"]} ({self.ability_modifiers["CON"]:+}), '
        text += f'INT: {self.ability_scores["INT"]} ({self.ability_modifiers["INT"]:+}), '
        text += f'WIS: {self.ability_scores["WIS"]} ({self.ability_modifiers["WIS"]:+}), '
        text += f'CHA: {self.ability_scores["CHA"]} ({self.ability_modifiers["CHA"]:+}) \n'
 
        text += f'AC: {self.AC}{t}'
        text += f'max HP: {self.max_HP}{t}'
        text += f'current HP: {self.HP}{t}'
 
        text += f'Saving throws: {", ".join(self.saving_throw_proficiencies)} \n'
        text += f'Proficency bonus: {self.proficiency_bonus} \n'
        text += f'Skills: \n{nl.join([t + name + ": " + str(self.skills[name]) + (" (proficient)" if name in self.skill_proficiencies else "") for name in self.skills.keys()])} \n'
 
        if item_descriptions:
            text += f'Equipment: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.equipment])} \n'
            text += f'Inventory: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.inventory])} \n'
        else:
            text += f'Equipment: \n{", ".join([t + item["name"] for item in self.equipment])}'
            text += f'Equipment: \n{", ".join([t + item["name"] for item in self.inventory])}'
        print("------------SOFAR: ")
        from pprint import pprint
        print(self.features)
        print(self.class_features)
        if feature_descriptions:
            text += f'Race traits: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.race_traits])} \n'
            text += f'Features: \n {nl.join([t + item["name"] + ": " + item["description"] for item in self.features])} \n'
        else:
            text += f'Race traits: \n {", ".join([t + item["name"] for item in self.race_traits])} \n'
            text += f'Features: \n {", ".join([t + item["name"] for item in self.features])} \n'
        print("------------POST: ")

        text += f'Conditions: \n {nl.join([t + condition["name"] + ": " + condition["description"] + " (Duration: " + self.duration_to_string(condition["duration"]) + ")" for condition in self.conditions])} \n'

        text += 'Spellcasting. \n'
        text += f'Spellcasting ability: {self.spellcasting_ability}{t}'
        text += f'Spellcasting ability modifier: {self.spellcasting_ability_mod}{t}'
        text += f'Spell attack bonus: {self.spell_attack_bonus}{t}'
        text += f'Spell save DC: {self.spell_save_DC} \n'
        text += f'Spell slots: {", ".join(["Level " + str(i+1) + ": " + str(self.spell_slots[i]) + "/" + str(val) for (i, val) in enumerate(self.max_spell_slots)])} \n'

        if spell_descriptions: 
            text += f'{"Spells" if self.character_class != "Wizard" else "Spellbook"}: {nl.join([spell["name"] + ": " + spell["description"] for spell in self.spells])} \n'
        else:
            text += f'{"Spells" if self.character_class != "Wizard" else "Spellbook"}: {", ".join([spell["name"] for spell in self.spells])} \n'

        if self.character_class == 'Sorcerer':
            text += f'Sorcery points: {self.sorcery_points}/{self.max_sorcery_points} \n'
 
        if self.character_class == 'Barbarian':
            text += f'Rages: {self.rages}/{self.max_rages}{t}'
            text += f'Rage damage: {self.rage_damage} \n'
 
        if self.character_class == 'Druid':
            text += f'Wild Shapes: {self.wild_shape_num}/2'
 
        return text
 
    def compute_modifier(self, stat):
        return (stat - 10) // 2
 
    def compute_proficiency_bonus(self):
        return 2 + (self.level - 1) // 4
 
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
 
    def compute_spellcasting_ability(self):
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
 
    def compute_saving_throw_proficiencies(self):
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
 
    def compute_max_spell_slots(self):
 
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
        ][self.level - 1]
        elif self.character_class in ['Bard', 'Cleric', 'Druid', 'Sorcerer', 'Wizard']:
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
        ][self.level - 1]
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
            ][self.level - 1]
 
 
    def compute_max_sorcery_points(self):
        if self.character_class == 'Sorcerer':
            return self.level if self.level > 1 else 0
        else:
            return 0
 
    def compute_max_rages(self):
        if self.character_class == 'Barbarian':
            return [2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 100][self.level - 1]
        else:
            return 0
 
    def compute_rage_damage(self):
        if self.character_class == 'Barbarian':
            return [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4][self.level - 1]
        else:
            return 0
 
    def compute_wild_shape_num(self):
        if self.character_class == 'Druid':
            return 2
        else:
            return 0
 
    def compute_special_levels(self):
        if self.character_class in ['Fighter']:
            return [4, 6, 8, 12, 14, 16, 19]
        elif self.character_class in ['Paladin', 'Ranger', 'Rogue', 'Wizard' 'Bard', 'Cleric', 'Druid', 'Sorcerer', 'Barbarian']:
            return [4, 8, 12, 16, 19]
 
    def compute_feats(self):
        return FEATS
    
    def compute_race_traits(self):
        if self.race == 'Elf':
            return ELF_RACE_TRAITS
        elif self.race == 'Dwarf':
            return DWARF_RACE_TRAITS
        elif self.race == 'Halfling':
            return HALFLING_RACE_TRAITS
        elif self.race == 'Human':
            return HUMAN_RACE_TRAITS
        elif self.race == 'Dragonborn':
            return DRAGONBORN_RACE_TRAITS
        elif self.race == 'Gnome':
            return GNOME_RACE_TRAITS
        elif self.race == 'Half-Elf':
            return HALFELF_RACE_TRAITS
        elif self.race == 'Half-Orc':
            return HALFORC_RACE_TRAITS
        elif self.race == 'Tiefling':
            return TIEFLING_RACE_TRAITS
        else:
            return []
 
    def compute_class_features(self):
        if self.character_class == 'Barbarian':
            return BARBARIAN_CLASS_FEATURES
        elif self.character_class == 'Bard':
            return BARD_CLASS_FEATURES
        elif self.character_class == 'Cleric':
            return CLERIC_CLASS_FEATURES
        elif self.character_class == 'Druid':
            return DRUID_CLASS_FEATURES
        elif self.character_class == 'Fighter':
            return FIGHTER_CLASS_FEATURES
        elif self.character_class == 'Paladin':
            return PALADIN_CLASS_FEATURES
        elif self.character_class == 'Ranger':
            return RANGER_CLASS_FEATURES
        elif self.character_class == 'Rogue':
            return ROGUE_CLASS_FEATURES
        elif self.character_class == 'Sorcerer':
            return SORCERER_CLASS_FEATURES
        elif self.character_class == 'Wizard':
            return WIZARD_CLASS_FEATURES
        else:
            return []
 
    def compute_XP_table(self):
        return [
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
            355000,  # Level 20
            99999999,
            99999999
        ]

    def compute_spells(self, spell_level):
        return [spell for spell in spell_dictionary if spell['level'] == spell_level and self.character_class in spell['classes']]
 
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
                self.remove_condition(condition['name'])
 
    def duration_to_string(self, duration):
        return f'{duration["days"]}d {duration["hours"]}h {duration["minutes"]}m {duration["seconds"]}s'
 

        
        
#char = CharacterSheet("Adric", "Dwarf", "Druid", "investigation", "intimidation", 10, 11, 12, 13, 14, 15)
 

#print(char.print())


class DisplayedCharacterSheet(CharacterSheet):

    def __init__(self):
        super()
        