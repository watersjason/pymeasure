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
from pymeasure.instruments.validators import (strict_range,
                                              strict_discrete_set,
                                              truncated_range)

from .buffer import KeithleyBuffer

import numpy as np
import time

class Keithley6514(Instrument):
    """ Implements functions for the Keithley 6514 Systems Electrometer.

        TODO: example code
    """
    # CALCulate
    calculate_format=Instrument.control(
        "CALC:FORM?",
        "CALC:FORM %s",
        """ Select MATH format; values are `linear` or `percent` """,
        validator=strict_discrete_set,
        values={'linear':'MXB','percent':'PERC'},
        map_values=True
    )
    calculate_linear_slope=Instrument.control(
        "CALC:KMAT:MMF?",
        "CALC:KMAT:MMF %g",
        """ Query or set the slope for the linear calculation.""",
        validator=strict_range,
        values=(-9.99999e20,9.99999e20)
    )
    calculate_linear_intercept=Instrument.control(
        "CALC:KMAT:MBF?",
        "CALC:KMAT:MBF %g",
        """ Query or set the intercept for the linear calculation.""",
        validator=strict_range,
        values=(-9.99999e20,9.99999e20)
    )
    calculate_linear_units=Instrument.control(
        "CALC:KMAT:MUN?",
        "CALC:KMAT:MUN %s",
        """ A string parameter for the units of the linear calculation.
            The maximum string length is 3 letters (A-Z)."""
    )
    calculate_percent_reference=Instrument.control(
        "CALC:PERC?",
        "CALC:PERC:REF",
        """ Query or set the math percentage reference value. """,
        validator=strict_range,
        values=(-9.99999e20,9.99999e20)
    )
    calculate_state=Instrument.control(
        "CALC:STAT?",
        "CALC:STAT %i",
        """ Query/set the calculate state. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    calculate_data=Instrument.measurement(
        "CALC:DATA?",
        """ Query and return calculation results from
            all measurements collected since the last trigger. """
    )
    calculate_data_latest=Instrument.measurement(
        "CALC:DATA:LAT?",
        """ Query and return calculation the single latest result from
            the measurements collected since the last trigger. """
    )
    # CALCulate3
    calculate_statistics_format=Instrument.control(
        "CALC3:FORM?",
        "CALC3:FORM %s",
        """ A string parameter for the statistical value returned by the stats
            register.
            Values are: `mean`, `sdev`, `max`, `min` or `peak to peak`. """,
        validator=strict_discrete_set,
        values={'mean':'MEAN',
                'sdev':'SDEV',
                'max':'MAX',
                'min':'MIN',
                'peak to peak':'PKPK'},
        map_values=True
    )
    calculate_statistics_data=Instrument.measurement(
        "CALC3:DATA?",
        "Query and return the value from the statistics register."
    )
    # DISPlay
    display_digits=Instrument.control(
        ":DISP:DIG?",
        ":DISP:DIG %g",
        """An integer parameter for the digits (4 to 7) on the front display""",
        validator=strict_discrete_set,
        values=list(range(4,8,1)),
        cast=int
    )
    display_state=Instrument.control(
        ":DISP:ENAB?",
        ":DISP:ENAB %i",
        """ A boolean parameter for the display state.
        When `True`, the front display is enabled.""",
        validator=strict_range,
        values=(0,1),
        cast=bool
    )
    # FORMat
    # SENSe
    sense_function=Instrument.control(
        ":SENS:FUNC?",
        ":SENS:FUNC %s",
        """ A string parameter for the device sense function:
            DC `voltage`, DC `current`, `resistance`, or `charge`. """,
        validator=strict_discrete_set,
        values={'voltage':'VOLT','current':'CURR',
                'resistance':'RES','charge':'CHAR'},
        map_values=True
    )
    sense_latest=Instrument.measurement(
        ":SENS:DATA:LAT?",
        """ A float parameter that returns the last instrument reading."""
    )
    sense_nplc=Instrument.control(
        ":SENS:VOLT:NPLC?",
        ":SENS:VOLT:NPLC %g",
        """ A float parameter for the number of power line cycles
            used for the measurement integration. This command affects
            all sense functions. """,
        validator=truncated_range,
        values=[i/100 for i in range(1,1001,1)]
    )
    voltage_range=Instrument.control(
        ":SENS:VOLT:RANG:UPP?",
        ":SENS:VOLT:RANG:UPP %i",
        """ An integer parameter for the measurement range. Value in volts.""",
        validator=strict_discrete_set,
        values=list(range(-211,211,1)),
        cast=int
    )
    voltage_range_auto=Instrument.control(
        ":SENS:VOLT:RANG:AUTO?",
        ":SENS:VOLT:RANG:AUTO %i",
        """ A boolean parameter for the enabled
            state of the measurement autorange. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    voltage_range_auto_upper=Instrument.control(
        ":SENS:VOLT:RANG:AUTO:ULIM?",
        ":SENS:VOLT:RANG:AUTO:ULIM %f",
        """ A float parameter for the upper value of the measurement autorange.
            Value in volts. """,
        validator=truncated_range,
        values=(-210,210)
    )
    voltage_range_auto_lower=Instrument.control(
        ":SENS:VOLT:RANG:AUTO:LLIM?",
        ":SENS:VOLT:RANG:AUTO:LLIM %f",
        """ A float parameter for the lower value of the measurement autorange.
            Value in volts. """,
        validator=truncated_range,
        values=(-210,210)
    )
    voltage_guard=Instrument.control(
        ":SENS:VOLT:GUAR?",
        ":SENS:VOLT:GUAR %s",
        """ A boolean parameter for the enabled state of the driven guard. """
    )
    voltage_external_feedback=Instrument.control(
        ":SENS:VOLT:XFE?",
        ":SENS:VOLT:XFE %i",
        """ A boolean parameter for the enabled state of external feedback. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    # SOURce
    # STATus
    # SYSTem
    # TRACe
    # TRIGger

    def __init__(self,adapter,**kwargs):
        super(Keithley6514, self).__init__(adapter,
                                           "Keithley 6514 Systems Electrometer")
    # CALCulate
    @property
    def calculate_percent_reference_acquire(self):
        """ Use the input signal as the
            :param:`self.calculate_percent_reference` value. """
        self.write("CALC:PERC:ACQ")
