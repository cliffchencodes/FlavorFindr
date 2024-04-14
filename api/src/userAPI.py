import requests
import json
from src.agg_functions import *
from flask import Blueprint, request, jsonify


userAPI = Blueprint("userAPI", __name__)
DATABASE_URLS = {
    0: 'https://dsci551-final-db0-default-rtdb.firebaseio.com/' #'a-e',
    1: 'https://dsci551-final-db1-default-rtdb.firebaseio.com/' #'f-j',
    2: 'https://dsci551-final-db2-default-rtdb.firebaseio.com/' #'k-o',
    3: 'https://dsci551-final-db3-default-rtdb.firebaseio.com/' #'p-t',
    4: 'https://dsci551-final-db4-default-rtdb.firebaseio.com/' #'u-z'
}

def hashing(foodName):
    temp = 0
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
        
key = "b"

# PUT method
@userAPI.route("/add", methods=["PUT"])
def create():
    try:
        """
        UI: [2 inputs: data: nutrition data to input --> {json}, id: name of food --> bread]
        """
        data = request.json
        id = key
        hash_val = hashing(data["foodName"])
        
        url = f"{DATABASE_URLS[hash_val]}foods/{id}.json"
        response = requests.put(url, json=data)
        response.raise_for_status()  # raise error if req not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"


# GET Method
@userAPI.route("/list")
def read():
    try:
        url = f'{DATABASE_URLS[hash_val]}foods.json?orderBy=\"calcium\"&equalTo=0'
        response = requests.get(url)
        # response = requests.get(f"{DATABASE_URLS[hash_val]}foods.json")
        response.raise_for_status()  # raise error if req not successful
        all_foods = response.json()
        return jsonify(all_foods), 200
    except Exception as error:
        return f"An error occurred {error}"


# POST method
@userAPI.route("/update", methods=["POST"])
def update():
    try:
        data = request.json

        """
        UI: [3 inputs: id: food to reference --> bread, field1: key to reference --> calcium, 
                        field1_val: new value --> 4]
        """
        id = key 
        field1 = "food_group" 
        field1_val = data.get("food_group") 

        if not id or not field1_val:
            return jsonify({"error": "Food ID or Calcium value not provided"}), 400

        url = f"{DATABASE_URLS[hash_val]}foods/{id}/{field1}.json"

        response = requests.put(url, json=field1_val)
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
        filter type --> [gt, lt, eq], value --> 5]
        """
        # id = key  # User input
        id = key
        filter_field = 'calcium'
        filter_type = 'equalTo'  # possible values: equalTo, less (endAt), greater (startAt)
        val_threshold = 0

        # url = f"{DATABASE_URLS[hash_val]}foods.json"
        url = f"{DATABASE_URLS[hash_val]}foods.json?orderBy=\"calcium\"&equalTo=0"
        # url = f"{DATABASE_URLS[hash_val]}foods.json?orderBy=\"calcium\"&equalTo=0"
        # query = {'orderBy': f"\"{filter_field}\"", filter_type: val_threshold}
        response = requests.delete(url)
        # response = requests.delete(url, params=query)
        response.raise_for_status()  # Raise an error if the request was not successful
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

    url = f"{DATABASE_URLS[hash_val]}foods.json"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request was not successful

    sorted_df = dict(
        sorted(response.json().items(), key=lambda x: x[1][sb_cat], reverse=desc)
    )
    for key, vals in sorted_df.items():
        output_list.append({key: vals})
    return jsonify(output_list)


# AGGREGATE method
@userAPI.route("/aggregate", methods=["GET"])
def aggregation():

    # group_by_column = request.args.get("group_by")  # TO ADD: user input group by col
    # agg_operation = request.args.get("aggregation")  # TO ADD: user input agg type

    # UI: [2 inputs: group by cat --> food_group, aggregation operation --> sum]
    group_by_column = "food_group"
    agg_op = "sum"

    # aggregate data by querying from db
    response = requests.get(f"{DATABASE_URLS[hash_val]}foods.json")
    response.raise_for_status()
    all_foods = response.json()

    # INSERT FUNCTIONS HERE
    if agg_op == "sum":
        res = groupby_sum_totals(all_foods)  # sum
    elif agg_op == "count":
        res = groupby_count(all_foods)  # count
    elif agg_op == "avg":
        res = groupby_avg(all_foods)  # avg
    elif agg_op == "min":
        # min - in tester
        pass
    elif agg_op == "max":
        # max - in tester
        pass
    else:
        return jsonify({"Error": "Invalid Aggregation Type"})

    aggregation_result = {
        "group_by": group_by_column,
        f"{agg_op}": res,  # insert val
    }
    return jsonify(aggregation_result)
