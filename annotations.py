from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Self, Sequence, TextIO, override

from time_serialization import TimeParseError, format_time_str_from_ms, parse_time_str_to_ms

class AnnotationParseError(ValueError):
  pass

class TooManyOrFewFields(AnnotationParseError):
  pass

@dataclass
class Event(ABC):
  time_ms: int

  @classmethod
  @abstractmethod
  def get_tag_name(cls) -> str:
    pass

  @classmethod
  @abstractmethod
  def parse(cls, ev_time: int, fields: Sequence[str]) -> Self:
    pass

  @abstractmethod
  def fmt(self) -> tuple[str]:
    pass

@dataclass
class NullEvent(Event):
  @classmethod
  @override
  def get_tag_name(cls) -> str:
    raise AssertionError

  @classmethod
  @override
  def parse(cls, ev_time: int, fields: Sequence[str]) -> Self:
    raise AssertionError

  @override
  def fmt(self) -> tuple[str]:
    raise AssertionError

@dataclass
class DialogueEvent(Event):
  @classmethod
  @override
  def get_tag_name(cls) -> str:
    return 'dialogue'

  @classmethod
  @override
  def parse(cls, ev_time: int, fields: Sequence[str]) -> Self:
    if len(fields) != 0:
      raise TooManyOrFewFields

    return cls(ev_time)

  @override
  def fmt(self) -> tuple[str]:
    return ()

@dataclass
class EventList:
  inner: Event
  ll_prev: Optional[Self] = None
  ll_next: Optional[Self] = None

class Annotations:
  class _Parser:
    def __init__(self, f: TextIO):
      self.__f = f
      self.__instance = Annotations()

      self.__lno = 0
      self.__sect_line_cb = None
      self.__known_sects: set[str] = set()

      self.__ev_tail = self.__instance.get_events()

      try:
        first = self.__next_non_blank_line()
      except StopIteration:
        return

      if not first.startswith('-'):
        raise self.__at_line('Expecting section label')

      self.__do_sect_lbl_line(first)

    def __next_non_blank_line(self):
      line = ''
      while line == '':
        line = next(self.__f).removesuffix('\n')
        self.__lno += 1
      return line

    def __at_line(self, msg: str) -> Exception:
      return AnnotationParseError(f'Line #{self.__lno}: {msg}')

    def __add_event(self, ev: Event):
      if ev.time_ms < self.__ev_tail.inner.time_ms:
        raise self.__at_line('Event time jumping back')

      item = EventList(ev, self.__ev_tail)
      self.__ev_tail.ll_next = item
      self.__ev_tail = item

    def __parse_add_event(self, event_type: type[Event], ev_time: int, extra: Sequence[str]):
      try:
        ev = event_type.parse(ev_time, extra)
      except AnnotationParseError as exc:
        raise self.__at_line('Failed to parse event') from exc
      else:
        self.__add_event(ev)

    def __do_event_line(self, line: str):
      fields = line.split('\t')
      if len(fields) < 2:
        raise self.__at_line('Too few event fields')

      tag, ts, *extra = fields
      try:
        ev_time = parse_time_str_to_ms(ts)
      except TimeParseError as exc:
        raise self.__at_line('Cannot parse event time') from exc

      match tag:
        case 'dialogue':
          self.__parse_add_event(DialogueEvent, ev_time, extra)
        case _:
          raise self.__at_line(f'Unknown event {tag!r}')

    def __do_sect_lbl_line(self, line: str):
      sect_name = line[1:]
      if sect_name in self.__known_sects:
        raise self.__at_line(f'Duplicate section {sect_name!r}')

      match sect_name:
        case 'events':
          self.__sect_line_cb = self.__do_event_line
        case _:
          raise self.__at_line(f'Unknown section {sect_name!r}')

      self.__known_sects.add(sect_name)

    def __do_sect_line(self, line: str):
      assert self.__sect_line_cb is not None
      self.__sect_line_cb(line)

    def do_line(self):
      line = self.__next_non_blank_line()
      if line.startswith('-'):
        self.__do_sect_lbl_line(line)
      else:
        self.__do_sect_line(line)

    def get_instance(self) -> Annotations:
      return self.__instance

  def __init__(self):
    self.__events = EventList(NullEvent(0))

  def get_events(self) -> EventList:
    return self.__events

  @classmethod
  def load(cls, path: str) -> Self:
    with open(path, 'r', encoding='utf-8') as f:
      parser = cls._Parser(f)

      while True:
        try:
          parser.do_line()
        except StopIteration:
          break

      return parser.get_instance()

  def save(self, path: str):
    with open(path, 'w', encoding='utf-8') as f:
      f.write('-events\n')

      ev = self.__events
      while ev is not None:
        if isinstance(ev.inner, NullEvent):
          pass
        else:
          tag = ev.inner.get_tag_name()
          ts = format_time_str_from_ms(ev.inner.time_ms)
          fields = ev.inner.fmt()
          f.write('\t'.join((tag, ts, *fields)))
          f.write('\n')

        ev = ev.ll_next
