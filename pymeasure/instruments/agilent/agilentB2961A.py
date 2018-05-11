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
    voltage_range_auto = Instrument.control(
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
    resistance_nplc = Instrument.control(
        ":SENS:RES:NPLC?",
        ":SENS:RES:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). Values outside of these ranges are automatically trucated. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    resistance_connection = Instrument.control(
        ":SENS:REM?",
        ":SENS:REM %s",
        """ A string property that controls the number of wires used in resistance meaasurments. Accepts a value of `ON` for the Kelvin (4 wire) connection or `OFF` for the standard (2 wire) connection. """,
        validator=strict_discrete_set,
        values={'ON','OFF'}
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
