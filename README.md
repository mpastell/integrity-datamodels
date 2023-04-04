
# Data models for INTEGRITY research project

These data models are defined using openapi schema YAML format, either manually or trough automatic conversions. YAML format can be converted to context files to be used with NGSI-LD context brokers with the instructions in `Converting.md`.

The models are work in progress and are not yet meant to be usable outside of the [INTEGRITY](https://www.suscrop.eu/funded-projects/3rd-call/integrity) project.

## Some information

### Crop management and soil

Models in `models/ICASAModels.yaml` are converted from AgMIP ICASA Terraref ontology: https://terraref.github.io/icasa/1.0-alpha/core/. Some NGSI-LD specific fields are added in the conversion, see: `scripts/icasa2yaml.py`.

### Livestock and feed models

Models in `models/AnimalModels.yaml` have been defined manually, ATOL and EHOL ontologies have been used to the terms where possible.

