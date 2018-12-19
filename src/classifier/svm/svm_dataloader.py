'''
Created on 07/02/2014

@author: Benny, Manuel
'''

'''general imports '''
import os
import numpy as np
#import pandas as pd

''' custom imports '''
from classifier.svm.svm_preprocessor import Preprocessor


class Dataloader():
    def __init__(self, config):
        ''' initialization '''
        self.config = config
        self.preprocessor = Preprocessor(self.config, None)

        ''' general settings '''
        self.subdirs = self.config['used_gestures'].split(',')
        self.nClasses = int(self.config['used_classes'])
        self.samples_per_frame = int(self.config['samples_per_frame'])

        ''' static settings '''
        self.gestures_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'gestures')

    def updatePreprocessorInstance(self, ref_frequency_frame):
        self.preprocessor = Preprocessor(self.config, ref_frequency_frame)

    def load_framesets(self, textfile):
        #frames_plain = np.asarray(pd.read_csv(textfile, sep=',', header=None))
        frames_plain = np.loadtxt(textfile, delimiter=",")
        num_framesets = frames_plain.shape[0]
        num_samples_total = frames_plain.shape[1]
        num_frames_per_frameset = num_samples_total // self.samples_per_frame
        framesets = frames_plain.reshape(num_framesets, num_frames_per_frameset, self.samples_per_frame)
        return framesets

    def load_gesture_framesets(self):
        gestures = []
        targets = []
        for gesture_nr in range(0, self.nClasses):
            print("load gesture", gesture_nr)
            for subdir in self.subdirs:
                filepath = os.path.join(self.gestures_path, subdir, 'gesture_' + str(gesture_nr))
                files = [allfiles for root, dirs, allfiles in os.walk(filepath)][0]
                for textfile in files:
                    #print "\t",os.path.join(filepath, textfile)
                    ''' load and reshape textfile with gesture data '''
                    text_file_with_path = os.path.join(self.gestures_path, subdir, 'gesture_' + str(gesture_nr),
                                                       textfile)
                    gesture_framesets_plain = self.load_framesets(text_file_with_path)

                    ''' reduce each framewindow from 64 to 40 values '''
                    gesture_framesets = self.preprocessor.slice_framesets(gesture_framesets_plain)

                    ''' create one gesture frame from relevant frames '''
                    for frameset_nr in range(0, gesture_framesets.shape[0]):
                        ''' start preprocessing of frameset '''
                        normalised_gesture_frame = self.preprocessor.preprocess_frames(gesture_framesets[frameset_nr])

                        ''' append gestureframe and targetclass to their corresponding arrays '''
                        gestures.append(normalised_gesture_frame)
                        targets.append(gesture_nr)

        ''' convert to numpy array '''
        data = np.vstack(gestures)
        targets = np.array(targets)
        print(data.shape, targets.shape)
        return data, targets

    def load_ref_frequency_frame(self):
        ''' load referencefrequency data with 18500Hz '''
        ref_frequency_txt_file = os.path.join(self.gestures_path, self.config['used_gestures'], 'gesture_6', '1545185566.1343.txt')
        ref_frequency_framesets_plain = self.load_framesets(ref_frequency_txt_file)

        ''' normalse referencefrequency datadarames '''
        ref_frequency_framesets = self.preprocessor.normalise_framesets(ref_frequency_framesets_plain, 0)

        ''' reduce to one single average referencefrequency frame and slice to 40 datavalues '''
        ref_frequency_avg_frameset = np.mean(ref_frequency_framesets, axis=1)
        ref_frequency_frame = self.preprocessor.slice_frame(np.mean(ref_frequency_avg_frameset, axis=0))
        return ref_frequency_frame
