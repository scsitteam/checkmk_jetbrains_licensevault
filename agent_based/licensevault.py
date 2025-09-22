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

import json

from typing import Any
from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
    Metric,
)


JSONSection = dict[str, Any] | None


def parse_jetbrains_licensevault(string_table: StringTable) -> JSONSection:
    if string_table:
        return {
            lic['displayName']: lic
            for lic in json.loads(string_table[0][0]).get('licenseUsages')
        }
    return None


agent_section_jetbrains_licensevault = AgentSection(
    name='jetbrains_licensevault',
    parse_function=parse_jetbrains_licensevault,
)


def discovery_jetbrains_licensevault(section: JSONSection | None) -> DiscoveryResult:
    if section is None:
        return
    for name, lic in section.items():
        if lic['regularTotal'] > 0 or lic['trueUpTotal'] > 0 or lic['virtualTotal'] > 0:
            yield Service(item=name)


def check_jetbrains_licensevault(
    item: str,
    params: dict,
    section: JSONSection | None,
) -> CheckResult:
    if item not in section:
        yield Result(state=State.UNKNOWN, summary=f"License'{item}' not found")
        return

    lic = section[item]

    if 'regular_upper' in params or lic.get('regularTotal', 0) > 0:
        levels_upper = params.get('regular_upper', None)
        match levels_upper:
            case ('used', level):
                levels_upper = level
            case ('free', ('fixed', (warn, crit))):
                levels_upper = ('fixed', (lic['regularTotal'] - warn, lic['regularTotal'] - crit))
            case ('used_percent', ('fixed', (warn, crit))):
                levels_upper = ('fixed', (lic['regularTotal'] * warn, lic['regularTotal'] * crit))
            case ('free', level):
                levels_upper = level
            case ('used_percent', level):
                levels_upper = level
        yield from check_levels(
            value=lic['regularInUse'],
            levels_upper=levels_upper,
            metric_name='regular_inuse',
            render_func=int,
            label="Regular in use",
            boundaries=(0, lic['regularTotal'])
        )
        yield Metric('regular_total', lic['regularTotal'])

    if 'virtual_upper' in params or lic.get('virtualTotal', 0) > 0:
        levels_upper = params.get('virtual_upper', None)
        match levels_upper:
            case ('used', level):
                levels_upper = level
            case ('free', ('fixed', (warn, crit))):
                levels_upper = ('fixed', (lic['virtualTotal'] - warn, lic['virtualTotal'] - crit))
            case ('used_percent', ('fixed', (warn, crit))):
                levels_upper = ('fixed', (lic['virtualTotal'] * warn, lic['virtualTotal'] * crit))
            case ('free', level):
                levels_upper = level
            case ('used_percent', level):
                levels_upper = level
        yield from check_levels(
            value=lic['virtualInUse'],
            levels_upper=levels_upper,
            metric_name='virtual_inuse',
            render_func=int,
            label="Virtual in use",
            boundaries=(0, lic['virtualTotal'])
        )
        yield Metric('virtual_total', lic['virtualTotal'])

    if 'trueup_upper' in params or lic.get('trueUpTotal', 0) > 0:
        levels_upper = params.get('trueup_upper', None)
        match levels_upper:
            case ('used', level):
                levels_upper = level
            case ('free', ('fixed', (warn, crit))):
                levels_upper = ('fixed', (lic['trueUpTotal'] - warn, lic['trueUpTotal'] - crit))
            case ('used_percent', ('fixed', (warn, crit))):
                levels_upper = ('fixed', (lic['trueUpTotal'] * warn, lic['trueUpTotal'] * crit))
            case ('free', level):
                levels_upper = level
            case ('used_percent', level):
                levels_upper = level
        yield from check_levels(
            value=lic['trueUpInUse'],
            levels_upper=levels_upper,
            metric_name='trueup_inuse',
            render_func=int,
            label="TrueUp in use",
            boundaries=(0, lic['trueUpTotal'])
        )
        yield Metric('trueup_total', lic['trueUpTotal'])


check_plugin_jetbrains_licensevault = CheckPlugin(
    name='jetbrains_licensevault',
    service_name='LicenseVault %s',
    discovery_function=discovery_jetbrains_licensevault,
    check_function=check_jetbrains_licensevault,
    check_default_parameters={},
    check_ruleset_name='jetbrains_licensevault',
)
