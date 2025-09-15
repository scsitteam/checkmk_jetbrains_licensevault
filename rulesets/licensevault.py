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
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    Percentage,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition


def _lic_parameter_form(title):
    return CascadingSingleChoice(
        title=title,
        elements=[
            CascadingSingleChoiceElement(
                name='used',
                title=Title('Used licenses'),
                parameter_form=SimpleLevels(
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=InputHint(value=0),
                ),
            ),
            CascadingSingleChoiceElement(
                name='free',
                title=Title('Free licenses'),
                parameter_form=SimpleLevels(
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=InputHint(value=0),
                ),
            ),
            CascadingSingleChoiceElement(
                name='used_percent',
                title=Title('Used licenses in percent'),
                parameter_form=SimpleLevels(
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=InputHint(value=0),
                ),
            ),
        ],
    )


def _parameter_form_jetbrains_licensevault():
    return Dictionary(
        elements={
            'regular_upper': DictElement(
                parameter_form=_lic_parameter_form(
                    title=Title('Regular license usage limit'),
                ),
                required=False,
            ),
            'virtual_upper': DictElement(
                parameter_form=_lic_parameter_form(
                    title=Title('Virtual license usage limit'),
                ),
                required=False,
            ),
            'trueup_upper': DictElement(
                parameter_form=_lic_parameter_form(
                    title=Title('Postpaid license usage limit'),
                ),
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
