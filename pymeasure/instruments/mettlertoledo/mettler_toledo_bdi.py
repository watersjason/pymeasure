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
    auto_door=Instrument.control(
        "AD?",
        "AD %i",
        """ A string parameter that enables or disables
            the automatic draft shield operation.""",
        validators=strict_discrete_set,
        values={'on':1,'off':0},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    base=Instrument.setting(
        "B %f",
        "A float value subtracted from all future weighing results.",
        validators=truncated_range,
        values=[0,20]
    )
    calibration_mode=Instrument.control(
        "CA ?",
        "CA %s",
        """ A string parameter that enables the automatic calibration, disables
            the automatic calibration, sets the calibration mode to an external
            user calibration, or starts an internal calibration.""",
        validators=strict_discrete_set,
        values={'auto off':0, 'auto on':1, 'external':'U', 'internal':'T'},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    calibration_status=Instrument.measurement(
        "CA S",
        "A string parameter representing the current calibration status.",
        validators=strict_discrete_set,
        values={'idle':'CA=I',
                'waiting':'CA=W',
                'auto calibrate':'CA=CA',
                'manual calibrate':'CA=CX',
                'test running':'CA=CT'},
        map_values=True
    )
    config_unlock=Instrument.control(
        "CFG ?",
        "CFG %i",
        """ An integer parameter that allows access
            to reset the default configuration.""",
        validators=strict_discrete_set,
        values=(0,1),
        get_process=lambda v:v.split("=")[-1]
    )
    display_text=Instrument.setting(
        "D %s",
        "Display a message on the balance panel."
    )
    generate_sound=Instrument.setting(
        "%s",
        "Device generates a sound.",
        validators=strict_discrete_set,
        values={'suppress':'DB 0','short':'DB','long':'DB 1',
                'double':'DB 2','mixed':'DB 3',
                'termination':'DB C','error':'DB E'},
        map_values=True
    )
    display_status=Instrument.control(
        "DST ?",
        "DST %s",
        """ Control behavior of the status indicators for:
            vibration adapter (wave symbol),
            weighing process adapter (droplet symbol),
            and interface (I/O symbol).""",
        validators=strict_discrete_set,
        values={'clear':0,'keep':1,'temporary':'A'},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    dispaly_state=Instrument.setting(
        "DSX %s",
        """ A string parameter that selects active
            display if an auxiliary display is attached.""",
        validators=strict_discrete_set,
        values={'both':0,'main':1,'auxiliary':2},
        map_values=True
    )
    # skip the DeltaTrac display control
    # skip the DeltaTrac weigh in
    command_acknowedge=Instrument.control(
        "EC ?",
        "EC %i",
        "An integer parameter enabling/disabling the command acknowledge mode.",
        validators=strict_discrete_set,
        values=(0,1),
        get_process=lambda v:v.split("=")[-1]
    )
    end_of_line=Instrument.control(
        "EOL ?",
        "EOL %s",
        "A string parameter indicating the end-of-line mode: `CR` or `CRLF`.",
        validators=strict_discrete_set,
        values=('CR','CRLF'),
        get_process=lambda v:v.split("=")[-1]
    )
    handshake_mode=Instrument.control(
        "HS ?",
        "HS %s",
        """ A string parameter indicating the handshake mode:
            `hard` (DTR/CTS),
            `soft` (XON/XOFF),
            `pause` (1s delay after line is sent),
            `cl` (Mettler Toledo CL mode), or
            `off`.""",
        validators=strict_discrete_set,
        values={"hard":"hard","soft":"soft","pause":"PAUSE",
                "cl":"CL","off":"off","factory default":""},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    identify=Instrument.measurement(
        "ID",
        "Transmit the device identification text."
    )
    identify_extended=Instrument.command(
        "IDX",
        "ID %s",
        "A string parameter with the user-definable identification string."
    )
    mode_reset=Instrument.setting(
        "M",
        """ Returns the vibration adapter (wave), weighing process adapter
            (droplet), stability indicator (ASD), AutoZero (AZ) and the
            readout increment (d) to the factory setting."""
    )
    # skip the readout increment setting
    mode_vibration_adapter=Instrument.command(
        "MI ?",
        "MI %g",
        """ A string parameter for the vibration adapter. Input string
            represents the type of vibration enviroment:
            `stable`, `normal`, or `unstable`.""",
        validators=strict_discrete_set,
        values=("stable","normal","unstable"),
        get_process=lambda v:v.split("=")[-1]
    )
    mode_process_adapter=Instrument.command(
        "ML ?",
        "ML %g",
        """ A string parameter for the weighing process adapter. Input string
            represents the adaptation type:
            `none`, `dispensing`, `universal`, or `absolute`.""",
        validators=strict_discrete_set,
        values={"none":0,"dispensing":1,"universal":2,"absolute":3},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    mode_stability_detector=Instrument.command(
        "MS ?",
        "MS %g",
        """ TODO """,
        validators=strict_discrete_set,
        values=(0,1,2,3,4,5,6,7),
        get_process=lambda v:v.split("=")[-1]
    )
    mode_data_transmission=Instrument.command(
        "MT ?",
        "MT %s",
        """ A string parameter that modifies the data transmission mode. String
            values are:
            `stable`    - send only stable readings,
            `all`       - send all readings,
            `auto`      - automatically send readings,
            `continuous`- continuously send readings,
            `factory`   - return to factory default setting.""",
        validators=strict_discrete_set,
        values={"stable":"Stb","all":"All","auto":"Auto",
                "continuous":"Cont","factory":""},
        get_process=lambda v:v.split("=")[-1]
    )
    mode_autozero=Instrument.command(
        "MZ ?",
        "MZ %g",
        "A string parameter that turns the autozero function `on` or `off`.",
        validators=strict_discrete_set,
        values={"off":0,"on":1},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    )
    range_select=Instrument.command(
        "RG ?",
        "RG %s",
        "A string parameter for the weighing range.",
        validators=strict_discrete_set,
        values={"coarse":"C","fine":"F","toggle":""},
        map_values=True,
        get_process=lambda v:v.split("=")[-1]
    ) # TODO physical test, might require a set_process to strip whitespace

    def __init__(self,adapter,**kwargs):
        super(MettlerToledoBDI, self).__init__(adapter,
        "Generic Mettler Toledo Bidirectional Data Interface Balance",
        includeSCPI=False,**kwargs)

    @property
    def config_reset_to_defaults(self):
        """ Sets all balance parameters, except for the serial interface
            parameters, to the factory setting."""
        self.write("CFD")
    @property
    def config_save_new_defaults(self):
        """ Save current configuration in the permanent device memory. """
        self.write("CFE")
