from os.path import exists
from traceback import format_exc, print_exc
from typing import Optional

from PySide6.QtCore import Slot, QUrl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from ui_loader_dlg import Ui_LoaderDialog

from annotations import Annotations, AnnotationParseError
from player_window import PlayerWindow
from user_preferences import UserPreferences

class LoaderDialog(QWidget):
  def __init__(self):
    QWidget.__init__(self)

    self.__ui = Ui_LoaderDialog()
    self.__ui.setupUi(self)

    self.__user_file_path: Optional[str] = None
    self.__user_pref: Optional[UserPreferences] = None

    self.__ui.btnPickAnnotationFile.clicked.connect(self.__do_pick_annotation_file)
    self.__ui.btnPickVidFile.clicked.connect(self.__do_pick_vid_file)
    self.__ui.btnOK.clicked.connect(self.__do_jump_to_player)

  def __set_vid_file_path(self, path: str):
    self.__ui.fieldVidFileUrl.setText(path)
    self.__ui.btnOK.setEnabled(True)

  @Slot()
  def __do_pick_annotation_file(self):
    path = QFileDialog.getOpenFileName(self, filter='Annotation Files (*.annotations)')
    if path == '':
      return

    self.__ui.btnOK.setEnabled(False)

    self.__user_pref = None
    self.__user_file_path = f'{path}.user'

    self.__ui.fieldVidFileUrl.clear()
    self.__ui.fieldAnnotationFileUrl.setText(path)
    self.__ui.fieldVidFileUrl.setEnabled(True)

    if exists(self.__user_file_path):
      try:
        self.__user_pref = UserPreferences.load(self.__user_file_path)
      except OSError:
        print_exc()
      else:
        if self.__user_pref.last_vid_path is not None and exists(self.__user_pref.last_vid_path):
          self.__set_vid_file_path(self.__user_pref.last_vid_path)

    self.__ui.btnPickVidFile.setEnabled(True)

  @Slot()
  def __do_pick_vid_file(self):
    path = QFileDialog.getOpenFileName(self, filter='Video Files (*.mp4 *.mkv)')
    if path != '':
      self.__set_vid_file_path(path)

  @Slot()
  def __do_jump_to_player(self):
    try:
      annotations = Annotations.load(self.__ui.fieldAnnotationFileUrl.text())
    except AnnotationParseError:
      QMessageBox.warning(self, 'Invalid annotation file', format_exc())
      return
    except OSError as exc:
      QMessageBox.warning(self, 'Unable to open annotation file', exc.strerror)
      return

    vid_path = self.__ui.fieldVidFileUrl.text()
    vid_url = QUrl.fromLocalFile(vid_path)

    # TODO: show loader window again after player is closed

    player = PlayerWindow(annotations, vid_url)
    player.show()

    pref = self.__user_pref if self.__user_pref is not None else UserPreferences()
    pref.last_vid_path = vid_path

    # XXX: config is always saved even if the video didn't play
    #      e.g. the selected video file is not accessible

    try:
      pref.save(self.__user_file_path)
    except OSError:
      print_exc()

    self.close()
