#!/bin/bash
set -e

# Validar argumento
if [[ -z "$1" ]]; then
  echo "❌ Debes proporcionar el nombre de la función a desplegar (ej: ./deploy.sh asma_extract)"
  exit 1
fi

FUNC="$1"
REGION="us-central1"
RUNTIME="python311"
MEMORY="1024MB"

FUNC_PATH="functions/$FUNC/main.py"

# Verificar existencia del archivo
if [[ ! -f "$FUNC_PATH" ]]; then
  echo "❌ No se encontró $FUNC_PATH — no se puede desplegar $FUNC"
  exit 1
fi

echo "📤 Desplegando $FUNC..."

gcloud functions deploy "$FUNC" \
  --entry-point "$FUNC" \
  --runtime "$RUNTIME" \
  --trigger-http \
  --allow-unauthenticated \
  --region="$REGION" \
  --memory="$MEMORY" \
  --source .

echo "✅ $FUNC desplegada correctamente"
