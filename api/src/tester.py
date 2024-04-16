# %%
import requests
import json

# from flask import Blueprint, request, jsonify

DB_URL = "https://dsci551---oogabooga-default-rtdb.firebaseio.com/"  # change to one kelly made
key = "corn"

try:
    response = requests.get(f"{DB_URL}foods.json")
    response.raise_for_status()  # raise error if req not successful
    all_foods = response.json()  # root db in json form
    print(all_foods)
except Exception as error:
    print(f"An error occurred {error}")

# %%
# group_by_column = request.get("group_by")
# agg_operation = request.get("aggregation")


# %% sum total values - THIS WORKS
aggregated_sums = {}

for food, attributes in all_foods.items():
    food_group = attributes["food_group"]
    if food_group not in aggregated_sums:
        aggregated_sums[food_group] = {
            "calcium": 0,
            "fat": 0,
            "protein": 0,
        }  # Initialize sums to 0 for each food group - ADJUST TO BE DYNAMIC
    aggregated_sums[food_group]["calcium"] += attributes["calcium"]
    aggregated_sums[food_group]["fat"] += attributes["fat"]
    aggregated_sums[food_group]["protein"] += attributes["protein"]

# Printing aggregated sums for each "food group"
for food_group, sums in aggregated_sums.items():
    print(f"Food Group: {food_group}, Aggregated Sums: {sums}")


# %% count num values - THIS WORKS
grouped_data = {}
for food, nutri_facts in all_foods.items():
    key = nutri_facts["food_group"]
    if key not in grouped_data:
        grouped_data[key] = []
    grouped_data[key].append(food)

for food_group, foods in grouped_data.items():
    print(f"There are {len(foods)} food(s) in the '{food_group}' food group")

# %% avg total values
aggregated_sums = {}
for _, attributes in all_foods.items():
    food_group = attributes["food_group"]
    if food_group not in aggregated_sums:
        aggregated_sums[food_group] = {
            "calcium": 0,
            "fat": 0,
            "protein": 0,
            "count": 0,
        }  # Initialize sums to 0 for each food group - ADJUST TO BE DYNAMIC
    aggregated_sums[food_group]["calcium"] += attributes["calcium"]
    aggregated_sums[food_group]["fat"] += attributes["fat"]
    aggregated_sums[food_group]["protein"] += attributes["protein"]
    aggregated_sums[food_group]["count"] += 1

for food_group in aggregated_sums:
    num = aggregated_sums[food_group]["count"]
    aggregated_sums[food_group] = {
        key: value / num for key, value in aggregated_sums[food_group].items()
    }

aggregated_sums.pop("count", None)
print(aggregated_sums)


# %% Max

"""
Need to decide for each food (max of a category (i.e. fat) then take associated
nutrition facts or gross highest for each nutrition)
"""
# UI:
max_cat = "fat"
nested_keys = [key for value in all_foods.values() for key in value.keys()]
unique_labels = list(set(nested_keys))

# Code:
max_categories = {}
for food, attributes in all_foods.items():
    food_group = attributes["food_group"]
    if food_group not in max_categories:
        max_categories[food_group] = {
            "food": "",
            "calcium": 0,
            "fat": 0,
            "protein": 0,
        }  # Initialize sums to 0 for each food group - ADJUST TO BE DYNAMIC
    if attributes[max_cat] > max_categories[food_group][max_cat]:
        for label in unique_labels:
            max_categories[food_group][label] = attributes[label]
        max_categories[food_group]["food"] = food
print(max_categories)

# %% Min

"""
Need to decide for each food (max of a category (i.e. fat) then take associated
nutrition facts or gross highest for each nutrition)
"""
# UI: [2 inputs: group by cat --> food_group, aggregation cat --> fat]
min_cat = "fat"
nested_keys = [key for value in all_foods.values() for key in value.keys()]
unique_labels = list(set(nested_keys))

# Code
min_categories = {}
for food, attributes in all_foods.items():
    food_group = attributes["food_group"]
    if food_group not in min_categories:
        min_categories[food_group] = {
            "food": "",
            "calcium": 10000000000,
            "fat": 100000000000,
            "protein": 100000000000,
        }  # Initialize sums to 0 for each food group - ADJUST TO BE DYNAMIC
    if attributes[min_cat] < min_categories[food_group][min_cat]:
        for label in unique_labels:
            min_categories[food_group][label] = attributes[label]
        min_categories[food_group]["food"] = food

print(min_categories)

# %% Sort By
# UI: [3 inputs: group by cat --> food_group, sort by cat --> fat, asc --> T/F]
sb_cat = "fat"
desc = False

sorted_df = dict(sorted(all_foods.items(), key=lambda x: x[1][sb_cat], reverse=desc))
rank = 1
for key in sorted_df:
    print(f"{rank}. {key}: {sorted_df[key]}")
    rank += 1

# %% LEGACY DELETE FUNCTION:

#     # id = key  # User input
#     id = foodName
#     filter_field = 'calcium'
#     filter_type = 'equalTo'  # possible values: equalTo, less (endAt), greater (startAt)
#     val_threshold = 0
#     hash_val = hashing(foodName)  # should be dynamic

#     # url = f"{DATABASE_URLS[hash_val]}foods.json"
#     url = f"{DATABASE_URLS[hash_val]}foods.json?orderBy=\"calcium\"&equalTo=0"
#     # url = f"{DATABASE_URLS[hash_val]}foods.json?orderBy=\"calcium\"&equalTo=0"
#     # query = {'orderBy': f"\"{filter_field}\"", filter_type: val_threshold}
#     response = requests.delete(url)
#     # response = requests.delete(url, params=query)
#     response.raise_for_status()  # Raise an error if the request was not successful
#     return jsonify({"success": True}), 200
