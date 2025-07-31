# -*- coding: utf-8 -*-
def read_recipes(filename):
    cook_book = {}
    with open(filename, 'r', encoding='utf-8') as file:
        while True:
            # dish_name_0 = file.readline()
            # print("0_dish_name_0", dish_name_0)
            dish_name = file.readline().strip()
            # print("1_dish_name", dish_name)
            if not dish_name:
                break
            num_ingredients = int(file.readline().strip())
            # print("2_num_ingredients", num_ingredients)
            ingredients = []
            for num in range(num_ingredients):
                ingredient_name, quantity, measure = file.readline().strip().split(' | ')
                ingredients.append({
                    'ingredient_name': ingredient_name,
                    'quantity': int(quantity),
                    'measure': measure
                })
                # print("3_num_количество ингредиентов добавлено:", num + 1)
            cook_book[dish_name] = ingredients
            file.readline()
    return cook_book

all_cook_book = read_recipes('recipes.txt')
cook_book={}
for dish, ingredients in all_cook_book.items():
    # print(f"4_ {dish}: {ingredients}")
    cook_book[dish]=ingredients
print("#задача №1")
print("cook_book = ", cook_book)

# Задача №2
def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for ingredient in cook_book.get(dish, []):
            name = ingredient['ingredient_name']
            if name in shop_list:
                shop_list[name]['quantity'] += ingredient['quantity'] * person_count
            else:
                shop_list[name] = {
                    'measure': ingredient['measure'],
                    'quantity': ingredient['quantity'] * person_count
                }
    return shop_list

shop_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)
all_shop_list = {}
for ingredient, details in shop_list.items():
    all_shop_list[ingredient] = details
    # print(f"5_ {ingredient}: {details}")
print("#задача №2")
print(all_shop_list)
