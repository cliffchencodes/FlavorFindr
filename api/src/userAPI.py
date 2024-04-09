import uuid
import requests
from flask import Blueprint, request, jsonify


userAPI = Blueprint("userAPI", __name__)
DB_URL = "https://dsci551---oogabooga-default-rtdb.firebaseio.com/"  # change to one kelly made


# PUT method
@userAPI.route("/add", methods=["PUT"])
def create():
    try:
        data = request.json
        id = uuid.uuid4().hex
        url = f"{DB_URL}/user/{id}.json"
        response = requests.put(url, json=data)
        response.raise_for_status()  # raise error if req not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"


# GET Method
@userAPI.route("/list")
def read():
    try:
        response = requests.get(f"{DB_URL}user.json")
        response.raise_for_status()  # raise error if req not successful
        all_users = response.json()
        return jsonify(all_users), 200
    except Exception as error:
        return f"An error occurred {error}"


# POST method - this method does not work lol
@userAPI.route("/update/<user_id>", methods=["POST"])
def update(user_id):
    try:
        data = request.json
        url = f"https://dsci551---oogabooga-default-rtdb.firebaseio.com/user/{user_id}.json"
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error if the request was not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"


# DELETE method
@userAPI.route("/delete/<user_id>", methods=["DELETE"])
def delete(user_id):
    try:
        url = f"https://dsci551---oogabooga-default-rtdb.firebaseio.com/user/{user_id}.json"
        response = requests.delete(url)
        response.raise_for_status()  # Raise an error if the request was not successful
        return jsonify({"success": True}), 200
    except Exception as error:
        return f"An error occurred: {error}"
