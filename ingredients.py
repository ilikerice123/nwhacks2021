import json

class Node:
    def __init__(self, word, parent):
        self.word = word
        self.parent = parent
        self.children = {}

class Ingredients:
    def __init__(self):
        with open('ingredients.json') as f:
            ingredients = set(json.load(f))
        
        self.root = Node("*", None)
        for ingredient in ingredients:
            self._encode_ingredient(ingredient)

    # search for ingredients in the current fragment
    # do not care if ingredients are cut off between fragments...
    def parse_ingredients(self, fragment):
        words = fragment.lower().split()
        ret = []
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
        

