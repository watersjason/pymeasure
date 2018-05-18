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

class Agilent3458A(Instrument):
    """
    Represent the Agilent/Keysight 3458A digital multi-meter.

    .. code-block:: python

        multi_meter = Agilent3458A("GPIB::1::INSTR")   # Esablish the Agilent/Keysight B3458A source measurement device

        multi_meter.device_calibrate                    # Run the self calibtration

        TODO

    """

    ###############
    # Calibration #
    ###############

    calibration_internal = Instrument.setting(
        "ACAL %i",
        """ A string property that instructs the multimeter to perform a specified type of internal self calibration. Calibration security must be removed by :meth:`~Agilent3458A.calibration_secure`. """,
        validator=strict_discrete_set,
        values={'all':0, 'dc':1, 'ac':2, 'resistance':4},
        map_values=True
    )
    calibration_number = Instrument.measurement(
        "CALNUM?",
        """ An integer property indicating the number of times the multimeter has been calibrated. """,
        cast=int
    )
    calibration_string = Instrument.command(
        "CALSTR?",
        "CALSTR %s",
        """ A string property that is stored in the multimeter's nonvolatile calibration RAM. Recommended usage is to store the meter's internal temperature at the time of calibration, the date of calibration, and the scheduled date for the next calibration. """
    )
    calibration_secure = Instrument.setting(
        "SECURE %s",
        """ A string property of the form: `old_code, new_code[, acal_secure]`, where `old_code` is the previous security code, `new_code` is the new security code, and [,acal_secure] is an optional property to turn the autocalibration security `OFF` or `ON`.

        The string `3458,3458,OFF` maintains the default security code but disables the autocalibration security. Disabiling the autocalibration security is required to use :meth:`~Agilent3458A.calibrate_self`. """
    )
    device_temperature = Instrument.measurement(
        "TEMP?",
        """ Returns the internal temperature of the multimeter in degrees C. """
    )
    device_revision = Instrument.measurement(
        "REV?",
        """ A string property with the master and slave processor firmware revisions. """
    )


    #
    #
    #

    def __init__(self, adapter, **kwargs):
        super(AgilentB2961A, self).__init__(adapter,
        "Agilent 3458A Source-Measurement Unit", includeSCPI=False, **kwargs
        )

        self.adapter.connection.timeout = (kwargs.get('timeout', 5) * 1000)

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
