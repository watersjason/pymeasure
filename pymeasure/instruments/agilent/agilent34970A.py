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
    # Channel list
    __channel_list = []
    @property
    def channel_list(self):
        """ A list property specifying the channels that a command is applied.
            Individual channels are of the form: ``scc``, where ``s`` is the
            card slot number (1, 2, 3) and ``cc`` is the channel number on the
            specified card.
        """
        return self.__channel_list
    @channel_list.setter
    def channel_list(self, channels):
        self.__channels = channels

    # CALCulate
    math_average = Instrument.measurement(
        "CALC:AVER:AVER?",
        """ Returns a float value of the calculated
            average value of the math register. """
    ) #TODO link to channel list
    math_minimum = Instrument.measurement(
        "CALC:AVER:MIN?",
        """ Returns a float value of the calculated
            minimum value of the math register. """
    ) #TODO link to channel list
    math_maximum = Instrument.measurement(
        "CALC:AVER:MAX?",
        """ Returns a float value of the calculated
            maximum value of the math register. """
    ) #TODO link to channel list
    math_minimum_time = Instrument.measurement(
        "CALC:AVER:MIN:TIME?",
        """ TODO """
    ) #TODO link to channel list
    math_maximum_time = Instrument.measurement(
        "CALC:AVER:MAX:TIME?",
        """ TODO """
    ) #TODO link to channel list
    math_range = Instrument.measurement(
        "CALC:AVER:PTP?",
        """ Returns a float value of the calculated
            peak to peak range of the math register.  """
    ) #TODO link to channel list
    math_count = Instrument.measurement(
        "CALC:AVER:COUN?",
        """ Returns a float value of the total number
            of data points in the math register.  """
    ) #TODO link to channel list
    # DATA
    data_last = Instrument.measurement(
        "DATA:LAST?",
        """ TODO """
    )
    # FORMat
    read_alarm_enable = Instrument.control(
        "FORM:READ:ALAR?",
        "FORM:READ:ALAR %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True,
        cast=bool
    )
    read_channel_enable = Instrument.control(
        "FORM:READ:CHAN?",
        "FORM:READ:CHAN %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True,
        cast=bool
    )
    read_time_enable = Instrument.control(
        "FORM:READ:TIME?",
        "FORM:READ:TIME %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True,
        cast=bool
    )
    read_unit_enable = Instrument.control(
        "FORM:READ:UNIT?",
        "FORM:READ:UNIT %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True,
        cast=bool
    )
    read_time_relative = Instrument.control(
        "FORM:READ:TIME:TYPE?",
        "FORM:READ:TIME:TYPE %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={True:'REL',
                False:'ABS'},
        map_values=True,
        cast=bool
    )
    # INSTrument
    dmm_installed = Instrument.measurement(
        "INST:DMM:INST?",
        """ A boolean property for the physically installed DMM. """,
        cast=bool
    )
    dmm_enable = Instrument.control(
        "INST:DMM?",
        "INST:DMM %s",
        """ A boolean property for the enabled state of the internal DMM. """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True,
        cast=bool
    )
    # MEASure
    # TODO
    # ROUTe
    remote_channel = Instrument.control(
        "ROUT:MON?",
        "ROUT:MON %s",
        """ An integer parameter that sets the remote channel. """,
        set_process=lambda v: '(@'+str(v)+')',
        get_process=lambda v: int(v.strip(')').split('@')[-1])
    )
    remote_enable = Instrument.control(
        "ROUT:MON:STAT?",
        "ROUT:MON:STAT %s",
        """ A boolean parameter that enables the remote interface. """,
        validator=strict_discrete_set,
        values={False:'OFF',
                True:'ON'},
        map_values=True,
        cast=bool
    )
    remote_data = Instrument.measurement(
        "ROUT:DATA?",
        """ Read data from the channel selected by
            :attr:`~.Agilent34970A.remote_channel`. """
    )
    scan = Instrument.control(
        "ROUT:SCAN?",
        "ROUT:SCAN %s",
        """ TODO """
    ) # TODO link to scan list
    scan_list_size = Instrument.measurement(
        "ROUT:SCAN:SIZE?",
        """ TODO """
    )
    remote_channel_delay = Instrument.control(
        "ROUT:CHAN:DEL?",
        "ROUT:CHAN:DEL %g",
        """ TODO """
    ) # TODO link to channel list
    remote_channel_delay_auto = Instrument.control(
        "ROUT:CHAN:DEL:AUTO?",
        "ROUT:CHAN:CEL:AUTO %s",
        """ TODO """
    ) # TODO link to channel list
    remote_channel_source = Instrument.control(
        "ROUT:CHAN:ADV:SOUR?",
        "ROUT:CHAN:ADV:SOUR %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={'external':'EXT',
                'bus':'BUS',
                'immediate':'IMM'},
        map_values=True
    )
    remote_channel_4_wire = Instrument.control(
        "ROUT:CHAN:FWIR?",
        "ROUT:CHAN:FWIR %i",
        """ TODO """,
        validator=strict_discrete_set,
        values={True,'ON',
                False,'OFF'},
        map_values=True,
        cast=bool
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

    def __init__(self, adapter, **kwargs):
        super(Agilent34970A, self).__init__(adapter,
              "Agilent 34970A DAQ/Switch Unit", **kwargs)
    @property
    def abort(self):
        """ TODO """
        self.write('ABOR')
    @property
    def init(self):
        """ TODO """
        self.write('INIT')
    # CALCulate
    @property
    def math_clear(self):
        """ Clear all data in the math register. """
        self.write('CALC:AVER:CLE')  # TODO channel list
    @property
    def null_channel(self):
        """ Make a null measurement and apply it as
            an offset to the current channel. """,
        self.write('CALC:SCAL:OFFSET:NULL') # TODO channel list
