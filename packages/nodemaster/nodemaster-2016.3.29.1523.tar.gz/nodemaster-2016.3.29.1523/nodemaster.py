#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# nodemaster                                                                   #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides node control utilities.                                #
#                                                                              #
# 2014 Will Breaden Madden, w.bm@cern.ch                                       #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

name    = "nodemaster"
version = "2016-03-29T1523Z"

import os
import subprocess

def launch_tmux(
    commands = None
    ):
    configuration =\
    """
    set -g set-remain-on-exit on
    new -s "nodemaster"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 5000
    ## mouse mode
    set -g mode-mouse on
    set -g mouse-select-pane on
    set -g mouse-select-window on
    set -g mouse-resize-pane on # resize panes with mouse (drag borders)
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    """
    for command in range(1, len(commands)):
        configuration += "\nsplit-window -v\nselect-layout even-vertical"
    for index, command in enumerate(commands):
        configuration += "\nselect-pane -t {index}".format(
            index = index
        )
        configuration += "\nsend-keys '{command}' Enter".format(
            command = command
        )
    configuration += "\nset -g set-remain-on-exit off"
    command = \
        "configurationtmux=\"$(mktemp)\" && { echo \"" +\
        configuration                                  +\
        "\" > \"${configurationtmux}\"; "              +\
        "tmux"                                         +\
        " -f \"${configurationtmux}\" attach; "        +\
        "unlink \"${configurationtmux}\"; }"
    os.system(command)

def working_nodes_LXPLUS(
    number = None
    ):
    nodes = [
        #"lxplus0000.cern.ch",
        "lxplus0001.cern.ch",
        #"lxplus0002.cern.ch",
        #"lxplus0003.cern.ch",
        "lxplus0004.cern.ch",
        #"lxplus0005.cern.ch",
        #"lxplus0006.cern.ch",
        #"lxplus0007.cern.ch",
        "lxplus0008.cern.ch",
        "lxplus0009.cern.ch",
        "lxplus0010.cern.ch",
        "lxplus0011.cern.ch",
        "lxplus0012.cern.ch",
        "lxplus0013.cern.ch",
        "lxplus0014.cern.ch",
        "lxplus0015.cern.ch",
        "lxplus0016.cern.ch",
        "lxplus0017.cern.ch",
        "lxplus0018.cern.ch",
        "lxplus0019.cern.ch",
        "lxplus0020.cern.ch",
        "lxplus0021.cern.ch",
        "lxplus0022.cern.ch",
        "lxplus0023.cern.ch",
        "lxplus0024.cern.ch",
        "lxplus0025.cern.ch",
        "lxplus0026.cern.ch",
        "lxplus0027.cern.ch",
        "lxplus0028.cern.ch",
        "lxplus0029.cern.ch",
        "lxplus0030.cern.ch",
        "lxplus0031.cern.ch",
        "lxplus0032.cern.ch",
        "lxplus0033.cern.ch",
        "lxplus0034.cern.ch",
        "lxplus0035.cern.ch",
        "lxplus0036.cern.ch",
        "lxplus0037.cern.ch",
        "lxplus0038.cern.ch",
        "lxplus0039.cern.ch",
        "lxplus0040.cern.ch",
        "lxplus0041.cern.ch",
        "lxplus0042.cern.ch",
        "lxplus0043.cern.ch",
        "lxplus0044.cern.ch",
        "lxplus0045.cern.ch",
        "lxplus0046.cern.ch",
        "lxplus0047.cern.ch",
        "lxplus0048.cern.ch",
        "lxplus0049.cern.ch",
        "lxplus0050.cern.ch",
        "lxplus0051.cern.ch",
        "lxplus0052.cern.ch",
        "lxplus0053.cern.ch",
        "lxplus0054.cern.ch",
        "lxplus0055.cern.ch",
        "lxplus0056.cern.ch",
        "lxplus0057.cern.ch",
        "lxplus0058.cern.ch",
        "lxplus0059.cern.ch",
        "lxplus0060.cern.ch",
        "lxplus0061.cern.ch",
        "lxplus0062.cern.ch",
        "lxplus0063.cern.ch",
        "lxplus0064.cern.ch",
        "lxplus0065.cern.ch",
        "lxplus0066.cern.ch",
        "lxplus0067.cern.ch",
        "lxplus0068.cern.ch",
        "lxplus0069.cern.ch",
        "lxplus0070.cern.ch",
        "lxplus0072.cern.ch",
        "lxplus0073.cern.ch",
        "lxplus0074.cern.ch",
        "lxplus0075.cern.ch",
        "lxplus0076.cern.ch",
        "lxplus0077.cern.ch",
        "lxplus0078.cern.ch",
        "lxplus0079.cern.ch",
        "lxplus0080.cern.ch",
        "lxplus0081.cern.ch",
        "lxplus0082.cern.ch",
        "lxplus0083.cern.ch",
        "lxplus0084.cern.ch",
        "lxplus0085.cern.ch",
        "lxplus0086.cern.ch",
        "lxplus0087.cern.ch",
        "lxplus0088.cern.ch",
        "lxplus0089.cern.ch",
        "lxplus0090.cern.ch",
        "lxplus0091.cern.ch",
        "lxplus0092.cern.ch",
        "lxplus0093.cern.ch",
        "lxplus0094.cern.ch",
        "lxplus0095.cern.ch",
        "lxplus0096.cern.ch",
        "lxplus0097.cern.ch",
        "lxplus0098.cern.ch",
        "lxplus0099.cern.ch",
        "lxplus0100.cern.ch",
        "lxplus0101.cern.ch",
        "lxplus0102.cern.ch",
        "lxplus0103.cern.ch",
        "lxplus0103.cern.ch",
        "lxplus0104.cern.ch",
        "lxplus0105.cern.ch",
        "lxplus0106.cern.ch",
        "lxplus0107.cern.ch",
        "lxplus0108.cern.ch",
        "lxplus0109.cern.ch",
        "lxplus0110.cern.ch",
        "lxplus0111.cern.ch",
        "lxplus0112.cern.ch",
        "lxplus0113.cern.ch",
        "lxplus0114.cern.ch",
        "lxplus0141.cern.ch",
        "lxplus0148.cern.ch",
        "lxplus0159.cern.ch",
        "lxplus0233.cern.ch"
    ]
    working_nodes = []
    for node in nodes:
        #log.debug("check node {node}".format(node = node))
        return_code = subprocess.call([
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            node,
            "uptime"
        ])
        #log.debug("return code: {return_code}".format(
        #    return_code = return_code
        #))
        if return_code == 0:
            working_nodes.append(node)
        if len(working_nodes) == number:
            return working_nodes
    return working_nodes

