
import numpy as np
from scipy import misc
import os
import scipy.io
from PIL import Image
import numpy as np
import cv2
from imageio import imread,imwrite,imsave

## detection_lesion_example using the data we have trained
def filter(base_root, crops_list='crops_LiTS_gt2.txt', input_config='masked_out_lesion', results_list='det_lesion', th=0.5):
#def filter(base_root, crops_list='crops_LiTS_gt_2.txt', input_config='masked_out_lesion', results_list='det_lesion', th=0.5):
    #crops_list = base_root + '/utils/crops_list/' + crops_list
    crops_list1 = os.path.join(base_root ,'utils','crops_list',crops_list)
    #results_list = base_root + '/detection_results/' + results_list + '/soft_results.txt'
    results_list = os.path.join(base_root,'detection_results',results_list,'soft_results.txt')

    if crops_list1 is not None:
        with open(crops_list1) as t:
            crops_lines = t.readlines()

    #input_results_path = base_root + '/results/' + input_config
    input_results_path = os.path.join(base_root,'results',input_config)
    #output_results_path = base_root + '/results/det_' + input_config
    output_results_path = os.path.join(base_root,'results','det_' + input_config)

    if not os.path.exists(os.path.join(output_results_path)):
        os.makedirs(os.path.join(output_results_path))

    if results_list is not None:
        with open(results_list) as t:
            results_lines = t.readlines()  ###################### SOFT_RESULTS --> need to follow this and make sure it can read full path. 

    for i in range(105, 131):
            ######################################################
            folder_name = str(i)
            images = []
            
            #nm = folder_name + '/'
            nm = os.path.join('images_volumes',folder_name)
            for x in results_lines:
                if nm in x:
                    images.append(x)

            slices_names = []

            if not os.path.exists(os.path.join(output_results_path, folder_name)):
                os.makedirs(os.path.join(output_results_path, folder_name))

            for j in range(len(images)):
                ################################################# does this work? or do web need to alter to just dir_name and slice?
                slices_names.append(images[j].split()[0])
                ### previously this would have just been /directory/image (ie, 105/301)

            unique_slices_names = np.unique(slices_names)
            for x in range(len(unique_slices_names)):
                total_mask = []
                for l in range(len(slices_names)):
                    if slices_names[l] == unique_slices_names[x]:
                        if float(images[l].split()[3]) < th:
                            print(images[l])
                            print('is negative')                           
                        if float(images[l].split()[3]) > th:
                            print(images[l])
                            print('is positive')
                            aux_mask = np.zeros([512, 512])
                            x_bb = int(float(images[l].split()[1]))
                            y_bb = int(float(images[l].split()[2].split('\n')[0]))
                            #########################################################
                            #######################################################
                            aux_name = images[l].split()[0] + '.png'
                            ################################################################
                            fname = os.path.basename(aux_name) # get file name out
                            dname = os.path.dirname(aux_name) # get directory name
                            dname = os.path.basename(dname) # get directory name
                            ##################################################################
                            aux_name = os.path.join(dname,fname)
                            ##################################################################
                            total_patch = (np.array(Image.open(os.path.join(input_results_path, aux_name)), dtype=np.uint8))/255.0
                            #########################################################################################################
                            cropped_patch = total_patch[x_bb: (x_bb + 80), y_bb:(y_bb + 80)]
                            aux_mask[x_bb: (x_bb + 80), y_bb:(y_bb + 80)] = cropped_patch
                            total_mask.append(aux_mask)
                if len(total_mask) > 0:
                    if len(total_mask) > 1:
                        summed_mask = np.sum(total_mask, axis=0)
                    else:
                        summed_mask = np.array(total_mask)[0]

                    thresholded_total_mask = np.greater(total_mask, 0.0).astype(float)
                    summed_thresholded_total_mask = np.sum(thresholded_total_mask, axis= 0)
                    summed_thresholded_total_mask[summed_thresholded_total_mask == 0.0] = 1.0
                    summed_mask = np.divide(summed_mask, summed_thresholded_total_mask)
                    summed_mask = summed_mask*255.0
                    #################################################################
                    #info = np.iinfo(summed_mask.dtype) # Get the information of the incoming image type
                    #summed_mask = summed_mask.astype(np.float64) / info.max # normalize the data to 0 - 1
                    #summed_mask = 255 * summed_mask # Now scale by 255
                    #summed_mask = summed_mask.astype(np.uint8)
                    
                    ###################################################################

                    
                    ##################################################################
                    
                    
                    ##############################################################
                    #############################################################
                    name = unique_slices_names[x].split('.')[0] + '.png'
                    ##############################################################
                    fname = os.path.basename(name) # get file name out
                    dname = os.path.dirname(name) # get directory name
                    dname = os.path.basename(dname) # get directory name
                    ##############################################################
                    name = os.path.join(dname,fname)
                    ##############################################################
                    print("Saving")
                    print(os.path.join(output_results_path, name))
                    output_results_plus_dir_name = os.path.join(output_results_path,dname,fname)
                    imsave(output_results_plus_dir_name, summed_mask)

    for i in range(len(crops_lines)):
            result = crops_lines[i].split(' ')
            if len(result) > 2:
                id_img, bool_zoom, mina, maxa, minb, maxb  = result
            else:
                id_img, bool_zoom = result

            #if int(id_img.split('/')[-2]) > 104:
            if int(os.path.split(id_img)[0]) > 104:
                fname = os.path.join(os.path.split(id_img)[1]+'.png')
                dname = os.path.dirname(id_img)
                output_results_plus_dir_name = os.path.join(output_results_path,dname,fname)
                #if not os.path.exists(os.path.join(output_results_path, id_img + '.png')):
                if not os.path.exists(output_results_plus_dir_name):
                    mask = np.zeros([512, 512])
                    #misc.imsave(os.path.join(output_results_path, id_img + '.png'), mask)
                    imsave(output_results_plus_dir_name, mask)
