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
                                              joined_validators)

class Agilent34970A(Instrument):
    """
    TODO

    .. code-block:: python

        # Establish the Agilent 34970A Data Acquisition/Switch Unit
        daq = Agilent34970A("GPIB::1::INSTR")

        TODO

    """
    # Default parameters for channels and connection types
    _channel = '(@)'
    _channel_digital = '(@)'
    _resistance_connection = 'FRES'
    _rtd_connection = 'FRTD'

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

    # CALibration subsystem commands
    calibration = Instrument.measurement(
        "CAL?",
        """ Perform an internal calibration of the DMM. Returns `True` if
            calibration succeeds. """,
        validator = strict_discrete_set,
        values = {True:0, False:1},
        map_values = True
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

    # DATA subsystem commands
    data_last = Instrument.measurement(
        "DATA:LAST?",
        """ Returns the most recent reading on `channel`. """
    )
    data_length = Instrument.measurement(
        "DATA:POIN?",
        """ A float parameter for the total number
            of readings stored in reading memory. """
    )
    data_length_threshold = Instrument.control(
        "DATA:POIN:EVEN:THR?",
        "DATA:POIN:EVEN:THR %g",
        """ An integer parameter for the number of readings that must be
            collected to set the Standard Operation Register group event. """,
        validator = truncated_range,
        values = (1,50000),
        cast = int
    )
    # skip DATA:REMOVE? command

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

    # IEEE-488 commands
    register_clear = Instrument.setting(
        "*CLS",
        """ Clear the event registers for all register groups. """
    )
    # skip *ESE/*ESE? and ESR?
    power_on_state = Instrument.control(
        "*PSC?",
        "*PSC %g",
        """ A boolean parameter for the state of the power-on status.
            When `True`, the device registers are cleared on power-on. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    # skip *RCL and *SAV
    # skip *SRE and *STB?
    device_test = Instrument.measurement(
        "*TST?",
        """ Run the device test. Returns `True` if 1 or more tests fail. """,
        cast=bool
    )

    # INSTrument subsystem commands
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
        cast=bool,
        set_process=lambda v: v.strip('\n')
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
    channel_scan_list = Instrument.control(
        "ROUT:SCAN?",
        "ROUT:SCAN %s",
        """ An integer, float or list parameter for the
            channels included in the device scan list. """,
        get_process=lambda v:[_i for _i in v.strip('()@')],
        set_process=lambda v:'@('+str([v]).strip('()[]')+')'
    )
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

    # SENSe subsystem commands
    current_ac_bandwidth = Instrument.control(
        "SENS:CURR:AC:BAND?",
        "SENS:CURR:AC:BAND %g,{}".format(_channel),
        """ A string parameter for the AC filter bandwidth speed.
            Values for the bandwidth speed are: `slow`, `medium`, `fast`.

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values={'slow':3,'medium',20,'fast':200},
        map_values=True
    )
    current_ac_range = Instrument.control(
        "SENS:CURR:AC:RANG?",
        "SEMS:CURR:AC:RANG %g",
        """ A string (or list of string) parameters for the AC current range.
            Values for the AC current range are: `min`, `med`, `max`.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values={'min':10e-3,'med':100e-3,'max':1},
        map_values=True
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
    current_ac_resolution = Instruement.measurement(
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
            integration time. Setting the aperature integration time is not
            supported.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """
    )
    current_dc_nplc = Instrument.control(
        "SENS:CURR:DC:NPLC?",
        "SENS:CURR:DC:NPLC %g",
        """ A float (or list of floats) parameter for the DC current
            integration in number of power line cycles. Accepted values are
            in the range: (0.02,0.2,1,2,10,20,100,200).

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            Command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values=(0.02,0.2,1,2,10,20,100,200)
    )
    current_dc_range = Instrument.control(
        "SENS:CURR:DC:RANG?",
        "SENS:CURR:DC:RANG %g",
        """ A string (or list of string) parameters for the DC current range.
            Values for the AC current range are: `min`, `med`, `max`.

            Use with the 34901A multiplexer module (channels 21 & 22 only).

            The command is applied to the preset channel scan list; use
            :param:`~Agilent34970A.channel` to edit the channel list. """,
        validator=strict_discrete_set,
        values={'min':10e-3,'med':100e-3,'max':1},
        map_values=True
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

    voltage_ac_range
    voltage_ac_range_auto
    voltage_ac_bandwidth

    voltage_dc_aperature
    voltage_dc_nplc
    voltage_dc_range
    voltage_dc_range_auto
    voltage_dc_resolution

    resistance_connection
    resistance_aperature
    resistance_nplc
    resistance_compensation
    resistance_range
    resistance_range_auto
    resistance_resolution

    frequency_aperature
    frequency_range_lower
    frequency_voltage_range
    frequency_voltage_range_auto

    period_aperature
    period_voltage_range
    period_voltage_range_auto

    temperature_aperature
    temperature_nplc
    temperature_junction

    temperature_rtd_compensation
    temperature_rtd_reference
    temperatuer_rtd_type

    temperature_tc_check
    temperature_tc_junction
    temperature_tc_junction_type
    temperature_tc_type

    temperature_therm_type

    temperature_transducer_type

    io_read_byte
    io_read_word
    totalize_clear
    totalize_get_data
    totalize_slope
    totalize_start
    totalize_stop
    totalize_type

    sense_function
    sense_zero_auto

    # SOURce subsystem commands
    source_dio_word = Instrument.control(
        "SOUR:DIG:DATA:WORD? (@{})".format(_channel_digital),
        "SOUR:DIG:DATA:WORD %s,(@{})".format(_channel_digital),
        """ An integer parameter representing the 16 bit word that is output
            on `channel_digital`. """
    )
    source_dio_byte = Instrument.control(
        "SOUR:DIG:DATA:BYTE? (@{})".format(_channel_digital),
        "SOUR:DIG:DATA:BYTE %g,(@{})".format(_channel_digital),
        """ An integer parameter representing the 8 bit byte that is output
            on `channel_digital`. """
    )
    source_dio_state = Instrument.measurement(
        "SOUR:DIG:STAT? (@{})".format(_channel_digital),
        """ Returns the status (input or output) of the digital channels
            specified by `channel_digital`. """
    )
    source_dac_voltage = Instrument.control(
        "SOUR:VOLT? (@{})".format(_channel_digital),
        "SOUR:VOLT %g,(@{})".format(_channel_digital),
        """ A float parameter for the output voltage level on the DAC
            specified by `channel_digital`. Each DAC channel is capable of
            outputting -12 V to +12 V (resolution 1 mV) at 10 mA max. """,
        validator = truncated_range,
        values = (-12, 12)
    )

    # STATus subsystem commands
    # TODO: Subsystem replies are a string of length 16. Convert reply string
    #       to a list of integers. Use the list to index the bit definitions.

    # SYSTem subsystem commands
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
    card_reset = Instrument.setting(
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
    # skip lock commands
    system_preset = Instrument.setting(
        "SYST:PRES",
        """ Put the device in preset configuration. """
    )
    # skip security command
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
        self.write('ROUT:SCAN (@)')

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
        return [int(_i) for _i in self._channel.strip('()@')]
    @channel.setter
    def channel(self, channel):
        if isinstance(channel, (int, float)):
            _channel = str(channel)
        elif isinstance(_channel, list):
            for _i in _channel:
                if not isinstance(_i, (int, float)):
                    raise TypeError('The elements in `channel` must be '
                                    'integers or floats.')
            _channel = str(channel).strip('()[]')
        else:
            raise TypeError('The `channel` must be an integer, float, or a '
                            'list of integers and floats.')
        self._channel = '(@' + _channel + ')'
    @property
    def channel_digital(self):
        """ TODO """
        return [int(_i) for _i in self._channel_digital.strip('()@')]
    @channel_digital.setter
    def channel_digital(self, channel):
        if isinstance(channel, (int,float)):
            _channel = str(channel)
        elif isinstance(channel, list):
            for _i in _channel:
                if not isinstance(_i, (int, float)):
                    raise TypeError('The elements in `channel` must be '
                                    'integers or floats.')
            _channel = str(channel).strip('()[]')
        else:
            raise TypeError('The `channel` must be an integer, float, or a '
                            'list of integers and floats.')
        self._channel_digital = '(@' + _channel + ')'

    #
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
        return self.query("CAL:SEC:STAT?")
    @calibration_secure.setter
    def calibration_secure(self,state_code):
        if len(state_code) is not 2:
            raise TypeError('The `state_code` must have a length of 2.')
        self.write("CAL:SEC:STAT {},{}",format(state_code))

    # SYSTem subsystem commands
    @property
    def card_id(self):
        """ Get the card ID for `channel`. """
        try:
            strict_discrete_set(self.channel, (100,200,300))
        except ValueError:
            raise ValueError('Parameter `channel` must be 100, 200, or 300.')
        return self.ask('SYST:CTYP? {}'.format(self.channel)).strip('\n')

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

    # SENSe
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
    def temperature_rtd_connection(self):
        """ A string parameter for the RTD resistance measurement connection.
            Values are: `RTD` for 2 wire connections, or `FRTD` for 4 wires. """
        return self._rtd_connection
    @resistance_connection.setter
    def temperature_rtd_connection(self, connection):
        """ A string parameter for the RTD resistance measurement connection.
            Values are: `RTD` for 2 wire connections, or `FRTD` for 4 wires. """
        strict_discrete_set(connection, ('RTD','FRTD'))
        self._rtd_connection = connection
