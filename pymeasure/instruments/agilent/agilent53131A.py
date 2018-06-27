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
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, truncated_discrete_set

class Agilent53131A(Instrument):
    """
    Represent the 2 channel HP/Agilent 53131A 225 MHz universal counter.

    Does not contain full suite of device commands.

    .. code-block:: python

        counter = Agilent53131A("GPIB::1::INSTR")   # Esablish the Agilent 53131A counter device

        counter.device_calibrate                    # Run the self calibtration

        TODO

    """

    ##########
    # Device #
    ##########

    device_system_version = Instrument.measurement(
        ':SYST:VERS?',
        """ TODO """
    )

    device_system_error = Instrument.measurement(
        ':SYST:ERR?',
        """ TODO """
    )

    device_calibration = Instrument.measurement(
        '*CAL?',
        """ TODO """,
        validator=strict_discrete_set,
        values={'pass':0, 'fail':1},
        map_values=True
    )

    #########################
    # Channel Configuration #
    #########################

    channel_mode = Instrument.control(
        ':SENS:EVENT2:FEED?',
        ':SENS:EVENT2:FEED %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'common':'"INP"', 'independent':'"INP2"'},
        map_values=True
    )

    channel_1_couple = Instrument.control(
        ':INP1:COUP?',
        ':INP1:COUP %s',
        """ TODO """,
        validator=strict_discrete_set,
        values=('AC','DC')
    )

    channel_2_couple = Instrument.control(
        ':INP2:COUP?',
        ':INP2:COUP %s',
        """ TODO """,
        validator=strict_discrete_set,
        values=('AC','DC')
    )

    channel_1_impedance = Instrument.control(
        ':INP1:IMP?',
        ':INP1:IMP %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(50,1e6)
    )

    channel_2_impedance = Instrument.control(
        ':INP2:IMP?',
        ':INP2:IMP %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(50,1e6)
    )

    channel_1_attenuation = Instrument.control(
        ':INP1:ATT?',
        ':INP1:ATT %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(1,10)
    )

    channel_2_attenuation = Instrument.control(
        ':INP2:ATT?',
        ':INP2:ATT %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(1,10)
    )

    channel_1_filter = Instrument.control(
        ':INP1:FILT?',
        ':INP1:FILT %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(1,0)
    )

    channel_2_filter = Instrument.control(
        ':INP2:FILT?',
        ':INP2:FILT %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(1,0)
    )

    channel_1_filter_frequency = Instrument.measurement(
        ':INP1:FILT:FREQ?',
        """ TODO """
    )

    channel_2_filter_frequency = Instrument.measurement(
        ':INP2:FILT:FREQ?',
        """ TODO """
    )

    channel_1_sensitivity = Instrument.control(
        ':SENS:EVENT1:HYST:REL?',
        ':SENS:EVENT1:HYST:REL %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'min':0, 'norm':50, 'max':100},
        map_values=True
    )

    channel_2_sensitivity = Instrument.control(
        ':SENS:EVENT2:HYST:REL?',
        ':SENS:EVENT2:HYST:REL %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'min':0, 'norm':50, 'max':100},
        map_values=True
    )

    channel_1_trigger_level = Instrument.control(
        ':SENS:EVENT1:LEVEL?',
        ':SENS:EVENT1:LEVEL %g',
        """ TODO """,
        validator=truncated_range,
        values=(-5.125, 5.125)
    )

    channel_2_trigger_level = Instrument.control(
        ':SENS:EVENT2:LEVEL?',
        ':SENS:EVENT2:LEVEL %g',
        """ TODO """,
        validator=truncated_range,
        values=(-5.125, 5.125)
    )

    channel_1_trigger_auto_level = Instrument.control(
        ':SENS:EVENT1:LEVEL:REL?',
        ':SENS:EVENT1:LEVEL:REL %g',
        """ TODO """,
        validator=truncated_discrete_set,
        values=list(range(0, 100, 10))
    )

    channel_2_trigger_auto_level = Instrument.control(
        ':SENS:EVENT2:LEVEL:REL?',
        ':SENS:EVENT2:LEVEL:REL %g',
        """ TODO """,
        validator=truncated_discrete_set,
        values=list(range(0, 100, 10))
    )

    channel_1_trigger_auto = Instrument.control(
        ':SENS:EVENT1:LEVEL:AUTO?',
        ':SENS:EVENT1:LEVEL:AUTO %g',
        """ TODO """,
        validator=strict_discrete_set,
        values={'on':1,'off':0},
        map_values=True
    )

    channel_2_trigger_auto = Instrument.control(
        ':SENS:EVENT2:LEVEL:AUTO?',
        ':SENS:EVENT2:LEVEL:AUTO %g',
        """ TODO """,
        validator=strict_discrete_set,
        values={'on':1,'off':0},
        map_values=True
    )

    channel_1_trigger_slope = Instrument.control(
        ':SENS:EVENT1:SLOPE?',
        ':SENS:EVENT1:SLOPE %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'positive':'POS', 'negative':'NEG'},
        map_values=True
    )

    channel_2_trigger_slope = Instrument.control(
        ':SENS:EVENT2:SLOPE?',
        ':SENS:EVENT2:SLOPE %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'positive':'POS', 'negative':'NEG'},
        map_values=True
    )

    ###########################
    # Reference Configuration #
    ###########################

    reference_source = Instrument.control(
        ':SENS:ROSC:SOUR?',
        ':SENS:ROSC:SOUR %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'internal':'INT', 'external':'EXT'},
        map_values=True
    )

    reference_external_validator = Instrument.control(
        ':SENS:ROSC:EXT:CHEC?',
        ':SENS:ROSC:EXT:CHEC %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'on':'ON', 'off':'OFF', 'once':'ONCE'},
        map_values=True
    )

    reference_external_frequency = Instrument.measurement(
        ':SENS:ROSC:EXT:FREQ?',
        """ TODO """
    )

    ###########
    # Measure #
    ###########

    query_data = Instrument.measurement(
        ':SENS:DATA?',
        """ TODO """
    )

    measure_function = Instrument.control(
        ':SENSE:FUNC?',
        ':SENSE:FUNC %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'time_interval':'"TINT"'},
        map_values=True
    )

    measure_continuous = Instrument.control(
        ':INIT:CONT?',
        ':ABORT;:INIT:CONT %g',
        """ TODO """,
        validator=strict_discrete_set,
        values=(1, 0, True, False),
        cast=int
    )

    time_interval_arm_start = Instrument.control(
        ':SENS:TINT:ARM:START:SOUR?',
        ':SENS:TINT:ARM:START:SOUR %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'immediate':'IMM', 'external':'EXT'},
        map_values=True
    )

    time_interval_arm_stop = Instrument.control(
        ':SENS:TINT:ARM:STOP:SOUR?',
        ':SENS:TINT:ARM:STOP:SOUR %s',
        """ TODO """,
        validator=strict_discrete_set,
        values={'immediate':'IMM', 'timer':'TIM'},
        map_values=True
    )

    time_interval_timer_value = Instrument.control(
        ':SENS:TINT:ARM:STOP:TIM?',
        ':SENS:TINT:ARM:STOP:TIM %g',
        """ TODO """
    )

    time_interval_arm_start_slope = Instrument.control(
        ':SENS:TINT:ARM:START:SLOPE?',
        ':SENS:TINT:ARM:START:SLOPE %s',
        """ A string parameter that represents the polarity of the ARM slope. """,
        validator=strict_discrete_set,
        values={'positive':'POS', 'negative':'NEG'},
        map_values=True
    )

    def __init__(self, adapter, **kwargs):
        super(Agilent53131A, self).__init__(adapter, "Agilent 53131A Universal Counter", **kwargs
        )

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)

    @property
    def trigger_init(self):
            """ TODO """
            self.write(':INIT')

    def time_interval_config(self, channel_1_trigger_level, channel_2_trigger_level, channel_1_slope='positive', channel_2_slope='negative', channel_mode='common', impedance=1e6, couple='DC', measure_continuous=True):
        """ TODO """
        self.measure_continuous=measure_continuous
        self.measure_function='time_interval'
        self.channel_mode=channel_mode
        self.channel_1_impedance=impedance
        self.channel_2_impedance=impedance
        self.channel_1_couple=couple
        self.channel_2_couple=couple
        self.channel_1_trigger_level=channel_1_trigger_level
        self.channel_2_trigger_level=channel_2_trigger_level
        self.channel_1_trigger_slope=channel_1_slope
        self.channel_2_trigger_slope=channel_2_slope
