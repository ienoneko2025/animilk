#include <string.h>

#include <qapplication.h>

#include "dialogue_view.h"

DialogueView::DialogueView ()
: QWidget(nullptr)
{
}

int
main ()
{
  int unused_0;
  char unused_1[16];
  QApplication *app;
  DialogueView *view;

  unused_0 = 1;
  strcpy(unused_1, "./this.program");
  app = new QApplication(unused_0, (char *[]){unused_1, nullptr});

  view = new DialogueView();
  view->show();

  app->exec();

  delete view;
  delete app;

  return 0;
}
