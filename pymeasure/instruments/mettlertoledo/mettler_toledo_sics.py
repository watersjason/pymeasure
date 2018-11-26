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
    zero=Instrument.measurement(
        "Z",
        "Zero the balance when stable.")
    zero_immediate=Instrument.measurement(
        "ZI",
        "Zero now and ingore instability.")
    reset=Instrument.setting(
        "@",
        "Reset balance without zeroing.")


    def __init__(self,adapter,**kwargs):
        super(MettlerToledoSICS, self).__init__(adapter,
        "Generic Mettler Toledo SICS Balance",
        includeSCPI=False,
        **kwargs)
    @property
    def send_stable(self,full_output=False):
        """ Cancel any existing commands and send the next stable
            weighing result.

            :param full_output: A boolean parameter that enables output
                                of the device full output string. When `False`,
                                the numeric weighing value is returned.
        """
        _data_str=self.ask("S")
        if _data_str is "S":
            raise VisaIOError("Value not read from device.")
        if full_output:
            return(_data_str)
        else:
            try:
                return(float(_data_str.split()[1]))
            except:
                raise ValueError("Value could not be converted to float.")
    @property
    def send_immediate(self,full_output=False):
    """ Cancel any existing commands and send the weighing
        result immediately.

        :param full_output: A boolean parameter that enables output
                            of the device full output string. When `False`,
                            the numeric weighing value is returned.
    """
    _data_str=self.ask("SI")
    if _data_str is "SI":
        raise VisaIOError("Value could not be read from device.")
    if full_output:
        return(_data_str)
    else:
        try:
            return(float(_data_str.split()[1]))
        except:
            raise ValueError("Value could not be converted to float.")
    measure_repeatidly=Instrument.measurement(
        "SIR",
        "Repeatedly measure & immediately send weight.")
