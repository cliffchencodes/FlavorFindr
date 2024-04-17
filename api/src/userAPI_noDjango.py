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
        calories = request.form.get('calories')
        protein = request.form.get('protein')
        total_fat = request.form.get('total_fat')
        carbohydrates = request.form.get('carbohydrates')

        food_data = {
        "restaurant_name": restaurant_name,
        "name": food_name,
        "calories": int(calories),
        "protein": int(protein),
        "total_fat": int(total_fat),
        "carbohydrates": int(carbohydrates)
        }

        hash_val = hashing(food_name)
        url = f"{DATABASE_URLS[hash_val]}foods/{food_name}.json"
        response = requests.put(url, json=food_data)
        response.raise_for_status()  # raise error if req not successful
        # return jsonify({"success": True}), 200
        return render_template('success.html')
    else:
        return render_template("failure.html")


# GET Method - NEED TO ADJUST FILTERING - ONLY 1 FILTER CONDITION SENT TO FIREBASE - NEED TO DO REST MANUALLY 
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
    rest_name = request.args.get("restaurant_name")
    carb_filt = request.args.get("carb_filt_type")
    carb_val = request.args.get("carbs")
    cal_filt = request.args.get("cal_filt_type")
    cal_val = request.args.get("cals")
    fat_filt = request.args.get("fat_filt_type")
    fat_val = request.args.get("total_fat")
    prot_filt = request.args.get("pro_filt_type")
    prot_val = request.args.get("protein")

    # check input values if empty
    all_entries = [
        food_name,
        rest_name,
        carb_filt,
        carb_val,
        cal_filt,
        cal_val,
        fat_filt,
        fat_val,
        prot_filt,
        prot_val
        ]    
    # result dictionary
    all_foods = {}

    # return all entries
    if all(entry == "" or entry is None for entry in all_entries):
        for i in range(5):
            db_base = f"{DATABASE_URLS[i]}"
            url = f'{db_base}foods.json'
            response = requests.get(url)
            response.raise_for_status()  # raise error if req not successful
            all_foods.update(response.json())
        items = [v for _, v in all_foods.items()]
        # print(f"Items: \n{items}\n\n")
        return render_template('query.html', items=items)


    # filters to apply
    filters = []
    for val, filt, nutri in zip([carb_val, cal_val, fat_val, prot_val], 
                        [carb_filt, cal_filt, fat_filt, prot_filt],
                        ['carbohydrates', 'calories', 'total_fat', 'protein']):
        if filt != None:
            filters.append((val, filt, nutri))
    # print(f"\nfilters:{filters}\n")

    try:
        # name-based food search: 
        if food_name != "":
            hash_val = hashing(food_name)  # should be dynamic
            db_base = f"{DATABASE_URLS[hash_val]}"
            url = f'{db_base}foods/{food_name}.json'
            response = requests.get(url)
            response.raise_for_status()  # raise error if req not successful
            all_foods = {food_name: response.json()}
            # print(f"\nAll foods: {all_foods}\n")
        else:
            # initial restaurant filter
            if rest_name != '': 
                print('rest_name')
                for i in range(5):
                    # get all foods from restaurant
                    url = f'{DATABASE_URLS[i]}foods.json?' + f'orderBy="restaurant_name"&equalTo="{rest_name}"'
                    response = requests.get(url)
                    response.raise_for_status()  # raise error if req not successful
                    all_foods.update(response.json())
            
            # Initial filter if no restaurant name
            elif filters:
                first_op = filters[0]
                filters = filters[1:]
                # print(f"FIRST_OP: \n{first_op}\n")
                for i in range(5):
                    if first_op[1] == 'equal':
                        url = f'{DATABASE_URLS[i]}foods.json?' + f'orderBy="{first_op[2]}"&equalTo={first_op[0]}'
                    elif first_op[1] == 'greater':
                        url = f'{DATABASE_URLS[i]}foods.json?' + f'orderBy="{first_op[2]}"&startAt={int(first_op[0]) + 1}'
                    elif first_op[1] == 'less':
                        url = f'{DATABASE_URLS[i]}foods.json?' + f'orderBy="{first_op[2]}"&endAt={int(first_op[0]) - 1}'
                    response = requests.get(url)
                    response.raise_for_status()  # raise error if req not successful
                    all_foods.update(response.json())
                # print(f"FINAL ALL_FOODS: \n{all_foods}\n")
            else:
                return render_template("failure.html")

            # filter first_pull                
            try:
                # print(f"REST OF FILTERS TO APPLY: \n{filters}\n")
                all_foods = apply_filters(all_foods, filters)
            except:
                print('passed')
                pass
        
        items = [v for k, v in all_foods.items()]
        # print(f"Items: \n{items}\n\n")
        return render_template('query.html', items=items)
    
    except Exception as error:
        return f"An error occurred {error}"


