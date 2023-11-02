import json

def fetch_permission(value: int):
    with open("../common/json/permissions.json", "r") as f:
        data = json.load(f)
        return data[str(value)]
    
def fetch_all_permissions():
    with open("../common/json/permissions.json", "r") as f:
        data = json.load(f)
        return data

def max_permission_level():
    max_level = max(map(int, fetch_all_permissions().keys()))
    return fetch_permission(max_level)

def min_permission_level():
    min_level = min(map(int, fetch_all_permissions().keys()))
    return fetch_permission(min_level)
