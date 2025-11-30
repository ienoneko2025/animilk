#!/bin/sh

set -o pipefail
set -e

if [ $# -ne 0 ]; then
  echo "Usage: $0" >&2
  exit 1
fi

export PATH="/usr/lib/qt6:${PATH}"

if ! uic -v 2>/dev/null | grep -E -q '^uic +6\.[0-9]+\.[0-9]+$'; then
  echo 'Cannot find Qt 6 tools' >&2
  exit 1
fi

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
