import abc

class IClassifier:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getName(self):
        pass

    @abc.abstractmethod
    def startTraining(self, args=[]):
        pass

    @abc.abstractmethod
    def classify(self, data):
        pass

    @abc.abstractmethod
    def startValidation(self):
        pass

    @abc.abstractmethod
    def load(self, filename=""):
        pass

    @abc.abstractmethod
    def save(self, filename=""):
        pass

    @abc.abstractmethod
    def loadData(self, filename=""):
        pass

    @abc.abstractmethod
    def saveData(self, filename=""):
        pass

    @abc.abstractmethod
    def printClassifier(self):
        pass

    def startGui(self, recorder, callback):
        raise NotImplementedError("No GUI implemented!")
