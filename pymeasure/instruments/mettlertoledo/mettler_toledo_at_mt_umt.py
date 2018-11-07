#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2017 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import (truncated_range,
                                              strict_discrete_set,
                                              joined_validators)

import time

class MettlerToledoAT20(Instrument):
    """ TODO """

    door_state = Instrument.control(
        "WI ?",
        "WI %s",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1)
    )

    door_auto_close = Instrument.control(
        "AD ?",
        "AD %s",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1)
    )

    unit = Instrument.setting(
        "U %s",
        """ TODO """,
        validator=strict_discrete_set,
        values=()
    )

    def __init__(self, adapter, **kwargs):
        super(MettlerToledoAT, self).__init__(adapter,
        "Mettler Toledo AT/MT/UMT Balance", include_scpi=False, **kwargs
        )

    @property
    def tare(self):
        """ TODO """
        self.write('T')

    @property
    def id(self):
        """ TODO """
        self.write("ID")
        _ = self.read().strip()
        _ = _ + ', ' + self.read().strip()
        _ = _ + ', ' + self.read().strip()
        return(_)
