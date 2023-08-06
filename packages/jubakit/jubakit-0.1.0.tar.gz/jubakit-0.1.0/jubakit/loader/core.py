# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from ..base import BaseLoader
from ..compat import *

class LineBasedStreamLoader(BaseLoader):
  """
  Loader to process line-oriented text stream.
  You can override `preprocess` method to separate the row into fields.
  """

  def __init__(self, f, close=False):
    self._f = f
    self._close = close
    self._lines = 0

  def __iter__(self):
    for line in self._f:
      yield self.preprocess({str(self._lines): line})
      self._lines += 1
    if self._close:
      self._f.close()

  def preprocess(self, ent):
    return {'line': list(ent.values())[0]}

class LineBasedFileLoader(LineBasedStreamLoader):
  """
  Loader to process line-oriented text file.
  """

  def __init__(self, filename, *args, **kwargs):
    f = open(filename, *args, **kwargs)
    super(LineBasedFileLoader, self).__init__(f, True)
