import requests


def getEqual(filt_field, filt_val, db):
    url = f'{db}foods.json?orderBy="{filt_field}"&equalTo={filt_val}'
    response = requests.get(url)
    response.raise_for_status()  # raise error if req not successful
    return response.json()


def getGreater(filt_field, filt_val, db):
    url = f'{db}foods.json?orderBy="{filt_field}"&startAt={filt_val + 1}'
    response = requests.get(url)
    response.raise_for_status()  # raise error if req not successful
    return response.json()


def getLesser(filt_field, filt_val, db):
    url = f'{db}foods.json?orderBy="{filt_field}"&endAt={filt_val - 1}'
    response = requests.get(url)
    response.raise_for_status()  # raise error if req not successful
    return response.json()
