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

import time

class AgilentB2961A(Instrument):
    """
    Represent the Agilent/Keysight B2961A (with the ultra-low-noise option) source measurement units. For multi-channel units, channel 1 is used and any other channels are not supported.

    Possibly will work with other units in the B2900 series, but only in the limited current/voltage source/measure ranges allowed by the B2961A.

    .. code-block:: python

        source_measure_unit = AgilentB2900A("GPIB::1::INSTR")   # Esablish the Agilent/Kesight B2961A source measurement device

        TODO

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

    #################
    # Configuration #
    #################

    device_enable = Instrument.control(
        ":OUTP:STAT?",
        ":OUTP %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    device_float = Instrument.control(
        ":OUTP:LOW?",
        ":OUTP:STAT 0;:OUTP:LOW %s",
        """ A string property that selects the state of the low terminal. Sets the disables the source output when called to set the terminal state. """,
        validator=strict_discrete_set,
        values={"float":"FLO", "ground":"GRO"},
        map_values=True
    )
    device_calibrate = Instrument.measurement(
        "*CAL?",
        """ TODO """
    )
    device_test = Instrument.measurement(
        "*TST?",
        """ TODO """
    )
    device_protection = Instrument.control(
        ":OUTP:PROT?",
        ":OUTP:PROT %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    device_status_operation_condition = Instrument.measurement(
        ":FORM:SREG ASC;:STAT:OPER:COND?",
        """ TODO """,
        cast=int
    )
    output_off_mode = Instrument.control(
        ":OUTP:OFF:MODE?",
        ":OUTP:OFF:MODE %s",
        """ TODO """,
        validator=strict_discrete_set,
        values=("ZERO","HIZ","NORM")
    )
    output_auto_out_enable = Instrument.control(
        ":OUTP:ON:AUTO?",
        ":OUTP:ON:AUTO %i",
        """ Enables or disables the automatic output on function. If this function is enabled, the source output is automatically turned on when the `:INIT` or `:READ` command is sent. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    output_auto_out_disable = Instrument.control(
        ":OUTP:OFF:AUTO?",
        ":OUTP:OFF:AUTO %i",
        """ Enables or disables the automatic output off function. If this function is enabled, the source output is automatically turned off immediately when the grouped channels change status from busy to idle. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )

    #######################
    # Arm / Trigger Count #
    #######################

    trigger_count_measure = Instrument.control(
        ":TRIG:ACQ:COUN?",
        ":TRIG:ACQ:COUN %s",
        """ An integer property (or string property representing an internally programmed default value) that configures the trigger count for the trigger-level measurement (acquisition) data. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','default':'DEF','max':'MAX','infinity':'INF'},[1,1e6]]
    )
    arm_count_measure = Instrument.control(
        ":ARM:ACQ:COUN?",
        ":ARM:ACQ:COUN %s",
        """ An integer property (or string property representing an internally programmed default value) that configures the trigger count for the arm-level measurement (acquisition) data. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','default':'DEF','max':'MAX','infinityinfinity':'INF'},[1,1e6]]
    )
    trigger_count_source = Instrument.control(
        ":TRIG:TRAN:COUN?",
        ":TRIG:TRAN:COUN %s",
        """ An integer property (or string property representing an internally programmed default value) that configures the trigger count for the trigger-level source (transient) data. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','default':'DEF','max':'MAX','infinity':'INF'},[1,1e6]]
    )
    arm_count_source = Instrument.control(
        ":ARM:TRAN:COUN?",
        ":ARM:TRAN:COUN %s",
        """ An integer property (or string property representing an internally programmed default value) that configures the trigger count for the arm-level source (transient) data. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','default':'DEF','max':'MAX','infinity':'INF'},[1,1e6]]
    )
    trigger_count = Instrument.setting(
        ":TRIG:COUN %s",
        """  An integer property (or string property representing an internally programmed default value) that sets the trigger count for the trigger-level source (transient) and measurement (acquisition) data. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[{'min':'MIN','default':'DEF','max':'MAX','infinity':'INF'},[1,1e6]]
    )
    arm_count = Instrument.setting(
        ":ARM:COUN %s",
        """ An integer property (or string property representing an internally programmed default value) that sets the trigger count for the arm-level source (transient) and measurement (acquisition) data. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','default':'DEF','max':'MAX','infinity':'INF'},[1,1e6]]
    )

    #######################
    # Arm / Trigger Delay #
    #######################

    trigger_delay_measure = Instrument.control(
        ":TRIG:ACQ:DEL?",
        ":TRIG:ACQ:DEL %s",
        """ A delay, in seconds, for the trigger-level measurement (acquisition) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    arm_delay_measure = Instrument.control(
        ":ARM:ACQ:DEL?",
        ":ARM:ACQ:DEL %s",
        """ A delay, in seconds, for the arm-level measurement (acquisition) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    trigger_delay_source = Instrument.control(
        ":TRIG:TRAN:DEL?",
        ":TRIG:TRAN:DEL %s",
        """ A delay, in seconds, for the trigger-level source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    arm_delay_source = Instrument.control(
        ":ARM:TRAN:DEL?",
        ":ARM:TRAN:DEL %s",
        """ A delay, in seconds, for the arm-level source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    trigger_delay = Instrument.setting(
        ":TRIG:DEL %s",
        """ A delay, in seconds, for the trigger-level measurement (acquire) and source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    arm_delay = Instrument.setting(
        ":ARM:DEL %s",
        """ A delay, in seconds, for the arm-level measurement (acquire) and source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )

    ########################
    # Arm / Trigger Period #
    ########################

    trigger_period_measure = Instrument.control(
        ":TRIG:ACQ:TIM?",
        ":TRIG:ACQ:TIM %s",
        """ A float property (or string property representing an internally programmed default value) that configures the period/interval (in seconds) of the trigger-level signal for the specified measurement device action. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[2e-5,1e5]]
    )
    arm_period_measure = Instrument.control(
        ":ARM:ACQ:TIM?",
        ":ARM:ACQ:TIM %s",
        """ A float property (or string property representing an internally programmed default value) that configures the period/interval (in seconds) of the arm-level signal for the specified measurement device action. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[2e-5,1e5]]
    )
    trigger_period_source = Instrument.control(
        ":TRIG:TRAN:TIM?",
        ":TRIG:TRAN:TIM %s",
        """ A float property (or string property representing an internally programmed default value) that configures the period/interval (in seconds) of the trigger-level signal for the specified source device action. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[2e-5,1e5]]
    )
    arm_period_source = Instrument.control(
        ":ARM:TRAN:TIM?",
        ":ARM:TRAN:TIM %s",
        """ A float property (or string property representing an internally programmed default value) that configures the period/interval (in seconds) of the arm-level signal for the specified source device action. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[2e-5,1e5]]
    )
    trigger_period = Instrument.setting(
        ":TRIG:TIM %s",
        """ A float property (or string property representing an internally programmed default value) that sets the period/interval (in seconds) of the trigger-level signal for the specified source and measurement device actions. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[2e-5,1e5]]
    )
    arm_period = Instrument.setting(
        ":ARM:TIM %s",
        """ A float property (or string property representing an internally programmed default value) that sets the period/interval (in seconds) of the arm-level signal for the specified source and measurement device actions. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[2e-5,1e5]]
    )

    ########################
    # Arm / Trigger Signal #
    ########################

    trigger_signal_measure = Instrument.control(
        ":TRIG:ACQ:SOUR?",
        ":TRIG:ACQ:SOUR %s",
        """ A string property that selects the trigger-level measure signal to enable a specified device action. """,
        validator=strict_discrete_set,
        values={'auto':'AINT','bus':'BUS','time':'TIM','internal_1':'INT1','internal_2':'INT2','lan':'LAN','external_1':'EXT1','external_2':'EXT2','external_3':'EXT3','external_4':'EXT4','external_5':'EXT5','external_6':'EXT6','external_7':'EXT7','external_8':'EXT8','external_9':'EXT9','external_10':'EXT10','external_11':'EXT11','external_12':'EXT12','external_13':'EXT13','external_14':'EXT14'},
        map_values=True
    )
    arm_signal_measure = Instrument.control(
        ":ARM:ACQ:SOUR?",
        ":ARM:ACQ:SOUR %s",
        """ A string property that selects the arm-level measure signal to enable a specified device action. """,
        validator=strict_discrete_set,
        values={'auto':'AINT','bus':'BUS','time':'TIM','internal_1':'INT1','internal_2':'INT2','lan':'LAN','external_1':'EXT1','external_2':'EXT2','external_3':'EXT3','external_4':'EXT4','external_5':'EXT5','external_6':'EXT6','external_7':'EXT7','external_8':'EXT8','external_9':'EXT9','external_10':'EXT10','external_11':'EXT11','external_12':'EXT12','external_13':'EXT13','external_14':'EXT14'},
        map_values=True
    )
    trigger_signal_source = Instrument.control(
        ":TRIG:TRAN:SOUR?",
        ":TRIG:TRAN:SOUR %s",
        """ A string property that selects the trigger-level source signal to enable a specified device action. """,
        validator=strict_discrete_set,
        values={'auto':'AINT','bus':'BUS','time':'TIM','internal_1':'INT1','internal_2':'INT2','lan':'LAN','external_1':'EXT1','external_2':'EXT2','external_3':'EXT3','external_4':'EXT4','external_5':'EXT5','external_6':'EXT6','external_7':'EXT7','external_8':'EXT8','external_9':'EXT9','external_10':'EXT10','external_11':'EXT11','external_12':'EXT12','external_13':'EXT13','external_14':'EXT14'},
        map_values=True
    )
    arm_signal_source = Instrument.control(
        ":ARM:TRAN:SOUR?",
        ":ARM:TRAN:SOUR %s",
        """ A string property that selects the arm-level source signal to enable a specified device action. """,
        validator=strict_discrete_set,
        values={'auto':'AINT','bus':'BUS','time':'TIM','internal_1':'INT1','internal_2':'INT2','lan':'LAN','external_1':'EXT1','external_2':'EXT2','external_3':'EXT3','external_4':'EXT4','external_5':'EXT5','external_6':'EXT6','external_7':'EXT7','external_8':'EXT8','external_9':'EXT9','external_10':'EXT10','external_11':'EXT11','external_12':'EXT12','external_13':'EXT13','external_14':'EXT14'},
        map_values=True
    )
    trigger_signal = Instrument.setting(
        ":TRIG:SOUR %s",
        """ A string property that sets the trigger-level measure and source signals to enable a specified device action. """,
        validator=strict_discrete_set,
        values={'auto':'AINT','bus':'BUS','time':'TIM','internal_1':'INT1','internal_2':'INT2','lan':'LAN','external_1':'EXT1','external_2':'EXT2','external_3':'EXT3','external_4':'EXT4','external_5':'EXT5','external_6':'EXT6','external_7':'EXT7','external_8':'EXT8','external_9':'EXT9','external_10':'EXT10','external_11':'EXT11','external_12':'EXT12','external_13':'EXT13','external_14':'EXT14'},
        map_values=True
    )
    arm_signal = Instrument.setting(
        ":ARM:SOUR %s",
        """ A string property that sets the arm-level measure and source signals to enable a specified device action. """,
        validator=strict_discrete_set,
        values={'auto':'AINT','bus':'BUS','time':'TIM','internal_1':'INT1','internal_2':'INT2','lan':'LAN','external_1':'EXT1','external_2':'EXT2','external_3':'EXT3','external_4':'EXT4','external_5':'EXT5','external_6':'EXT6','external_7':'EXT7','external_8':'EXT8','external_9':'EXT9','external_10':'EXT10','external_11':'EXT11','external_12':'EXT12','external_13':'EXT13','external_14':'EXT14'},
        map_values=True
    )

     ###########
     # Current #
     ###########

    current = Instrument.measurement(
        ":MEAS:CURR?",
        """ Returns the measured current in Amps. """
    )
    current_nplc = Instrument.control(
        ":SENS:CURR:NPLC?",
        ":SENS:CURR:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). Values outside of these ranges are automatically trucated. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    current_compliance = Instrument.control(
        ":SENS:CURR:PROT:LEV?",
        ":SENS:CURR:PROT:LEV %g",
        """ A floating point property that controls the complaince current in Amps. """,
        validator=truncated_range,
        values=[-105e-3,105e-3]
    )
    current_in_compliance = Instrument.measurement(
        ":SENS:CURR:PROT:TRIP?",
        """ A boolean property that indicates if the current is in the compliance state or not. """,
        cast=bool
    )
    current_source = Instrument.control(
        ":SOUR:CURR?",
        ":SOUR:CURR %g",
        """ A floating point property that controls the source current in Amps. """
    )
    current_source_range = Instrument.control(
        ":SOUR:CURR:RANG?",
        ":SOUR:CURR:RANG %s",
        """ TODO """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[1e-8,10],["MIN","MAX","DEF"]]
    )
    current_source_range_auto = Instrument.control(
        ":SOUR:CURR:RANG:AUTO?",
        ":SOUR:CURR:RANG:AUTO %s",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1)
    )

    ###########
    # VOLTAGE #
    ###########

    voltage = Instrument.measurement(
        ":MEAS:VOLT?",
        """ Returns the measured voltage in Volts. """
    )
    voltage_nplc = Instrument.control(
        ":SENS:VOLT:NPLC?",
        ":SENS:VOLT:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC voltage measurements. This property sets the integration period and measurement speed. The input options are: `MIN`, `MAX`, `DEF`, or a numeric value between 4e-4 and 100 (50 Hz)/ 4.8e-4 and 120 (60 Hz). Values outside of these ranges are automatically trucated. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    voltage_compliance = Instrument.control(
        ":SENS:VOLT:PROT?",
        ":SENS:VOLT:PROT %g",
        """ A floating point property that controls the compliance voltage in Volts. """,
        validator=truncated_range,
        values=[-42, 42]
    )
    voltage_in_compliance = Instrument.measurement(
        ":SENS:VOLT:PROT:TRIP?",
        """ A boolean property that indicates if the voltage is in the compliance state or not. """,
        cast=bool
    )
    voltage_source = Instrument.control(
        ":SOUR:VOLT?",
        ":SOUR:VOLT %g",
        """ A floating point property that controls the source voltage in Volts. """,
        validator=truncated_range,
        values=[-42,42]
    )
    voltage_source_range = Instrument.control(
        ":SOUR:VOLT:RANG?",
        ":SOUR:VOLT:RANG %s",
        """ A floating-point/string property that controls the source voltage range in Volts. Auto-range is disabled when this property is set. """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[2e-1, 2e2],["MIN","MAX","DEF"]]
    )
    voltage_source_range_auto = Instrument.control(
        ":SOUR:VOLT:RANG:AUTO?",
        ":SOUR:VOLT:RANG:AUTO %i",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )

    ##############
    # Resistance #
    ##############

    resistance = Instrument.measurement(
        ":MEAS:RES?",
        """ Reads the resistance in Ohms. """
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
        """ An integer property that controls the number of wires used in resistance meaasurments. Accepts a value of `1` for the Kelvin (4 wire) connection or `0` for the standard (2 wire) connection. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    resistance_mode = Instrument.control(
        ":SENS:RES:MODE?",
        ":SENS:RES:MODE %g",
        """ A string parameter to set the resistance measurement mode to: automatic or manual. """,
        validator=strict_discrete_set,
        values={'automatic':'AUTO','manual':'MAN'},
        map_values=True
    )
    resistance_compensation = Instrument.control(
        ":SENS:RES:OCOM?",
        ":SENS:RES:OCOM %g",
        """ TODO """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )

    ################
    # Buffer Trace #
    ################

    buffer_points = Instrument.control(
        ":TRAC:POIN?",
        ":TRAC:POIN %d",
        """ An integer property that controls the number of buffer points ALLOWED in the instrument trace. This does not represent the actual number of points stored in the buffer, but is instead the configuration value. """,
        validator=truncated_range,
        values=[1, 100000],
        cast=int
    )
    buffer_length = Instrument.measurement(
        ":TRAC:POIN:ACT?",
        """ An integer property representing the actual number of points in the trace buffer. """,
        cast=int
    )
    buffer_feed = Instrument.control(
        ":TRAC:FEED?",
        ":TRAC:FEED %s",
        """ Specifies the data feed the trace buffer. This command is effective when the trace buffer control mode is :param never: by  :meth:`~.AgilentB2961A.buffer_control`. """,
        validator=strict_discrete_set,
        values={"sense":"SENS","math":"MATH","limit":"LIM"},
        map_values=True
    )
    buffer_control = Instrument.control(
        "TRAC:FEED:CONT?",
        "TRAC:FEED:CONT %s",
        """ Selects the trace buffer control. """,
        validator=strict_discrete_set,
        values={"next":"NEXT","never":"NEV"},
        map_values=True
    )
    buffer_get_data = Instrument.measurement(
        ":TRAC:DATA?",
        """ Reads the data from the trace buffer and returns the buffer data as a comma-seperated string. Control over which data is passed by the output is achieved with :attr:`~AgilentB2961A.buffer_data_header`.""",
        cast=float
    )
    buffer_data_header = Instrument.control(
        ":FORM:ELEM:SENS?",
        ":FORM:ELEM:SENS %s",
        """ A string attribute that describes which data is passed into the output of the query for the buffer data by  :attr:`~AgilentB2961A.buffer_get_stat_data_string`. """,
        validator=strict_discrete_set,
        values={"voltage":"VOLT","current":"CURR","resistance":"RES","time":"TIME","status":"STAT","source":"SOUR","electrical":"VOLT,CURR,RES","physical":"VOLT,CURR,RES,TIME","all":"VOLT,CURR,RES,TIME,STAT,SOUR"},
        map_values=True
    )
    buffer_get_stat_data = Instrument.measurement(
        ":TRAC:STAT:DATA?",
        """ Reads the statisical data from the trace buffer and returns the buffer data as a comma-seperated string. Control over which data is passed by the output is achieved with :attr:`~AgilentB2961A.buffer_stat_data_header`. """,
        cast=float
    )
    buffer_stat_data_header = Instrument.control(
        ":TRAC:STAT:FORM?",
        ":TRAC:STAT:FORM %s",
        """ A string attribute that describes which data is passed into the output of the query for the buffer statisical data by  :attr:`~AgilentB2961A.buffer_get_stat_data_string`. """,
        validator=strict_discrete_set,
        values={"mean":"MEAN","std_dev":"SDEV","range":"PKPK","min":"MIN","max":"MAX"},
        map_values=True
    )

    #
    #
    #

    def __init__(self, adapter, **kwargs):
        super(AgilentB2961A, self).__init__(adapter,
        "Agilent B2961A Source-Measurement Unit", **kwargs
        )

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)

    @property
    def buffer_clear(self):
        """ Clears data in the device trace buffer. """
        self.write(":TRAC:FEED:CONT NEV;:TRAC:CLE")

    def enable_source(self):
        """ Enables the source output. Depending on the instrument configuration, the source output is VOLT|CURR. """
        self.device_enable = 1

    def disable_source(self):
        """ Disables the source output. """
        self.device_enable = 0

    def measure_resistance(self, nplc=10, kelvin_connection=True, compensation=False):
        """ Configures the measurement of resistance.

        :param nplc: Number of power line cycles (NPLC) to integrate over; from 0.0004 to 100.
        :param kelvin_connection: Enables the 4-wire Kelvin resistance measurement.
        :param compensation: Enables the internal resistance measurement compensation. """
        log.info("%s is measuring resistance." % self.name)
        self.write(":SENS:FUNC RES;:SENS:RES:MODE MAN;:FORM:ELEM:SENS RES")
        self.resistance_nplc=nplc
        if kelvin_connection:
            self.resistance_connection=1
        else:
            self.resistance_connection=0
        if compensation:
            self.resistance_compensation=1
        else:
            self.resistance_compensation=0
        self.check_errors()

    def measure_voltage(self, nplc=10):
        """ Configures the measurement of voltage.

        :param nplc: Number of power line cycles (NPLC) to integrate over; from 0.0004 to 100.
        :param voltage: Upper limit of voltage in Volts; from -42 V to 42 V. This value is ignored when :param auto_range: is True.
        :param autorange: Enables auto_range of meter when True, else the upper limit is controlled by the value of :param voltage:. """
        log.info("%s is measuring voltage." % self.name)
        self.write(":SENS:FUNC VOLT;:FORM:ELEM:SENS VOLT")
        self.voltage_nplc = nplc
        self.check_errors()

    def measure_current(self, nplc=10):
        """ Configures the measurement of current.

        :param nplc: Number of power line cycles (NPLC) from 0.0004 to 100.
        :param current: Upper limit of current in Amps, from -105e-3 A and +105e-3 A.
        :param auto_range: Enables auto_range if True, else uses the value set by :param current:. """
        log.info("%s is measuring current." % self.name)
        self.write(":SENS:FUNC 'CURR';:FORM:ELEM CURR")
        self.current_nplc = nplc
        self.check_errors()

    def source_auto_range(self):
        """ Configures the source to use automatic ranging by :attr:`~AgilentB2961A.current_source_range_auto` or :attr:`~AgilentB2961A.voltage_source_range_auto`. """
        if self.source_mode == 'current':
            self.current_source_range_auto=1
        else:
            self.voltage_source_range_auto=1

    def apply_current(self, current, current_range=None, compliance_voltage=42):
        """ Configures the instrument to apply a souce current and uses and auto-range unless a current range is specified. The compliance voltage is also set.

        :param current_source: A :attr:`~AgilentB2961A.current_source` value.
        :param current_range: A :attr:`~AgilentB2961A.current_source_range` value or None. If None, the source auto-range is enabled by :attr:`~AgilentB2961A.current_source_range_auto`.
        :param compliance_voltage: A float in the correct range for a :attr:`~.AgilentB2961A.voltage_compliance`.
        """
        log.info("%s is sourcing current." % self.name)
        self.source_mode = "current"
        if current_range is None:
            self.current_source_range_auto=1
        else:
            self.current_source_range = current_range
        self.current_source = current
        self.voltage_compliance = compliance_voltage
        self.check_errors()

    def apply_voltage(self, voltage, voltage_range=None, compliance_current=0.1):
        """ Configures the instrument to apply a souce voltage and uses and auto-range unless a voltage range is specified. The compliance current is also set.

        :param voltage: A :attr:`~AgilentB2961A.voltage_source` value.
        :param voltage_range: A :attr:`~AgilentB2961A.voltage_source_range` value or None. If None, the source auto-range is enabled by :attr:`~AgilentB2961A.voltage_source_range_auto`.
        :param compliance_current: A float in the correct range for a :attr:`~.AgilentB2961A.current_compliance`.
        """
        log.info("%s is sourcing voltage." % self.name)
        self.source_mode = "voltage"
        if voltage_range is None:
            self.voltage_source_range_auto=1
        else:
            self.voltage_source_range = voltage_range
        self.voltage_source = voltage
        self.current_compliance = compliance_current
        self.check_errors()

    def beep(self, frequency=2e9, duration=1):
        """ Sounds a system beep.

        :param frequency: A frequency in Hz between 65 Hz and 2 MHz
        :param duration: A time in seconds between 0 and 7.9 seconds
        """
        self.write(":SYST:BEEP:STAT ON;:SYST:BEEP %f, %f" % (frequency, duration))

    def triad(self, base_frequency=2e6, duration=1):
        """ Sounds a musical triad using the system beep.

        :param base_frequency: A frequency in Hz between 65 Hz and 1.3 MHz
        :param duration: A time in seconds between 0 and 7.9 seconds
        """
        self.beep(base_frequency, duration)
        time.sleep(duration)
        self.beep(base_frequency*5.0/4.0, duration)
        time.sleep(duration)
        self.beep(base_frequency*6.0/4.0, duration)

    def reset(self):
        """ Resets the instrument and clears the queue.  """
        self.write("status:queue:clear;*RST;:stat:pres;:*CLS;")

    def timeout(self, milliseconds=None):
        """ Returns timeout value when :param milliseconds: is None, or sets new value when a :param milliseconds: value is passed. """
        if timeout is None:
            return(self.adapter.connection.timeout)
        else:
            self.adapter.connection.timeout=milliseconds

    @property
    def status_byte(self):
        """ TODO """
        return(self.ask(":FORM:SREG ASC;*STB?"))

    @property
    def trigger_is_idle(self):
        """ Checks the status of the specified device action and WAITS until the status is changed to idle. """
        if self.device_status_operation_condition == 1170:
            if self.ask(":IDLE?"):
                return((1,'Trigger in idle state.'))
            else:
                return(0, 'Trigger not in idle state.')
        else:
            return((0, 'Trigger not in idle state.'))

    @property
    def trigger(self):
        """ TODO """
        self.write(":ARM;:TRIG;:INIT;*TRG")

    @property
    def trigger_abort(self):
        """ Aborts the specified device action. Trigger status is set to idle. """
        self.write(":ABOR")

    @property
    def error(self):
        """ Reads and removes the top item in the error queue and returns a tuple of an error code and message from the single error. """
        err = self.values(":SYST:ERR?")
        if len(err) < 2:
            err = self.read() # Try reading again
        code = err[0]
        message = err[1].replace('"', '')
        return(code, message)

    def check_errors(self):
        """ Logs any system errors reported by the instrument. """
        code, message = self.error
        while code != 0:
            t = time.time()
            log.info("Agilent B2961a reported error: %d, %s" % (code, message))
            code, message = self.error
            if (time.time()-t)>10:
                log.warning("Timed out for Agilent B2961a error retrieval.")

    def shutdown(self):
        """ Ensures the current/voltage output is set to zero and disabled. """
        log.info("Shutting down the connection to %s." % self.name)
        if self.source_mode == 'current':
            self.current_source = 0.
        else:
            self.voltage_source = 0.
        self.disable_source()
