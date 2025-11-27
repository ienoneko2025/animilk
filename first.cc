#include <qboxlayout.h>
#include <qlabel.h>
#include <qlistwidget.h>
#include <qpushbutton.h>

#include "first.h"

scr_first::scr_first ()
: QWidget(nullptr)
{
  m_layout = new QVBoxLayout();
  setLayout(m_layout);

  m_layout->addWidget(m_btn_bar.base = new QWidget());
  m_btn_bar.base->setLayout(m_btn_bar.layout = new QHBoxLayout());

  m_btn_bar.layout->addWidget(m_btn_bar.new_btn = new QPushButton("&New"));
  m_btn_bar.layout->addWidget(m_btn_bar.open_btn = new QPushButton("&Open"));

  m_recent_lbl = new QLabel("Recent");
  m_layout->addWidget(m_recent_lbl);

  m_recent_lst = new QListWidget();
  m_layout->addWidget(m_recent_lst);
}

scr_first::~scr_first ()
{
}
