import uuid
import requests
from flask import Blueprint, request, jsonify


userAPI = Blueprint("userAPI", __name__)
DB_URL = "https://dsci551---oogabooga-default-rtdb.firebaseio.com/"  # change to one kelly made
key = "cheese"


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
        all_users = response.json()
        return jsonify(all_users), 200
    except Exception as error:
        return f"An error occurred {error}"


# POST method
@userAPI.route("/update", methods=["POST"])
def update():
    try:
        data = request.json

        # user inputs & check:
        id = key  # will be user input
        field1 = "calcium"  # will be user input
        field1_val = data.get("calcium")
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
        id = key
        url = f"{DB_URL}foods/{id}.json"
        response = requests.delete(url)
        response.raise_for_status()  # Raise an error if the request was not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"
