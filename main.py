import time
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Final_Project.shares import shareBuilder
from Final_Project.encrypt import objectEncryptor
## NOTE : MAKE SURE modFile.txt is ready (use ssd_detect.py)

NUM_OF_SHARES = 150
MOD_FILE = "modFile.txt"
INPUT_FILE = "../test/720.mp4"
OUTPUT_FILE_DECRYPT = "out_dec.avi"
OUTPUT_FILE_ENC = "out_enc.avi"

## check for files

shares=shareBuilder(NUM_OF_SHARES,"../test/720.mp4")
shares.buildShare()

"""
    How to encrypt files when compression artifact is a major problem ??
    
    Original Video --> Encrypted Uncompressed Video {to share} (FFV1) --> Uncompressed Decrypted Video (FFV1) --> Compressed Decrypted Video (MJPG)
                                |
                                V
             Compressed Encrypted Video (For Testing Purpose) (MJPG)

"""

stage1=objectEncryptor(MOD_FILE,NUM_OF_SHARES,INPUT_FILE,"encrypted_RAW.mkv")
stage1.process(0) ## process 0 --> encrypt
del stage1

stage2=objectEncryptor(MOD_FILE,NUM_OF_SHARES,"encrypted_RAW.mkv","dec_RAW.mkv")
stage2.process(1) ## process 1 --> decrypt
del stage2

## Start Encoding

stage3=objectEncryptor(MOD_FILE,NUM_OF_SHARES,"dec_RAW.mkv","")
stage3.encode_convert_to_MJPG(OUTPUT_FILE_DECRYPT)
del stage3

stage4=objectEncryptor(MOD_FILE,NUM_OF_SHARES,"encrypted_RAW.mkv","")
stage4.encode_convert_to_MJPG(OUTPUT_FILE_ENC)
del stage4

stage5=objectEncryptor(MOD_FILE,NUM_OF_SHARES,INPUT_FILE,"")
stage5.encode_convert_to_MJPG("input_encode.avi")
## Done All
