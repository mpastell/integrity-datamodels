
# Convert atol to json-ld using Apache Jena:

```
riot --output=JSONLD atol.rdf > example.jsonld
python3 rdf_to_ngsi.py
```

ICASA

```
riot --output=RDFXML icasa-mgmt-info.owl > icasa.rdf
riot --output=JSONLD icasa-mgmt-info.owl > icasa.jsonld
```
