#!/usr/bin/env python
import os
import sys

import PIL
from PIL import ImageTk

if sys.version_info[0] < 3:
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk as ttk

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


class MainView:
    """Main GUI class responsible for initiating separate window frames for the various monitors."""

    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, padx=5, pady=5)
        self.metar_view = METARview(master)
        self.taf_view = TAFview(master)
        self.controls_view = ControlsView(master)


class METARview:
    """Label window frame containing the widgets for METAR monitoring setup. """

    def __init__(self, root):
        self.arrowup = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/arrowup.gif'))
        self.arrowdown = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/arrowdown.gif'))
        self.arrowstraight = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/arrowstraight.gif'))
        self.grey = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/grey.gif'))

        self.frame_metar_monitor = tk.LabelFrame(root, text='Diversion Watch (METAR monitor)')
        self.frame_metar_monitor.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        self.icao1_label = ttk.Label(self.frame_metar_monitor, text="ICAO :")
        self.icao1_label.grid(row=1, column=0, padx=5, pady=5)

        self.icao1 = tk.StringVar()
        self.icao1_entry = ttk.Entry(self.frame_metar_monitor, textvariable=self.icao1, width=6)
        self.icao1_entry.grid(row=1, column=1, padx=5, pady=5)

        self.icao2_label = ttk.Label(self.frame_metar_monitor, text="ICAO :")
        self.icao2_label.grid(row=2, column=0, padx=5, pady=5)

        self.icao2 = tk.StringVar()
        self.icao2_entry = ttk.Entry(self.frame_metar_monitor, textvariable=self.icao2, width=6)
        self.icao2_entry.grid(row=2, column=1, padx=5, pady=5)

        self.icao3_label = ttk.Label(self.frame_metar_monitor, text="ICAO :")
        self.icao3_label.grid(row=3, column=0, padx=5, pady=5)

        self.icao3 = tk.StringVar()
        self.icao3_entry = ttk.Entry(self.frame_metar_monitor, textvariable=self.icao3, width=6)
        self.icao3_entry.grid(row=3, column=1, padx=5, pady=5)

        self.icao4_label = ttk.Label(self.frame_metar_monitor, text="ICAO :")
        self.icao4_label.grid(row=4, column=0, padx=5, pady=5)

        self.icao4 = tk.StringVar()
        self.icao4_entry = ttk.Entry(self.frame_metar_monitor, textvariable=self.icao4, width=6)
        self.icao4_entry.grid(row=4, column=1, padx=5, pady=5)

        self.prev_last_label = ttk.Label(self.frame_metar_monitor, text='Previous')
        self.prev_last_label.grid(row=0, column=2, padx=5, pady=5)

        self.prev_now_label = ttk.Label(self.frame_metar_monitor, text='Latest')
        self.prev_now_label.grid(row=0, column=3, padx=5, pady=5)

        self.metar1_last_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar1_last_label.grid(row=1, column=2, padx=5, pady=5)

        self.metar1_now_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar1_now_label.grid(row=1, column=3, padx=5, pady=5)

        self.metar2_last_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar2_last_label.grid(row=2, column=2, padx=5, pady=5)

        self.metar2_now_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar2_now_label.grid(row=2, column=3, padx=5, pady=5)

        self.metar3_last_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar3_last_label.grid(row=3, column=2, padx=5, pady=5)

        self.metar3_now_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar3_now_label.grid(row=3, column=3, padx=5, pady=5)

        self.metar4_last_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar4_last_label.grid(row=4, column=2, padx=5, pady=5)

        self.metar4_now_label = ttk.Label(self.frame_metar_monitor, image=self.grey)
        self.metar4_now_label.grid(row=4, column=3, padx=5, pady=5)

        self.metar1_arrow_label = ttk.Label(self.frame_metar_monitor, image=self.arrowstraight)
        self.metar1_arrow_label.grid(row=1, column=4, padx=5, pady=5)

        self.metar2_arrow_label = ttk.Label(self.frame_metar_monitor, image=self.arrowstraight)
        self.metar2_arrow_label.grid(row=2, column=4, padx=5, pady=5)

        self.metar3_arrow_label = ttk.Label(self.frame_metar_monitor, image=self.arrowstraight)
        self.metar3_arrow_label.grid(row=3, column=4, padx=5, pady=5)

        self.metar4_arrow_label = ttk.Label(self.frame_metar_monitor, image=self.arrowstraight)
        self.metar4_arrow_label.grid(row=4, column=4, padx=5, pady=5)

        self.latest_metar1_label = ttk.Label(self.frame_metar_monitor, text="Latest METAR/SPECI :")
        self.latest_metar1_label.grid(sticky=tk.W, row=0, column=5, padx=5, pady=5)

        self.latest_metar1 = tk.StringVar()
        self.latest_metar1_result = ttk.Label(self.frame_metar_monitor, textvariable=self.latest_metar1, width=80,
                                              wraplength=480, justify='left', anchor=tk.W)
        self.latest_metar1_result.grid(row=1, column=5, padx=5, pady=5)

        self.latest_metar2 = tk.StringVar()
        self.latest_metar2_result = ttk.Label(self.frame_metar_monitor, textvariable=self.latest_metar2, width=80,
                                              wraplength=480, justify='left', anchor=tk.W)
        self.latest_metar2_result.grid(row=2, column=5, padx=5, pady=5)

        self.latest_metar3 = tk.StringVar()
        self.latest_metar3_result = ttk.Label(self.frame_metar_monitor, textvariable=self.latest_metar3, width=80,
                                              wraplength=480, justify='left', anchor=tk.W)
        self.latest_metar3_result.grid(row=3, column=5, padx=5, pady=5)

        self.latest_metar4 = tk.StringVar()
        self.latest_metar4_result = ttk.Label(self.frame_metar_monitor, textvariable=self.latest_metar4, width=80,
                                              wraplength=480, justify='left', anchor=tk.W)
        self.latest_metar4_result.grid(row=4, column=5, padx=5, pady=5)

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)


