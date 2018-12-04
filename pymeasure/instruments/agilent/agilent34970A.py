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
                                              truncated_discrete_set)

class Agilent34970A(Instrument):
    """
    TODO

    .. code-block:: python

        # Establish the Agilent 34970A Data Acquisition/Switch Unit
        daq = Agilent34970A("GPIB::1::INSTR")

        TODO

    """
    # MEASure
    # TODO
    # ROUTe:MONitor
    monitor_channel = Instrument.control(
        "ROUT:MON?",
        "ROUT:MON %s",
        """ TODO """
    )
    monitor_state = Instrument.control(
        "ROUT:MON:STAT?",
        "ROUT:MON:STAT %s",
        """ TODO """,
        validator=strict_discrete_set,
        values=('OFF','ON')
    )
    monitor_data = Instrument.measurement(
        "ROUT:DATA?",
        """ TODO """
    )
    # ROUTe:SCAN
    scan_list = Instrument.control(
        "ROUT:SCAN?",
        "ROUT:SCAN %s",
        """ TODO """
    )
    scan_list_size = Instrument.measurement(
        "ROUT:SCAN:SIZE?",
        """ TODO """
    )
    # ROUTe:CHANnel:DELay
    monitor_channel_delay_value = Instrument.control() # TODO
    monitor_channel_delay_auto = Instrument.control() # TODO
    # CALCulate
    math_average
    math_minimum
    math_maximum
    math_minimum_time
    math_maximum_time
    math_range
    math_count
    math_clear
    # DATA
    data_last = Instrument.measurement(
        "DATA:LAST?",
        """ TODO """
        get_process=lambda v:v.split(',')
    )
    # TRIGger
    trigger_source = Instrument.control(
        "TRIG:SOUR?",
        "TRIG:SOUR %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={'bus':      'BUS',
                'immediate':'IMM',
                'external': 'EXT',
                'alarm 1':  'ALAR1',
                'alarm 2':  'ALAR2',
                'alarm 3':  'ALAR3',
                'alarm 4':  'ALAR4',
                'timer':    'TIM'},
        map_values=True
    )
    trigger_timer = Instrument.control(
        "TRIG:TIM?",
        "TRIG:TIM %s",
        """ TODO """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[0,3600],['MIN','MAX']]
    ) # TODO check numeric range of validator values
    trigger_count = Instrument.control(
        "TRIG:COUN?",
        "TRIG:COUNT %s",
        """ TODO """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[1,50000],['MIN','MAX','INF']]
    )
