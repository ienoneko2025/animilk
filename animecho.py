import PySide6.QtWidgets

import xlib_binding
import workspace

def _main():
  # recommended by LibVLC documentation
  xlib_binding.enable_threads()

  app = PySide6.QtWidgets.QApplication(
    [
      './this.program',

      # LibVLC 3.0.x still doesn't support Wayland surface
      '-platform', 'xcb',
    ],
  )

  app.setApplicationName('animecho')

  ws = workspace.Workspace()
  ws.show()

  app.exec()

_main()
