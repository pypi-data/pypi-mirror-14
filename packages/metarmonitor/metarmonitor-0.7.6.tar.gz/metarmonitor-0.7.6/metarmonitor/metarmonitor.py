#!/usr/bin/env python
import os
import sys

import twilio
import PIL
from PIL import ImageTk
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from twilio.rest import TwilioRestClient

import metarxml
import metarmonitor_gui as gui

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
    from tkinter import messagebox

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


class Model:
    """Load resources and provide a means of selecting colour boxes from METAR colour states"""
    def __init__(self):
        self.sms_nbr = ''
        self.twilio_sid = ''
        self.twilio_auth = ''
        self.twilio_nbr = ''
        self.latest_colour_box_image = None
        self.previous_colour_box_image = None

        # Load the images (colour state boxes/arrows( used in the application)
        self.arrowup = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/arrowup.gif'))
        self.arrowdown = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/arrowdown.gif'))
        self.arrowstraight = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/arrowstraight.gif'))
        self.tick = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/tick.gif'))
        self.cross = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/cross.gif'))
        self.blue = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/blue.gif'))
        self.white = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/white.gif'))
        self.green = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/green.gif'))
        self.yellow1 = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/yellow1.gif'))
        self.yellow2 = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/yellow2.gif'))
        self.amber = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/amber.gif'))
        self.red = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/red.gif'))
        self.grey = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images/grey.gif'))

    def set_latest_colour_box(self, colour_state):
        """Set the colour of the latest METAR colour state box
        :param colour_state: The numeric METAR colour state (1-7)
        """
        if colour_state == 7:
            self.latest_colour_box_image = self.blue
        elif colour_state == 6:
            self.latest_colour_box_image = self.white
        elif colour_state == 5:
            self.latest_colour_box_image = self.green
        elif colour_state == 4:
            self.latest_colour_box_image = self.yellow1
        elif colour_state == 3:
            self.latest_colour_box_image = self.yellow2
        elif colour_state == 2:
            self.latest_colour_box_image = self.amber
        elif colour_state == 1:
            self.latest_colour_box_image = self.red

    def set_previous_colour_box(self, colour_state):
        """Set the colour of the previous METAR colour state box
        :param colour_state: The numeric METAR colour state (1-7)
        """
        if colour_state == 7:
            self.previous_colour_box_image = self.blue
        elif colour_state == 6:
            self.previous_colour_box_image = self.white
        elif colour_state == 5:
            self.previous_colour_box_image = self.green
        elif colour_state == 4:
            self.previous_colour_box_image = self.yellow1
        elif colour_state == 3:
            self.previous_colour_box_image = self.yellow2
        elif colour_state == 2:
            self.previous_colour_box_image = self.amber
        elif colour_state == 1:
            self.previous_colour_box_image = self.red

    def resource_path(self, relative):
        """Obtain a full OS resource path to enable images etc. to be easily referenced
        :param relative: The relative (to the application) path locating the image or data file
        """
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)


