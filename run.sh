#!/run/current-system/sw/bin/sh

MODEL_NAME="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

vllm serve $MODEL_NAME --tensor-parallel-size 1 --max-model-len 32768 --enforce-eager

