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
from pymeasure.instruments.validators import strict_discrete_set, strict_range
from numpy import array

class MettlerToledoSICS(Instrument):
    """ Implements the functions included the
        Mettler Toledo SICS programming manual.
        The SICS protocol is used by most modern
        Mettler Toledo balances.
    """
    # Select MT-SICS level 0 states
    device_version=Instrument.measurement(
        "I1",
        "A string parameter with the SICS level and version.")
    device_data=Instrument.measurement(
        "I2",
        "A string parameter of the balance data. Unit dependent reply.")
    device_software_version=Instrument.measurement(
        "I3",
        "A string parameter of the software version and type.")
    device_serial=Instrument.measurement(
        "I4",
        "A string parameter with the device serial number.",
        get_process=lambda v:v.split(' ')[-1])
    device_software_id=Instrument.measurement(
        "I5",
        "A string parameter with the software identification number.",
        get_process=lambda v:v.split(' ')[-1])
    send_stable=Instrument.measurement(
        "S",
        """ Cancel existing commands and send
            the next stable weighing result. """
    )
    send_immediate=Instrument.measurement(
        "SI",
        """ Cancel existing commands and send
            the immediate weighing result. """
    )
    zero_stable=Instrument.measurement(
        "Z",
        "Zero the balance when stable.")
    zero_immediate=Instrument.measurement(
        "ZI",
        "Zero now and ingore instability.")
    # level 1
    display_text=Instrument.setting(
        'D %s',
        """ Display text on the balance screen. """
    )
    tare_stable=Instrument.measurement(
        "T",
        """ Tare the balance when stable and
            return the value stored to the
            tare memory."""
    )
    tare_value=Instrument.control(
        "TA",
        "TA %s",
        """ A float property for the mass
            stored in the tare memory. """
    )
    tare_immediate=Instrument.measurement(
        "TI",
        """ Tare the balance immediately and
            return the new value stored to
            the tare memory."""
    )
    # Level 2
    calibration_mode=Instrument.control(
        "C0",
        "C0 %s",
        """ Inquiry of the calibration mode.
            An iterable property with the elements:
                mode        (`manual`|`auto`),
                cal_weigh   (`internal`,`external`) """
    )
    device_date=Instrument.control(
        "DAT",
        "DAT %s",
        """ TODO """
    )
    device_name=Instrument.control(
        "I10",
        "I10 %s",
        """ TODO """
    )
    device_model=Instrument.measurement(
        "I11",
        """ A string parameter of the balance model number. """
    )
    device_powerup=Instrument.setting(
        "PWR",
        """ An integer parameter to switch the balance
            to standby mode (0) or to switch it on (1)."""
    )
    device_time=Instrument.control(
        "TIM",
        "TIM %s",
        """ TODO """
    )
    door_state=Instrument.control(
        "WS",
        "WS %i",
        """ """,
        validator=strict_discrete_set,
        values={}
    )
    weighing_mode=Instrument.control(
        "M01",
        "M01 %i",
        """ """
    )
    weighing_environment=Instrument.control(
        "M02",
        "M02 %i",
        """ """
    )
    auto_zero_enable=Instrument.control(
        "M03",
        "M03 %i",
        """ An integer parameter to enable the
            balance AutoZero function."""
    )
    door_auto_enable=Instrument.control(
        "M07",
        "M07 %i",
        """ An integer parameter to enable the
            balance AutoDoor function. """
    )
    beep=Instrument.setting(
        "M12 %i",
        """ Create a tone. An integer parameter
            sets the tone variant. """
    )
    weighing_unit=Instrument.control(
        "M21",
        "M21 %s",
        """ TODO """
    )
    weighing_resolution=Instrument.control(
        "M23",
        "M23 %i",
        """ TODO """
    )
    calibration_history=Instrument.measurement(
        "M27",
        """ TODO """
    )
    temperature=Instrument.measurement(
        "M28",
        """ TODO """
    )
    weighing_stability_mode=Instrument.measurement(
        "M29",
        """ TODO """
    )

    def __init__(self,adapter,**kwargs):
        super(MettlerToledoSICS, self).__init__(
        adapter, "Generic Mettler Toledo SICS Balance",
        includeSCPI=False, **kwargs
        )

        self._cal_mode_val_set= {'manual':0,
                                 'auto':1}
        self._cal_mode_val_get=self._flip_dict(self._cal_mode_val_set)
        self._cal_weight_val_set=   {'internal':0,
                                     'external':1}
        self._cal_weight_val_get=self._flip_dict(self._cal_mode_val_set)

        self._door_get_states=  {0:'close',
                                 1:'open',
                                 2:'left',
                                 8:'error',
                                 9:'transion'}
        self._door_set_states=  {'close':0,
                                 'open':1,
                                 'left':2}

        self._weighing_mode_set_val= {'normal':0,
                                 'dosing':1,
                                 'other': 2}
        self._weighing_mode_get_val=self._flip_dict(
                                                self._weighing_mode_set_val)
        self._weighing_environment_set_val= {'very stable':  0,
                                             'stable':       1,
                                             'standard':     2,
                                             'unstable':     3,
                                             'very unstable':4}
        self._weighing_environment_get_val=self._flip_dict(
                                            self._weighing_environment_set_val)

        self._unit_designation_set_val= {'main':0,
                                         'display':1,
                                         'information':2}
        self._unit_designation_get_val=self._flip_dict(
                                        self._unit_designation_set_val)
        self._unit_set_val= {'gram':       0,
                             'kilogram':   1,
                             'milligram':  3,
                             'microgram':  4}
        self._unit_get_val=self._flip_dict(self._unit_set_val)

        self._weighing_resolution_set_val = {1:       0,
                                             10:      1,
                                             100:     2,
                                             1000:    3}
        self._weighing_resolution_get_val=self._flip_dict(
                                            self._weighing_resolution_set_val)

        self._weighing_stability_mode_set_val = {'very fast':       0,
                                                 'fast':            1,
                                                 'fast reliable':   2,
                                                 'reliable':        3,
                                                 'very reliable':   4}
        self._weighing_stability_mode_get_val=self._flip_dict(
                                        self._weighing_stability_mode_set_val)
    def _flip_dict(self, dictionary):
        """ Flips a dictionary keys to items and
            items to keys.
            Returns the fliped dictionary. """
        return {v:k for k,v in dictionary.items()}
    def _checker(self,command):
        """ Check the reply string from the SICs device.
            Loops through reading the buffer until the last
            line is read. """
        data = []
        data.append(self.ask(command).split())
        command = data[-1][0]
        condition = data[-1][1]

        while condition is not 'A':
            if condition is 'B' or command is 'SIR':
                data.append(self.read().split())
                command = data[-1][0]
                condition = data[-1][1]
            elif condition is '+':
                raise ValueError('Balance overload or upper limit exceeded.')
            elif condition is '-':
                raise ValueError('Balance underload or lower limit not met.')
            elif condition is 'I':
                raise VisaIOError('Command not executable at present.')
            elif condition is 'L':
                raise ValueError('Command correct, but has an incorrect value.')
            elif condition is 'R':
                break
            elif condition is 'S' and command is not 'SIR':
                return data
                break
            elif condition is 'D' and command is not 'SIR':
                return data
                break
            else:
                raise ValueError('Error processing values in device reply.')

        if len(data) == 1:
            return data[0]
        else:
            return data
    # level 1 properties
    @device_version.getter
    def device_version(self):
        return self._checker("I1")
    @device_data.getter
    def device_data(self):
        return self._checker("I3")
    @device_serial.getter
    def device_serial(self):
        return self._checker("I4")
    @device_software_id.getter
    def device_software_id(self):
        return _checker("I5")
    @send_stable.getter
    def send_stable(self):
        return _checker("S")
    @send_immediate.getter
    def send_immediate(self):
        return _checker("SI")
    @zero_stable.getter
    def zero_stable(self):
        return _checker("Z")
    @zero_immediate.getter
    def zero_immediate(self):
        return _checker("ZI")
    @property
    def reset(self):
        "Reset balance without zeroing."
        return self._checker("@")
    # level 2 properties
    @display_text.setter
    def display_text(self, message):
        return self._checker('D "{}"'.format(message))
    @property
    def display_weight(self):
        """ Switch main display to indicate weight. """
        return self._checker("DW")
    @tare_stable.getter
    def tare_stable(self):
        return self._checker("T")
    @tare_value.setter
    def tare_value(self,value_unit):
        try:
            value, unit = value_unit
        except ValueError:
            raise ValueError('Input `value_unit` is an iterable with elements:'
                             ' tare value, unit.')
        strict_range(value, (0, 220))
        strict_discrete_set(unit, ('g','mg'))
        return self._checker("TA {} {}".format(value, unit))
    @tare_value.getter
    def tare_value(self):
        _arg = self._checker("TA")
        return (float(_arg[-2]), _arg[-1])
    @property
    def tare_clear(self):
        """ Clear the value in the tare memory. """
        return self._checker("TAC")
    @tare_immediate.getter
    def tare_immediate(self):
        return self._checker("TI")
    # Level 3 properties
    @calibration_mode.setter
    def calibration_mode(self, mode_weight):
        try:
            mode, weight = mode_weight
        except ValueError:
            raise ValueError('An interable with values for the mode and '
                             'calibration weight must be passed.')

        strict_discrete_set(mode, list(self._cal_mode_val.keys()))
        strict_discrete_set(weight, list(self._cal_weight_val.keys()))

        return self._checker("C0 {} {}".format(self._cal_mode_val[mode],
                                               self._cal_weight_val[weight]))
    @calibration_mode.getter
    def calibration_mode(self):
        _arg=self._checker("C0")

        if len(_arg)==5:
            _mode=int(_arg[-3])
            _weight=int(_arg[-2])
        elif len(_arg)==6:
            _mode=int(_arg[-4])
            _weight=int(_arg[-3])
        else:
            raise ValueError('TODO')

        return self._cal_mode_val_get[_mode], self._cal_weight_val_get[_weight]
    @property
    def calibration_internal(self):
        """ Initiate an internal calibration. """
        _time=self.adapter.connection.timeout
        self.adapter.connection.timeout=120000
        _out = self._checker("C3")[-1][1]
        self.adapter.connection.timeout=_time
        return _out=='A'
    @device_date.getter
    def device_date(self):
        return self._checker("DAT")[-3:]
    @device_date.setter
    def device_date(self,dd_mm_yyyy):
        try:
            dd, mm, yyyy = dd_mm_yyyy
        except ValueError:
            raise ValueError('Input must be of the form: [dd, mm, yyyy].')
        strict_range(int(dd),(1,31))
        strict_range(int(mm),(1,12))
        strict_range(int(yyyy),(2000,3000))
        return self._checker("DAT {} {} {}".format(int(dd),int(mm),int(yyyy)))
    @device_name.getter
    def device_name(self):
        return self._checker("I10")[-1]
    @device_name.setter
    def device_name(self,name_str):
        if len(str) > 20:
            raise ValueError("Name must be less than 20 characters.")
        return self._checker("I10 {}".format(name_str))
    @device_model.getter
    def device_model(self):
        return self._checker("I11")[-1]
    @device_powerup.setter
    def device_powerup(self,powerup):
        strict_discrete_set(powerup,(0,1))
        return self._checker("PWR {}".format(powerup))
    @device_time.setter
    def device_time(self,hh_mm_ss):
        try:
            hh, mm, ss = hh_mm_ss
        except ValueError:
            raise ValueError('Must pass an iterable of the form:'
                             ' [hh, mm, ss].')
        strict_range(int(hh),(0,24))
        strict_range(int(mm),(0,60))
        strict_range(int(ss),(0,60))
        return self._checker("TIM {} {} {}".format(int(hh),int(mm),int(ss)))
    @device_time.getter
    def device_time(self):
        return self._checker("TIM")[-3:]
    @door_state.setter
    def door_state(self,state):
        strict_discrete_set(state, list(self._door_set_states.keys()))
        return self._checker("WS {}".format(self._door_set_states[state]))
    @door_state.getter
    def door_state(self):
        _arg=int(self._checker("WS")[-1])
        return self._door_get_states[_arg]
    @weighing_mode.setter
    def weighing_mode(self,mode):
        strict_discrete_set(mode, self._weighing_modes.keys())
        self._checker("M01 {}".format(_weighing_modes[mode]))
    @weighing_mode.getter
    def weighing_mode(self):
        _arg=int(self._checker("M01")[-1])
        return self._weighing_modes_get[_arg]
    @weighing_environment.setter
    def weighing_environment(self,environment):
        strict_discrete_set(environment,self._weighing_mode_set_val.keys())
        self._checker("M02 {}".format(self._weighing_environment_set_val[
                                                                environment]))
    @weighing_environment.getter
    def weighing_environment(self):
        _arg=int(self._checker("M02")[-1])
        return self._weighing_environment_get_val[_arg]
    @auto_zero_enable.setter
    def auto_zero_enable(self,state):
        strict_discrete_set(state,(0,1))
        self._checker("M03 {}".format(state))
    @auto_zero_enable.getter
    def auto_zero_enable(self):
        return int(selt._checker("M03"))
    @door_auto_enable.setter
    def door_auto_enable(self,state):
        strict_discrete_set(state,(0,1))
        self._checker("M07 {}".format(state))
    @door_auto_enable.getter
    def door_auto_enable(self):
        return int(selt._checker("M07"))
    @beep.setter
    def beep(self,tone):
        strict_discrete_set(tone,(0,1,2))
        self._checker("M12 {}".format(tone))
    @weighing_unit.setter
    def weighing_unit(self,designation_unit):
        try:
            designation, unit = designation_unit
        except ValueError:
            raise ValueError('Input must be an interatble with '
                             'values: `designation`, `unit`.')
        strict_discrete_set(desination, self._unit_designation_set_val)
        strict_discrete_set(unit, self._unit_set_val)
        self._checker("M21 {} {}".format(
                                    self._unit_designation_set_val[desination],
                                    self._unit_set_val[unit]))
    @weighing_unit.getter
    def weighing_unit(self):
        _arg=self._checker("M21")[-2:]
        return (self._unit_designation_get_val[int(_arg[0])],
                self._unit_get_val[int(_arg[1])])
    @weighing_resolution.setter
    def weighing_resolution(self, resolution):
        strict_discrete_set(resolution,self._weighing_resolution_set_val.keys())
        self._checker("M23 {}".format(
                                self._weighing_resolution_set_val[resolution]))
    @weighing_resolution.getter
    def weighing_resolution(self):
        return self._weighing_resolution_get_val[int(self._checker("M23")[-1])]
    @calibration_history.getter
    def calibration_history(self):
        return self._checker("M27")
    @temperature.getter
    def temperature(self):
        return [float(i) for i in array(self._checker("M28"))[:,-1]]
    @weighing_stability_mode.setter
    def weighing_stability_mode(self,mode):
        strict_discrete_set(mode,self._weighing_stability_mode_set_val.keys())
        self._checker("M29 {}".format(
                                self._weighing_stability_mode_set_val[mode]))
    @weighing_stability_mode.getter
    def weighing_stability_mode(self):
        return self._weighing_stability_mode_get_val[
                                                int(self._checker("M29")[-1])]