# POST method - DONE
@userAPI.route("/update", methods=["POST"])
def update():
    try:
        """
        UI: [5 inputs: id: food to reference --> bread, 
                        filt_type: filter type --> [greater, less, equal, None],
                        filt_field: key to reference --> calories, 
                        old_val: val to filter on --> 0, 
                        new_val: new value --> 4]
        """
        food_name =  request.form.get("id")
        filt_field = request.form.get('filt_field')
        filt_type = request.form.get('filt_type') 
        filt_type = None if filt_type == "none" else filt_type
        old_val = request.form.get('old_val')
        new_val = request.form.get('new_val')

        # name-based food search: 
        if food_name:
            hash_val = hashing(food_name)  # should be dynamic
            url = f"{DATABASE_URLS[hash_val]}foods/{food_name}/{filt_field}.json"
            response = requests.put(url, json=new_val)
            response.raise_for_status()

        else:
            if filt_field and filt_type and old_val and new_val:
                # update equal 
                if filt_type == 'equal':
                    updateEqual(filt_field, old_val, new_val, DATABASE_URLS)
                
                # update greater 
                elif filt_type == 'greater':
                    updateGreater(filt_field, old_val, new_val, DATABASE_URLS)
                
                # update less
                elif filt_type == 'less':
                    updateLesser(filt_field, old_val, new_val, DATABASE_URLS)
            else:
                raise Exception("Invalid input, please double check")
        # return jsonify({"success": True}), 200
        return render_template('success.html')

    except Exception as error:
        # return f"An error occurred: {error}"
        return render_template("failure.html")


# DELETE method - DONE
@userAPI.route("/delete", methods=["POST", "DELETE"])
def delete():
    try:
        """
        # UI 1: [1 input: id(s) to specify path --> bread OR bread/calcium]
        # UI 2: [4 input: id(s) to specify path --> bread, filter field --> calcium, 
        filter type --> [greater, less, equal, None], value --> 5]
        """
        food_name = request.form.get("id")
        filt_field = request.form.get('filt_field')
        filt_type = request.form.get('filt_type')
        filt_val = request.form.get('filt_val')

        if food_name:
            hash_val = hashing(food_name)  # should be dynamic
            url = f"{DATABASE_URLS[hash_val]}foods/{food_name}.json"
            response = requests.delete(url)
            print('deleted')
            response.raise_for_status()
        else:
            if filt_field != "" and filt_type != "" and filt_val != "":
                if filt_type == 'equal':
                    deleteAll(filt_field, filt_val, DATABASE_URLS)
                elif filt_type == 'greater':
                    deleteGreater(filt_field, filt_val, DATABASE_URLS)
                elif filt_type == 'less':
                    deleteLesser(filt_field, filt_val, DATABASE_URLS)
                else:
                    print("Please enter a valid comparison operator")
        # return jsonify({"success": True}), 200
        return render_template('success.html')
    except Exception as error:
        # return f"An error occurred: {error}"
        return render_template("failure.html")


# ORDERBY method - Done
@userAPI.route("/orderby", methods=["GET"])
def orderby():
    # UI: [2 inputs:  sort by cat --> fat, asc --> T/F]
    sb_cat = request.args.get("agg_field") 
    desc = True if request.args.get("descending") else False

    output_list = []
    out_dict = {}
    for i in range(5):
        url = f"{DATABASE_URLS[i]}foods.json"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request was not successful
        out_dict.update(response.json())
    print(f"{out_dict}\n\n")
    sorted_df = dict(
        sorted(out_dict.items(), key=lambda x: int(x[1][sb_cat]), reverse=desc)
    )

    items = [v for k, v in sorted_df.items()]

    print(f"Output List: \n{output_list}\n")
    # return jsonify(output_list)
    return render_template('query.html', items=items)


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
        cat = request.args.get("agg_field")
        res = min_food(all_foods, group_by_column, cat)
    elif agg_op == "max":
        cat = request.args.get("agg_field")
        res = max_food(all_foods, group_by_column, cat)
    else:
        return jsonify({"Error": "Invalid Aggregation Type"}), 400

    if agg_op in ["min", "max"]:
        return render_template('groupby.html',
                               grouped_data=res,
                               group_by_field=group_by_column,
                               aggregate_function=agg_op,
                               agg_field=cat)
    else:
        return render_template('groupby.html',
                               grouped_data=res,
                               group_by_field=group_by_column,
                               aggregate_function=agg_op)
