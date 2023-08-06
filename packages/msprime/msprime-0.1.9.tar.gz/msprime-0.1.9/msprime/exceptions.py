#
# Copyright (C) 2015 Jerome Kelleher <jerome.kelleher@well.ox.ac.uk>
#
# This file is part of msprime.
#
# msprime is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# msprime is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with msprime.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Module defining the exceptions that may be thrown by msprime.
"""
from __future__ import division
from __future__ import print_function


class MsprimeException(Exception):
    """
    Base class for all the exceptions that may be thrown by
    msprime.
    """


class OutOfMemoryError(MsprimeException):
    """
    An out-of-memory condition was encountered. This can happen in two
    ways: (1) a low-level malloc failed because the operating system
    could not allocate any more memory; or (2) msprime would have used
    more memory than the max_memory parameter allows.

    **TODO** document properly.
    """
    def __init__(self):
        msg = "Out of memory. Try increasing the max_memory parameter."
        super(OutOfMemoryError, self).__init__(msg)
