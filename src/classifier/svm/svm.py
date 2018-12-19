'''
Created on 14/01/2014

@author: Benny, Manuel
'''

''' general imports '''
import os
import numpy as np
import pylab as pl
import warnings
import re

''' explicit imports '''
from sklearn.externals import joblib
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

''' custom imports '''
from classifier.classifier import IClassifier
from classifier.svm.svm_dataloader import Dataloader
from classifier.svm.svm_preprocessor import Preprocessor
from classifier.svm.svm_appstarter import Starter
from classifier.svm.svm_keybinder import KeyBinder

''' catch warnings as error '''
np.set_printoptions(precision=4, suppress=True, threshold=np.nan)
np.seterr(all='warn')
warnings.simplefilter("error", RuntimeWarning)


class SVM(IClassifier):
    def __init__(self, recorder=None, config=None, relative=""):
        ''' initialization '''
        self.config = config

        ''' general settings '''
        self.subdirs = self.config['used_gestures'].split(',')
        self.nClasses = int(self.config['used_classes'])
        self.samples_per_frame = int(self.config['samples_per_frame'])

        ''' preprocessing settings '''
        self.slice_left = int(self.config['slice_left'])
        self.slice_right = int(self.config['slice_right'])
        self.wanted_frames = self.samples_per_frame - self.slice_left - self.slice_right
        self.framerange = int(self.config['framerange'])
        self.timeout = int(self.config['timeout'])
        self.smooth = float(self.config['smooth'])
        self.use_each_second = int(self.config['use_each_second'])
        self.threshold = float(self.config['threshold'])
        self.new_preprocess = self.config['new_preprocess'] in ["True", "true", "1"]

        ''' svm settings '''
        self.kernel = self.config['kernel']
        self.c = float(self.config['c'])
        self.gamma = float(self.config['gamma'])
        self.degree = int(self.config['degree'])
        self.coef0 = float(self.config['coef0'])

        ''' static settings '''
        self.gestures_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'gestures')
        self.path = os.path.join(os.path.dirname(__file__), 'svm_trained.pkl')
        print(self.path)

        self.datalist = []
        self.datanum = 0
        self.gesturefound = 0
        self.gestureindex = 0

        self.X_train, self.Y_train = None, None

        ''' initialization methods '''
        self.classifier = self.load(self.path)

        # create dataloader instance
        self.dataloader = Dataloader(self.config)
        self.ref_frequency_frame = self.dataloader.load_ref_frequency_frame()
        self.dataloader.updatePreprocessorInstance(self.ref_frequency_frame)

        # create preprocessor instance
        self.preprocessor = Preprocessor(self.config, self.ref_frequency_frame)

        # create appstarter instance
        # self.appstarter = Starter()
        self.tapping = KeyBinder()

    def classify(self, data):
        if self.classifier != None:
            ''' start first preprocessing of framedata '''
            frame = self.preprocessor.preprocess_frame(data)

            ''' store frame in datalist and increment running index '''
            self.datalist.append(frame)
            self.datanum += 1

            ''' increment timeout value to allow user to move his hand without any classification after one gesture '''
            if self.timeout < self.framerange // 2:
                self.timeout += 1
                if self.timeout == self.framerange // 2:
                    print("...")

            ''' check if frame has some relevant information and store this running index '''
            if np.amax(frame) > 0.0 and self.gesturefound == False and self.timeout == self.framerange // 2:
                self.gestureindex = self.datanum
                self.gesturefound = True

            ''' check if framerange is reached and gesturefound is true '''
            if self.gestureindex + self.framerange == self.datanum and self.gesturefound == True:
                self.gestureindex = 0
                self.gesturefound = False
                self.timeout = 0

                normalised_gesture_frame = self.preprocessor.preprocess_frames(self.datalist[-self.framerange:])
                # print(normalised_gesture_frame)
                try:
                    ''' start actual classification and applicationstarter '''
                    target_prediction = self.classifier.predict(normalised_gesture_frame.reshape(1,-1))[0]  # only each second?!?
                    # self.appstarter.controlProgram(target_prediction)
                    self.tapping.KeyTap(target_prediction)
                except:
                    print("some error occured =(")

            ''' delete unneeded frames from datalist '''
            if self.datanum > self.framerange:
                del self.datalist[0]

    def loadData(self, filename=""):
        ''' delegate the task of loading the data to the specific module instance dataloader '''
        data, targets = self.dataloader.load_gesture_framesets()
        return data, targets

    def load(self, filename=""):
        try:
            return joblib.load(filename)
        except:
            print("file does not exist")
            return None

    def getName(self):
        return "SVM"

    def startTraining(self, args=[]):
        ''' load training data if necessary '''
        # if self.X_train == None or self.Y_train == None:
        self.X_train, self.Y_train = self.loadData()

        ''' start training '''
        classifier = svm.SVC(kernel=self.kernel, C=self.c, gamma=self.gamma, degree=self.degree, coef0=self.coef0)
        classifier.fit(self.X_train, self.Y_train)

        ''' save classifier and store reference in global variable '''
        joblib.dump(classifier, self.path, compress=9)
        self.classifier = classifier

    def startValidation(self):
        # if self.X_train == None or self.Y_train == None:
        self.X_train, self.Y_train = self.loadData()

        ''' own implementation of confusion matrix '''
        l = len(self.Y_train) // 10
        p = 0
        confmat = np.zeros((self.nClasses, self.nClasses))
        for i in range(len(self.Y_train)):
            if (i + 1) % l == 0:
                p += 10
                print(p, "%")
            realclass = self.Y_train[i]
            predictedclass = self.classifier.predict(self.X_train[i].reshape(1,-1))[0]
            confmat[realclass][predictedclass] += 1

        ''' compute error '''
        sum_wrong = 0
        sum_all = 0
        for i in range(self.nClasses):
            for j in range(self.nClasses):
                if i != j:
                    sum_wrong += confmat[i][j]
                sum_all += confmat[i][j]
        error = sum_wrong / sum_all
        print(confmat)
        print("error: " + str(100. * error) + "%")


    def save(self, filename=""):
        pass

    def saveData(self, filename=""):
        pass

    def printClassifier(self):
        if self.classifier != None:
            pattern = re.compile(r'\s+')
            classifierinfo = [re.sub(pattern, '', part).replace("SVC(", "").replace(")", "").replace("=", " : ") for
                              part in str(self.classifier).split(',')]
            print(100 * "=")
            print("Path to saved classifier:\n\t", self.path, "\n")
            print("Information about saved classifier:")
            for i in classifierinfo:
                print("\t", i)
            print(100 * "=")

    def show_confusion_matrix(self):
        ''' method for creating confusion matrix with graphical visualization '''
        ''' callable from separate svm_confusion.py module '''

        x, y = self.loadData()

        a_train, a_test, b_train, b_test = train_test_split(x, y, test_size=0.33, random_state=42)
        ''' start training '''
        classifier = svm.SVC(kernel=self.kernel, C=self.c, gamma=self.gamma, degree=self.degree, coef0=self.coef0)
        classifier.fit(a_train, b_train)

        target_names = ["gesture 0", "gesture 1", "gesture 2", "gesture 3", "gesture 4", "gesture 5", "gesture 6"]
        b_pred = self.classifier.predict(a_test)
        cm = confusion_matrix(b_test, b_pred)
        print(100 * "=")
        print("Confusion matrix:\n")
        print(cm)
        print("\nReport:\n")
        print(classification_report(b_test, b_pred, target_names=target_names))

        definition = '''
The precision is the ratio tp / (tp + fp) where tp is the number of true positives and fp the number of false positives.
The precision is intuitively the ability of the classifier not to label as positive a sample that is negative.

The recall is the ratio tp / (tp + fn) where tp is the number of true positives and fn the number of false negatives.
The recall is intuitively the ability of the classifier to find all the positive samples.

The F-beta score can be interpreted as a weighted harmonic mean of the precision and recall, 
where an F-beta score reaches its best value at 1 and worst score at 0.

The F-beta score weights recall more than precision by a factor of beta.
beta == 1.0 means recall and precision are equally important.

The support is the number of occurrences of each class in y_true.
        '''
        print("\nDefinition:")
        print(definition)
        print(100 * "=")

        ''' plot confusion matrix in a separate window '''
        pl.matshow(cm)
        pl.title('Confusion matrix')
        pl.colorbar()
        pl.ylabel('Actual gestures')
        pl.xlabel('Predicted gestures')
        pl.show()
