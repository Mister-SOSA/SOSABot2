import json

def get_convar(file_name: str, convar: str):
    try:
        with open(f'convars/{file_name}.json', encoding='utf-8') as f:
            data = json.load(f)
            return data[convar]

    except FileNotFoundError:
        raise FileNotFoundError(f"convars/{file_name}.json not found")
    
def set_convar(file_name: str, convar: str, value):
    try:
        with open(f'convars/{file_name}.json') as f:
            data = json.load(f)
            data[convar] = value
            
        with open(f'convars/{file_name}.json', 'w') as f:
            json.dump(data, f)
            
    except FileNotFoundError:
        raise FileNotFoundError(f"convars/{file_name}.json not found")
    
def clear_convar(file_name: str, convar: str):
    try:
        with open(f'convars/{file_name}.json') as f:
            data = json.load(f)
            data[convar] = None
            
        with open(f'convars/{file_name}.json', 'w') as f:
            json.dump(data, f)
            
    except FileNotFoundError:
        raise FileNotFoundError(f"convars/{file_name}.json not found")