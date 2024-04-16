import requests

"""
The following function will delete any entries where the ----- attribute is 
EQUAL TO ------ value. These "blanks" will serve as the parameters to the function.
"""


def deleteAll(attribute, val, glb_db):
    for i in range(5):
        URL = f"{glb_db[i]}"
        response = requests.get(f'{URL}/foods.json?orderBy="{attribute}"&equalTo={val}')
        if response.status_code == 200:
            data = response.json()
            for key in data:
                delete = requests.delete(
                    f"{URL}/foods/{key}.json"
                )  # check node for final implementation

                if delete.status_code == 200:
                    print(f"Item with key {key} deleted successfully.")
                else:
                    print(f"Failed to delete item with key {key}.")
        else:
            print("Failed to retrieve data from the database.")


"""
The following function will delete any entries where the ----- attribute is GREATER THAN ------ value. These "blanks" will serve as the parameters to the function.
"""


def deleteGreater(attribute, val, glb_db):
    for i in range(5):
        URL = f"{glb_db[i]}"

        response = requests.get(f'{URL}/foods.json?orderBy="{attribute}"&startAt={val}')

        if response.status_code == 200:
            data = response.json()

            for key in data:
                delete = requests.delete(
                    f"{URL}/foods/{key}.json"
                )  # check node for final implementation

                if delete.status_code == 200:
                    print(f"Item with key {key} deleted successfully.")
                else:
                    print(f"Failed to delete item with key {key}.")
        else:
            print("Failed to retrieve data from the database.")
    return


"""
The following function will delete any entries where the ----- attribute is LESS THAN ------ value. These "blanks" will serve as the parameters to the function.
"""


# CHANGE NODE.JSON TO THE ACTUAL PATH --> wasn't too sure, ask group
def deleteLesser(attribute, val, glb_db):
    for i in range(5):
        URL = f"{glb_db[i]}"

        response = requests.get(
            f'{URL}/foods.json?orderBy="{attribute}"&endAt={val - 1}'
        )

        if response.status_code == 200:
            data = response.json()

            for key in data:
                delete = requests.delete(
                    f"{URL}/foods/{key}.json"
                )  # check node for final implementation

                if delete.status_code == 200:
                    print(f"Item with key {key} deleted successfully.")
                else:
                    print(f"Failed to delete item with key {key}.")
        else:
            print("Failed to retrieve data from the database.")
    return


# UPDATE EQUAL TO
def updateEqual(attribute, val, new, glb_db):
    for i in range(5):
        URL = f"{glb_db[i]}"
        response = requests.get(f'{URL}/foods.json?orderBy="{attribute}"&equalTo={val}')
        if response.status_code == 200:
            data = response.json()
            for item in data:
                data[item][attribute] = new
                requests.put(f"{URL}/foods/{item}.json", json=data[item])


# UPDATE GREATER TO
def updateGreater(attribute, val, new, glb_db):
    for i in range(5):
        URL = f"{glb_db[i]}"
        response = requests.get(
            f'{URL}/foods.json?orderBy="{attribute}"&startAt={val + 1}'
        )
        if response.status_code == 200:
            data = response.json()
            for item in data:
                data[item][attribute] = new
                requests.put(f"{URL}/foods/{item}.json", json=data[item])


def updateLesser(attribute, val, new, glb_db):
    for i in range(5):
        URL = f"{glb_db[i]}"
        response = requests.get(
            f'{URL}/foods.json?orderBy="{attribute}"&endAt={val - 1}'
        )
        if response.status_code == 200:
            data = response.json()
            for item in data:
                data[item][attribute] = new
                requests.put(f"{URL}/foods/{item}.json", json=data[item])
