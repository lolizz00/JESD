
import sys


from  ConsoleApp import ConsoleApp

# --- Нормальный вывод ошибок
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))


    print('\n\n-------------------------------------------- \n')
    print(text)
    print('\n----------------------------------------------\n')


import sys
sys.excepthook = log_uncaught_exceptions

def start():

    if len(sys.argv) == 1:
        from MainForm import MW
        from PyQt5 import QtWidgets

        app = QtWidgets.QApplication(sys.argv)
        mw = MW()
        sys.exit(app.exec_())
    else:
        app = ConsoleApp()
        ret = app.handleArgs(sys.argv[1:])
        print(ret)
        sys.exit(ret)


if __name__ == '__main__':
    start()