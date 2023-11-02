import json

def fetch_value(filename, key):
    with open(filename, "r") as f:
        data = json.load(f)
        return data[key]

def fetch_convar(key):
    return fetch_value("../common/json/config.json", key)


def fetch_constant(key):
    return fetch_value("../common/json/constants.json", key)
