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
        ":SENS:VOLT:GUAR %g",
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
    sense_average_filter=Instrument.control(
        ":SENS:AVER:TCON?",
        ":SENS:AVER:TONC %s",
        """ A string parameter for the digital filter control. Values are:
            `moving` or `repeating`. """,
        validator=strict_discrete_set,
        values={'moving':'MOV','repeating':'REP'},
        map_values=True
    )
    sense_average_count=Instrument.control(
        ":SENS:AVER:COUN?",
        ":SENS:AVER:COUN %g",
        """ An integer parameter for the number of
            points averaged in the filter.""",
        validator=strict_discrete_set,
        values=list((range(2,101,1))),
        cast=int
    )
    sense_average_enable=Instrument.control(
        ":SENS:AVER:STAT?",
        ":SENS:AVER:STAT %g",
        """A boolean parameter for the enabled state of the average filter.""",
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    sense_median_rank=Instrument.control(
        ":SENS:MED:RANK?",
        ":SENS:MED:RANK %g",
        """ An integer parameter for the median filter rank. """,
        validator=truncated_range,
        values=(1,5),
        cast=int
    )
    sense_median_enable=Instrument.control(
        ":SENS:MED:STAT?",
        ":SENS:MED:STAT %g",
        """A boolean parameter for the enabled state of the median filter.""",
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    # SOURce
    # STATus
    # SYSTem
    zero_check_enable=Instrument.control(
        ":SYST:ZCH?",
        ":SYST:ZCH %g",
        """ A boolean parameter for the enabled state
            of the device zero check. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    zero_correct_enable=Instrument.control(
        ":SYST:ZCOR?",
        ":SYST:ZCOR %g",
        """ A boolean parameter for the enabled state
            of the device zero correct. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    power_line_freq=Instrument.control(
        ":SYST:LFR?",
        ":SYST:LFR %g",
        """ An integer parameter for the power line frequency (Hz). """,
        validator=strict_discrete_set,
        values=(50,60)
    )
    auto_zero_enable=Instrument.control(
        ":SYST:AZER:STAT?",
        ":SYST:AZER:STAT %g",
        """ A boolean parameter for the device autozero enable state. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    error_get_next=Instrument.measurement(
        ":SYST:ERR:NEXT?",
        """ Read and clear the oldest error/status code """
    )
    error_get_all=Instrument.measurement(
        ":SYST:ERR:ALL?",
        """ Read and clear all error/status codes """
    )
    error_count=Instrument.measurement(
        ":SYST:ERR:COUN?",
        """ An integer parameter for the number
            of error/status codes in the register. """
    )
    # TRACe
    data_get=Instrument.measurement(
        ":DATA:DATA?",
        """ Read the contents of the trace/data buffer. """
    )
    data_points=Instrument.control(
        ":DATA:POIN?",
        ":DATA:POIN %g",
        """ An integer parameter for the size of the query buffer. """
    )
    data_points_actual=Instrument.measurement(
        ":DATA:POIN:ACT?",
        """ An integer parameter for the actual number of
            readings stored in the trigger/data buffer. """
    )
    data_source=Instrument.control(
        ":DATA:FEED?",
        ":DATA:FEED %s",
        """ A string parameter for source of readings to the buffer. """,
        validator=strict_discrete_set,
        values={'sense':'SENS1','calculate':'CALC1','calculate2':'CALC2'},
        map_values=True
    )
    data_source_control=Instrument.control(
        ":DATA:FEED:CONT?",
        ":DATA:FEED:CONT %s",
        """ A string parameter for the data source feed.
            Values are: `next` or `never`.""",
        validator=strict_discrete_set,
        values={'next':'NEX','never':'NEV'},
        map_values=True
    )
    timestamp_format=Instrument.control(
        ":DATA:TST:FORM?",
        ":DATA:TST:FORM %s",
        """ A string paramter for the timestamp format.
            Values are `absolute` or `relative`. """,
        validator=strict_discrete_set,
        values={'absolute':'ABS','relative':'REL'},
        map_values=True
    )
    # TRIGger
    arm_source=Instrument.control(
        ":ARM:LAY1:SOUR?",
        ":ARM:LAY1:SOUR %s",
        """ Select the ARM control source.
            Values are `immediate`, `timer`, `bus`, `manual`.""",
        validator=strict_discrete_set,
        values={'immediate':'IMM','timer':'TIM','bus':'BUS','manual':'MAN'},
        map_values=True
    )
    arm_count=Instrument.control(
        ":ARM:LAY1:COUN?",
        ":ARM:LAY1:COUN %s",
        """ An integer paramter for the ARM measurement count. The string `INF`
            can be passed for an infinte ARM count. """,
        validator=strict_discrete_set,
        values=list(range(1,2501,1))+['INF']
    )
    arm_timer=Instrument.control(
        ":ARM:LAY1:TIM?",
        ":ARM:LAY1:TIM %g",
        """ A float parameter for the ARM DELAY timer. """,
        validator=truncated_range,
        values=(0.001,99999.999)
    )
    trig_source=Instrument.control(
        ":TRIG:SEQ1:SOUR?",
        ":TRIG:SEQ1:SOUR %s",
        """ A string parameter for the Trigger control source.
            Values are: `immediate` or `link`. """,
        validator=strict_discrete_set,
        values={'immediate':'IMM','link':'TLIN'},
        map_values=True
    )
    trig_count=Instrument.control(
        ":TRIG:SEQ1:COUN?",
        ":TRIG:SEQ1:COUN %g",
        """ An integer paramter for the TRIG measurement count. The string `INF`
            can be passed for an infinte ARM count. """,
        validator=strict_discrete_set,
        values=list(range(1,2501,1))+['INF']
    )
    trig_delay=Instrument.control(
        ":TRIG:SEQ1:DEL?",
        ":TRIG:SEQ1:DEL %g",
        """ A float parameter for the trigger delay in seconds. """,
        validator=strict_range,
        values=(0,999.9999)
    )
    trig_delay_auto_enable=Instrument.control(
        ":TRIG:SEQ1:DEL:AUTO?",
        ":TRIG:SEQ1:DEL:AUTO %g",
        """ A boolean parameter for the enabled
            state of the trigger auto-delay. """,
        validator=strict_discrete_set,
        values=(0,1)
    )

    def __init__(self,adapter,**kwargs):
        super(Keithley6514, self).__init__(adapter,
                                           "Keithley 6514 Systems Electrometer")
    # CALCulate
    @property
    def calculate_percent_reference_acquire(self):
        """ Use the input signal as the
            :param:`self.calculate_percent_reference` value. """
        self.write("CALC:PERC:ACQ")
    # SYSTem
    @property
    def zero_correct_acquire(self):
        """ Acquire a new value for the zero correct. """
        self.write(":SYST:ZCOR:ACQ")
    @property
    def preset_restore(self):
        """ Reset the device to default state. """
        self.write(":SYST:PRES")
    @property
    def timestamp_reset(self):
        """ Reset the timestamp to 0 seconds. """
        self.write(":SYST:TIME:RES")
    @property
    def error_clear_all(self):
        """ Clear all error/status messages """
        self.write(":SYST:ERR:CLE")
    @property
    def system_local(self):
        """ Take device out of remote mode. """
        self.write(":SYST:LOC")
    @property
    def system_remote(self):
        """ Put device into remote mode. """
        self.write(":SYST:REM")
    @property
    def system_lock(self):
        """ Put device into or out of local lockout. """
        self.write(":SYST:RWL")
    @property
    def data_clear_all(self):
        """ Clear all readings from the trigger/data buffer. """
        self.write(":DATA:CLE")
    @property
    def trig_init(self):
        """ Immediately initiate one trigger cycle. """
        self.write(":INIT:IMM")
    @property
    def trig_reset(self):
        """ Reset trigger system to idle state. """
        self.write(":ABOR")
    @property
    def trig_clear(self):
        """ Immediately clears the input triggers. """
        self.write(':TRIG:CLE')
