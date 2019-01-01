import numpy as np
from scipy import misc
import os
import glob
import math
import scipy.io
from imageio import imread,imwrite

MIN_AREA_SIZE = 512.0*512.0

crops_list_name = 'crops_LiTS_gt_2.txt'

## Having to fix a lot of path issues here, as I am working in windows. trying to remove all slashes and let os.path put those in to avoid problems 
#database_root = '../../LiTS_database/'
database_root = os.path.join('..','..','LiTS_database')

#utils_path = '../crops_list/'
utils_path = os.path.join('..','crops_list')

#results_path = '../../results/'
results_path = os.path.join('..','..','results')

images_path = os.path.join(database_root, 'images_volumes')

#labels_path = os.path.join(database_root,  'item_seg/')
#labels_liver_path = os.path.join(database_root,  'liver_seg/')
labels_path = os.path.join(database_root,  'item_seg')
labels_liver_path = os.path.join(database_root,  'liver_seg')

output_images_path_bb = os.path.join(database_root, 'bb_images_volumes_alldatabase3_gt_nozoom_common_bb')
output_labels_path_bb = os.path.join(database_root,  'bb_liver_lesion_seg_alldatabase3_gt_nozoom_common_bb')
output_labels_liver_path_bb = os.path.join(database_root,  'bb_liver_seg_alldatabase3_gt_nozoom_common_bb')

#
#liver_results = os.path.join(database_root, 'seg_liver_ck/')
liver_results = os.path.join(database_root, 'seg_liver')

output_liver_results_path_bb = os.path.join(database_root, 'liver_results')

# This script computes the bounding boxes around the liver from the ground truth, computing
# a single 3D bb for all the volume.

if not os.path.exists(output_labels_path_bb):
    os.makedirs(output_labels_path_bb)
        
if not os.path.exists(output_images_path_bb):
    os.makedirs(output_images_path_bb)
        
if not os.path.exists(output_labels_liver_path_bb):
    os.makedirs(output_labels_liver_path_bb)

if not os.path.exists(output_liver_results_path_bb):
    os.makedirs(output_liver_results_path_bb)


def numerical_sort(value):
    return int(value)

def numerical_sort_path(value):
    file_name = os.path.basename(value)
    file_name = os.path.splitext(file_name)
    return int(file_name[0])
    #return int(value.split('.png')[0].split('/')[-1])
    #return int(value.split('.png')[0].split('\\')[1])

## If no labels, the masks_folder, should contain the results of liver segmentation
# masks_folders = os.listdir(results_path + 'liver_seg/')
masks_folders = os.listdir(labels_liver_path)
sorted_mask_folder = sorted(masks_folders, key=numerical_sort)

crops_file = open(os.path.join(utils_path, crops_list_name), 'w')
aux = 0


