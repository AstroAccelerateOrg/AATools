import struct
import os

def read_file_analysis(file_data):
    print(file_data)
    file_bytes = os.stat(file_data).st_size
    f = open(file_data, "rb")
    #number = struct.unpack('{0}f'.format(4), f.read(16))
    #while number:
    #print(number)
    #number = struct.unpack('{0}f'.format(4), f.read(16))
    line_to_read = int(file_bytes/16)
    candidates = []
    for i in range(0,line_to_read,1000):
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
    return candidates

