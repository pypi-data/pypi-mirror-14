# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2016, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
def helpsub(pattern, replacement):
  """Set docstring = re.sub(pattern, replacement, original_docstring)."""
  assert pattern
  assert replacement is not None
  def _helpsub(fn):
    assert fn.__doc__
    fn.__doc__ = re.sub(pattern, replacement, fn.__doc__)
    return fn
  return _helpsub
