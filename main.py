import ctypes
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from window_dialogs.hwid import HwidDialog
from window_dialogs.loading import LoadingDialog

from check_hwid import check_hwid, get_hwid, get_hdsn

APP_ICON = r'icons/vk/ic.ico'

if __name__ == '__main__':
    try:
        if check_hwid():
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('main')
            app = QApplication(sys.argv)
            app.setQuitOnLastWindowClosed(True)
            app_icon = QIcon(APP_ICON)
            app.setWindowIcon(app_icon)
            window = LoadingDialog()
            sys.exit(app.exec())
        else:
            app = QApplication([])
            error_dialog = HwidDialog()
            error_dialog.set_text(f'HWID:')
            error_dialog.set_hwid(get_hwid() + '-' + get_hdsn())
            error_dialog.show()
            app.exec_()
    except Exception as e:
        raise e
