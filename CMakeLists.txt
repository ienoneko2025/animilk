cmake_minimum_required(VERSION 4.2.0)
project(Animecho LANGUAGES CXX)

if (NOT EMSCRIPTEN)
  message(WARNING "Expecting Wasm target")
endif()

# required by Qt 6
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)

# N.B. specify target so header deps will work
qt_wrap_cpp(QT_MOC_SRCS
  dialogue_view.h

  TARGET dialogue_view)

add_executable(dialogue_view
  ${QT_MOC_SRCS}
  dialogue_view.cc)
target_link_libraries(dialogue_view PRIVATE
  Qt6::Widgets)
# let Qt fixup the link deps
qt_finalize_target(dialogue_view)
