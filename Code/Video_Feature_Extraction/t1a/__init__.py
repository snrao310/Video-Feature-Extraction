from __future__ import division

# define imports
import numpy as np
import cv2
import os
import math


sqrt_2_by_2 = math.sqrt(2) / 2


def get_y_component(cap, frame_count):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    success, image = cap.read()
    if image is not None:
        height, width, channel = image.shape
        roiYUV = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(roiYUV)
        return y, height, width


def quantize(n, block, step):
    pixelcount = n * [0]
    # qblock=np.array([8*[0]]*8)
    for i in range(0, 8):
        for j in range(0, 8):
            divide = block[i, j]
            divide = int(divide / step)
            if divide == n:
                divide -= 1
            # qblock[i,j]=int(divide*step+int(step/2))
            pixelcount[divide] += 1

    return pixelcount

if __name__ == '__main__':
    # Prompt the user to enter the absolute file path of the video.
    video_file_input = raw_input("Enter the path of the video File:")

    n = int(input("Enter the value of n:"))


    # Check if the file exists. if not, raise an assertion error.
    assert os.path.exists(video_file_input), "Sorry, we were unable to locate video file at " + str(video_file_input)

    video_file_name = os.path.basename(video_file_input)
    print "Video File is : ", video_file_name

    output_file = open("video_" + video_file_name + "_hist_" + str(n) + ".hst", "w+")
    print "Output will be at %s" % os.path.abspath(output_file.name)

    print >> output_file, "FRAME_ID, BLOCK_COORDINATES, GRAYSCALE_INSTANCE_ID, NUM_PIXELS"

    cap = cv2.VideoCapture(video_file_input)
    frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print "The frame count of this video is ", frameCount

    count = 0
    #y2, height, width = get_y_component(cap, count)
    while frameCount >= 1:
        if get_y_component(cap, count + 1) is not None:
            y, height, width = get_y_component(cap, count)
        if y is not None:
            for row in range(0, height, 8):
                for column in range(0, width, 8):
                    block = y[row:row + 8, column:column + 8]
                    block = np.float32(block)

                    # print count
                    # print block1
                    #print block2
                    #print block3

                    step = 255 / n
                    pixelcount = quantize(n, block, step)
                    for i in range(0, n):
                        print>> output_file, count, (row, column), int(i * step + int(step / 2)), pixelcount[i]
        count += 1
        frameCount -= 1
        print>> output_file, "\n"

