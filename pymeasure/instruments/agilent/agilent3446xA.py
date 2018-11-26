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
    configure_get = Instrument.measurement(
        "CONF?",
        """ Returns a list of strings indicating the
            present function, range and resolution. """,
        get_process=lambda result: result.split(',')
    )
    _configure_capacitance = Instrument.setting(
        "CONF:CAP %s",
        """ A parameter that takes a list input of the
            range for capacitance measurements. The resolution
            is fixed at 4.5 digits. """,
        validator=truncated_discrete_set,
        values=(1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,'AUTO','MIN','MAX','DEF')
    )
    _configure_current_ac_range = Instrument.setting(
        "CONF:CURR:AC %s",
        """ TODO """
        validator=truncated_discrete_set,
        values=(1e-4,1e-3,1e-2,1e-1,1,3,10,'AUTO','MIN','MAX','DEF')
    )
    _configure_current_dc_range = Instrument.setting(
        "CONF:CURR:DC %s",
        """ TODO """,
        validator=truncated_discrete_set,
        values=(1e-4,1e-3,1e-2,1e-1,1,3,10,'AUTO','MIN','MAX','DEF')
    )
    _configure_resistance_range_2_wire = Instrument.setting(
        "CONF:RES %s",
        """ Set all measurement and trigger parameters
            to their default values for 2 wire resistance
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9,'AUTO','DEF')
    )
    _configure_resistance_range_4_wire = Instrument.setting(
        "CONF:FRES %s",
        """ Set all measurement and trigger parameters
            to their default values for 4 wire resistance
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9,'AUTO','DEF')
    )
    _configure_voltage_ac_range = Instrument.setting(
        "CONF:VOLT:AC %s",
        """ Set all measurement and trigger parameters
            to their default values for AC voltage
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e-1,1,1e1,1e2,1e3,'AUTO','DEF')
    )
    _configure_voltage_dc_range = Instrument.setting(
        "CONF:VOLT:DC %s",
        """ Set all measurement and trigger parameters
            to their default values for DC voltage
            measurements and set the range. """,
        validator=truncated_discrete_set,
        values=(1e-1,1,1e1,1e2,1e3,'AUTO','DEF')
    )
    # DATA Subsystem Commands
    data_points_last = Instrument.measurement(
        "DATA:LAST?",
        """ Return a list of the last measured value and the unit. """,
        get_process=lambda v:(float(v.split(' ')[0]), v.split(' ')[1])
    )
    data_points_count = Instrument.measurement(
        "DATA:POIN?",
        """ Return the total number of measurements in memory. """
    )
    data_points_threshold = Instrument.control(
        "DATA:POIN:EVEN:THR?",
        "DATA:POIN:EVEN:THR %g",
        """ An integer parameter that sets the number of
            data points to store before setting bit 9 in
            the Standard Operation Register to 1.""",
        validator=truncated_range,
        values=(1,2e6)
    )
    # DISPlay Subsystem Commands
    display_state = Instrument.control(
        "DISP:STAT?",
        "DISP:STAT %s",
        """ A string parameter that enables/disables
            the front panel display. """,
        validator=strict_discrete_set,
        values={'OFF':0,'ON':1},
        map_values=True
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
        values={'normal':'NORM','swapped':'SWAP'},
        map_values=True
    )
    format_data = Instrument.control(
        "FORM:DATA?",
        "FORM:DATA %s",
        """ A string parameter for the data format. """,
        validator=strict_discrete_set,
        values={'ascii':'ASC','real':'REAL'},
        map_values=True
    )
    # HCOPy Subsystem Commands
    panel_image_format = Instrument.control(
        "HCOP:SDUM:DATA:FORM?",
        "HCOP:SDUM:DATA:FORM %s",
        """ A string parameter that sets the image
            file format for the front panel screen shot. """,
        validator=strict_discrete_set,
        values=('PNG','BMP')
    )
    # IEEE 488.2 Common Commands
    # TODO import from standard agilent scpi class
    # LXI Subsystem Commands
    lxi_identify_state = Instrument.control(
        "LXI:IDEN:STAT?",
        "LXI:IDEN:STAT %i",
        """ An integer parameter that enables the LXI
            web identification by the LAN address. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    lxi_mdns_state = Instrument.control(
        "LXI:MDNS:ENAB?",
        "LXI:MDNS:ENAB %i",
        """ An integer parameter that enables the LXI
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
        if wait:
            self.values('DATA:REMOVE? %i, WAIT') % num_readings
        else:
            self.values('DATA:REMOVE %i') % num_readings
    # DISPlay Subsystem Commands
    @property
    def display_clear(self):
        """ Clear the text message from the front panel display. """
        self.write("DISP:TEXT:CLE")
    # FORMat Subsystem Commands
    # HCOPy Subsystem Commands
    @property
    def panel_image_capture(self):
        """ Captures the front panel image. """
        self.write("HCOP:SDUM:DATA?")
    # IEEE 488.2 Common Commands

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
    def _measure_capacitance(self, range='AUTO'):
        """ TODO """
        if range in (1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,'AUTO','MIN','MAX','DEF'):
            return float(self.ask("MEAS:CAP? {}".format(range)))
        else:
            raise ValueError('{} is not a valid range setting.'.format(range))
    def _measure_continuity(self):
        """ TODO """
        return float(self.ask("MEAS:CONT?"))
    def _measure_current(self,current_mode='DC',range='AUTO',resolution='DEF'):
        """ TODO """
        if current_mode in ('DC','AC'):
            if range in (1e-4,1e-3,1e-2,1e-1,1,3,10,'AUTO','MIN','MAX','DEF'):
                if resolution in ('MIN','MAX','DEF'): # TODO add other values
                    return float(self.ask("MEAS:CURR:{}? {}, {}".format(
                        current_mode, range, resolution)))
                else:
                    raise ValueError('''{} not a valid
                                     resolution setting.'''.format(resolution))
            else:
                raise ValueError()
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
        """ Sends command to arm, initialize
            and trigger the device.  """
        self.write(":ARM;:TRIG;:INIT;*TRG")
