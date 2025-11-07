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

import pytest  # type: ignore[import]
from cmk.agent_based.v2 import (
    Result,
    Service,
    State,
    Metric,
)
from cmk_addons.plugins.jetbrains_licensevault.agent_based import licensevault

EXAMPLE_STRINGTABLE = [
    [
        '{"denials": [{"description": "Unable to find suitable license", "product_name": "SequenceDiagram Core", "product_version": "4.0", "reason": "CANCELLED", "timestamp": "2025-08-18T08:26:37.836075076Z", "user_hostname": "host.fqdn", "user_ip": "1.2.3.4", "username": "Alice"},'
        '{"description": "Unable to find suitable license", "product_name": "IntelliJ IDEA Ultimate", "product_version": "2024.3", "reason": "CANCELLED", "timestamp": "2025-08-18T09:26:37.836075076Z", "user_hostname": "host.fqdn", "user_ip": "1.2.3.4", "username": "Alice"},'
        '{"description": "Unable to find suitable license", "product_name": "IntelliJ IDEA Ultimate", "product_version": "2024.3", "reason": "CANCELLED", "timestamp": "2025-08-17T09:26:37.836075076Z", "user_hostname": "host.fqdn", "user_ip": "1.2.3.4", "username": "Alice"}],'
        '"licenseUsages": [{"code": "ALL", "displayName": "All Products Pack", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 3, "virtualTotal": 50}, '
        '{"code": "CL", "displayName": "CLion", "regularInUse": 3, "regularTotal": 10, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "DB", "displayName": "DataGrip", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 1, "trueUpTotal": 5, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "DS", "displayName": "DataSpell", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "DUL", "displayName": "dotUltimate", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "GO", "displayName": "GoLand", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "II", "displayName": "IntelliJ IDEA Ultimate", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "PC", "displayName": "PyCharm", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "PS", "displayName": "PhpStorm", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "RC", "displayName": "ReSharper C++", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "RD", "displayName": "Rider", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "RM", "displayName": "RubyMine", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "RR", "displayName": "RustRover", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "RS0", "displayName": "ReSharper", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}, '
        '{"code": "WS", "displayName": "WebStorm", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0}], "timestamp": "2025-08-18T10:26:37.836075076Z"}'],
]

