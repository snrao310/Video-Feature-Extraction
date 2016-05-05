#========================================================================================================================================================#
#CS-408/598 Multimedia Information Systems
# Project Group 7.
#
# Project phase 3.
#
# File Name:        2D_DWT.py
#
# Purpose:          The program does 2D DWT transformations on each 8x8 of each frame of the video taking the Y component and finds the m most significant wavelet
#                   component. The output file data is in the format <frame_id, wavelet_comp_id, value>
#                   <video_filename_blockdwt_n.bwt>
#
# #=========================================================================================================================================================#
import os
import math

import cv2
import numpy as np


def discrete_wavelet_transform(input_block,level, rows,cols):
    data =input_block
    r=rows
    c=cols
    dwt_block =np.zeros(shape=(rows,cols))
    tmp =np.zeros(shape=(rows,cols))

    #1D DWT on row level.
    for l in xrange(0,level,1):
        diff_row_start = r/2
        diff_col_start = c/2
        for x in xrange(0,r,1):
            for y in xrange(0,c/2,1):
                #print data[x][y*2]
                #return data
                out_avg = (data[x][y*2]+ data[x][y*2+1])/2
                #print "passed"
                out_diff=(data[x][y*2]- data[x][y*2+1])/2
                #print "passed"
                tmp[x][y]=out_avg
                tmp[x][y + diff_row_start] = out_diff
        #1D DWT on column level.
        for y in xrange(0,c,1):
            for x in xrange(0,r/2,1):
                out_avg = (tmp[x*2][y]+ tmp[x*2+1][y])/2
                out_diff =(tmp[x*2][y]- tmp[x*2+1][y])/2
                dwt_block[x][y]=out_avg
                dwt_block[x+ diff_col_start][y] = out_diff
        r = r/2
        c= c/2
        data=dwt_block
    return np.int16(dwt_block)

def get_n_most_significant_components(dwt_block, n):
    significant_elements = np.zeros(n)
    i = 0
    j = 0
    counter = 0
    while n != 0:
        if i == 0 and j == 0:
            significant_elements[counter] = dwt_block[i, j]
            counter=counter+1
            n = n-1
            j = j+1
        elif (i == 0 and j > 0) or (j==7):
            significant_elements[counter] = dwt_block[i, j]
            n = n-1
            if n > 0:
                while (j != 0 and n > 0):
                    if i+1> 7:
                        break
                    counter = counter+1
                    j = j-1
                    i = i+1
                    significant_elements[counter] = dwt_block[i, j]
                    n = n-1
                if i+1 > 7:
                    j = j+1
                else:
                    i = i+1
            counter = counter+1
        elif (j == 0 and i > 0) or(i==7):
            significant_elements[counter] = dwt_block[i,j]
            n=n-1
            if n > 0:
                while (i != 0 and n > 0):
                    if j+1 > 7:
                        break
                    counter = counter+1
                    j = j+1
                    i = i-1
                    significant_elements[counter] = dwt_block[i,j]
                    n=n-1
                if j+1 > 7:
                    i = i+1
                else:
                    j = j+1
            counter = counter+1
        else:
            significant_elements[counter] = dwt_block[i,j]
    return np.int16(significant_elements)

def write_frame(frameid, significant_element, block_x, block_y):
    for index in range(significant_element.shape[0]):
        print>>output_file, frameid,(block_x,block_y), index+1, significant_element[index]

if __name__ == '__main__':
    # Prompt the user to enter the absolute file path of the video.
    video_file_input = raw_input("Enter the path of the video File:")

    # Check if the file exists. if not, raise an assertion error.
    assert os.path.exists(video_file_input), "Sorry, we were unable to locate video file at " + str(video_file_input)
    # else, capture the video
    cap = cv2.VideoCapture(video_file_input)
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    filename = os.path.basename(video_file_input)

    n= int(input("Enter the value of n:"))
    row, col = 0,0

    output_file = open("video_"+filename+"_blockdwt_"+str(n)+".bwt", "w+")
    print "Output will be at %s" % os.path.abspath(output_file.name)


    print >>output_file, "FRAME_ID, BLOCK_COORDINATES, WAVELET_COMPONENT_ID, VALUE"


    count = 0
    while True:
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            success,frame = cap.read()
            #height, width, channel =frame.shape
            #print height, width
            #data=[]
            #data.append(np.array([0,0,0,0,0,0,0,0]))
            #data.append(np.array([0,0,0,0,0,0,0,0]))
            #data.append(np.array([0,0,63,127,127,63,0,0]))
            #data.append(np.array([0,0,127,255,255,127,0,0]))
            #data.append(np.array([0,0,127,255,255,127,0,0]))
            #data.append(np.array([0,0,63,127,127,63,0,0]))
            #data.append(np.array([0,0,0,0,0,0,0,0]))
            #data.append(np.array([0,0,0,0,0,0,0,0]))

            if success:
                if count ==0:
                    height, width, channel =frame.shape
                    level = int(math.log(8,2))
                YUVConverted = cv2.cvtColor(frame,cv2.COLOR_RGB2YUV)
                y ,u,v = cv2.split(YUVConverted)
                for row in xrange(0, height, 8):
                    for col in xrange(0,width,8):
                        block = y[row:row+8,col:col+8]
                        block = np.int16(block)
                        dwt_transformed = discrete_wavelet_transform(block,level,8,8)
                        significant_components = get_n_most_significant_components(dwt_transformed, n)
                        write_frame(count, significant_components, row, col)
                count +=1
            else:
                break

