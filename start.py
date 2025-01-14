#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import math
import sys
import ftrobopy                                              # Import the ftrobopy module
from TouchStyle import *

class Command:
    STOP = 0
    START_POS_X = 1
    START_POS_Y = 2
    START_POS_PEN = 3
    END_POS_PEN = 4
    TO_MIDDLE_X = 5
    TO_MIDDLE_Y = 6
    MOVE_VECTOR = 7
    ELLIPSE = 8
    FLOWER = 9
    EXPLODE = 666

class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        w = TouchWindow("PLOTTER MD")

        txt_ip = os.environ.get('TXT_IP')                    # try to read TXT_IP environment variable
        try:
            self.txt = ftrobopy.ftrobopy("localhost", 65000, 0.100 ) # WLAN - connect to TXT's IO controller
            # self.txt = ftrobopy.ftrobopy("192.168.178.34", 65000, 0.100, "192.168.178.34", ) # LOCAL - connect to TXT's IO controller
        except:
            self.txt = None

        vbox = QVBoxLayout()


        if not self.txt:
            # display error of TXT could not be connected
            # error messages is centered and may span
            # over several lines
            err_msg = QLabel("Error connecting IO server")   # create the error message label
            err_msg.setWordWrap(True)                        # allow it to wrap over several lines
            err_msg.setAlignment(Qt.AlignCenter)             # center it horizontally
            vbox.addWidget(err_msg)                          # attach it to the main output area
        else:
            # initialization went fine. So the main gui
            # is being drawn
            button = QPushButton("STOP")                # create a button labeled "Toggle O1"
            button.clicked.connect(self.on_button_clicked)   # connect button to event handler
            vbox.addWidget(button)                           # attach it to the main output area

            button2 = QPushButton("GO")  # create a button labeled "Toggle O1"
            button2.clicked.connect(self.on_button2_clicked)  # connect button to event handler
            vbox.addWidget(button2)  # attach it to the main output area

            # configure all TXT outputs to normal mode
            M = [ self.txt.C_MOTOR, self.txt.C_MOTOR, self.txt.C_MOTOR, self.txt.C_MOTOR ]
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
            self.alpha_step = math.pi / 36
            self.beta_step = self.alpha_step / 10
            self.counter_x = 0
            self.counter_y = 0
            self.counter_z = 0
            self.alpha = 0
            self.beta = 0
            self.m1 = 0
            self.m2 = 0
            self.m3 = 0
            self.m4 = 0
            self.robot_mode = []
            self.timer = QTimer(self)  # create a timer
            self.timer.timeout.connect(self.on_timer)  # connect timer to on_timer slot

            self.run()
            print (self.robot_mode)

        w.centralWidget.setLayout(vbox)
        w.show()
        self.exec_()

    def run(self):
        self.reset_counter()
        self.alpha = 0
        self.beta = 0

        self.m1 = self.txt.motor(1)
        self.m2 = self.txt.motor(2)
        self.m3 = self.txt.motor(3)
        self.m4 = self.txt.motor(4)

        self.robot_mode = []
        self.robot_mode += [[Command.START_POS_Y, (0, 0)], [Command.START_POS_X, (0, 0)],
                            [Command.START_POS_PEN, (0, 0)]]
        self.robot_mode += [[Command.TO_MIDDLE_Y, (0, 0)], [Command.TO_MIDDLE_X, (0, 0)]]
        self.robot_mode += [[Command.END_POS_PEN, (0, 0)]]
        # self.robot_mode += [[Command.ELLIPSE, (15, 10)]]
        self.robot_mode += [[Command.FLOWER, (20, 10)]]
        # self.robot_mode += [[Command.MOVE_VECTOR, (5, 0)], [Command.MOVE_VECTOR, (0, 5)], [Command.MOVE_VECTOR, (-5, 0)], [Command.MOVE_VECTOR, (0, -5)]]
        # self.robot_mode += [[Command.MOVE_VECTOR, (10, 0)], [Command.MOVE_VECTOR, (0, 10)], [Command.MOVE_VECTOR, (-10, 0)], [Command.MOVE_VECTOR, (0, -10)]]
        # self.robot_mode += [[Command.MOVE_VECTOR, (10, 0)], [Command.MOVE_VECTOR, (0, 10)], [Command.MOVE_VECTOR, (-10, 0)], [Command.MOVE_VECTOR, (0, -10)]]
        self.robot_mode += [[Command.START_POS_PEN, (0, 0)], [Command.STOP]]

        self.timer.start(100)  # fire timer every 100ms (10 hz)

    # an event handler for our button (called a "slot" in qt)
    # it will be called whenever the user clicks the button
    def on_button_clicked(self):
        self.timer.stop()
        self.txt.stopAll()

    def on_button2_clicked(self):
        self.run()

    # an event handler for the timer (also a qt slot)
    def on_timer(self):
        current_command = list(self.robot_mode[0])[0]
        if current_command == Command.START_POS_X:
            print('START_X')
            self.start_position_x()
        if current_command == Command.START_POS_Y:
            print('START_Y')
            self.start_position_y()
        if current_command== Command.START_POS_PEN:
            print('START_PEN')
            self.start_position_pen()
        if current_command== Command.END_POS_PEN:
            print('END_PEN')
            self.end_position_pen()
        if current_command == Command.STOP:
            print('STOP')
            self.timer.stop()
        if current_command == Command.TO_MIDDLE_X:
            print('TO_MIDDLE_X')
            self.centre_position_x()
        if current_command == Command.TO_MIDDLE_Y:
            print('TO_MIDDLE_Y')
            self.centre_position_y()
        if current_command == Command.ELLIPSE:
            print('ELLIPSE')
            radius = list(self.robot_mode[0])[1]
            self.draw_ellipse(radius[0], radius[1])
        if current_command == Command.FLOWER:
            print('FLOWER')
            radius = list(self.robot_mode[0])[1]
            self.draw_flower(radius[0], radius[1])
        if current_command == Command.MOVE_VECTOR:
            pos = list(self.robot_mode[0])[1]
            print('MOVE', pos[0], ' / ', pos[1])
            self.draw_vector(pos[0], pos[1])

    def start_position_x(self):
        if self.get_switch_state(0) == 0:
            self.m1.setSpeed(512)
        else:
            self.m1.setSpeed(0)

        if self.get_switch_state(1) == 0:
            self.m2.setSpeed(512)
        else:
            self.m2.setSpeed(0)

        if self.get_switch_state(0) == 1 and self.get_switch_state(1) == 1:
            self.next_command()

    def start_position_y(self):
        if self.get_switch_state(2) == 0:
            self.m3.setSpeed(512)
        if self.get_switch_state(2) == 1:
            self.m3.setSpeed(0)
            self.next_command()

    def start_position_pen(self):
        print('Switch= ', self.get_switch_state(6))
        if self.get_switch_state(6) == 0:
            self.m4.setSpeed(256)
        if self.get_switch_state(6) == 1:
            self.m4.setSpeed(0)
            self.counter_z = 0
            self.next_command()

    def end_position_pen(self):
        self.counter_z += 1
        if self.counter_z < 3:
            self.m4.setSpeed(-128)
        else:
            self.m4.setSpeed(0)
            self.next_command()

    def centre_position_x(self):
        if self.counter_x < 40:
            self.counter_x += 1
            self.txt.SyncDataBegin()
            self.m1.setSpeed(-512)
            self.m2.setSpeed(-512)
            self.txt.SyncDataEnd()
        else:
            self.txt.SyncDataBegin()
            self.m1.setSpeed(0)
            self.m2.setSpeed(0)
            self.txt.SyncDataEnd()
            self.counter_x = 0
            self.next_command()

    def centre_position_y(self):
        if self.counter_y < 40:
            self.counter_y += 1
            self.m3.setSpeed(-512)
        else:
            self.m3.setSpeed(0)
            self.counter_y = 0
            self.next_command()


    def get_switch_state(self, number):
        return self.txt.getCurrentInput(number)


    def next_command(self):
        self.reset_counter()
        self.robot_mode.remove(self.robot_mode[0])
        print('next: ', self.robot_mode[0])

    def draw_vector(self, x, y):
        # calculate speed on x/y for a time interval
        ax = abs(x)
        ay = abs(y)
        max_val = max(ax, ay)
        spd_x = int(512 / max_val * ax)
        spd_y = int(512 / max_val * ay)
        if x < 0: spd_x = -spd_x
        if y < 0: spd_y = -spd_y

        print("vector ", spd_x, spd_y, self.counter_x, self.counter_y, x, y)
        self.txt.SyncDataBegin()
        if ax > self.counter_x:
            self.counter_x += 1
            self.m1.setSpeed(spd_x)
            self.m2.setSpeed(spd_x)
        else:
            self.m1.setSpeed(0)
            self.m2.setSpeed(0)
        if ay > self.counter_y:
            self.counter_y += 1
            self.m3.setSpeed(spd_y)
        else:
            self.m3.setSpeed(0)

        self.txt.SyncDataEnd()

        if ax <= self.counter_x and ay <= self.counter_y:
            self.stop_all()
            self.next_command()

    def draw_ellipse(self, rad_x, rad_y):
        # draw circle - start at 0/rad_y from centre
        self.reset_counter() # make sure, vector function doesn't decide to stop circle
        if self.alpha <= 2*math.pi:
            x_pos_delta = (-math.cos(self.alpha + self.alpha_step) - math.cos(self.alpha)) * rad_x
            y_pos_delta = (-math.sin(self.alpha + self.alpha_step) - math.sin(self.alpha)) * rad_y
            self.draw_vector(x_pos_delta, y_pos_delta)
            self.alpha += self.alpha_step
        else:
            self.stop_all()
            self.next_command()

    def draw_flower(self, radius_outside, radius_inside):
        # draw circle - start at 0/rad_y from centre
        self.reset_counter()  # make sure, vector function doesn't decide to stop circle
        if self.beta <= 2 * math.pi:
            x_pos_delta = (-math.cos(self.alpha + self.alpha_step) - math.cos(self.alpha)) * radius_outside
            y_pos_delta = (-math.sin(self.alpha + self.alpha_step) - math.sin(self.alpha)) * radius_outside
            x_pos_delta += (-math.cos(self.beta + self.beta_step) - math.cos(self.beta)) * radius_inside
            y_pos_delta += (-math.sin(self.beta + self.beta_step) - math.sin(self.beta)) * radius_inside
            self.draw_vector(x_pos_delta, y_pos_delta)
            self.alpha += self.alpha_step
            self.beta += self.beta_step
            if self.alpha > 2 * math.pi:
                self.alpha -= 2 * math.pi
        else:
            self.stop_all()
            self.next_command()

    def stop_all(self):
        self.m1.setSpeed(0)
        self.m2.setSpeed(0)
        self.m3.setSpeed(0)

    def reset_counter(self):
        self.counter_x = 0
        self.counter_y = 0
        self.counter_z = 0

if __name__ == "__main__":
    FtcGuiApplication(sys.argv)