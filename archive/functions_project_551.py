import requests

'''
The following function will delete any entries where the ----- attribute is 
EQUAL TO ------ value. These "blanks" will serve as the parameters to the function.
'''

# CHANGE NODE.JSON TO THE ACTUAL PATH --> wasn't too sure, ask group
def deleteAll(attribute, val):
	for i in range(5):
		URL = f'{DATABASE_URLS[i]}'

		response = requests.get(f"{URL}/node.json?orderBy=\"{attribute}\"&equalTo={val}")

		if response.status_code == 200:
		    data = response.json()
		    
		    for key in data:
		        delete = requests.delete(f"{URL}/your_node/{key}.json")
		        
		        if delete.status_code == 200:
		            print(f"Item with key {key} deleted successfully.")
		        else:
		            print(f"Failed to delete item with key {key}.")
		else:
		    print("Failed to retrieve data from the database.")
	return

'''
The following function will delete any entries where the ----- attribute is GREATER THAN ------ value. These "blanks" will serve as the parameters to the function.
'''

# CHANGE NODE.JSON TO THE ACTUAL PATH --> wasn't too sure, ask group
def deleteGreater(attribute, val):
	for i in range(5):
		URL = f'{DATABASE_URLS[i]}'

		response = requests.get(f"{URL}/node.json?orderBy=\"{attribute}\"&startAt={val}")

		if response.status_code == 200:
		    data = response.json()
		    
		    for key in data:
		        delete = requests.delete(f"{URL}/your_node/{key}.json")
		        
		        if delete.status_code == 200:
		            print(f"Item with key {key} deleted successfully.")
		        else:
		            print(f"Failed to delete item with key {key}.")
		else:
		    print("Failed to retrieve data from the database.")
	return


'''
The following function will delete any entries where the ----- attribute is LESS THAN ------ value. These "blanks" will serve as the parameters to the function.
'''

# CHANGE NODE.JSON TO THE ACTUAL PATH --> wasn't too sure, ask group
def deleteLesser(attribute, val):
	for i in range(5):
		URL = f'{DATABASE_URLS[i]}'

		response = requests.get(f"{URL}/node.json?orderBy=\"{attribute}\"&endAt={val - 1}")

		if response.status_code == 200:
		    data = response.json()
		    
		    for key in data:
		        delete = requests.delete(f"{URL}/your_node/{key}.json")
		        
		        if delete.status_code == 200:
		            print(f"Item with key {key} deleted successfully.")
		        else:
		            print(f"Failed to delete item with key {key}.")
		else:
		    print("Failed to retrieve data from the database.")
	return


# UPDATE EQUAL TO
def updateEqual(attribute, val, new):
	for i in range(5):
		URL = f'{DATABASE_URLS[i]}'
		response = requests.get(f"{URL}/node.json?orderBy=\"{attribute}\"&equalTo={val}")
		if response.status_code == 200:
			data = response.json()
			for item in data:
				data[item][attribute] = new
				update = requests.put(f"{URL}/node/{item}.json", json=data[item])
	return

# UPDATE GREATER TO
def updateGreater(attribute, val, new):
	for i in range(5):
		URL = f'{DATABASE_URLS[i]}'
		response = requests.get(f"{URL}/node.json?orderBy=\"{attribute}\"&startAt={val + 1}")
		if response.status_code == 200:
			data = response.json()
			for item in data:
				data[item][attribute] = new
				update = requests.put(f"{URL}/node/{item}.json", json=data[item])
	return


def updateLesser(attribute, val, new):
	for i in range(5):
		URL = f'{DATABASE_URLS[i]}'
		response = requests.get(f"{URL}/node.json?orderBy=\"{attribute}\"&endAt={val - 1}")
		if response.status_code == 200:
			data = response.json()
			for item in data:
				data[item][attribute] = new
				update = requests.put(f"{URL}/node/{item}.json", json=data[item])
	return





