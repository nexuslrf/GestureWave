'''
Created on 07/02/2014

@author: Benny, Manuel
'''

'''general imports '''
import numpy as np

''' explicit imports '''
from scipy.ndimage import gaussian_filter1d


class Preprocessor():
    def __init__(self, config, ref_frequency_frame):
        ''' initialization '''
        self.config = config
        self.ref_frequency_frame = ref_frequency_frame

        ''' general settings '''
        self.samples_per_frame = int(self.config['samples_per_frame'])

        ''' preprocessing settings '''
        self.slice_left = int(self.config['slice_left'])
        self.slice_right = int(self.config['slice_right'])
        self.wanted_frames = self.samples_per_frame - self.slice_left - self.slice_right
        self.framerange = int(self.config['framerange'])
        self.smooth = float(self.config['smooth'])
        self.use_each_second = int(self.config['use_each_second'])
        self.threshold = float(self.config['threshold'])
        self.new_preprocess = self.config['new_preprocess'] in ["True", "true", "1"]

    def normalise_framesets(self, framesets, ref_frequency_frame):
        ''' normalise framesets and substract ref_frequencyframe '''
        for frameset_nr in range(len(framesets)):
            for frame_nr in range(len(framesets[frameset_nr])):
                current_frame = framesets[frameset_nr][frame_nr]
                framesets[frameset_nr][frame_nr] = (current_frame / np.amax(current_frame)) - ref_frequency_frame
        return framesets

    def preprocess_frame(self, frame_data):
        frame = self.slice_frame(frame_data)
        try:
            ''' normalise frame '''
            normalized_data_with_ref_frequency = frame / np.amax(frame)
            frame = normalized_data_with_ref_frequency - self.ref_frequency_frame

            ''' set small noisy data to 0 '''
            frame[np.where(frame <= self.threshold)] = 0.0
        except:
            frame = np.zeros(self.wanted_frames)
        return frame

    def preprocess_frames(self, frames):
        if self.new_preprocess:
            ''' get all recordingframes which contain relevant gesture information '''
            # current_frameset = [self.preprocess_frame(frame) for frame in frames if np.amax(self.preprocess_frame(frame)) > 0]
            # list comprehension is maybe to difficult and probably slower because of two preprocessing-steps, so to keep it nice and simple a for-loop is used #
            current_frameset = []
            for frame in frames:
                processed_frame = self.preprocess_frame(frame)
                if np.amax(processed_frame) > 0:
                    current_frameset.append(processed_frame)

            ''' if less than 16, append frames with zeros '''
            while len(current_frameset) < self.framerange // 2:
                current_frameset.append(np.zeros(self.wanted_frames))

            ''' slice the first 16 recordingframes to two lists (even/odd) and compute the average of each pair '''
            current_frameset = np.asarray(current_frameset[:self.framerange // 2])
            relevant_frames = np.asarray(
                list(current_frameset[:self.framerange // 2:2] + current_frameset[1:self.framerange // 2:2]))

            ''' use only each second value if desired, smooth with corresponding value, default values for both parameters are false and 1.5 '''
            if self.use_each_second:
                processed_frames = gaussian_filter1d(
                    relevant_frames.reshape(self.wanted_frames * self.framerange // 4, ), self.smooth)[::2]
            else:
                processed_frames = gaussian_filter1d(
                    relevant_frames.reshape(self.wanted_frames * self.framerange // 4, ), self.smooth)

        else:
            ''' preprocess all frames '''
            # current_frameset = [self.preprocess_frame(frame, self.ref_frequency_frame) for frame in frames]
            # list comprehension is maybe easier and faster to read, but to keep it consistent a for-loop is used as in the if-branch #
            current_frameset = []
            for frame in frames:
                current_frameset.append(self.preprocess_frame(frame))

            ''' sum up all wanted frames to one gestureframe '''
            gesture_frame = np.asarray(current_frameset).sum(axis=0)

            ''' normalise summed gesture frame '''
            try:
                processed_frames = gesture_frame / np.amax(gesture_frame)
            except RuntimeWarning:
                processed_frames = np.zeros(gesture_frame.shape[0])
        return processed_frames

    def slice_frame(self, frame):
        ''' slice frame data if necessary '''
        if frame.shape[0] == self.wanted_frames:
            return frame
        else:
            ''' slice one single 1d-frame from 64 to 40 datavalues '''
            return frame[self.slice_left:(self.samples_per_frame - self.slice_right)]

    def slice_framesets(self, framesets):
        ''' slice 3d-framesets from 64 to 40 datavalues '''
        return framesets[:, :, self.slice_left:(self.samples_per_frame - self.slice_right)]
