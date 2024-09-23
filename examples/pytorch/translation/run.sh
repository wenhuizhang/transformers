#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install required Python packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the translation script
echo "Running translation model training and evaluation..."
python run_translation.py \
    --model_name_or_path t5-small \
    --do_train \
    --do_eval \
    --source_lang en \
    --target_lang ro \
    --dataset_name wmt16 \
    --dataset_config_name ro-en \
    --output_dir /tmp/tst-translation \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --overwrite_output_dir \
    --predict_with_generate

echo "Script completed successfully."

