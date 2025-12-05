import re

_TIME_STR_PATTERN = re.compile(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})')

class TimeParseError(ValueError):
  pass

def parse_time_str_to_ms(s: str) -> int:
  m = _TIME_STR_PATTERN.fullmatch(s)
  if m is None:
    raise TimeParseError(f'Malformed time string {s!r}')

  hrs, mins, secs, ms = map(int, m.groups())

  if hrs > 23 or mins > 59 or secs > 59:
    raise TimeParseError(f'Invalid time string {s!r}')

  mins += hrs * 60
  secs += mins * 60
  ms += secs * 1000

  return ms

def format_time_str_from_ms(ms: int) -> str:
  assert ms >= 0

  secs, ms = divmod(ms, 1000)
  mins, secs = divmod(secs, 60)
  hrs, mins = divmod(mins, 60)

  assert hrs <= 23

  return f'{hrs:02}:{mins:02}:{secs:02}.{ms:03}'
