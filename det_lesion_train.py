"""
Original code from OSVOS (https://github.com/scaelles/OSVOS-TensorFlow)
Sergi Caelles (scaelles@vision.ee.ethz.ch)

Modified code for liver and lesion segmentation:
Miriam Bellver (miriam.bellver@bsc.es)
"""


import os
import sys
import tensorflow as tf
slim = tf.contrib.slim
root_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(root_folder))
import det_lesion as detection
from dataset.dataset_det_data_aug import Dataset

gpu_id = 0

# Training parameters
#batch_size = 64
batch_size = 128
iter_mean_grad = 2 
#iter_mean_grad = 1 
#max_training_iters = 5000
max_training_iters = 5000
## ********** LOOK AT DOING A TESNROFLOW GRAPH AND JUST FIND BEST CHECKPOINT ***************
save_step = 200
display_step = 2
#learning_rate = 0.001
learning_rate = 0.0001



task_name = 'det_lesion'

database_root = os.path.join(root_folder, 'LiTS_database')
logs_path = os.path.join(root_folder, 'train_files', task_name, 'networks')
resnet_ckpt = os.path.join(root_folder, 'train_files', 'resnet_v1_50.ckpt')
#### these can be created using util/samppling sample_bbs.py
#train_file_pos = os.path.join(root_folder, 'det_DatasetList', 'training_positive_det_patches_data_aug.txt')
#train_file_neg = os.path.join(root_folder, 'det_DatasetList', 'training_negative_det_patches_data_aug.txt')
#val_file_pos = os.path.join(root_folder, 'det_DatasetList', 'testing_positive_det_patches_data_aug.txt')
#val_file_neg = os.path.join(root_folder, 'det_DatasetList', 'testing_negative_det_patches_data_aug.txt')

## Using my results from sample_bbs, training accuracy was 98% but validation accuracy was 50-60%. 
train_file_pos = os.path.join(root_folder, 'det_DatasetList', 'training_positive_det_patches_example.txt')
train_file_neg = os.path.join(root_folder, 'det_DatasetList', 'training_negative_det_patches_example.txt')
val_file_pos = os.path.join(root_folder, 'det_DatasetList', 'testing_positive_det_patches_example.txt')
val_file_neg = os.path.join(root_folder, 'det_DatasetList', 'testing_negative_det_patches_example.txt')

dataset = Dataset(train_file_pos, train_file_neg, val_file_pos, val_file_neg, None, None, database_root=database_root,
                  store_memory=False)

# Train the network
with tf.Graph().as_default():
    with tf.device('/gpu:' + str(gpu_id)):
        global_step = tf.Variable(0, name='global_step', trainable=False)
        #detection.train(dataset, resnet_ckpt, learning_rate, logs_path, max_training_iters, save_step, display_step,
                        #global_step, iter_mean_grad=iter_mean_grad, batch_size=batch_size, finetune=0,
                        #resume_training=False)
        detection.train(dataset, resnet_ckpt, learning_rate, logs_path, max_training_iters, save_step, display_step,
                        global_step, iter_mean_grad=iter_mean_grad, batch_size=batch_size, finetune=0,
                        resume_training=False)

###################### NEED TO UPDATE DETECTION.TRAIN TO ONLY SAVE BEST VALIDATION ACCURACY
        # https://stackoverflow.com/questions/39252901/tensorflow-save-the-model-with-smallest-validation-error