def working_nodes_PPELX(
    number = None
    ):
    nodes = [
        #"ppepc000",
        #"ppepc001",
        #"ppepc002",
        #"ppepc003",
        #"ppepc004",
        #"ppepc005",
        #"ppepc006",
        #"ppepc007",
        #"ppepc008",
        #"ppepc009",
        #"ppepc010",
        #"ppepc011",
        #"ppepc012",
        #"ppepc013",
        #"ppepc014",
        #"ppepc015",
        #"ppepc016",
        #"ppepc017",
        #"ppepc018",
        #"ppepc019",
        #"ppepc020",
        #"ppepc021",
        #"ppepc022",
        #"ppepc023",
        #"ppepc024",
        #"ppepc025",
        #"ppepc026",
        #"ppepc027",
        #"ppepc028",
        #"ppepc029",
        #"ppepc030",
        #"ppepc031",
        #"ppepc032",
        #"ppepc033",
        #"ppepc034",
        #"ppepc035",
        #"ppepc036",
        #"ppepc037",
        #"ppepc038",
        #"ppepc039",
        #"ppepc040",
        #"ppepc041",
        #"ppepc042",
        #"ppepc043",
        #"ppepc044",
        #"ppepc045",
        #"ppepc046",
        #"ppepc047",
        #"ppepc048",
        #"ppepc049",
        #"ppepc050",
        #"ppepc051",
        #"ppepc052",
        #"ppepc053",
        #"ppepc054",
        #"ppepc055",
        #"ppepc056",
        #"ppepc057",
        #"ppepc058",
        #"ppepc059",
        #"ppepc060",
        #"ppepc061",
        #"ppepc062",
        #"ppepc063",
        #"ppepc064",
        #"ppepc065",
        #"ppepc066",
        #"ppepc067",
        #"ppepc068",
        #"ppepc069",
        #"ppepc070",
        #"ppepc071",
        #"ppepc072",
        #"ppepc073",
        #"ppepc074",
        #"ppepc075",
        #"ppepc076",
        #"ppepc077",
        #"ppepc078",
        #"ppepc079",
        #"ppepc080",
        #"ppepc081",
        #"ppepc082",
        #"ppepc083",
        #"ppepc084",
        #"ppepc085",
        #"ppepc086",
        #"ppepc087",
        #"ppepc088",
        #"ppepc089",
        #"ppepc090",
        #"ppepc091",
        #"ppepc092",
        #"ppepc093",
        #"ppepc094",
        #"ppepc095",
        #"ppepc096",
        #"ppepc097",
        #"ppepc098",
        #"ppepc099",
        #"ppepc100",
        #"ppepc101",
        #"ppepc102",
        "ppepc103",
        "ppepc104",
        #"ppepc105",
        "ppepc106",
        #"ppepc107",
        #"ppepc108",
        #"ppepc109",
        #"ppepc110",
        #"ppepc111",
        #"ppepc112",
        #"ppepc113",
        #"ppepc114",
        #"ppepc115",
        #"ppepc116",
        "ppepc117", # signin
        #"ppepc118",
        #"ppepc119",
        #"ppepc120",
        "ppepc121",
        "ppepc122",
        "ppepc123",
        #"ppepc124",
        #"ppepc125",
        #"ppepc126",
        "ppepc127",
        "ppepc128",
        #"ppepc129",
        #"ppepc130",
        #"ppepc131",
        #"ppepc132",
        #"ppepc133",
        #"ppepc134",
        #"ppepc135",
        #"ppepc136",
        #"ppepc137",
        #"ppepc138",
        #"ppepc139",
        #"ppepc140",
        #"ppepc141",
        #"ppepc142",
        #"ppepc143",
        #"ppepc144",
        #"ppepc145",
        #"ppepc146",
        #"ppepc147",
        #"ppepc148",
        #"ppepc149",
        #"ppepc150",
        "ppepc151",
        "ppepc152",
        "ppepc153",
        #"ppepc154",
        "ppepc155",
        "ppepc156",
        "ppepc157",
        "ppepc158",
        "ppepc159",
        "ppepc160",
        "ppepc161",
        "ppepc162",
        "ppepc163",
        "ppepc164",
        "ppepc165",
        "ppepc166",
        "ppepc167",
        "ppepc168",
        "ppepc169",
        "ppepc170",
        "ppepc171",
        "ppepc172",
        "ppepc173",
        "ppepc174",
        "ppepc175",
        "ppepc176",
        "ppepc177",
        "ppepc178",
        "ppepc179",
        "ppepc180",
        "ppepc181",
        "ppepc182",
        "ppepc183",
        "ppepc184",
        "ppepc185",
        "ppepc186",
        "ppepc187",
        "ppepc188",
        "ppepc189",
        "ppepc190",
        "ppepc191",
        "ppepc192",
        "ppepc193",
        "ppepc194",
        "ppepc195",
        "ppepc196",
        "ppepc197",
        "ppepc198",
        "ppepc199",
        "ppepc200",
        "ppepc201",
        "ppepc202",
        "ppepc203",
        "ppepc204",
        "ppepc205",
        "ppepc206",
        "ppepc207",
        "ppepc208",
        "ppepc209",
        "ppepc210",
        "ppepc211",
        "ppepc212",
        "ppepc213",
        "ppepc214",
        "ppepc215",
        "ppepc216",
        "ppepc217",
        "ppepc218",
        "ppepc219",
        "ppepc220",
        "ppepc221",
        "ppepc222",
        "ppepc223",
        "ppepc224",
        "ppepc225",
        "ppepc226",
        "ppepc227",
        "ppepc228",
        "ppepc229",
        "ppepc230",
        "ppepc231",
        "ppepc232",
        "ppepc233",
        "ppepc234",
        "ppepc235",
        "ppepc236",
        "ppepc237",
        "ppepc238",
        "ppepc239",
        "ppepc240",
        "ppepc241",
        "ppepc242",
        "ppepc243",
        "ppepc244",
        "ppepc245",
        "ppepc246",
        "ppepc247",
        "ppepc248",
        "ppepc249",
        "ppepc250",
        "ppepc251",
        "ppepc252",
        "ppepc253",
        "ppepc254",
        "ppepc255",
        "ppepc256",
        "ppepc257",
        "ppepc258",
        "ppepc259",
        "ppepc260",
        "ppepc261",
        "ppepc262",
        "ppepc263",
        "ppepc264",
        "ppepc265",
        "ppepc266",
        "ppepc267",
        "ppepc268",
        "ppepc269",
        "ppepc270",
        "ppepc271",
        "ppepc272",
        "ppepc273",
        "ppepc274",
        "ppepc275",
        "ppepc276",
        "ppepc277",
        "ppepc278",
        "ppepc279",
        "ppepc280",
        "ppepc281",
        "ppepc282",
        "ppepc283",
        "ppepc284",
        "ppepc285",
        "ppepc286",
        "ppepc287",
        "ppepc288",
        "ppepc289",
        "ppepc290",
        "ppepc291",
        "ppepc292",
        "ppepc293",
        "ppepc294",
        "ppepc295",
        "ppepc296",
        "ppepc297",
        "ppepc298",
        "ppepc299",
        "ppepc300"
    ]
    working_nodes = []
    for node in nodes:
        #log.debug("check node {node}".format(node = node))
        return_code = subprocess.call([
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            node,
            "uptime"
        ])
        #log.debug("return code: {return_code}".format(
        #    return_code = return_code
        #))
        if return_code == 0:
            working_nodes.append(node)
        if len(working_nodes) == number:
            return working_nodes
    return working_nodes
