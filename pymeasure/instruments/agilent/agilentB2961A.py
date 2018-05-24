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

    Might work with other units in the B2900 series, but only in the limited current/voltage source/measure ranges allowed by the B2961A.

    .. code-block:: python

        source_measure_unit = AgilentB2961A("GPIB::1::INSTR")   # Esablish the Agilent/Keysight B2961A source measurement device

        source_measure_unit.device_calibrate                    # Run the self calibtration

        source_measure_unit.source_mode = 'current'             # Set the output to current

        source_measure_unit.current_source_level = 10e-3              # Set the source output current to 10 mA

        source_measure_unit.enable_source                       # Enable source output of the 10 mA current signal

        source_measure_unit.shutdown()                          # Ramp the current to 0 mA and disable output

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
        """ Enables or disables the source output. """,
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
        """ A query command to perform the self-calibtration. """
    )
    device_test = Instrument.measurement(
        "*TST?",
        """ A query command to perform the self-test. """
    )
    device_protection = Instrument.control(
        ":OUTP:PROT?",
        ":OUTP:PROT %i",
        """ An integer property that enables/disables the over voltage/current protection. If enabled and source reaches the set compliance level, then the source immediately and automatically is set to 0 volts/amperes and the output is switched off. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    device_nplc = Instrument.control(
        ":SENS:CURR:NPLC?",
        ":SENS:CURR:NPLC %s",
        """ A floating point property that controls the number of power line cycles (NPLC) for the DC current measurements. This property sets the integration period and measurement speed. NPLC is a common value for the current, voltage and resistance measurements. """,
        validator=joined_validators(strict_discrete_set, truncated_range),
        values=[['MIN','DEF','MAX'],[4e-4,120]]
    )
    device_nplc_auto = Instrument.control(
        ":SENS:CURR:NPLC:AUTO?",
        ":SENS:CURR:NPLC:AUTO %g",
        """ A boolean parameter that enables or disables the auto NPLC function. When enables, the NPLC is calculated from the measurement range. Auto-NPLC is a common value for the current, voltage and resistance measurements. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=bool
    )
    device_status_operation_condition = Instrument.measurement(
        ":FORM:SREG ASC;:STAT:OPER:COND?",
        """ A string parameter (ASCII format) that returns the device operating condition status. """,
        cast=int
    )
    output_off_mode = Instrument.control(
        ":OUTP:OFF:MODE?",
        ":OUTP:OFF:MODE %s",
        """ A string parameter that configures the device output off mode. """,
        validator=strict_discrete_set,
        values={'zero':'ZERO','high_impedance':'HIZ','normal':'NORM'},
        map_values=True
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
        """ Enables or disables the automatic output off function. If this function is enabled, the source output is automatically and immediately turned off when the grouped channels change status from busy to idle. """,
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
        """ A float property (the delay value in seconds, or a string representing an internally programmed default value) for the trigger-level measurement (acquisition) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    arm_delay_measure = Instrument.control(
        ":ARM:ACQ:DEL?",
        ":ARM:ACQ:DEL %s",
        """ A float property (the delay value in seconds, or a string representing an internally programmed default value) for the arm-level measurement (acquisition) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    trigger_delay_source = Instrument.control(
        ":TRIG:TRAN:DEL?",
        ":TRIG:TRAN:DEL %s",
        """ A float property (the delay value in seconds, or a string representing an internally programmed default value) for the trigger-level source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    arm_delay_source = Instrument.control(
        ":ARM:TRAN:DEL?",
        ":ARM:TRAN:DEL %s",
        """ A float property (the delay value in seconds, or a string representing an internally programmed default value) for the arm-level source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    trigger_delay = Instrument.setting(
        ":TRIG:DEL %s",
        """ A float property (the delay value in seconds, or a string representing an internally programmed default value) for the trigger-level measurement (acquire) and source (transient) signals. """,
        validator=joined_validators(strict_discrete_set,truncated_range),
        values=[{'min':'MIN','max':'MAX','default':'DEF'},[0,1e6]],
        cast=int
    )
    arm_delay = Instrument.setting(
        ":ARM:DEL %s",
        """ A float property (the delay value in seconds, or a string representing an internally programmed default value) for the arm-level measurement (acquire) and source (transient) signals. """,
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
    current_source_level = Instrument.control(
        ":SOUR:CURR?",
        ":SOUR:CURR %g",
        """ A floating point property that controls the source current level in Amps. """
    )
    current_source_level_trigger = Instrument.control(
        ":SOUR:CURR:TRIG?",
        ":SOUR:CURR:TRIG %g",
        """ A floating point property that controls the source current level for the triggered device in Amps. """
    )
    current_source_range = Instrument.control(
        ":SOUR:CURR:RANG?",
        ":SOUR:CURR:RANG %s",
        """ A floating-point/string property that controls the source current range in Amperes. :attr:`~AgilentB2961A.current_source_range_auto` is disabled when this property is set. """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[1e-8,10],["MIN","MAX","DEF"]]
    )
    current_source_range_auto = Instrument.control(
        ":SOUR:CURR:RANG:AUTO?",
        ":SOUR:CURR:RANG:AUTO %s",
        """ An integer parameter that enables/disables the current source auto-ranging function. """,
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
    voltage_source_level = Instrument.control(
        ":SOUR:VOLT?",
        ":SOUR:VOLT %g",
        """ A floating point property that controls the source voltage level in Volts. """,
        validator=truncated_range,
        values=[-42,42]
    )
    voltage_source_level_trigger = Instrument.control(
        ":SOUR:VOLT:TRIG?",
        ":SOUR:VOLT:TRIG %g",
        """ A floating point property that controls the source voltage level for the triggered device in Volts. """,
        validator=truncated_range,
        values=[-42,42]
    )
    voltage_source_range = Instrument.control(
        ":SOUR:VOLT:RANG?",
        ":SOUR:VOLT:RANG %s",
        """ A floating-point/string property that controls the source voltage range in Volts. :attr:`~AgilentB2961A.voltage_source_range_auto` is disabled when this property is set. """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[2e-1, 2e2],["MIN","MAX","DEF"]]
    )
    voltage_source_range_auto = Instrument.control(
        ":SOUR:VOLT:RANG:AUTO?",
        ":SOUR:VOLT:RANG:AUTO %i",
        """ An integer parameter that enables/disables the voltage source auto-ranging function. """,
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
    resistance_connection = Instrument.control(
        ":SENS:REM?",
        ":SENS:REM %d",
        """ An integer property that controls the connection type (2 wires versus 4 wires) used in resistance measurement. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )
    resistance_compensation = Instrument.control(
        ":SENS:RES:OCOM?",
        ":SENS:RES:OCOM %g",
        """ An integer property that enables/disables the offset-compensation for the resistance measurement. """,
        validator=strict_discrete_set,
        values=(0,1),
        cast=int
    )

    ################
    # Buffer Trace #
    ################

    buffer_points = Instrument.control(
        ":TRAC:POIN?",
        ":TRAC:POIN %s",
        """ An integer property that controls the number of buffer points ALLOWED in the instrument trace. This does not represent the actual number of points stored in the buffer, but is instead the configuration value. """,
        validator=joined_validators(truncated_range,strict_discrete_set),
        values=[[1, 1e6],{'max':'MAX','min':'MIN','default':'DEF'}],
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

    def __init__(self, adapter, **kwargs):
        super(AgilentB2961A, self).__init__(adapter,
        "Agilent B2961A Source-Measurement Unit", **kwargs
        )

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)

    def trigger_configure(self, source_mode, source_level, compliance_level, measure_mode='all', nplc='auto', kelvin_connection=True, compensation=False, device_float='float', clear_buffer=True, buffer_points='max', buffer_feed='sense', buffer_control='next', trigger_count='infinity', trigger_delay=0, trigger_period=1, trigger_signal='auto', arm_count='min', arm_delay=0, arm_period='default', arm_signal='auto', output_off_mode='normal', output_auto_out_enable=1, output_auto_out_disable=0):
        """ A convenience function to configure the device for triggering a source-measure event and the measurement data collected in the buffer.

        :param source_mode: A :attr:`~AgilentB2961A.source_mode` value.
        :param source_level: Depending on :param source_mode:, the value is interpreted as a :attr:`~AgilentB2961A.current_source_level` (amperes) or :attr:`~AgilentB2961A.voltage_source_level` (volts) value.
        :param compliance_level: Depending on :param source_mode:, the value is interpreted as a :attr:`~AgilentB2961A.current_compliance` (amperes) or :attr:`~AgilentB2961A.voltage_compliance` (volts) value.
        :param measure_mode: A :attr:`~AgilentB2961A.measure_mode` value.
        :param nplc: A value that configures the :attr:`~AgilentB2961A.device_nplc`, :attr:`~AgilentB2961A.device_nplc`, and :attr:`~AgilentB2961A.device_nplc`.
        :param kelvin_connection: A :attr:`~AgilentB2961A.resistance_connection` value.
        :param compensation: A :attr:`~AgilentB2961A.resistance_compensation` value.
        :param buffer_points: A :attr:`~AgilentB2961A.buffer_points` value.
        :param buffer_feed: A :attr:`~AgilentB2961A.buffer_feed` value.
        :param buff_control: A :attr:`~AgilentB2961A.buffer_control` value.
        :param trigger_count: A :attr:`~AgilentB2961A.trigger_count` value.
        :param trigger_delay: A :attr:`~AgilentB2961A.trigger_delay` value.
        :param trigger_period: A :attr:`~AgilentB2961A.trigger_period` value.
        :param trigger_signal: A :attr:`~AgilentB2961A.trigger_signal` value.
        :param arm_count: A :attr:`~AgilentB2961A.arm_count` value.
        :param arm_delay: A :attr:`~AgilentB2961A.arm_delay` value.
        :param arm_period: A :attr:`~AgilentB2961A.arm_period` value.
        :param arm_signal: A :attr:`~AgilentB2961A.arm_signal` value.
        :param output_off_mode: A :attr:`~AgilentB2961A.output_off_mode` value.
        :param output_auto_out_enable: A :attr:`~AgilentB2961A.output_auto_out_enable` value.
        :param output_auto_out_disable: A :attr:`~AgilentB2961A.output_auto_out_disable` value.
        """
        self.source_mode=source_mode
        if source_mode is 'current':
            self.current_source_level=source_level
            self.current_source_level_trigger=source_level
            self.voltage_compliance=compliance_level
            self.current_source_range_auto=1
        else:
            self.voltage_source_level=source_level
            self.voltage_source_level_trigger=source_level
            self.current_compliance=compliance_level
            self.voltage_source_range_auto=1

        self.write(':SENS:FUNC:ALL')

        if nplc == 'auto':
            self.device_nplc_auto=True
        else:
            self.device_nplc=nplc

        self.resistance_connection=kelvin_connection
        self.resistance_compensation=compensation
        self.device_float=device_float

        if clear_buffer:
            self.buffer_clear
        self.buffer_points=buffer_points
        self.buffer_feed=buffer_feed
        self.buffer_control=buffer_control

        self.trigger_count=trigger_count
        self.trigger_delay=trigger_delay
        self.trigger_period=trigger_period
        self.trigger_signal=trigger_signal

        self.arm_count=arm_count
        self.arm_delay=arm_delay
        self.arm_period=arm_period
        self.arm_signal=arm_signal

        self.output_off_mode=output_off_mode
        if output_auto_out_enable is not None:
            self.output_auto_out_enable=output_auto_out_enable
        if output_auto_out_disable is not None:
            self.output_auto_out_disable=output_auto_out_disable

    def measure_resistance(self, nplc=10, kelvin_connection=True, compensation=False, device_float='float'):
        """ Configures the measurement of resistance.

        :param nplc: A :attr:`~AgilentB2961A.device_nplc` value.
        :param kelvin_connection: A :attr:`~AgilentB2961A.resistance_connection` value.
        :param compensation: A :attr:`~AgilentB2961A.resistance_compensation` value.
        """
        log.info("%s is measuring resistance." % self.name)
        self.write(":SENS:FUNC RES;:SENS:RES:MODE MAN;:FORM:ELEM:SENS RES")
        self.device_nplc=nplc
        self.device_float=device_float
        if kelvin_connection:
            self.resistance_connection=1
        else:
            self.resistance_connection=0
        if compensation:
            self.resistance_compensation=1
        else:
            self.resistance_compensation=0
        self.check_errors

    def measure_voltage(self, auto_range=True, nplc=10, device_float='float'):
        """ Configures the measurement of voltage.

        :param nplc: A :attr:`~AgilentB2961A.device_nplc` value.
        :param autorange: A :attr:`~AgilentB2961A.voltage_source_range_auto` value.
        """
        log.info("%s is measuring voltage." % self.name)
        self.write(":SENS:FUNC VOLT;:FORM:ELEM:SENS VOLT")
        self.device_nplc = nplc
        self.device_float=device_float
        self.check_errors

    def measure_current(self, auto_range=True, nplc=10, device_float='float'):
        """ Configures the measurement of current.

        :param nplc: A :attr:`~AgilentB2961A.device_nplc` value.
        :param auto_range: A :attr:`~AgilentB2961A.current_source_range_auto` value.
        """
        log.info("%s is measuring current." % self.name)
        self.write(":SENS:FUNC 'CURR';:FORM:ELEM CURR")
        self.device_nplc = nplc
        self.device_float=device_float
        self.check_errors

    def source_auto_range(self):
        """ Configures the source to use automatic ranging by :attr:`~AgilentB2961A.current_source_range_auto` or :attr:`~AgilentB2961A.voltage_source_range_auto`. """
        if self.source_mode == 'current':
            self.current_source_range_auto=1
        else:
            self.voltage_source_range_auto=1

    def apply_current(self, current, current_range=None, compliance_voltage=42, device_float='float'):
        """ Configures the instrument to apply a souce current and uses and auto-range unless a current range is specified. The compliance voltage is also set.

        :param current_source_level: A :attr:`~AgilentB2961A.current_source_level` value.
        :param current_range: A :attr:`~AgilentB2961A.current_source_range` value. If None, then :attr:`~AgilentB2961A.current_source_range_auto` enables the auto-range.
        :param compliance_voltage: A :attr:`~.AgilentB2961A.voltage_compliance` value.
        """
        log.info("%s is sourcing current." % self.name)
        self.source_mode = "current"
        if current_range is None:
            self.current_source_range_auto=1
        else:
            self.current_source_range = current_range
        self.device_float = device_float
        self.current_source_level = current
        self.voltage_compliance = compliance_voltage
        self.check_errors

    def apply_voltage(self, voltage, voltage_range=None, compliance_current=0.1, device_float='float'):
        """ Configures the instrument to apply a souce voltage and uses and auto-range unless a voltage range is specified. The compliance current is also set.

        :param voltage: A :attr:`~AgilentB2961A.voltage_source_level` value.
        :param voltage_range: A :attr:`~AgilentB2961A.voltage_source_range` value. If None, then :attr:`~AgilentB2961A.voltage_source_range_auto` enables the auto-range.
        :param compliance_current: A :attr:`~.AgilentB2961A.current_compliance` value.
        """
        log.info("%s is sourcing voltage." % self.name)
        self.source_mode = "voltage"
        if voltage_range is None:
            self.voltage_source_range_auto=1
        else:
            self.voltage_source_range = voltage_range
        self.device_float = device_float
        self.voltage_source_level = voltage
        self.current_compliance = compliance_current
        self.check_errors

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

    def timeout(self, milliseconds=None):
        """ Returns timeout value when :param milliseconds: is None, or sets new value when a :param milliseconds: value is passed. """
        if timeout is None:
            return(self.adapter.connection.timeout)
        else:
            self.adapter.connection.timeout=milliseconds

    @property
    def reset(self):
        """ Resets the instrument and clears the queue.  """
        self.write("status:queue:clear;*RST;:stat:pres;:*CLS;")

    @property
    def buffer_clear(self):
        """ Clears data in the device trace buffer. """
        self.write(":TRAC:FEED:CONT NEV;:TRAC:CLE")

    @property
    def enable_source(self):
        """ Enables the source output. """
        self.device_enable = 1

    @property
    def disable_source(self):
        """ Disables the source output. """
        self.device_enable = 0

    @property
    def status_byte(self):
        """ Queries the device status byte and returns it in ASCII format. """
        return(self.ask(":FORM:SREG ASC;*STB?"))

    @property
    def trigger_is_idle(self):
        """ Checks the status of the status operation condition and device trigger. Will WAIT until the status is changed to idle or device timeout occurs. """
        if self.device_status_operation_condition == 1170:
            if self.ask(":IDLE?"):
                return((1,'Trigger in idle state.'))
            else:
                return(0, 'Trigger not in idle state.')
        else:
            return((0, 'Trigger not in idle state.'))

    @property
    def trigger(self):
        """ Sends command to arm, initialize, and trigger the device.  """
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

    @property
    def shutdown(self):
        """ Ensures the current/voltage output is set to zero and disabled. Sends an abort command to the device trigger. """
        log.info("Shutting down the connection to %s." % self.name)
        if self.source_mode == 'current':
            self.current_source_level = 0.
        else:
            self.voltage_source_level = 0.
        if not self.trigger_is_idle[0]:
            trigger_abort
        self.disable_source
