#!/run/current-system/sw/bin/sh

MODEL_NAME="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

# check if PERSONALLLM_SERVER_KEY is set
if [ -z "$PERSONAL_LLM_SERVER_KEY" ]; then
  echo "Error: PERSONAL_LLM_SERVER_KEY is not set."
  exit 1
fi

vllm serve $MODEL_NAME \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --enforce-eager \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key $PERSONAL_LLM_SERVER_KEY

