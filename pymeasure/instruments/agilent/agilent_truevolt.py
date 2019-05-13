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
from numpy import arange

class AgilentTruevolt(Instrument):
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
    slope_output_trigger = Instrument.control(
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
            are selected for the measurement.""",
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
            Input values are: C, F, or K. """,
        validator=strict_discrete_set,
        values=('C','F','K')
    )
    # CALCulate Subsystem Commands
    calc_limit_upper = Instrument.control(
        "CALC:LIM:UPP?",
        "CALC:LIM:UPP %g",
        """ Sets an upper limit for calculation data. """,
        validator=truncated_range,
        values=(-1e15,1e15)
    )
    calc_limit_lower = Instrument.control(
        "CALC:LIM:LOW?",
        "CALC:LIM:LOW %g",
        """ Sets an lower limit for calculation data. """,
        validator=truncated_range,
        values=(-1e15,1e15)
    )
    calc_limit_state = Instrument.control(
        "CALC:LIM:STAT?",
        "CALC:LIM:STAT %i",
        """ An integer parameter to enable the limit testing. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    calc_hist_count = Instrument.measurement(
        "CALC:TRAN:HIST:COUNT?",
        """ Returns the number of measurements collected since
            the histogram was last cleared. """,
        cast=int
    )
    calc_hist_bins = Instrument.control(
        "CALC:TRAN:HIST:POIN?",
        "CALC:TRAN:HIST:POIN %i",
        """ A parameter that sets the number of bins between the lower and
            upper range values for the histogram. Two additional bins are
            added: once for measurements below the lower range and a second
            for measurements above the upper range.""",
        validator=truncated_discrete_set,
        values=(10,20,40,100,200,400),
        cast=int
    )
    calc_hist_range_auto = Instrument.control(
        "CALC:TRAN:HIST:RANG:AUTO?",
        "CALC:TRAN:HIST:RANG:AUTO %i",
        """ An integer parameter to enable automatic
            selection of the histogram lower and
            upper range values. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    calc_hist_range_upper = Instrument.control(
        "CALC:TRAN:HIST:RANG:UPP?",
        "CALC:TRAN:HIST:RANG:UPP %g",
        """ A float parameter for the upper
            limit of the histogram range. """,
        validator=truncated_range,
        values=(-1e15,1e15)
    )
    calc_hist_range_lower = Instrument.control(
        "CALC:TRAN:HIST:RANG:LOW?",
        "CALC:TRAN:HIST:RANG:LOW %g",
        """ A float parameter for the lower
            limit of the histogram range. """,
        validator=truncated_range,
        values=(-1e15,1e15)
    )
    calc_hist_state = Instrument.control(
        "CALC:TRAN:HIST:STAT?",
        "CALC:TRAN:HIST:STAT %i",
        """ An integer parameter to enable the histogram. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    calc_stats_state = Instrument.control(
        "CALC:AVER:STAT?",
        "CALC:AVER:STAT %i",
        """ An integer parameter to enable
            statistical computations. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    calc_stats_average = Instrument.measurement(
        "CALC:AVER:AVER?",
        """ A float parameter of the arithmetic mean. """,
        cast=float
    )
    calc_stats_count = Instrument.measurement(
        "CALC:AVER:COUNT?",
        """ A flaot parameter of the number of
            values used in statisical computations. """,
        cast=float
    )
    calc_stats_max = Instrument.measurement(
        "CALC:AVER:MAX?",
        """ A float parameter of the maximum value
            used in statistical computations. """,
        cast=float
    )
    calc_stats_min = Instrument.measurement(
        "CALC:AVER:MIN?",
        """ A float parameter of the minimum value
            used in statistical computations. """,
        cast=float
    )
    calc_stats_peak2peak = Instrument.measurement(
        "CALC:AVER:PTP?",
        """ A float parameter of the peak to peak range
            of the values used in statistical computations. """,
        cast=float
    )
    calc_stats_sdev = Instrument.measurement(
        "CALC:AVER:SDEV?",
        """ A float parameter of the standard deviation
            of the values used in statistical computations. """,
        cast=float
    )
    calc_smoothing_rate = Instrument.control(
        "CALC:SMO:RESP?",
        "CALC:SMO:RESP %s",
        """ A string parameter that controls
            the boxcar filter smoothing rate. """,
        validator=strict_discrete_set,
        values={'slow':     'SLOW',
                'medium':   'MED',
                'fast':     'FAST'},
        map_values=True
    )
    calc_smoothing_state = Instrument.control(
        "CALC:SMO:STAT?",
        "CALC:SMO:STAT %i",
        """ An integer parameter to enable the smoothing filter. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    calc_trend_chart_state = Instrument.control(
        "CALC:TCH:STAT?",
        "CALC:TCH:STAT %i",
        """ An interger parameter to enable the trend chart
            when the unit is controlled remotely. Must be
            enabled before initiating the measurement sequence. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
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
            on the device. """,
        cast=int
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
        """ An integer parameter to secure the
            instrument calibration setting. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    ) # TODO setter condition for input of security code after state value
    _calibration_string = Instrument.control(
        "CAL:STR?",
        'CAL:STR "%s"',
        """ A string parameter stored in the calibration memory. """
    )
    calibration_temp = Instrument.measurement(
        "CAL:TEMP?",
        """ A float parameter of the
            last calibration temperature / °C. """,
        cast=float
    )
    calibration_time = Instrument.measurement(
        "CAL:TIME?",
        """ A string parameter of the time elapsed
            since the last calibration.
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
    _configure_get = Instrument.measurement(
        "CONF?",
        """ Returns a list of strings indicating the
            present function, range and resolution. """,
        get_process=lambda result: result.split(',')
    )
    _configure_capacitance = Instrument.setting(
        "CONF:CAP %g",
        """ A parameter that takes a list input of the
            range for capacitance measurements. The resolution
            is fixed at 4.5 digits. """,
        validator=truncated_discrete_set,
        values=(1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3)
    )
    _configure_current_ac_range = Instrument.setting(
        "CONF:CURR:AC %g",
        """ TODO """,
        validator=truncated_discrete_set,
        values=(1e-4,1e-3,1e-2,1e-1,1,3,10)
    )
    _configure_current_dc_range = Instrument.setting(
        "CONF:CURR:DC %g",
        """ TODO """,
        validator=truncated_discrete_set,
        values=(1e-4,1e-3,1e-2,1e-1,1,3,10)
    )
    _configure_resistance_range_2_wire = Instrument.setting(
        "CONF:RES %g",
        """ Set all measurement and trigger parameters
            to their default values for 2 wire resistance
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9)
    )
    _configure_resistance_range_4_wire = Instrument.setting(
        "CONF:FRES %g",
        """ Set all measurement and trigger parameters
            to their default values for 4 wire resistance
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9)
    )
    _configure_voltage_ac_range = Instrument.setting(
        "CONF:VOLT:AC %g",
        """ Set all measurement and trigger parameters
            to their default values for AC voltage
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e-1,1,1e1,1e2,1e3)
    )
    _configure_voltage_dc_range = Instrument.setting(
        "CONF:VOLT:DC %g",
        """ Set all measurement and trigger parameters
            to their default values for DC voltage
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e-1,1,1e1,1e2,1e3)
    )
    # DATA Subsystem Commands
    data_points_last = Instrument.measurement(
        "DATA:LAST?",
        """ Return a list of the last measured value and the unit. """,
        get_process=lambda v:(float(v.split(' ')[0]), v.split(' ')[1])
    )
    data_points_count = Instrument.measurement(
        "DATA:POIN?",
        """ Return the total number of measurements in memory. """,
        cast=int
    )
    data_points_threshold = Instrument.control(
        "DATA:POIN:EVEN:THR?",
        "DATA:POIN:EVEN:THR %g",
        """ An integer parameter that sets the number of
            data points to store before setting bit 9 in
            the Standard Operation Register to 1.""",
        validator=truncated_discrete_set,
        values=arange(1,2e6,1),
        cast=int
    )
    # DISPlay Subsystem Commands
    display_enable = Instrument.control(
        "DISP:STAT?",
        "DISP:STAT %i",
        """ An integer parameter to enable
            the front panel display. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    display_text = Instrument.control(
        "DISP:TEXT?",
        'DISP:TEXT "%s"',
        """ A string parameter that is displayed
            on the instrument front panel. """
    )
    display_view = Instrument.control(
        "DISP:VIEW?",
        "DISP:VIEW %s",
        """ A string parameter that specifies
            how the data is displayed. """,
        validator=strict_discrete_set,
        values={'numeric':'NUM',
                'histogram':'HIST',
                'trend chart':'TCH',
                'bar meter':'MET'},
        map_values=True
    )
    # FORMat Subsystem Commands
    format_border = Instrument.control(
        "FORM:BORD?",
        "FORM:BORD %s",
        """ A string parameter for the
            binary block transfer property. """,
        validator=strict_discrete_set,
        values={'normal':'NORM',
                'swapped':'SWAP'},
        map_values=True
    )
    format_data = Instrument.control(
        "FORM:DATA?",
        "FORM:DATA %s",
        """ A string parameter for the data format. """,
        validator=strict_discrete_set,
        values={'ascii':'ASC',
                'real':'REAL'},
        map_values=True
    )
    # HCOPy Subsystem Commands
    panel_image_format = Instrument.control(
        "HCOP:SDUM:DATA:FORM?",
        "HCOP:SDUM:DATA:FORM %s",
        """ A string parameter for the image
            file format used for the front
            panel screen shot. """,
        validator=strict_discrete_set,
        values=('PNG','BMP')
    )
    # IEEE 488.2 Common Commands
    """ TODO import from standard agilent scpi class """
    # LXI Subsystem Commands
    lxi_identify_enable = Instrument.control(
        "LXI:IDEN:STAT?",
        "LXI:IDEN:STAT %i",
        """ An integer parameter to enable the LXI
            web identification by the LAN address. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    lxi_mdns_enable = Instrument.control(
        "LXI:MDNS:ENAB?",
        "LXI:MDNS:ENAB %i",
        """ An integer parameter to enable the LXI
            multicast domain name system (mDNS) that
            provides DNS service discovery on a network
            without a DNS server.""",
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    lxi_mdns_name_host = Instrument.measurement(
        "LXI:MDNS:HNAM?",
        """ A string parameter of the resolved mDNS hostname
            in the form `K-<model number>-<serial>-N` where
            <serial> is the last 5 digits of the instrument's
            serial number. N is an integer appended to make
            the name unique and maynot be present. """
    )
    lxi_mdns_name_service_desired = Instrument.control(
        "LXI:MDNS:SNAME:DES?",
        'LXI:MDNS:SNAME:DES "%s"',
        """ A string parameter of the desired mDNS service name.
            Default value:
                `Keysight <model number> Digial Multimeter - <serial>`
            where <serial> is the last 5 digits of the instrument's
            serial number. """
    )
    lxi_mdns_name_service_resolved = Instrument.measurement(
        "LXI:MDNS:SNAM?",
        """ A string parameter of the resolved (actual) mDNS
            service name. """
    )
    # MEASure Subsystem Commands
    """ Not implemented. """
    # MMEMory Subsystem Commands - General Purpose & File Management
    """ TODO """
    # MMEMory Subsystem Commands - STATe and PREFerence Files
    """ TODO """
    # MMEMory Subsystem Commands - Data Transfer
    """ TODO """
    # SAMPle Subsystem Commands
    sample_count = Instrument.control(
        "SAMP:COUN?",
        "SAMP:COUN %s",
        """ An integer parameter for the number
            of sample measurements made per trigger.""",
        validator=truncated_discrete_set,
        values=arange(1,1e9,1),
        cast=int
    )
    sample_count_pretrigger = Instrument.control(
        "SAMP:COUN:PRET?",
        "SAMP:COUN:PRET %s",
        """ An integer parameter for the
            number of samples to be collected and
            saved in memory before the trigger. """,
        validator=truncated_discrete_set,
        values=arange(0,1999999,1),
        cast=int
    )
    sample_source = Instrument.control(
        "SAMP:SOUR?",
        "SAMP:SOUR %s",
        """ A string parameter for the source of the trigger signal. """,
        validator=strict_discrete_set,
        values={'timer':    'TIM',
                'immediate':'IMM'},
        map_values=True
    )
    sample_timer = Instrument.control(
        "SAMP:TIM?",
        "SAMP:TIM %s",
        """ A string parameter for the sample
            interval for timed sampling. """,
        validator=strict_discrete_set,
        values={'minimum':'MIN',
                'maximum':'MAX',
                'defualt':'DEF'},
        map_values=True
    )
    # SENSe Subsystem Commands
    sense_function = Instrument.control(
        "SENS:FUNC?",
        "SENS:FUNC %s",
        """ A string parameter for
            the measurement function. """,
        validator=strict_discrete_set,
        values={'capacitance':      '"CAP"',
                'continuity':       '"CONT"',
                'ac current':       '"CURR:AC"',
                'dc current':       '"CURR"',
                'diode':            '"DIOD"',
                'frequency':        '"FREQ"',
                '4 wire resistance':'"FRES"',
                '2 wire resistance':'"RES"',
                'period':           '"PER"',
                'temperature':      '"TEMP"',
                'ac voltage':       '"VOLT:AC"',
                'dc voltage':       '"VOLT"',
                'dc ratio':         '"VOLT:RAT"'},
        map_values=True
    )
    # SENSe Subsystem Commands - Capacitance
    """
    # TODO sense_capacitance_null_state = Instrument.control()
    # TODO sense_capacitance_null_value = Instrument.control()
    # TODO sense_capacitance_null_auto = Instrument.control()
    # TODO sense_capacitance_range = Instrument.control()
    # TODO sense_capacitance_range_auto = Instrument.control()
    # TODO sense_capacitance_secondary = Instrument.control()
    """
    # SENSe Subsystem Commands - Current
    """
    # TODO sense_current_ac_bandwidth = Instrument.control()
    # TODO sense_current_ac_null_state = Instrument.control()
    # TODO sense_current_dc_null_state = Instrument.control()
    # TODO sense_current_ac_null_value = Instrument.control()
    # TODO sense_current_dc_null_value = Instrument.control()
    # TODO sense_current_ac_null_auto = Instrument.control()
    # TODO sense_current_dc_null_auto = Instrument.control()
    # TODO sense_current_ac_range = Instrument.control()
    # TODO sense_current_dc_range = Instrument.control()
    # TODO sense_current_ac_range_auto = Instrument.control()
    # TODO sense_current_dc_range_auto = Instrument.control()
    # TODO sense_current_ac_terminals = Instrument.control()
    # TODO sense_current_dc_terminals = Instrument.control()
    # TODO sense_current_ac_secondary = Instrument.control()
    # TODO sense_current_dc_aperature = Instrument.control()
    # TODO sense_current_dc_aperature_enable = Instrument.control()
    # TODO sense_current_dc_nplc = Instrument.control()
    # TODO sense_current_dc_resolution = Instrument.control()
    # TODO sense_current_dc_secondary = Instrument.control()
    # TODO sense_current_dc_zero_auto = Instrument.control()
    # TODO sense_current_switch_mode = Instrument.control()
    """
    # SENSe Subsystem Commands - Data2
    sense_secondary_data = Instrument.measurement(
        "SENS:DATA2?",
        """ A string parameter of the secondary measurement.
            Output is dependent on secondary measurement settings. """
    )
    # SENSe Subsystem Commands - Frequency and Period
    """
    # TODO sense_frequency_aperature = Instrument.control()
    # TODO sense_period_aperature = Instrument.control()
    # TODO sense_frequency_null_state = Instrument.control()
    # TODO sense_period_null_state = Instrument.control()
    # TODO sense_frequency_null_value = Instrument.control()
    # TODO sense_period_null_value = Instrument.control()
    # TODO sense_frequency_null_auto = Instrument.control()
    # TODO sense_period_null_auto = Instrument.control()
    # TODO sense_frequency_range_lower = Instrument.control()
    # TODO sense_period_range_lower = Instrument.control()
    # TODO sense_frequency_auto_timeout = Instrument.control()
    # TODO sense_period_auto_timeout = Instrument.control()
    # TODO sense_frequency_voltage_range = Instrument.control()
    # TODO sense_period_voltage_range = Instrument.control()
    # TODO sense_frequency_voltage_range_auto = Instrument.control()
    # TODO sense_period_voltage_range_auto = Instrument.control()
    # TODO sense_frequency_secondary = Instrument.control()
    # TODO sense_period_secondary = Instrument.control()
    """
    # SENSe Subsystem Commands - Resistance
    sense_resistance_aperature = Instrument.control(
        "SENS:RES:APER?",
        "SENS:RES:APER %g",
        """ A float parameter for the integration time / s.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=truncated_discrete_set,
        values=arange(2e-5,1,2e-6,dtype=float)
    )
    sense_resistance_aperature_enable = Instrument.control(
        "SENS:RES:APER:ENAB?",
        "SENS:RES:APER:ENAB %s",
        """ An integer parameter to enable setting of the resistance
            measurement integration time. Common to both 2 and 4 wire
            resistance measurements. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_resistance_nplc = Instrument.control(
        "SENS:RES:NPLC?",
        "SENS:RES:NPLC %s",
        """ A float parameter for the resistance
            measurement integration time as the number of
            power line cycles. Common to both 2 and 4 wire
            resistance measurements. """,
        validator=truncated_discrete_set,
        values=(0.001,0.002,0.006,0.02,0.06,0.2,1,10,100)
    )
    sense_resistance_null_enable = Instrument.control(
        "SENS:RES:NULL:STAT?",
        "SENS:RES:NULL:STAT %i",
        """ An integer parameter to enable the resistance null state.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    sense_resistance_null_value = Instrument.control(
        "SENS:RES:NULL:VAL?",
        "SENS:RES:NULL:VAL %g",
        """ A float parameter for the resistance null value.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=truncated_range,
        values=(-1.2e9,1.2e9)
    )
    sense_resistance_null_auto_enable = Instrument.control(
        "SENS:RES:NULL:VAL:AUTO?",
        "SENS:RES:NULL:VAL:AUTO %i",
        """ An integer parameter that enables the auto null function.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_resistance_offset_enable = Instrument.control(
        "SENS:FRES:OCOM?",
        "SENS:FRES:OCOM %i",
        """ An integer parameter that enables offset compensation for
            both 2 and 4 wire resistance measurements. Offset compensation
            removes the effects of small DC voltages in the test circuit. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_resistance_limit_state_enable = Instrument.control(
        "SENS:RES:POW:LIM:STAT?",
        "SENS:RES:POW:LIM:STAT %i",
        """ An integer parameter that enables lower power resistance
            measurements. Common to both 2 and 4 wire measurements. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_resistance_range = Instrument.control(
        "SENS:RES:RANG?",
        "SENS:RES:RANG %s",
        """ A string or float parameter for a fixed measurement range.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9)
    )
    sense_resistance_range_auto_enable = Instrument.control(
        "SENS:RES:RANG:AUTO?",
        "SENS:RES:RANG:AUTO %i",
        """ An integer parameter that enables auto ranging of resistance
            measurements. Common to both 2 and 4 wire measurements. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_resistance_resolution = Instrument.control(
        "SENS:RES:RES?",
        "SENS:RES:RES %s",
        """ A string parameter for the measurement range.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=strict_discrete_set,
        values={'minimum':'MIN',
                'maximum':'MAX',
                'defualt':'DEF'},
        map_values=True
    )
    sense_resistance_secondary = Instrument.control(
        "SENS:RES:SEC?",
        "SENS:RES:SEC %s",
        """ A string parameter for the secondary resistance measurement.
            Common to both 2 and 4 wire resistance measurements. """,
        validator=strict_discrete_set,
        values={'off':'OFF',
                'raw':'CALC:DATA'},
        map_values=True
    )
    sense_resistance_auto_zero = Instrument.control(
        "SENS:RES:ZERO:AUTO?",
        "SENS:RES:ZERO:AUTO %s",
        """ A string parameter for the 2 wire resistance measurement
            auto zeroing state. """,
        validator=strict_discrete_set,
        values={'off':  'OFF',
                'on':   'ON',
                'once': 'ONCE'},
        map_values=True
    )
    # SENSe Subsystem Commands - Temperature
    """ TODO """
    # SENSe Subsystem Commands - Voltage
    sense_voltage_ac_bandwidth = Instrument.control(
        "SENS:VOLT:AC:BAND?",
        "SENS:VOLT:AC:BAND %i",
        """ A float or string parameter for the AC voltage
            bandwidth integration rate. """,
        validator=truncated_discrete_set,
        values=(3,20,200),
        cast=int
    )
    sense_voltage_ac_null_enable = Instrument.control(
        "SENS:VOLT:AC:NULL:STAT?",
        "SENS:VOLT:AC:NULL:STAT %i",
        """ An integer parameter to enable the AC voltage null state.
            The AC voltage null state is independent from the DC state. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    sense_voltage_dc_null_enable = Instrument.control(
        "SENS:VOLT:DC:NULL:STAT?",
        "SENS:VOLT:DC:NULL:STAT %i",
        """ An integer parameter to enable the DC voltage null state.
            The DC voltage null state is independent from the AC state. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    sense_voltage_ac_null_value = Instrument.control(
        "SENS:VOLT:AC:NULL:VAL?",
        "SENS:VOLT:AC:NULL:VAL %g",
        """ A float parameter for the AC voltage null value.
            The AC voltage null value is independent from the DC value. """,
        validator=truncated_range,
        values=(-1200,1200)
    )
    sense_voltage_dc_null_value = Instrument.control(
        "SENS:VOLT:DC:NULL:VAL?",
        "SENS:VOLT:DC:NULL:VAL %g",
        """ A float parameter for the DC voltage null value.
            The DC voltage null value is independent from the AC value. """,
        validator=truncated_range,
        values=(-1200,1200)
    )
    sense_voltage_ac_null_auto_enable = Instrument.control(
        "SENS:VOLT:AC:NULL:VAL:AUTO?",
        "SENS:VOLT:AC:NULL:VAL:AUTO %i",
        """ An integer parameter to enable the AC voltage auto null.
            The AC voltage null value is independent from the DC value. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_voltage_dc_null_auto_enable = Instrument.control(
        "SENS:VOLT:DC:NULL:VAL:AUTO?",
        "SENS:VOLT:DC:NULL:VAL:AUTO %i",
        """ An integer parameter to enable the DC voltage auto null.
            The DC voltage null value is independent from the AC value. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    sense_voltage_ac_range = Instrument.control(
        "SENS:VOLT:AC:RANG:VAL?",
        "SENS:VOLT:AC:RANG %g",
        """ A float parameter for the AC voltage range.
            The AC voltage range is independent from the DC value. """,
        validator=truncated_discrete_set,
        values=(1e-1,1,1e1,1e2,1e3)
    )
    sense_voltage_dc_range = Instrument.control(
        "SENS:VOLT:DC:RANG:VAL?",
        "SENS:VOLT:DC:RANG %s",
        """ A float parameter for the DC voltage range.
            The DC voltage range is independent from the AC value. """,
        validator=truncated_discrete_set,
        values=(1e-1,1,1e1,1e2,1e3)
    )
    sense_voltage_ac_range_auto_enable = Instrument.control(
        "SENS:VOLT:AC:RANG:AUTO?",
        "SENS:VOLT:AC:RANG:AUTO %s",
        """ A string parameter to enable the AC voltage auto range.
            The AC voltage null value is independent from the DC value. """,
        validator=strict_discrete_set,
        values={'off':  'OFF',
                'on':   'ON',
                'once': 'ONCE'},
        map_values=True
    )
    sense_voltage_dc_range_auto_enable = Instrument.control(
        "SENS:VOLT:DC:RANG:AUTO?",
        "SENS:VOLT:DC:RANG:AUTO %s",
        """ A string parameter to enable the DC voltage auto range.
            The DC voltage null value is independent from the AC value. """,
        validator=strict_discrete_set,
        values={'off':  'OFF',
                'on':   'ON',
                'once': 'ONCE'},
        map_values=True
    )
    sense_voltage_ac_secondary = Instrument.control(
        "SENS:VOLT:AC:SEC?",
        "SENS:VOLT:AC:SEC %s",
        """ A string parameter for the AC voltage
            secondary measurement function. """,
        validator=strict_discrete_set,
        values={'off':              '"OFF"',
                'raw':              '"CALC:DATA"',
                'signal frequency': '"FREQ"',
                'dc voltage':       '"VOLT"'},
        map_values=True
    )
    sense_voltage_dc_aperature_value = Instrument.control(
        "SENS:VOLT:DC:APER?",
        "SENS:VOLT:DC:APER %g",
        """ A float parameter for the DC
            voltage aperature integration time / s. """,
        validator=truncated_discrete_set,
        values=arange(2e-4,1,2e-6)
    )
    sense_voltage_dc_aperature_enable = Instrument.control(
        "SENS:VOLT:DC:APER:ENAB?",
        "SENS:VOLT:DC:APER:ENAB %i",
        """ An integer parameter to enable the DC
            voltage aperature integration state. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    sense_voltage_dc_impedance_auto = Instrument.control(
        "SENS:VOLT:DC:IMP:AUTO?",
        "SENS:VOLT:DC:IMP:AUTO %i",
        """ An integer parameter that enables the auto
            impedance mode for DC voltage measurements.
            When enabled, the input impedance is:
                >10e9 Ohm for DC voltage ranges <= 10 V, or
                10e6 Ohm for DC voltage ranges > 10 V.
            When disabled, the input impdance is fixed at 10e6 Ohm.""",
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    sense_voltage_dc_nplc = Instrument.control(
        "SENS:VOLT:DC:NPLC?",
        "SENS:VOLT:DC:NPLC %s",
        """ A float or string parameter for the DC voltage
            measurement integration time as the number of
            power line cycles. """,
        validator=truncated_discrete_set,
        values=(0.001,0.002,0.006,0.02,0.06,0.2,1,10,100)
    )
    sense_voltage_dc_ratio_secondary = Instrument.control(
        "SENS:VOLT:DC:RAT:SEC?",
        "SENS:VOLT:DC:RAT:SEC %s",
        """ A string parameter for the DC
            voltage secondary measurement. """,
        validator=strict_discrete_set,
        values={'off':          '"OFF"',
                'no math':      '"CALC:DATA"',
                'sense data':   '"SENS:DATA"'},
        map_values=True
    )
    sense_voltage_dc_resolution = Instrument.control(
        "SENS:VOLT:DC:RES?",
        "SENS:VOLT:DC:RES %g",
        """ A float parameter that sets the DC voltage and
            DC voltage ratio measurement resolution.""",
        validator=truncated_range,
        values=(1e-9,1e4)
    )
    sense_voltage_dc_secondary = Instrument.control(
        "SENS:VOLT:DC:SEC?",
        "SENS:VOLT:DC:SEC %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={'off':          '"OFF"',
                'no math':      '"CALC:DATA"',
                'ac voltage':   '"VOLT:AC"',
                'peak to peak': '"PTP"'},
        map_values=True
    )
    sense_voltage_dc_auto_zero = Instrument.control(
        "SENS:VOLT:DC:ZERO:AUTO?",
        "SENS:VOLT:DC:ZERO:AUTO %s",
        """ A string parameter for the DC voltage and
            DC voltage ratio auto zeroing state. """,
        validator=strict_discrete_set,
        values={'off':  'OFF',
                'on':   'ON',
                'once': 'ONCE'},
        map_values=True
    )
    # STATus Subsystem Commands
    """ TODO """
    # SYSTem Subsystem Commands - General Purpose
    autocal_date = Instrument.measurement(
        "SYST:ACAL:DATE?",
        """ A list with elements [yyyy, mm, dd].
            The elements represent the year, month and day
            of the last autocalibration. """,
        get_process=lambda v:[int(i) for i in v.split(',')]
    )
    autocal_temp = Instrument.measurement(
        "SYST:ACAL:TEMP?",
        """ A float parameter of the the internal
            temperature / °C during the last autocalibration. """
    )
    autocal_time = Instrument.measurement(
        "SYST:ACAL:TIME?",
        """ A list with elements [hh, mm, ss].
            The elements represent the hour, minute and
            seconds of the last autocalibration. """,
        get_process=lambda v:[int(i) for i in v.split(',')]
    )
    system_beep_enable = Instrument.control(
        "SYST:BEEP:STAT?",
        "SYST:BEEP:STAT %i",
        """ An integer parameter to enable
            the system beeper state.""",
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    system_click_enable = Instrument.control(
        "SYST:CLIC:STAT?",
        "SYTS:CLIC:TAT %i",
        """ An integer parameter to enable
            the audible click produced when
            a key is pressed. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    system_date = Instrument.control(
        "SYST:DATE?",
        "SYST:DATE %s",
        """ A list parameter that sets the system date.
            The list elements are: [<yyyy>,<mm>,<dd>]. """,
        set_process=lambda v:'{},{},{}'.format([v[0],v[1],v[2]])
    )
    error_get = Instrument.measurement(
        "SYST:ERR:NEXT?",
        """ Read and clear one error from the queue.
            Errors are retrieved following the
            first-in-first-out scheme. """
    )
    system_label = Instrument.control(
        "SYST:LAB?",
        "SYST:LAB %s",
        """ Place a message at the bottom half
            of the instrument's front panel. """
    )
    system_line_frequency = Instrument.measurement(
        "SYST:LFR?",
        """ A float parameter of the
            queried line frequency / Hz."""
    )
    system_security_count = Instrument.measurement(
        "SYST:SEC:COUN?",
        """ An integer parameter that returns
            the instrument security count. The
            security count is incremented by 1
            each time an action is performed
            that requires a security unlock.
            Calibration does not change the count.""",
        cast=int
    )
    system_temperature = Instrument.measurement(
        "SYST:TEMP?",
        """ A float parameter of the internal temperature / °C. """
    )
    system_time = Instrument.control(
        "SYST:TIME?",
        "SYST:TIME %s",
        """ A list parameter for the system time.
            The list elements are: [<hh>,<mm>,<ss.sss>].""",
        set_process=lambda v:'{},{},{}'.format([v[0],v[1],v[2]])
    )
    system_time_warmup = Instrument.measurement(
        "SYST:UPT?",
        """ A list parameter for the amount of time
            the system has been powered on. The list
            elements are: [<dd>,<hh>,<mm>,<ss>]. """
    )
    system_scpi_version = Instrument.measurement(
        "SYST:VERS?",
        """ A float parameter for the version of SCPI
            that the instrument complies with."""
    )
    system_power_message = Instrument.control(
        "SYST:WMES?",
        'SYST:WMES "%s"',
        """ TODO """
    )
    # SYSTem Subsystem Commands - I/O Configuration
    """ TODO """
    # SYSTem Subsystem Commands - LOCK
    """ TODO """
    # SYSTem Subsystem Commands - LICense
    """ TODO """
    # TRIGger Subsystem Commands
    trigger_count = Instrument.control(
        "TRIG:COUN?",
        "TRIG:COUN %i",
        """ A property for the number of triggers
            accepted before returning to idle. """,
        validator=strict_discrete_set,
        values=(1,9.9E37),
        cast=int,
        set_process=lambda v: 1e6 if v != 9.9E37 and v > 1e6 else v
    )
    trigger_delay_value = Instrument.control(
        "TRIG:DEL?",
        "TRIG:DEL %g",
        """ A float property for the period / s
            between the trigger signal
            and the first measurement. """,
        validator=truncated_discrete_set,
        values=(0,3600)
    )
    trigger_delay_auto_enable = Instrument.control(
        "TRIG:DEL:AUTO?",
        "TRIG:DEL:AUTO %i",
        """ An integer property to enable
            the automatic trigger delay. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    trigger_level = Instrument.control(
        "TRIG:LEV?",
        "TRIG:LEV %s",
        """ A string property for the
            level on which the trigger occurs
            when level triggering is enabled. """,
        validator=strict_discrete_set,
        values={'minimum':'MIN',
                'maximum':'MAX',
                'defualt':'DEF'},
        map_values=True
    )
    trigger_slope = Instrument.control(
        "TRIG:SLOP?",
        "TRIG:SLOP %s",
        """ A string parameter for the polarity
            of the external source level trigger. """,
        validator=strict_discrete_set,
        values={'positive':'POS',
                'negative':'NEG'},
        map_values=True
    )
    trigger_source = Instrument.control(
        "TRIG:SOUR?",
        "TRIG:SOUR %s",
        """ A string parameter for the
            trigger signal source. """,
        validator=strict_discrete_set,
        values={'immediate':    'IMM',
                'external':     'EXT',
                'bus':          'BUS',
                'internal':     'INT'},
        map_values=True
    )
    def __init__(self, adapter, **kwargs):
        super(Agilent3446xA, self).__init__(adapter,
        "Agilent 3446(7)xA Truevolt Digital Multimeter", **kwargs)

        self.write('SYST:IDEN DEF')

        _id_list = self.id().split(',')
        self.manufacturer = _id_list[0]
        self.model_number = _id_list[1]
        self.serial_number = _id_list[2]
        self.revision_code = _id_list[3]

        _resolution_factor = dict()
        _resolution_factor['34460A']=tuple(3e-6,1e-5,3e-5,1e-4,3e-4)
        _resolution_factor['34461A']=tuple(3e-7,1e-6,3e-6,1e-5,1e-4)
        _resolution_factor['34465A']=tuple(3e-8,1e-7,3e-7,7e-7,
                                            1.5e-6,3e-6,1.5e-5,3e-5)
        _resolution_factor['34470A']=tuple(1e-8,3e-8,1e-7,3e-7,5e-7,
                                            1e-6,3e-6,1e-5,3e-5)
        self._resolution_factor = _resolution_factor[self.model_number]
    # CALCulate Subsystem Commands
    @property
    def calc_clear(self):
        """ Clears all limits, histogram data,
            statistics and measurements. """
        self.write('CALC:CLE')
    @property
    def calc_limit_clear(self):
        """ Clears limit exceeded conditions
            for front panel and registers. """
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
            the nonvolatile memory. Do this at then end of a
            calibration to permanently save new calibration settings."""
        self.write("CAL:STOR")
    # CONFigure Subsystem Commands
    @property
    def _configure_continuity(self):
        """ Set all measurement and trigger parameters to
            their defualt values for continuity measurements. """
        self.write("CONF:CONT")
    @property
    def _configure_diode(self):
        """ Sets all measurement and trigger parameters
            to their default values for diode tests. """
        self.write("CONF:DIOD")
    # DATA Subsystem Commands
    def data_points_remove(self,num_readings,wait_for_values=False,**kwargs):
        """ Read and erase measurements from the reading memory.
            :param num_readings:    An integer parameter for the number
                                    of readings to query, return and erase.
            :param wait_for_values: A boolean parameter that delays the reply
                                    when the number of readings available is
                                    less than :param num_readings:.
        """
        if kwargs.get('timeout') is not None:
            pass # TODO change timeout value
        if wait_for_values:
            self.values('DATA:REMOVE? %i, WAIT') % num_readings
        else:
            self.values('DATA:REMOVE %i') % num_readings
    # DISPlay Subsystem Commands
    @property
    def display_clear(self):
        """ Clear the text message from the front panel display. """
        self.write("DISP:TEXT:CLE")
    # HCOPy Subsystem Commands
    @property
    def panel_image_capture(self):
        """ Captures the front panel image. """
        self.write("HCOP:SDUM:DATA?")
    # IEEE 488.2 Common Commands
    """ TODO """
    # LXI Subsystem Commands
    @property
    def lxi_reset(self):
        """ Reset LAN settings to a known operating state. """
        self.write("LXI:RES")
    @property
    def lxi_restart(self):
        """ Restart LAN with current settings specified by
            :func :. """ # TODO finish function name for SYST:COMM:LAN
        self.write("LXI:REST")
    # MEASure Subsystem Commands
    """ Not implemented. """
    # MMEMory Subsystem Commands - General Purpose & File Management
    """ TODO """
    # MMEMory Subsystem Commands - STATe and PREFerence Files
    """ TODO """
    # MMEMory Subsystem Commands - Data Transfer
    """ TODO """
    # SENSe Subsystem Commands - Data2
    @property
    def sense_secondary_clear(self):
        """ Clear the latest result(s) of the secondary measurement. """
        self.write("SENS:DATA2:CLE:IMM")
    # SENSe Subsystem Commands - Frequency and Period
    """ None """
    # SENSe Subsystem Commands - Resistance
    """ None """
    # SENSe Subsystem Commands - Temperature
    """ TODO """
    # SENSe Subsystem Commands - Voltage
    # STATus Subsystem Commands
    """ TODO """
    # SYSTem Subsystem Commands - General Purpose
    @property
    def system_beep(self):
        """ Issue a single beep. """
        self.write("SYST:BEEP:IMM")
    @property
    def system_local(self):
        """ Set the instrument state to local. """
        self.write("SYST:LOC")
    @property
    def system_preset(self):
        """ Reset the instrument for front panel operation. """
        self.write("SYST:PRES")
    # SYSTem Subsystem Commands - I/O Configuration
    """ TODO """
    # SYSTem Subsystem Commands - LOCK
    """ TODO """
    # SYSTem Subsystem Commands - LICense
    """ TODO """
    # TRIGger Subsystem Commands
    @property
    def trigger_abort(self):
        """ Aborts the measurement in progress and
            returns the trigger to the idle state."""
        self.write(":ABOR")
    @property
    def trigger(self):
        """ Sends command to arm, initialize
            and trigger the device.  """
        self.write(":ARM;:TRIG;:INIT;*TRG")
    # Convenience Functions
    def measure_configure(self,mode=None):
        """ TODO """
        if mode is None:
            return self._configure_get
        elif (mode is 'capacitance') or (mode is 'CAP'):
            pass
        elif (mode is 'continuity') or (mode is 'CONT'):
            pass
        elif (mode is 'ac current') or (mode is 'ACC'):
            pass
        elif (mode is 'dc current') or (mode is 'DCC'):
            pass
        elif (mode is 'diode') or (mode is 'DIOD'):
            pass
        elif (mode is 'frequency') or (mode is 'FREQ'):
            pass
        elif (mode is 'period') or (mode is 'PER'):
            pass
        elif (mode is 'resistance') or (mode is 'RES'):
            pass
        elif (mode is 'temperature') or (mode is 'TEMP'):
            pass
        elif (mode is 'ac voltage') or (mode is 'ACV'):
            pass
        elif (mode is 'dc voltage') or (mode is 'DCV'):
            pass
        elif (mode is 'dc ratio') or (mode is 'DCR'):
            pass
        else:
            raise ValueError('Input for mode is not an acceptable value.')
    def measure_immediate(self):
        """ """
    def measure_triggered(self):
        """ """

class Agilent34470A(AgilentTruevolt):
    def __init__(self, adapter, **kwargs):
        super().__init__(adapter, **kwargs)
