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
                                              truncated_discrete_set,
                                              joined_validators, strict_range)

class Agilent34970A(Instrument):
    """
    TODO

    .. code-block:: python

        # Establish the Agilent 34970A Data Acquisition/Switch Unit
        daq = Agilent34970A("GPIB::1::INSTR")

        TODO

    """
    # Default parameters for channels and connection types
    _channel_io = None
    _resistance_connection = 'FRES'
    _rtd_connection = 'FRTD'

    # CALCulate subsystem commands
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

    # CALibration subsystem commands
    calibration = Instrument.measurement(
        "CAL?",
        """ Perform an internal calibration of the DMM.
            Returns `True` if calibration fails. """,
        cast=int,
        get_process=lambda v:bool(v)
    )
    calibration_count = Instrument.measurement(
        "CAL:COUN?",
        """ A float property for the number
            of times the device was calibrated. """
    )
    calibration_security_code = Instrument.setting(
        "CAL:SEC:CODE %s",
        """ Takes a string of up to 12 characters and sets
            a new calibration security code. The first
            characeter must be a letter (A-Z). Remaining characters
            can be letters, numbers (0-9), or the underscore (_). """
    )
    calibration_string = Instrument.control(
        "CAL:STR?",
        "CAL:STR %s",
        """ A string property. Read or set the calibration string. """
    )
    calibration_value = Instrument.control(
        "CAL:VAL?",
        "CAL:VAL %g",
        """ A float parameter for the value of the calibration
            signal used in the internal DMM calibration. """
    )

    # CONFigure subsystem commands
    # See ...

    # DATA subsystem commands - commands are only partially implemented
    data_last = Instrument.measurement(
        "DATA:LAST?",
        """ Returns the most recent reading on `channel`. """
    ) #TODO test
    data_length = Instrument.measurement(
        "DATA:POIN?",
        """ A float parameter for the total number
            of readings stored in reading memory. """
    ) #TODO test
    data_length_threshold = Instrument.control(
        "DATA:POIN:EVEN:THR?",
        "DATA:POIN:EVEN:THR %g",
        """ An integer parameter for the number of readings that must be
            collected to set the Standard Operation Register group event. """,
        validator = truncated_range,
        values = (1,50000),
        cast = int
    ) #TODO test

    # DIAGnostic subsystem commands
    # Commands for this susbsystem are not implemented.

    # DISPlay subsystem commands
    display_enable = Instrument.control(
        "DISP?",
        "DISP %g",
        """ A boolean parameter for the display state. When `True`,
            the device front panel display is enabled. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    display_message = Instrument.control(
        "DISP:TEXT?",
        "DISP:TEXT %s",
        """ Set or query the 12 character message displayed on the device
            front panel display. The message is truncated at 12 characters. """
    )

    # FORMat subsystem commands
    read_alarm_enable = Instrument.control(
        "FORM:READ:ALAR?",
        "FORM:READ:ALAR %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:bool(v)
    )
    read_channel_enable = Instrument.control(
        "FORM:READ:CHAN?",
        "FORM:READ:CHAN %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:bool(v)
    )
    read_time_enable = Instrument.control(
        "FORM:READ:TIME?",
        "FORM:READ:TIME %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:bool(v)
    )
    read_unit_enable = Instrument.control(
        "FORM:READ:UNIT?",
        "FORM:READ:UNIT %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:bool(v)
    )
    read_time_format = Instrument.control(
        "FORM:READ:TIME:TYPE?",
        "FORM:READ:TIME:TYPE %s",
        """ A string parameter to set/get the time format for devoce timestamps.
            String values are: 'absolute' or 'relative'. The relative format is
            considerably faster than the absolute format
        """,
        validator=strict_discrete_set,
        values={'relative':'REL',
                'absolute':'ABS'},
        map_values=True
    )

    # IEEE-488 commands - commands are only partially implemented
    power_on_clear = Instrument.control(
        "*PSC?",
        "*PSC %g",
        """ A boolean parameter for the state of the power-on status.
            When `True`, the device registers are cleared on power-on. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int,
        get_process=lambda v:bool(v)
    )

    # INSTrument subsystem commands
    dmm_installed = Instrument.measurement(
        "INST:DMM:INST?",
        """ A boolean property for the physically installed DMM. """,
        cast=int,
        get_process=lambda v:bool(v)
    )
    dmm_enable = Instrument.control(
        "INST:DMM?",
        "INST:DMM %i",
        """ A boolean property for the enabled state of the internal DMM. """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:bool(v)
    )

    # LXI subsystem commands
    # Commands not implemented

    # MEASure subsystem commands
    # Commands not implemented. Use CONFigure and IEEE-488 susbsystem commands.

    # MEMory
    # TODO

    # MMEMory
    # TODO

    # ROUTe
    remote_channel = Instrument.control(
        "ROUT:MON?",
        "ROUT:MON %s",
        """ An integer parameter that sets the remote channel
            displayed on the device front panel. """,
        set_process=lambda v: '(@'+str(v)+')',
        get_process=lambda v: int(v.strip(')').split('@')[-1])
    )
    remote_enable = Instrument.control(
        "ROUT:MON:STAT?",
        "ROUT:MON:STAT %i",
        """ A boolean parameter that enables the remote interface. """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:bool(v)
    )
    remote_data = Instrument.measurement(
        "ROUT:DATA?",
        """ Read data from the channel selected by
            :attr:`~.Agilent34970A.remote_channel`. """
    )
    scan_list_size = Instrument.measurement(
        "ROUT:SCAN:SIZE?",
        """ An integer parameter for the total
            number of channels in the scan list. """,
        cast=int
    )
    remote_channel_delay = Instrument.control(
        "ROUT:CHAN:DEL?",
        "ROUT:CHAN:DEL %g",
        """ A float (or a list of float) parameter. The value is the delay
            (in seconds) between multiplexer channels in the scan list. The
            delay can take on values from 0 to 60 seconds with 1 ms resolution.

            List parameters are only supported for getting the channel delay
            values. When setting the channel delay values, a single float
            is applied to all channels set by :param:~`.Agilent34970A.channel`.
        """,
        validator=strict_range,
        values=(0,60)
    )
    remote_channel_delay_auto = Instrument.control(
        "ROUT:CHAN:DEL:AUTO?",
        "ROUT:CHAN:DEL:AUTO %i",
        """ A boolean (or a list of boolean) parameter. When `True`, the
            channel delay is determined by the device using on the function,
            range, integration time, and AC filter settings. """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:(bool(v) if isinstance(v, int) else
                              [bool(_v) for _v in v])
    )
    remote_advance_signal = Instrument.control(
        "ROUT:CHAN:ADV:SOUR?",
        "ROUT:CHAN:ADV:SOUR %s",
        """ A string parameter for the signal source that advances the device
            to the next channel when recieved.

            Options are: 'external' (TTL signal), 'bus' (software signal), or
            'immediate'. Only 'immediate' is allowed when the DMM is enabled by
            :param:~`.Agilent34970A.dmm_enable`. """,
        validator=strict_discrete_set,
        values={'external':'EXT',
                'bus':'BUS',
                'immediate':'IMM'},
        map_values=True
    )
    remote_channel_4_wire = Instrument.control(
        "ROUT:CHAN:FWIR?",
        "ROUT:CHAN:FWIR %i",
        """ A boolean (or a list of boolean) parameter. When `True`, the channel
            is configured for 4-wire measurements and channel 'n' is paired with
            channel 'n'+10 (34901A) or 'n'+8 (34902A). """,
        validator=strict_discrete_set,
        values=(True, False),
        cast=int,
        get_process=lambda v:(bool(v) if isinstance(v, int) else
                              [bool(_v) for _v in v])
    )

    # SENSe subsystem commands
    current_ac_bandwidth = Instrument.control(
        "SENS:CURR:AC:BAND?",
        "SENS:CURR:AC:BAND %g",
        """ A string parameter for the AC filter bandwidth speed.
            Values for the bandwidth speed are: `slow`, `medium`, `fast`.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values={'slow':3,'medium':20,'fast':200},
        map_values=True
    )
    current_ac_range = Instrument.control(
        "SENS:CURR:AC:RANG?",
        "SENS:CURR:AC:RANG %g",
        """ A float (or list of floats) parameters for the AC current range.
            Input values are automatically rounded up to the nearest value in
            the discrete set: (0.01, 0.1, 1) / Amp.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(10e-3,100e-3,1)
    )
    current_ac_range_auto = Instrument.control(
        "SENS:CURR:AC:RANG:AUTO?",
        "SENS:CURR:AC:RANG:AUTO %i",
        """ A boolean (or list of booleans) parameter to enable the AC current
            auto range.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    current_ac_resolution = Instrument.measurement(
        "SENS:CURR:AC:RES?",
        """ Returns a float (or list of floats) parameter for the AC current
            resolution. Setting the resolution is not supported.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """
    )
    current_dc_aperature = Instrument.control(
        "SENS:CURR:DC:APER?",
        "SENS:CURR:DC:APER %g",
        """ A float (or list of floats) parameter for the DC current aperature
            integration time. Values are automatically rounded up to the nearest
            valid value in the range (0.0004, 1) second.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_discrete_set,
        values = [x / 1e6 for x in range(400, 1000004, 4)]
    )
    current_dc_nplc = Instrument.control(
        "SENS:CURR:DC:NPLC?",
        "SENS:CURR:DC:NPLC %g",
        """ A float (or list of floats) parameter for the DC current
            integration in number of power line cycles. Input values are
            automatically rounded up to the nearest value in the range:
            (0.02,0.2,1,2,10,20,100,200).

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(0.02,0.2,1,2,10,20,100,200)
    )
    current_dc_range = Instrument.control(
        "SENS:CURR:DC:RANG?",
        "SENS:CURR:DC:RANG %g",
        """ A float (or list of floats) parameters for the DC current range.
            Input values are automatically rounded up to the nearest value in
            the discrete set: (0.01, 0.1, 1) / Amp.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(10e-3,100e-3,1)
    )
    current_dc_range_auto = Instrument.control(
        "SENS:CURR:DC:RANG:AUTO?",
        "SENS:CURR:DC:RANG:AUTO %i",
        """ A boolean (or list of booleans) parameter to enable the DC current
            auto range.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    current_dc_resolution = Instrument.measurement(
        "SENS:CURR:DC:RES?",
        """ Returns a float (or list of floats) parameter for the DC current
            resolution. Setting the resolution is not supported.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """
    )
    voltage_ac_range =  Instrument.control(
        "SENS:VOLT:AC:RANG?",
        "SENS:VOLT:AC:RANG %g",
        """ A float (or list of floats) parameters for the AC voltage range.
            Input values are automatically rounded up to the nearest value in
            the discrete set: (0.1, 1, 10, 100, 300) / Volt.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(0.1,1,10,100,300)
    )
    voltage_ac_range_auto = Instrument.control(
        "SENS:VOLT:AC:RANG:AUTO?",
        "SENS:VOLT:AC:RANG:AUTO %i",
        """ A boolean (or list of booleans) parameter to enable the AC voltage
            auto range.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    voltage_ac_bandwidth = Instrument.control(
        "SENS:VOLT:AC:BAND?",
        "SENS:VOLT:AC:BAND %g",
        """ A string parameter for the AC filter bandwidth speed.
            Values for the bandwidth speed are: `slow`, `medium`, `fast`.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values={'slow':3,'medium':20,'fast':200},
        map_values=True
    )
    voltage_dc_aperature = Instrument.control(
        "SENS:VOLT:DC:APER?",
        "SENS:VOLT:DC:APER %g",
        """ A float (or list of floats) parameter for the DC voltage aperature
            integration time. Values are automatically rounded up to the nearest
            valid value in the range (0.0003, 1) second.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_discrete_set,
        values = [x / 1e6 for x in range(300, 1000004, 4)]
    )
    voltage_dc_nplc = Instrument.control(
        "SENS:VOLT:DC:NPLC?",
        "SENS:VOLT:DC:NPLC %g",
        """ A float (or list of floats) parameter for the DC voltage
            integration in number of power line cycles. Input values are
            automatically rounded up to the nearest value in the range:
            (0.02,0.2,1,2,10,20,100,200).

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(0.02,0.2,1,2,10,20,100,200)
    )
    voltage_dc_range =  Instrument.control(
        "SENS:VOLT:DC:RANG?",
        "SENS:VOLT:DC:RANG %g",
        """ A float (or list of floats) parameters for the DC voltage range.
            Input values are automatically rounded up to the nearest value in
            the discrete set: (0.1, 1, 10, 100, 300) / Volt.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(0.1,1,10,100,300)
    )
    voltage_dc_range_auto = Instrument.control(
        "SENS:VOLT:DC:RANG:AUTO?",
        "SENS:VOLT:DC:RANG:AUTO %i",
        """ A boolean (or list of booleans) parameter to enable the DC voltage
            auto range.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    voltage_dc_resolution = Instrument.measurement(
        "SENS:VOLT:DC:RES?",
        """ Returns a float (or list of floats) parameter for the DC current
            resolution. Setting the resolution is not supported.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """
    )
    resistance_aperature = Instrument.control(
        "SENS:{}:APER?".format(_resistance_connection),
        "SENS:{}:APER %g".format(_resistance_connection),
        """ A float (or list of floats) parameter for the resistance aperature
            integration time. Values are automatically rounded up to the nearest
            valid value in the range (0.0004, 4) second.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_discrete_set,
        values = [x / 1e6 for x in range(400, 4000004, 4)]
    ) # TODO manual does not provide step size, test values w/ device
    resistance_nplc = Instrument.control(
        "SENS:{}:DC:NPLC?".format(_resistance_connection),
        "SENS:{}:DC:NPLC %g".format(_resistance_connection),
        """ A float (or a list of float) parameter for the resistance
            integration in number of power line cycles. Input values are
            automatically rounded up to the nearest value in the range:
            (0.02,0.2,1,2,10,20,100,200).

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(0.02,0.2,1,2,10,20,100,200)
    )
    resistance_compensation = Instrument.control(
        "SENS:{}:OCOM?".format(_resistance_connection),
        "SENS:{}:OCOM %i".format(_resistance_connection),
        """ A boolean (or a list of boolean) parameter for the resistance
            offset compensation.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = (0,1),
        cast = bool
    )
    resistance_range =  Instrument.control(
        "SENS:{}:RANG?".format(_resistance_connection),
        "SENS:{}:RANG %g".format(_resistance_connection),
        """ A float (or list of floats) parameters for the resistance range.
            Input values are automatically rounded up to the nearest value in
            the discrete set: (1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8) / Ohm.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8)
    )
    resistance_range_auto = Instrument.control(
        "SENS:{}:RANG:AUTO?".format(_resistance_connection),
        "SENS:{}:RANG:AUTO %i".format(_resistance_connection),
        """ A boolean (or list of booleans) parameter to enable the resistance
            auto range.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    resistance_resolution = Instrument.measurement(
        "SENS:{}:RES?".format(_resistance_connection),
        """ Returns a float (or list of floats) parameter for the resistance
            resolution. Setting the resolution is not supported.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """
    )
    frequency_aperature = Instrument.control(
        "SENS:FREQ:APER?",
        "SENS:FREQ:APER %g",
        """ A float (or list of floats) parameter for the frequency aperature
            integration time. Values are automatically rounded up to the nearest
            valid value from the set (0.01, 0.1, 1) second.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_discrete_set,
        values = (0.01,0.1,1)
    )
    frequency_range_lower = Instrument.control(
        "SENS:FREQ:RANG:LOW?",
        "SENS:FREQ:RANG:LOW %i",
        """ An integer (or a list of integer) parameter for the lowest expected
            frequency expected in the input signal.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_range,
        values = (3, 300000),
        cast = int
    )
    frequency_voltage_range = Instrument.control(
        "SENS:FREQ:VOLT:RANG?",
        "SENS:FREQ:VOLT:RANG %g",
        """ A float (or list of floats) parameters for the frequency measurement
            voltage range. Input values are automatically rounded up to the
            nearest value in the discrete set: (0.1, 1, 10, 100, 1000) / Volt.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8)
    )
    frequency_voltage_range_auto = Instrument.control(
        "SENS:FREQ:VOLT:RANG:AUTO?",
        "SENS:FREQ:VOLT:RANG:AUTO %i",
        """ A boolean (or list of booleans) parameter to enable the frequency
            measurement voltage auto range.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    period_aperature = Instrument.control(
        "SENS:PER:APER?",
        "SENS:FREQ:APER %g",
        """ A float (or list of floats) parameter for the period aperature
            integration time. Values are automatically rounded up to the nearest
            valid value from the set (0.01, 0.1, 1) second.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_discrete_set,
        values = (0.01,0.1,1)
    )
    period_voltage_range = Instrument.control(
        "SENS:PER:VOLT:RANG?",
        "SENS:PER:VOLT:RANG %g",
        """ A float (or list of floats) parameters for the period measurement
            voltage range. Input values are automatically rounded up to the
            nearest value in the discrete set: (0.1, 1, 10, 100, 1000) / Volt.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8)
    )
    period_voltage_range_auto = Instrument.control(
        "SENS:PER:VOLT:RANG:AUTO?",
        "SENS:PER:VOLT:RANG:AUTO %i",
        """ A boolean (or list of booleans) parameter to enable the period
            measurement voltage auto range.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(True,False),
        cast=bool
    )
    temperature_aperature = Instrument.control(
        "SENS:TEMP:APER?",
        "SENS:TEMP:APER %g",
        """ A float (or list of floats) parameter for the temperature
            measurement aperature integration time. Values are automatically
            rounded up to the nearest valid value in the range
            (4e-4, 1, 4e-6) second.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = truncated_discrete_set,
        values = [x / 1e6 for x in range(400, 1000004, 4)]
    )
    temperature_nplc = Instrument.control(
        "SENS:TEMP:NPLC?",
        "SENS:TEMP:NPLC %g",
        """ A float (or list of floats) parameter for the temperature
            integration in number of power line cycles. Input values are
            automatically rounded up to the nearest value in the range:
            (0.02,0.2,1,2,10,20,100,200).

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=truncated_discrete_set,
        values=(0.02,0.2,1,2,10,20,100,200)
    )
    temperature_ref_junction = Instrument.measurement(
        "SENS:TEMP:RJUN?",
        """ Returns a float (or a list of float) parameter for the internal
            reference junction temperature on the specified channels. Values
            are always returned in degrees Celsius.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list.
        """
    )
    temperature_rtd_compensation = Instrument.control(
        "SENS:TEMP:TRAN:{}:OCOM?".format(_rtd_connection),
        "SENS:TEMP:TRAN:{}:OCOM %i".format(_rtd_connection),
        """ A boolean (or a list of boolean) parameters for the state of the
            RTD and FRTD (4 wire RTD) resistance measurement offset
            compensation.

            Use with the 34901A, 34902A and 34908A (RTD only) multiplexer
            modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validators = strict_discrete_set,
        values = (0,1),
        cast = bool
    )
    temperature_rtd_reference = Instrument.control(
        "SENS:TEMP:TRAN:{}:RES:REF?".format(_rtd_connection),
        "SENS:TEMP:TRAN:{}:RES:REF %g".format(_rtd_connection),
        """ A float (or a list of float) parameters for the nominal resistance
            (R0 / Ohms) for a RTD or FRTD (4 wire RTD) at 0 degrees Celsius.

            Use with the 34901A, 34902A and 34908A (RTD only) multiplexer
            modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_range,
        values = (49,2100)
    )
    temperature_rtd_type = Instrument.control(
        "TEMP:TRAN:{}:TYPE?".format(_rtd_connection),
        "TEMP:TRAN:{}:TYPE %i".format(_rtd_connection),
        """ An integer (or a list of integer) parameter for the RTD type.
            Supported RTD types are: `85` (a=0.00385) or `91` (a=0.00391).

            Use with the 34901A, 34902A and 34908A (RTD only) multiplexer
            modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = (85,91)
    )
    temperature_tc_check = Instrument.control(
        "SENS:TEMP:TRAN:TC:CHEC?",
        "SENS:TEMP:TRAN:TC:CHEC %i",
        """ A boolean (or a list of boolean) parameter to enable the check
            function for an overload condition in thermocouple temperature
            measurements.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = (0,1),
        cast = bool
    )
    temperature_tc_ref_junction = Instrument.control(
        "SENS:TEMP:TRAN:TC:RJUN?",
        "SENS:TEMP:TRAN:TC:RJUN %g",
        """ A float (or a list of float) parameter for the thermocouple
            fixed reference junction temperature in degrees Celsius.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_range,
        values = (-20, 80)
    )
    temperature_tc_ref_junction_type = Instrument.control(
        "SENS:TEMP:TRAN:TC:RJUN:TYPE?",
        "SENS:TEMP:TRAN:TC:RJUN:TYPE %s",
        """ A string (or a list of string) parameter for the type of reference
            junction temperature used in thermocouple measurements. Values are:
            `internal`, `external`, or `fixed`.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list.  """,
        validator = strict_discrete_set,
        values = {'external':'EXT', 'internal':'INT', 'fixed':'FIX'},
        map_values = True
    )
    temperature_tc_type = Instrument.control(
        "SENS:TEMP:TRAN:TC:TYPE?",
        "SENS:TEMP:TRAN:TC:TYPE %s",
        """ A string (or a list of string) for the thermocouple type. Values
            are in the set: ('B', 'E', 'J', 'K', 'N', 'R', 'S', 'T').

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = ('B','E','J','K','N','R','S','T')
    )
    temperature_thermistor_type = Instrument.control(
        "SENS:TEMP:TRAN:THER:TYPE?",
        "SENS:TEMP:TRAN:THER:TYPE %i",
        """ An integer (or a list of integer) for the thermistor type. Values
            are in the set: (2252, 5000, 10000).

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = (2252, 5000, 10000)
    )
    temperature_transducer_type = Instrument.control(
        "SENS:TEMP:TRAN:TYPE?",
        "SENS:TEMP:TRAN:TYPE %s",
        """ A string (or a list of string) for the temperature probe type.
            Values are in the set: ('TC', 'RTD', 'FRTD', 'Thermistor').

            Use with the 34901A, 34902A and 34908A (RTD & thermistor only)
            multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = ('TC', 'RTD', 'FRTD', 'Thermistor')
    )
    totalize_get_data = Instrument.measurement(
        "SENS:TOT:DATA?",
        """ Immediately read the count data on the specified counter/totalizer
            channel. The maximum count is 2^26-1 and the device automatically
            rolls over to 0 after exceeding the maximum count value.

            Use with the 34907A multifunction module (channel 3 only).

            The channel is set by :param:`~Agilent34970A.channel_digital`. The
            channel number must be `s03`, where `s` is the module location. """
    )
    totalize_slope = Instrument.control(
        "SENS:TOT:SLOP?",
        "SENS:TOT:SLOP %s",
        """ A string (or a list of string) parameters that specifies the
            polarity of the totalizer input signal slope.

            Use with the 34907A multifunction module (channel 3 only).

            The channel is set by :param:`~Agilent34970A.channel_digital`. The
            channel number must be `s03`, where `s` is the module location. """,
        validator = strict_discrete_set,
        values = {'positive':'POS', 'negative':'NEG'},
        map_values = True
    )
    totalize_type = Instrument.control(
        "SENS:TOT:TYPE?",
        "SENS:TOT:TYPE %s",
        """ A string (or a list of string) paramter for the totalizer channel
            mode. Values are: `continue` (read the count without reseting the
            measurement) and `reset` (read the count and reset the measurement).

            Use with the 34907A multifunction module (channel 3 only).

            The channel is set by :param:`~Agilent34970A.channel_digital`. The
            channel number must be `s03`, where `s` is the module location. """,
        validator = strict_discrete_set,
        values = {'continue':'READ', 'reset':'RRES'},
        map_values = True
    )
    sense_function = Instrument.control(
        "SENS:FUNC?",
        "SENS:FUNC %s",
        """ A string (or a list of string) parameters for the
            measurement functions on the channels.

            Use with the 34901A, 34902A and 34908A multiplexer modules.

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator = strict_discrete_set,
        values = ('TEMP','VOLT','VOLT:AC','RES',
                  'FRES','CURR','CURR:AC','FREQ','PER'),
        get_process = lambda v: v.strip('"'),
        set_process = lambda v: '"'+v+'"'
    )
    sense_zero_auto = Instrument.control(
        "SENS:ZERO:AUTO?",
        "SENS:ZERO:AUTO %s",
        """ A string (or a list of string) parameters for the device autozero
            mode.

            The channel is set by :param:`~Agilent34970A.channel`. The
            channel number must be `sxx`, where `s` is the module location and
            `xx` is the location on the module. """,
        validator = strict_discrete_set,
        values = {'off':'OFF', 'once':'ONCE', 'on':'ON', 'on':1, 'off':0},
        map_values = True
    )

    # STATus subsystem commands
    # TODO: Subsystem replies are a string of length 16. Convert reply string
    #       to a list of integers. Use the list to index the bit definitions.

    # SYSTem subsystem commands - commands are only partially implemented
    system_alarm = Instrument.measurement(
        "SYST:ALAR?",
        """ Read the alarm data from the alarm queue. Returns a dictionary with
            the keys: `reading`, `yyyy`(year), `mm`(month), `dd`(day),
            `hh`(hour), `mm`(minute), `ss`(second),
            `channel number`(3 digit int), `alarm threshold`(int; 0:no alarm,
            1: LO, 2: HI), and `alarm number`(int, range:1-4). """,
        get_process=lambda v:dict(zip(('reading','yyyy','mm','dd','hh','mm',
                                       'ss','channel number','alarm threshold',
                                       'alarm number'), v))
    )
    system_card_reset = Instrument.setting(
        "SYST:CPON %s",
        """ Resets the module in the specified slot to its power-on state.
            See manual for Factory Reset State for a complete listing of
            the instrument's Factory configuration. """,
        validator=strict_discrete_set,
        values=(100,200,300,'ALL')
    )
    system_date = Instrument.control(
        "SYST:DATE?",
        "SYST:DATE %s",
        """ A numeric list for the date with the format: `(yyyy, mm, dd)`. """
    )
    system_error = Instrument.measurement(
        "SYST:ERR?",
        """ Query, read and remove one error from the error queue. Errors are
            queried using the first-in-first-out protocol. """
    )
    system_remote_interface = Instrument.control(
        "SYST:INT?",
        "SYST:INT %s",
        """ A string parameter for the device remote interface protocol. """,
        validator = strict_discrete_set,
        values = ('GPIB','RS232')
    )
    system_command_set = Instrument.control(
        "SYST:LANG?",
        "SYST:LANG %s",
        """ A string parameter that specifies whether the instrument behaves as
            a `34970A` or `34972A`. """,
        validator = strict_discrete_set,
        values = ('34970A', '34972A')
    )
    system_line_frequency = Instrument.measurement(
        "SYST:LFR?",
        """ Query the current power-line reference frequency used by the
            device. This value is used to determine the integration time. """
    )
    system_control_mode = Instrument.setting(
        "SYST:%s",
        """ A string parameter that puts the device in local mode (`local`),
            remote mode (`remote`), or local-lockout mode (`lockout`) """,
        validator = strict_discrete_set,
        values = {'local':  'LOC',
                  'remote': 'REM',
                  'lockout':'RWL'},
        set_process = lambda v: v.casefold()
    )
    system_preset = Instrument.setting(
        "SYST:PRES",
        """ Put the device in preset configuration. """
    )
    system_time = Instrument.control(
        "SYST:TIME?",
        "SYST:TIME %s",
        """ A numeric list for the device time stamp. The list values are:
            (`hh`, `mm`, `ss.sss`). """
    )
    scan_time = Instrument.measurement(
        "SYST:TIME:SCAN?",
        """ Returns a numeric list representing the time at the start of a
            measurement scan. The list format is (`yyyy`, `mm`, `dd`, `hh`,
            `mm`, `ss.sss`). """
    )
    system_version = Instrument.measurement(
        "SYST:VERS?",
        """ Returns a string with the version of the device SCPI standard. """
    )

    # TRIGger subsystem commands
    trigger_count = Instrument.control(
        "TRIG:COUN?",
        "TRIG:COUNT %s",
        """ TODO """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[1,50000],['MIN','MAX','INF']]
    )
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

    def __init__(self, adapter, **kwargs):
        super(Agilent34970A, self).__init__(adapter,
              "Agilent 34970A DAQ/Switch Unit", **kwargs)
        self.adapter.connection.timeout = 5000

    #
    @property
    def timeout(self):
        return self.adapter.connection.timeout
    @timeout.setter
    def timeout(self, milliseconds):
        self.adapter.connection.timeout = milliseconds

    # Channel lists
    @property
    def channel(self):
        """ An integer, float, or list of int/float specifying the channels
            that a command is applied. Individual channels are of the form:
            `scc`, where `s` is the card slot number (1, 2, or 3) and `cc` is
            the channel number on the specified card. """
        _channel = self.ask('ROUT:SCAN?').split('(')[-1].strip('@)\n')
        _channel = _channel.split(',')

        if self._channel == ['']:
            raise AttributeError('The `channel` is not set.')
        elif len(self._channel) == 1:
            self._channel = int(self._channel[0])
        else:
            self._channel = [int(_i) for _i in self._channel]
        return _channel
    @channel.setter
    def channel(self, channel):
        if channel is None:
            self.write('ROUT:SCAN (@)')
        elif isinstance(channel, (int, float)):
            self.write('ROUT:SCAN (@{})'.format(channel))
        elif isinstance(channel, (list, tuple)):
            for _i in channel:
                if not isinstance(_i, (int, float)):
                    raise TypeError('Elements in `channel` must be int/float.')
            _cmd = 'ROUT:SCAN (@ {})'.format(channel)
            _cmd = _cmd.replace('(@ (', '(@ ').replace('))', ')')
            self.write(_cmd)
        else:
            raise TypeError('The `channel` must be an integer, float, or a '
                            'list of integers and floats.')
    @property
    def channel_io(self):
        """ The device channel for IO processes. """
        if self._channel_io is None:
            raise ValueError('The `channel_io` is not set; values '
                             'must be set before they can be get. ')
        else:
            return self._channel_io
    @channel_io.setter
    def channel_io(self, channel):
        if isinstance(channel, (int,float,list,tuple)):
            self._channel_io = channel
        else:
            raise ValueError('The `channel` must be an int, float,'
                             ' or a list/tuple of int and float.')

    # General device commands
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

    # CALibration
    @property
    def calibration_secure(self):
        """ Unsecures or secures the instrument for calibration. This feature
            requires you to provide a security code to prevent accidental or
            unauthorized calibrations of the instrument.

            Args
            ----
            state_code -    An iterable, of len 2. Element 1: the new security
                            state (0, 1); element 2: the security code.
            """
        return bool(int(self.ask("CAL:SEC:STAT?")))
    @calibration_secure.setter
    def calibration_secure(self,state_code):
        if len(state_code) is not 2:
            raise TypeError('The `state_code` must have a length of 2.')
        strict_discrete_set(state_code[0], (True,False))
        self.write("CAL:SEC:STAT {0:d}, {1}".format(*state_code))

    # SYSTem subsystem commands
    @property
    def system_card_identify(self):
        """ Returns a tuple with the ordered ID strings for
            the cards in the device slots 100, 200, and 300. """
        _val = []
        _val.append(self.ask('SYST:CTYP? 100').strip('\n'))
        _val.append(self.ask('SYST:CTYP? 200').strip('\n'))
        _val.append(self.ask('SYST:CTYP? 300').strip('\n'))
        return tuple(_val)

    # CONFigure subsystem commands
    @property
    def configure(self):
        """ Returns the present measurement configuration for `channel`. """
        _val = self.ask("CONF? (@{})".format(self.channel)).strip('\n')

    # DISPlay subsystem commands
    @property
    def display_message_clear(self):
        """ Clear the display message. """
        self.write('DISP:TEXT:CLE')

    # IEEE-488 commands
    @property
    def register_clear(self):
        """ Clear the event registers for all register groups. """
        self.write("*CLS")
    @property
    def device_test(self):
        """ Run the device test. If none of the tests fail, return `True`. """
        _timeout = self.timeout
        self.timeout = 60000
        _reply = not(bool(int(self.ask("*TST?"))))
        self.timeout = _timeout
        return _reply
    @property
    def operation_complete(self):
        """ Start the operation completion status engine. """
        self.write('*OPC')
    @property
    def operation_status(self):
        """ Query the operation completion status engine. Returns
            `True` when the current operation is complete. """
        _status = 0
        _count = 0
        while not _status:
            try:
                _status = int(self.query('*OPC'))
            except VisaIOError:
                if _count > 25:
                    raise VisaIOError('Current operation was never completed.')
    @property
    def reset_to_factory_state(self):
        """ Reset the device to the default factory configuration. """
        self.write('*RST')
    @property
    def trigger(self):
        """ Send the BUS trigger signal. Device must be pre-configured to
            recieve the signal over the BUS by :attr:~`trigger_source`. """
        self.write('*TRG')
    @property
    def wait_for_completion(self):
        """ Force the device to wait for all pending operations to complete. """
        self.write('*WAI')

    # SENSe subsystem commands
    @property
    def resistance_connection(self):
        """ A string parameter for the resistance measurement connection type.
            Values are: `RES` for 2 wire connections, or `FRES` for 4 wires. """
        return self._resistance_connection
    @resistance_connection.setter
    def resistance_connection(self, connection):
        """ A string parameter for the resistance measurement connection type.
            Values are: `RES` for 2 wire connections, or `FRES` for 4 wires. """
        strict_discrete_set(connection, ('RES','FRES'))
        self._resistance_connection = connection
    @property
    def temperature_connection(self):
        """ A string parameter for the RTD resistance measurement connection.
            Values are: `RTD` for 2 wire connections, or `FRTD` for 4 wires. """
        return self._rtd_connection
    @resistance_connection.setter
    def temperature_connection(self, connection):
        """ A string parameter for the RTD resistance measurement connection.
            Values are: `RTD` for 2 wire connections, or `FRTD` for 4 wires. """
        strict_discrete_set(connection, ('RTD','FRTD'))
        self._rtd_connection = connection
    @property
    def totalize_clear(self):
        """ Immediately clear the count on the specified counter/totalizer
            channel.

            Use with the 34907A multifunction module (channel 3 only).

            The channel is set by :param:`~Agilent34970A.channel_digital`. The
            channel number must be `s03`, where `s` is the module location. """
        self.write("SENS:TOT:CLE:IMM")
    @property
    def totalize_start(self):
        """Immediately start the count on the specified counter/totalizer
            channel.

            Use with the 34907A multifunction module (channel 3 only).

            The channel is set by :param:`~Agilent34970A.channel_digital`. The
            channel number must be `s03`, where `s` is the module location. """
        self.write("SENS:TOT:STAR:IMM")
    @property
    def totalize_stop(self):
        """Immediately stop the count on the specified counter/totalizer
            channel.

            Use with the 34907A multifunction module (channel 3 only).

            The channel is set by :param:`~Agilent34970A.channel_digital`. The
            channel number must be `s03`, where `s` is the module location. """
        self.write("SENS:TOT:STOP:IMM")

    # SOURce subsystem commands
    @property
    def io_word(self):
        """
        An integer parameter representing the 16 bit word read from or written
        to `channel_io`.
        """
        _channel = str(self.channel_io).strip('()[]')
        if _channel[-1] == '1':
            return int(self.ask("SOUR:DIG:DATA:WORD? (@{})".format(_channel)))
        else:
            raise ValueError('IO words can only be read from channel `x01`. '
                             'Use `io_byte` to read from other channels.')
    @io_word.setter
    def io_word(self, word):
        strict_range(word, (0,65535))
        _channel = str(self.channel_io).strip('()[]')
        if _channel[-1] == '1':
            self.write("SOUR:DIG:DATA:WORD {}, (@{})".format(word, _channel))
        else:
            raise ValueError('IO words can only be written to channel `x01`. '
                             'Use `io_byte` to write to other channels.')
    @property
    def io_byte(self):
        """
        An integer (or a list of integer) parameter representing the 8 bit byte
        read from or written to `channel_io`.
        """
        _channel = str(self.channel_io).strip('()[]')
        _val = self.ask("SOUR:DIG:DATA:BYTE? (@{})".format(_channel)).split(',')
        _val = tuple([int(_v) for _v in _val])
        if len(_val) == 1:
            return _val[0]
        else:
            return _val
    @io_byte.setter
    def io_byte(self, byte):
        strict_range(byte, (0,255))
        _channel = str(self.channel_io).strip('()[]')
        self.write("SOUR:DIG:DATA:BYTE {}, (@{})".format(byte, _channel))
    @property
    def io_state(self):
        """ Returns the state ('input' or 'output') of the digital channels
            specified by `channel_io`. """
        _channel = str(self.channel_io).strip('()[]')
        _val = self.ask("SOUR:DIG:STAT? (@{})".format(_channel)).split(',')
        _val = tuple(['output' if int(_v) else 'input' for _v in _val])
        if len(_val) == 1:
            return _val[0]
        else:
            return _val
    @property
    def dac_voltage(self):
        """ A float parameter for the output voltage level on the DAC
            specified by `channel_io`. Each DAC channel is capable of
            outputting -12 V to +12 V (resolution 1 mV) at 10 mA max. """
        _channel = str(self.channel_io).strip('()[]')
        _val = self.ask("SOUR:VOLT? (@{})".format(_channel)).split(',')
        if len(_val) == 1:
            return float(_val[0])
        else:
            return tuple([float(_v) for _v in _val])
    @dac_voltage.setter
    def dac_voltage(self, voltage):
        truncated_range(voltage, (-12, 12))
        _channel = _channel = str(self.channel_io).strip('()[]')
        self.write("SOUR:VOLT {}, (@{})".format(voltage, _channel))
