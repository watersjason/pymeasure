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
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, joined_validators, truncated_discrete_set

import time

class Agilent3458A(Instrument):
    """
    Represent the Agilent/Keysight 3458A digital multi-meter.

    .. code-block:: python

        multi_meter = Agilent3458A("GPIB::1::INSTR")   # Esablish the Agilent/Keysight B3458A source measurement device

        multi_meter.device_calibrate                    # Run the self calibtration

        TODO

    """

    ##########
    # Device #
    ##########

    identify = Instrument.measurement(
        "ID?",
        """ Returns the device ID. """
    )
    lock_out = Instrument.command(
        "LOCK?",
        "LOCK %g",
        """ An integer parameter that turns the front panel keyboard `on` or `off`. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    output_format = Instrument.command(
        "OFORMAT?",
        "OFORMAT %g",
        """ A string parameter that sets the multimeter output format. """,
        validator=strict_discrete_set,
        values={'ascii':1,'sint':2,'dint':3,'sreal':4,'dreal':5},
        map_values=True
    )
    options_installed = Instrument.measurement(
        "OPT?",
        """ A string parameter that returns the physically installed options. """,
        validator=strict_discrete_set,
        values={'none':0,'extended_memory':1},
        map_values=True
    )
    preset_state = Instrument.measurement(
        "PRESET?",
        "PRESET %g",
        """ A string parameter which puts the multimeter into an internally defined state. """,
        validator=strict_discrete_set,
        values={'fast':0,'normal':1,'digital':2},
        map_values=True
    )
    query_format = Instrument.command(
        "QFORMAT?",
        "QFORMAT %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={'number':'NUM','normal':'NORM','alpha':'ALPHA'},
        map_values=True
    )
    #TODO RESET
    device_revision = Instrument.measurement(
        "REV?",
        """ A string property with the master and slave processor firmware revisions. """
    )
    # TODO TEST
    # TODO RQS Needs bit mapping feature
    service_request = Instrument.setting(
        "SRQ %g",
        """ An integer parameter that sets the status register bit 2. If bit 2 is enabled to assert the GPIB service request, then it is also set. """,
    ) # TODO service_request validator
    status = Instrument.measurement(
        "STB?",
        """ An integer parameter that represents the bits returned from the status byte query. """
    )
    temperature = Instrument.measurement(
        "TEMP?",
        """ A parameter that represents the internally measured multimeter temperature in degrees Centigrade. """
    )
    terminals = Instrumnet.measurement(
        "TERM?",
        """ A string parameter of `FRONT` or `REAR` that designates which terminals are selected. """
    )

    ###############
    # Calibration #
    ###############

    calibration_external = Instrument.setting(
        "CAL %g",
        """ The value sent with the CAL command must exactly equal the actual output value of the adjustment source. It is recommended that 10V be used for CAL 10 and 10K ohms be used for CAL 10E3.

        Any standard value between 1 V and 12 V or 1k ohms and 12k ohms can be used. A value less than 10 V or less than 10k ohms will introduce additional uncertainty to the multimeter's accuracy specifications. """
    ) #TODO calibration_external validator, needs bit mapping feature
    # TODO CAL?
    calibration_internal = Instrument.setting(
        "ACAL %g",
        """ A string property that instructs the multimeter to perform a specified type of internal self calibration. Calibration security must be removed by :meth:`~Agilent3458A.calibration_secure`. """,
        validator=strict_discrete_set,
        values={'all':0, 'dc':1, 'ac':2, 'resistance':4},
        map_values=True
    )
    calibration_number = Instrument.measurement(
        "CALNUM?",
        """ An integer property indicating the number of times the multimeter has been calibrated. """,
        cast=int
    )
    calibration_string = Instrument.command(
        "CALSTR?",
        "CALSTR %s",
        """ A string property that is stored in the multimeter's nonvolatile calibration RAM. Recommended usage is to store the meter's internal temperature at the time of calibration, the date of calibration, and the scheduled date for the next calibration. """
    )
    calibration_secure = Instrument.setting(
        "SECURE %s",
        """ A string property of the form: `old_code, new_code[, acal_secure]`, where `old_code` is the previous security code, `new_code` is the new security code, and [,acal_secure] is an optional property to turn the autocalibration security `OFF` or `ON`.

        The string `3458,3458,OFF` maintains the default security code but disables the autocalibration security. Disabiling the autocalibration security is required to use :meth:`~Agilent3458A.calibrate_self`. """
    )
    device_temperature = Instrument.measurement(
        "TEMP?",
        """ Returns the internal temperature of the multimeter in degrees C. """
    )

    ###############
    # Measurement #
    ###############

    range_auto = Instrument.command(
        "ARANGE?",
        "ARANGE %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'off':0,'on':1,'once':2},
        map_values=True
    )
    auto_zero = Instrument.command(
        "AZERO?",
        "AZERO %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'off':0,'on':1,'once':2},
        map_values=True
    )
    fix_input_impedance = Instrument.command(
        "FIXEDZ?",
        "FIXEDZ %g",
        """ An integer parameter that turns the fixed input resistance function for DC voltage measurements `on` or `off`. When enabled, the multimeter maintains its input resistance at 10e6 ohms for all ranges. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    integer_scale_factor = Instrument.measurement(
        "ISCALE?",
        """ Returns the scale factor for the internal conversion from the intger (`SINT`, `DINT`) formats to the real (`ASCII`, `SREAL`, `DREAL`) formats. Multiplying the integer values by this factor returns the actual values. """
    )
    line_frequency = Instrument.measurement(
        "LINE?",
        """ Returns the AC line frequency. """
    )
    digits = Instrument.command(
        "NDIG?",
        "NDIG %g",
        """ TODO """,
        validator=strict_discrete_set,
        values=(list(range(3,9,1)))
    )
    nplc = Instrument.command(
        "NPLC?",
        "NPLC %g",
        """ An integer parameter that sets the number of power line cycles over which the A/D converter integrates the input signal. """,
        validator=strict_discrete_set,
        values=(list(range(0,10,1)) + list(range(10,1001,10)))
    )
    offset_compensation_state = Instrument.command(
        "OCOMP?",
        "OCOMP %g",
        """ A string parameter that switches the state of the offset resistance compensation function. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    #TODO RANGE
    measure_ratio_state = Instrument.command(
        "RATIO?",
        "RATIO %g",
        """ A string parameter that instructs the multimeter to measure a DC reference voltage applied to the Sense terminals and a signal voltage applied to the Input terminals. The ratio is calculated as input_resistance / sense_resistance. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    ac_voltage_mode = Instrument.command(
        "SETACV?",
        "SETACV %g",
        """ A string parameter for the AC/AC+DC voltage conversion method. """,
        validator=strict_discrete_set,
        values={"analog":0,"rand_sampling":1,"sync_sampling":2},
        map_values=True
    )
    # TODO tone


    ###############
    # Subsampling #
    ###############

    # TODO subsampling commands
    # TODO SSAC
    # TODO SSDC
    # TODO SSPARM?
    # TODO SSRC
    # TODO SSTATE
    # TODO SUB
    # TODO SUBEND

    ########
    # MATH #
    ########

    # TODO NULL
    # TODO STAT
    math_recall = Instrument.setting(
        "RMATH %g",
        """ A string parameter that recalls and returns the math register contents. """,
        validator=strict_discrete_set,
        values={'degree':1,'lower_bound':2,'max_pfail':3,'mean':4,'min_pfail':5,'number_sample':6,'null_offset':7,'perc':8,'reference_value':9,'reference_impedance':10,'scale_divisor':11,'standard_deviation':12,'upper_bound':13,'number_pfail':15},
        map_values=True
    )
    # TODO SMATH

    #########
    # Error #
    #########

    #TODO EMASK
    #TODO ERR?
    #TODO ERRSTR?

    ##############
    # Triggering #
    ##############

    trigger_delay = Instrument.command(
        "DELAY?",
        "DELAY %g",
        """ TODO """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[[-1,0],[1e-7,6000]]
    )
    trigger_num_readings = Instrument.command(
        "NRDGS?",
        "NRDGS %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'auto':1,'external':2,'sync':5,'timer':6,'level':7,'line':8},
        map_values=True
    )
    # TODO SWEEP
    # TODO TARM
    trigger_buffer_state = Instrument.command(
        "TBUFF?",
        "TBUFF %g",
        """ A boolean parameter to enable or disable the trigger buffer. When enabled, the trigger is buffered to avoid the error: `TRIGGER TOO FAST`. """,
        validator=strict_discrete_set
        values=[False,True],
        map_values={False:0,True:1},
        cast=bool
    )
    # TODO TIMER
    trigger = Instrument.command(
        "TRIG?",
        "TRIG %g",
        """ A string parameter that specifies the trigger control event. """,
        validator=strict_discrete_set,
        values={'auto':1,'external':1,'single':2,'hold':4,'sync':5,'level':6,'line':7},
        map_values=True
    )

    ##########
    # Buffer #
    ##########

    buffer_state = Instrument.control(
        "INBUF?",
        "INBUF %g",
        """ An integer parameter that sets the input buffer `off` or `on`.  """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    buffer_count = Instrument.measurement(
        "MCOUNT?",
        """ Returns the total number of stored readings. """
    )
    memory_state = Instrument.control(
        "MEM?",
        "MEM %g",
        """ Enables or disables reading memory and designates the storage mode. """,
        validator=strict_discrete_set,
        values={'off':0,'lifo':1,'fifo':2,'cont':3},
        map_values=True
    )
    memory_format = Instrument.control(
        "MFORMAT?",
        "MFORMAT %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'ascii':1,'sint':2,'dint':3,'sreal':4,'dreal:5'},
        map_values=True
    )
    # TODO RMEM

    #
    #
    #

    def __init__(self, adapter, **kwargs):
        super(AgilentB2961A, self).__init__(adapter,
        "Agilent 3458A Source-Measurement Unit", includeSCPI=False, **kwargs
        )

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)

    @property
    def error(self):
        """ Reads and removes the top item in the error queue and returns a tuple of an error code and message from the single error. """
        err = self.values(":SYST:ERR?")
        if len(err) < 2:
            err = self.read() # Try reading again
        code = err[0]
        message = err[1].replace('"', '')
        return(code, message)

    @property
    def check_errors(self):
        """ Logs any system errors reported by the instrument. """
        code, message = self.error
        while code != 0:
            t = time.time()
            log.info("Agilent B2961a reported error: %d, %s" % (code, message))
            code, message = self.error
            if (time.time()-t)>10:
                log.warning("Timed out for Agilent B2961a error retrieval.")
