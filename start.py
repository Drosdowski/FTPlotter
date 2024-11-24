#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
import ftrobopy                                              # Import the ftrobopy module
from TouchStyle import *

class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        w = TouchWindow("Tut_3_4")

        txt_ip = os.environ.get('TXT_IP')                    # try to read TXT_IP environment variable
        try:
            self.txt = ftrobopy.ftrobopy("192.168.178.34", 65000) # connect to TXT's IO controller
        except:
            self.txt = None

        vbox = QVBoxLayout()

        # share of C:\Users\micha\PycharmProjects <-->

        if not self.txt:
            # display error of TXT could no be connected
            # error messages is centered and may span
            # over several lines
            err_msg = QLabel("Error connecting IO server")   # create the error message label
            err_msg.setWordWrap(True)                        # allow it to wrap over several lines
            err_msg.setAlignment(Qt.AlignCenter)             # center it horizontally
            vbox.addWidget(err_msg)                          # attach it to the main output area
        else:
            # initialization went fine. So the main gui
            # is being drawn
            button = QPushButton("Toggle O1")                # create a button labeled "Toggle O1"
            button.clicked.connect(self.on_button_clicked)   # connect button to event handler
            vbox.addWidget(button)                           # attach it to the main output area

            # configure all TXT outputs to normal mode
            M = [ self.txt.C_OUTPUT, self.txt.C_OUTPUT, self.txt.C_OUTPUT, self.txt.C_OUTPUT ]
            I = [ (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ) ]
            self.txt.setConfig(M, I)
            self.txt.updateConfig()

            self.timer = QTimer(self)                        # create a timer
            self.timer.timeout.connect(self.on_timer)        # connect timer to on_timer slot
            self.timer.start(100)                            # fire timer every 100ms (10 hz)

            self.robot_mode = 'START_X'

        w.centralWidget.setLayout(vbox)
        w.show()
        self.exec_()

    # an event handler for our button (called a "slot" in qt)
    # it will be called whenever the user clicks the button
    def on_button_clicked(self):
        self.robot_mode = "NOT_AUS"
        self.txt.setPwm(0, 0)
        self.txt.setPwm(1, 0)
        self.txt.setPwm(2, 0)
        self.txt.setPwm(3, 0)

    # an event handler for the timer (also a qt slot)
    def on_timer(self):
        if self.robot_mode == 'START_X':
            print('START_X')
            self.start_position_x()
        if self.robot_mode == 'START_Y':
            print('START_Y')
            self.start_position_y()
        if self.robot_mode == 'START_PEN':
            print('START_PEN')
            self.start_position_pen()
        if self.robot_mode == 'STOP':
            print('STOP')
        if self.robot_mode == 'NOT-AUS':
            print('NOT-AUS')

    def start_position_x(self):
        if self.get_switch_state(0) == 0:
            self.txt.setPwm(0, 512)
        else:
            self.txt.setPwm(0, 0)

        if self.get_switch_state(1) == 0:
            self.txt.setPwm(2, 512)
        else:
            self.txt.setPwm(2, 0)

        if self.get_switch_state(0) == 1 and self.get_switch_state(1) == 1:
            self.robot_mode = 'START_Y'

    def start_position_y(self):
        if self.get_switch_state(2) == 0:
            self.txt.setPwm(4, 512)
        if self.get_switch_state(2) == 1:
            self.txt.setPwm(4, 0)
            self.robot_mode = 'START_PEN'

    def start_position_pen(self):
        if self.get_switch_state(6) == 0:
            self.txt.setPwm(6, 512)
        if self.get_switch_state(6) == 1:
            self.txt.setPwm(6, 0)
            self.robot_mode = 'STOP'

    def get_switch_state(self, number):
        return self.txt.getCurrentInput(number)


if __name__ == "__main__":
    FtcGuiApplication(sys.argv)