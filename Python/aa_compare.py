#!/usr/bin/env python3

"""
Compare two binary files return the difference between them
"""

__author__ = "Jacob Wilkins"
__version__ = "0.1"
__license__ = """
MIT License

Copyright (c) 2019 Jacob Wilkins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
__email__ = "jacob.wilkins@oerc.ox.ac.uk"
__status__ = "Development"

import struct
import argparse

parser = argparse.ArgumentParser(description=__doc__, add_help=True)
parser.add_argument("-f", "--fields", help="Comma-separated list of fields in file to read", default="dm,ts,snr,wi")
parser.add_argument("-N", "--data-size", type=int, help="Size of data in bytes", default=4)
parser.add_argument("-T", "--data-type", help="Type of data in each byte block", default="f")
parser.add_argument("--unaligned", help="Disable alignment checks of data", action="store_true")
parser.add_argument("FILE", nargs=2, help="List of sources to compile")
argList = parser.parse_args()
fields = argList.fields.split(',')
dataSize = argList.data_size
dataType = argList.data_type
unaligned = argList.unaligned
filename1, filename2 = argList.FILE
def get_fields(inFile):
    """ Get binary data as array of fields """
    fileBytes = 1
    try:
        while fileBytes:
            fieldDict = {}
            for dataField in fields:
                fileBytes = inFile.read(dataSize)
                [fieldDict[dataField]] = struct.unpack(dataType, fileBytes)
            yield fieldDict
    except struct.error:
        if unaligned:
            return
        raise struct.error("Incomplete final float in file, perhaps an offset issue")


with open(filename1, 'rb') as file1, open(filename2, 'rb') as file2:
    dataFields1 = get_fields(file1)
    dataFields2 = get_fields(file2)

#    for data in zip(dataFields1, dataFields2):
#        print(data)
#    quit()
    maxDiff = {field:0 for field in fields}
    meanDiff = {field:0 for field in fields}
    sumDiff = {field:0 for field in fields}
    n = 0
    for n, (data1, data2) in enumerate(zip(dataFields1, dataFields2)):
        if not data1 or not data2:
            if unaligned:
                print("Files of different lengths exiting at cycle", n)
            else:
                raise IndexError("Files of different at cycle", n)

        for field in fields:
            diff = data1[field] - data2[field]
            absDiff = abs(diff)
            maxDiff[field] = max(absDiff, maxDiff[field])
            sumDiff[field] += absDiff

print("Max", *[f"{key} : {val}" for key, val in maxDiff.items()], sep=", ")
print("Sum", *[f"{key} : {val}" for key, val in sumDiff.items()], sep=", ")
print("Ave", *[f"{key} : {val/n}" for key, val in sumDiff.items()], sep=", ")
