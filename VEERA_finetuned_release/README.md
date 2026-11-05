# VEERA Fine-tuned Checkpoint

Base model: Qwen/Qwen2.5-VL-3B-Instruct
Method: LoRA fine-tuning
Adapter: adapter_model.safetensors

This release contains the adapter, processor/tokenizer assets, experiment
summary, and saved baseline/fine-tuned evaluation predictions.

IMPORTANT:
- The full Qwen2.5-VL-3B-Instruct base model weights are NOT included.
- Download the base model separately when setting up local inference.
- This checkpoint has been evaluated for RePOPE-style yes/no VQA.
- Do not interpret the results as validation of evidence acquisition or
  abstention behavior.
