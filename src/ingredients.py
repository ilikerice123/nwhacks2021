import json
from fractions import Fraction
class Node:
    def __init__(self, word, parent):
        self.word = word
        self.parent = parent
        self.children = {}

class Ingredients:
    def __init__(self):
        with open('../../datasets/json/ingredients.json') as f:
            ingredients = set(json.load(f))
        with open('../../datasets/json/units.json') as f:
            self.units = json.load(f)
        with open('../../datasets/json/amounts.json') as f:
            self.amounts = json.load(f)

        self.root = Node("*", None)
        for ingredient in ingredients:
            self._encode_ingredient(ingredient)

    # search for ingredients in the current fragment
    # do not care if ingredients are cut off between fragments...
    def parse_ingredients(self, fragment):
        words = self._words(fragment)
        ret = []
        # TODO fix this shit and remove b/c it's temporary
        i = 0
        while i < len(words):
            if words[i] in self.root.children:
                # word exists in ingredients, time to walk the tree
                cur_node = self.root
                while i < len(words) and words[i] in cur_node.children:
                    cur_node = cur_node.children[words[i]]
                    i += 1
                if '*' in cur_node.children:
                    ret.append(self._extract_string(cur_node))
            i += 1
        return ret

    # search for any measurements in the current fragment
    # do not care if measurements are cut off between fragments
    def parse_measurements(self, fragment):
        words = self._words(fragment)
        amounts = []
        units = []
        for word in words:
            amount = self._tryAmount(word)
            if amount is not None:
                # number! woot woot
                amounts.append(amount)
                continue
            unit = self._tryUnit(word)
            if unit is not None:
                # unit! woot woot
                units.append(unit)

        measurements = []
        for i in range(len(amounts)):
            if i >= len(units):
                measurements.append((str(amounts[i]), None))
                break
            measurements.append((str(amounts[i]), units[i]))
        return measurements

    # tries to parse a word into an amount
    # returns None if not an amount
    def _tryAmount(self, s):
        for amount in self.amounts:
            if amount == s:
                return s
        try:
            return Fraction(s)
        except Exception:
            return None

    # tries to parse a word into a unit
    # returns None if not a unit
    def _tryUnit(self, s):
        for unit in self.units:
            if unit in s:
                return s
        return None
        
    def _words(self, fragment):
        return fragment.lower().replace(',', '').replace('.', '').split()
            
    def _extract_string(self, node):
        ingredient = ''
        while (node != self.root):
            ingredient = node.word + ' ' + ingredient
            node = node.parent
        return ingredient.strip()

    def _encode_ingredient(self, ingredient):
        words = ingredient.lower().split()
        cur_node = self.root

        # walk the tree, add new words to it 
        for word in words:
            if word not in cur_node.children:
                new_node = Node(word, cur_node)
                cur_node.children[word] = new_node
            cur_node = cur_node.children[word]

        # use '*' to mark the end of an ingredient
        if '*' not in cur_node.children:
            cur_node.children['*'] = Node('*', cur_node)
        

