#!/bin/sh

set -o pipefail
set -e

if [ $# -ne 0 ]; then
  echo "Usage: $0" >&2
  exit 1
fi

export PATH="/usr/lib/qt6:${PATH}"

dropout_qt_tools=('uic' 'rcc')

for dropout_qt_tool in "${dropout_qt_tools[@]}"; do
  if ! $dropout_qt_tool -v 2>/dev/null | grep -E -q "^${dropout_qt_tool} +6\\.[0-9]+\\.[0-9]+\$"; then
    echo 'Cannot find Qt 6 tools' >&2
    exit 1
  fi
done

dropout_forms=('player_window'
               'loader_dlg')

for dropout_form in "${dropout_forms[@]}"; do
  dropout_out="ui_${dropout_form}.py"
  dropout_src="${dropout_form}.ui"

  if [ -e "$dropout_out" -a "$dropout_src" -ot "$dropout_out" -a "$dropout_out" -nt "$(which uic)" -a "$dropout_out" -nt "$0" ]; then
    # already up-to-date
    continue
  fi

  (set -x && uic --no-autoconnection -g python -o "$dropout_out" "$dropout_src")
done

dropout_static_web_files=('dialogue_view.wasm'
                          'dialogue_view.js'
                          'qtloader.js'
                          'dialogue_view.html'
                          'qtlogo.svg')

function dropout_gen_webpage_res ()
{
  (set -x && rcc -g python -o webpage_rc.py webpage.qrc)
}

if [ ! -e webpage_rc.py -o "$(which rcc)" -nt webpage_rc.py -o "$0" -nt webpage_rc.py -o webpage.qrc -nt webpage_rc.py ]; then
  dropout_gen_webpage_res
else
  for dropout_static_web_file in "${dropout_static_web_files[@]}"; do
    if [ "$dropout_static_web_file" -nt webpage_rc.py ]; then
      dropout_gen_webpage_res
      break
    fi
  done
fi
