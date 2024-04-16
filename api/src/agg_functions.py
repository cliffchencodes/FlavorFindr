import json


def groupby_sum_totals(all_foods, group_by_col):
    aggregated_sums = {}

    for _, attributes in all_foods.items():
        resto = attributes[group_by_col]
        if resto not in aggregated_sums:
            aggregated_sums[resto] = {
                "calories": 0,
                "carbohydrates": 0,
                "total_fat": 0,
                "protein": 0,
            }  # Initialize sums to 0 for each food group - ADJUST TO BE DYNAMIC
        aggregated_sums[resto]["calories"] += attributes["calories"]
        aggregated_sums[resto]["carbohydrates"] += attributes["carbohydrates"]
        aggregated_sums[resto]["total_fat"] += attributes["total_fat"]
        aggregated_sums[resto]["protein"] += attributes["protein"]

    # Printing aggregated sums for each "food group"
    # for restaurant, sums in aggregated_sums.items():
    #     print(f"Restaurant: {restaurant}, Aggregated Sums: {sums}")
    return aggregated_sums


# ADJUST TO GROUP BY CERTAIN FIELD
def groupby_count(all_foods, group_by_col):
    grouped_data = {}
    for food, attributes in all_foods.items():
        key = attributes[group_by_col]
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(food)

    for key, value in grouped_data.items():
        count = len(value)
        grouped_data[key] = {"num_items": count}

    return grouped_data


def groupby_avg(all_foods, group_by_col):
    aggregated_sums = {}
    for _, attributes in all_foods.items():
        resto = attributes[group_by_col]
        if resto not in aggregated_sums:
            aggregated_sums[resto] = {
                "calories": 0,
                "carbohydrates": 0,
                "total_fat": 0,
                "protein": 0,
                "count": 0,
            }
        aggregated_sums[resto]["calories"] += attributes["calories"]
        aggregated_sums[resto]["carbohydrates"] += attributes["carbohydrates"]
        aggregated_sums[resto]["total_fat"] += attributes["total_fat"]
        aggregated_sums[resto]["protein"] += attributes["protein"]
        aggregated_sums[resto]["count"] += 1

    for resto in aggregated_sums:
        num = aggregated_sums[resto]["count"]
        aggregated_sums[resto] = {
            key: value / num for key, value in aggregated_sums[resto].items()
        }

    aggregated_sums.pop("count", None)
    return aggregated_sums


def min_food(all_foods, group_by_col, min_cat):
    nutri_cats = ["calories", "carbohydrates", "total_fat", "protein"]

    # Code
    min_categories = {}
    for food, attributes in all_foods.items():
        resto = attributes[group_by_col]
        if resto not in min_categories:
            min_categories[resto] = {
                "food": "",
                "calories": 10000000000,
                "carbohydrates": 100000000000,
                "total_fat": 100000000000,
                "protein": 100000000000,
            }  # Initialize sums to 0 for each food group - ADJUST TO BE DYNAMIC
        if attributes[min_cat] < min_categories[resto][min_cat]:
            for cat in nutri_cats:
                min_categories[resto][cat] = attributes[cat]
            min_categories[resto]["food"] = food
    return min_categories


def max_food(all_foods, group_by_col, max_cat):
    nutri_cats = ["calories", "carbohydrates", "total_fat", "protein"]

    # Code:
    max_categories = {}
    for food, attributes in all_foods.items():
        resto = attributes[group_by_col]
        if resto not in max_categories:
            max_categories[resto] = {
                "food": "",
                "calories": 0,
                "carbohydrates": 0,
                "total_fat": 0,
                "protein": 0,
            }
        if attributes[max_cat] > max_categories[resto][max_cat]:
            for cat in nutri_cats:
                max_categories[resto][cat] = attributes[cat]
            max_categories[resto]["food"] = food
    return max_categories
