# Deploy DoED Agentic App

## Deploy Chroma

```
oc new-project chroma
helm repo add chroma https://amikos-tech.github.io/chromadb-chart/
helm repo update
helm install chroma chroma/chromadb
oc expose service chroma-chromadb
```

## Build Custom Workbench Image

```
source .env
cd docker
podman build -t quay.io/oawofolurh/agentic-wb:latest .
podman push quay.io/oawofolurh/agentic-wb:latest
cd -
```

OR

```
oc new-build --name=data-prep-wb --to="quay.io/oawofolurh/agentic-wb:latest" --strategy=docker --binary
oc start-build data-prep-wb --from-dir docker --follow
```

## Deploy Workbench
* Use the image built above to import a new notebook image
	* Attach a GPU accelerator profile if one exists
2. When creating the workbench in the Web GUI Console:
	* Use the following script to generate the **wb-secret.yaml** file to attach to the workbench:
	
	```
	oc create secret generic data-prep-wb --from-env-file .env
	oc get secret data-prep-wb -oyaml > openshift/wb-secret.yaml
	
### Serving LLMs on Openshift AI
1. Install Minio: (see <a href="https://ai-on-openshift.io/tools-and-applications/minio/minio/#log-on-to-your-project-in-openshift-console" target="_blank">link</a>)

```zh
oc new-project minio --display-name="Minio S3 for LLMs"
oc apply -f k8s/minio/minio-all.yaml
```