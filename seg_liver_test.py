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
import numpy as np
root_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(root_folder))
import seg_liver as segmentation
from dataset.dataset_seg import Dataset

number_slices = 3

#task_name = 'seg_liver_ck'
# This was actually saved as seg_liver from seg_liver_train.py
task_name = 'seg_liver'

database_root = os.path.join(root_folder, 'LiTS_database')
logs_path = os.path.join(root_folder, 'train_files', task_name, 'networks')
result_root = os.path.join(root_folder, 'results')

#model_name = os.path.join(logs_path, "seg_liver.ckpt")
# The last saved checkpoint from seg_liver_train.py
model_name = os.path.join(logs_path, "seg_liver.ckpt-50000")


## Computer_3D_bbs_from_gt_liver.py requires running testing_volume_3 then training_volume_3 so that you have segmented the entire dataset. 
#test_file = os.path.join(root_folder, 'seg_DatasetList/testing_volume_3.txt')
test_file = os.path.join(root_folder, 'seg_DatasetList/training_volume_3.txt')

# once completed, will need to move this directory as indicated in the readme file.
# copy 'seg_liver' from results folder to the LiTS_database


dataset = Dataset(None, test_file, None, database_root, number_slices, store_memory=False)

result_path = os.path.join(result_root, task_name)
checkpoint_path = model_name

## As is, line 54 (segmentation.test...) throws an error: 
#ValueError: Variable seg_liver/conv1/conv1_1/weights already exists, disallowed. Did you mean to set reuse=True or reuse=tf.AUTO_REUSE in VarScope? Originally defined at:

# Adding the following line seems to resolve the problem:
tf.reset_default_graph() 

segmentation.test(dataset, checkpoint_path, result_path, number_slices)
