import requests
import json
from src.agg_functions import *
from src.del_post_functions import * 
from src.get_functions import *
from flask import Blueprint, request, jsonify, render_template


userAPI = Blueprint("userAPI", __name__)

# GLOBAL VARS:
DATABASE_URLS = {
    0: 'https://dsci551-final-db0-default-rtdb.firebaseio.com/', #'a-e',
    1: 'https://dsci551-final-db1-default-rtdb.firebaseio.com/', #'f-j',
    2: 'https://dsci551-final-db2-default-rtdb.firebaseio.com/', #'k-o',
    3: 'https://dsci551-final-db3-default-rtdb.firebaseio.com/', #'p-t',
    4: 'https://dsci551-final-db4-default-rtdb.firebaseio.com/' #'u-z'
}
foodName = "Quarter Pounder Bacon"

def hashing(foodName):
    foodName = foodName.lower()
    firstLetter = foodName[0]

    if firstLetter >= 'a' and firstLetter <= 'e':
        return 0
    elif firstLetter >= 'f' and firstLetter <= 'j':
        return 1
    elif firstLetter >= 'k' and firstLetter <= 'o':
        return 2
    elif firstLetter >= 'p' and firstLetter <= 't':
        return 3
    elif firstLetter >= 'u' and firstLetter <= 'z':
        return 4
    else:
        print('Please input information under a valid food name. Must start with a letter.')
        return None
        

