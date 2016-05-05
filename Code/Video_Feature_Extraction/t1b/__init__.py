# ====================================================================================== #
# =============================CS-598 Project Phase 3, Group 7========================== #
# File Name :       Task1b.py
# Purpose   :       To perform block 2D-DCT on a input video. The output is
#                   written to a file of the name format video_<filename>_blockdct_<n>.bct
#                   The program also retrieves the n most significant frequency
#                   components from the 8-by-8 block. The significance of the order
#                   is determined by the traversing the DCT matrix in a zig-zag
#                   manner.
# Input     :       Video File complete Path, integer n
# Output    :       File of the format video_<filename>_blockdct_<n>.bct
#
# ====================================================================================== #

from __future__ import division

# define imports
import numpy as np
import cv2
import os
import math


sqrt_2_by_2 = math.sqrt(2)/2

# ======================================================================================= #
# Function which retrieves the frame from the input video and returns the y component and
# the height and the width.
# ======================================================================================= #


def get_y_component(frame_count):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    success, image = cap.read()
    if image is not None:
        height, width, channel = image.shape
        roiYUV = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(roiYUV)
        return y, height, width

# ======================================================================================= #
# Function which retrieves the n most-significant components from a 2D-DCT matrix
# The order of significance is determined by traversing the array in a zig-zag fashion
# ======================================================================================= #


def get_n_most_significant_components(DCT_BLOCK, n):
    significant_elements = np.zeros(n)
    i = 0
    j = 0
    counter = 0
    while n != 0:
        if i == 0 and j == 0:
            significant_elements[counter] = DCT_BLOCK[i, j]
            counter=counter+1
            n = n-1
            j = j+1
        elif (i == 0 and j > 0) or (j==7):
            significant_elements[counter] = DCT_BLOCK[i, j]
            n = n-1
            if n > 0:
                while (j != 0 and n > 0):
                    if i+1> 7:
                        break
                    counter = counter+1
                    j = j-1
                    i = i+1
                    significant_elements[counter] = DCT_BLOCK[i, j]
                    n = n-1
                if i+1 > 7:
                    j = j+1
                else:
                    i = i+1
            counter = counter+1
        elif (j == 0 and i > 0) or(i==7):
            significant_elements[counter] = DCT_BLOCK[i,j]
            n=n-1
            if n > 0:
                while (i != 0 and n > 0):
                    if j+1 > 7:
                        break
                    counter = counter+1
                    j = j+1
                    i = i-1
                    significant_elements[counter] = DCT_BLOCK[i,j]
                    n=n-1
                if j+1 > 7:
                    i = i+1
                else:
                    j = j+1
            counter = counter+1
        else:
            significant_elements[counter] = DCT_BLOCK[i,j]
    return np.int16(significant_elements)



cosine_matrix_data = np.zeros(shape=(8,8))
coefficient_matrix_data = np.zeros(shape=(8,8))


# ============================================================================================== #
# Function, which calcuates the Coefficient matrix for an 8 by 8 block. THis table can be used
# to perform look up in the direct cosine transformation
# ============================================================================================== #

def coefficient_matrix():
    for i in range(0,8,1):
        for j in range(0,8,1):
            if i == 0 and j == 0:
                coefficient_matrix_data[i,j] = (2*sqrt_2_by_2*sqrt_2_by_2)/(math.sqrt(64))
            elif i == 0 or j == 0:
                coefficient_matrix_data[i,j] = (2*sqrt_2_by_2)/(math.sqrt(64))
            else:
                coefficient_matrix_data[i,j] = 2/math.sqrt(64)


# ============================================================================================== #
# Function, which calcuates the cosine matrix for an 8 by 8 block. This table can be used
# to perform look up in the direct cosine transformation
# ============================================================================================== #

def cosine_matrix():
    for i in range(0,8,1):
        for j in range(0,8,1):
            cosine_matrix_data[i,j] = math.cos(((2*i + 1)*(j*math.pi))/(16))

# ======================================================================================= #
# Function which performs 2D - Cosine Transform on an input 8-by-8 block.
# TO_DO : Make this performant. Although, the output is the same as from in-built dct
#         function, but this is slow. Need to check ways of improving it.
#
# ======================================================================================= #


def direct_cosine_transform(input_array):
    dct_block = np.zeros(shape=(8,8))
    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            cosine_prod = 0
            for m in range(0, 8, 1):
                for n in range(0, 8, 1):
                    intermediate_sum = cosine_matrix_data[m, i]*cosine_matrix_data[n,j]*input_array[m,n]
                    cosine_prod = cosine_prod + intermediate_sum
            dct_block[i,j] = np.int16(coefficient_matrix_data[i,j]*cosine_prod)
    return dct_block

# ======================================================================================= #
# Function which writes the output to the output file
# ======================================================================================= #


def write_frame(frameid, significant_element, block_x, block_y):
    for index in range(significant_element.shape[0]):
        print>>output_file, frameid,(block_x,block_y), index+1, significant_element[index]

if __name__ == '__main__':
    # Prompt the user to enter the absolute file path of the video.
    video_file_input = raw_input("Enter the path of the video File:")

    n = int(input("Enter the value of n:"))


    # Check if the file exists. if not, raise an assertion error.
    assert os.path.exists(video_file_input), "Sorry, we were unable to locate video file at " + str(video_file_input)

    video_file_name = os.path.basename(video_file_input)
    print "Video File is : ", video_file_name


    output_file = open("video_"+video_file_name+"_blockdct_"+str(n)+".bct", "w+")
    print "Output will be at %s" % os.path.abspath(output_file.name)
    cosine_matrix()
    coefficient_matrix()

    print >>output_file, "FRAME_ID, BLOCK_COORDINATES, FREQUENCY_COMPONENT_ID, VALUE"

    cap = cv2.VideoCapture(video_file_input)
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print "The frame count of this video is ", frameCount

    count = 0
    while frameCount>=1:
        if get_y_component(count) is not None:
            y, height, width = get_y_component(count)
        if y is not None:
            for row in range(0, height, 8):
                for column in range(0, width, 8):
                    block = y[row:row+8, column:column+8]
                    block = np.float32(block)
                    dctblock = direct_cosine_transform(block)
                    significant_components = get_n_most_significant_components(dctblock, n)
                    write_frame(count, significant_components, row, column)
        count += 1
        frameCount -= 1