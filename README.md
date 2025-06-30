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

## Deploy App

```
source .env
oc new-build --binary --strategy=docker --name $APP_NAME
oc start-build $APP_NAME --from-dir . --follow
oc new-app -i $APP_NAME:latest -e VLLM_TARGET_DEVICE=$VLLM_TARGET_DEVICE -e CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES -e GRANITE_API_KEY=$GRANITE_API_KEY -e GRANITE_API_BASE=$GRANITE_API_BASE -e TAVILY_API_KEY=$TAVILY_API_KEY
oc expose deploy $APP_NAME
oc expose service $APP_NAME
```