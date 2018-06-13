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

    id = Instrument.measurement(
        "ID?",
        """ Returns the device ID. """
    )
    line_frequency = Instrument.measurement(
        "LINE?",
        """ Returns the AC line frequency. """
    )
    lock_out = Instrument.control(
        "LOCK?",
        "LOCK %g",
        """ An integer parameter that turns the front panel keyboard `on` or `off`. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    output_format = Instrument.control(
        "OFORMAT?",
        "OFORMAT %g",
        """ A string parameter that sets the multimeter output format. """,
        validator=strict_discrete_set,
        values={'ascii':1,'sint':2,'dint':3,'sreal':4,'dreal':5},
        map_values=True
    )
    options_installed = Instrument.measurement(
        "OPT?",
        """ A string parameter that returns the physically installed options. """
    )
    preset_state = Instrument.control(
        "PRESET?",
        "PRESET %g",
        """ A string parameter which puts the multimeter into an internally defined state. """,
        validator=strict_discrete_set,
        values={'fast':0,'normal':1,'digital':2},
        map_values=True
    )
    query_format = Instrument.control(
        "QFORMAT?",
        "QFORMAT %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={'number':'NUM','normal':'NORM','alpha':'ALPHA'},
        map_values=True
    )
    revision = Instrument.measurement(
        "REV?",
        """ A string property with the master and slave processor firmware revisions. """
    )
    status_set_condition = Instrument.setting(
        "RQS %g",
        """ Enable a status register condition. """,
        validator=strict_discrete_set,
        values=list(range(1,255,1)),
        cast=int
    )
    status_get_condition = Instrument.measurement(
        "STB?",
        """ An integer parameter that represents the bits returned from the status byte query. """,
        cast=int
    )
    terminals = Instrument.measurement(
        "TERM?",
        """ A string parameter of `FRONT` or `REAR` that designates which terminals are selected. """,
        validator=strict_discrete_set,
        values={'open':0,'front':1,'rear':2},
        cast=int,
        map_values=True
    )
    output_eoi = Instrument.control(
        "END?",
        "END %g",
        """ A string parameter that enables or disables the GPIB End or Identify (EOI) function.

        In ASCII format, each reading output to GPIB that is followed by the EOI (carriage return, line feed) indicates the transmission is done.

        This command controls when the EOI is sent. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1,'always':2},
        map_values=True
    )

    ###############
    # Calibration #
    ###############

    calibration_external = Instrument.setting(
        "CAL %g",
        """ The value sent with the CAL command must exactly equal the actual output value of the adjustment source. It is recommended that 10V be used for CAL 10 and 10K ohms be used for CAL 10E3.

        Any standard value between 1 V and 12 V or 1k ohms and 12k ohms can be used. A value less than 10 V or less than 10k ohms will introduce additional uncertainty to the multimeter's accuracy specifications. """
    )
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
    calibration_string = Instrument.control(
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

    auto_zero = Instrument.control(
        "AZERO?",
        "AZERO %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'off':0,'on':1,'once':2},
        map_values=True
    )
    digits = Instrument.control(
        "NDIG?",
        "NDIG %g",
        """ TODO """,
        validator=strict_discrete_set,
        values=(list(range(3,9,1)))
    )
    fix_input_impedance = Instrument.control(
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
    nplc = Instrument.control(
        "NPLC?",
        "NPLC %g",
        """ An integer parameter that sets the number of power line cycles over which the A/D converter integrates the input signal. """,
        validator=strict_discrete_set,
        values=(list(range(0,10,1)) + list(range(10,1001,10)))
    )
    offset_compensation = Instrument.control(
        "OCOMP?",
        "OCOMP %g",
        """ A string parameter that switches the state of the offset resistance compensation function. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    range_auto = Instrument.control(
        "ARANGE?",
        "ARANGE %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'off':0,'on':1,'once':2},
        map_values=True
    )
    range = Instrument.control(
        "RANGE?",
        "RANGE %g",
        """ TODO """,
    )
    voltage_dc_ratio = Instrument.control(
        "RATIO?",
        "RATIO %g",
        """ A string parameter that instructs the multimeter to measure a DC reference voltage applied to the Sense terminals and a signal voltage applied to the Input terminals. The ratio is calculated as input_resistance / sense_resistance. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    voltage_ac_mode = Instrument.control(
        "SETACV?",
        "SETACV %g",
        """ A string parameter for the AC/AC+DC voltage conversion method. """,
        validator=strict_discrete_set,
        values={"analog":0,"rand_sampling":1,"sync_sampling":2},
        map_values=True
    )

    ########
    # MATH #
    ########

    math_recall = Instrument.measurement(
        "RMATH %g",
        """ Reads the meter memory and returns the value of the requested math operation. """,
        validator=strict_discrete_set,
        values={'degree':1,'lower':2,'max':3,'mean':4,'min':5,'nsamp':6,'offset':7,'perc':8,'ref':9,'res':10,'scale':11,'sdev':12,'upper':13,'pfailnum':15},
        map_values=True
    )

    #########
    # Error #
    #########

    error_mask = Instrument.setting(
        "EMASK %g",
        """ An integer property that creates a user specified error condition. """
    ) # TODO validator with bit array
    error_query = Instrument.setting(
        "ERR?",
        """ An integer property that represents the sum of all device errors. """
    )

    ##############
    # Triggering #
    ##############

    trigger_delay = Instrument.control(
        "DELAY?",
        "DELAY %g",
        """ TODO """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[[-1,0],[1e-7,6000]]
    )
    trigger_n_readings = Instrument.control(
        "NRDGS?",
        "NRDGS %g",
        """ TODO """,
        validator=truncated_range,
        values=(1,16777215),
        cast=int
    )
    trigger_buffer_state = Instrument.control(
        "TBUFF?",
        "TBUFF %g",
        """ A string parameter to enable or disable the trigger buffer. When enabled, the trigger is buffered to avoid the error: `TRIGGER TOO FAST`. """,
        validator=strict_discrete_set,
        values={'off':0,'on':1},
        map_values=True
    )
    trigger_period = Instrument.control(
        "TIMER?",
        "TIMER %g",
        """ An integer property that defines the time interval between readings. """,
        validator=truncated_range,
        values=[2e-5,6000],
        cast=int
    )
    trigger_event = Instrument.control(
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
    memory_count = Instrument.measurement(
        "MCOUNT?",
        """ Returns the total number of stored readings. """,
        cast=int
    )
    memory_state = Instrument.control(
        "MEM?",
        "MEM %g",
        """ Enables or disables reading memory and designates the storage mode. """,
        validator=strict_discrete_set,
        values={'off':0,'lifo':1,'fifo':2,'continue':3},
        map_values=True
    )
    memory_format = Instrument.control(
        "MFORMAT?",
        "MFORMAT %g",
        """ TODO """,
        validator=strict_discrete_set,
        values={'ascii':1,'sint':2,'dint':3,'sreal':4,'dreal':5},
        map_values=True
    )

    def __init__(self, adapter, **kwargs):
        super(Agilent3458A, self).__init__(adapter,
        "Agilent 3458A Source-Measurement Unit", includeSCPI=False, **kwargs
        )

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)

        self.write("END ALWAYS")

    @property
    def reset(self):
        """ TODO """
        self.write('RESET')

    @property
    def tone(self):
        """ Causes the multimeter to beep once. """
        self.write('TONE')

    @property
    def device_test(self):
        """ Perform a series of internal self tests. If a hardware error is detected, the bit 0 in the error register is set by the meter and an error description is set in the auxiliary error register. """
        self.write('TEST')

    @property
    def service_request(self):
        """ An integer parameter that sets the status register bit 2. If bit 2 is enabled to assert the GPIB service request, then it is also set. """
        self.write("SRQ")

    def cal_query(self, constant_id, cal_item):
        """ TODO """
        self.values('CAL? %i,%i' % (constant_id, cal_item))

    @property
    def math_off(self):
        """ Turns off the math functions. """
        self.write('MATH OFF')

    @property
    def math_null(self):
        """ Uses the present value as the null offset value and calculates new output value. """
        self.write('MATH NULL')

    @property
    def math_stat(self):
        """ TODO """
        if self.values("MATH?") == [9,0]:
            self.write("MATH CONT,STAT")
        else:
            self.write("MATH STAT")

    def trigger(self, trigger_event=None, n_trigger_events=None):
        """ TODO """
        events = {'auto':1, 'external':2, 'single':3, 'hold':4, 'syn':5}

        if trigger_event is None and n_trigger_events is None:
            return(self.ask('NRDGS?').strip())
        elif n_trigger_events is none:
            self.write('NRDGS 1, %g' % events[trigger_event])
        else:
            self.write('NRDGS %g, %g' % (events[trigger_event], n_arm_events))

    def trigger_arm(self, arm_event=None, n_arm_events=None):
        """ A string parameter that sets the arm level trigger event. The optional integer parameter `n_arm_events` sets the number of arm events passed to the device. """
        events = {'auto':1, 'external':2, 'single':3, 'hold':4, 'syn':5}

        if arm_event is None and n_arm_events is None:
            return(self.ask('TARM?').strip())
        elif n_arm_events is None:
            self.write('TARM %i' % events[arm_event])
        else:
            self.write('TARM %i, %i' % (events[arm_event], n_arm_events))

    def read_memory_record(self, n_readings=1, start_position=1, record_number=1):
        """ Returns the reading (or group of readings) stored on a record in the device memory.

        """
        eoi = self.output_eoi
        self.output_eoi = 'on'

        val = self.values('RMEM %g, %g, %g' % (start_position, n_readings, record_number))

        self.memory_state = 'continue'
        self.output_eoi = eoi

        return(val)

    @property
    def error(self):
        """ Reads and removes the top item in the error queue and returns a tuple of an error code and message from the single error. """
        err = self.values("ERRSTR?")
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
            log.info("Agilent 3458a reported error: %d, %s" % (code, message))
            code, message = self.error
            if (time.time()-t)>10:
                log.warning("Timed out for Agilent 3458a error retrieval.")
