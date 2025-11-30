from typing import cast, override

from PySide6.QtCore import Qt, QEvent, QObject, QUrl, Signal, Slot
from PySide6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent, QShortcut
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget

from ui_player_window import Ui_PlayerWindow

from annotations import Annotations

class PlayerWindow(QWidget):
  playerQuit = Signal()

  class _PlayerControllings(QObject):
    toggleFullscreen = Signal()
    playOrPause = Signal()
    quitRequest = Signal()

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
      match event.type():
        case QEvent.Type.MouseButtonPress:
          casted = cast(QMouseEvent, event)

          match casted.button():
            case Qt.MouseButton.RightButton:
              self.playOrPause.emit()
              return True

        case QEvent.Type.KeyPress:
          casted = cast(QKeyEvent, event)

          if casted.modifiers() == Qt.KeyboardModifier.NoModifier:
            match casted.key():
              case Qt.Key.Key_F:
                self.toggleFullscreen.emit()
                return True

              case Qt.Key.Key_Q:
                self.quitRequest.emit()
                return True

      return QObject.eventFilter(self, watched, event)

  # TODO: allowing changing these so instance can
  #       be reused thus reducing webview load-time?
  def __init__(self, annotations: Annotations, vid_url: QUrl):
    QWidget.__init__(self)

    self.__ui = Ui_PlayerWindow()
    self.__ui.setupUi(self)

    self.__ao = QAudioOutput()
    self.__mp = QMediaPlayer(source=vid_url, audioOutput=self.__ao, videoOutput=self.__ui.vidWidget)
    # TODO: handle errors

    self.__ctrls = self._PlayerControllings()
    self.__ctrls.toggleFullscreen.connect(self.__do_toggle_fullscreen)
    self.__ctrls.playOrPause.connect(self.__do_play_or_pause)
    self.__ctrls.quitRequest.connect(self.__do_quit)
    self.__ui.vidWidget.installEventFilter(self.__ctrls)

    self.__side_bar_toggle = QShortcut(Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_B, self)
    self.__side_bar_toggle.activated.connect(self.__do_toggle_side_bar)

  @override
  def closeEvent(self, event: QCloseEvent):
    if self.__mp.isPlaying():
      self.__mp.stop()

    self.playerQuit.emit()

    QWidget.closeEvent(self, event)

  @Slot()
  def __do_toggle_fullscreen(self):
    if self.isFullScreen():
      self.showNormal()
    else:
      self.showFullScreen()

  @Slot()
  def __do_toggle_side_bar(self):
    if self.__ui.webView.isVisible():
      self.__ui.webView.setVisible(False)
      self.__ui.vidWidget.setFocus()
    else:
      self.__ui.webView.setVisible(True)

  @Slot()
  def __do_play_or_pause(self):
    if self.__mp.isPlaying():
      self.__mp.pause()
    else:
      self.__mp.play()

  @Slot()
  def __do_quit(self):
    self.close()
