#!/usr/bin/env python

from sys import exit, stderr, version_info

if version_info < (3, 12):
  print('Python too old', file=stderr)
  exit(1)

from re import match

from PySide6.QtCore import qVersion
from PySide6.QtWidgets import QApplication

from loader_dlg import LoaderDialog

def _assert_qt_ver():
  vs = qVersion()
  m = match(r'(\d+)\.(\d+)\.\d+', vs)
  if m is None:
    print('Cannot determine Qt version', file=stderr)
    exit(1)

  vt = tuple(map(int, m.groups()))
  if vt < (6, 5):
    print('Update your Qt installation', file=stderr)
    exit(1)

def _main():
  _assert_qt_ver()

  app = QApplication([])

  dlg = LoaderDialog()
  dlg.show()

  app.exec()

_main()
