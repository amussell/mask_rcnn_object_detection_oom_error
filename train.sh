#!/bin/bash
python setup.py
OBJECT_DETECTION_DIR="$(python -c "import object_detection; import os; print(os.path.dirname(object_detection.__file__))")"
cd $OBJECT_DETECTION_DIR
PIPELINE_CONFIG_PATH=$HOME/tmp/mask_rcnn_object_detection_oom_error/configs/mask_rcnn_inception_v2.config
MODEL_DIR=$HOME/tmp/mask_rcnn_object_detection_oom_error/models/train_output/
NUM_TRAIN_STEPS=50000
SAMPLE_1_OF_N_EVAL_EXAMPLES=1
python model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr
