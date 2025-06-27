# Deploy DoED Agentic App

## Deploy Chroma

```
oc new-project chroma
helm repo add chroma https://amikos-tech.github.io/chromadb-chart/
helm repo update
helm search repo chroma/
helm install chroma chroma/chromadb
oc expose service chroma-chromadb
```