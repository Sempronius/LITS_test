import numpy as np
from scipy import misc
import os
from imageio import imread,imwrite,imsave

def crop(base_root, input_config='lesion',
         crops_list='crops_LiTS_gt2.txt'):
    
    crops_list = os.path.join(base_root,'utils','crops_list',crops_list)
    input_results_path = os.path.join(base_root,'results',input_config)
    output_results_path = os.path.join(base_root,'results','out_' + input_config)

    if crops_list is not None:
        with open(crops_list) as t:
            crops_lines = t.readlines()

    for i in range(len(crops_lines)):
            result = crops_lines[i].split(' ')

            if len(result) > 2:
                id_img, bool_zoom, mina, maxa, minb, maxb = result
                mina = int(mina)
                maxa = int(maxa)
                minb = int(minb)
                maxb = int(maxb.split('\n')[0])
            else:
                id_img, bool_zoom = result


            #print(int(id_img.split('/')[-2]))
            #print('int(os.path.split(id_img)[0])')
            #print(int(os.path.split(id_img)[0]))
            
            
            #if int(id_img.split('/')[-2]) > 104:
            if int(os.path.split(id_img)[0]) > 104:
 
                #print(not os.path.exists(os.path.join(output_results_path, id_img.split('/')[0])))
                #if not os.path.exists(os.path.join(output_results_path, id_img.split('/')[0])):

                if not os.path.exists(os.path.join(output_results_path, os.path.split(id_img)[0])):
                    os.makedirs(os.path.join(output_results_path, os.path.split(id_img)[0]))

                mask = np.zeros([512, 512])
                if bool_zoom == '1':
                    zoomed_mask = misc.imread(os.path.join(input_results_path, id_img + '.png'))
                    mask[mina:maxa, minb:maxb] = zoomed_mask
                print('Saving file:')
                print(os.path.join(output_results_path, id_img))
                mask
                
                
                ############################################################################# this might fix lossy error?
                #info = np.iinfo(mask.dtype) # Get the information of the incoming image type
                #mask = mask.astype(np.float64) / info.max # normalize the data to 0 - 1
                #mask = 255 * mask # Now scale by 255
                #mask = mask.astype(np.uint8)
                ############################################################################
                                               
                imsave(os.path.join(output_results_path, id_img + '.png'), mask*255)
                #imsave(os.path.join(output_results_path, id_img + '.png'), mask)
        
        
