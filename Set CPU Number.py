#!/usr/bin/python
"""
Collect Info

To be used in a Jamf Pro workflow to prompt a user/tech for info

Heavily cribbed from Jamf's iPhone ordering script:
https://github.com/jamfit/iPhone-Ordering
"""

import AppKit
import sys
import os
import Tkinter
import tkFont
import tkMessageBox
import subprocess
import plistlib

# Path to Jamf binary
JAMF = "/usr/local/bin/jamf"

PLISTPATH = "/Library/Application Support/UNCA/db/deploy.plist"

# base64-encoded GIF for "icon" at the top of the GUI
# MUST BE A GIF!
mbp_icon = '''
R0lGODlhLAGWAMQfADc3N7KysvX19URERJaWltLS0qurq/v7+8XFxRQUFCUlJczMzPj4+GlpafHx8bu7u3Jycuzs7GJiYo2NjeTk5IGBgVNTU3t7e6SkpNzc3FtbWwcHB/7+/gAAAP///wAAACH/C1hNUCBEYXRhWE1QPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS4zLWMwMTEgNjYuMTQ1NjYxLCAyMDEyLzAyLzA2LTE0OjU2OjI3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M2IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjdFMEY3NDkyNjhEODExRTdBMDlCOTI2NjA4QjYwMzU0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjdFMEY3NDkzNjhEODExRTdBMDlCOTI2NjA4QjYwMzU0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RjY2Q0NGN0Y2OENEMTFFN0EwOUI5MjY2MDhCNjAzNTQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RjY2Q0NGODA2OENEMTFFN0EwOUI5MjY2MDhCNjAzNTQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9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
'''

class App:
    def __init__(self, master):
        """Main GUI window"""
        self.master = master
        self.master.resizable(False, False)
        self.master.title("Assign CPU Number")

        self.master.protocol("WM_DELETE_WINDOW", self.cancel)
        self.master.call('wm', 'attributes', '.', '-topmost', True)
        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        self.master.geometry("+{0}+{1}".format(x, y))
        # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        # self.master.overrideredirect(1)
        # self.master.geometry("%dx%d+0+0" % (w, h))

        bgcolor = '#F0F0F0'
        self.master.tk_setPalette(background=bgcolor,
                                  highlightbackground=bgcolor)

        font = tkFont.nametofont('TkDefaultFont')
        font.config(family='system',
                    size=14)
        self.master.option_add("*Font", font)

        menu_bar = Tkinter.Menu(self.master)
        self.master.config(menu=menu_bar)

        print('Starting app')

        # Input variables
        self.input_assigned_computer = Tkinter.StringVar()


        # Get icon
        self.icon_data = Tkinter.PhotoImage(data=mbp_icon)

        # Icon Frame
        self.frame1 = Tkinter.Frame(self.master)
        self.photo_canvas = Tkinter.Canvas(self.frame1, width=300, height=150)
        self.photo_canvas.pack()
        self.icon = self.photo_canvas.create_image(0, 0, anchor="nw", image=self.icon_data)
        self.frame1.pack(padx=40, pady=(30, 5))



        # Inputs frame
        self.frame3 = Tkinter.Frame(self.master)

        computer_label = Tkinter.Label(self.frame3, text="Please enter the computer number located\n on the sticker label after the letters \"CPU\":")
        computer_label.pack()
        self.entry_assigned_computer = Tkinter.Entry(self.frame3,
                                                 background='white',
                                                 textvariable=self.input_assigned_computer,
                                                 width=30)
        self.entry_assigned_computer.pack(pady=(0, 20))


        self.frame3.pack(padx=40, pady=5)

        # Buttons
        self.frame5 = Tkinter.Frame(self.master)
        submit = Tkinter.Button(self.frame5, text='Assign', height=1, width=8, command=self.submit)
        submit.pack(side='right')
        cancel = Tkinter.Button(self.frame5, text='Cancel', height=1, width=8, command=self.cancel)
        cancel.pack(side='right')
        self.frame5.pack(padx=40, pady=(5, 30))

        # Add GUI padding

    def cancel(self):
        """Exit the GUI"""
        print('User has closed the app')
        self.master.destroy()

    def submit(self):
        """
        Do something with the data submitted

        You can do...well, anything you want here.

        I use the gathered data to set the computer's name to conform with
        our naming convention and submit the asset tag and end user's username
        to the JSS.
        """
        print('User has submitted')


        # Splitting each character of the input with split(), then re-joining
        # with ''.join() strips all whitespace as opposed to strip() which
        # just cleans the head and tail

        i_computer = ''.join(self.input_assigned_computer.get().split())


        # Assemble hostname
        hostname = "cpu{}".format(i_computer)

        print "Hostname: {}".format(hostname)

        # Rename the computer
        cmd = [JAMF, 'setComputerName', '-name', hostname]
        rename = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        (out, err) = rename.communicate()
        if rename.returncode == 0:
            print "Set computer name to {}".format(hostname)
        else:
            print "Rename failed!"
            sys.exit(1)

        # Submit new inventory
        cmd = [JAMF, 'recon']
        inventory = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        (out, err) = inventory.communicate()
        if inventory.returncode == 0:
            print "Submitted inventory to JSS"
        else:
            print "Inventory update failed!"
            sys.exit(1)

        self.master.destroy()


def main():
    # Prevent the Python app icon from appearing in the Dock
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info['CFBundleIconFile'] = u'PythonApplet.icns'
    info['LSUIElement'] = True

    root = Tkinter.Tk()
    app = App(root)
    # Have the GUI appear on top of all other windows
    AppKit.NSApplication.sharedApplication().activateIgnoringOtherApps_(True)
    rdata = app.master.mainloop()

    sys.exit(0)

if __name__ == '__main__':
    main()
