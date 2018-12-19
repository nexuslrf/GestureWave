'''
Created on 07/02/2014

@author: Benny, Manuel
'''

''' custom imports '''
import properties.config as c
from svm import SVM 


def show_confusion_matrix():
    svm_config = c.getInstance('../../').getConfig("svm")
    svm = SVM(None, svm_config)
    svm.show_confusion_matrix()


def main():
    show_confusion_matrix()


if __name__ == "__main__":
    main()