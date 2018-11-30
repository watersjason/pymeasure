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
                                              truncated_range,
                                              strict_discrete_set,
                                              truncated_discrete_set)

class Agilent53131A(Instrument):
    """
    Represent the 2 channel HP/Agilent 53131A 225 MHz universal counter.

    Does not contain full suite of device commands.

    .. code-block:: python

        # Esablish the Agilent 53131A counter device
        counter = Agilent53131A("GPIB::1::INSTR")

        # Run the self calibtration
        counter.device_calibrate

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
    # CALibration subsystem
    calibration_self = Instrument.measurement(
        '*CAL?',
        """ Run an internal interpolator self-calibration.
            Returns string parameter of `pass` or `fail`. """,
        validator=strict_discrete_set,
        values={'pass':0, 'fail':1},
        map_values=True
    )
    calibration_count = Instrument.measurement(
        "CAL:COUN?",
        """ Returns an integer parameter with the number
            of times the device has been calibrated. """,
        get_process=lambda v:int(v)
    )
    calibration_data = Instrument.control(
        "CAL:DATA?",
        "CAL:DATA %s",
        """ TODO """
    )
    calibration_security_code = Instrument.setting(
        "CAL:SEC:CODE %s",
        """ An integer parameter, in the range 0 to 9999999,
            that replaces the device security code. The
            device must be unsecured to use this command. """
    )
    calibration_security_enable = Instrument.control(
        "CAL:SEC:STAT?",
        "CAL:SEC:STAT %s",
        """ Returns a boolean parameter that indicates if
            the device is secured.

            The security state is toggled by an iterable
            with the elements: `boolean`, `security code`."""
    )
    # DISPlay subsystem
    display_enable = Instrument.control(
        "DISP:ENAB?",
        "DISP:ENAB %i",
        """ A boolean parameter that represents
            the enabled state of the front display. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=int
    )
    display_menu_enable = Instrument.control(
        "DISP:MENU:STAT?",
        "DISP:MENU:STAT %s",
        """ A boolean parameter for the display
            menu state. When the menu display is
            disabled, the results are displayed. """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True,
        cast=bool
    )
    display_feed = Instrument.control(
        "DISP:WIND:TEXT:FEED?",
        "DISP:WIND:TEXT:FEED:%s",
        """ A string parameter for the CALC data
            flow that is fed to the display. """,
        validator=strict_discrete_set,
        values=('CALC2','CALC3')
    )
    display_number_separation = Instrument.control(
        "DISP:WIND:TEXT:RAD?",
        "DISP:WIND:TEXT:RAD %s",
        """ A string parameter for the character used
            in numerical convention of incrementally
            seperating numbers every 3 digits. """,
        validator=strict_discrete_set,
        values={'comma':'COMM',
                'decimal':'DPO'},
        map_values=True
    )
    # FORMat subsystem
    format_data = Instrument.control(
        "FORM:DATA?",
        "FORM:DATA %s",
        """ """,
        validator=strict_discrete_set,
        values={'ascii':'ASC',
                'real':'REAL'},
        map_values=True
    )
    # HCOPy subsystem
    device_print_continuous = Instrument.control(
        "HCOP:CONT?",
        "HCOP:CONT %s",
        """ A boolean parameter that enables
            the printing of data results. """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
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
        values={'common':'"INP"','independent':'"INP2"'},
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
        """ A string parameter that represents
            the polarity of the ARM slope. """,
        validator=strict_discrete_set,
        values={'positive':'POS', 'negative':'NEG'},
        map_values=True
    )

    def __init__(self, adapter, **kwargs):
        super(Agilent53131A, self).__init__(adapter,
              "Agilent 53131A Universal Counter", **kwargs)

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)
        self.channel=kwargs.get('channel',1)

    @property
    def abort(self):
        """ A property that causes the device to abort
            any measurements in progress. The command
            processes as quickly as possible."""
        self.write("ABORT")


    @property
    def trigger_init(self):
            """ TODO """
            self.write(':INIT')

    def time_interval_config(self,
                             channel_1_trigger_level,
                             channel_2_trigger_level,
                             channel_1_slope='positive',
                             channel_2_slope='negative',
                             channel_mode='common',
                             impedance=1e6,
                             couple='DC',
                             measure_continuous=True):
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
    #
    @calibration_security_enable.setter
    def calibration_security_enable(self,state_code):
        try:
            state, code = state_code
        except ValueError:
            raise ValueError('The setting must be an iterable with the'
                             'elements: state, security_code.')
        strict_discrete_set(state,(0,1))
        strict_range(code,(0,9999999))
        self.write("CAL:SEC:STAT {}, {}".format(state,code))
    @display_menu_enable.setter
    def display_menu_enable(self,value):
        if value == 0:
            self.write("DISP:MENU:STAT OFF")
