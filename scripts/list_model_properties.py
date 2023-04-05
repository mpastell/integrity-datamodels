
#%%
import os
from prance import ResolvingParser
import json

yaml_file_path = "integrity.yaml"
parser = ResolvingParser(yaml_file_path, strict=False)


# %%
#data = json.loads(parser.json())
data = parser.specification
schemas = data["components"]["schemas"]

# %%
import flatdict
entities = list(schemas.keys())
ent = entities[0]
properties = schemas[ent]

#for entity in entities:

# %%

expanded_yaml = parser.specification

def find_properties(data, key="properties", path=""):
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = f"{path}.{k}" if path else k
            if k == key:
                yield (new_path, v)
            else:
                yield from find_properties(v, key, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            yield from find_properties(item, key, new_path)

properties = dict(find_properties(expanded_yaml))

for path, prop in properties.items():
    #print(f"Path: {path}")
    #print(f"Properties: {prop}")
    for k,v in prop.items():
        print(k)
        if "description" in v:
            #print(f"{prop}")
            d = v['description']
            print(f"\tDescription: {d}")
    print()


# %%