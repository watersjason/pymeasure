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
from pymeasure.instruments.validators import truncated_range, strict_discrete_set, joined_validators

class AgilentB2961A(Instrument):
    """
    Represent the HP/Agilent/Keysight B2961A (with the ultra-low-noise option) source measurement units.

    .. code-block:: python

        source_measure_unit = AgilentB2900A("GPIB::1::INSTR")   # Esablish the HP/Agilent/Kesight B2900A source measurement device
        source_measure_unit.apply_current()                     # Set up to source current
        source_measure_unit.source_current_range = 10e-3        # Set the source current range to 10 mA
        source_measure_unit.compliance_voltage = 10             # Set the source compliance voltage to 10 V
        source_measure_unit.source_current = 0                  # Set the source current to 0 mA
        source_measure_unit.enable_source()                     # Enable the source output
        source_measure_unit.measure_voltage()                   # Set up to measure voltages
        source_measure_unit.ramp_to_current(5e-3)               # Ramp the current to 5 mA
        print(source_measure_unit.voltage)                      # print the measured voltage in voltages
        source_measure_unit.shutdown()                          # Ramp the current to 0 mA and diable output

    """

    source_mode = Instrument.control(
        ":SOUR:FUNC:MODE?",
        ":SOUR:FUNC:MODE %s",
        """ A string property that controls the source mode, which can take the values 'current' or 'voltage'. The convenience methods :meth:`~.AglientB2900A.apply_current` and :meth:`~.AgilentB2900A.apply_voltage` can also be used. This will not enable source output. """,
        validator=strict_discrete_set,
        values={'current':'CURR', 'voltage':'VOLT'},
        map_values=True
    )
    source_enable = Instrument.control(
        ":OUTP:STAT?",
        ":OUTP %i",
        """  """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    source_float = Instrument.control(
        ":OUTP:LOW?",
        ":OUTP:STAT 0;:OUTP:LOW %s",
        """ A string property that selects the state of the low terminal. Sets the disables the source output when called to set the terminal state. """,
        validator=strict_discrete_set,
        values={"float":"FLO", "ground":"GRO"}
        map_values=True
    )

     ###########
     # Current #
     ###########

    current = Instrument.measurement(
        ":MEAS:CURR?",
        """ Returns the measured current in Amps. """
    )
    current_range = Instrument.control(
        ":SENS:CURR:RANG?",
        ":SENS:CURR:RANG:AUTO 0;:SENS:CURR:RANG %g",
        """ A floating point property that controls the measurement current range in Amps, which can take values between -105e-3 and +105e-3 A. Auto-range is disabled when this property is set. """,
        validator=truncated_range,
        values=[-105e-3,105e-3]
    ) # TODO This times out
    current_auto_range = Instrument.control(
        ":SENS:CURR:RANG:AUTO?",
        ":SENS:CURR:RANG:AUTO %i",
        """ An integer property that disables (0) or enables (1) the source current auto-range. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    current_nplc = Instrument.control(
        ":SENS:CURR:NPLC?",
        ":SENS:CURR:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). Values outside of these ranges are automatically trucated. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    compliance_current = Instrument.control(
        ":SENS:CURR:PROT:LEV?",
        ":SENS:CURR:PROT:LEV %g",
        """ A floating point property that controls the complaince current in Amps. """,
        validator=truncated_range,
        values=[-105e-3,105e-3]
    ) # TODO validate
    source_current = Instrument.control(
        ":SOUR:CURR?",
        ":SOUR:CURR:LEV %g",
        """ A floating point property that controls the source current in Amps. """
    )

    ###########
    # VOLTAGE #
    ###########

    voltage = Instrument.measurement(
        ":MEAS:VOLT?",
        """ Returns the measured voltage in Volts. """
    )
    voltage_range = Instrument.control(
        ":SENS:VOLT:RANG?",
        ":SENS:VOLT:RANG:AUTO 0;:SENS:VOLT:RANG %g",
        """ A floating point property that controls the measurement voltage range in Volts, which can take values from -42 to 42 V. Auto-range is disabled when this property is set. """,
        validator=truncated_range,
        values=[-42,42]
    ) # TODO This times out
    voltage_auto_range = Instrument.control(
        ":SENS:VOLT:RANG:AUTO:MODE?",
        ":SENS:VOLT:RANG:AUTO 1;:SENS:VOLT:RANG:AUTO:MODE %s",
        """ A string property to set the auto range mode for voltage measurements. Input options are: `NORM`, `RES` and `SPE`. The channel automatically sets the range """,
        validator=strict_discrete_set,
        values=('NORM','RES','SPE')
    ) # TODO function does not work
    voltage_nplc = Instrument.control(
        ":SENS:VOLT:NPLC?",
        ":SENS:VOLT:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). Values outside of these ranges are automatically trucated. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    compliance_voltage = Instrument.control(
        ":SENS:VOLT:PROT?",
        ":SENS:VOLT:PROT %g",
        """ A floating point property that controls the compliance voltage in Volts. """,
        validator=truncated_range,
        values=[-42, 42]
    )
    source_voltage = Instrument.control(
        ":SOUR:VOLT?",
        ":SOUR:VOLT:LEV %g",
        """ A floating point property that controls the source voltage in Volts. """,
        validator=truncated_range,
        values=[-42,42]
    )
    source_voltage_range = Instrument.control(
        ":SOUR:VOLT:RANG?",
        ":SOUR:VOLT:RANG:AUTO 0;:SOUR:VOLT:RANG %g",
        """ A floating point property that controls the source voltage range in Volts, which can take values from -42 to 42 V. Auto-range is disabled when this property is set. """,
        validator=truncated_range,
        values=[-42, 42]
    )

    ##############
    # Resistance #
    ##############

    resistance = Instrument.measurement(
        ":MEAS:RES?",
        """ Reads the resistance in Ohms. """
    )
    resistance_range = Instrument.control(
        ":SENS:RES:RANG?",
        ":SENS:RES:RANG:AUTO 0;:SENS:RES:RANG %g",
        """ A floating point property that controls the resistance range in Ohms, which can take values from 0 to 210 MOhms. Auto-range is disabled when this property is set. """,
        validator=truncated_range,
        values=[0, 210e6]
    ) #TODO update values in doc str and values list
    resistance_auto_range = Instrument.control(
        ":SENS:RES:RANG:AUTO?",
        ":SENS:RES:RANG:AUTO %i",
        """ A property that controls the auto-range setting for the resistance measurement. Accepts input of 0 (disable) or 1 (enable auto-range). """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    resistance_nplc = Instrument.control(
        ":SENS:RES:NPLC?",
        ":SENS:RES:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). Values outside of these ranges are automatically trucated. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    resistance_connection = Instrument.control(
        ":SENS:REM?",
        ":SENS:REM %d",
        """ A string property that controls the number of wires used in resistance meaasurments. Accepts a value of `1` for the Kelvin (4 wire) connection or `0` for the standard (2 wire) connection. """,
        validator=strict_discrete_set,
        values={0,1}
    )

    ################
    # Buffer Trace #
    ################

    buffer_points = Instrument.control(
        ":TRAC:POIN?",
        ":TRAC:POIN %d",
        """ An integer property that controls the number of buffer points ALLOWED in the instrument trace. This does not represent the actual number of points stored in the buffer, but is instead the configuration value. Accepts values from 1 to 100000. Values outside of these ranges are automatically trucated to the nearest allowed value. """,
        validator=truncated_range,
        values=[1, 100000],
        cast=int
    )

    #
    #
    #

    def __init__(self, adapter, **kwargs):
        super(AgilentB2961A, self).__init__(adapter, "Agilent B2961A Source-Measurement Unit", **kwargs)

    def enable_source(self):
        """ Enables the source output. Depending on the instrument configuration, the source output is VOLT|CURR. """
        self.source_enable(1)

    def disable_source(self):
        """ Disables the source output. """
        self.source_enable(0)

    def measure_resistance(self, nplc=10, resistance=2.1e5, auto_range=True, kelvin_connection=True):
        """" Configures the measurement of resistance.

        :param nplc: Number of power line cycles (NPLC) to integrate over; from 0.0004 to 100.
        :param resistance: Upper limit of resistance in Ohms; from 0 MOhm to 210 MOhm. This value is ignored when :param auto_range: is True.
        :param autorange: Enables auto_range of meter when True, else the upper limit is controlled by the value of :param resistance:.
        :param kelvin_connection: Enables the 4-wire Kelvin resistance measurement. """"
        log.info("%s is measuring resistance." % self.name)
        self.write(":SENS:FUNC RES;:SENS:RES:MODE MAN;:FORM:ELEM:SENS RES")
        self.resistance_nplc(nplc)
        if auto_range:
            self.resistance_auto_range(1)
        else:
            self.resistance_range = resistance
        if kelvin_connection:
            self.resistance_connection(1)
        else:
            self.resistance_connection(0)
        self.check_errors()

    def measure_voltage(self, nplc=10, voltage=42, auto_range=True):
        """ Configures the measurement of voltage.

        :param nplc: Number of power line cycles (NPLC) to integrate over; from 0.0004 to 100.
        :param voltage: Upper limit of voltage in Volts; from -42 V to 42 V. This value is ignored when :param auto_range: is True.
        :param autorange: Enables auto_range of meter when True, else the upper limit is controlled by the value of :param voltage:. """
        log.info("%s is measuring voltage." % self.name)
        self.write(":SENS:FUNC VOLT;:FORM:ELEM:SENS VOLT")
        self.voltage_nplc(nplc)
        if auto_range:
            self.voltage_auto_range("NORM")
        else:
            self.voltage_range = voltage
        self.check_errors()

    def measure_current(self, nplc=10, current=10e-3, auto_range=True):
        """ Configures the measurement of current.

        :param nplc: Number of power line cycles (NPLC) from 0.0004 to 100.
        :param current: Upper limit of current in Amps, from -105e-3 A and +105e-3 A.
        :param auto_range: Enables auto_range if True, else uses the value set by :param current:. """
        log.info("%s is measuring current." % self.name)
        self.write(":SENS:FUNC 'CURR';:FORM:ELEM CURR")
        self.current_nplc(nplc)
        if auto_range:
            self.current_auto_range(1)
        else:
            self.current_range(current)
        self.check_errors()

    def auto_range_source(self):
        """ Configures the source to use the automatic range. """
        if self.source_mode == 'current':
            self.write(":SOUR:CURR:RANG:AUTO 1")
        else:
            self.write(":SOUR:VOLT:RANG:AUTO 1")

    def apply_current(self, current_range=None, compliance_voltage=1):
        """ Configures the instrument to apply a souce current and uses and auto-range unless a current range is specified. The compliance voltage is also set.

        :param compliance_voltage: A float in the correct range for a :attr:`~.AgilentB2961A.compliance_voltage`.
        :param current_range: A :attr:`~AgilentB2961A.current_range` value or None. """
        log.info("%s is sourcing current." % self.name)
        self.source_mode = "current"
        if current_range is None:
            self.auto_range_source()
        else:
            self.source_current_range = current_range
        self.compliance_voltage = compliance_voltage
        self.check_errors()

    def apply_voltage(self, voltage_range=None, compliance_current=0.1):
        """ Configures the instrument to apply a souce voltage and uses and auto-range unless a voltage range is specified. The compliance current is also set.

        :param compliance_current: A float in the correct range for a :attr:`~.AgilentB2961A.compliance_current`.
        :param voltage_range: A :attr:`~AgilentB2961A.voltage_range` value or None. """
        log.info("%s is sourcing voltage." % self.name)
        self.source_mode = "voltage"
        if voltage_range is None:
            self.auto_range_source()
        else:
            self.source_voltage_range = voltage_range
        self.compliance_current = compliance_current
        self.check_errors()

    def beep(self, frequency, duration):
        """ Sounds a system beep.

        :param frequency: A frequency in Hz between 65 Hz and 2 MHz
        :param duration: A time in seconds between 0 and 7.9 seconds
        """
        self.write(":SYST:BEEP %g, %g" % (frequency, duration))

    def triad(self, base_frequency, duration):
        """ Sounds a musical triad using the system beep.

        :param base_frequency: A frequency in Hz between 65 Hz and 1.3 MHz
        :param duration: A time in seconds between 0 and 7.9 seconds
        """
        self.beep(base_frequency, duration)
        time.sleep(duration)
        self.beep(base_frequency*5.0/4.0, duration)
        time.sleep(duration)
        self.beep(base_frequency*6.0/4.0, duration)

    @property
    def error(self):
        """ Returns a tuple of an error code and message from a
        single error. """
        err = self.values(":SYST:ERR?")
        if len(err) < 2:
            err = self.read() # Try reading again
        code = err[0]
        message = err[1].replace('"', '')
        return (code, message)

    def check_errors(self):
        """ Logs any system errors reported by the instrument. """
        code, message = self.error
        while code != 0:
            t = time.time()
            log.info("Agilent B2961a reported error: %d, %s" % (code, message))
            code, message = self.error
            if (time.time()-t)>10:
                log.warning("Timed out for Agilent B2961a
                 error retrieval.")

    def reset(self):
        """ Resets the instrument and clears the queue.  """
        self.write("status:queue:clear;*RST;:stat:pres;:*CLS;")

    def 
