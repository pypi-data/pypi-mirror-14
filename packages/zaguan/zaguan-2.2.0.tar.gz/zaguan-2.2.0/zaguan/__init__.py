from __future__ import absolute_import
from __future__ import print_function
try:
    import gtk
    import gobject
    from gtk import gdk
    timeout_add = gobject.timeout_add
    WINDOW_TOPLEVEL = gtk.WINDOW_TOPLEVEL
    WIN_POS_CENTER_ALWAYS = gtk.WIN_POS_CENTER_ALWAYS
except (ImportError, AttributeError):
    print("GTK not installed")
    try:
        from gi.repository import GLib, Gtk as gtk, Gdk as gdk
        timeout_add = GLib.timeout_add
        WINDOW_TOPLEVEL = gtk.WindowType.TOPLEVEL
        WIN_POS_CENTER_ALWAYS = gtk.WindowPosition.CENTER_ALWAYS
    except ImportError:
        print("PyGi not installed")
try:
    import sys
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    print("QT not installed")


from time import sleep

from zaguan.controller import WebContainerController


class Zaguan(object):
    def __init__(self, uri, controller=None):
        if controller is None:
            controller = WebContainerController()
        self.controller = controller
        self.uri = uri
        self.on_close = None
        self.exiting = False

    def run(self, settings=None, window=None, debug=False,
            qt=False, on_close=None, cef=False):
        self.on_close = on_close

        if qt:
            self.run_qt(settings, window, debug)
        elif cef:
            self.run_cef(settings, window, debug)
        else:
            self.run_gtk(settings, window, debug)

    def run_cef(self, settings=None, window=None, debug=False):
        gdk.threads_init()

        if window is None:
            self.window = gtk.Window(WINDOW_TOPLEVEL)
            self.window.set_position(WIN_POS_CENTER_ALWAYS)
            self.window.set_size_request(width=800, height=600)
            self.window.realize()
        else:
            self.window = window

        self.window.set_border_width(0)

        self.controller.get_cef_browser(self.uri, self.window)
        sleep(1)
        self.window.show_all()
        self.window.show()
        timeout_add(10, self.OnTimer)

        gtk.main()
        cefpython.Shutdown()

    def OnTimer(self):
        if self.exiting:
            return False
        from cefpython3 import cefpython
        cefpython.MessageLoopWork()
        return True

    def OnExit(self, widget, data=None):
        self.exiting = True
        gtk.main_quit()

    def run_gtk(self, settings=None, window=None, debug=False):
        gdk.threads_init()

        if window is None:
            self.window = gtk.Window(WINDOW_TOPLEVEL)
            self.window.set_position(WIN_POS_CENTER_ALWAYS)
        else:
            self.window = window

        browser = self.controller.get_browser(self.uri, debug=debug,
                                              settings=settings)
        self.window.connect("delete-event", self.quit)
        self.window.set_border_width(0)
        self.window.add(browser)

        sleep(1)
        self.window.show_all()
        self.window.show()
        gtk.main()

    def run_qt(self, settings, window, debug):
        if window is None:
            self.window = QApplication(sys.argv)
        else:
            self.window = window

        browser = self.controller.get_browser(self.uri, debug=debug,
                                              settings=settings, qt=True)
        browser.show()
        sys.exit(self.window.exec_())

    def quit(self, widget, event):
        if self.on_close is not None:
            self.on_close(widget, event)
