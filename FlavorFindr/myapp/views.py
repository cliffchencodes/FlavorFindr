from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.contrib import messages
import requests


def home(request):
    # render the main page
    return render(request, "home.html")


def query(request):
    if request.method == "GET":
        search_field = request.GET.get("search_field", "")
        search_operation = request.GET.get("search_operation", "")
        search_value = request.GET.get("search_value", "")
        order_by = request.GET.get("order_by", "")

        # with open("myapp/sample_food_items.json", "r") as file:
        with open("FlavorFindr/myapp/sample_food_items.json", "r") as file:
            items = json.load(file)

        if search_value:
            if search_operation == "eq":
                filtered_items = [
                    item
                    for item in items
                    if str(item.get(search_field, "")).lower() == search_value.lower()
                ]
            elif search_operation in ["gt", "lt"] and search_field in [
                "calories",
                "protein",
                "total_fat",
                "carbohydrates",
            ]:
                search_value = float(
                    search_value
                )  # Convert to float for numerical comparison
                if search_operation == "gt":
                    filtered_items = [
                        item
                        for item in items
                        if float(item.get(search_field, 0)) > search_value
                    ]
                elif search_operation == "lt":
                    filtered_items = [
                        item
                        for item in items
                        if float(item.get(search_field, 0)) < search_value
                    ]
            else:
                filtered_items = items
        else:
            filtered_items = items  # no search value, don't filter

        if order_by:
            reverse_order = request.GET.get("order_direction", "") == "desc"
            if order_by in ["calories", "protein", "total_fat", "carbohydrates"]:
                # Sort by numerical values
                filtered_items.sort(
                    key=lambda x: float(x.get(order_by, 0)), reverse=reverse_order
                )
            else:
                # Sort by string values (e.g., restaurant_name, item_name)
                filtered_items.sort(
                    key=lambda x: str(x.get(order_by, "")).lower(),
                    reverse=reverse_order,
                )

        return render(request, "results.html", {"items": filtered_items})

    return render(request, "search_form.html")


def results(request):
    # Retrieve the filtered items from the session and display them
    filtered_items = request.session.get("filtered_items", [])
    return render(request, "results.html", {"items": filtered_items})


def my_filter_function(items, get_data):
    attribute = get_data.get("search_field")
    operation = get_data.get("search_operation")
    value = get_data.get("search_value")

    if value:
        try:
            value = float(value)
        except ValueError:

            return []
        if attribute in ["calories", "protein", "total_fat", "carbohydrates"]:
            value = float(value)
        if attribute in ["restaurant_name", "name"]:
            if operation == "eq":
                filtered_items = [
                    item
                    for item in items
                    if item.get(attribute, "").lower() == value.lower()
                ]

        else:
            if operation == "eq":
                filtered_items = [
                    item for item in items if item.get(attribute, 0) == value
                ]
            elif operation == "gt":
                filtered_items = [
                    item for item in items if item.get(attribute, 0) > value
                ]
            elif operation == "lt":
                filtered_items = [
                    item for item in items if item.get(attribute, 0) < value
                ]

    else:
        filtered_items = items

    return filtered_items


def success(request):
    if request.method == "POST":
        operation = request.POST.get("operation")
        if operation == "delete":
            pass
        elif operation == "update":
            pass
        elif operation == "create":
            pass
        return render(request, "success.html", {"message": "Operation successful"})
    else:
        return render(request, "success.html", {"message": "No operation performed"})


def add_item(request):
    if request.method == "POST":
        new_item = {
            "restaurant_name": request.POST.get("restaurant_name"),
            "item_name": request.POST.get("item_name"),
            "calories": request.POST.get("calories"),
            "protein": request.POST.get("protein"),
            "total_fat": request.POST.get("total_fat"),
            "carbohydrates": request.POST.get("carbohydrates"),
        }

        with open("myapp/sample_food_items.json", "r") as file:
            data = json.load(file)

        data.append(new_item)

        with open("myapp/sample_food_items.json", "w") as file:
            json.dump(data, file, indent=4)

        return redirect("success")  # Redirect to a success page or the home page

    else:

        return render(request, "add-item.html")


