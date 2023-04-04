datamodelgen ngsi -i integrity.yaml > context-ngsi.jsonld
NGPOD=$(microk8s kubectl get pods -o=name |  sed "s/^.\{4\}//" | grep nginx)
microk8s kubectl cp context-ngsi.jsonld $NGPOD:/app
