from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib import messages
import requests


"""
~~~~~~~~~~ CONNECTION FUNCTIONS ~~~~~~~~~~~~~
"""


# GET FUNCTION
def call_flask_api(request):
    if request.method == "GET":
        # Get inputs from Django frontend
        id = ""
        filt_type = None
        filt_field = "calcium"
        filt_val = 3

        # Make GET request to Flask API with inputs as query parameters
        response = requests.get(
            "http://localhost:5000/foods/list",
            params={
                "id": id,
                "filt_type": filt_type,
                "filt_field": filt_field,
                "filt_val": filt_val,
            },
        )  # Example API endpoint in Flask
        if response.status_code == 200:
            data = response.json()
            return render(request, "flask_data.html", {"data": data})
        else:
            # Handle error response
            return HttpResponse(
                "Error fetching data from Flask API", status=response.status_code
            )
    else:
        # Handle unsupported HTTP method
        return HttpResponse("Method Not Allowed", status=405)


# # PUT FUNCTION
# def add_food_to_flask(request):
#     # request.method is get
#     print(request.method)
#     request = requests.put("https://google.com")
#     if request.method == "PUT":
#         try:
#             # Get input data from the request

#             # food_data = {
#             #     "restaurant_name": request.get("restaurant_name"),
#             #     "item_name": request.get("item_name"),
#             #     "calories": request.get("calories"),
#             #     "protein": request.get("protein"),
#             #     "total_fat": request.get("total_fat"),
#             #     "carbohydrates": request.get("carbohydrates"),
#             # }

#             # food_data = request.json
#             food_name = "Pepperoni Pizza"
#             food_data = {
#                 "restaurant_name": "Domino's",
#                 "name": "Pepperoni Pizza",
#                 "calories": 300,
#                 "protein": 12,
#                 "total_fat": 13.5,
#                 "carbohydrates": 34,
#             }

#             # Construct the URL for the Flask endpoint
#             url = "http://localhost:5000/add"

#             # Send a PUT request to the Flask endpoint
#             response = requests.put(
#                 url, params={"food_name": food_name, "food_data": food_data}
#             )

#             # Check if the request was successful
#             if response.status_code == 200:
#                 return JsonResponse({"success": True})
#             else:
#                 return JsonResponse(
#                     {"success": False, "error": "Error adding food to Flask backend"},
#                     status=500,
#                 )
#         except Exception as e:
#             return JsonResponse(
#                 {"success": False, "error": str(e) + "failed in except"}, status=500
#             )
#     else:
#         return JsonResponse(
#             {"success": False, "error": "Method not allowed"}, status=405
#         )


# PUT FUNCTION
def add_food_to_flask(request):
    # request.method is get

    # Get input data from the request

    # food_data = {
    #     "restaurant_name": request.get("restaurant_name"),
    #     "item_name": request.get("item_name"),
    #     "calories": request.get("calories"),
    #     "protein": request.get("protein"),
    #     "total_fat": request.get("total_fat"),
    #     "carbohydrates": request.get("carbohydrates"),
    # }

    # food_data = request.json
    request.method = "PUT"
    food_name = "Pepperoni Pizza"
    food_data = {
        "restaurant_name": "Domino's",
        "name": "Pepperoni Pizza",
        "calories": 300,
        "protein": 12,
        "total_fat": 13.5,
        "carbohydrates": 34,
    }

    # Construct the URL for the Flask endpoint
    url = "http://localhost:5000/add"

    # Send a PUT request to the Flask endpoint
    response = requests.put(
        url, params={"food_name": food_name, "food_data": food_data}
    )

    # Check if the request was successful
    if response.status_code == 200:
        return JsonResponse({"success": True})
    else:
        return JsonResponse(
            {"success": False, "error": "Error adding food to Flask backend"},
            status=500,
        )
