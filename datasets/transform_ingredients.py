import json
ingredients = set([])

with open('json/train.json') as f:
    data = json.load(f)

for recipe in data:
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients:
            ingredients.add(ingredient)

parsed = list(ingredients)
with open('json/ingredients.json', 'w') as fi:
    json.dump(parsed, fi)
