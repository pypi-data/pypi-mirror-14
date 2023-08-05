# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


from json import dumps, loads

from zaguan.container import launch_browser
try:
    from zaguan_inspector import Inspector
    inspector_available = True
except ImportError:
    inspector_available = False


class WebContainerController(object):
    """Base class for the web containers of the controllers."""
    def __init__(self):
        self.processors = []

    def on_navigation_requested(self, elem, view, frame, req, data=None):
        """This is the Callback executed each time  URI inside the webkit
        object is loaded"""
        uri = req.get_uri()
        self.process_uri(uri)

    def process_uri(self, uri):
        """Procces the url on each processor."""
        for processor in self.processors:
            processor(uri)

    def set_screen(self, screen, **kwargs):
        """Sends the change sreen command to the web interface."""
        self.send_command("change_screen", [screen, kwargs])

    def send_command(self, command, data=None):
        """Inyects the JS in the browser for the givven command."""
        json_data = dumps(data).replace("\\\"", "\\\'")
        self.send_function("run_op('%s', '%s')" % (command, json_data))

    def get_browser(self, uri, settings=None, debug=False, qt=False):
        """Gets the browser objects and prpare it to bo able to be used in it's
        context.
        """
        if settings is None:
            settings = []

        if debug and inspector_available:
            settings.append(('enable-default-context-menu', True))
            settings.append(('enable-developer-extras', True))

        browser, web_send = launch_browser(uri, echo=debug,
                                           user_settings=settings, qt=qt)
        if debug and inspector_available:
            try:
                inspector = browser.get_web_inspector()
            except AttributeError:
                inspector = browser.get_inspector()

            self.inspector = Inspector(inspector)

        self.send_function = web_send
        if not qt:
            browser.connect("resource-request-starting",
                            self.on_navigation_requested)
        return browser

    def get_cef_browser(self, uri, window, debug=False):
        import re
        from cefpython3 import cefpython

        settings = {
            "debug": False, #debug, # cefpython debug messages in console and in log_file
            "log_severity": cefpython.LOGSEVERITY_INFO, # LOGSEVERITY_VERBOSE
            "release_dcheck_enabled": True, # Enable only when debugging
            # This directories must be set on Linux
            "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
            "resources_dir_path": cefpython.GetModuleDirectory(),
            "browser_subprocess_path": "%s/%s" % (
                cefpython.GetModuleDirectory(), "subprocess"),
        }

        cefpython.Initialize(settings)

        m = re.search("GtkWindow at 0x(\w+)", str(window))
        hexID = m.group(1)
        windowID = int(hexID, 16)

        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsChild(windowID)
        browser = cefpython.CreateBrowserSync(
            windowInfo,
            browserSettings={
                "web_security_disabled": True,
            },
            navigateUrl=uri)
        self.cef_window = browser

        jsBindings = cefpython.JavascriptBindings(
            bindToFrames=False, bindToPopups=True)

        jsBindings.SetFunction("zaguan", self.process_uri)
        browser.SetJavascriptBindings(jsBindings)

        self.send_function = browser.GetMainFrame().ExecuteJavascript

    def add_processor(self, url_word, instance=None):
        def _inner(uri):
            scheme, path = uri.split(':', 1)
            if scheme == "http":
                parts = path.split("/")[2:]
                if parts[0] == url_word:
                    remain = parts[1]
                elif parts[1] == url_word:
                    remain = parts[2]
                else:
                    remain = None
                if remain is not None:
                    try:
                        action, data = remain.split("?")
                    except ValueError:
                        action = remain
                        data = "null"

                    data = loads(unquote(data))
                    # search the action at the 'action controller' instance
                    # argument. if we dont find the action, we try to get it
                    # from the controller itself.
                    method = getattr(instance, action, None)
                    if method is None:
                        method = getattr(self, action, None)

                    if not method:
                        raise NotImplementedError(action)
                    return method(data)

        self.processors.append(_inner)
