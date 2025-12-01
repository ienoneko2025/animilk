from sys import exit, stderr, version_info

if version_info < (3, 12):
  print('Python too old', file=stderr)
  exit(1)

from PySide6.QtWidgets import QApplication

from loader_dlg import LoaderDialog

def _main():
  app = QApplication([])

  dlg = LoaderDialog()
  dlg.show()

  app.exec()

_main()
