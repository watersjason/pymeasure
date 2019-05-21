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
                                              joined_validators,
                                              truncated_discrete_set)
from numpy import arange, concatenate
import time

class Agilent3458A(Instrument):
    """
    Represent the Agilent/Keysight 3458A digital multi-meter.

    .. code-block:: python

        dmm = Agilent3458A("GPIB::1::INSTR")
        dmm.digits

        TODO

    """
    # Device
    id = Instrument.measurement(
        "ID?",
        """ Returns the device ID. """
    )
    line_frequency = Instrument.measurement(
        "LINE?",
        """ Returns the AC line frequency. """
    )
    lock_enable = Instrument.control(
        "LOCK?",
        "LOCK %i",
        """ A boolean parameter to enable the front panel key lock. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    output_format = Instrument.control(
        "OFORMAT?",
        "OFORMAT %g",
        """ A string parameter for the multimeter output data format.

            Values:
                ``'ascii'``    ASCII
                ``'sint'``     single integer
                ``'dint'``     double integer
                ``'sreal'``    single real
                ``'dreal'``    double real

            See :attr:`~.Agilent3458A.integer_scale_factor` for the integer to
            real conversion factor.
        """,
        validator=strict_discrete_set,
        values={'ascii':1,
                'sint': 2,
                'dint': 3,
                'sreal':4,
                'dreal':5},
        map_values=True
    )
    options_installed = Instrument.measurement(
        "OPT?",
        """ A string parameter of the physically installed options. """
    )
    preset_state = Instrument.control(
        "PRESET?",
        "PRESET %i",
        """ A string parameter that puts the multimeter into an internally
            defined state.

            Values:
                ``'fast'``      Optimizes device for fast reading and transfer.
                ``'normal'``    Optimizes device for remote operation.
                ``'digital'``   Configures device for DCV digitizing.
        """,
        validator=strict_discrete_set,
        values={'fast':     0,
                'normal':   1,
                'digital':  2},
        map_values=True
    )
    query_format = Instrument.control(
        "QFORMAT?",
        "QFORMAT %s",
        """ A string parameter for the query response format.

            Values:
            ``'number'``    All responses are numeric without headers.
            ``'normal'``    GPIB responses are numeric without headers;
                            display responses are alpha with alpha headers.
            ``'alpha'``     All responses are alpha with alpha headers.
            """,
        validator=strict_discrete_set,
        values={'number':   'NUM',
                'normal':   'NORM',
                'alpha':    'ALPHA'},
        map_values=True
    )
    revision = Instrument.measurement(
        "REV?",
        """ A string property with the master and slave processor firmware
            revisions. """
    )
    request_service = Instrument.setting(
        "RQS %i",
        """ Enable a status register condition. """,
        validator=truncated_discrete_set,
        values=arange(1,255,1,dtype=int),
        cast=int
    )
    status_condition = Instrument.measurement(
        "STB?",
        """ An integer parameter that represents the bits returned from the
            status byte query. """,
        cast=int
    )
    terminals = Instrument.measurement(
        "TERM?",
        """ A string parameter of ``'FRONT'`` or ``'REAR'`` that designates
            which terminals are selected for signal input. """,
        validator=strict_discrete_set,
        values={'open': 0,
                'front':1,
                'rear': 2},
        map_values=True
    )
    output_eoi = Instrument.control(
        "END?",
        "END %i",
        """ A string parameter that controls when the GPIB End or Identify (EOI)
            function is sent.

            In ASCII format, each reading output to GPIB that is followed by the
            EOI (carriage return, line feed) indicates the transmission is done.

            Values:
            ``'off'``       EOI is never set ``True``.
            ``'on'``        For multiple readings, the EOI is set ``True`` when
                            the final reading is set. For a single reading, the
                            EOI is set ``True`` with each reading.
            ``'always'``    EOI is set ``True`` after each reading is sent.
        """,
        validator=strict_discrete_set,
        values={'off':      0,
                'on':       1,
                'always':   2},
        map_values=True
    )
    integer_scale_factor = Instrument.measurement(
        "ISCALE?",
        """ Returns the scale factor for the internal conversion from the
            intger (`SINT`, `DINT`) formats to the
            real (`ASCII`, `SREAL`, `DREAL`) formats. Multiplying the integer
            values by this factor returns the actual values. """
    )
    # Calibration
    calibration_external_dcv = Instrument.setting(
        "CAL %g",
        """ Adjust the internal DC voltage reference against a
            calibrated, 10 V nominal standard DC voltage.
            Connect the voltage standard to the multimeter's
            front panel HI and LO Input terminals. If using a
            Guard wire, set the Guard switch to the Open position.
            If not using a Guard wire, set the Guard switch to
            the the LO position.

            Excecute this command with the exact output voltage of
            the standard. The standard voltage must be between 1 V
            and 12 V, but should be ~ 10 V for highest accuracy.
            """,
        validator=strict_discrete_set,
        values=[1,12]
    )
    calibration_external_resistance = Instrument.setting(
        "CAL %g",
        """ Adjust the internal resistance reference against a
            calibrated, 10k Ohm nominal standard resistance.
            A DCV calibration should be run before calibration
            of the internal resistance standard. Enabling the
            meter offset compensation (:param offset_compensation_enable:)
            is recommended for most applications. Connect the
            standard resistor to the front panel HI and LOW
            Input and HI and LOW Sense terminals. If using a
            Guard wire, set the Guard switch to the Open position.
            If not using a Guard wire, set the Guard switch to
            the the LO position.

            Excecute this command with the exact value of
            the standard. The standard resistor must be between
            1k Ohms and 12k Ohms, but should be ~ 10k Ohms for
            highest accuracy.
            """,
        validator=strict_discrete_set,
        values=[1e3,12e3]
    )
    calibration_autocal = Instrument.setting(
        "ACAL %g",
        """ A string property that instructs the multimeter to perform the
            specified type of internal self calibration. Always perform the
            ``'dcv'`` calibration prior to a ``'acv'`` or ``'ohm'`` calibration.

            Calibration security must not be enabled. Security is disabled by
            :attr:`~.Agilent3458A.calibration_secure`

            Values:
            ``'all'``   Run the ``'dcv'``, ``'acv'`` and ``'ohm'`` calibrations.
            ``'dcv'``   Run the DCV gain and offset calibrations.
            ``'acv'``   Run the ACV flatness, gain and offset calibrations.
            ``'ohm'``   Run the OHM gain and offset calibrations.
        """,
        validator=strict_discrete_set,
        values={'all':0,
                'dcv':1,
                'acv':2,
                'ohm':4},
        map_values=True
    )
    calibration_number = Instrument.measurement(
        "CALNUM?",
        """ An integer property indicating the number of
            times the multimeter has been calibrated. """,
        cast=int
    )
    calibration_string = Instrument.control(
        "CALSTR?",
        "CALSTR %s",
        """ A string property that is stored in the multimeter's
            nonvolatile calibration RAM. Recommended usage is to
            store the meter's internal temperature at the time of
            calibration, the date of calibration, and the
            scheduled date for the next calibration. """
    )
    calibration_secure = Instrument.setting(
        "SECURE %s",
        """ Takes a dictionary with the keys:
            :param old_code:    A required float parameter of the old
                                security code.
            :param new_code:    A required float parameter of the new
                                security code.
            :param acal_state:  An optional string parameter ('ON'|'OFF')
                                to control the security state for the
                                autocalibration.

            The security is disabled when :param new_code: is 0

            An input error results in an empty string sent to
            the device and a device error is raised.

            Disabiling the security is required to use certain
            calibration methods. """,
        set_process=lambda v: ('{old_code},{new_code},{acal_state}'.format(
                                v['old_code'],v['new_code'],v['acal_state'])
                              if len(v)==3 else '{old_code},{new_code}'.format(
                                v['old_code'],v['new_code'])
                              if len(v)==2 else '')
    )
    device_temperature = Instrument.measurement(
        "TEMP?",
        """ Returns the internal temperature of the multimeter in degrees C. """
    )
    # Measurement
    configure_auto_zero = Instrument.control(
        "AZERO?",
        "AZERO %g",
        """ A string parameter for the autozero function.

            Values:
            ``'off'``   The autozero function is not enabled.
            ``'on'``    The autozero function is updated after each measurement.
            ``'once'``  The autozero function is updated once after each
                        function, range, aperature, NPLC or resolution change.
            """,
        validator=strict_discrete_set,
        values={'off':  0,
                'on':   1,
                'once': 2},
        map_values=True
    )
    configure_resolution = Instrument.control(
        "NDIG?",
        "NDIG %i",
        """ An integer parameter, in the range 3 to 9, for the number of digits
            of resolution displayed by the meter. """,
        validator=truncated_discrete_set,
        values=arange(3,9,1,dtype=int),
        cast=int
    )
    configure_fix_impedance = Instrument.control(
        "FIXEDZ?",
        "FIXEDZ %i",
        """ A boolean parameter that enables the fixed input resistance
            function for DC voltage measurements. When ``True``, the multimeter
            maintains am input resistance of 10e6 Ohms for all ranges. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    configure_nplc = Instrument.control(
        "NPLC?",
        "NPLC %g",
        """ An integer parameter that sets the number of power line cycles over
            which the A/D converter integrates the input signal. """,
        validator=strict_discrete_set,
        values=concatenate([arange(0,10,1,dtype=int),
                            arange(10,1001,10,dtype=int)])
    )
    configure_offset_compensation = Instrument.control(
        "OCOMP?",
        "OCOMP %i",
        """ A boolean parameter to enable the offset resistance compensation
            function. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    configure_range_auto = Instrument.control(
        "ARANGE?",
        "ARANGE %g",
        """ A string parameter for the autorange function.

            Values:
            ``'off'``   Disables the autorange function.
            ``'on'``    Enables the autorange function.
            ``'once'``  Enables a single autorange function and then disables
                        the function for future measurements.
            """,
        validator=strict_discrete_set,
        values={'off':  0,
                'on':   1,
                'once': 2},
        map_values=True
    )
    configure_range = Instrument.control(
        "RANGE?",
        "RANGE %g",
        """ A float parameter for the meter measurement range. """
    )
    configure_dc_ratio = Instrument.control(
        "RATIO?",
        "RATIO %i",
        """ A boolean parameter. When ``True``, the meter measures the ratio
            between a DC reference voltage on the Sense terminals and a signal
            voltage on the Input terminals. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    configure_ac_mode = Instrument.control(
        "SETACV?",
        "SETACV %g",
        """ A string parameter for the AC/AC+DC voltage conversion method.

            Values:
            ``'analog'``    Perform an analog RMS conversion.
            ``'rand_s'``    Perform a random sampling conversion.
            ``'sync_s'``    Perform a synchronous sampling conversion.
        """,
        validator=strict_discrete_set,
        values={"analog":0,
                "rand_s":1,
                "sync_s":2},
        map_values=True
    )
    configure_measurement_function = Instrument.control(
        "FUNC?",
        "FUNC %i",
        """ A string parameter for the measurement function. The measurement
            range is configured by :param configure range: or
            :param configure_range_auto: and the measurement resolution is
            configured by :param configure_nplc: or
            :param configure_resolution:.

            Values:
            ``'DCV'``   for DC voltage
            ``'ACV'``   for AC voltage
            ``'ACDCV'`` for AC+DC voltage
            ``'OHM'``   for 2 wire resistance
            ``'OHMF'``  for 4 wire resistance
            ``'DCI'``   for DC current
            ``'ACI'``   for AC current
            ``'ACDCI'`` for AC+DC current
            ``'FREQ'``  for frequency
            ``'PER'``   for period
            ``'DSAC'``  for AC coupled direct sampling
            ``'DSDC'``  for DC coupled direct sampling
            ``'SSAC'``  for AC coupled sub-sampling
            ``'SSDC'``  for DC coupled sub-sampling""",
        validator=strict_discrete_set,
        values={'DCV':  1,
                'ACV':  2,
                'ACDCV':3,
                'OHM':  4,
                'OHMF': 5,
                'DCI':  6,
                'ACI':  7,
                'ACDCI':8,
                'FREQ': 9,
                'PER':  10,
                'DSAC': 11,
                'DSDC': 12,
                'SSAC': 13,
                'SSDC': 14},
        map_values=True,
        get_process=lambda v:v.split(',')[0]
    )
    # MATH
    math_recall = Instrument.measurement(
        "RMATH %g",
        """ Reads the meter memory and returns the value of the requested math
            operation.

            Values:
            ``'degree'``    Time constant for FILTER and RMS.
            ``'lower'``     Smallest value in the STATS register.
            ``'max'``       Upper limit for failure event.
            ``'mean'``      Average value of data in the STATS register.
            ``'min'``       Lower limit for failure event.
            ``'nsamp'``     Number of samples in STATS register.
            ``'offset'``    Value used in NULL and SCALE operations.
            ``'perc'``      Percentage value for PERC operation.
            ``'ref'``       Reference value for DB operation.
            ``'res'``       Reference impedance for DBM operation.
            ``'scale'``     Divisor of the SCALE operation.
            ``'sdev'``      Standard deviation of values in the STATS register.
            ``'upper'``     Largest value in the STATS register.
            ``'pfailnum'``  Number of passed readings before failed read event.
            """,
        validator=strict_discrete_set,
        values={'degree':1,
                'lower':2,
                'max':3,
                'mean':4,
                'min':5,
                'nsamp':6,
                'offset':7,
                'perc':8,
                'ref':9,
                'res':10,
                'scale':11,
                'sdev':12,
                'upper':13,
                'pfailnum':15},
        map_values=True
    )
    # Error
    error_mask = Instrument.setting(
        "EMASK %i",
        """ An integer property that creates a user specified error condition.
        """
    )
    error_query = Instrument.setting(
        "ERR?",
        """ An integer property that represents the sum of all device errors.
        """
    )
    # Triggering
    trigger_delay = Instrument.control(
        "DELAY?",
        "DELAY %g",
        """ A float parameter for time interval that between the trigger event
            and the first sample event """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[[-1,0],[1e-7,6000]]
    )
    trigger_n_readings = Instrument.control(
        "NRDGS?",
        "NRDGS %i",
        """ An integer parameter, between 1 and 16777215, for the number of
            readings taken per trigger and the event (sample event) """,
        validator=truncated_range,
        values=(1,16777215),
        cast=int
    )
    trigger_buffer_enable = Instrument.control(
        "TBUFF?",
        "TBUFF %i",
        """ A boolean parameter to enable the trigger buffer. When enabled, the
            trigger is buffered to avoid the error: ``TRIGGER TOO FAST``. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    trigger_period = Instrument.control(
        "TIMER?",
        "TIMER %g",
        """ A float property that defines the time interval between readings.

            Values:
               min:    2e-5 seconds,
               max:    6000 seconds
        """,
        validator=truncated_range,
        values=[2e-5,6000],
        cast=int
    )
    trigger_event = Instrument.control(
        "TRIG?",
        "TRIG %g",
        """ A string parameter that specifies the trigger control event.

            Values:
            ``'auto'``      Triggers whenever the multimeter is not busy.
            ``'external'``  Triggers on a falling TTL signal on the external
                            trigger connector.
            ``'single'``    Triggers once when signal is BUS recieved.
            ``'hold'``      Disables readings.
            ``'sync'``      Triggers when the multimeter's output buffer is
                            empty, memory is off or empty, and the controller
                            requests data.
            ``'level'``     Triggers when the input signal reaches the
                            voltage specified by the LEVEL command on the
                            slope specified by the SLOPE command.
            ``'line'``      Triggers on a zero crossing of the AC line voltage.
            """,
        validator=strict_discrete_set,
        values={'auto':1,
                'external':1,
                'single':2,
                'hold':4,
                'sync':5,
                'level':6,
                'line':7},
        map_values=True
    )
    # Buffer
    buffer_enable = Instrument.control(
        "INBUF?",
        "INBUF %g",
        """ A boolean parameter to enable the input buffer.  """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    memory_count = Instrument.measurement(
        "MCOUNT?",
        """ Returns the total number of stored readings. """,
        cast=int
    )
    memory_state = Instrument.control(
        "MEM?",
        "MEM %g",
        """ A string parameter for the read memory the storage mode.

            Values:
            ``'off'``   Stops storing readings, but stored reading stay intact.
            ``'lifo'``  Clears reading memory and stores new readings using the
                        LIFO (last-in-first-out) protocol.
            ``'fifo'``  Clears reading memory and stores new readings using the
                        FIFO (first-in-first-out) protocol.
            ``'cont'``  Keeps memory intact and selects previous mode. If
                        there was no previous mode, ``'fifo'`` is selected.
        """,
        validator=strict_discrete_set,
        values={'off':  0,
                'lifo': 1,
                'fifo': 2,
                'cont': 3},
        map_values=True
    )
    memory_format = Instrument.control(
        "MFORMAT?",
        "MFORMAT %g",
        """ Clears reading memory and designates the storage format for new
            readings.

            Values:
            ``'ascii'`` ASCII format with 16 bytes per reading
            ``'sint'``  Single integer-16 bit format with 2 bytes per reading
            ``'dint'``  Double integer-32 bit format with 4 bytes per reading
            ``'sreal'`` Single real-32 bit format with 4 byte per reading
            ``'dreal'`` Double real-64 bit format with 8 bytes per reading
            """,
        validator=strict_discrete_set,
        values={'ascii':1,
                'sint': 2,
                'dint': 3,
                'sreal':4,
                'dreal':5},
        map_values=True
    )

    def __init__(self, adapter, **kwargs):
        super(Agilent3458A, self).__init__(adapter,
        "Agilent 3458A Source-Measurement Unit", includeSCPI=False, **kwargs)
        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)
        self.output_eoi='always'
        self._math_operations= {'off'       :0,
                                'therm 5k c':2,
                                'null'      :9,
                                'pass fail' :11,
                                'stats'     :14,
                                'therm 2k'  :16,
                                'therm 10k' :17,
                                'rtd 85 100':20,
                                'rtd 92 100':21}
        self._inv_math_operat= {v:k for k,v in self._math_operations.items()}
    # Device
    @property
    def reset(self):
        """ Set the multimeter to the power-on state without cycling power. """
        self.write('RESET')
    @property
    def tone(self):
        """ Causes the multimeter to beep once. """
        self.write('TONE')
    @property
    def device_test(self):
        """ Perform a series of internal self tests. If a hardware error is
            detected, the bit 0 in the error register is set by the meter and
            an error description is set in the auxiliary error register. """
        self.write('TEST')
    @property
    def service_request(self):
        """ An integer parameter that sets the status register bit 2. If bit 2
            is enabled to assert the GPIB service request, then it is also set.
        """
        self.write("SRQ")
    # Calibration
    @property
    def calibration_external_offset(self):
        """ Perform a calibration offset adjustment. The adjustment uses
            an external 4-terminal short. After installing the short,
            wait 5 minutes for thermal adjustment.

            The multimeter makes offset measurements and stores constants
            for the DCV, DCI, OHM, and OHMF functions. The constants
            compensate for internal offset errors for the selected
            terminal. The adjustment must be made seperately for the
            front and rear terminals."""
        self.write("CAL 0")
    @property
    def calibration_constants(self):
        """ Return a dictionary with the meter calibration coefficients for the
            internal OHM and DCV references. """
        _c_id={ '40 K Reference':1,
                '7 V Reference': 2}

        _item={ 'nominal value':0,
                'actual value': 1,
                'upper limit':  3,
                'lower limit':  5}

        calibration_values = {}

        for id_key, id_value in _c_id:
            for item_key, item_value in _item:
                calibration_values[id_key][item_key] = self.values(
                                    'CAL? {},{}'.format(id_value, item_value))
        return calibration_values
    # Math
    @property
    def configure_math(self):
        """ Configures the math register operations. If previous operations are
            in effect, then new operation overwrites the secondary operation,
            but keeps the primary operation intact. If no operations are in
            effect, the requested operation is made the primary math operation.

            Values:
            ``'off'``           Disable all previous math operations.
            ``'therm 5k'``      Measure the t / Celsius of a 5 kOhm thermistor.
            ``'null'``          Use the current value as the null value.
            ``'pass fail'``     Compare reading to the PASS/FAIL register.
            ``'stats'``         Enable the collection of the statistical data.
            ``'therm 2k'``      Measure the t / Celsius of a 2 kOhm thermistor.
            ``'therm 10k'``     Measure the t / Celsius of a 10 kOhm thermistor.
            ``'rtd 85 100'``    Measure the t / Celsius of an a=85 100 Ohm PRTD.
            ``'rtd 92 100'``    Measure the t / Celsius of an a=92 100 Ohm PRTD.
        """
        _val = [int(_) for _ in self.values("MATH?")]
        return [self._inv_math_operat[_] for _ in _val]
    @configure_math.setter
    def configure_math(self,operation):

        original_operation = [int(_) for _ in self.values("MATH?")]

        if operation is 'off':
            self.write("MATH 0,0")
        elif original_operation[0] == 0:
            print(1,"MATH {},0".format(self._math_operations[operation]))
            self.write("MATH {},0".format(self._math_operations[operation]))
        else:
            print(2,"MATH {},{}".format(original_operation[0],
                                            self._math_operations[operation]))
            self.write("MATH {},{}".format(original_operation[0],
                                            self._math_operations[operation]))
    # Triggering
    def configure_trigger(self, event, signal=None, n_events=None):
        """ Configures the level event trigger and arm signals.

            :param event:    A string parameter for the `trigger` or
                             or `arm` level event.
            :param signal:   A string parameter for the signal type
                             that initiates the level event. Values are:
                             `auto`, `external`, `single`, `hold` and
                             `syn`.
            :param n_events: An integer parameter that sets the
                             number of level events passed to the
                             device. Defaults to a single level event."""

        signals={'auto':     1,
                 'external': 2,
                 'single':   3,
                 'hold':     4,
                 'syn':      5}

        if event is 'trigger':
            if signal is None and n_events is None:
                return self.ask('NRDGS?').strip()
            elif n_events is None:
                self.write('NRDGS 1, {}'.format(signals[signal]))
            else:
                self.write('NRDGS {}, {}'.format(signals[signal],n_events))
        elif event is 'arm':
            if signal is None and n_events is None:
                return(self.ask('TARM?').strip())
            elif n_events is None:
                self.write('TARM {}'.format(signals[signal]))
            else:
                self.write('TARM {}, {}'.format(signals[signal],n_events))
        else:
            raise ValueError('Input value for event is incorrect.')
    # Buffer
    def read_memory_record(self,readings=1,start=1,record=1):
        """ Returns the reading (or group of readings) stored on a record in
            the device memory."""
        eoi = self.output_eoi
        self.output_eoi = 'on'

        val = self.values('RMEM {}, {}, {}'.format(start,readings,record))

        self.memory_state = 'cont'
        self.output_eoi = eoi
        return(val)
    # Error
    @property
    def error(self):
        """ Reads and removes the top item in the error queue and returns a
            tuple of an error code and message from the single error. """
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
            log.info("Agilent 3458a reported error: {}, {}".format(code,
                                                                   message))
            code, message = self.error
            if (time.time()-t)>10:
                log.warning("Timed out for Agilent 3458a error retrieval.")
