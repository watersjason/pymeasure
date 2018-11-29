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
                                              joined_validators)

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
            the next stable weighing result. """,
        get_process=lambda v:v.split()[1]
    )
    send_immediate=Instrument.measurement(
        "SI",
        """ Cancel existing commands and send
            the immediate weighing result. """,
        get_process=lambda v:v.split()[1]
    )
    zero=Instrument.measurement(
        "Z",
        "Zero the balance when stable.")
    zero_immediate=Instrument.measurement(
        "ZI",
        "Zero now and ingore instability.")
    reset=Instrument.setting(
        "@",
        "Reset balance without zeroing.")
    # level 1
    display_text=Instrument.setting(
        'D %s',
        """ Display text on the balance screen. """
    )
    tare_stable=Instrument.measurement(
        "T",
        """ Tare the balance when stable and
            return the value stored to the
            tare memory.""",
        get_process=lambda v:v.split()[-2]
    )
    tare_value=Instrument.control(
        "TA",
        "TA %s",
        """ A float property for the mass
            stored in the tare memory. """,
        unit=kwargs.get('unit','g'),
        set_process=lambda v:'{} {}'.format(v,unit),
        get_process=lambda v:v.split()[-2]
    )
    tare_immediate=Instrument.measurement(
        "TI",
        """ Tare the balance immediately and
            return the new value stored to
            the tare memory.""",
        get_process=lambda v:v.split()[-2]
    )
    # Level 2
    calibration_setting=Instrument.control(
        "CO",
        "CO %s",
        """ TODO """,
        validator=strict_discrete_set,
        values={'manual internal':[0,0],
                'manual external':[0,1],
                'automatic internal':[1,0],
                'automatic external':[1,1]},
        map_values=True,
        get_process=lambda v:v.split()[2:3],
        set_process=lambda v:'{} {}'.format(v[0],v[1])
    )
    date=Instrument.control(
        "DAT",
        "DAT %s",
        """ TODO """
    )
    time=Instrument.control(
        "TIM",
        "TIM %s",
        """ TODO """
    )
    door_state=Instrument.control(
        "WS",
        "WS %i",
        """ """,
        validator=strict_discrete_set,
        values={'close':        0,
                'right':        1,
                'left':         2,
                'error':        8,
                'intermediate': 9},
        map_values=True,
        get_process=lambda v:v.split()[-1]
    )
    mode=Instrument.control(
        "M01",
        "M01 %i",
        """ """,
        validator=strict_discrete_set,
        values={'normal':0,
                'dosing':1,
                'other': 2},
        map_values=True
    )
    environment=Instrument.control(
        "M02",
        "M02 %i",
        """ """,
        validator=strict_discrete_set,
        values={'very stable':  0,
                'stable':       1,
                'standard':     2,
                'unstable':     3,
                'very unstable':4},
        map_values=True
    )
    auto_zero_enable=Instrument.control(
        "M03",
        "M03 %i",
        """ An integer parameter to enable the
            balance AutoZero function.""",
        validator=strict_discrete_set,
        values=(0,1)
    )
    door_auto_enable=Instrument.control(
        "M07",
        "M07 %i",
        """ An integer parameter to enable the
            balance AutoDoor function. """,
        validator=strict_discrete_set,
        values=(0,1)
    )
    beep=Instrument.setting(
        "M12 %i",
        """ Create a tone. An integer parameter
            sets the tone variant. """,
        validator=strict_discrete_set,
        values=(0,1,2)
    )
    unit=Instrument.control(
        "M21",
        "M21 %s",
        """ TODO """,
        set_process=lambda v:'{} {}'.format(unit_field,v),
        get_process=lambda v:v.split()[-1],
        validator=strict_discrete_set,
        values={'gram':       0,
                'kilogram':   1,
                'milligram':  3,
                'microgram':  4},
        map_values=True
    )
    resolution=Instrument.control(
        "M23",
        "M23 %i",
        """ TODO """,
        validator=strict_discrete_set,
        values={'1d':       0,
                '10d':      1,
                '100d':     2,
                '1000d':    3},
        map_values=True,
        get_process=lambda v:v.split()[-1]
    )
    calibration_history=Instrument.measurement(
        "M27",
        """ TODO """
    )
    temperature=Instrument.measurement(
        "M28",
        """ TODO """
    )
    stability_mode=Instrumentmeasurement(
        "M29",
        """ TODO """
    )
    
    def __init__(self,adapter,**kwargs):
        super(MettlerToledoSICS, self).__init__(
        adapter, "Generic Mettler Toledo SICS Balance",
        includeSCPI=False, **kwargs
        )
    # level 2 properties
    @property
    def display_weight(self):
        """ Switch main display to indicate weight. """
        self.write("DW")
    @property
    def tare_clear(self):
        """ Clear the value in the tare memory. """
        self.write("TAC")
    # Level 3
    @property
    def calibration_init(self):
        """ Initiate an internal calibration. """
        self.write("C3") # TODO thread + loop
