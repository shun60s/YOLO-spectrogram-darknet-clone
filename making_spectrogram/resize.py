#coding:utf-8

#  For YOLO train and test,
#    a) resize jpg to multiple of 32
#    b) rename jpg and label to serial number
#    c) make train list and valid list

import sys
import os
import shutil
import argparse
import pathlib
import glob
import numpy as np
from PIL import Image

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy  1.18.4
#  Pillow 7.2.0


def get_jpg_files( dir_path ):
    # get jpg file list which has label txt.
    jpg_list=glob.glob( dir_path + "*.jpg")
    jpg_list_with_labeltxt=[]
    for l in jpg_list:
        if os.path.exists(os.path.splitext(l)[0] + '.txt'):
            jpg_list_with_labeltxt.append(l)
    #
    return jpg_list_with_labeltxt


def save_list2txt( file_path, output_list):
    with open(file_path, mode='w',newline='\n') as f:  # windows環境での改行指定
        f.write('\n'.join(output_list))  # 改行コード \n, UNIXスタイル
        print ('wrote ', file_path)


if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='Re-size jpg file')
    parser.add_argument('--jpg_dir', '-w', default='./result', help='spectrogram jpg and label directory')
    parser.add_argument('--out_dir', '-o', default='./result_resized', help='output directory')
    args = parser.parse_args()
    
    path0= args.jpg_dir + '/'
    path1= args.out_dir + '/'
    
    #
    jpg_files_list= get_jpg_files( path0)
    print ('number of jpg files', len(jpg_files_list))
    print ('Please clear the directory ', path1)
    #print (jpg_files_list)
    
    # set the size to resize
    if 0:
        w_size= 32*20  # x20=640, x10=320
        h_size= 32*15  # x15=480, x7=224
    else:
        w_size= 32*10  # x20=640, x10=320
        h_size= 32*7  # x15=480, x7=224
    
    #
    for i,f in enumerate(jpg_files_list):
        #
        print (f)
        img0 = Image.open(f)
        img0_resize = img0.resize((w_size,h_size), Image.LANCZOS)
        #img0_resize.save(path1 + pathlib.PurePath(f).name)
        img0_resize.save(path1 + 'img' + str(i) + '.jpg')
        
        # copy label txt file to out_dir
        shutil.copyfile( os.path.splitext(f)[0] + '.txt', path1 + 'img' + str(i)  + '.txt')
        
        
    # make train.txt for tarin and test.txt for valid
    # set ratio of valid (test) data
    percentage_test = 0.2
    jpg_files_list1=get_jpg_files( path1)
    jpg_files_list2= [ s.replace('\\','/') for s in jpg_files_list1] # replace from \\ to /
    num_test= int(len(jpg_files_list2) * percentage_test)
    num_train=  len(jpg_files_list2) - num_test
    print('total number ', len(jpg_files_list2), ' train number ', num_train, ' valid number ', num_test)
    rand_list= np.random.choice(len(jpg_files_list2),len(jpg_files_list2), replace=False)
    train_list = np.array(jpg_files_list2)[rand_list[:num_train]].tolist()
    test_list  = np.array(jpg_files_list2)[rand_list[num_train:]].tolist()
    
    save_list2txt( path1 + 'train.txt', train_list)
    save_list2txt( path1 + 'test.txt',  test_list)
    