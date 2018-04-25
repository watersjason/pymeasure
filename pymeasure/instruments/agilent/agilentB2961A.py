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

from pymeasure.instruments import Instrument

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
        ":SOUR:FUNC?",
        ":SOUR:FUNC %s",
        """ A string property that controls the source mode, which can take the values 'current' or 'voltage'. The convenience methods :meth:`~.AglientB2900A.apply_current` and :meth:`~.AgilentB2900A.apply_voltage` can also be used. """,
        validator=strict_discrete_set,
        values={'current':'CURR', 'voltage':'VOLT'},
        map_values=True
    )
    source_enabled = Instrument.measurement(
        ":OUTP:STAT?",
        """ Reads a boolean value that is True if the source is enabled. """,
        cast=bool
    )

     ###########
     # Current #
     ###########

     current = Instrument.measure(
        ":READ?",
        """ Reads the current in Amps, if configured for this reading. """
     )
     current_range = Instrument.control(
        ":SENS:CURR:RANG?",
        ":SENS:CURR:RANG:AUTO 0;:SENS:CURR:RANG %g",
        """ A floating point property that controls the measurement current range in Amps, which can take values between -1.05e-3 and +1.05e-3 A. Auto-range is disabled when this property is set. """,
        validator=truncated_range,
        values=[-1.05e-3,1.05e-3]
     )
     current_nplc = Instrument.control(
        ":SENS:CURR:NPLC?",
        ":SENS:CURR:NPLC %g",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). """
     )
