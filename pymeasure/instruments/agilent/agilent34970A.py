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
    _channel = []
    @property
    def channel(self):
        """ A list property specifying the channels that a command is applied.
            Individual channels are of the form: ``scc``, where ``s`` is the
            card slot number (1, 2, 3) and ``cc`` is the channel number on the
            specified card.
        """
        return _channel
    @channel.setter
    def channel(self, channel):
        _channel = channel

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

    #MEMory

    # MMEMory

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

    # SENSe subsystem commands

    # SOURce subsystem commands
    source_dio_word = Instrument.control(
        "SOUR:DIG:DATA:WORD? (@{})".format(channel_digital),
        "SOUR:DIG:DATA:WORD %s,(@{})".format(channel_digital),
        """ An integer parameter representing the 16 bit word that is output
            on `channel_digital`. """
    )
    source_dio_byte = Instrument.control(
        "SOUR:DIG:DATA:BYTE? (@{})".format(channel_digital),
        "SOUR:DIG:DATA:BYTE %g,(@{})".format(channel_digital),
        """ An integer parameter representing the 8 bit byte that is output
            on `channel_digital`. """
    )
    source_dio_state = Instrument.measurement(
        "SOUR:DIG:STAT? (@{})".format(channel_digital),
        """ Returns the status (input or output) of the digital channels
            specified by `channel_digital`. """
    )
    source_dac_voltage = Instrument.control(
        "SOUR:VOLT? (@{})".format(channel_digital),
        "SOUR:VOLT %g,(@{})".format(channel_digital),
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
                                       'alarm number'), v.split(',')))
    )
    card_reset = Instrument.setting(
        "SYST:CPON %s",
        """ Resets the module in the specified slot to its power-on state.
            See manual for Factory Reset State for a complete listing of
            the instrument's Factory configuration. """,
        validator=strict_discrete_set,
        values=(100,200,300,'ALL')
    )
    card_id = Instrument.measurement(
        "SYST:CTYP? %s" % self._channel,
        """ Get the card ID for `channel`. """,
        get_process = lambda v: dict(zip(('manufacturer', 'card model number',
                                          'card serial number',
                                          'firmware revision'), v.split(',')))
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
