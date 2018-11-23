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

class Agilent3446xA(Instrument):
    """
    TODO

    .. code-block:: python

        # Esablish the Agilent 3446(7)xA Truevolt Digital Multimeter
        dmm = Agilent3446xA("GPIB::1::INSTR")

        # Run the self calibtration
        dmm.device_calibrate

        TODO

    """

    # Non-Subsystem Commands
    output_trigger_slope = Instrument.control(
        ":OUTP:TRIG:SLOP?",
        ":OUTP:TRIG:SLOP %s",
        """ A string property for the polarity of the slope
            for the device output signal on the rear-panel BNC. """,
        validator=strict_discrete_set,
        values={'negative':'NEG','positive':'POS'},
        map_values=True
    )
    get_all_measurement_data = Instrument.measurement(
        "R?",
        """ Read and erase all measurements from the read memory."""
    )
    terminal_route = Instrument.measurement(
        "ROUT:TERM?",
        """ A string parameter that indicates which terminals
            are selected for the measurement."""
        values={'front':'FRON','rear':'REAR'},
        map_values=True
    )
    self_test = Instrument.measurement(
        "TEST:ALL?",
        """ Run a comprehensive device test. All input connections
            must be disconnected before running :param`self_test`.
            Returns +1 if an error is detected."""
    )
    temperature_unit = Instrument.control(
        "UNIT:TEMP?",
        "UNIT:TEMP %s",
        """ A string parameter for the temperature unit.
            Input values are: C, F, or K. """
        validator=strict_discrete_set,
        values=('C','F','K')
    )
    # CALCulate Subsystem Commands
    calc_limit_upper = Instrument.control(
        "CALC:LIM:UPP?",
        "CALC:LIM:UPP %s",
        """ Sets an upper limit for calculation data. """,
        validator=truncated_range,
        values=(-1e15,1e15,'MIN','MAX','DEF')
    )
    calc_limit_lower = Instrument.control(
        "CALC:LIM:LOW?",
        "CALC:LIM:LOW %s",
        """ Sets an lower limit for calculation data. """,
        validator=truncated_range,
        values=(-1e15,1e15,'MIN','MAX','DEF')
    )
    calc_limit_state = Instrument.control(
        "CALC:LIM:STAT?",
        "CALC:LIM:STAT %i",
        """ A parameter that enables/disables the limit testing. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    )
    calc_hist_count = Instrument.measurement(
        "CALC:TRAN:HIST:COUNT?",
        """ Returns the number of measurements collected since
            the histogram was last cleared. """
    )
    calc_hist_bins = Instrument.control(
        "CALC:TRAN:HIST:POIN?",
        "CALC:TRAN:HIST:POIN %i",
        """ A parameter that sets the number of bins between the lower and
            upper range values for the histogram. Two additional bins are
            added: once for measurements below the lower range and a second
            for measurements above the upper range.""",
        validator=strict_discrete_set,
        values=(10,20,40,100,200,400,'MIN','MAX','DEF')
    )
    calc_hist_range_auto = Instrument.control(
        "CALC:TRAN:HIST:RANG:AUTO?",
        "CALC:TRAN:HIST:RANG:AUTO %s",
        """ A parameter that enables/disables automatic selection of the
            histogram lower and upper range values. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    )
    calc_hist_range_upper = Instrument.control(
        "CALC:TRAN:HIST:RANG:UPP?",
        "CALC:TRAN:HIST:RANG:UPP %s",
        """ Sets an upper limit for histogram range. """,
        validator=truncated_range,
        values=(-1e15,1e15,'MIN','MAX','DEF')
    )
    calc_hist_range_lower = Instrument.control(
        "CALC:TRAN:HIST:RANG:LOW?",
        "CALC:TRAN:HIST:RANG:LOW %s",
        """ Sets an lower limit for histogram range. """,
        validator=truncated_range,
        values=(-1e15,1e15,'MIN','MAX','DEF')
    )
    calc_hist_state = Instrument.control(
        "CALC:TRAN:HIST:STAT?",
        "CALC:TRAN:HIST:STAT %s",
        """ A parameter that enables/disables the histogram. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    )
    calc_stats_state = Instrument.control(
        "CALC:AVER:STAT?",
        "CALC:AVER:STAT %s",
        """ A parameter that enables/disables statistical computations. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    )
    calc_stats_average = Instrument.measurement(
        "CALC:AVER:AVER?",
        """ A parameter that returns the arithmetic mean. """,
        cast=float
    )
    calc_stats_count = Instrument.measurement(
        "CALC:AVER:COUNT?",
        """ A parameter that returns the number of
            values used in statisical computations. """,
        cast=float
    )
    calc_stats_max = Instrument.measurement(
        "CALC:AVER:MAX?",
        """ A parameter that returns the maximum value
            used in statistical computations. """,
        cast=float
    )
    calc_stats_min = Instrument.measurement(
        "CALC:AVER:MIN?",
        """ A parameter that returns the minimum value
            used in statistical computations. """,
        cast=float
    )
    calc_stats_peak2peak = Instrument.measurement(
        "CALC:AVER:PTP?",
        """ A parameter that returns the peak to peak range
            of the values used in statistical computations. """,
        cast=float
    )
    calc_stats_sdev = Instrument.measurement(
        "CALC:AVER:SDEV?",
        """ A parameter that returns the standard deviation
            of the values used in statistical computations. """,
        cast=float
    )
    calc_smoothing_rate = Instrument.control(
        "CALC:SMO:RESP?",
        "CALC:SMO:RESP %s",
        """ A string parameter that controls
            the boxcar filter smoothing rate. """,
        validator=strict_discrete_set,
        values=("SLOW","MED","MEDIUM","FAST")
    )
    calc_smoothing_state = Instrument.control(
        "CALC:SMO:STAT?",
        "CALC:SMO:STAT %s",
        """ A parameter that enables/disables the smoothing filter. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    )
    calc_trend_chart_state = Instrument.control(
        "CALC:TCH:STAT?",
        "CALC:TCH:STAT %s",
        """ A parameter that enables/disables the trend chart
            when the unit is controlled remotely. Must be
            enabled before initiating the measurement sequence. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    )
    # CALibration Subsystem Commands
    _calibration_adc = Instrument.measurement(
        "CAL:ADC",
        """ Perform a low level calibration of the ADC circuitry. """,
        validator=strict_discrete_set,
        values={'pass':0,'fail':1},
        map_values=True
    )
    _calibration_init = Instrument.measurement(
        "CAL?",
        """ Perform a calibration using an internal calibration value.
            The calibration is performed for the function and range
            set by the configuration setting. """,
        validator=strict_discrete_set,
        values={'pass':0,'fail':1},
        map_values=True
    )
    _calibration_count = Instrument.measurement(
        "CAL:COUN?",
        """ A parameter of the total number of calibrations made
            on the device. """
    )
    calibration_date = Instrument.measurement(
        "CAL:DATE?",
        """ A string parameter of the last calibration
            date in the format: yyyy,mmm,dd."""
    )
    _calibration_code_set = Instrument.setting(
        "CAL:SEC:CODE %s",
        """ A string parameter of up to 12 characters that
            is set as a new calibration security code. The
            calibration setting must be unsecured to set a
            new calibration code. """
    )
    _calibration_secure = Instrument.control(
        "CAL:SEC:STAT?",
        "CAL:SEC:STAT %s",
        """ A parameter that unsecures/secures the instrument
            calibration setting. """,
        validator=strict_discrete_set,
        values=(0,'OFF',1,'ON')
    ) # TODO setter condition for input of security code after state value
    _calibration_string = Instrument.control(
        "CAL:STR?",
        'CAL:STR "%s"',
        """ Stores a string in the calibration memory. """
    )
    calibration_temp = Instrument.measurement(
        "CAL:TEMP?",
        """ A float parameter of the last calibration temperature / °C. """,
        cast=float
    )
    calibration_time = Instrument.measurement(
        "CAL:TIME?",
        """ A string parameter of the time elapsed since the last calibration.
            String format is hh,mm,ss.sss """
    )
    _calibration_value = Instrument.control(
        "CAL:VAL?",
        "CAL:VAL %g",
        """ A float parameter that specifies the value of
            the applied calibration signal. The parameter
            defaults to 0. after *RST or SYST:PRES. """,
            cast=float
    )
    # CONFigure Subsystem Commands

    # DATA Subsystem Commands

    # DISPlay Subsystem Commands

    # FORMat Subsystem Commands

    # HCOPy Subsystem Commands

    # IEEE 488.2 Common Commands

    # LXI Subsystem Commands

    # MEASure Subsystem Commands

    # MMEMory Subsystem Commands - General Purpose & File Management

    # MMEMory Subsystem Commands - STATe and PREFerence Files

    # MMEMory Subsystem Commands - Data Transfer

    # SAMPle Subsystem Commands

    # SENSe Subsystem Commands

    # STATus Subsystem Commands

    # SYSTem Subsystem Commands - General Purpose

    # SYSTem Subsystem Commands - I/O Configuration

    # SYSTem Subsystem Commands - LOCK

    # SYSTem Subsystem Commands - LICense

    # TRIGger Subsystem Commands

    def __init__(self, adapter, **kwargs):
        super(Agilent3446xA, self).__init__(adapter,
        "Agilent 3446(7)xA Truevolt Digital Multimeter", **kwargs)

    # CALCulate Subsystem Commands
    @property
    def calc_clear(self):
        """ Clears all limits, histogram data, statistics and measurements. """
        self.write('CALC:CLE')
    @property
    def calc_limit_clear(self):
        """ Clears limit exceeded conditions for front panel and registers. """
        self.write('CALC:LIM:CLE')
    @property
    def calc_hist_clear(self):
        """ Clear the histogram data. """
        self.write('CALC:TRAN:HIST:CLE')
    @property
    def calc_stats_clear(self):
        """ Clears all computed statistics. """
        self.write('CALC:AVER:CLE')
    # CALibration Subsystem Commands
    @property
    def _calibration_save(self):
        """ Saves the calibration settings in volatile memory to
            the nonvolatile memory. Do this at then end of a calibration
            to permanently save new calibration settings."""
        self.write("CAL:STOR")
    # CONFigure Subsystem Commands

    # DATA Subsystem Commands

    # DISPlay Subsystem Commands

    # FORMat Subsystem Commands

    # HCOPy Subsystem Commands

    # IEEE 488.2 Common Commands

    # LXI Subsystem Commands

    # MEASure Subsystem Commands

    # MMEMory Subsystem Commands - General Purpose & File Management

    # MMEMory Subsystem Commands - STATe and PREFerence Files

    # MMEMory Subsystem Commands - Data Transfer

    # SAMPle Subsystem Commands

    # SENSe Subsystem Commands

    # STATus Subsystem Commands

    # SYSTem Subsystem Commands - General Purpose

    # SYSTem Subsystem Commands - I/O Configuration

    # SYSTem Subsystem Commands - LOCK

    # SYSTem Subsystem Commands - LICense

    # TRIGger Subsystem Commands
    @property
    def trigger_abort(self):
        """ Aborts the measurement in progress and
            returns the trigger to the idle state."""
        self.write(":ABOR")
    @property
    def trigger(self):
        """ Sends command to arm, initialize, and trigger the device.  """
        self.write(":ARM;:TRIG;:INIT;*TRG")