class Controller:
    """Main GUI controller, handles mouse, keyboard and data change events."""

    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.main_view = gui.MainView(self.root)

        self.metar1 = ''
        self.metar2 = ''
        self.metar3 = ''
        self.metar4 = ''
        self.metar_taf = ''
        self.taf = ''

        self.icao1 = None
        self.icao2 = None
        self.icao3 = None
        self.icao4 = None
        self.icao_taf = None

        self.metar1_prev_state = 0
        self.metar2_prev_state = 0
        self.metar3_prev_state = 0
        self.metar4_prev_state = 0

        self.monitoring = False

        self.main_view.controls_view.monitor_button.bind('<Button>', self.start_monitor)
        self.main_view.controls_view.monitor_button.bind('<Return>', self.start_monitor)

        self.main_view.controls_view.exit_button.bind('<Button>', self.exit_app)
        self.main_view.controls_view.exit_button.bind('<Return>', self.exit_app)

        self.main_view.controls_view.update_data_button.bind('<Button>', self.update_data_now)
        self.main_view.controls_view.update_data_button.bind('<Return>', self.update_data_now)

        self.main_view.metar_view.icao1_entry.bind('<KeyRelease>', self.caps)
        self.main_view.metar_view.icao2_entry.bind('<KeyRelease>', self.caps)
        self.main_view.metar_view.icao3_entry.bind('<KeyRelease>', self.caps)
        self.main_view.metar_view.icao4_entry.bind('<KeyRelease>', self.caps)
        self.main_view.taf_view.icao_taf_entry.bind('<KeyRelease>', self.caps)

    def run(self):
        """Start the application"""
        self.root.title('METAR and TAF Monitor v0.7BETA  - mark.baker@metoffice.gov.uk')
        self.root.deiconify()
        self.root.mainloop()

    def start_monitor(self, event):
        """Start the automatic monitoring of METARs and TAFs, initial messages are collected and fields updated
        before setting up scheduled checks
        :param event: Start Monitoring button pressed"""
        if not self.monitoring:
            self.monitoring = True
            self.update_data()
            self.data_check_sched()
            self.main_view.controls_view.monitor_button.configure(text='Monitoring...')
            self.main_view.controls_view.status_label.configure(text='checking status every 10 mins...')

    def data_check_sched(self):
        """Set a schedule for updating and checking METAR/TAF messages using a background scheduler. Each metar/taf
        update has its own job as this seems to work more reliably (jobs finishing promptly) than combining them all
        into one job"""
        scheduler = BackgroundScheduler()
        trigger = IntervalTrigger(seconds=600)

        scheduler.add_job(self.update_metar1, trigger)
        scheduler.add_job(self.update_metar2, trigger)
        scheduler.add_job(self.update_metar3, trigger)
        scheduler.add_job(self.update_metar4, trigger)
        scheduler.add_job(self.update_taf_monitor, trigger)
        scheduler.start()

    def update_data_now(self, event):
        """Response action for 'Update Now' button press - initiate update of METAR and TAF fields and logic
        :param event: 'Update Now' button pressed.
        """
        self.main_view.controls_view.update_data_button.configure(text='Update Now')
        self.update_data()

    def update_data(self):
        """Perform a 'batch' update of the METAR and TAF fields"""
        self.update_metar1()
        self.update_metar2()
        self.update_metar3()
        self.update_metar4()
        self.update_taf_monitor()

    def update_metar1(self):
        """Update METAR 1 (first ICAO from top of window) fields. If no ICAO has is entered, clear the fields, if a
        new or changed ICAO is entered then get the latest METAR, reset the previous METAR history and update the latest
        colour status.

        If the ICAO has
        not changed, get the latest METAR, update the previous and latest METAR colour boxes and arrows. Finally if
        colour state has increased or decreased change the arrow, send an information message to the screen and transmit
        and SMS text message if a phone number has been entered."""
        # no ICAO entered
        if self.main_view.metar_view.icao1.get() == '':
            self.main_view.metar_view.latest_metar1.set('')
            self.metar1_prev_state = 0
            self.icao1 = None
            self.main_view.metar_view.metar1_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar1_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar1_arrow_label.configure(image=self.model.arrowstraight)

        # Different or new ICAO entered
        elif self.main_view.metar_view.icao1.get() != self.icao1:
            self.icao1 = self.main_view.metar_view.icao1.get()
            self.main_view.metar_view.metar1_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar1_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar1_arrow_label.configure(image=self.model.arrowstraight)
            self.metar1 = metarxml.get_metar_data(self.main_view.metar_view.icao1.get())
            if self.metar1 is not None:
                self.metar1_prev_state = self.metar1[1]
                self.main_view.metar_view.latest_metar1.set(self.metar1[3])
                self.model.set_latest_colour_box(self.metar1[1])
                self.main_view.metar_view.metar1_now_label.configure(image=self.model.latest_colour_box_image)

        # ICAO unchanged, update if new METAR, update previous colour states and send notifications of changes
        elif self.main_view.metar_view.icao1.get() == self.icao1:
            new_metar1 = metarxml.get_metar_data(self.main_view.metar_view.icao1.get())
            if new_metar1 is not None:
                if new_metar1[0] != self.metar1[0]:
                    self.main_view.metar_view.latest_metar1.set(new_metar1[3])
                    self.model.set_latest_colour_box(new_metar1[1])
                    self.main_view.metar_view.metar1_now_label.configure(image=self.model.latest_colour_box_image)
                    self.model.set_previous_colour_box(self.metar1[1])
                    self.main_view.metar_view.metar1_last_label.configure(image=self.model.previous_colour_box_image)

                if new_metar1[1] < self.metar1_prev_state:
                    self.main_view.metar_view.metar1_arrow_label.configure(image=self.model.arrowdown)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao1 + ' DETERIORATED ' + new_metar1[3])
                    tk.messagebox.showinfo('Colour state change', self.icao1 + ' DETERIORATED')

                elif new_metar1[1] > self.metar1_prev_state and self.metar1_prev_state is not 0:
                    self.main_view.metar_view.metar1_arrow_label.configure(image=self.model.arrowup)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao1 + ' IMPROVEMENT ' + new_metar1[3])
                    tk.messagebox.showinfo('Colour state change', self.icao1 + ' IMPROVEMENT')

                else:
                    if new_metar1[1] == self.metar1_prev_state:
                        self.main_view.metar_view.metar1_arrow_label.configure(image=self.model.arrowstraight)

                self.metar1_prev_state = new_metar1[1]

    def update_metar2(self):
        """Update METAR 2 fields. If no ICAO has is entered, clear the fields, if a new or changed ICAO is entered then
        get the latest METAR, reset the previous METAR history and update the latest colour status.

        If the ICAO has not changed, get the latest METAR updated the previous and latest METAR colour boxes and arrows. Finally if
        colour state has increased or decreased change the arrow, send an information message to the screen and transmit
        and SMS text message if a phone number has been entered."""
        # no ICAO entered
        if self.main_view.metar_view.icao2.get() == '':
            self.main_view.metar_view.latest_metar2.set('')
            self.metar2_prev_state = 0
            self.icao2 = None
            self.main_view.metar_view.metar2_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar2_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar2_arrow_label.configure(image=self.model.arrowstraight)

        # Different or new ICAO entered
        elif self.main_view.metar_view.icao2.get() != self.icao2:
            self.icao2 = self.main_view.metar_view.icao2.get()
            self.main_view.metar_view.metar2_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar2_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar2_arrow_label.configure(image=self.model.arrowstraight)
            self.metar2 = metarxml.get_metar_data(self.main_view.metar_view.icao2.get())
            if self.metar2 is not None:
                self.metar2_prev_state = self.metar2[1]
                self.main_view.metar_view.latest_metar2.set(self.metar2[3])
                self.model.set_latest_colour_box(self.metar2[1])
                self.main_view.metar_view.metar2_now_label.configure(image=self.model.latest_colour_box_image)

        # ICAO unchanged, update if new METAR, update previous colour states and send notifications of changes
        elif self.main_view.metar_view.icao2.get() == self.icao2:
            new_metar2 = metarxml.get_metar_data(self.main_view.metar_view.icao2.get())
            if new_metar2 is not None:
                if new_metar2[0] != self.metar2[0]:
                    self.main_view.metar_view.latest_metar2.set(new_metar2[3])
                    self.model.set_latest_colour_box(new_metar2[1])
                    self.main_view.metar_view.metar2_now_label.configure(image=self.model.latest_colour_box_image)
                    self.model.set_previous_colour_box(self.metar2[1])
                    self.main_view.metar_view.metar2_last_label.configure(image=self.model.previous_colour_box_image)

                if new_metar2[1] < self.metar2_prev_state:
                    self.main_view.metar_view.metar2_arrow_label.configure(image=self.model.arrowdown)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao2 + ' DETERIORATED ' + new_metar2[3])
                    tk.messagebox.showinfo('Colour state change', self.icao2 + ' DETERIORATED')

                elif new_metar2[1] > self.metar2_prev_state and self.metar2_prev_state is not 0:
                    self.main_view.metar_view.metar2_arrow_label.configure(image=self.model.arrowup)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao2 + ' IMPROVEMENT ' + new_metar2[3])
                    tk.messagebox.showinfo('Colour state change', self.icao2 + ' IMPROVEMENT')

                else:
                    if new_metar2[1] == self.metar2_prev_state:
                        self.main_view.metar_view.metar2_arrow_label.configure(image=self.model.arrowstraight)

                self.metar2_prev_state = new_metar2[1]
                self.metar2 = new_metar2
                
    def update_metar3(self):
        """Update METAR 3 fields. If no ICAO has is entered, clear the fields, if a new or changed ICAO is entered then
        get the latest METAR, reset the previous METAR history and update the latest colour status.

        If the ICAO has not changed, get the latest METAR updated the previous and latest METAR colour boxes and arrows. Finally if
        colour state has increased or decreased change the arrow, send an information message to the screen and transmit
        and SMS text message if a phone number has been entered."""
        # no ICAO entered
        if self.main_view.metar_view.icao3.get() == '':
            self.main_view.metar_view.latest_metar3.set('')
            self.metar3_prev_state = 0
            self.icao3 = None
            self.main_view.metar_view.metar3_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar3_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar3_arrow_label.configure(image=self.model.arrowstraight)

        # Different or new ICAO entered
        elif self.main_view.metar_view.icao3.get() != self.icao3:
            self.icao3 = self.main_view.metar_view.icao3.get()
            self.main_view.metar_view.metar3_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar3_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar3_arrow_label.configure(image=self.model.arrowstraight)
            self.metar3 = metarxml.get_metar_data(self.main_view.metar_view.icao3.get())
            if self.metar3 is not None:
                self.metar3_prev_state = self.metar3[1]
                self.main_view.metar_view.latest_metar3.set(self.metar3[3])
                self.model.set_latest_colour_box(self.metar3[1])
                self.main_view.metar_view.metar3_now_label.configure(image=self.model.latest_colour_box_image)

        # ICAO unchanged, update if new METAR, update previous colour states and send notifications of changes
        elif self.main_view.metar_view.icao3.get() == self.icao3:
            new_metar3 = metarxml.get_metar_data(self.main_view.metar_view.icao3.get())
            if new_metar3 is not None:
                if new_metar3[0] != self.metar3[0]:
                    self.main_view.metar_view.latest_metar3.set(new_metar3[3])
                    self.model.set_latest_colour_box(new_metar3[1])
                    self.main_view.metar_view.metar3_now_label.configure(image=self.model.latest_colour_box_image)
                    self.model.set_previous_colour_box(self.metar3[1])
                    self.main_view.metar_view.metar3_last_label.configure(image=self.model.previous_colour_box_image)

                if new_metar3[1] < self.metar3_prev_state:
                    self.main_view.metar_view.metar3_arrow_label.configure(image=self.model.arrowdown)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao3 + ' DETERIORATED ' + new_metar3[3])
                    tk.messagebox.showinfo('Colour state change', self.icao3 + ' DETERIORATED')

                elif new_metar3[1] > self.metar3_prev_state and self.metar3_prev_state is not 0:
                    self.main_view.metar_view.metar3_arrow_label.configure(image=self.model.arrowup)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao3 + ' IMPROVEMENT ' + new_metar3[3])
                    tk.messagebox.showinfo('Colour state change', self.icao3 + ' IMPROVEMENT')

                else:
                    if new_metar3[1] == self.metar3_prev_state:
                        self.main_view.metar_view.metar3_arrow_label.configure(image=self.model.arrowstraight)

                self.metar3_prev_state = new_metar3[1]
                self.metar3 = new_metar3

    def update_metar4(self):
        """Update METAR 4 fields. If no ICAO has is entered, clear the fields, if a new or changed ICAO is entered then
        get the latest METAR, reset the previous METAR history and update the latest colour status.

        If the ICAO has not changed, get the latest METAR updated the previous and latest METAR colour boxes and arrows. Finally if
        colour state has increased or decreased change the arrow, send an information message to the screen and transmit
        and SMS text message if a phone number has been entered."""
        # no ICAO entered
        if self.main_view.metar_view.icao4.get() == '':
            self.main_view.metar_view.latest_metar4.set('')
            self.metar4_prev_state = 0
            self.icao4 = None
            self.main_view.metar_view.metar4_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar4_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar4_arrow_label.configure(image=self.model.arrowstraight)

        # Different or new ICAO entered
        elif self.main_view.metar_view.icao4.get() != self.icao4:
            self.icao4 = self.main_view.metar_view.icao4.get()
            self.main_view.metar_view.metar4_now_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar4_last_label.configure(image=self.model.grey)
            self.main_view.metar_view.metar4_arrow_label.configure(image=self.model.arrowstraight)
            self.metar4 = metarxml.get_metar_data(self.main_view.metar_view.icao4.get())
            if self.metar4 is not None:
                self.metar4_prev_state = self.metar4[1]
                self.main_view.metar_view.latest_metar4.set(self.metar4[3])
                self.model.set_latest_colour_box(self.metar4[1])
                self.main_view.metar_view.metar4_now_label.configure(image=self.model.latest_colour_box_image)

        # ICAO unchanged, update if new METAR, update previous colour states and send notifications of changes
        elif self.main_view.metar_view.icao4.get() == self.icao4:
            new_metar4 = metarxml.get_metar_data(self.main_view.metar_view.icao4.get())
            if new_metar4 is not None:
                if new_metar4[0] != self.metar4[0]:
                    self.main_view.metar_view.latest_metar4.set(new_metar4[3])
                    self.model.set_latest_colour_box(new_metar4[1])
                    self.main_view.metar_view.metar4_now_label.configure(image=self.model.latest_colour_box_image)
                    self.model.set_previous_colour_box(self.metar4[1])
                    self.main_view.metar_view.metar4_last_label.configure(image=self.model.previous_colour_box_image)

                if new_metar4[1] < self.metar4_prev_state:
                    self.main_view.metar_view.metar4_arrow_label.configure(image=self.model.arrowdown)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao4 + ' DETERIORATED ' + new_metar4[3])
                    tk.messagebox.showinfo('Colour state change', self.icao4 + ' DETERIORATED')

                elif new_metar4[1] > self.metar4_prev_state and self.metar4_prev_state is not 0:
                    self.main_view.metar_view.metar4_arrow_label.configure(image=self.model.arrowup)
                    if self.main_view.controls_view.phone_nbr.get() != '':
                        self.send_twilio_sms(self.icao4 + ' IMPROVEMENT ' + new_metar4[3])
                    tk.messagebox.showinfo('Colour state change', self.icao4 + ' IMPROVEMENT')

                else:
                    if new_metar4[1] == self.metar4_prev_state:
                        self.main_view.metar_view.metar4_arrow_label.configure(image=self.model.arrowstraight)

                self.metar4_prev_state = new_metar4[1]
                self.metar4 = new_metar4

    def update_taf_monitor(self):
        """Check if there is an ICAO entered into the TAF monitor frames - if not then clear the fields
         otherwise get a new message and update the TAF monitor fields."""
        # No ICAO
        if self.main_view.taf_view.icao_taf_entry.get() == '':
            self.icao_taf = None
            self.metar_taf = ''
            self.main_view.taf_view.taf_status_result.configure(image=self.model.grey)
            self.main_view.taf_view.metar_taf_colour.configure(image=self.model.grey)
            self.main_view.taf_view.latest_metar.set('')
            self.main_view.taf_view.latest_taf.set('')

        else:
            self.icao_taf = self.main_view.taf_view.icao_taf.get()
            new_metar_taf = metarxml.get_metar_data(self.main_view.taf_view.icao_taf_entry.get())
            new_taf = metarxml.get_taf_data(self.main_view.taf_view.icao_taf_entry.get())
            if new_metar_taf is not None:
                if self.metar_taf != new_metar_taf:
                    self.main_view.taf_view.latest_metar.set(new_metar_taf[3])
                    self.model.set_latest_colour_box(new_metar_taf[1])
                    self.main_view.taf_view.metar_taf_colour.configure(image=self.model.latest_colour_box_image)
                    self.metar_taf = new_metar_taf

            if self.taf is not None:
                if self.taf != new_taf:
                    self.main_view.taf_view.latest_taf.set(new_taf[3])
                    self.taf = new_taf

            if new_metar_taf[1] >= new_taf[1]:
                self.main_view.taf_view.taf_status_result.configure(image=self.model.tick)
            else:

                self.main_view.taf_view.taf_status_result.configure(image=self.model.cross)
                if self.main_view.controls_view.phone_nbr.get() != '':
                    self.send_twilio_sms(self.icao_taf + ' TAF BUST!')
                tk.messagebox.showinfo('TAF monitor', self.icao_taf +' TAF BUST!')


    def caps(self, event):
        """Capatilise characters typed into ICAO boxes
        :param event: Keyboard character typed into an ICAO box."""
        self.main_view.metar_view.icao1.set(self.main_view.metar_view.icao1.get().upper())
        self.main_view.metar_view.icao2.set(self.main_view.metar_view.icao2.get().upper())
        self.main_view.metar_view.icao3.set(self.main_view.metar_view.icao3.get().upper())
        self.main_view.metar_view.icao4.set(self.main_view.metar_view.icao4.get().upper())
        self.main_view.taf_view.icao_taf.set(self.main_view.taf_view.icao_taf.get().upper())

    def send_twilio_sms(self, message):
        """Send an SMS text message using the Twilio service (www.twilio.com)
        :param message: Text message to send via SMS. SID/TOKEN and account number are provided with a Twilio trial account
        """
        try:
            sid = 'ACeb7c76bb2c603e8705066259dd312ea5'
            token = 'c8d1d99771afe9f781f9f7366f341af6'
            acc_nbr = '+441484906108'
            sms_nbr = self.main_view.controls_view.phone_nbr.get()
            twilio_client = TwilioRestClient(sid, token)
            twilio_client.messages.create(body=message, from_=acc_nbr, to=sms_nbr)
        except twilio.TwilioRestException as e:
            tk.messagebox.showerror('SMS message error', 'SMS sending error: ' + e)

    @staticmethod
    def exit_app(self):
        sys.exit()


if __name__ == '__main__':
    controller = Controller()
    controller.run()
