from jproperties import Properties
import os
import json


def read_properties(keys):
    config_filepath = os.path.join(os.getcwd(),'data','config.properties')
    prop = Properties()
    with open(config_filepath, 'rb') as config_file:
        prop.load(config_file)
    return prop.properties[keys]

def read_json(filename):
    base_path =os.path.join(os.getcwd())
    json_path = f"{base_path}/data/{filename}.json"
    with open(json_path,'r') as file:
        data = json.load(file)
    return data    