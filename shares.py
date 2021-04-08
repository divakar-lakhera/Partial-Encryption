import numpy as np
import time
import cv2
import random
from imutils.video import FPS


class shareBuilder:
    def __init__(self,noOfSharesToMake,fileName):
        self.dummy=0
        self.noOfShares=noOfSharesToMake
        self.file=fileName
        self.capture=cv2.VideoCapture(fileName)
        self.totalFrames=int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.randomImg=np.random.randint(255, size=(self.height,self.width,3),dtype=np.uint8)

    def dumpRand(self):
        cv2.imshow("RAND",self.randomImg)

    def buildShare(self):
        print("Building Shares.."+str( self.noOfShares))
        stime = time.time()
        blkSz=self.totalFrames//self.noOfShares
        currentBlk=0
        for i in range(self.noOfShares):
            randIdx=(random.randrange(self.totalFrames))%blkSz;
            ## SEEK
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, currentBlk+randIdx-1)
            res,frame=self.capture.read();
            ## XOR
            frame=cv2.bitwise_xor(frame,self.randomImg)
            cv2.imwrite("share_"+str(i)+".png",frame)
            currentBlk+=blkSz ## goto next block
        etime=time.time()
        print("Done..."+str(etime-stime));

"""
if __name__ == '__main__':
    print("Starting")
    tmp=shareBuilder(5,"../test/360.mp4")
    tmp.dumpRand()
    tmp.buildShare()
    print("Done")
"""