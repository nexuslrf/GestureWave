import view.ui_plot
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import qwt as Qwt
from threading import Thread
from properties.config import ConfigProvider


class View:

    def __init__(self, recorder=None, applicationClose=None):
        # application
        self.app = None
        if recorder == None:
            raise Exception("No Recorder, so go home")
        self.recorder = recorder
        if applicationClose == None:
            raise Exception("No close callback")
        self.applicationClose = applicationClose
        self.curve = None
        self.uiplot = None
        config = ConfigProvider()
        self.amplitude = float(config.getAudioConfig()['amplitude'])
        self.guiIntervall = float(config.getRecordConfig()['guiintervall'])


    def callback(self, recClass):
        print("Recording finished for class " + str(recClass))
        self.status_btn_gesture(True)

    def record_0(self):
        self.recorder.setRecordClass(0, self.callback)
    def record_1(self):
        self.recorder.setRecordClass(1, self.callback)
    def record_2(self):
        self.recorder.setRecordClass(2, self.callback)
    def record_3(self):
        self.recorder.setRecordClass(3, self.callback)
    def record_4(self):
        self.recorder.setRecordClass(4, self.callback)
    def record_5(self):
        self.recorder.setRecordClass(5, self.callback)
    def record_6(self):
        self.recorder.setRecordClass(6, self.callback)
    def record_7(self):
        self.recorder.setRecordClass(7, self.callback)


    def record(self):
        self.status_btn_gesture(False)

    def plotSignal(self):
        data = self.recorder.getTransformedData()
        if data == None:
            return
        xs, ys = data
        self.curve.setData(xs, ys)
        self.uiplot.qwtPlot.replot()

    def status_btn_gesture(self, state):
        self.uiplot.btn_gesture_0.setEnabled(state)
        self.uiplot.btn_gesture_1.setEnabled(state)
        self.uiplot.btn_gesture_2.setEnabled(state)
        self.uiplot.btn_gesture_3.setEnabled(state)
        self.uiplot.btn_gesture_4.setEnabled(state)
        self.uiplot.btn_gesture_5.setEnabled(state)
        self.uiplot.btn_gesture_6.setEnabled(state)
        self.uiplot.btn_gesture_7.setEnabled(state)

    def bindButtons(self):
        self.uiplot.btn_gesture_0.clicked.connect(self.record_0)
        self.uiplot.btn_gesture_1.clicked.connect(self.record_1)
        self.uiplot.btn_gesture_2.clicked.connect(self.record_2)
        self.uiplot.btn_gesture_3.clicked.connect(self.record_3)
        self.uiplot.btn_gesture_4.clicked.connect(self.record_4)
        self.uiplot.btn_gesture_5.clicked.connect(self.record_5)
        self.uiplot.btn_gesture_6.clicked.connect(self.record_6)
        self.uiplot.btn_gesture_7.clicked.connect(self.record_7)

    def startNewThread(self):
        self.t = Thread(name="ControlGui", target=self.start, args=())
        self.t.start()
        return self.t

    def is_alive(self):
        if self.t is not None:
            return self.t.is_alive()
        return False

    def start(self):
        # application
        self.app = QtWidgets.QApplication(sys.argv)

        self.win_plot = view.ui_plot.QtWidgets.QMainWindow()
        self.uiplot = view.ui_plot.Ui_win_plot()
        self.uiplot.setupUi(self.win_plot)

        self.curve = Qwt.QwtPlotCurve()
        self.curve.attach(self.uiplot.qwtPlot)

        self.uiplot.qwtPlot.setAxisScale(self.uiplot.qwtPlot.yLeft, 0, self.amplitude * 1000)

        self.uiplot.timer = QtCore.QTimer()
        self.uiplot.timer.start(self.guiIntervall)

        self.uiplot.timer.timeout.connect(self.plotSignal)

        self.bindButtons()

        # ## DISPLAY WINDOWS
        self.win_plot.show()
        code = self.app.exec_()
        self.applicationClose(code)
#         sys.exit(code)
#         self.recorder.close()
