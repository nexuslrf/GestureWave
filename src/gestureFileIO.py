import os
import numpy as np
import pandas as pd
import time

FILE_END = ".txt"
GESTURE_PREFIX = "/gesture_"

class GestureFileIO():

    def __init__(self, name="", gesturePath="../gestures", relative=""):
        self.filenamebase = str(time.time())[:-3]
        self.basePath = relative + gesturePath
        self.name = name
        self.namedPath = self.basePath + "/" + self.name
        self.avg = None
        if name is not "":
            if not os.path.exists(self.namedPath):
                os.makedirs(self.namedPath)
            for i in range(8):
                outdir = self.namedPath + GESTURE_PREFIX + str(i) + "/"
                if not os.path.isdir(outdir):
                    os.mkdir(outdir)

    def writeGesture(self, recordClass, recordData):
        ''' adds the give gesture to the personal gesture file '''
        outfile = self.getFileName(recordClass)
        oid = open(outfile, "a")
        # flatten all inputs to 1 vector
        data = np.array([np.array(np.ravel(recordData))])
#         print("Wrote record for class " + str(recordClass)
        np.savetxt(oid, data, delimiter=",", fmt='%1.4f')
        oid.close()


    def getGesture2D(self, recordClass, names=[]):
        ''' get gesture as numpy 2D array '''
        # example: svm, tree
        if len(names) == 0:
            for (path, dirs, files) in os.walk(self.basePath):
                for directory in dirs:
                    names.append(directory)
                break
        completearray = None
        for name in names:
            indir = self.basePath + "/" + name + GESTURE_PREFIX + str(recordClass) + "/"
            if(os.path.exists(indir)):
                for infile in os.listdir(indir):
                    if infile.endswith(FILE_END):
                        arr = pd.read_csv(indir + infile, sep=',', header=None)
                        arr = np.asarray(arr)
                        if completearray is None:
                            completearray = arr
                        else:
                            completearray = np.append(completearray, arr, axis=0)
        if completearray is None:
            print("empty data set returned")
            completearray = np.zeros((1, 2048))
        return completearray

    def getGesture3D(self, recordClass, names=[]):
        ''' get gesture as numpy 3D array '''
        # example: markovmodel, lstm
        data2d = self.getGesture2D(recordClass, names)
        data3d = data2d.reshape((np.shape(data2d)[0], 32, 64))
        return data3d

    def setFileName(self, name):
        self.filenamebase = str(name)

    def getFileName(self, recordClass):
        outdir = self.namedPath + GESTURE_PREFIX + str(recordClass) + "/"
        outfile = outdir + self.filenamebase + FILE_END
        return outfile

    def getGesture3DNormalized(self, recordClass, names=[], merge67=False):
        rawData = self.getGesture3D(recordClass, names)
        normalizedData = self._normalise(rawData)
        return normalizedData

    def getGesture3DDiffAvg(self, recordClass, names=[], merge67=False):
        normalizedData = self.getGesture3DNormalized(recordClass, names)
        avg = self.getAvgFrequency(names, merge67)
        diffAvgData = normalizedData - avg
        return diffAvgData

    def getAvgFrequency(self, names=[], merge67=False):
        if(self.avg == None):
            if(merge67):
                normalizedData6 = self.getGesture3DNormalized(6, names)
                normalizedData7 = self.getGesture3DNormalized(7, names)
                normalizedData = np.append(normalizedData6, normalizedData7, axis=0)
            else:
                normalizedData = self.getGesture3DNormalized(6, names)
            self.avg = np.mean(normalizedData, axis=1)
            self.avg = np.mean(self.avg, axis=0)
        return self.avg

    def _normalise(self, arr):
        ''' normalise each frame '''
        for d in range(len(arr)):
            for dd in range(len(arr[d])):
                arr[d][dd] = arr[d][dd] / np.amax(arr[d][dd])
        return arr

if __name__ == "__main__":

    import pylab
    x = np.arange(64)
    gesture = 10
    gclass = 6
    def make_plot(arr, length, c):
        ''' plot all recordingFrames '''
        for i in range(length):
            ax = pylab.subplot(5, 8, i)
            pylab.plot(x, arr[i], c)
            ax.set_ylim([-0.2, 1])

    gestures = GestureFileIO()
    normalizedData = gestures.getGesture3DNormalized(gclass)
    diffAvgData = gestures.getGesture3DDiffAvg(gclass)
    avg = gestures.getAvgFrequency()
    ''' plot normalised and averaged frequency data '''
    pylab.subplot(5, 8, 39)
    pylab.plot(x, avg, "g")

    ''' plot normalised gessture data '''
    length = len(normalizedData[gesture])
    make_plot(normalizedData[gesture], length, "b")
    make_plot(diffAvgData[gesture], length, "r")

    pylab.show()
