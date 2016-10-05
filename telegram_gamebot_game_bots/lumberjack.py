# Use:
# watch xdotool getmouselocation
# To get the locations for the buttons and branches.

# TODO: Start automatically:
# If both left and right are blue, hit any twice.

import time
import sys

import pyautogui
import gtk.gdk


import Queue
class ExitWhenPressed:
    class CleanExit:
            pass

    def __init__(self):
        from pyzmo import EventHandler
        from evdev import ecodes

        import threading

        def pollEvents(q):
            app = EventHandler('name')
            @app.key(ecodes.KEY_B, states=['down', 'hold', 'up'])
            def back(events):
                q.put(self.CleanExit)
                sys.exit()

            EventHandler.poll(app,'/dev/input/by-id/usb-Logitech_USB_Keyboard-event-kbd')


        self.q = Queue.Queue()
        t = threading.Thread(target=pollEvents, args=(self.q,))
        t.daemon = True
        t.start()

    def check(self):
        try:
            if self.q.get_nowait() == self.CleanExit:
                return True
        except Queue.Empty:
            return False


def pixel_at(x,y):
    rw = gtk.gdk.get_default_root_window()
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
    pixbuf = pixbuf.get_from_drawable(rw, rw.get_colormap(), x, y, 0, 0, 1, 1)
    return tuple(pixbuf.pixel_array[0, 0])

leftX = 900
rightX = 1080
leftY = rightY = 950
sleepTime = 0.005

treePixel = (175, 221, 127)
skyPixel = (211, 247, 255)

exitP = ExitWhenPressed()

while(True):
    if exitP.check():
        sys.exit()

    time.sleep(sleepTime)
    pixels = (pixel_at(909,628), pixel_at(1076,628))
    if pixels[0] == treePixel and pixels[1] == skyPixel:
        pyautogui.click(rightX, rightY)
        time.sleep(sleepTime)
        pyautogui.click(rightX, rightY)
    elif pixels[1] == treePixel and pixels[0] == skyPixel:
        pyautogui.click(leftX, leftY)
        time.sleep(sleepTime)
        pyautogui.click(leftX, leftY)
    else:
        print "There is something wrong with the pixels. Waiting."
        time.sleep(sleepTime)
