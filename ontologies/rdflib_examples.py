#%%
import json
from rdflib import Graph
from rdflib.serializer import Serializer
g = Graph().parse("icasa.rdf")
#json_ld = g.serialize(format='json-ld', indent=4)
#json.loads(json_ld)[0]

for subj, pred, obj in g:
    print(f"{subj} : {obj}")
#%%
from rdflib import Graph
import json
import pyld

# Load the RDF data into an rdflib graph
g = Graph().parse("atol.rdf")

# Serialize the graph to JSON-LD format
#json_ld = g.serialize(format='json-ld', indent=4)
# Compact the JSON-LD document using the context provided by the graph
# Not working, from ChatGPT -> gives the right idea
#compacted = json.loads(json_ld)
#compacted = pyld.jsonld.compact(compacted, json.loads(context))
# Print the resulting JSON-LD document
#print(json.dumps(compacted, indent=4))

# %%
from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import OWL
import owlrl
#ontology_file = "icasa-mgmt-info.owl"
ontology_file = "atol.owl"
graph = Graph()
graph.parse(ontology_file, format="xml")  # use "xml" for RDF/XML format or "turtle" for Turtle format
# Get IRIs
#owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=True, datatype_axioms=True).expand(graph)
#%%
idx = 0
for class_iri in graph.subjects(RDF.type, OWL.Class):
    labels = [str(label) for label in graph.objects(URIRef(class_iri), RDFS.label)]
    comments = [str(comment) for comment in graph.objects(URIRef(class_iri), RDFS.comment)]
    print(class_iri)
    print("Label ", labels)
    print("Comments " , comments)

    idx += 1
    if idx > 2:
        break

# %%
# How can I get "In domain of" variables
from rdflib.namespace import OWL, RDFS
import yaml
# Define the class IRI you want to check the domain for
#class_iri = "http://opendata.inra.fr/ATOL/ATOL_0002161"

class_name = "FertilizerApplication"
class_iri = f"http://purl.org/icasa/core#{class_name}"

properties = {}
# Iterate over properties that have the specific class in their domain
for property_iri, domain_iri in graph.subject_objects(predicate=RDFS.domain):
    if str(domain_iri) == class_iri:
        # print(f"Property {property_iri} has domain {class_iri}")
        # Get the property labels (rdfs:label)
        #labels = [label for label in graph.objects(property_iri, RDFS.label)]
        comments = [comment for comment in graph.objects(property_iri, RDFS.comment)]
        #print(f"Property IRI: {property_iri}")
        #print(f"Labels: {', '.join([str(label) for label in labels])}")
        labels = [str(label) for label in graph.objects(property_iri, RDFS.label)]
        prop = {"description" : str(comments[0])}
        prop_name = labels[-1]
        prop["externalDocs"] = {"url" : str(property_iri)}
        properties[prop_name] = prop
from rdflib import Graph, Namespace, RDF, RDFS, URIRef
comments = [comment for comment in graph.objects(URIRef(class_iri), RDFS.comment)]

model = {class_name : {
    "description" : "".join(comments),
    "properties" : properties}}

with open(f"../models/ICASA/{class_name}.yaml", "w") as yaml_file:
    yaml.dump(model, yaml_file, default_flow_style=False)

# %%
import yaml
from itertools import chain
from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.namespace import OWL
# Collect property IRIs and labels
properties = []
for property_iri in chain(
        graph.subjects(RDF.type, OWL.ObjectProperty),
        graph.subjects(RDF.type, OWL.DatatypeProperty)):
    labels = [str(label) for label in graph.objects(property_iri, RDFS.label)]

    properties.append({
        "iri": str(property_iri),
        "labels": labels
    })

# Write the properties to a YAML file
with open("properties.yaml", "w") as yaml_file:
    yaml.dump(properties, yaml_file, default_flow_style=False)



# %%
