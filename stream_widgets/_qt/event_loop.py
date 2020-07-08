import os
import sys
from contextlib import contextmanager
from os.path import dirname, join

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QApplication, QSplashScreen


_config = {'logopath': None, 'app_name': ''}


def set_logo(logopath):
    _config['logopath'] = logopath


def set_app_name(app_name):
    _config['app_name'] = app_name


def get_app_name():
    return _config['app_name']


@contextmanager
def gui_qt(*, startup_logo=False):
    """Start a Qt event loop in which to run the application.

    Parameters
    ----------
    startup_logo : bool
        Show a splash screen with a logo during startup.

    Notes
    -----
    This context manager is not needed if running the app within an interactive
    IPython session. In this case, use the ``%gui qt`` magic command, or start
    IPython with the Qt GUI event loop enabled by default by using
    ``ipython --gui=qt``.
    """
    splash_widget = None
    app = QApplication.instance()
    if not app:
        # automatically determine monitor DPI.
        # Note: this MUST be set before the QApplication is instantiated
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        # if this is the first time the Qt app is being instantiated, we set
        # the name, so that we know whether to raise_ in Window.show()
        app = QApplication([_config['app_name']])
        if startup_logo and _config['logopath'] is not None:
            logopath = _config['logopath']
            pm = QPixmap(logopath).scaled(
                360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            splash_widget = QSplashScreen(pm)
            splash_widget.show()
            app._splash_widget = splash_widget
    else:
        app._existed = True
    yield app
    # if the application already existed before this function was called,
    # there's no need to start it again.  By avoiding unnecessary calls to
    # ``app.exec_``, we avoid blocking.
    if app.applicationName() == _config['app_name']:
        if splash_widget and startup_logo:
            splash_widget.close()
        app.exec_()
