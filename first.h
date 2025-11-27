#ifndef ANIMECHO_FIRST_H
#define ANIMECHO_FIRST_H

#include <qwidget.h>

class QHBoxLayout;
class QLabel;
class QListWidget;
class QPushButton;
class QVBoxLayout;

class scr_first
: public QWidget
{
  Q_OBJECT

public:
  scr_first ();
  ~scr_first ();

private slots:

private:
  QVBoxLayout *m_layout;

  struct
  {
    QWidget *base;
    QHBoxLayout *layout;

    QPushButton *new_btn;
    QPushButton *open_btn;
  } m_btn_bar;

  QLabel *m_recent_lbl;
  QListWidget *m_recent_lst;
};

#endif
