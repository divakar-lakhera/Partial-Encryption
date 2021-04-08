## hashTest.py
import hashlib
INPUT_FILE="input_encode.avi"
OUTPUT_FILE="out_dec.avi"
ifile=open(INPUT_FILE,'rb').read()
ofile=open(OUTPUT_FILE,'rb').read()
inputHash=hashlib.sha256(ifile).hexdigest()
outputHash=hashlib.sha256(ofile).hexdigest()
print(inputHash)
print(outputHash)
if inputHash==outputHash:
    print("All ok Hash Match !!")
else:
    print("Error, Hash not matching")
