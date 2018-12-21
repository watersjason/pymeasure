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
                                              truncated_discrete_set,
                                              discreteTruncate)
from numpy import arange

class Agilent53131A(Instrument):
    """
    Represent the HP/Agilent 53131A 225 MHz universal counter. Channel specific
    commands use the value set by the property :attr:`~.Agilent53131A.channel`.

    Does not support full suite of device commands.

    .. code-block:: python

        counter = Agilent53131A(
                    "GPIB::1::INSTR")   # Esablish device communication

        counter.device_calibrate        # Run the self calibtration

        counter.channel                 # Read the current channel
        counter.input_impedance = 50    # Channel 1 input impedance to 50 Ohm

        counter.channel=2               # Change the channel to 2
        counter.input_impedance = 50    # Channel 2 input impedance to 50 Ohm

    """
    # property that sets channel used for channel-specific commands
    __channel_list = (1,2)
    __channel = 1
    @property
    def channel(self):
        """ Value for channel-specific device commands . """
        return self.__channel
    @channel.setter
    def channel(self, value):
        strict_discrete_set(value, self.__channel_list)
        self.__channel=value

    # CALCulate subsystem - commands not implemented
    # CALibration subsystem
    calibration_self = Instrument.measurement(
        '*CAL?',
        """ Run an internal interpolator self-calibration. Returns string
            parameter of ``pass`` or ``fail``. """,
        validator=strict_discrete_set,
        values={'pass':0,
                'fail':1},
        map_values=True
    )
    calibration_count = Instrument.measurement(
        "CAL:COUN?",
        """ Returns an integer parameter with the number of times the device
            has been calibrated. """,
        cast=int
    )
    calibration_data = Instrument.control(
        "CAL:DATA?",
        "CAL:DATA %s",
        """ An iterable property with the device calibration data. """
    )
    calibration_security_code = Instrument.setting(
        "CAL:SEC:CODE %s",
        """ An integer parameter in the range(0, 9999999) that replaces the
            device security code. The device must be unsecured to use this
            command. """
    )
    calibration_security_enable = Instrument.control(
        "CAL:SEC:STAT?",
        "CAL:SEC:STAT %s",
        """ Returns a boolean parameter that indicates if the device is secured.
            The security state is toggled by an iterable with the elements:
            (``boolean``, ``security code``)."""
    )
    # CONFigure subsystem - commands not implemented; use sense_function
    # DIAGnostic subsystem - commands not implemented
    # DISPlay subsystem
    display_enable = Instrument.control(
        "DISP:ENAB?",
        "DISP:ENAB %i",
        """ A boolean parameter that represents the enabled state of the front
            display. """,
        validator=strict_discrete_set,
        values=(True,False)
    )
    display_menu_enable = Instrument.control(
        "DISP:MENU:STAT?",
        "DISP:MENU:STAT %s",
        """ A boolean parameter for the display menu state. When ``False``, the
            menu display is disabled and the measurement results are shown on
            the screen. """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True
    )
    display_feed = Instrument.control(
        "DISP:WIND:TEXT:FEED?",
        "DISP:WIND:TEXT:FEED:%s",
        """ A string parameter for the CALC data flow that is fed to the
            display. """,
        validator=strict_discrete_set,
        values=('CALC2','CALC3')
    )
    display_number_separation = Instrument.control(
        "DISP:WIND:TEXT:RAD?",
        "DISP:WIND:TEXT:RAD %s",
        """ A string parameter for the character used in numerical convention
            of incrementally seperating numbers every 3 digits. """,
        validator=strict_discrete_set,
        values={'comma':'COMM',
                'decimal':'DPO'},
        map_values=True
    )
    # FETCh subsystem - commands not implemented
    # FORMat subsystem
    format_data = Instrument.control(
        "FORM:DATA?",
        "FORM:DATA %s",
        """ A string parameter for the output data format. Values are:
            ``ascii`` or ``real``. """,
        validator=strict_discrete_set,
        values={'ascii':'ASC',
                'real':'REAL'},
        map_values=True
    )
    # HCOPy subsystem
    device_print_continuous = Instrument.control(
        "HCOP:CONT?",
        "HCOP:CONT %s",
        """ A boolean parameter that enables the printing of data results. """,
        validator=strict_discrete_set,
        values={True:'ON',
                False:'OFF'},
        map_values=True
    )
    # INITiate subsystem
    init_auto = Instrument.control(
        "INIT:AUTO?",
        "INIT:AUTO %i",
        """ A boolean parameter for the device automatic initiatation state.
            When ``True``, the device stops collecting data on a limit test
            failure. When `False`, the data collection continues even after
            a failed limit test. """,
        validator=strict_discrete_set,
        values=(True,False)
    )
    init_continuous = Instrument.control(
        "INIT:CONT?",
        "INIT:CONT %i",
        """ A boolean parameter for the device continuously initiated
            measurement state. When ``True``, a new measurement immediately
            follows a completed measurement. When ``False``, no new
            measurements are collected.""",
        validator=strict_discrete_set,
        values=(True,False)
    )
    # INPut subsystem
    input_attenuation = Instrument.control(
        "INP{}:ATT?".format(channel),
        "INP{}:ATT %g".format(channel),
        """ An integer parameter for the channel-specific input attenuation.
            The channel is specified by the :attr:`~.Agilent53131A.channel`
            property. """
    )
    input_coupling = Instrument.control(
        "INP{}:COUP?".format(channel),
        "INP{}:COUP %s".format(channel),
        """ A string parameter for the channel-specific input couple. The
            channel is specified by the :attr:`~.Agilent53131A.channel`
            property. """
    )
    input_filter_enable = Instrument.control(
        "INP{}:FILT:LPAS:STAT?".format(channel),
        "INP{}:FILT:LPAS:STAT %i".format(channel),
        """ A boolean parameter to enable the channel-specific low-pass filter.
            The channel is specified by the :attr:`~.Agilent53131A.channel`
            property. """
    )
    input_filter_frequency = Instrument.measurement(
        "INP{}:FILT:LPAS:FREQ?".format(channel),
        """ An integer parameter for the channel-specific low-pass filter
            frequency. The channel is specified by the
            :attr:`~.Agilent53131A.channel` property. """
    )
    input_impedance = Instrument.control(
        "INP{}:IMP?".format(channel),
        "INP{}:IMP %g".format(channel),
        """ An integer parameter for the channel-specific input impedance.
            Values for the impedance are 50, or 1e6 Ohms. The channel is
            specified by the :attr:`~.Agilent53131A.channel` property. """
    )
    # INPut3 (INP3) subsystem - commands not implemented
    # MEASure subsystem
    # MEMory subsystem - commands not implemented
    # SENSe subsystem
    sense_data = Instrument.measurement(
        ':SENS:DATA?',
        """ Returns the current measurement result data of the SENSe subsystem.
            No offset or scale is applied to the returned data.

            If this query executes while a measurement is in progress, then the
            prior measurement result is returned, or if no valid data is
            availiable, the query returns ``-9.91E37``. """
    )
    # SENSe:EVENt[1|2] subtree
    sense_common_mode = Instrument.control(
        'SENS:EVEN2:FEED?',
        'SENS:EVEN2:FEED %s',
        """ A boolean parameter. When ``True``, the channel 2 feed is linked to
            the channel 1 feed. When ``False``, the channel 2 feed is
            independent of the channel 1 feed.""",
        validator=strict_discrete_set,
        values={True:   '"INP"',
                False:  '"INP2"'},
        map_values=True
    )
    trigger_relative_hysteresis = Instrument.control(
        'SENS:EVEN{}:HYST:REL?'.format(channel),
        'SENS:EVEN{}:HYST:REL %g'.format(channel),
        """ A channel specific float parameter for the relative hysteresis.
            Larger values of relative hysteresis have low senesitivity and
            high noise immunity. Values range from 0 to 100.

            The channel is set by the :attr:`~.Agilent53131A.channel` property.
        """
    )
    trigger_level = Instrument.control(
        'SENS:EVEN{}:LEV:ABS?'.format(channel),
        'SENS:EVEN{}:LEV:ABS %g'.format(channel),
        """ A channel specific float parameter for the level at the center of
            the hysteresis window. Values range from -5.125 to 5.125 Volts.
            The actual trigger event occurs at the top of the hysteresis window
            (for POSitive slope) or at the bottom of the hysteresis window (for
            NEGative slope).

            The channel is set by the :attr:`~.Agilent53131A.channel` property.
        """
    )
    trigger_auto_enable = Instrument.control(
        "SENS:EVEN{}:LEV:ABS:AUTO?".format(channel),
        "SENS:EVEN{}:LEV:ABS:AUTO %i".format(channel),
        """ A channel-specific boolean parameter to enable automatic selection
            of the trigger level.

            The channel is set by the :attr:`~.Agilent53131A.channel` property.
        """
    )
    trigger_auto_level = Instrument.control(
        'SENS:EVEN{}:LEV:REL?'.format(channel),
        'SENS:EVEN{}:LEV:REL %s'.format(channel),
        """ A channel-specific integer parameter for the percentage of the
            peak-to-peak range of the signal at which the intrument
            automatically triggers. An integer value in range(0, 100, 10). """
    )
    trigger_slope_positive = Instrument.control(
        'SENS:EVEN{}:SLOP?'.format(channel),
        'SENS:EVEN{}:SLOP %s'.format(channel),
        """ A channel-specific boolean parameter to enable the device to trigger
            on the positive slope (rising edge) of the input signal.
            When ``False``, the trigger occurs on the negative slope (falling
            edge) of the input signal.

            The channel is set by the :attr:`~.Agilent53131A.channel` property.
        """
    )
    # SENSe:EVENt3 subtree - commands not implemented
    # SENSe:FREQuency:ARM subtree
    sense_function = Instrument.control(
        "SENS:FUNC:ON?",
        "SENS:FUNC:ON %s",
        """ A string parameter for the device sense function. Values are:
                ``'duty cycle'``, ``'fall time'``, ``'frequency'``,
                ``'frequency 2'``, ``'frequency 3'``, ``'frequency ratio'``,
                ``'frequency ratio 1,3'``, ``'frequency ratio 2,1'``,
                ``'frequency ratio 3,1'``, ``'negative width'``, ``'period'``,
                ``'period 2'``, ``'period 3'``, ``'phase'``, ``'phase 2'``,
                ``'positive width'``, ``'time interval'``, ``'totalize'``,
                ``'rise time'``, ``'voltage max'``, ``'voltage max 2'``,
                ``'voltage min'``, ``'voltage min 2'``: ``'voltage range'``,
                ``'voltage range 2'``. """,
        validator=strict_discrete_set,
        values={'duty cycle':          '"DCTC"',
                'fall time':           '"FTIM"',
                'frequency':           '"FREQ"',
                'frequency 2':         '"FREQ 2"',
                'frequency 3':         '"FREQ 3"',
                'frequency ratio':     '"FREQ:RAT"',
                'frequency ratio 1,3': '"FREQ:RAT 1,3"',
                'frequency ratio 2,1': '"FREQ:RAT 2,1"',
                'frequency ratio 3,1': '"FREQ:RAT 3,1"',
                'negative width':      '"NWID"',
                'period':              '"PER"',
                'period 2':            '"PER 2"',
                'period 3':            '"PER 3"',
                'phase':               '"PHAS"',
                'phase 2':             '"PHAS 2"',
                'positive width':      '"PWID"',
                'time interval':       '"TINT"',
                'totalize':            '"TOT"',
                'rise time':           '"RTIM"',
                'voltage max':         '"VOLT:MAX"',
                'voltage max 2':       '"VOLT:MAX 2"',
                'voltage min':         '"VOLT:MIN"',
                'voltage min 2':       '"VOLT:MIN 2"',
                'voltage range':       '"VOLT:PTP"',
                'voltage range 2':     '"VOLT:PTP 2"'
                },
        map_values=True
    )
    # SENSe:PHASe:ARM subtree - commands not implemented
    # SENSe:ROSCillator subtree
    reference_external_check = Instrument.control(
        ':SENS:ROSC:EXT:CHEC?',
        ':SENS:ROSC:EXT:CHEC %s',
        """ A string property that enables a check for the validity and presence
            of an external reference signal. Values are:
            ``'ON'``    If :attr:`~.Agilent53131A.reference_source_external`=
                        ``True`` and
                        :attr:`~.Agilent53131A.reference_source_auto`=``False``,
                        the external reference signal is monitored at each
                        measurement completion to ensure that the frequency is
                        1, 5, or 10 MHz.
            ``'OFF'``   The external reference signal is not checked at all.
            ``'ONCE'``  If :attr:`~.Agilent53131A.reference_source_external`=
                        ``True``, then the external reference signal is checked
                        a single time and then set to ``'OFF'``. """,
        validator=strict_discrete_set,
        values=('ON','OFF','ONCE')
    )
    reference_external_frequency = Instrument.measurement(
        ':SENS:ROSC:EXT:FREQ?',
        """ Returns the frequency (Hz) from the external reference oscillator
            signal. """
    )
    reference_source_external = Instrument.control(
        ':SENS:ROSC:SOUR?',
        ':SENS:ROSC:SOUR %s',
        """ A boolean parameter that enables the external reference source.
            When ``True``, the reference signal is sourced from the external
            reference input. When ``False``, the reference signal is from the
            internal source.""",
        validator=strict_discrete_set,
        values={False:  'INT',
                True:   'EXT'},
        map_values=True
    )
    reference_source_auto = Instrument.control(
        ":SENS:ROSC:SOUR:AUTO?",
        ":SENS:ROSC:SOUR:AUTO %i",
        """ A boolean parameter that enables the automatic selection of the
            reference signal source. When ``True`` and a valid signal is
            present on the external reference input, the external reference is
            selected; otherwise the internal source is used. When ``False``,
            the source is determined by
            :attr:`~.Agilent53131A.reference_source_external`.""",
        validator=strict_discrete_set,
        values=(True,False)
    )
    # SENSe:TINTerval subtree - commands partially supported
    interval_start_arm_slope_positive = Instrument.control(
        "SENS:TINT:ARM:ESTART:LAY2:SLOP?",
        "SENS:TINT:ARM:ESTART:LAY2:SLOP %s",
        """ A boolean parameter that sets the time interval measurement start
            trigger to the positive edge. When ``True``, the event slope is
            positive. When ``False``, the event slope is negative.""",
        validator=strict_discrete_set,
        values={True:   'POS',
                False:  'NEG'},
        map_values=True
    )
    interval_start_arm_source_external = Instrument.control(
        "SENS:TINT:ARM:ESTART:LAY2:SOUR?",
        "SENS:TINT:ARM:ESTART:LAY2:SOUR %s",
        """ A boolean parameter that sets the signal for the time measurement
            start trigger to the external source. When ``True``, the trigger
            signal waits for an external signal. When ``False``, the trigger
            signal is sent immediately. """,
        validator=strict_discrete_set,
        values={True:   'EXT',
                False:  'IMM'},
        map_values=True
    )
    interval_start_trig_count = Instrument.control(
        "SENS:TINT:ARM:ESTART:LAY1:ECO?",
        "SENS:TINT:ARM:ESTART:LAT1:ECO %i",
        """ An integer parameter for the number of events used to delay the
            start arm signal for time interval measurements. """,
        validator=discreteTruncate,
        values=arange(1,99999999,1),
        cast=int
    )
    interval_start_trig_source = Instrument.control(
        "SENS:TINT:ARM:ESTART:LAY1:SOUR?",
        "SENS:TINT:ARM:ESTART:LAY1:SOUR %s",
        """ A string parameter for the arm start signal source.

            Parameter values are:
            ``immediate``   Armed immediately.
            ``time``        Armed after delay set by
                            :attr:`~.Agilent53131A.interval_start_arm_delay`.
            ``internal``    Armed after required number of signals recieved.
                            Number of singals is set by
                            :attr:`~.Agilent53131A.interval_start_arm_count`.
        """,
        validator=strict_discrete_set,
        values={'immediate':    'IMM',
                'time':         'TIM',
                'internal':     'INT'},
        map_values=True
    )
    interval_start_trig_delay = Instrument.control(
        "SENS:TINT:ARM:ESTART:LAY1:TIM?",
        "SENS:TINT:ARM:ESTART:LAY1:TIM %g",
        """ A float parameter for the time delay value used for the start arm
            event of time interval measurements. Values are in
            range(100e-9, 0.9999999, 100e-9). """,
        validator=discreteTruncate,
        values=arange(100e-9,0.9999999,100e-9)
    )
    interval_stop_arm_slope_positive = Instrument.control(
        "SENS:TINT:ARM:ESTOP:LAY2:SLOP?",
        "SENS:TINT:ARM:ESTOP:LAY2:SLOP %s",
        """ A boolean parameter that sets the time interval measurement
            stop trigger to the positive edge. When ``True``, the slope is
            positive. When ``False``, the slope is negative.""",
        validator=strict_discrete_set,
        values={True:   'POS',
                False:  'NEG'},
        map_values=True
    )
    interval_stop_arm_source_external = Instrument.control(
        "SENS:TINT:ARM:ESTOP:LAY2:SOUR?",
        "SENS:TINT:ARM:ESTOP:LAY2:SOUR %s",
        """ A boolean parameter that sets the signal for the time measurement
            stop trigger to the external source. When ``True``, the trigger
            signal waits for an external signal. When ``False``, the trigger
            signal is sent immediately. """,
        validator=strict_discrete_set,
        values={True:   'EXT',
                False:  'IMM'},
        map_values=True
    )
    interval_stop_trig_count = Instrument.control(
        "SENS:TINT:ARM:ESTOP:LAY1:ECO?",
        "SENS:TINT:ARM:ESTOP:LAT1:ECO %i",
        """ An integer parameter for the number of events used to delay the
            stop arm signal for time interval measurements.  """,
        validator=discreteTruncate,
        values=arange(1,99999999,1),
        cast=int
    )
    interval_stop_trig_source = Instrument.control(
        "SENS:TINT:ARM:ESTOP:LAY1:SOUR?",
        "SENS:TINT:ARM:ESTOP:LAY1:SOUR %s",
        """ A string parameter for the arm stop signal source.

            Parameter values are:
            ``immediate``   Armed immediately.
            ``time``        Armed after delay set by
                            :attr:`~.Agilent53131A.interval_stop_arm_delay`.
            ``internal``    Armed after required number of signals recieved.
                            Number of singals is set by
                            :attr:`~.Agilent53131A.interval_stop_arm_count`.
        """,
        validator=strict_discrete_set,
        values={'immediate':    'IMM',
                'time':         'TIM',
                'internal':     'INT'},
        map_values=True
    )
    interval_stop_trig_delay = Instrument.control(
        "SENS:TINT:ARM:ESTOP:LAY1:TIM?",
        "SENS:TINT:ARM:ESTOP:LAY1:TIM %g",
        """ A float parameter for the time delay value used for the stop arm
            event of time interval measurements. Values are in
            range(100e-9, 0.9999999, 100e-9). """,
        validator=discreteTruncate,
        values=arange(100e-9,0.9999999,100e-9)
    )
    # STATus subsystem - commands not implemented
    # SYSTem subsystem - commands partially implemented
    system_version = Instrument.measurement(
        ':SYST:VERS?',
        """ A string parameter for the system SCPI version number. """
    )
    system_error = Instrument.measurement(
        ':SYST:ERR?',
        """ A dictionary parameter of the queried oldest error in the device
            error queue. The error is removed after querying the queue.
            A dictionary of the form:
                {'error_number':<int>,
                'error_description':<str>}
            is returned. """,
        get_process=lambda v:{'error_number':       v[0],
                              'error_description':  v[1]}
    )
    # TRACe subsystem - commands not implemented
    # TRIGger subsystem
    trigger_auto_count_enable = Instrument.control(
        "TRIG:COUN:AUTO?",
        "TRIG:COUNT:AUTO %i",
        """ A boolean parameter for the state of automatic control of the
            number of measurements made per trigger signal. """,
        validator=strict_discrete_set,
        values=(True,False)
    )

    def __init__(self, adapter, **kwargs):
        super(Agilent53131A, self).__init__(adapter,
              "Agilent 53131A Universal Counter", **kwargs)
        self.adapter.connection.timeout = (kwargs.get('timeout', 1) * 1000)
        self.format_data='ascii'
    # SCPI subsystem
    @property
    def abort(self):
        """ A property that causes the device to abort any measurements in
            progress. The command processes as quickly as possible."""
        self.write("ABORT")
    # INITiate subsystem
    @property
    def init(self):
        """ The device immediately initiates a single measurement or a block of
            measurements. """
        self.write("INIT:IMM")
    # CALibration subsystem
