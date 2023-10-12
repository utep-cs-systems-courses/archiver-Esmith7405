#! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists
import subprocess # executing program

debug = 1

#Framer's job
  #Byte-array -> a framed sequence of bytes written to a fd
class Framer:
    def __init__(self, writeFD):
        self.writeFD = writeFD
    def frame(self, byteArray):
        return (str(len(byteArray)) + ":" + str(byteArray) + ":")  

#Unframer
  #Reading from a fd -> Byte array
class Unframer:
    def __init__(self, readFD):
        self.readFD = readFD
    def unFrame(self):
        fileName = "fileName"
        fileContents = "FileContents"
        pass

class TarWriter:
    def __init__(self, writeFD):
        self.writeFD = writeFD
        sys.stdout.write("B\'") #begin the tar file
    def storeFile(self, fileName):
        tarFramer = Framer(fileName)
        framedFileName = tarFramer.frame(fileName)
        #decode file contents into a byte array
        fd = os.open("src/" + fileName, os.O_RDONLY)
        fileContents = ""
        buffer = os.read(fd, 100000)
        fileContents += str(buffer)
        '''
        while buffer != []:
            buffer = os.read(fd, 100)
            fileContents += str(buffer)
        '''
        #Frame(byteArray containing the file contents)
        framedFileContents = tarFramer.frame(fileContents)
        os.close(fd)
        sys.stdout.write(framedFileName)
        sys.stdout.write(framedFileContents)
        pass

class TarReader:
  def init(self, readFD):
      self.readFD = readFD
  def Untar(self):
    tarUnFramer = Unframer(self.readFD)
    tarIn = os.open(self.readFD, os.O_RDONLY)
    #until input file end is reached
    #read entire tar File as one object
    #Split the tar file
    #Alternate between assigning file names and file contents, writing them when finished
      #Name = unframe().decode()
      #Contents[] = unframe()
      #write contents to fileName
    os.close(tarIn)
    pass

#Begin Execution
if len(sys.argv) < 2:
    print("Correct usage: mytar.py c <input1> <input2> ... <inputN> > <out.tar> \nmytar.py x <output.txt>")
    exit()

#mytar.py c <input1> <input2> > <out.tar> - Take the input files, encode them and aggregate them to 1 text file
if sys.argv[1] == "c":
    if debug: print("Create\n")
    
    #Run through all inputs, adding them to a list
    filesIn = []
    for i in range(2, len(sys.argv)):
      filesIn.append(sys.argv[i])

    for file in filesIn:
        if debug: print(file)

    writer = TarWriter("out.tar") 
    for fd in filesIn:
        writer.storeFile(fd)

#mytar.py x <output.txt> - Take the output file and seperate it into its respective files
if sys.argv[1] == "x":
    if debug: print("Extracting\n")

    reader = TarReader(sys.argv[2])
    reader.Untar()