class TAFview:
    """Label window frame containing the widgets for . """

    def __init__(self, root):
        self.tick = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/tick.gif'))
        self.cross = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/cross.gif'))
        self.blue = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/blue.gif'))
        self.white = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/white.gif'))
        self.green = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__),'images/green.gif'))
        self.yellow1 = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/yellow1.gif'))
        self.yellow2 = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/yellow2.gif'))
        self.amber = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/amber.gif'))
        self.red = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/red.gif'))
        self.grey = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/grey.gif'))

        self.frame_taf_monitor = tk.LabelFrame(root, text='TAF monitor')
        self.frame_taf_monitor.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.taf_label = ttk.Label(self.frame_taf_monitor, text="ICAO :")
        self.taf_label.grid(row=1, column=0, padx=5, pady=5)

        self.icao_taf = tk.StringVar()
        self.icao_taf_entry = ttk.Entry(self.frame_taf_monitor, textvariable=self.icao_taf, width=6)
        self.icao_taf_entry.grid(row=1, column=1, padx=5, pady=5)

        self.colour_label = ttk.Label(self.frame_taf_monitor, text='Current')
        self.colour_label.grid(row=0, column=2, padx=0, pady=5)

        self.metar_taf_colour = ttk.Label(self.frame_taf_monitor, image=self.grey)
        self.metar_taf_colour.grid(row=1, column=2, padx=5, pady=5)

        self.taf_status_label = ttk.Label(self.frame_taf_monitor, text='TAF Status')
        self.taf_status_label.grid(row=0, column=3, padx=5, pady=5)

        self.taf_status_label = ttk.Label(self.frame_taf_monitor, text='Latest TAF:')
        self.taf_status_label.grid(sticky=tk.W, row=0, column=5, padx=5, pady=5)

        self.taf_status_result = ttk.Label(self.frame_taf_monitor, image=self.grey)
        self.taf_status_result.grid(row=1, column=3, padx=5, pady=5)

        self.latest_taf = tk.StringVar()
        self.latest_taf_result = ttk.Label(self.frame_taf_monitor, textvariable=self.latest_taf, width=85,
                                           wraplength=510, justify='left', anchor=tk.W)
        self.latest_taf_result.grid(row=1, column=5, padx=5, pady=5)

        self.latest_metar_label = ttk.Label(self.frame_taf_monitor, text="METAR/SPECI:")
        self.latest_metar_label.grid(row=2, column=2, padx=5, pady=5, columnspan=2)

        self.latest_metar = tk.StringVar()
        self.latest_metar_result = ttk.Label(self.frame_taf_monitor, textvariable=self.latest_metar, width=85,
                                             wraplength=510, justify='left', anchor=tk.W)
        self.latest_metar_result.grid(sticky=tk.W, row=2, column=5, padx=5, pady=5, columnspan=6)

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)


class ControlsView:
    def __init__(self, root):
        validcmd = (root.register(validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.frame_controls = ttk.Frame(root)
        self.frame_controls.grid(row=2, column=0, padx=5, pady=5)

        self.monitor_button = ttk.Button(self.frame_controls, text='Start Monitor', width=15)
        self.monitor_button.grid(sticky=tk.W, row=0, column=0, padx=5, pady=5)

        self.status_label = ttk.Label(self.frame_controls, width=30, text='Status: ')
        self.status_label.grid(sticky=tk.W, row=0, column=1, padx=5, pady=5)

        self.phone_label = ttk.Label(self.frame_controls, text="SMS Alerts (disabled):")
        self.phone_label.grid(sticky=tk.W, row=0, column=2, padx=5, pady=5)

        self.phone_nbr = tk.StringVar()
        self.phone_entry = ttk.Entry(self.frame_controls, textvariable=self.phone_nbr, width=14, validate='key',
                                     validatecommand=validcmd)
        self.phone_entry.grid(sticky=tk.W, row=0, column=3, padx=5, pady=5)

        self.update_data_button = ttk.Button(self.frame_controls, text='Update Now')
        self.update_data_button.grid(sticky=tk.W, row=0, column=4, padx=5, pady=5)

        self.exit_button = ttk.Button(self.frame_controls, text='Exit')
        self.exit_button.grid(sticky=tk.E, row=0, column=5, padx=5, pady=5)


def validate_int(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
    """

    :param action:
    :param index:
    :param value_if_allowed:
    :param prior_value:
    :param text:
    :param validation_type:
    :param trigger_type:
    :param widget_name:
    :return:
    """
    if not value_if_allowed:
        return True

    if text in '0123456789':
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False


def validate_float(self, action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
    # action=1 -> insert
    if action == '1':
        if text in '0123456789':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True
