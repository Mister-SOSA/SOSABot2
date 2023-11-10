import json

def fetch_value(filename, key):
    with open(filename, "r") as f:
        data = json.load(f)
        return data[key]

def fetch_convar(key):
    return fetch_value("../common/json/config.json", key)


def fetch_constant(key):
    return fetch_value("../common/json/constants.json", key)

def set_value(filename, key, value):
    with open(filename, "r+") as f:
        data = json.load(f)
        data[key] = value
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        
def set_convar(key, value):
    set_value("../common/json/config.json", key, value)
    
def set_constant(key, value):
    set_value("../common/json/constants.json", key, value)
    
def fetch_convars() -> dict:
    with open("../common/json/config.json", "r") as f:
        return json.load(f)
    
def fetch_convar_keys() -> list:
    return list(fetch_convars().keys())