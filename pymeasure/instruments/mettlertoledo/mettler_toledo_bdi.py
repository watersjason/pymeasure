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

class MettlerToledoBDI(Instrument):
    """ Implements the functions included the
        Mettler Toledo Bidirectional Data Interface
        programming manual. The SICS protocol is
        used by most modern Mettler Toledo balances.
    """
    door_auto_mode=Instrument.control(
        "AD ?",
        "AD %i",
        """ A boolean parameter that enables or disables
            the automatic draft shield operation.
        """,
        validator=strict_discrete_set,
        values=(0,1),
        get_process = lambda cmd: int(cmd.strip().split('=')[-1])
    )
    weight_offset_value=Instrument.setting(
        "B %f",
        "A float value subtracted from all future weighing results.",
        validator=truncated_range,
        values=[0,20]
    )
    calibration_mode=Instrument.control(
        "CA ?",
        "CA %s",
        """ A string parameter that enables the automatic
            calibration, disables the automatic calibration,
            sets the calibration mode to an external user
            calibration, or starts an internal calibration.
        """,
        validator=strict_discrete_set,
        values={"auto off":"0",
                "auto on":"1",
                "external":"U",
                "internal":"T"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    calibration_status=Instrument.measurement(
        "CA S",
        """ A string parameter representing the
            current calibration status.
        """,
        values={"idle":"CA=I",
                "waiting to calibrate":"CA=W",
                "running auto calibration":"CA=CA",
                "running user calibration":"CA=CX",
                "running calibration":"CA=CT",
                "completing calibration":"CAL END",
                "starting calibration":"CAL BEGIN"},
        map_values=True
    )
    config_unlock=Instrument.control(
        "CFG ?",
        "CFG %i",
        """ An integer parameter that allows access
            to reset the default configuration.
        """,
        validator=strict_discrete_set,
        values=(0,1),
        get_process=lambda v:int(v.split("=")[-1])
    )
    display_text=Instrument.setting(
        "D %s",
        "Display a message on the balance panel."
    )
    generate_sound=Instrument.setting(
        "%s",
        """ A string parameter that causes
            the device to generate sound.""",
        validator=strict_discrete_set,
        values={"suppress":"DB 0",
                "short":"DB",
                "long":"DB 1",
                "double":"DB 2",
                "mixed":"DB 3",
                "termination":"DB C",
                "error":"DB E"},
        map_values=True
    ) # TODO: physical test times out
    display_status=Instrument.control(
        "DST ?",
        "DST %s",
        """ Control behavior of the status indicators for:
            vibration adapter, weighing process adapter,
            and the device interface.
        """,
        validator=strict_discrete_set,
        values={"clear":"0",
                "keep":"1",
                "temporary":"A"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    display_state=Instrument.setting(
        "DSX %s",
        """ A string parameter that selects active
            display if an auxiliary display is attached.
        """,
        validator=strict_discrete_set,
        values={"both":"0",
                "main":"1",
                "auxiliary":"2"},
        map_values=True
    )
    command_acknowedge=Instrument.control(
        "EC ?",
        "EC %i",
        """ An integer parameter enabling/disabling
            the command acknowledge mode.
        """,
        validator=strict_discrete_set,
        values=(0,1),
        get_process=lambda v:int(v.split("=")[-1])
    )
    end_of_line=Instrument.control(
        "EOL ?",
        "EOL %s",
        """ A string parameter indicating the
            end-of-line mode: `CR` or `CRLF`.
        """,
        validator=strict_discrete_set,
        values=("CR",
                "CRLF"),
        get_process=lambda v:v.split("=")[-1]
    )
    handshake_mode=Instrument.control(
        "HS ?",
        "%s",
        """ A string parameter indicating the handshake mode:
            `hard` (DTR/CTS),
            `soft` (XON/XOFF),
            `pause` (1s delay after line is sent),
            `cl` (Mettler Toledo CL mode), or
            `off`.
        """,
        validator=strict_discrete_set,
        values={"hard":"HS hard",
                "soft":"HS soft",
                "pause":"HS PAUSE",
                "cl":"HS CL",
                "off":"HS off",
                "factory default":"HS"},
        map_values=True,
        get_process=lambda v:"HS "(+v.split("=")[-1])
    )
    id=Instrument.measurement(
        "ID",
        "Transmit the device identification text."
    ) # TODO this needs to be read additional times to get all data
    mode_vibration_adapter=Instrument.control(
        "MI ?",
        "MI %s",
        """ A string parameter for the vibration adapter.
            Input string represents the type of vibration
            enviroment:
            `stable`,
            `normal`, or
            `unstable`.
        """,
        validator=strict_discrete_set,
        values={"stable":"1",
                "normal":"2",
                "unstable":"3"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    mode_process_adapter=Instrument.control(
        "ML ?",
        "ML %g",
        """ A string parameter for the weighing process adapter.
            Input string represents the adaptation type:
            `none`,
            `dispensing`,
            `universal`, or
            `absolute`.
        """,
        validator=strict_discrete_set,
        values={"none":"0",
                "dispensing":"1",
                "universal":"2",
                "absolute":"3"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    mode_stability_detection=Instrument.control(
        "MS ?",
        "MS %g",
        """ An integer parameter that selects the relative
            meauresment stability requirement for a given
            period. The period is based on the input value.
            Values range from 0 (off) to 7 (highest stability).
            The device factory default setting is 3.
        """,
        validator=truncated_range,
        values=[0,7],
        get_process=lambda v:int(v.split("=")[-1]),
        cast=int
    )
    mode_data_transmission=Instrument.control(
        "MT ?",
        "%s",
        """ A string parameter that modifies the data
            transmission mode. String values are:
            `stable`    - send only stable readings,
            `all`       - send all readings,
            `auto`      - automatically send readings,
            `continuous`- continuously send readings,
            `factory`   - return to factory default.
        """,
        validator=strict_discrete_set,
        values={"stable":"MT Stb",
                "all":"MT All",
                "auto":"MT Auto",
                "continuous":"MT Cont",
                "factory":"MT"},
        map_values=True,
        get_process=lambda v:"MT"+(v.split("=")[-1])
    )
    mode_autozero=Instrument.control(
        "MZ ?",
        "MZ %g",
        """ A string parameter that turns the
            autozero function `on` or `off`.
        """,
        validator=strict_discrete_set,
        values={"off":"0",
                "on":"1"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    range_select=Instrument.control(
        "RG ?",
        "%s",
        "A string parameter for the weighing range.",
        validator=strict_discrete_set,
        values={"coarse":"RG C",
                "fine":"RG F",
                "toggle":"RG"},
        map_values=True,
        get_process=lambda v:"RG "+(v.split("=")[-1])
    )
    key_restrict=Instrument.control(
        "RK ?",
        "RK %s",
        """ A string parameter that enables or disables
            the device keys. The door keys are not included
            in the keys controlled.
        """,
        validator=strict_discrete_set,
        values={"disable all":"00000000",
                "enable all":"11111111"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    door_state=Instrument.control(
        "WI ?",
        "WI %s",
        """ A string parameter that controls
            the motorized draft shield doors.
            Control options:
                `open`          - opens doors
                `right`         - opens right door
                `left`          - opens left door
                `close`         - closes doors
                `disable`       - disables door keys
                `enable`        - enables door keys
            Additional reply options:
                `intermediate`  - intermediate position
                `moving`        - doors are moving
        """,
        validator=strict_discrete_set,
        values={"open":"0",
                "right":"0 R",
                "left":"0 L",
                "close":"1",
                "disable":"D",
                "enable":"E",
                "intermediate":"2",
                "moving":"3"},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )

    def __init__(self,adapter,includeSCPI=False,**kwargs):
        super(MettlerToledoBDI, self).__init__(adapter,
        "Generic Mettler Toledo Bidirectional Data Interface Balance",
        includeSCPI=False,**kwargs)

        self.adapter.connection.timeout = kwargs.get('timeout', 60000)
    @property
    def calibrate(self):
        """ Manually intitate the calibration """
        self.write("CA")
    @property
    def config_reset_to_defaults(self):
        """ Sets all balance parameters, except for the serial
            interface parameters, to the factory setting.
        """
        self.write("CFD")
    @property
    def config_save_new_defaults(self):
        """ Save current configuration in the
            permanent device memory.
        """
        self.write("CFE")
    @property
    def break_interface(self):
        """ Cancel all balance setting changes
            effected via the remote interface.
            Command has similar effect as a
            physical break of the input line.
        """
        self.write("@")
    @property
    def abort(self):
        """ Aborts command execution. """
        _reply=self.ask(".")
        if _reply is "EL":
            raise VisaIOError("No command in progress capable of aborting.")
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
    def send_immediate_repeat(self,full_output=False):
        """ Cancel any existing commands and then
            repeatedly and send the immediate
            weighing results.

            :param full_output: A boolean parameter that enables output
                                of the device full output string. When `False`,
                                the numeric weighing value is returned.
        """
        pass # TODO:
    def send_stable_repeat(self,full_output=False):
        """ Cancel any existing commands and then
            repeatedly and send the stable weighing
            results.

            :param full_output: A boolean parameter that enables output
                                of the device full output string. When `False`,
                                the numeric weighing value is returned.
        """
        pass # TODO:
    def send_on_change(self,disable=False,threshold=None,full_output=False):
        """ Cancel any existing commands, then send
            the immediate unstable weighing result
            when the load changes by the threshold
            value, finally send the next stable
            weighing result.

            :param disable:     A boolean parameter that disables the
                                command at the device level.
            :param threshold:   A float parameter indcating the necessary
                                load change to trigger data transmission.
                                If None, is set to max between 12.5% of the
                                last stable weighing value and 0.01 g.
            :param full_output: A boolean parameter that enables output
                                of the device full output string. When `False`,
                                the numeric weighing value is returned.
        """
        if disable:
            self.write("SR 0")
        else:
            if threshold is None:
                self.write("SR")
            elif isinstance(threshold,float) or isinstance(threshold,int):
                if threshold<0.001:
                    threshold=0.001
                self.write("SR {}".format(threshold))
            _data_str=self.read()
            pass # TODO
    @property
    def tare(self):
        """ Tares the balance or switches it on again after a
            power failure. `timeout` is temporarily set to 60 s.
            Raises `VisaIOError` if device tare is not successful.
        """
        self.write("T")
    @property
    def clear(self):
        """ Clear the resource IO. """
        self.adapter.connection.clear()
    @property
    def display_clear(self):
        """ Clear displayed message from the balance panel. """
        self.write("D")
    @property
    def mode_reset(self):
        """ Returns the vibration adapter, weighing process
            adapter, stability indicator, AutoZero and the
            readout increment to the factory setting.
        """
        self.write("M")
