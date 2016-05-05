from __future__ import division

# define imports
import os
import re

def parse_t1a(infile):
    fil = open(infile)
    frameblock = []
    tlist = []
    max = -1
    binmax = -256
    line1 = 0
    pix=[]

    for line in fil:

        if (line1 == 0):
            line1 = 1
            continue

        t = line.split()
        if not t:
            continue
        t[1] += t[2]
        del t[2]
        framen = int(t[0])
        block = t[1]
        qbin = int(t[2])
        numpix = int(t[3])

        if (line1 == 1):
            tblock = block
            tframen = framen
            line1 = 2
            pix.append(numpix)
            continue

        if (tblock != block):
            tlist.append(pix)
            pix=[]
            binmax = -256
            max = -1
            tblock = block

        if (tframen != framen):
            frameblock.append(tlist)
            tlist = []
            tframen = framen

        max = numpix
        binmax = qbin
        pix.append(numpix)

    tlist.append(pix)
    #tlist.append(binmax)
    frameblock.append(tlist)

    # print frameblock
    return frameblock


def parse_t1d(input_file):
    return parse_t1a(input_file)


def parse_t1b(file_name, n):
    array = []
    final_array = []
    sum = []
    with open(file_name) as file:
        for line in file:
            if re.match('^[0-9]', line):
                line = line.replace('(', ' ')
                line = line.replace(')', ' ')
                line = line.replace(',', ' ')
                number = [int(i) for i in line.split()]
                frame_id = number[0]
                if frame_id == 0:
                    if number[3] == 1:
                        sum.append(number[4])
                    elif number[3] != 1:
                        sum.append(number[4])
                    if number[3] == n:
                        array.append(sum)
                        sum = []
                elif frame_id != prev_frame_id:
                    sum.append(number[4])
                    final_array.append(array)
                    array=[]
                elif frame_id == prev_frame_id:
                    if number[3] == 1:
                        sum.append(number[4])
                    elif number[3] != 1:
                        sum.append(number[4])
                    if(number[3] == n):
                        array.append(sum)
                        sum = []
                prev_frame_id = frame_id
    final_array.append(array)
    return final_array

def parse_t1c(filename, n):
    return parse_t1b(filename, n)


# n is the number of significant components
def parse_t2(file_name, n):
    array = []
    final_array = []
    sum = []
    with open(file_name) as file:
        for line in file:

            if re.match('^[0-9]', line):
                line = line.replace('(', ' ')
                line = line.replace(')', ' ')
                line = line.replace(',', ' ')
                number = [int(i) for i in line.split()]
                frame_id = number[0]
                if frame_id == 0:
                    if number[1] == 1:
                        sum.append(number[2])
                    elif number[1] != 1:
                        sum.append(number[2])
                    if number[1] == n:
                        array.append(sum)
                        sum = []
                elif frame_id != prev_frame_id:
                    sum.append(number[2])
                    final_array.append(array)
                    array=[]
                elif frame_id == prev_frame_id:
                    if number[1] == 1:
                        sum.append(number[2])
                    elif number[1] != 1:
                        sum.append(number[2])
                    if(number[1] == n):
                        array.append(sum)
                        sum = []
                prev_frame_id = frame_id
    return final_array
