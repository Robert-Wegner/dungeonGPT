import os
import pickle
import pandas as pd
import openai
from openai.embeddings_utils import cosine_similarity
from fractions import Fraction
import pprint

def get_file_path(file_path):
    file_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    new_path = os.path.join(file_dir, file_path)
    return os.path.abspath(os.path.realpath(new_path))

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

class Dictionary:

    def __init__(self):
        self.spells = []
        self.monsters = []
        self.magic_items = []
        self.places = [{"name": "Example place", "description": "Somewhere, just as an example"}]
        self.characters = [{"name": "Example character", "description": "Someone, just as an example"}]
        self.other = [{"name": "Example place", "description": "Something, just as an example"}]
        self.weapons = [
            {"name": "Club", "cost": "1 sp", "damage": "1d4 B", "weight": "2 lb.", "properties": ""},
            {"name": "Dagger", "cost": "2 gp", "damage": "1d4 P", "weight": "1 lb.", "properties": "Finesse Weapon, Thrown Rg(20/60)"},
            {"name": "Greatclub", "cost": "2 sp", "damage": "1d8 B", "weight": "10 lb.", "properties": "Two Handed"},
            {"name": "Handaxe", "cost": "5 gp", "damage": "1d6 S", "weight": "2 lb.", "properties": "Thrown Rg(20/60)"},
            {"name": "Javelin", "cost": "5 sp", "damage": "1d6 P", "weight": "2 lb.", "properties": "Thrown Rg(30/120)"},
            {"name": "Light hammer", "cost": "2 gp", "damage": "1d4 B", "weight": "2 lb.", "properties": "Thrown Rg(20/60)"},
            {"name": "Mace", "cost": "5 gp", "damage": "1d6 B", "weight": "4 lb.", "properties": "-"},
            {"name": "Quarterstaff", "cost": "2 sp", "damage": "1d6 B", "weight": "4 lb.", "properties": "Versatile(1d8)"},
            {"name": "Sickle", "cost": "1 gp", "damage": "1d4 S", "weight": "2 lb.", "properties": ""},
            {"name": "Spear", "cost": "1 gp", "damage": "1d6 P", "weight": "3 lb.", "properties": "Thrown Rg(20/60), Versatile(1d8)"},
            {"name": "Crossbow, light", "cost": "25 gp", "damage": "1d8 P", "weight": "5 lb.", "properties": "Ammunition, Rg(80/320), Two Handed"},
            {"name": "Dart", "cost": "5 cp", "damage": "1d4 P", "weight": "1/4 lb.", "properties": "Finesse Weapon, Thrown Rg(20/60)"},
            {"name": "Shortbow", "cost": "25 gp", "damage": "1d6 P", "weight": "2 lb.", "properties": "Ammunition, Rg(80/320), Two Handed"},
            {"name": "Sling", "cost": "1 sp", "damage": "1d4 B", "weight": "---", "properties": "Ammunition, Rg(320)"},
            {"name": "Battleaxe", "cost": "10 gp", "damage": "1d8 S", "weight": "4 lb.", "properties": "Versatile(1d10)"},
            {"name": "Flail", "cost": "10 gp", "damage": "1d8 B", "weight": "2 lb.", "properties": "-"},
            {"name": "Glaive", "cost": "20 gp", "damage": "1d10 S", "weight": "6 lb.", "properties": "Reach, Two Handed"},
            {"name": "Greataxe", "cost": "30 gp", "damage": "1d12 S", "weight": "7 lb.", "properties": "Two Handed"},
            {"name": "Greatsword", "cost": "50 gp", "damage": "2d6 S", "weight": "6 lb.", "properties": "Two Handed"},
            {"name": "Halberd", "cost": "20 gp", "damage": "1d10 S", "weight": "6 lb.", "properties": "Reach, Two Handed"},
            {"name": "Lance", "cost": "10 gp", "damage": "1d12 P", "weight": "6 lb.", "properties": "Reach, Special"},
            {"name": "Longsword", "cost": "15 gp", "damage": "1d8 S", "weight": "3 lb.", "properties": "Versatile(1d10)"},
            {"name": "Maul", "cost": "10 gp", "damage": "2d6 B", "weight": "10 lb.", "properties": "Two Handed"},
            {"name": "Morningstar", "cost": "15 gp", "damage": "1d8 P", "weight": "4 lb.", "properties": "-"},
            {"name": "Pike", "cost": "5 gp", "damage": "1d10 P", "weight": "18 lb.", "properties": "Reach, Two Handed"},
            {"name": "Rapier", "cost": "25 gp", "damage": "1d8 P", "weight": "2 lb.", "properties": "Finesse Weapon"},
            {"name": "Scimitar", "cost": "25 gp", "damage": "1d6 S", "weight": "3 lb.", "properties": "Finesse Weapon"},
            {"name": "Shortsword", "cost": "10 gp", "damage": "1d6 P", "weight": "2 lb.", "properties": "Finesse Weapon"},
            {"name": "Trident", "cost": "5 gp", "damage": "1d6 P", "weight": "4 lb.", "properties": "Thrown Rg(20/60), Versatile(1d8)"},
            {"name": "War pick", "cost": "5 gp", "damage": "1d8 P", "weight": "2 lb.", "properties": "-"},
            {"name": "Warhammer", "cost": "15 gp", "damage": "1d8 B", "weight": "2 lb.", "properties": "Versatile(1d10)"},
            {"name": "Whip", "cost": "2 gp", "damage": "1d4 S", "weight": "3 lb.", "properties": "Finesse Weapon, Reach"},
            {"name": "Blowgun", "cost": "10 gp", "damage": "1 P", "weight": "1 lb.", "properties": "Ammunition, Rg(25/100)"},
            {"name": "Crossbow, hand", "cost": "75 gp", "damage": "1d6 P", "weight": "3 lb.", "properties": "Ammunition, Rg(30/120)"},
            {"name": "Crossbow, heavy", "cost": "50 gp", "damage": "1d10 P", "weight": "18 lb.", "properties": "Ammunition, Rg(100/400), Two Handed"},
            {"name": "Longbow", "cost": "50 gp", "damage": "1d8 P", "weight": "2 lb.", "properties": "Ammunition, Rg(150,600), Two Handed"},
            {"name": "Net", "cost": "1 gp", "damage": "---", "weight": "3 lb.", "properties": "Special, Thrown Rg(5/15)"}
        ]
        self.armor = [
            {"name": "Padded", "cost": "5 gp", "AC": "11 + Dex mod", "weight": "8 lb."},
            {"name": "Leather", "cost": "10 gp", "AC": "11 + Dex mod", "weight": "10 lb."},
            {"name": "Studded leather", "cost": "45 gp", "AC": "12 + Dex mod", "weight": "13 lb."},
            {"name": "Hide", "cost": "10 gp", "AC": "12 + Dex mod (Max 2)", "weight": "12 lb."},
            {"name": "Chain shirt", "cost": "50 gp", "AC": "13 + Dex mod (Max 2)", "weight": "20 lb."},
            {"name": "Scale mail", "cost": "50 gp", "AC": "14 + Dex mod (Max 2)", "weight": "45 lb."},
            {"name": "Breastplate", "cost": "400 gp", "AC": "14 + Dex mod (Max 2)", "weight": "20 lb."},
            {"name": "Half plate", "cost": "750 gp", "AC": "15 + Dex mod (Max 2)", "weight": "40 lb."},
            {"name": "Ring mail", "cost": "30 gp", "AC": "14", "weight": "40 lb."},
            {"name": "Chain mail", "cost": "75 gp", "AC": "16", "weight": "55 lb."},
            {"name": "Splint", "cost": "200 gp", "AC": "17", "weight": "60 lb."},
            {"name": "Plate", "cost": "1,500 gp", "AC": "18", "weight": "65 lb."},
            {"name": "Shield", "cost": "10 gp", "AC": "+2", "weight": "6 lb."}
        ]
        self.df_everything = []

    def stringify_spell(self, spell):
        return f"Name: {spell['name']} \n Classes: {', '.join(spell['classes'])} \n Description: {spell['description']}"
    
    def stringify_monster(self, monster):
        return f"Name: {monster['name']} \n Description: {monster['description']} \n Challenge Level: {monster['challenge_level']}"

    def stringify_magic_item(self, magic_item):
        return f"Name: {magic_item['name']} \n Description: {magic_item['description']}"
    
    def stringify_weapon(self, weapon):
        return f"Name: {weapon['name']} \n Cost: {weapon['cost']} \n Damage: {weapon['damage']} \n Weight: {weapon['weight']} \n Properties: {weapon['properties']}"

    def stringify_armor(self, armor):
        return f"Name: {armor['name']} \n Cost: {armor['cost']} \n AC: {armor['AC']} \n Weight: {armor['weight']}"
    
    def stringify_place(self, place):
        return f"Name: {place['name']} \n Description: {place['description']}"
    
    def stringify_character(self, character):
        return f"Name: {character['name']} \n Description: {character['description']}"

    def stringify_other(self, other):
        return f"Name: {other['name']} \n Description: {other['description']}"
    
    def make_dataframes(self):
        self.df_spells = pd.DataFrame(self.spells)
        self.df_monsters = pd.DataFrame(self.monsters)
        self.df_magic_items = pd.DataFrame(self.magic_items)
        self.df_weapons = pd.DataFrame(self.weapons)
        self.df_armor = pd.DataFrame(self.armor)
        self.df_places = pd.DataFrame(self.places)
        self.df_characters = pd.DataFrame(self.characters)
        self.df_other = pd.DataFrame(self.other)

        self.df_spells['stringified'] = self.df_spells.apply(lambda x: self.stringify_spell(x), axis=1)
        self.df_monsters['stringified'] = self.df_monsters.apply(lambda x: self.stringify_monster(x), axis=1)
        self.df_magic_items['stringified'] = self.df_magic_items.apply(lambda x: self.stringify_magic_item(x), axis=1)
        self.df_weapons['stringified'] = self.df_weapons.apply(lambda x: self.stringify_weapon(x), axis=1)
        self.df_armor['stringified'] = self.df_armor.apply(lambda x: self.stringify_armor(x), axis=1)
        self.df_places['stringified'] = self.df_places.apply(lambda x: self.stringify_place(x), axis=1)
        self.df_characters['stringified'] = self.df_characters.apply(lambda x: self.stringify_character(x), axis=1)
        self.df_other['stringified'] = self.df_other.apply(lambda x: self.stringify_other(x), axis=1)

        self.df_everything = pd.concat([
            self.df_spells[['name', 'stringified']].assign(Type='Spell'),
            self.df_monsters[['name', 'stringified']].assign(Type='Monster'),
            self.df_magic_items[['name', 'stringified']].assign(Type='Magic Item'),
            self.df_weapons[['name', 'stringified']].assign(Type='Weapon'),
            self.df_armor[['name', 'stringified']].assign(Type='Armor'),
            self.df_places[['name', 'stringified']].assign(Type='Place'),
            self.df_characters[['name', 'stringified']].assign(Type='Character'),
            self.df_other[['name', 'stringified']].assign(Type='Other')
        ], ignore_index=True)
        
    def load_individual_from_pickle(self):
        with open(get_file_path("data/magic_items.p"), "rb") as f:
            self.magic_items = pickle.load(f)
        with open(get_file_path("data/spells.p"), "rb") as f:
            self.spells = pickle.load(f)
        with open(get_file_path("data/monsters.p"), "rb") as f:
            self.monsters = pickle.load(f)

        self.make_dataframes()

    def load_everything_from_pickle(self):
        with open(get_file_path("data/df_everything.p"), "rb") as f:
            self.df_everything = pickle.load(f)

    def load_everything_embedded_from_pickle(self):
        with open(get_file_path("data/df_everything_embedded.p"), "rb") as f:
            self.df_everything = pickle.load(f)

    def save_individual_to_pickle(self):
        pickle.dump(self.magic_items, open(get_file_path("data/magic_items.p"), "wb"))
        pickle.dump(self.spells, open(get_file_path("data/spells.p"), "wb"))
        pickle.dump(self.monsters, open(get_file_path("data/monsters.p"), "wb"))
        pickle.dump(self.df_magic_items, open(get_file_path("data/df_magic_items.p"), "wb"))
        pickle.dump(self.df_spells, open(get_file_path("data/df_spells.p"), "wb"))
        pickle.dump(self.df_monsters, open(get_file_path("data/df_monsters.p"), "wb"))
        
    def save_everything_to_pickle(self):
        pickle.dump(self.df_everything, open(get_file_path("data/df_everything.p"), "wb"))

    def save_everything_embedded_to_pickle(self):
        pickle.dump(self.df_everything, open(get_file_path("data/df_everything_embedded.p"), "wb"))

    def create_and_save_embeddings(self):

        self.df_everything['embedding'] = self.df_everything.apply(lambda x: get_embedding(x['stringified'], model='text-embedding-ada-002'), axis=1)

        self.save_everything_embedded_to_pickle()

    def search(self, search_term, type='everything', num=3):

        def search_reviews(df, product_description, n=3, pprint=True):
            embedding = get_embedding(product_description, model='text-embedding-ada-002')
            df['similarities'] = df.embedding.apply(lambda x: cosine_similarity(x, embedding))
            res = df.sort_values('similarities', ascending=False).head(n)
            return res
        if type == 'everything':
            return search_reviews(self.df_everything, search_term, n=num)
        else:
            return search_reviews(self.df_everything.loc[self.df_everything['Type'] == type], search_term, n=num)

    def load_from_text(self):
        file_path = get_file_path("data/spells.txt")

        def extract_spells(file):
            spells = []
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    line_buffer = ''
                    prev_spell_name = ''
                    prev_spell_level = 0
                    spell_name = ''
                    spell_level = 0
                    for i in range(1, len(lines)):

                        if ' - ' in lines[i]:
                            prev_spell_name = spell_name
                            prev_spell_level = spell_level
                            spell_name = lines[i-1].strip()
                            spell_level = lines[i][lines[i].find(' - ') - 1]

                            if i > 2:
                                spells.append({
                                    'name': prev_spell_name,
                                    'level': int(prev_spell_level),
                                    'description': line_buffer.strip()
                                })
                                line_buffer = ''
                            

                        else:
                            if 'Description not available' not in lines[i-1]:
                                line_buffer += lines[i-1]

                return spells
            else:
                print("File " + file_path + " not found.")
                return []

        self.spells = []

        classes = ['sorcerer', 'bard', 'cleric', 'druid', 'paladin', 'ranger', 'warlock', 'wizard']

        for class_name in classes:
            file_path = get_file_path(f"data/{class_name}_spells.txt")
            class_spells = extract_spells(file_path)

            for spell in class_spells:
                if spell['name'] not in [sp['name'] for sp in self.spells]:
                    spell['classes'] = [class_name.capitalize()]
                    self.spells.append(spell)
                else:
                    index = [sp['name'] for sp in self.spells].index(spell['name'])
                    self.spells[index]['classes'].append(class_name.capitalize())

        def extract_monsters(file):
            monsters = []
            if os.path.exists(file_path):
                with open(file_path, "r", encoding='utf-8') as file:
                    lines = file.readlines()
                    line_buffer = ''
                    prev_monster_name = ''
                    monster_name = ''
                    for i in range(2, len(lines)):

                        if 'Armor Class' in lines[i]:
                            prev_monster_name = monster_name
                            monster_name = lines[i-2].strip()

                            if i > 2:
                                start = line_buffer.find('Challenge ')
                                start += len('Challenge ')
                                if start != -1 and line_buffer[start] != '-':
                                    end = line_buffer.find(' ', start)

                                    challenge_level = round(float(Fraction(line_buffer[start:end+1])), 2)
                                else:
                                    challenge_level = 12

                                monsters.append({
                                    'name': prev_monster_name,
                                    'description': line_buffer.strip(),
                                    'challenge_level': challenge_level
                                })
                                line_buffer = ''

                        else:
                            line_buffer += lines[i-2]

                return monsters
            else:
                print("File " + file_path + " not found.")
                return []

        file_path = get_file_path("data/monsters.txt")
        self.monsters = extract_monsters(file_path)

        def extract_magic_items(file):
            magic_items = []
            if os.path.exists(file_path):
                with open(file_path, "r", encoding='utf-8') as file:
                    lines = file.readlines()
                    line_buffer = ''
                    prev_magic_item_name = ''
                    magic_item_name = ''
                    skip = False
                    for i in range(1, len(lines)):

                        if '=\n' in lines[i]:
                            skip = True
                            prev_magic_item_name = magic_item_name
                            magic_item_name = lines[i-1].strip()

                            if i > 2:

                                line_buffer = line_buffer.replace('\xa0', '')
                                line_buffer = line_buffer.replace('*', '')
                                line_buffer = line_buffer.replace(']', '')
                                line_buffer = line_buffer.replace('[', '')
                                while line_buffer.find('(https:') != -1:
                                    start = line_buffer.find('(https:')
                                    end = line_buffer.find(')', start)
                                    if end != -1:
                                        line_buffer = line_buffer[:start] + line_buffer[end+1:]
                
                                magic_items.append({
                                    'name': prev_magic_item_name,
                                    'description': line_buffer.strip()
                                })
                                line_buffer = ''

                        else:
                            if skip:
                                skip = False
                            else:
                                line_buffer += lines[i-1]

                return magic_items
            else:
                print("File " + file_path + " not found.")
                return []
            
        
        file_path = get_file_path("data/magic_items.txt")
        self.magic_items = extract_magic_items(file_path)


dict = Dictionary()

dict.load_everything_embedded_from_pickle()

print(dict.df_everything)
while True:
    search_term = input('Search: ')

    results = list(dict.search(search_term, num=6)['stringified'])
    for (n, res) in enumerate(results):
        print('\n')
        print('----------- ' + str(n) + ' -----------')
        print(res)
        print('\n')