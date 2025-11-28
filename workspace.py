import typing

import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets

import vlc

import ui_workspace

class Workspace(PySide6.QtWidgets.QWidget):
  _TEST_VID_PATH = '/mnt/mydata/cache/sshfs_mount/_hidden/tr-dl/[Taedium] Tonari no Kyuuketsuki-san - 01-12 [1080p BD][HEVC FLAC]/[Taedium] Tonari no Kyuuketsuki-san - 01 [1080p BD][HEVC FLAC].mkv'

  class _PlayerKeyControls(PySide6.QtCore.QObject):
    toggleFullscreen = PySide6.QtCore.Signal()

    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
      if event.type() == PySide6.QtCore.QEvent.Type.KeyPress:
        if event.modifiers() == PySide6.QtCore.Qt.KeyboardModifier.NoModifier:
          match event.key():
            case PySide6.QtCore.Qt.Key.Key_F:
              self.toggleFullscreen.emit()
              return True

      return PySide6.QtCore.QObject.eventFilter(self, watched, event)

  def __init__(self):
    PySide6.QtWidgets.QWidget.__init__(self)

    self.__ui = ui_workspace.Ui_Workspace()
    self.__ui.setupUi(self)

    self.resize(1600, 900)

    self.__vlc = vlc.Instance(
      '--no-spu',  # disable built-in subtitle support
    )
    self.__mp: typing.Optional[vlc.MediaPlayer] = None

    self.__toggle_side_bar_key = PySide6.QtGui.QShortcut(PySide6.QtCore.Qt.KeyboardModifier.ControlModifier | PySide6.QtCore.Qt.Key.Key_B, self)

    self.__toggle_side_bar_key.activated.connect(self.__do_toggle_side_bar)

    self.__key_filter = self._PlayerKeyControls()
    self.__ui.videoWidget.installEventFilter(self.__key_filter)

    self.__key_filter.toggleFullscreen.connect(self.__do_toggle_fullscreen)

    self.__ui.loadTestVideoButton.clicked.connect(self.__do_load_test_vid)

  @PySide6.QtCore.Slot()
  def __do_toggle_side_bar(self):
    if self.__ui.sideBar.isVisible():
      self.__ui.sideBar.setVisible(False)
      # otherwise somehow, the focus could be still on the now hidden widget
      self.__ui.videoWidget.setFocus()
    else:
      self.__ui.sideBar.setVisible(True)

  @PySide6.QtCore.Slot()
  def __do_toggle_fullscreen(self):
    if self.isFullScreen():
      self.showNormal()
    else:
      self.showFullScreen()

  @PySide6.QtCore.Slot()
  def __do_load_test_vid(self):
    self.__mp = vlc.MediaPlayer(self.__vlc, self._TEST_VID_PATH)
    self.__mp.set_xwindow(self.__ui.videoWidget.winId())
    self.__mp.play()
    self.__ui.videoWidget.setUpdatesEnabled(False)  # fixes flickering during Qt window resize
    self.__ui.loadTestVideoButton.setEnabled(False)