EXAMPLE_SECTION = {
    "All Products Pack": {"code": "ALL", "displayName": "All Products Pack", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 3, "virtualTotal": 50, "denials": 0},
    "CLion": {"code": "CL", "displayName": "CLion", "regularInUse": 3, "regularTotal": 10, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "DataGrip": {"code": "DB", "displayName": "DataGrip", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 1, "trueUpTotal": 5, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "DataSpell": {"code": "DS", "displayName": "DataSpell", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "dotUltimate": {"code": "DUL", "displayName": "dotUltimate", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "GoLand": {"code": "GO", "displayName": "GoLand", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "IntelliJ IDEA Ultimate": {"code": "II", "displayName": "IntelliJ IDEA Ultimate", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 1},
    "PyCharm": {"code": "PC", "displayName": "PyCharm", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "PhpStorm": {"code": "PS", "displayName": "PhpStorm", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "ReSharper C++": {"code": "RC", "displayName": "ReSharper C++", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "Rider": {"code": "RD", "displayName": "Rider", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "RubyMine": {"code": "RM", "displayName": "RubyMine", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "RustRover": {"code": "RR", "displayName": "RustRover", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "ReSharper": {"code": "RS0", "displayName": "ReSharper", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0},
    "WebStorm": {"code": "WS", "displayName": "WebStorm", "regularInUse": 0, "regularTotal": 0, "trueUpInUse": 0, "trueUpTotal": 0, "virtualInUse": 0, "virtualTotal": 0, "denials": 0}
}


@pytest.mark.parametrize('string_table, result', [
    ([], None),
    (EXAMPLE_STRINGTABLE, EXAMPLE_SECTION),
])
def test_parse_jetbrains_licensevault(freezer, string_table, result):
    freezer.move_to('2025-08-18 10:27')
    assert licensevault.parse_jetbrains_licensevault(string_table) == result


@pytest.mark.parametrize('section, result', [
    (None, []),
    ({}, []),
    (EXAMPLE_SECTION, [Service(item='All Products Pack'), Service(item='CLion'), Service(item='DataGrip')]),
])
def test_discovery_jetbrains_licensevault(section, result):
    assert list(licensevault.discovery_jetbrains_licensevault(section)) == result


@pytest.mark.parametrize('item, params, result', [
    ('Unknown', {}, [
        Result(state=State.UNKNOWN, summary="License'Unknown' not found"),
    ]),
    ('All Products Pack', {}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, summary='Virtual in use: 3'),
        Metric('virtual_inuse', 3.0, boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('CLion', {}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, summary='Regular in use: 3'),
        Metric('regular_inuse', 3.0, boundaries=(0.0, 10.0)),
        Metric('regular_total', 10.0),
        Result(state=State.OK, notice='Virtual in use: 0'),
        Metric('virtual_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('virtual_total', 0.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('DataGrip', {}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, notice='Virtual in use: 0'),
        Metric('virtual_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('virtual_total', 0.0),
        Result(state=State.OK, summary='TrueUp in use: 1'),
        Metric('trueup_inuse', 1.0, boundaries=(0.0, 5.0)),
        Metric('trueup_total', 5.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('used', ('fixed', (40, 45)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, summary='Virtual in use: 3'),
        Metric('virtual_inuse', 3.0, levels=(40.0, 45.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('used', ('fixed', (1, 5)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.WARN, summary='Virtual in use: 3 (warn/crit at 1/5)'),
        Metric('virtual_inuse', 3.0, levels=(1.0, 5.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('used', ('fixed', (1, 2)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.CRIT, summary='Virtual in use: 3 (warn/crit at 1/2)'),
        Metric('virtual_inuse', 3.0, levels=(1.0, 2.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('free', ('fixed', (10, 5)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, summary='Virtual in use: 3'),
        Metric('virtual_inuse', 3.0, levels=(40.0, 45.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('free', ('fixed', (49, 45)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.WARN, summary='Virtual in use: 3 (warn/crit at 1/5)'),
        Metric('virtual_inuse', 3.0, levels=(1.0, 5.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('free', ('fixed', (49, 48)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.CRIT, summary='Virtual in use: 3 (warn/crit at 1/2)'),
        Metric('virtual_inuse', 3.0, levels=(1.0, 2.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('used_percent', ('fixed', (0.8, 0.9)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, summary='Virtual in use: 3'),
        Metric('virtual_inuse', 3.0, levels=(40.0, 45.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('used_percent', ('fixed', (0.02, 0.1)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.WARN, summary='Virtual in use: 3 (warn/crit at 1/5)'),
        Metric('virtual_inuse', 3.0, levels=(1.0, 5.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('All Products Pack', {'virtual_upper': ('used_percent', ('fixed', (0.02, 0.04)))}, [
        Result(state=State.OK, notice='Denials in 24H: 0'),
        Metric('denials_24h', 0.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.CRIT, summary='Virtual in use: 3 (warn/crit at 1/2)'),
        Metric('virtual_inuse', 3.0, levels=(1.0, 2.0), boundaries=(0.0, 50.0)),
        Metric('virtual_total', 50.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('IntelliJ IDEA Ultimate', {}, [
        Result(state=State.CRIT, notice='Denials in 24H: 1 (warn/crit at 1/1)'),
        Metric('denials_24h', 1.0, levels=(1.0, 1.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, notice='Virtual in use: 0'),
        Metric('virtual_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('virtual_total', 0.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
    ('IntelliJ IDEA Ultimate', {'denials': ('fixed', (5, 10))}, [
        Result(state=State.OK, notice='Denials in 24H: 1'),
        Metric('denials_24h', 1.0, levels=(5.0, 10.0), boundaries=(0.0, None)),
        Result(state=State.OK, notice='Regular in use: 0'),
        Metric('regular_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('regular_total', 0.0),
        Result(state=State.OK, notice='Virtual in use: 0'),
        Metric('virtual_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('virtual_total', 0.0),
        Result(state=State.OK, notice='TrueUp in use: 0'),
        Metric('trueup_inuse', 0.0, boundaries=(0.0, 0.0)),
        Metric('trueup_total', 0.0),
    ]),
])
def test_check_jetbrains_licensevault(item, params, result):
    assert list(licensevault.check_jetbrains_licensevault(item, params, EXAMPLE_SECTION)) == result