#    @calibration_data.getter
#    def calibration_data(self):
#        return self.adapter.ask_values("CAL:DATA?")
    @calibration_security_enable.setter
    def calibration_security_enable(self,value):
        try:
            state, code = value
        except ValueError:
            raise ValueError('The setting must be an iterable with the'
                             'elements: state, security_code.')
        strict_discrete_set(state,(0,1))
        strict_range(code,(0,9999999))
        self.write("CAL:SEC:STAT {}, {}".format(state,code))
    # DISPlay subsystem
    @display_menu_enable.setter
    def display_menu_enable(self,value):
        if value == 0:
            self.write("DISP:MENU:STAT OFF")
    # INPut subsystem
    @input_attenuation.setter
    def input_attenuation(self,value):
        strict_discrete_set(value, (1,10))
        self.write('INP{}:ATT {}'.format(self.channel, value))
    @input_attenuation.getter
    def input_attenuation(self):
        return int(self.ask('INP{}:ATT?'.format(self.channel)))
    @input_coupling.setter
    def input_coupling(self,value):
        strict_discrete_set(value, ('AC','DC'))
        self.write("INP{}:COUP {}".format(self.channel, value))
    @input_coupling.getter
    def input_coupling(self):
        return self.ask("INP{}:COUP?".format(self.channel).strip())
    @input_filter_enable.setter
    def input_filter_enable(self,value):
        strict_discrete_set(value,(True,False))
        self.write('INP{}:FILT:LPAS:STAT {}'.format(self.channel,value))
    @input_filter_enable.getter
    def input_filter_enable(self):
        return bool(self.ask('INP{}:FILT:LPAS:STAT?'.format(self.channel)
                            ).strip())
    @input_filter_frequency.getter
    def input_filter_frequency(self):
        return float(self.ask('INP{}:FILT:LPAS:FREQ?'.format(self.channel)
                              ).strip())
    @input_impedance.setter
    def input_impedance(self,value):
        strict_discrete_set(value,(50,1e6))
        self.write('INP{}:IMP {}'.format(self.channel,value))
    @input_impedance.getter
    def input_impedance(self):
        return float(self.ask('INP{}:IMP?'.format(self.channel)).strip())
    #
    @trigger_relative_hysteresis.setter
    def trigger_relative_hysteresis(self,value):
        truncated_discrete_set(value, (0,50,100))
        self.write('SENS:EVEN{}:HYST:REL {}'.format(self.channel,value))
    @trigger_relative_hysteresis.getter
    def trigger_relative_hysteresis(self):
        _var = self.ask('SENS:EVEN{}:HYST:REL?'.format(self.channel))
        return int(_var.strip().split('+')[-1])
    @trigger_level.setter
    def trigger_level(self,value):
        truncated_range(value, (-5.125, 5.125))
        self.write('SENS:EVEN{}:LEV:ABS {}'.format(self.channel,value))
    @trigger_level.getter
    def trigger_level(self):
        return float(self.ask('SENS:EVEN{}:LEV:ABS?'.format(self.channel)
                              ).strip())
    @trigger_auto_enable.setter
    def trigger_auto_enable(self,value):
        strict_discrete_set(value,(True,False))
        self.write('SENS:EVEN{}:LEV:ABS:AUTO {}'.format(self.channel,value))
    @trigger_auto_enable.getter
    def trigger_auto_enable(self):
        return int(self.ask('SENS:EVEN{}:LEV:ABS:AUTO?'.format(self.channel)
                                                                    ).strip())
    @trigger_auto_level.setter
    def trigger_auto_level(self,value):
        discreteTruncate(value, arange(0, 100, 10))
        self.write('SENS:EVEN{}:LEV:REL {}'.format(self.channel,value))
    @trigger_auto_level.getter
    def trigger_auto_level(self):
        return int(self.ask('SENS:EVEN{}:LEV:REL?'.format(self.channel)
                                                    ).strip().split('+')[-1])
    @trigger_slope_positive.setter
    def trigger_slope_positive(self,value):
        strict_discrete_set(value,(True,False))
        _values={True:'POS', False:'NEG'}
        self.write('SENS:EVEN{}:SLOP {}'.format(self.channel,_values[value]))
    @trigger_slope_positive.getter
    def trigger_slope_positive(self):
        _val = self.ask('SENS:EVEN{}:SLOP?'.format(self.channel)).strip()
        _values={'POS':True, 'NEG':False}
        return _values[_val]
    # convenience functions
    def interval_external_ttl(self):
        """ Configure the time interval measurement for a 5V TTL signal input on
            channel 1. The interval measurement triggers when the voltage of
            the input signal reaches 4V and terminates when the signal voltage
            drops below 2V. """
        self.sense_function='time interval'
        self.reference_source_auto=False
        self.reference_source_external=True
        self.reference_external_check='ON'
        #self.measure_function='interval'
        self.init_continuous=False
        self.sense_common_mode=True
        self.trigger_auto_count_enable=False

        self.channel=1
        self.trigger_relative_hysteresis=50
        self.trigger_auto_enable=False
        self.trigger_auto_level=False
        self.input_impedance=1e6
        self.input_coupling='DC'
        self.trigger_level=4
        self.trigger_slope_positive=True

        self.channel=2
        self.trigger_relative_hysteresis=50
        self.trigger_auto_enable=False
        self.trigger_auto_level=False
        self.input_impedance=1e6
        self.input_coupling='DC'
        self.trigger_level=2
        self.trigger_slope_positive=False

        self.init