for i in range(len(masks_folders)):
    if not masks_folders[i].startswith(('.', '\t')):
        dir_name = masks_folders[i]
        ## If no labels, the masks_folder, should contain the results of liver segmentation
        
        
        masks_of_volume1 = os.path.join(labels_liver_path,dir_name,'*.png')
        masks_of_volume = glob.glob(masks_of_volume1)
        #masks_of_volume = glob.glob(labels_liver_path + dir_name + '/*.png')
        
        
        
        file_names = (sorted(masks_of_volume, key=numerical_sort_path))
        depth_of_volume = len(masks_of_volume)

    if not os.path.exists(os.path.join(output_labels_path_bb, dir_name)):
        os.makedirs(os.path.join(output_labels_path_bb, dir_name))
        
    if not os.path.exists(os.path.join(output_images_path_bb, dir_name)):
        os.makedirs(os.path.join(output_images_path_bb, dir_name))
        
    if not os.path.exists(os.path.join(output_labels_liver_path_bb, dir_name)):
        os.makedirs(os.path.join(output_labels_liver_path_bb, dir_name))

    if not os.path.exists(os.path.join(output_liver_results_path_bb, dir_name)):
        os.makedirs(os.path.join(output_liver_results_path_bb, dir_name))
        
    total_maxa = 0
    total_mina = 10000000
    
    total_maxb = 0
    total_minb = 10000000
        
    for j in range(0, depth_of_volume):
        #img = misc.imread(file_names[j])
        file_name = os.path.basename(file_names[j])
        file_name = os.path.splitext(file_name)
        dir_plus_filename = os.path.join(dir_name,file_name[0])
        img = imread(file_names[j])
        img = img/255.0
        img[np.where(img > 0.5)] = 1
        img[np.where(img < 0.5)] = 0
        a, b = np.where(img == 1)
        
        if len(a) > 0:

            maxa = np.max(a)
            maxb = np.max(b)
            mina = np.min(a)
            minb = np.min(b)
            
            if maxa > total_maxa:
                total_maxa = maxa
            if maxb > total_maxb:
                total_maxb = maxb
            if mina < total_mina:
                total_mina = mina
            if minb < total_minb:
                total_minb = minb
            
    for j in range(0, depth_of_volume):
        #img = misc.imread(file_names[j])
        file_name = os.path.basename(file_names[j])
        file_name = os.path.splitext(file_name)
        dir_plus_filename = os.path.join(dir_name,file_name[0])
        img = imread(file_names[j])
        img = img/255.0
        img[np.where(img > 0.5)] = 1
        img[np.where(img < 0.5)] = 0

        a, b = np.where(img == 1)
        
        if len(a) > 0:

            new_img = img[total_mina:total_maxa, total_minb:total_maxb]

        if len(np.where(img == 1)[0]) > 500:
            area = 1
            zoom = math.sqrt(MIN_AREA_SIZE/area)
            aux = 1
            
            #crops_file.write(file_names[j].split('.png')[0].split('liver_seg/')[-1] + ' ' + str(aux) + ' ' +
                             #str(total_mina) + ' ' + str(total_maxa) + ' ' + str(total_minb) + ' ' + str(total_maxb) + '\n')

            
            crops_file.write(dir_plus_filename + ' ' + str(aux) + ' ' +
                             str(total_mina) + ' ' + str(total_maxa) + ' ' + str(total_minb) + ' ' + str(total_maxb) + '\n')


            #original_img = np.array(scipy.io.loadmat(os.path.join(images_path, dir_name, file_names[j].split('.png')[0].split('/')[-1] + '.mat'))['section'], dtype = np.float32)
            #original_img = np.array(scipy.io.loadmat(os.path.join(images_path, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.mat'))['section'], dtype = np.float32)
            original_img = np.array(scipy.io.loadmat(os.path.join(images_path, dir_plus_filename + '.mat'))['section'], dtype = np.float32)
            o_new = original_img[total_mina:total_maxa, total_minb:total_maxb]

            #scipy.io.savemat(os.path.join(output_images_path_bb, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.mat'), mdict={'section': o_new})
            scipy.io.savemat(os.path.join(output_images_path_bb, dir_plus_filename + '.mat'), mdict={'section': o_new})
            
            masked_original_img = o_new
            masked_original_img[np.where(new_img == 0)] = 0
           
            #original_label = imread(os.path.join(labels_path, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.png'))
            original_label = imread(os.path.join(labels_path, dir_plus_filename + '.png'))
            lbl_new = original_label[total_mina:total_maxa, total_minb:total_maxb]

            #misc.imsave(os.path.join(output_labels_path_bb, dir_name, file_names[j].split('.png')[0].split('/')[-1] + '.png'), lbl_new)
            #imwrite(os.path.join(output_labels_path_bb, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.png'), lbl_new)
            imwrite(os.path.join(output_labels_path_bb, dir_plus_filename + '.png'), lbl_new)
            
            #original_liver_label = imread(os.path.join(labels_liver_path, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.png'))
            original_liver_label = imread(os.path.join(labels_liver_path, dir_plus_filename + '.png'))
            lbl_liver_new = original_liver_label[total_mina:total_maxa, total_minb:total_maxb]

            #misc.imsave(os.path.join(output_labels_liver_path_bb, dir_name,  file_names[j].split('.png')[0].split('\\')[1] + '.png'), lbl_liver_new)
            #imwrite(os.path.join(output_labels_liver_path_bb, dir_name,  file_names[j].split('.png')[0].split('\\')[1] + '.png'), lbl_liver_new)
            imwrite(os.path.join(output_labels_liver_path_bb, dir_plus_filename + '.png'), lbl_liver_new)

            
            #original_results_label = imread(os.path.join(liver_results, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.png'))
            res_liver_new = original_results_label[total_mina:total_maxa, total_minb:total_maxb]

            #misc.imsave(os.path.join(output_liver_results_path_bb, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.png'), res_liver_new)
            #imwrite(os.path.join(output_liver_results_path_bb, dir_name, file_names[j].split('.png')[0].split('\\')[1] + '.png'), res_liver_new)
            imwrite(os.path.join(output_liver_results_path_bb, dir_plus_filename + '.png'), res_liver_new)
           
            #print(dir_name, file_names[j].split('.png')[0].split('\\')[1])

        else:
            aux = 0
            #crops_file.write(file_names[j].split('.png')[0].split('liver_seg/')[-1]  + ' ' + str(aux) + '\n')
            crops_file.write(dir_plus_filename + ' ' + str(aux) + '\n')


crops_file.close()
