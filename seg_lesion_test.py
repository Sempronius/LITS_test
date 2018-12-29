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
import seg_lesion as segmentation
from dataset.dataset_seg import Dataset
import utils.crop_to_image
import utils.mask_with_liver
import utils.det_filter

gpu_id = 0

number_slices = 3
# Test crops_LiTs (default)
#crops_list = 'crops_LiTS_gt.txt'
#crops list output from compute_3D_bbs_from_gt_liver.py --> This doesn't work. Something is wrong with how compute_3D_bbs is generating its cropsList file. 
crops_list = 'crops_LiTS_gt_2.txt'

# Changed to match task_name from 'det_lesion_test.py --> however this doesn't work. Something is wrong with det_lesion_test.py and the list it generates
#det_results_list = 'detection_lesion_example'
det_results_list = 'det_lesion'

#Changed to match task_name from seg_lesion_train.py
task_name = 'seg_lesion'



database_root = os.path.join(root_folder, 'LiTS_database')

liver_results_path = os.path.join(database_root, 'out_liver_results')
###########################################################
## There is not directory created call "out_liver_results". This must be the results from liver_seg, which are in the directory "liver_seg"
# SO, to make it work, we copy the contents of results\liver_seg (output from liver_seg.py) into the directory LiTsdatavase/out_liver_results, manually.
##########################################################
# maybe just try and direct it to the results/liver_seg ? Rather than copying the files manually? 


logs_path = os.path.join(root_folder, 'train_files', task_name, 'networks')
result_root = os.path.join(root_folder, 'results')
#Changed to match last trained checkpoint from seg_lesion_train.py
model_name = os.path.join(logs_path, "seg_lesion.ckpt-50000")

test_file = os.path.join(root_folder, 'seg_DatasetList/testing_volume_3_crops.txt')

dataset = Dataset(None, test_file, None, database_root, number_slices, store_memory=False)

result_path = os.path.join(result_root, task_name)
checkpoint_path = model_name

## As is, line 58 (segmentation.test...) throws an error: 
#ValueError: Variable seg_lesion/conv1/conv1_1/weights already exists, disallowed. Did you mean to set reuse=True or reuse=tf.AUTO_REUSE in VarScope? Originally defined at:
# Adding the following line seems to resolve the problem:
tf.reset_default_graph() 
segmentation.test(dataset, checkpoint_path, result_path, number_slices)

utils.crop_to_image.crop(base_root=root_folder, input_config=task_name, crops_list=crops_list)
utils.mask_with_liver.mask(base_root=root_folder, labels_path=liver_results_path, input_config='out_' + task_name, th=0.5)
utils.det_filter.filter(base_root=root_folder, crops_list=crops_list, input_config='masked_out_' + task_name,
                        results_list=det_results_list, th=0.33)



