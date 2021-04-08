import numpy as np
import time
import cv2
import random
from imutils.video import FPS


class objectEncryptor:
    def __init__(self,modFile,shares,fileName,outputFileName):
        self.dummy=0
        self.modFile=open(modFile,"r")
        self.capture=cv2.VideoCapture(fileName)
        self.outFile=outputFileName
        self.videoFPS=int(self.capture.get(cv2.CAP_PROP_FPS))
        if(self.videoFPS==0):
            print("ERROR: FPS reported 0")
            exit(0)
        self.totalFrames=int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.TotalShares=shares
        self.share=[]
        for i in range(shares):
            try:
                self.share.append(cv2.imread("share_"+str(i)+".png"))
            except:
                print("Read Failed")
                exit(1)

        self.key=self.share[0]
        for i in range(1,shares):
            self.key=cv2.bitwise_xor(self.key,self.share[i])

    def dumpKey(self):
        cv2.imshow("KEY",self.key)
        cv2.waitKey()

    def encode_convert_to_FFV1(self,fname):
        stime = time.time()
        print("Encoding to FFV1..",end="")
        fcc = cv2.VideoWriter_fourcc(*'FFV1')
        video = cv2.VideoWriter(fname, fcc, self.videoFPS, (self.width, self.height))
        while (self.capture.isOpened()):
            ret, frame = self.capture.read()
            if(ret == True):
                video.write(frame)
            else:
                break
        video.release()
        etime=time.time()
        print("Done..."+str(etime-stime));

    def encode_convert_to_MJPG(self,fname):
        stime=time.time()
        print("Encoding to MJPG..", end="")
        fcc = cv2.VideoWriter_fourcc(*'MJPG')
        video = cv2.VideoWriter(fname, fcc, self.videoFPS, (self.width, self.height))
        while (self.capture.isOpened()):
            ret, frame = self.capture.read()
            if(ret == True):
                video.write(frame)
            else:
                break
        video.release()
        etime=time.time()
        print("Done..."+str(etime-stime));

    def process(self,proc):   ## proc=0 encrypt proc=1 decrypt
        startTime = time.time();
        if(proc==1):
            print("Starting Decryption..")
        else:
            print("Starting Encryption..")

        fcc = cv2.VideoWriter_fourcc(*'FFV1')
        video = cv2.VideoWriter(self.outFile,fcc, self.videoFPS, (self.width, self.height))
        print("Total Frames: "+str(self.totalFrames))
        framesProcessed=0
        while (self.capture.isOpened()):
            ret, frame = self.capture.read()
            if ret == True:
                coordinates=[]
                for line in self.modFile:
                    if(line[0]=='!'):
                        break;
                    x,y,w,h=line.split(" ")
                    tmp=[int(x),int(y),int(w),int(h)]
                    coordinates.append(tmp);
                for k in coordinates:
                    if(len(k)<4):
                        break
                    for xr in range(k[0],min(k[2]+1,self.height),1):
                        for yr in range(k[1],min(k[3]+1,self.width),1):
                            if(proc==0):
                                frame[xr][yr][0] = (int(frame[xr][yr][0]) + int(self.key[xr][yr][0])) % 256
                                frame[xr][yr][1] = (int(frame[xr][yr][1]) + int(self.key[xr][yr][1])) % 256
                                frame[xr][yr][2] = (int(frame[xr][yr][2]) + int(self.key[xr][yr][2])) % 256
                            else:
                                frame[xr][yr][0] = (int(frame[xr][yr][0]) - int(self.key[xr][yr][0]) + 256) % 256;
                                frame[xr][yr][1] = (int(frame[xr][yr][1]) - int(self.key[xr][yr][1]) + 256) % 256;
                                frame[xr][yr][2] = (int(frame[xr][yr][2]) - int(self.key[xr][yr][2]) + 256) % 256;
                video.write(frame)
                framesProcessed+=1
                print("\r"+str((framesProcessed/self.totalFrames)*100)+" %",end="")
            else:
                break
        video.release()
        print()
        endTime = time.time();
        print("Time Taken: "+str(endTime-startTime))
        print("DONE")

"""
if __name__ == '__main__':

    tmp=objectEncryptor("modFile.txt",5,"../test/360.mp4","out.avi")
    tmp.encode_convert_to_FFV1("pre.avi")

    tmp2=objectEncryptor("modFile.txt",5,"../test/360.mp4","out.avi");
    tmp2.process(0)
    del tmp2
    tmp3=objectEncryptor("modFile.txt",5,"out.avi","outdec.avi")
    tmp3.process(1)
    del tmp3
    tmpp=objectEncryptor("modFile.txt",5,"out.avi","")
    tmpp.encode_convert_to_MJPG("out_play.avi");
    tmpp=objectEncryptor("modFile.txt",5,"outdec.avi","")
    tmpp.encode_convert_to_MJPG("outdec_play.avi");
"""