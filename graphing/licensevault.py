#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# checkmk_jetbrains_licensevault - Jetbrains LicenseVault Agent and checks
#
# Copyright (C) 2025  Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cmk.graphing.v1 import graphs, metrics

metric_virtual_inuse = metrics.Metric(
    name='virtual_inuse',
    title=metrics.Title('Virtual in use'),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.DARK_BLUE,
)

graph_virtual_inuse = graphs.Graph(
    name='virtual_inuse',
    title=graphs.Title('License Usage'),
    minimal_range=graphs.MinimalRange(0, 1),
    compound_lines=[
        'virtual_inuse',
        metrics.Difference(
            graphs.Title("Virtual free"),
            metrics.Color.LIGHT_BLUE,
            minuend="virtual_total",
            subtrahend="virtual_inuse",
        ),
    ],
)
