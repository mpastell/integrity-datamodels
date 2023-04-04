
# Conversion from YAML to context, python etc.

These data models are defined using openapi schema YAML format, either manually or trough automatic conversions. YAML format can be converted to context file to be used with NGSI-LD context brokers using a command line tool adapted from: https://github.com/FIWARE/tutorials.Understanding-At-Context.


Install command line tool

```bash
npm install -g --production ./context-file-generator
```

Convert from YAML to context and documentation.

```
datamodelgen ngsi -i integrity.yaml > context-ngsi.jsonld
datamodelgen jsonld -i integrity.yaml > context-json.jsonld
datamodelgen markdown -i integrity.yaml > integrity.md
```

Copy to Kubernetes pod:

```
NGPOD=$(kubectl get pods -o=name |  sed "s/^.\{4\}//" | grep nginx)
kubectl cp context-ngsi.jsonld $NGPOD:/app
```

# Pydantic

Pydantic models can be generated from the definition:

````
pip install datamodel-code-generator
datamodel-codegen --input integrity.yaml --output models.py
```

Generate docs:

```
npm install @openapitools/openapi-generator-cli -g
openapi-generator-cli generate -i integrity.yaml -g html -o /tmp/test
```

> **Note:** The Data Models used here for `@context` generation are defined using OpenAPI 3.0
> [Swagger format](https://swagger.io/specification). To help with the generation of IRIs the specification has been
> extended with additional annotations as necessary. The `x-ngsi` attribute, as the name suggests is just a simple
> [Specification Extension](https://swagger.io/specification/#specificationExtensions) - usually it is not relevant to
> Swagger, and indeed you could generate a simple `@context` file without it, but the data held within in has been used
> to help generate a rich [`@graph`](https://w3c.github.io/json-ld-syntax/#dfn-graph-object) and more comprehensive
> documentation.
>
> The simple NGSI-LD `@context` generator in the tutorial defaults to using `uri.fiware.org` namespaces and updates with
> corrected URIs based on the `x-ngsi.uri` and `x-ngsi.uri-prefix` attributes. The code and defaults found within this
> tutorial can be altered if necessary.



