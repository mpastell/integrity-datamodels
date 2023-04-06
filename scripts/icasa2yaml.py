# Convert ICASA classes from ICASA OWL to YAML files
#
# https://terraref.github.io/icasa/1.0-alpha/core/
# https://github.com/terraref/icasa

# %%
from collections import OrderedDict
from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import OWL
import yaml
#import owlrl

# From https://terraref.github.io/icasa/1.0-alpha/core/icasa-mgmt-info.owl
ontology_file = "../ontologies/icasa-mgmt-info.owl"
graph = Graph()
graph.parse(ontology_file, format="xml")  # use "xml" for RDF/XML format or "turtle" for Turtle format
yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

#%%

def owl_class_to_yaml(class_iri, graph):
    """Convert OWL class to YAML in OpenAPI schema format"""
    #class_iri = URIRef("http://purl.org/icasa/core#FertilizerApplication")
    class_name = str(graph.value(class_iri, RDFS.label))
    properties = OrderedDict()
    # Iterate over properties that have the specific class in their domain
    for property_iri, domain_iri in graph.subject_objects(predicate=RDFS.domain):
        if str(domain_iri) == str(class_iri):
            comments = [comment for comment in graph.objects(property_iri, RDFS.comment)]
            labels = [str(label) for label in graph.objects(property_iri, RDFS.label)]
            prop = {"description" : str(comments[0])}
            prop_name = labels[-1]
            prop["externalDocs"] = {"url" : str(property_iri)}
            prop["x-ngsi"] = {"uri" : str(property_iri)}
            properties[prop_name] = prop
    comments = [comment for comment in graph.objects(URIRef(class_iri), RDFS.comment)]

    model = {class_name : {
        "description" : "".join(comments),
        "properties" : properties}}

    #with open(f"../models/ICASA/{class_name}.yaml", "w") as yaml_file:
    #    yaml.dump(model, yaml_file, default_flow_style=False)
    return model

def management_class_to_yaml(class_iri, graph):
    """Convert ICASA field management action from OWL class to YAML in OpenAPI schema format
    with added fields.
    """

    class_name = str(graph.value(class_iri, RDFS.label))
    properties = OrderedDict()

    # Additional properties from smart data models agriparcel operation
    properties["agriparcel"] = {"description" : "Reference to the AgriParcel",
                                "x-ngsi" : {"type" : "Relationship"}}
    properties["category"] = {"description" : "Constant `ManagementActivity` used for querying all operations"}
    properties["dateObserved"] = {"description" : "Date when the operation was executed"}

    if class_name == "Planting":
        properties["genotype"] = {"description" : "Reference to genotype http://purl.org/icasa/core#Genotype"}

    # Iterate over properties that have the specific class in their domain
    for property_iri, domain_iri in graph.subject_objects(predicate=RDFS.domain):
        if str(domain_iri) == str(class_iri):
            comments = [comment for comment in graph.objects(property_iri, RDFS.comment)]
            labels = [str(label) for label in graph.objects(property_iri, RDFS.label)]
            prop = {"description" : str(comments[0])}
            prop_name = labels[-1]
            prop["externalDocs"] = {"url" : str(property_iri)}
            prop["x-ngsi"] = {"uri" : str(property_iri)}
            properties[prop_name] = prop
    comments = [comment for comment in graph.objects(URIRef(class_iri), RDFS.comment)]
    del properties["id"]

    model = {class_name : {
        "description" : "".join(comments),
        "properties" : properties}}

    #with open(f"../models/ICASA/{class_name}.yaml", "w") as yaml_file:
        #yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))
        #yaml.dump(model, yaml_file, default_flow_style=False)

    return model


models = OrderedDict()

#%%
# Convert field management data models YAML
mgmt_names = ["FertilizerApplication", "HarvestEvent", "Planting",
              "IrrigationApplication", "OrganicMaterialApplication",
              "TillageEvent"]

for class_iri in graph.subjects(RDF.type, OWL.Class):
    class_name = str(graph.value(class_iri, RDFS.label))
    if class_name in mgmt_names:
        m = management_class_to_yaml(class_iri, graph)
        models.update(m)

#%%
# Other classes to be converted as is
other_names = ["Genotype", "Soil", "SoilProfile", "SoilProfileLayer"]

# Iterate over class iris and convert to yaml files
for class_iri in graph.subjects(RDF.type, OWL.Class):
    class_name = str(graph.value(class_iri, RDFS.label))
    if class_name in other_names:
        m = owl_class_to_yaml(class_iri, graph)
        models.update(m)


doc = OrderedDict()
doc["components"] = {"schemas" : models}
doc["info"] = {"description": "Model Definitions for INTEGRITY research project",
                "title": "ICASE converted data models",
                "version": "0.0.1"}
doc["openapi"] = "3.0.0"
doc["paths"] = {}

with open("../models/ICASAModels.yaml", "w") as yaml_file:
    yaml_file.write("---\n")
    yaml.dump(doc, yaml_file, default_flow_style=False)
