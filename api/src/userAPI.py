import requests
from src.agg_functions import *
from flask import Blueprint, request, jsonify


userAPI = Blueprint("userAPI", __name__)
DB_URL = "https://dsci551---oogabooga-default-rtdb.firebaseio.com/"  # change to one kelly made
key = "corn"


# PUT method
@userAPI.route("/add", methods=["PUT"])
def create():
    try:
        data = request.json
        id = key
        url = f"{DB_URL}foods/{id}.json"
        response = requests.put(url, json=data)
        response.raise_for_status()  # raise error if req not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"


# GET Method
@userAPI.route("/list")
def read():
    try:
        response = requests.get(f"{DB_URL}foods.json")
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

        # user inputs & check:
        id = key  # will be user input
        field1 = "food_group"  # change this value - UI
        field1_val = data.get("food_group")  # change this value - UI
        if not id or not field1_val:
            return jsonify({"error": "Food ID or Calcium value not provided"}), 400

        url = f"{DB_URL}foods/{id}/{field1}.json"

        response = requests.put(url, json=field1_val)
        response.raise_for_status()  # Raise an error if the request was not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"


# DELETE method
@userAPI.route("/delete", methods=["DELETE"])
def delete():
    try:
        id = key  # User input
        url = f"{DB_URL}foods/{id}.json"
        response = requests.delete(url)
        response.raise_for_status()  # Raise an error if the request was not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"


# AGGREGATE method - WIP
@userAPI.route("/aggregate", methods=["GET"])
def perform_aggregation():

    # group_by_column = request.args.get("group_by")  # TO ADD: user input group by col
    # agg_operation = request.args.get("aggregation")  # TO ADD: user input agg type

    group_by_column = "food_group"
    agg_op = "sum"

    # aggregate data by querying from db
    response = requests.get(f"{DB_URL}foods.json")
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
