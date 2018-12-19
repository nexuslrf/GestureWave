'''
Created on 06/02/2014

@author: Benny, Manuel
'''

''' general imports '''
import subprocess as sp
import time

'''                              '''
'''         WINDOWS ONLY         '''
'''                              '''


class Starter():
    def __init__(self):

        ''' dictionary which holds some information about programs and corresponding gesturenumbers '''
        self.executed = {0: {"program": "notepad", "started": False, "processname": "notepad"},
                         1: {"program": "notepad", "number": 0},
                         2: {"program": "taskmanager", "started": False, "processname": "taskmgr"},
                         3: {"program": "taskmanager", "number": 2},
                         4: {"program": "calculator", "started": False, "processname": "calc"},
                         5: {"program": "calculator", "number": 4}}

    def controlProgram(self, number):
        ''' wrapper method which will be called from svm classifier '''
        self.logic(number)

    def logic(self, number):
        ''' if predicted gesturenumber is not 6, continue to some small logic, wether to start or terminate a program '''
        if number != 6:
            if number % 2 == 0:
                if self.executed[number]["started"] == False:
                    self.executed[number]["started"] = self.start(number, self.executed[number]["program"],
                                                                  self.executed[number]["processname"])
                else:
                    self.log("\t" + str(number) + " => " + self.executed[number][
                        "program"] + " already started, only one instance allowed")
            else:
                if self.executed[self.executed[number]["number"]]["started"] != False:
                    self.executed[self.executed[number]["number"]]["started"] = self.terminate(number,
                                                                                               self.executed[number][
                                                                                                   "program"],
                                                                                               self.executed[
                                                                                                   self.executed[
                                                                                                       number][
                                                                                                       "number"]][
                                                                                                   "started"])
                else:
                    self.log("\t" + str(number) + " => " + self.executed[number][
                        "program"] + " not started, nothing to terminate")

    def start(self, number, program, processname):
        ''' start programm and return process id '''
        self.log("\t" + str(number) + " => starting " + program)
        proc = sp.Popen(processname)
        return proc.pid

    def terminate(self, number, program, processid):
        ''' terminate programm and return False '''
        self.log("\t" + str(number) + " => terminating " + program)
        sp.Popen("TASKKILL /F /PID {pid} /T".format(pid=processid), shell=True, stdout=sp.PIPE)
        return False

    def log(self, message):
        ''' some heavy method for printing stuff =) '''
        print(message)

def main():
    ''' just for testing '''
    app = Starter()
    app.controlProgram(5)
    app.controlProgram(4)
    app.controlProgram(4)
    time.sleep(1)
    app.controlProgram(5)
    app.controlProgram(5)

if __name__ == "__main__":
    main()
