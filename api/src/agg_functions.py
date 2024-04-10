# ADJUST TO GROUP BY CERTAIN FIELD
def groupby_sum_totals(all_foods):
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
    return aggregated_sums


# ADJUST TO GROUP BY CERTAIN FIELD
def groupby_count(all_foods):
    grouped_data = {}
    for food, nutri_facts in all_foods.items():
        key = nutri_facts["food_group"]
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(food)

    for food_group, foods in grouped_data.items():
        print(f"There are {len(foods)} food(s) in the '{food_group}' food group")
