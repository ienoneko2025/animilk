from typing import cast, override

from PySide6.QtCore import Qt, QEvent, QObject, QUrl, Signal, Slot
from PySide6.QtGui import QCloseEvent, QMouseEvent
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWebEngineCore import QWebEngineUrlScheme
from PySide6.QtWidgets import QMainWindow, QMessageBox

from ui_player_window import Ui_PlayerWindow

from annotations import Annotations

def _setup_qrc_for_webview():
  scheme = QWebEngineUrlScheme('qrc'.encode())
  scheme.setFlags(QWebEngineUrlScheme.Flag.SecureScheme | QWebEngineUrlScheme.Flag.ViewSourceAllowed | QWebEngineUrlScheme.Flag.FetchApiAllowed)
  QWebEngineUrlScheme.registerScheme(scheme)

class PlayerWindow(QMainWindow):
  _setup_qrc_for_webview()

  playerQuit = Signal()

  class _PlayerMouseControls(QObject):
    toggleFullscreen = Signal()
    playOrPause = Signal()

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
      match event.type():
        case QEvent.Type.MouseButtonDblClick:
          casted = cast(QMouseEvent, event)

          match casted.button():
            case Qt.MouseButton.LeftButton:
              self.toggleFullscreen.emit()
              return True

        case QEvent.Type.MouseButtonPress:
          casted = cast(QMouseEvent, event)

          match casted.button():
            case Qt.MouseButton.RightButton:
              self.playOrPause.emit()
              return True

      return QObject.eventFilter(self, watched, event)

  # TODO: allowing changing these so instance can
  #       be reused thus reducing webview load-time?
  def __init__(self, annotations: Annotations, vid_url: QUrl):
    QMainWindow.__init__(self)

    self.__ui = Ui_PlayerWindow()
    self.__ui.setupUi(self)

    self.__ao = QAudioOutput()
    self.__mp = QMediaPlayer(source=vid_url, audioOutput=self.__ao, videoOutput=self.__ui.vidWidget)
    self.__mp.errorOccurred.connect(self.__do_show_mp_err)

    self.__mouse_ctrls = self._PlayerMouseControls()
    self.__mouse_ctrls.toggleFullscreen.connect(self.__do_toggle_fullscreen)
    self.__mouse_ctrls.playOrPause.connect(self.__do_play_or_pause)
    self.__ui.vidWidget.installEventFilter(self.__mouse_ctrls)

    self.__ui.actionQuit.triggered.connect(self.__do_quit)
    self.__ui.actionPlayPause.triggered.connect(self.__do_play_or_pause)
    self.__ui.actionFullscreen.triggered.connect(self.__do_toggle_fullscreen)
    self.__ui.actionSideBar.triggered.connect(self.__do_toggle_side_bar)

    self.__ui.vidWidget.setFocus()

  @override
  def closeEvent(self, event: QCloseEvent):
    if self.__mp.isPlaying():
      self.__mp.stop()

    self.playerQuit.emit()

    QMainWindow.closeEvent(self, event)

  @override
  def changeEvent(self, event: QEvent):
    match event.type():
      case QEvent.Type.WindowStateChange:
        self.__ui.actionFullscreen.setChecked(bool(self.windowState() & Qt.WindowState.WindowFullScreen))

  @Slot(QMediaPlayer.Error, str)
  def __do_show_mp_err(self, err: QMediaPlayer.Error, strerror: str):
    QMessageBox.warning(self, 'An error occurred', strerror)

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
