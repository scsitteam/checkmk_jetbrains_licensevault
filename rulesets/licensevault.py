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

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition


def _parameter_form_jetbrains_licensevault():
    return Dictionary(
        elements={
            'virtual_upper': CascadingSingleChoice(
                title=Title("Virtual in use limit"),
                elements=[
                    CascadingSingleChoiceElement(
                        name="fixed", title=Title("Global")),
                    CascadingSingleChoiceElement(name="china", title=Title("China")),
                ],
                required=False,
            ),
        }
    )


rule_spec_jetbrains_licensevault = CheckParameters(
    name='jetbrains_licensevault',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_jetbrains_licensevault,
    title=Title('JetBrains LicenseVault check'),
    help_text=Help('This rule configures thresholds for JetBrains LicenseVault check.'),
    condition=HostAndItemCondition(item_title=Title('License')),
)
