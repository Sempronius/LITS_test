import numpy as np
from scipy import misc
import os
import glob
import math
from imageio import imread,imwrite,imsave

def numerical_sort(value):
    #return int(value.split('.png')[0].split('/')[-1])
    return int(value.split('.png')[0].split('\\')[-1])


def mask(base_root, labels_path, input_config='out_lesion', th=0.5):

    #results_path = base_root + '/results/'
    results_path = os.path.join(base_root , 'results')

    input_images_path = os.path.join(results_path,input_config)
    output_images_path = os.path.join(results_path , 'masked_' + input_config)

    masks_folders = os.listdir(input_images_path)

    if not os.path.exists(os.path.join(output_images_path)):
        os.makedirs(os.path.join(output_images_path))
    for i in range(len(masks_folders)):
        if 1:
            if not masks_folders[i].startswith(('.', '\t')):
                dir_name = masks_folders[i]
                masks_of_volume = glob.glob(os.path.join(input_images_path, dir_name + '/*.png'))
                file_names = (sorted(masks_of_volume, key=numerical_sort))
                depth_of_volume = len(masks_of_volume)
                if not os.path.exists(os.path.join(output_images_path, dir_name)):
                    os.makedirs(os.path.join(output_images_path, dir_name))

            for j in range(0, depth_of_volume):
                img = imread(file_names[j])
                img = img/255.0


                fname = os.path.basename(file_names[j])
                #original_label = misc.imread(os.path.join(labels_path, dir_name, file_names[j].split('.png')[0].split('/')[-1] + '.png'))
                #original_label = imread(os.path.join(labels_path, dir_name, file_names[j].split('.png')[0].split('\\')[-1] + '.png'))
                original_label = imread(os.path.join(labels_path, dir_name, fname))
                
                
                original_label = original_label/255.0
                original_label[np.where(original_label > th)] = 1
                original_label[np.where(original_label < th)] = 0
                img[np.where(original_label == 0)] = 0
                ## Added to avoid lossy error:
                #img = img.astype(np.uint8)

                #misc.imsave(os.path.join(output_images_path,  dir_name,  file_names[j].split('.png')[0].split('/')[-1] + '.png'), img)
                #imsave(os.path.join(output_images_path,  dir_name,  file_names[j].split('.png')[0].split('\\')[-1] + '.png'), img)
                print("Mask with Liver, saving:")
                print(os.path.join(output_images_path,  dir_name,  fname))
                imsave(os.path.join(output_images_path,  dir_name,  fname), img)