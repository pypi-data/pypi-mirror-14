#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Martin Raspaud

# Author(s):

#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
"""


import logging
from datetime import datetime
from trollcast.server import serve
import sys

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logging.getLogger("").setLevel(logging.DEBUG)
    ch1 = logging.StreamHandler()
    ch1.setLevel(logging.DEBUG)
    logger = logging.getLogger("trollcast")
    logger.addHandler(ch1)
    logger.debug("aiaiai")
    serve(sys.argv[1])
