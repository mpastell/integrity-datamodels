#%%
from prance.util import resolver #version '0.22.2.22.0'
from prance.util.formats import parse_spec
from collections import OrderedDict
import os
import sys
import yaml
yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))


#%%
def read_schemas(yaml_file):
    spec_string = open(yaml_file).read()
    spec = parse_spec(spec_string, yaml_file)
    url = os.path.split(os.path.abspath(yaml_file))[0]
    r = resolver.RefResolver(spec, url=url)
    r.resolve_references()
    return r.specs["components"]["schemas"]

if __name__ == "__main__":
    files = sys.argv[1:]
    models = OrderedDict()
    for yaml_file in files:
        m = read_schemas(yaml_file)
        for mdl in m.keys():
            # Add id and type fields if missing
            if "id" not in m[mdl]["properties"] :
                m[mdl]["properties"]["id"] = {"description" : "nglsi-id id"}
                if "required" in m[mdl]:
                    m[mdl]["required"].append("id")
                else:
                    m[mdl]["required"] = ["id"]
            if "type" not in m[mdl]["properties"]:
                m[mdl]["properties"]["type"] = {"description" : f"nglsi-id type, has to be {mdl}"}
                if "required" in m[mdl]:
                    m[mdl]["required"].append("type")
                else:
                    m[mdl]["required"] = ["type"]


        models.update(m)

    doc = OrderedDict()
    doc["components"] = {"schemas" : models}
    doc["info"] = {"description": "Model Definitions for INTEGRITY research project",
                "title": "INTEGRITY Data Models",
                "version": "0.0.1"}
    doc["openapi"] = "3.0.0"
    doc["paths"] = {}
    with open("integrity.yaml", "w") as yaml_file:
        yaml_file.write("---\n")
        yaml.dump(doc, yaml_file, default_flow_style=False)
    print("Combined schema written to integrity.yaml")
    #list(models.keys())





# %%
