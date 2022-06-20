import struct
import os
import time

def read_file_analysis(file_all):
    candidates = []
    start = time.time()
    for file_data in file_all:
        print(file_data)
        file_bytes = os.stat(file_data).st_size
        f = open(file_data, "rb")
        #number = struct.unpack('{0}f'.format(4), f.read(16))
        #while number:
        #print(number)
        #number = struct.unpack('{0}f'.format(4), f.read(16))
        line_to_read = int(file_bytes/16)
        print("\tNumber of candidates:", line_to_read)
        if (line_to_read > 1000000):
            line_to_read_step = 1000
        elif (line_to_read > 100000):
            line_to_read_step = 100
        else:
            line_to_read_step = 1
        print("\tShowing each {0:4.0f} candidate in the plot.\n".format(line_to_read_step))
        for i in range(0,line_to_read,line_to_read_step):
            #if (i % 100 == 0):
                #print("position " + str(i), flush=True)
            number = f.read(16)
            #print(number)
            test = list(struct.unpack('{0}f'.format(4), number))
            candidates.append(test)
            #print(test)
            #test = struct.unpack('{0}f'.format(1), number)
            #print(test)
        f.close()
    end = time.time()
    print("Time to read the candidate file(s): {0:4.3f} second(s).".format(end-start))
    return candidates