def get_items():

    # response = requests.get('http://flask_api_url/items')
    # items = response.json()
    with open("path/to/your/json/file.json", "r") as file:
        items = json.load(file)
    return items


def save_items(items):

    # requests.put('http://flask_api_url/items', json=items)
    with open("path/to/your/json/file.json", "w") as file:
        json.dump(items, file, indent=4)


def find_item_by_name(items, name):
    for item in items:
        if item["name"] == name:
            return item
    return None


def edit_item(request, name):
    if request.method == "POST":
        items = get_items()
        item = find_item_by_name(items, name)
        if not item:
            messages.error(request, "Item not found.")
            return redirect("item_list")

        operation = request.POST.get("operation")
        if operation == "delete":

            # requests.delete('http://flask_api_url/items/' + str(item['id']))
            items.remove(item)
            save_items(items)
            messages.success(request, "Item deleted successfully.")
        elif operation == "update":

            # requests.put('http://flask_api_url/items/' + str(item['id']), json=item_data)

            save_items(items)
            messages.success(request, "Item updated successfully.")
        else:
            messages.error(request, "Invalid operation specified.")

        return redirect("item_list")
    else:

        pass


def group_by(request):
    if request.method == "GET":
        group_by_field = request.GET.get("group_by_field")
        aggregate_function = request.GET.get("aggregate_function")

        with open("myapp/sample_food_items.json", "r") as file:
            items = json.load(file)

        grouped_data = {}
        for item in items:
            key = item.get(group_by_field)
            if key not in grouped_data:
                grouped_data[key] = {
                    "calories": [],
                    "protein": [],
                    "carbohydrates": [],
                    "total_fat": [],
                }

            grouped_data[key]["calories"].append(item["calories"])
            grouped_data[key]["protein"].append(item["protein"])
            grouped_data[key]["carbohydrates"].append(item["carbohydrates"])
            grouped_data[key]["total_fat"].append(item["total_fat"])

        for key, nutrients in grouped_data.items():
            for nutrient, values in nutrients.items():
                if aggregate_function == "max":
                    grouped_data[key][nutrient] = max(values)
                elif aggregate_function == "min":
                    grouped_data[key][nutrient] = min(values)
                elif aggregate_function == "avg":
                    if values:  # to avoid division by zero
                        grouped_data[key][nutrient] = sum(values) / len(values)
                elif aggregate_function == "sum":
                    grouped_data[key][nutrient] = sum(values)

        return render(
            request,
            "groupby.html",
            {
                "grouped_data": grouped_data,
                "group_by_field": group_by_field,
                "aggregate_function": aggregate_function,
            },
        )


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


# PUT FUNCTION
def add_food_to_flask(request):
    if request.method == "PUT":
        try:
            # Get input data from the request
            # food_data = {
            #     "restaurant_name": "Domino's",
            #     "name": "Pepperoni Pizza",
            #     "calories": 300,
            #     "protein": 12,
            #     "total_fat": 13.5,
            #     "carbohydrates": 34,
            # }

            food_data = {
                "restaurant_name": request.PUT.get("restaurant_name"),
                "item_name": request.PUT.get("item_name"),
                "calories": request.PUT.get("calories"),
                "protein": request.PUT.get("protein"),
                "total_fat": request.PUT.get("total_fat"),
                "carbohydrates": request.PUT.get("carbohydrates"),
            }

            # food_data = request.json
            food_name = "Pepperoni Pizza"

            # Construct the URL for the Flask endpoint
            url = "http://localhost:5000/add"

            # Send a PUT request to the Flask endpoint
            response = requests.put(url, params={"data": food_data, "id": food_name})

            # Check if the request was successful
            if response.status_code == 200:
                return JsonResponse({"success": True})
            else:
                return JsonResponse(
                    {"success": False, "error": "Error adding food to Flask backend"},
                    status=500,
                )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": str(e) + "failed in except"}, status=500
            )
    else:
        return JsonResponse(
            {"success": False, "error": "Method not allowed"}, status=405
        )
