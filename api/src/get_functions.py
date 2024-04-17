import requests


def getEqual(filt_field, filt_val, db):
    url = f'{db}foods.json?orderBy="{filt_field}"&equalTo={filt_val}'
    response = requests.get(url)
    response.raise_for_status()  # raise error if req not successful
    return response.json()


def getGreater(filt_field, filt_val, db):
    url = f'{db}foods.json?orderBy="{filt_field}"&startAt={int(filt_val) + 1}'
    response = requests.get(url)
    response.raise_for_status()  # raise error if req not successful
    return response.json()


def getLesser(filt_field, filt_val, db):
    url = f'{db}foods.json?orderBy="{filt_field}"&endAt={int(filt_val) - 1}'
    response = requests.get(url)
    response.raise_for_status()  # raise error if req not successful
    return response.json()


def apply_filters(data, filters):
    to_rem = []
    for val, filt, nutri in filters:
        print(f"NUTRI: \n{nutri}\n")
        for k, v in data.items():
            if filt == "less":
                if int(v[nutri]) > int(val):
                    print(f"k to remove: \n{k}\n")
                    to_rem.append(k)
            elif filt == "greater":
                if int(v[nutri]) < int(val):
                    to_rem.append(k)
            elif filt == "equal":
                if int(v[nutri]) != int(val):
                    to_rem.append(k)

    for k in list(set(to_rem)):
        del data[k]
    return data
