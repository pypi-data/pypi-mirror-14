
import os
import sys

def start():
    cfile = sys.argv[1]
    os.system("g++ " + cfile + " -o ouput && ./ouput")
    os.remove("./ouput")
