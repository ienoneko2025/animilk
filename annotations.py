from typing import Self

class AnnotationParseError(ValueError):
  pass

class Annotations:
  @classmethod
  def load(cls, path: str) -> Self:
    instance = cls()

    with open(path, 'r', encoding='utf-8') as f:
      pass

    return instance

  def save(self, path: str):
    with open(path, 'w', encoding='utf-8') as f:
      pass
