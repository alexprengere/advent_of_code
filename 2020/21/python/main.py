import sys

FOOD = []
INGREDIENTS = set()
ALLERGENS = set()

for row in sys.stdin:
    ingredients, allergens = row.rstrip().split(" (contains ")
    ingredients = set(ingredients.split())
    allergens = set(allergens.rstrip(")").split(", "))

    FOOD.append((ingredients, allergens))
    INGREDIENTS |= ingredients
    ALLERGENS |= allergens


# allergen => possible ingredients containing it
#
possibilities = {}
for allergen in ALLERGENS:
    possibilities[allergen] = INGREDIENTS.copy()

for ingredients, allergens in FOOD:
    for allergen in allergens:
        possibilities[allergen] &= set(ingredients)

# We iteratively reduce the possibilities when only 1 ingredient is possible.
# Note that the loop might never break, if the simple algorithm fails to reduce
# possibilities to {}.
# In that case we would need backtracking, like a Sudoku.
result = {}
while possibilities:
    for allergen, ingredients in list(possibilities.items()):
        if len(ingredients) == 1:
            ingredient = ingredients.pop()
            result[ingredient] = allergen
            del possibilities[allergen]
            for other_allergen, other_ingredients in possibilities.items():
                if ingredient in other_ingredients:
                    other_ingredients.remove(ingredient)


# PART 1
#
allergic = set(result)  # set of ingredients containing an allergen
print(sum(len(ingredients - allergic) for ingredients, _ in FOOD))


# PART 2
#
print(
    ",".join(ingredient for ingredient in sorted(result, key=lambda ing: result[ing]))
)
