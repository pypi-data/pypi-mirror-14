# -*- coding: utf-8 -*-
#
# Copyright 2015 Simone Campagna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Project version:

>>> print(VERSION_INFO)
VersionInfo(major=0, minor=1, patch=0)
>>> print(VERSION)
0.1.0
>>>

"""

import collections


__author__ = "Simone Campagna"
__copyright__ = 'Copyright (c) 2016 Simone Campagna'
__license__ = 'Apache License Version 2.0'

__all__ = (
    'VersionInfo',
    'VERSION_INFO',
    'VERSION',
)


VersionInfo = collections.namedtuple('VersionInfo', (
    'major',
    'minor',
    'patch',
))

VERSION_INFO = VersionInfo(major=0, minor=1, patch=0)

VERSION = '.'.join(str(v) for v in VERSION_INFO)

