from PySide6.QtWidgets import QApplication

from loader_dlg import LoaderDialog

def _main():
  app = QApplication([])

  dlg = LoaderDialog()
  dlg.show()

  app.exec()

_main()
