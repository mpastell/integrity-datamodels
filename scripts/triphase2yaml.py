# Convert ICASA classes from ICASA OWL to YAML files
#
# https://terraref.github.io/icasa/1.0-alpha/core/
# https://github.com/terraref/icasa

# %%
from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import OWL
import yaml

# From https://terraref.github.io/icasa/1.0-alpha/core/icasa-mgmt-info.owl
#ontology_file = "../ontologies/triphase.rdf"
ontology_file = "../ontologies/atol.owl"
graph = Graph()
graph.parse(ontology_file)

#%%

classes = list(graph.subjects(RDF.type, OWL.Class))
labels = [graph.value(c, RDFS.label) for c in classes]

idx = 0
class_name = classes[0]
classes = {}

for property_iri, domain_iri in graph.subject_objects(predicate=RDFS.subClassOf):
    parent = f"{graph.value(domain_iri, RDFS.label)}"
    cls = f"{graph.value(property_iri, RDFS.label)}"
    if parent in classes:
        classes[parent].append(cls)
    else:
        classes[parent] = [cls]
        print(parent)
    print(f"\t{cls}")
    #print(f"{graph.value(property_iri, RDFS.label)}: {graph.value(domain_iri, RDFS.label)}")
    #idx += 1
    #if idx == 100:
    #    break




#%%

def owl_class_to_yaml(class_iri, graph):
    #class_iri = URIRef("http://purl.org/icasa/core#FertilizerApplication")
    class_name = str(graph.value(class_iri, RDFS.label))
    properties = {}
    # Iterate over properties that have the specific class in their domain
    for property_iri, domain_iri in graph.subject_objects(predicate=RDFS.isDefinedBy):
        if str(domain_iri) == str(class_iri):
            comments = [comment for comment in graph.objects(property_iri, RDFS.comment)]
            labels = [str(label) for label in graph.objects(property_iri, RDFS.label)]
            prop = {"description" : str(comments[0])}
            prop_name = labels[-1]
            prop["externalDocs"] = {"url" : str(property_iri)}
            properties[prop_name] = prop
    comments = [comment for comment in graph.objects(URIRef(class_iri), RDFS.comment)]

    model = {class_name : {
        "description" : "".join(comments),
        "properties" : properties}}
    return model

    #with open(f"../models/ICASA/{class_name}.yaml", "w") as yaml_file:
    #    yaml.dump(model, yaml_file, default_flow_style=False)

#%%
# Iterate ower class iri's and convert to yaml files
for class_iri in graph.subjects(RDF.type, OWL.Class):
    m = owl_class_to_yaml(class_iri, graph)
    break

# %%
