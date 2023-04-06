
# Data models for INTEGRITY research project

These data models are defined using openapi schema YAML format, either manually or trough automatic conversions. YAML format can be converted to context files to be used with NGSI-LD context brokers with the instructions in `Converting.md`.

The models are work in progress and are not yet meant to be usable outside of the [INTEGRITY](https://www.suscrop.eu/funded-projects/3rd-call/integrity) project.

## Some information

### Field and farm basic information

Models in `models/Fields.yaml` have been defined manually.

### Crop management and soil

Models in `models/ICASAModels.yaml` are converted from AgMIP ICASA Terraref ontology: https://terraref.github.io/icasa/1.0-alpha/core/. Some NGSI-LD specific fields are added in the conversion, see: `scripts/icasa2yaml.py`.

### Livestock and feed models

Models in `models/AnimalModels.yaml` have been defined manually, ATOL and EHOL ontologies have been used to the terms where possible.

### Combine all models to one schema

Combine, generate NGSI-LD context and pydantic models.

```bash
python3 scripts/merge_yaml_schemas.py models/*.yaml
datamodelgen ngsi -i integrity.yaml > integrity-ngsi.jsonld
datamodel-codegen --input integrity.yaml --output notebooks/integritymodels.py
```