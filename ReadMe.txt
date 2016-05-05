#====================================README.TXT============================================================================================================#
#
# Programming language - Python ver 2.7
#
# Python libraries used - openCV 3.0, numpy for Python 2.7, scipy for python 2.7, re and os, matplotlib for Python 2.7
# 
# Description -> Phase 3 of the project, deals with feature extraction of the video and retrival, where the features are of the following types.
#		1. based on the gray scale bin of each 8x8 block
#		2. based on the significant components by DCT transformations on each 8x8 block
#		3. based on the significant components by DwT transformations on each 8x8 block and performing DWT on individual frames
#		4. based on the differences between current frame and previous frame.
# finally based on the features 10 best mactching frames are displayed 
#===========================================================================================================================================================#

All the programs for task 1a, task 1b, task 1c, task 1d, task 2, parse_tasks are present in separate folder for the purpose of importing in th task3.
The programs will run for 2^n X 2^n frame size only. Eg. both height and width should be similar(64x64)

All output files are placed in the current directory where the program resides.

TASK 1a

folder:Group7_project_phase3\code\Video_Feature_Extraction\t1a

Code file name : _init_.py

1.	This program reads the video file from the given path.
2.	The user has to input values of n for gray scale histogram of each 8x8 block.
3.	output file is of the format  video_filename_hist_n.hst, where n is the user input value.

TASK 1b

folder:Group7_project_phase3\code\Video_Feature_Extraction\t1b

Code file name : _init_.py

1.	This program reads the video file from the given path.
2.	The user has to input values of n for extracting signifcant frequency components of each 8x8 block
3.	output file is of the format  video_filename_blockdct_n.bct, where n is the user input value.

TASK 1c

folder:Group7_project_phase3\code\Video_Feature_Extraction\t1c

Code file name : _init_.py

1.	This program reads the video file from the given path.
2.	The user has to input values of n for extracting signifcant wavelet components of each 8x8 block
3.	output file is of the format  video_filename_blockdwt_n.dwt, where n is the user input value.

TASK 1d

folder:Group7_project_phase3\code\Video_Feature_Extraction\t1d

Code file name : _init_.py

1.	This program reads the video file from the given path.
2.	The user has to input values of n for difference histogram of each 8x8 block
3.	output file is of the format  video_filename_diff_n.dhc, where n is the user input value.


TASK 2

folder:Group7_project_phase3\code\Video_Feature_Extraction\t2

Code file name : _init_.py

1.	This program reads the video file from the given path.
2.	The user has to input values of m for extracting signifcant wavelet components of each 8x8 block
3.	output file is of the format  video_filename_framedwt_m.fwt, where m is the user input value.


TASK 3

folder:Group7_project_phase3\code\Video_Feature_Extraction

Code file name : t3.py

1.	This program reads the video file from the given path.
2.	The user has to input values of n and m for querying the frame.
3.	The user has to input the frame id to query.
4.	The output will display ten mathing with the features extracted.



