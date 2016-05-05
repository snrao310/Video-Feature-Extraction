#/Users/scari/demo/R2.mp4

from __future__ import division


#imports
import numpy as np
import cv2
import os

import parse_tasks
import t1a

from matplotlib import pyplot as plt


def show_image(cap, result_tuple, task_string):
    fig = plt.figure(task_string.capitalize())
    cur_axes = fig.gca()
    cur_axes.axes.get_xaxis().set_visible(False)
    cur_axes.axes.get_yaxis().set_visible(False)
    cur_axes.axes.get_xaxis().set_ticks([])
    cur_axes.axes.get_yaxis().set_ticks([])
    cur_axes.axes.get_xaxis().set_ticklabels([])
    cur_axes.axes.get_yaxis().set_ticklabels([])
    start = 1
    sub = plt.subplot(4, 3, start)
    plt.imshow(frame,'gray'),plt.title('ORIGINAL', fontsize=12)
    sub.set_xticks([])
    sub.set_yticks([])
    for (sum, index) in result_tuple:
        y, _, _ = t1a.get_y_component(cap, index)
        start += 1
        sub = plt.subplot(4, 3, start)
        sub.set_xticks([])
        sub.set_yticks([])
        plt.imshow(y, 'gray'),plt.title('Frame' + str(index) + ' (' +str(sum) + ')', fontsize=12)
    plt.tight_layout(pad=0.5)
    plt.show()


MAX_MATCHES = 10

#Prompt the user to enter the absolute file path of the video.
video_file_input = raw_input("Enter the path of the video File:")

#Check if the file exists. if not, raise an assertion error.
assert os.path.exists(video_file_input), "Sorry, we were unable to locate video file at " + str(video_file_input)

video_file_name = os.path.basename(video_file_input)
print "Video File is : ", video_file_name

cap = cv2.VideoCapture(video_file_input)
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print "The frame count of this video(%dX%d) is %d" % (height, width, frameCount)

frame_id = input("Enter the query frame id: ")
if frame_id <= 0 or frame_id > frameCount:
    print "Invalid frame id"
    exit(1)
frame, frameHeight, frameWidth = t1a.get_y_component(cap,frame_id)

n = input("Enter n: ")
m = input("Enter m: ")


#Task 1a
task1a_file_name = "t1a%svideo_%s_hist_%d.hst" % (os.sep, os.path.basename(video_file_input), n)
assert os.path.exists(task1a_file_name), "Sorry, we were unable to locate task 1a file at " + str(task1a_file_name)
task1a = parse_tasks.parse_t1a(task1a_file_name)

task1a_frame = task1a[frame_id]
task1a_result = []
for i in range(0,  len(task1a)):
    if i==frame_id:
        continue
    task1a_result.append((np.sum(np.absolute(np.subtract(task1a[i], task1a_frame))), i))

task1a_result.sort()
print "TASK 1a : ", task1a_result[0:MAX_MATCHES]
show_image(cap, task1a_result[0:MAX_MATCHES], 'Task 1a')


#Task 1b
task1b_file_name = "t1b%svideo_%s_blockdct_%d.bct" % (os.sep, os.path.basename(video_file_input), n)
assert os.path.exists(task1b_file_name), "Sorry, we were unable to locate task 1a file at " + str(task1b_file_name)
task1b = parse_tasks.parse_t1b(task1b_file_name, n)

task1b_frame = task1b[frame_id]
task1b_result = []
for i in range(0,  len(task1b)):
    if i==frame_id:
        continue
    task1b_result.append((np.sum(np.absolute(np.subtract(task1b[i], task1b_frame))), i))

task1b_result.sort()
print "TASK 1b : ", task1b_result[0:MAX_MATCHES]
show_image(cap, task1b_result[0:MAX_MATCHES], 'Task 1b')


#Task 1c
task1c_file_name = "t1c%svideo_%s_blockdwt_%d.bwt" % (os.sep, os.path.basename(video_file_input), n)
assert os.path.exists(task1c_file_name), "Sorry, we were unable to locate task 1a file at " + str(task1c_file_name)
task1c = parse_tasks.parse_t1c(task1c_file_name, n)

task1c_frame = task1c[frame_id]
task1c_result = []
for i in range(0,  len(task1c)):
    if i==frame_id:
        continue
    task1c_result.append((np.sum(np.absolute(np.subtract(task1c[i], task1c_frame))), i))

task1c_result.sort()
print "TASK 1c : ", task1c_result[0:MAX_MATCHES]
show_image(cap, task1c_result[0:MAX_MATCHES], 'Task 1c')


#Task 1d
task1d_file_name = "t1d%svideo_%s_diff_%d.dhc" % (os.sep, os.path.basename(video_file_input), n)
assert os.path.exists(task1d_file_name), "Sorry, we were unable to locate task 1a file at " + str(task1d_file_name)
task1d = parse_tasks.parse_t1d(task1d_file_name)

task1d_frame = task1d[frame_id]
task1d_result = []
for i in range(0, len(task1d)):
    if i == frame_id:
        continue
    task1d_result.append((np.sum(np.absolute(np.subtract(task1d[i], task1d_frame))), i))

task1d_result.sort()
print "TASK 1d : ", task1d_result[0:MAX_MATCHES]
show_image(cap, task1d_result[0:MAX_MATCHES], 'Task 1d')


#Task 2
task2_file_name = "t2%svideo_%s_framedwt_%d.fwt" % (os.sep, os.path.basename(video_file_input), m)
assert os.path.exists(task2_file_name), "Sorry, we were unable to locate task 1a file at " + str(task2_file_name)
task2 = parse_tasks.parse_t2(task2_file_name, m)

task2_result = []
task2_frame = task2[frame_id]
for i in range(0, len(task2)):
    if i==frame_id:
        continue
    task2_result.append((np.sum(np.absolute(np.subtract(task2[i], task2_frame))), i))

task2_result.sort()
print "TASK 2 : ", task2_result[0:MAX_MATCHES]
show_image(cap, task2_result[0:MAX_MATCHES], 'Task 2')