# PUT method - DONE
@userAPI.route("/add", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # Process form data
        restaurant_name = request.form.get('restaurant_name')
        food_name = request.form.get('food_name')
        calories = int(request.form.get('calories'))
        protein = int(request.form.get('protein'))
        total_fat = int(request.form.get('total_fat'))
        carbohydrates = int(request.form.get('carbohydrates'))

        food_data = {
        "restaurant_name": restaurant_name,
        "name": food_name,
        "calories": calories,
        "protein": protein,
        "total_fat": total_fat,
        "carbohydrates": carbohydrates
        }

        hash_val = hashing(food_name)
        url = f"{DATABASE_URLS[hash_val]}foods/{food_name}.json"
        response = requests.put(url, json=food_data)
        response.raise_for_status()  # raise error if req not successful
        return jsonify({"success": True}), 200
    else:
        return render_template("create.html")


# GET Method - DONE 
@userAPI.route("/list", methods=['GET'])
def read():
    """
    UI: [5 inputs: id: food to reference --> bread, 
                        filt_type: filter type --> [greater, less, equal, None],
                        filt_field: key to reference --> calcium, 
                        filt_val: val to filter on --> 0
                        ]
    """

    food_name = request.args.get("food_name")
    filt_type = request.args.get('filt_type')
    filt_type = filt_type if filt_type != "" else None  # error handling
    filt_field = request.args.get('filt_field')
    filt_field = filt_field if filt_field != "" else None  # error handling
    filt_val = request.args.get('filt_val')
    filt_val = filt_val if filt_val != "" else None  # error handling
    
    try:

        # name-based food search: 
        if food_name:
            hash_val = hashing(food_name)  # should be dynamic
            db_base = f"{DATABASE_URLS[hash_val]}"
            url = f'{db_base}foods/{food_name}.json'
            response = requests.get(url)
            response.raise_for_status()  # raise error if req not successful
            all_foods = response.json()
        
        else:
            # number-based search
            if filt_type and filt_field and filt_val: 
                all_foods = {}
                for i in range(5):
                    db_base = f"{DATABASE_URLS[i]}"

                    # all foods equal to x
                    if filt_type == 'equal':
                        tmp_foods = getEqual(filt_field, filt_val, db_base)

                    # all foods greater than x 
                    elif filt_type == 'greater':
                        tmp_foods = getGreater(filt_field, filt_val, db_base)

                    # all foods less than y
                    elif filt_type == 'lesser': 
                        tmp_foods = getLesser(filt_field, filt_val, db_base)
                    all_foods.update(tmp_foods)
            else:
                raise Exception ("Invalid input combination")

        # if get not working, might need invalid input check
        return jsonify(all_foods), 200
    
    except Exception as error:
        return f"An error occurred {error}"


# POST method
@userAPI.route("/update", methods=["POST"])
def update():
    try:
        data = request.json

        """
        UI: [5 inputs: id: food to reference --> bread, 
                            filt_type: filter type --> [greater, less, equal, None],
                            filt_field: key to reference --> calcium, 
                            old_val: val to filter on --> 0, 
                            new_val: new value --> 4]
        """
        id = foodName
        filt_type = 'equal'
        filt_field = "food_group" 
        old_val = 0
        new_val = data.get("food_group") 

        # check for valid input
        if not id or not new_val:
            return jsonify({"error": "Food ID or Calcium value not provided"}), 400
        # update equal 
        if filt_type == 'equal':
            updateEqual(filt_field, old_val, new_val, DATABASE_URLS)
        # update greater 
        elif filt_type == 'greater':
            updateGreater(filt_field, old_val, new_val, DATABASE_URLS)
        # update less
        elif filt_type == 'less':
            updateLesser(filt_field, old_val, new_val, DATABASE_URLS)
        # update only on field name
        elif filt_type == None:
            hash_val = hashing(foodName)  # should be dynamic
            url = f"{DATABASE_URLS[hash_val]}foods/{id}/{filt_field}.json"
            response = requests.put(url, json=new_val)
            response.raise_for_status()  # Raise an error if the request was not successful
        return jsonify({"success": True}), 200
    
    except Exception as error:
        return f"An error occurred: {error}"


# DELETE method
@userAPI.route("/delete", methods=["DELETE"])
def delete():
    try:
        """
        # UI 1: [1 input: id(s) to specify path --> bread OR bread/calcium]
        # UI 2: [4 input: id(s) to specify path --> bread, filter field --> calcium, 
        filter type --> [greater, less, equal, None], value --> 5]
        """
        filt_field = ''
        filt_type = None
        val = 0

        if filt_type == 'equal':
            deleteAll(filt_field, val, DATABASE_URLS)
        elif filt_type == 'greater':
            deleteGreater(filt_field, val, DATABASE_URLS)
        elif filt_type == 'less':
            deleteLesser(filt_field, val, DATABASE_URLS)
        elif filt_type == None:
            hash_val = hashing(foodName)  # should be dynamic
            url = f'{DATABASE_URLS[hash_val]}foods/{filt_field}.json'
            response = requests.delete(url)
            response.raise_for_status()  # Raise an error if the request was not successful
        else:
            print("Please enter a valid comparison operator")
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"



# ORDERBY method
@userAPI.route("/orderby", methods=["GET"])
def orderby():

    # group_by_column = request.args.get("group_by")  # TO ADD: user input group by col
    # sb_cat = request.args.get("aggregation")  # TO ADD: user input agg type

    # UI: [3 inputs: group by cat --> food_group, sort by cat --> fat, asc --> T/F]
    group_by_column = "food_group"
    sb_cat = "fat"
    desc = True
    output_list = []
    hash_val = hashing(foodName)  # should be dynamic

    url = f"{DATABASE_URLS[hash_val]}foods.json"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request was not successful

    sorted_df = dict(
        sorted(response.json().items(), key=lambda x: x[1][sb_cat], reverse=desc)
    )
    for key, vals in sorted_df.items():
        output_list.append({key: vals})
    return jsonify(output_list)


# AGGREGATE method - DONE
@userAPI.route("/aggregate", methods=["GET"])
def aggregation():

    # UI: [2 inputs: group by cat --> food_group, aggregation operation --> sum]
    group_by_column = request.args.get("agg_cat")
    agg_op = request.args.get("agg_operation")

    all_foods = {}

    for i in range(5):
        response = requests.get(f"{DATABASE_URLS[i]}foods.json")
        response.raise_for_status()
        all_foods.update(response.json())

    # INSERT FUNCTIONS HERE
    if agg_op == "sum":
        res = groupby_sum_totals(all_foods, group_by_column)  # sum
    elif agg_op == "count":
        res = groupby_count(all_foods, group_by_column)  # count
    elif agg_op == "avg":
        res = groupby_avg(all_foods, group_by_column)  # avg
    elif agg_op == "min":
        min_cat = request.args.get("agg_field")
        res = min_food(all_foods, group_by_column, min_cat)
    elif agg_op == "max":
        max_cat = request.args.get("agg_field")
        res = max_food(all_foods, group_by_column, max_cat)
    else:
        return jsonify({"Error": "Invalid Aggregation Type"})

    aggregation_result = {
        "group_by": group_by_column,
        f"{agg_op}": res,  
    }
    return jsonify(aggregation_result)
